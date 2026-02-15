---
name: kling-docs
description: Use when the user asks about KLING AI/Kling API documentation, endpoints, request/response schemas, authentication, rate limits, billing, model capabilities, or quick-start guidance from the official docs at app.klingai.com/global/dev/document-api.
---

# KLING Docs

Use this skill to answer questions from the KLING developer documentation corpus.

## Coverage

- Source docs root: `https://app.klingai.com/global/dev/document-api/quickStart/productIntroduction/overview`
- Page snapshots: `references/pages/` (40 pages)
- API schema snapshots: `references/api/` (24 API bundles with endpoint definitions)
- Master index: `references/index.md`
- Machine-readable index: `references/index.json`

## Workflow

1. Read `references/index.md` first to locate the relevant page or API schema file.
2. For conceptual/docs pages (quick start, billing, protocols, announcements), read files in `references/pages/`.
3. For endpoint details (headers, params, request/response fields, examples), read files in `references/api/`.
4. Prefer exact field names, enums, limits, and endpoint paths from the references over memory.
5. If a requested detail is not present, say so explicitly instead of inferring.

## Refresh Docs

Rebuild references from live KLING docs:

```bash
node scripts/build_kling_docs_refs.js
```

For Chinese-language snapshots:

```bash
node scripts/build_kling_docs_refs.js --zh
```

## Notes

- The KLING docs site is SPA-based; this skill extracts compiled route pages and API chunks directly from production bundles.
- API schema files include raw endpoint data and examples from `api-*.js` chunks.
