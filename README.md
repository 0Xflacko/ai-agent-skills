# ai-agent-skills

Open-source AI agent skills curated from my active setup, packaged for reuse with Codex, Cursor, and OpenClaw.

## What is included

- 48 publishable skills under `skills/`
- Multi-source sync tooling (Codex, Cursor, Cursor plugins)
- Verification tooling for reproducible releases
- Machine-readable manifest at `manifest/skills.json`

## Skill sources

| Source | Count | Description |
|--------|-------|-------------|
| Codex (`~/.codex/skills`) | 29 | Custom Codex skills |
| Cursor (`~/.cursor/skills-cursor`) | 5 | Cursor-authored IDE skills |
| Cursor Team Kit (plugin) | 12 | Cursor dev-workflow skills |
| Vercel (plugin) | 1 | React/Next.js best practices |
| Supabase (plugin) | 1 | Postgres best practices |

## All skills

### Codex skills

`algorithmic-art` `brand-guidelines` `canvas-design` `content-research-writer` `develop-web-game` `doc-coauthoring` `frontend-design` `internal-comms` `kling-docs` `mcp-builder` `meta-ads` `openai-docs` `security-best-practices` `security-ownership-map` `security-threat-model` `sentry` `skill-creator` `skill-seekers` `slack-gif-creator` `sora` `spreadsheet` `theme-factory` `twitter-algorithm-optimizer` `vercel-deploy` `web-artifacts-builder` `webapp-testing` `wtf-growth-orchestrator` `wtfgames-casino-growth` `wtfleagues-content-growth`

### Cursor skills

`create-rule` `create-skill` `create-subagent` `migrate-to-skills` `update-cursor-settings`

### Cursor Team Kit skills

`check-compiler-errors` `deslop` `fix-ci` `fix-merge-conflicts` `get-pr-comments` `loop-on-ci` `new-branch-and-pr` `pr-review-canvas` `review-and-ship` `run-smoke-tests` `weekly-review` `what-did-i-get-done`

### Plugin skills

`supabase-postgres-best-practices` `vercel-react-best-practices`

## Repository layout

- `skills/` - published skill folders
- `config/include-skills.txt` - release allowlist
- `scripts/sync_skills.sh` - multi-source sync from local skill directories
- `scripts/verify_release.sh` - release integrity checks
- `manifest/skills.json` - machine-readable skill manifest

## Use with Codex

1. Pick a skill folder from `skills/`.
2. Copy it to your Codex skills directory:

```bash
cp -R skills/<skill-name> ~/.codex/skills/<skill-name>
```

3. Restart your Codex session so the skill is reloaded.

## Use with Cursor

Copy the `SKILL.md` into your Cursor skills directory:

```bash
mkdir -p ~/.cursor/skills-cursor/<skill-name>
cp skills/<skill-name>/SKILL.md ~/.cursor/skills-cursor/<skill-name>/SKILL.md
```

Or use as project-level rules:

```bash
cp skills/<skill-name>/SKILL.md .cursorrules
```

Then restart Cursor for the new rules to take effect.

## Release workflow

```bash
scripts/sync_skills.sh
scripts/verify_release.sh
```

Use `--dry-run` with the sync script to preview changes without writing files.

## Excluded from this release

The following are intentionally excluded:

- `docx`
- `pdf`
- `pptx`
- `xlsx`
- `.system`
