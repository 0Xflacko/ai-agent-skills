#!/usr/bin/env python3
"""Fetch public Instagram profile and post signals via web profile endpoint."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)
IG_APP_ID = "936619743392459"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ts_to_iso(ts: int | None) -> str:
    if not ts:
        return now_utc()
    return datetime.fromtimestamp(ts, tz=timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fetch_json(url: str, timeout: int) -> dict[str, Any]:
    req = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "x-ig-app-id": IG_APP_ID,
            "Accept": "application/json",
        },
    )
    with urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8", errors="replace")
    return json.loads(body)


def parse_post(node: dict[str, Any], account: str) -> dict[str, Any]:
    shortcode = node.get("shortcode", "")
    product_type = node.get("product_type", "")
    if shortcode:
        path = "reel" if product_type == "clips" else "p"
        link = f"https://www.instagram.com/{path}/{shortcode}/"
    else:
        link = f"https://www.instagram.com/{account}/"

    caption_edges = node.get("edge_media_to_caption", {}).get("edges", [])
    caption = ""
    if caption_edges:
        caption = caption_edges[0].get("node", {}).get("text", "") or ""

    return {
        "id": str(node.get("id", "")),
        "account": account,
        "platform": "instagram",
        "created_at_utc": ts_to_iso(node.get("taken_at_timestamp")),
        "text": caption,
        "media_type": "video" if node.get("is_video") else "image",
        "likes": int(node.get("edge_liked_by", {}).get("count", 0) or 0),
        "comments": int(node.get("edge_media_to_comment", {}).get("count", 0) or 0),
        "reposts": 0,
        "views": int(node.get("video_view_count", 0) or 0),
        "link": link,
    }


def collect_username(username: str, post_limit: int, timeout: int) -> tuple[dict[str, Any] | None, list[dict[str, Any]], str | None, str]:
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={quote(username)}"
    try:
        payload = fetch_json(url, timeout=timeout)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        return None, [], f"{username}: failed to fetch profile: {exc}", "low"

    user = payload.get("data", {}).get("user") or {}
    if not user:
        return None, [], f"{username}: empty user payload", "low"

    profile = {
        "platform": "instagram",
        "account": username,
        "followers": int(user.get("edge_followed_by", {}).get("count", 0) or 0),
        "following": int(user.get("edge_follow", {}).get("count", 0) or 0),
        "total_posts": int(user.get("edge_owner_to_timeline_media", {}).get("count", 0) or 0),
        "verified": bool(user.get("is_verified", False)),
        "captured_at_utc": now_utc(),
        "source": url,
    }

    edges = user.get("edge_owner_to_timeline_media", {}).get("edges", [])
    posts = [parse_post(edge.get("node", {}), username) for edge in edges[:post_limit]]

    quality = "high"
    if not posts:
        quality = "medium"

    return profile, posts, None, quality


def as_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Instagram Snapshot",
        "",
        f"- Captured: {payload['captured_at_utc']}",
        f"- Source quality: {payload['source_quality']}",
        "",
        "## Profiles",
        "",
        "| Account | Followers | Following | Posts | Verified |",
        "|---|---:|---:|---:|---|",
    ]

    for p in payload.get("profiles", []):
        lines.append(
            f"| @{p['account']} | {p['followers']} | {p['following']} | {p['total_posts']} | {str(p['verified']).lower()} |"
        )

    lines.extend(["", "## Recent Posts", "", "| Account | ID | Likes | Comments | Views | Text |", "|---|---|---:|---:|---:|---|"])
    for post in payload.get("posts", []):
        text = (post.get("text") or "").replace("|", "\\|")
        lines.append(
            f"| @{post['account']} | {post['id']} | {post['likes']} | {post['comments']} | {post['views']} | {text[:120]} |"
        )

    if payload.get("errors"):
        lines.extend(["", "## Errors", ""])
        for err in payload["errors"]:
            lines.append(f"- {err}")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch public Instagram profile info.")
    parser.add_argument("--usernames", default="wtfleagues,wtfbulletin", help="Comma-separated Instagram usernames")
    parser.add_argument("--post-limit", type=int, default=12, help="Recent posts per account")
    parser.add_argument("--timeout", type=int, default=20, help="HTTP timeout in seconds")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args()

    usernames = [u.strip().lstrip("@") for u in args.usernames.split(",") if u.strip()]

    payload: dict[str, Any] = {
        "platform": "instagram",
        "source": "instagram-web-profile-info",
        "captured_at_utc": now_utc(),
        "source_quality": "low",
        "profiles": [],
        "posts": [],
        "errors": [],
    }

    qualities: list[str] = []
    for username in usernames:
        profile, posts, error, quality = collect_username(username, args.post_limit, args.timeout)
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
