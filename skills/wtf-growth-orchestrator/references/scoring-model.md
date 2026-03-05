# Scoring Model and Data Contract

## Shared JSON Contract

### SocialProfile

- `platform`
- `account`
- `followers`
- `following`
- `total_posts`
- `verified`
- `captured_at_utc`
- `source`

### SocialPost

- `id`
- `account`
- `platform`
- `created_at_utc`
- `text`
- `media_type`
- `likes`
- `comments`
- `reposts`
- `views`
- `link`

### SnapshotScore

- `reach_score`
- `engagement_score`
- `conversion_proxy_score`
- `composite_score`

## Composite Formula

Use fixed weighting:

- `composite_score = 0.50 * reach_score + 0.30 * engagement_score + 0.20 * conversion_proxy_score`

## Reach-First Interpretation

- Reach is derived primarily from views, with likes as fallback when views are missing.
- Engagement is derived from likes + comments + reposts.
- Conversion proxy is heuristic and should reflect CTA signals in text/link fields.

## Missing Data Handling

- Treat missing numeric metrics as zero.
- Continue scoring even when a platform source partially fails.
- Lower source confidence instead of aborting snapshot creation.
