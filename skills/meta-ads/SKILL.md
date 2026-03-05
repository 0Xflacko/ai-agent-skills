---
name: meta-ads
description: End-to-end support for Meta ads across Facebook and Instagram. Use when requests involve Meta Ads Manager strategy, campaign/ad set/ad structure, audience and creative testing, budget or bid optimization, pixel and Conversions API setup, Marketing API automation, troubleshooting, or performance reporting.
---

# Meta Ads

Drive planning, execution, optimization, and API implementation for Meta ads across Facebook and Instagram.

## Workflow Router

1. Classify the request as one of: `strategy`, `build`, `optimize`, or `api`.
2. Gather minimum context: business goal, conversion event, geo, budget, assets, timeline, constraints.
3. If critical context is missing, ask focused follow-up questions. If speed is required, proceed with explicit assumptions.

## Strategy And Build Workflow

1. Map the growth goal to a currently available Ads Manager objective and verify naming in current docs or UI.
2. Build a test matrix with audience, creative, and offer hypotheses.
3. Output launch structure at three levels: campaign, ad set, and ad.
4. Include Facebook and Instagram placement logic unless the user explicitly limits placements.
5. Add launch controls: naming convention, budget guardrails, stop rules, and scale rules.

## Optimization And Reporting Workflow

1. Diagnose by level (`campaign`, `ad set`, `ad`) and by placement, audience, creative, and time.
2. Tie symptoms to likely causes and fixes:
- high CPM
- low CTR
- low CVR
- rising CPA or declining ROAS
3. Return a 7-day prioritized action plan with expected impact and rollback criteria.
4. If data is incomplete, specify exact report fields to pull from Ads Manager or Insights API.

## API Workflow

1. Use `references/meta-doc-map.md` to choose canonical docs and endpoints.
2. For API requests, provide:
- endpoint sequence
- required auth and permissions
- minimal payload examples
- error handling steps
3. Prefer version-pinned Graph API paths and confirm current version/changes in changelog docs before finalizing.
4. Default to raw Graph API examples for clarity; use Meta Business SDK when the user asks for SDK-specific implementation.

## Troubleshooting Protocol

1. Validate authentication and authorization first.
2. Validate object chain consistency: ad account -> campaign -> ad set -> ad.
3. Validate creative and asset readiness before delivery/debug changes.
4. Check limits, retriable errors, and async status for large jobs.
5. Check changelog and out-of-cycle docs when previously working behavior changes.

## Required References

- `references/meta-doc-map.md`

## Output Standard

1. Always include assumptions, rationale, and next actions.
2. For strategy work, provide test-ready creative and copy angles with KPI targets.
3. For technical work, provide reproducible API calls and verification steps.
4. Keep outputs compliant: avoid misleading claims, prohibited targeting, and guaranteed-results wording.
