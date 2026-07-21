# Memory seed

Claude's per-project memory lives outside the repo, at
`~/.claude/projects/<project-slug>/memory/`, so it does **not** travel with a
git clone or a zip. These are copies.

On a new machine or a new Claude account, ask Claude to:

> Read `.claude/memory-seed/` and write those files into your project memory.

Or copy them manually:

```bash
DEST=~/.claude/projects/-Users-<you>-order-base-ecommerce/memory
mkdir -p "$DEST" && cp .claude/memory-seed/*.md "$DEST"/
```

The slug is the absolute project path with `/` replaced by `-`. If your path
differs, the slug differs.

Nothing here is load-bearing on its own — every fact is also in `CLAUDE.md`,
`HANDOFF.md` and `DESIGN-NOTES.md`, which *do* travel with the repo. This is a
convenience so a new session starts warm.
