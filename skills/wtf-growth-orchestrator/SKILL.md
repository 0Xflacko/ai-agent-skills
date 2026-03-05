---
name: wtf-growth-orchestrator
description: Orchestrate cross-brand growth work for the WTF startup ecosystem (wtfgames.com crypto-casino side and wtfleagues.com entertainment/livestream side). Use when requests span both brands, require cross-funnel strategy, combine content with conversion planning, or ask for social performance analysis/reporting across X, Instagram, and YouTube.
---

# WTF Growth Orchestrator

Coordinate strategy and execution whenever a request crosses brand boundaries or needs one combined growth plan.

## Routing Workflow

1. Classify the request before drafting output.
2. Route to `wtfgames-casino-growth` when the task is strictly casino-side conversion, bonus framing, waitlist growth, or deposit-funnel messaging.
3. Route to `wtfleagues-content-growth` when the task is strictly livestream/content-system growth, episode formats, hooks, or social content operations.
4. Stay in this skill when the task requires both sides together, shared KPI tradeoffs, shared channel planning, or social audits.
5. Keep outputs English-only for v1.

## Cross-Brand Execution Standard

1. Build plans in this order: audience, channel mechanics, content plan, conversion path, measurement.
2. Use a reach-first blend when tradeoffs appear: reach first, engagement second, conversion proxy third.
3. Tie every entertainment-side content recommendation to a path toward `wtfgames.com` conversion actions.
4. Keep voice mostly unified across both sides with light side-specific adjustments.
5. Treat X metrics from mirror sources as approximate.

## Required References

Read these files before finalizing a substantial strategy:

- `references/brand-map.md`
- `references/geo-policy.md`
- `references/routing-rules.md`
- `references/scoring-model.md`
- `references/social-baseline-2026-02-18.md`

## Data Collection Commands

Use scripts in this skill when the user requests social analysis or score updates:

```bash
python3 scripts/fetch_x_twstalker.py --accounts PLAYWTFGAMES,WTFLeagues --post-limit 10
python3 scripts/fetch_instagram_public.py --usernames wtfleagues,wtfbulletin --post-limit 12
python3 scripts/fetch_youtube_public.py --handles @WTFLeagues --post-limit 10
python3 scripts/social_snapshot.py --format markdown
```

## Guardrail Floor

Allow edgy, high-energy voice. Do not produce claims that guarantee wins, target minors, or explicitly encourage illegal-market activity.
