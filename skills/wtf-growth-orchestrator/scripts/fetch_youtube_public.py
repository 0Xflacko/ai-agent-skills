#!/usr/bin/env python3
"""Fetch public YouTube channel and feed signals for snapshot use."""

from __future__ import annotations

import argparse
import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fetch_text(url: str, timeout: int) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_compact_int(raw: str) -> int:
    value = (raw or "").strip().replace(",", "")
    if not value:
        return 0
    value = value.replace("subscribers", "").replace("subscriber", "").strip()
    mult = 1
    suffix = value[-1].lower() if value else ""
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


def parse_channel_html(html: str, handle: str) -> dict[str, Any]:
    channel_id_match = re.search(r'"channelId":"([^"]+)"', html)
    if not channel_id_match:
        channel_id_match = re.search(r'\\"channelId\\":\\"([^\\"]+)\\"', html)
    if not channel_id_match:
        channel_id_match = re.search(r'"browseId":"(UC[^"]+)"', html)
    if not channel_id_match:
        channel_id_match = re.search(r'\\"browseId\\":\\"(UC[^\\"]+)\\"', html)
    title_match = re.search(r"<title>(.*?)</title>", html, flags=re.S | re.I)
    subs_match = re.search(r'"subscriberCountText":\{"simpleText":"([^"]+)"', html)
    if not subs_match:
        subs_match = re.search(r'"subscriberCountText".*?"label":"([^"]+)"', html)
    if not subs_match:
        subs_match = re.search(r'\\"subscriberCountText\\".*?\\"label\\":\\"([^\\"]+)\\"', html)

    channel_id = channel_id_match.group(1) if channel_id_match else ""
    title = title_match.group(1).strip() if title_match else handle
    followers = parse_compact_int(subs_match.group(1)) if subs_match else None

    return {
        "channel_id": channel_id,
        "title": title,
        "followers": followers,
    }


def parse_feed(feed_xml: str, handle: str, post_limit: int) -> list[dict[str, Any]]:
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "yt": "http://www.youtube.com/xml/schemas/2015",
    }
    root = ET.fromstring(feed_xml)
    posts: list[dict[str, Any]] = []

    for entry in root.findall("atom:entry", ns)[:post_limit]:
        video_id = entry.findtext("yt:videoId", default="", namespaces=ns)
        title = entry.findtext("atom:title", default="", namespaces=ns)
        published = entry.findtext("atom:published", default=now_utc(), namespaces=ns)

        link_el = entry.find("atom:link", ns)
        link = link_el.attrib.get("href", "") if link_el is not None else ""

        posts.append(
            {
                "id": video_id,
                "account": handle,
                "platform": "youtube",
                "created_at_utc": published,
                "text": title,
                "media_type": "video",
                "likes": 0,
                "comments": 0,
                "reposts": 0,
                "views": 0,
                "link": link,
            }
        )

    return posts


def collect_handle(handle: str, post_limit: int, timeout: int) -> tuple[dict[str, Any] | None, list[dict[str, Any]], str | None, str]:
    normalized = handle if handle.startswith("@") else f"@{handle}"
    channel_url = f"https://www.youtube.com/{normalized}"

    try:
        html = fetch_text(channel_url, timeout)
    except (HTTPError, URLError, TimeoutError) as exc:
        return None, [], f"{normalized}: failed to fetch channel page: {exc}", "low"

    meta = parse_channel_html(html, normalized)
    channel_id = meta.get("channel_id", "")
    posts: list[dict[str, Any]] = []

    if channel_id:
        feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        try:
            feed_xml = fetch_text(feed_url, timeout)
            posts = parse_feed(feed_xml, normalized, post_limit)
        except (HTTPError, URLError, TimeoutError, ET.ParseError) as exc:
            return (
                {
                    "platform": "youtube",
                    "account": normalized,
                    "followers": meta.get("followers"),
                    "following": None,
                    "total_posts": None,
                    "verified": None,
                    "captured_at_utc": now_utc(),
                    "source": channel_url,
                    "channel_id": channel_id,
                    "channel_title": meta.get("title"),
                },
                [],
                f"{normalized}: feed fetch/parse failed: {exc}",
                "medium",
            )

    profile = {
        "platform": "youtube",
        "account": normalized,
        "followers": meta.get("followers"),
        "following": None,
        "total_posts": len(posts) if posts else None,
        "verified": None,
        "captured_at_utc": now_utc(),
        "source": channel_url,
        "channel_id": channel_id,
        "channel_title": meta.get("title"),
    }

    quality = "high" if posts else "medium"
    if not channel_id:
        quality = "low"

    return profile, posts, None, quality


def as_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# YouTube Snapshot",
        "",
        f"- Captured: {payload['captured_at_utc']}",
        f"- Source quality: {payload['source_quality']}",
        "",
        "## Channels",
        "",
        "| Handle | Channel ID | Followers |",
        "|---|---|---:|",
    ]

    for p in payload.get("profiles", []):
        followers = p.get("followers") if p.get("followers") is not None else "unknown"
        lines.append(f"| {p.get('account')} | {p.get('channel_id', '')} | {followers} |")

    lines.extend(["", "## Recent Videos", "", "| Handle | Video ID | Published | Title |", "|---|---|---|---|"])
    for post in payload.get("posts", []):
        title = (post.get("text") or "").replace("|", "\\|")
        lines.append(f"| {post.get('account')} | {post.get('id')} | {post.get('created_at_utc')} | {title[:120]} |")

    if payload.get("errors"):
        lines.extend(["", "## Errors", ""])
        for err in payload["errors"]:
            lines.append(f"- {err}")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch public YouTube channel/feed signals.")
    parser.add_argument("--handles", default="@WTFLeagues", help="Comma-separated channel handles")
    parser.add_argument("--post-limit", type=int, default=10, help="Recent feed entries per channel")
    parser.add_argument("--timeout", type=int, default=20, help="HTTP timeout in seconds")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args()

    handles = [h.strip() for h in args.handles.split(",") if h.strip()]

    payload: dict[str, Any] = {
        "platform": "youtube",
        "source": "youtube-public-channel-and-feed",
        "captured_at_utc": now_utc(),
        "source_quality": "low",
        "profiles": [],
        "posts": [],
        "errors": [],
    }

    qualities: list[str] = []
    for handle in handles:
        profile, posts, error, quality = collect_handle(handle, args.post_limit, args.timeout)
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
