#!/usr/bin/env python3
"""Fetch public X profile and post signals from TwStalker mirrors.

This is intentionally best-effort and should be treated as approximate.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)
TWITTER_EPOCH_MS = 1288834974657


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_compact_int(raw: str) -> int:
    value = (raw or "").strip().replace(",", "")
    if not value:
        return 0
    mult = 1
    suffix = value[-1].lower()
    if suffix in {"k", "m", "b"}:
        if suffix == "k":
            mult = 1_000
        elif suffix == "m":
            mult = 1_000_000
        elif suffix == "b":
            mult = 1_000_000_000
        value = value[:-1]
    try:
        return int(float(value) * mult)
    except ValueError:
        return 0


def strip_html(text: str) -> str:
    cleaned = re.sub(r"<a [^>]*>(.*?)</a>", r"\1", text, flags=re.S)
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()


def status_id_to_utc(status_id: str) -> str:
    try:
        status_num = int(status_id)
        timestamp_ms = (status_num >> 22) + TWITTER_EPOCH_MS
        dt = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
        return dt.replace(microsecond=0).isoformat().replace("+00:00", "Z")
    except Exception:
        return now_utc()


def fetch_html(url: str, timeout: int) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception:
        # TwStalker frequently blocks urllib user agents while allowing curl-like requests.
        cmd = [
            "curl",
            "-L",
            "-A",
            USER_AGENT,
            "-s",
            "--max-time",
            str(timeout),
            url,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode != 0 or not result.stdout.strip():
            raise URLError(f"curl fallback failed (code={result.returncode}) for {url}")
        return result.stdout


def parse_counters(html: str) -> dict[str, int]:
    pairs = re.findall(
        r'<div class="dscun-txt">\s*([^<]+)\s*</div>\s*<div class="dscun-numbr">\s*([^<]+)\s*</div>',
        html,
        flags=re.I,
    )
    out: dict[str, int] = {}
    for label, val in pairs:
        out[label.strip().lower()] = parse_compact_int(val)
    return out


def parse_verified(html: str, account: str) -> bool:
    heading_match = re.search(
        rf"<h4>(.*?)<span>\s*@{re.escape(account)}\s*</span>.*?</h4>",
        html,
        flags=re.S | re.I,
    )
    if not heading_match:
        return False
    return 'data-testid="icon-verified"' in heading_match.group(0)


def parse_posts(html: str, account: str, post_limit: int) -> list[dict[str, Any]]:
    posts: list[dict[str, Any]] = []
    segments = html.split('<div class="activity-posts">')[1:]

    for seg in segments:
        status_match = re.search(rf'href="/{re.escape(account)}/status/(\d+)">([^<]+)</a>', seg, flags=re.I)
        if not status_match:
            continue
        status_id, time_label = status_match.group(1), status_match.group(2).strip()

        text_match = re.search(r'<div class="activity-descp">\s*<p>(.*?)</p>', seg, flags=re.S | re.I)
        text = strip_html(text_match.group(1)) if text_match else ""

        nums = re.findall(r"<span><ins></ins>\s*([^<\s]+)\s*</span>", seg)
        while len(nums) < 4:
            nums.append("0")

        comments = parse_compact_int(nums[0])
        reposts = parse_compact_int(nums[1])
        likes = parse_compact_int(nums[2])
        views = parse_compact_int(nums[3])

        media_type = "text"
        lowered = seg.lower()
        if "video" in lowered or "amplify_video_thumb" in lowered or "tweet_video" in lowered:
            media_type = "video"
        elif "<img" in lowered:
            media_type = "image"

        posts.append(
            {
                "id": status_id,
                "account": account,
                "platform": "x",
                "created_at_utc": status_id_to_utc(status_id),
                "published_label": time_label,
                "text": text,
                "media_type": media_type,
                "likes": likes,
                "comments": comments,
                "reposts": reposts,
                "views": views,
                "link": f"https://x.com/{account}/status/{status_id}",
            }
        )

        if len(posts) >= post_limit:
            break

    return posts


def collect_account(base_url: str, account: str, post_limit: int, timeout: int) -> tuple[dict[str, Any] | None, list[dict[str, Any]], str | None, str]:
    url = f"{base_url.rstrip('/')}/{account}"
    try:
        html = fetch_html(url, timeout=timeout)
    except (HTTPError, URLError, TimeoutError) as exc:
        return None, [], f"{account}: failed to fetch {url}: {exc}", "low"

    counters = parse_counters(html)
    posts = parse_posts(html, account, post_limit)

    profile = {
        "platform": "x",
        "account": account,
        "followers": counters.get("followers", 0),
        "following": counters.get("following", 0),
        "total_posts": counters.get("tweets", 0),
        "verified": parse_verified(html, account),
        "captured_at_utc": now_utc(),
        "source": url,
    }

    quality = "high"
    if profile["followers"] == 0 and profile["total_posts"] == 0:
        quality = "medium" if posts else "low"
    elif not posts:
        quality = "medium"

    return profile, posts, None, quality


def as_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# X Snapshot (TwStalker)",
        "",
        f"- Captured: {payload['captured_at_utc']}",
        f"- Source quality: {payload['source_quality']}",
        "",
        "## Profiles",
        "",
        "| Account | Followers | Following | Tweets | Verified |",
        "|---|---:|---:|---:|---|",
    ]
    for p in payload.get("profiles", []):
        lines.append(
            f"| @{p['account']} | {p['followers']} | {p['following']} | {p['total_posts']} | {str(p['verified']).lower()} |"
        )

    lines.extend(["", "## Recent Posts", "", "| Account | ID | Likes | Comments | Reposts | Views | Text |", "|---|---|---:|---:|---:|---:|---|"])
    for post in payload.get("posts", []):
        text = (post.get("text") or "").replace("|", "\\|")
        lines.append(
            f"| @{post['account']} | {post['id']} | {post['likes']} | {post['comments']} | {post['reposts']} | {post['views']} | {text[:120]} |"
        )

    if payload.get("errors"):
        lines.extend(["", "## Errors", ""])
        for err in payload["errors"]:
            lines.append(f"- {err}")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch approximate X metrics from TwStalker mirrors.")
    parser.add_argument("--accounts", default="PLAYWTFGAMES,WTFLeagues", help="Comma-separated X handles")
    parser.add_argument("--base-url", default="https://ww.twstalker.com", help="TwStalker base URL")
    parser.add_argument("--post-limit", type=int, default=10, help="Recent posts per account")
    parser.add_argument("--timeout", type=int, default=20, help="HTTP timeout in seconds")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args()

    accounts = [a.strip().lstrip("@") for a in args.accounts.split(",") if a.strip()]

    payload: dict[str, Any] = {
        "platform": "x",
        "source": "twstalker",
        "captured_at_utc": now_utc(),
        "source_quality": "low",
        "profiles": [],
        "posts": [],
        "errors": [],
        "notes": "Approximate metrics from public mirror infrastructure.",
    }

    qualities: list[str] = []
    for account in accounts:
        profile, posts, error, quality = collect_account(args.base_url, account, args.post_limit, args.timeout)
        qualities.append(quality)
        if profile:
            payload["profiles"].append(profile)
        payload["posts"].extend(posts)
        if error:
            payload["errors"].append(error)

    if qualities and all(q == "high" for q in qualities) and not payload["errors"]:
        payload["source_quality"] = "high"
    elif payload["profiles"] or payload["posts"]:
        payload["source_quality"] = "medium"
    else:
        payload["source_quality"] = "low"

    if args.format == "markdown":
        print(as_markdown(payload))
    else:
        print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
