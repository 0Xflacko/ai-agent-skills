# ai-agent-skills

Open-source AI agent skills curated from my active setup, packaged for reuse with Codex and Cursor.

## What is included

- 24 publishable skills under `skills/`
- Sync and verification tooling for reproducible releases
- Launch copy for X in `posts/x-launch.md`

## Repository layout

- `skills/` - published skill folders
- `config/include-skills.txt` - release allowlist
- `scripts/sync_skills.sh` - sync from local `~/.codex/skills`
- `scripts/verify_release.sh` - release integrity checks
- `manifest/skills.json` - machine-readable skill manifest
- `posts/x-launch.md` - launch post text

## Use with Codex

1. Pick a skill folder from `skills/`.
2. Copy it to your Codex skills directory:

```bash
cp -R skills/<skill-name> ~/.codex/skills/<skill-name>
```

3. Restart your Codex session so the skill is reloaded.

## Use with Cursor

Use the relevant `SKILL.md` content as persistent project/global guidance.

Example project-level flow with `.cursorrules`:

```bash
cp skills/<skill-name>/SKILL.md .cursorrules
```

Then restart Cursor for the new rules to take effect.

## KLING example

I added `kling-docs` so agents can consistently follow KLING standards and use KLING docs deeply, including endpoint/schema-specific references.

## Release workflow

```bash
scripts/sync_skills.sh
scripts/verify_release.sh
```

## Excluded from this release

The following are intentionally excluded from v1:

- `docx`
- `pdf`
- `pptx`
- `xlsx`
- `skill-seekers`
- `.system`
