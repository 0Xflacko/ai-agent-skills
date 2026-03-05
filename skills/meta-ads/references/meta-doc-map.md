# Meta Ads Official Docs Map

Validated on 2026-02-18 against `https://developers.facebook.com/docs`.

Use this file to route requests to the correct official Meta documentation page before giving implementation guidance.

## Core Marketing API

- Marketing API home: https://developers.facebook.com/docs/marketing-api
  - Use for top-level capability scope and navigation.
- Overview: https://developers.facebook.com/docs/marketing-api/overview
  - Use for what the Marketing API can do across ads, audiences, and reporting.
- Get started: https://developers.facebook.com/docs/marketing-api/get-started
  - Use for setup prerequisites and entry workflow.
- Authentication: https://developers.facebook.com/docs/marketing-api/get-started/authentication
  - Use for access token acquisition/renewal guidance.
- Authorization: https://developers.facebook.com/docs/marketing-api/overview/authorization
  - Use for permission and authorization model clarification.

## Campaign Build And Delivery

- Basic ad creation: https://developers.facebook.com/docs/marketing-api/get-started/basic-ad-creation
- Create an ad campaign: https://developers.facebook.com/docs/marketing-api/get-started/basic-ad-creation/create-an-ad-campaign
- Manage campaigns: https://developers.facebook.com/docs/marketing-api/get-started/manage-campaigns
- Ad optimization basics: https://developers.facebook.com/docs/marketing-api/get-started/ad-optimization-basics

Use these pages when creating, editing, pausing, resuming, or deleting campaigns/ad sets/ads.

## Optimization, Safety, And Operations

- Insights API: https://developers.facebook.com/docs/marketing-api/insights
- Audiences: https://developers.facebook.com/docs/marketing-api/audiences
- Bidding: https://developers.facebook.com/docs/marketing-api/bidding
- Ad creative: https://developers.facebook.com/docs/marketing-api/creative
- Ad rules engine: https://developers.facebook.com/docs/marketing-api/ad-rules
- Conversions API: https://developers.facebook.com/docs/marketing-api/conversions-api
- Catalog: https://developers.facebook.com/docs/marketing-api/catalog
- Brand safety and suitability: https://developers.facebook.com/docs/marketing-api/brand-safety-and-suitability
- Best practices: https://developers.facebook.com/docs/marketing-api/best-practices
- Troubleshooting: https://developers.facebook.com/docs/marketing-api/troubleshooting

## API Reference Entry Points

- Reference index: https://developers.facebook.com/docs/marketing-api/reference
- Ad account object: https://developers.facebook.com/docs/marketing-api/reference/ad-account
- Ad account campaigns edge: https://developers.facebook.com/docs/marketing-api/reference/ad-account/campaigns/
- Ad account ad sets edge: https://developers.facebook.com/docs/marketing-api/reference/ad-account/adsets/
- Ad account ads edge: https://developers.facebook.com/docs/marketing-api/reference/ad-account/ads/
- Ad account creatives edge: https://developers.facebook.com/docs/marketing-api/reference/ad-account/adcreatives/
- Ad account insights edge: https://developers.facebook.com/docs/marketing-api/reference/ad-account/insights/
- Ad creative previews edge: https://developers.facebook.com/docs/marketing-api/reference/ad-creative/previews/
- Lead retrieval edge: https://developers.facebook.com/docs/marketing-api/reference/adgroup/leads/

Use these pages when producing exact endpoint flows and payload structures.

## Companion Platform Docs

- Graph API overview: https://developers.facebook.com/docs/graph-api
- Using Graph API: https://developers.facebook.com/docs/graph-api/using-graph-api
- Meta Business SDK: https://developers.facebook.com/docs/business-sdk
- Business Management APIs: https://developers.facebook.com/docs/business-management-apis

Use these when a request spans auth, SDK implementation, or broader Business API integration.

## Change Monitoring

- Marketing API changelog: https://developers.facebook.com/docs/marketing-api/marketing-api-changelog
- Out-of-cycle changes: https://developers.facebook.com/docs/marketing-api/out-of-cycle-changes

Check these pages whenever behavior changes unexpectedly or when the user asks for the latest API behavior.

## Notes

- Path `https://developers.facebook.com/docs/graph-api/reference/user/adaccounts` returned a Page Not Found during validation on 2026-02-18.
- Prefer current docs plus version-pinned requests over memory for object fields and edge behavior.
