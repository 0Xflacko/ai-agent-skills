#!/usr/bin/env python3
"""Build a reach-first cross-platform snapshot for WTF growth work."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

WEIGHTS = {
    "reach": 0.50,
    "engagement": 0.30,
    "conversion_proxy": 0.20,
}

QUALITY_RANK = {"low": 0, "medium": 1, "high": 2}


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run_script(script_path: Path, extra_args: list[str]) -> dict[str, Any]:
    cmd = [sys.executable, str(script_path), *extra_args, "--format", "json"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except Exception as exc:  # noqa: BLE001
        return {
            "source_quality": "low",
            "profiles": [],
            "posts": [],
            "errors": [f"{script_path.name}: {exc}"],
        }


def safe_num(value: Any) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def conversion_proxy_raw(post: dict[str, Any]) -> float:
    text = (post.get("text") or "").lower()
    link = (post.get("link") or "").lower()

    strong = ["signup", "sign up", "join discord", "watch now", "bonus", "cashback", "bet", "play", "deposit"]
    soft = ["live", "stream", "watch", "early access", "launch", "winner"]
    domains = ["wtfgames.com", "wtfleagues.com", "discord.gg", "youtube.com"]

    score = 0.0
    for kw in strong:
        if kw in text:
            score += 1.0
    for kw in soft:
        if kw in text:
            score += 0.25
    for kw in domains:
        if kw in text or kw in link:
            score += 0.75
    if link.startswith("http"):
        score += 0.25

    return min(score, 5.0)


def normalize(raw: float, maximum: float) -> float:
    if maximum <= 0:
        return 0.0
    return (raw / maximum) * 100.0


def score_posts(posts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not posts:
        return []

    reach_values: list[float] = []
    engagement_values: list[float] = []
    conversion_values: list[float] = []

    for post in posts:
        views = safe_num(post.get("views"))
        likes = safe_num(post.get("likes"))
        comments = safe_num(post.get("comments"))
        reposts = safe_num(post.get("reposts"))

        reach = views if views > 0 else likes
        engagement = likes + comments + reposts
        conversion = conversion_proxy_raw(post)

        reach_values.append(reach)
        engagement_values.append(engagement)
        conversion_values.append(conversion)

    max_reach = max(reach_values) if reach_values else 0.0
    max_eng = max(engagement_values) if engagement_values else 0.0
    max_conv = max(conversion_values) if conversion_values else 0.0

    scored: list[dict[str, Any]] = []
    for idx, post in enumerate(posts):
        reach_score = normalize(reach_values[idx], max_reach)
        engagement_score = normalize(engagement_values[idx], max_eng)
        conversion_score = normalize(conversion_values[idx], max_conv)
        composite = (
            WEIGHTS["reach"] * reach_score
            + WEIGHTS["engagement"] * engagement_score
            + WEIGHTS["conversion_proxy"] * conversion_score
        )

        enriched = dict(post)
        enriched["score"] = {
            "reach_score": round(reach_score, 2),
            "engagement_score": round(engagement_score, 2),
            "conversion_proxy_score": round(conversion_score, 2),
            "composite_score": round(composite, 2),
        }
        scored.append(enriched)

    scored.sort(key=lambda p: p["score"]["composite_score"], reverse=True)
    return scored


def aggregate_by_account(posts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for post in posts:
        key = f"{post.get('platform', 'unknown')}:{post.get('account', 'unknown')}"
        grouped.setdefault(key, []).append(post)

    out: list[dict[str, Any]] = []
    for key, rows in grouped.items():
        reach_avg = sum(r["score"]["reach_score"] for r in rows) / len(rows)
        eng_avg = sum(r["score"]["engagement_score"] for r in rows) / len(rows)
        conv_avg = sum(r["score"]["conversion_proxy_score"] for r in rows) / len(rows)
        comp_avg = sum(r["score"]["composite_score"] for r in rows) / len(rows)

        platform, account = key.split(":", 1)
        out.append(
            {
                "platform": platform,
                "account": account,
                "posts_count": len(rows),
                "reach_score": round(reach_avg, 2),
                "engagement_score": round(eng_avg, 2),
                "conversion_proxy_score": round(conv_avg, 2),
                "composite_score": round(comp_avg, 2),
            }
        )

    out.sort(key=lambda row: row["composite_score"], reverse=True)
    return out


def combine_quality(platform_payloads: list[dict[str, Any]], has_data: bool) -> str:
    if not has_data:
        return "low"

    qualities = [p.get("source_quality", "low") for p in platform_payloads]
    ranks = [QUALITY_RANK.get(q, 0) for q in qualities]

    if ranks and all(r == QUALITY_RANK["high"] for r in ranks):
        return "high"
    if ranks and any(r == QUALITY_RANK["low"] for r in ranks):
        return "medium"
    return "medium"


def as_markdown(snapshot: dict[str, Any]) -> str:
    lines = [
        "# WTF Cross-Platform Snapshot",
        "",
        f"- Generated: {snapshot['generated_at_utc']}",
        f"- Source quality: {snapshot['source_quality']}",
        f"- Weights: reach={WEIGHTS['reach']:.2f}, engagement={WEIGHTS['engagement']:.2f}, conversion_proxy={WEIGHTS['conversion_proxy']:.2f}",
        "",
        "## Account Scores",
        "",
        "| Platform | Account | Posts | Reach | Engagement | Conversion Proxy | Composite |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]

    for row in snapshot.get("account_scores", []):
        lines.append(
            f"| {row['platform']} | {row['account']} | {row['posts_count']} | {row['reach_score']:.2f} | {row['engagement_score']:.2f} | {row['conversion_proxy_score']:.2f} | {row['composite_score']:.2f} |"
        )

    lines.extend(["", "## Top Posts (by composite score)", "", "| Platform | Account | ID | Composite | Text |", "|---|---|---|---:|---|"])
    for post in snapshot.get("posts_scored", [])[:10]:
        text = (post.get("text") or "").replace("|", "\\|")
        lines.append(
            f"| {post.get('platform')} | {post.get('account')} | {post.get('id')} | {post['score']['composite_score']:.2f} | {text[:120]} |"
        )

    if snapshot.get("errors"):
        lines.extend(["", "## Errors", ""])
        for err in snapshot["errors"]:
            lines.append(f"- {err}")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a cross-platform WTF social snapshot.")
    parser.add_argument("--x-accounts", default="PLAYWTFGAMES,WTFLeagues")
    parser.add_argument("--ig-usernames", default="wtfleagues,wtfbulletin")
    parser.add_argument("--yt-handles", default="@WTFLeagues")
    parser.add_argument("--post-limit", type=int, default=10)
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    x_payload = run_script(
        script_dir / "fetch_x_twstalker.py",
        ["--accounts", args.x_accounts, "--post-limit", str(args.post_limit)],
    )
    ig_payload = run_script(
        script_dir / "fetch_instagram_public.py",
        ["--usernames", args.ig_usernames, "--post-limit", str(args.post_limit)],
    )
    yt_payload = run_script(
        script_dir / "fetch_youtube_public.py",
        ["--handles", args.yt_handles, "--post-limit", str(args.post_limit)],
    )

    platform_payloads = [x_payload, ig_payload, yt_payload]

    profiles: list[dict[str, Any]] = []
    posts: list[dict[str, Any]] = []
    errors: list[str] = []

    for payload in platform_payloads:
        profiles.extend(payload.get("profiles", []))
        posts.extend(payload.get("posts", []))
        errors.extend(payload.get("errors", []))

    scored_posts = score_posts(posts)
    account_scores = aggregate_by_account(scored_posts)

    snapshot = {
        "generated_at_utc": now_utc(),
        "source_quality": combine_quality(platform_payloads, has_data=bool(profiles or posts)),
        "weights": WEIGHTS,
        "platform_summaries": {
            "x": {
                "source_quality": x_payload.get("source_quality", "low"),
                "profiles": len(x_payload.get("profiles", [])),
                "posts": len(x_payload.get("posts", [])),
            },
            "instagram": {
                "source_quality": ig_payload.get("source_quality", "low"),
                "profiles": len(ig_payload.get("profiles", [])),
                "posts": len(ig_payload.get("posts", [])),
            },
            "youtube": {
                "source_quality": yt_payload.get("source_quality", "low"),
                "profiles": len(yt_payload.get("profiles", [])),
                "posts": len(yt_payload.get("posts", [])),
            },
        },
        "profiles": profiles,
        "posts_scored": scored_posts,
        "account_scores": account_scores,
        "errors": errors,
    }

    output = as_markdown(snapshot) if args.format == "markdown" else json.dumps(snapshot, indent=2, ensure_ascii=False)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
