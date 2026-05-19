# Design system

Generated projects include a root-level `DESIGN.md` file.

`DESIGN.md` is a human- and agent-readable design source of truth. It follows the public Google Labs Code [`DESIGN.md`](https://github.com/google-labs-code/design.md) alpha format: YAML design tokens at the top, followed by markdown guidance explaining how to apply those tokens.

## Why it exists

This starter is often edited by humans and AI coding agents. A checked-in `DESIGN.md` gives every contributor the same baseline for:

- colors and semantic roles
- typography scale
- spacing and radius choices
- common component styling
- layout patterns
- practical do/don't guardrails

The default file is intentionally generic for most SaaS projects. It should be updated once your product has a clearer brand or UI direction.

## How to use it

Before making broad UI changes, read `DESIGN.md` and keep new templates/components consistent with it.

When the design direction changes:

1. Update the YAML tokens first.
2. Update the markdown sections so the prose matches the tokens.
3. Run the linter:

```bash
npx @google/design.md lint DESIGN.md
```

4. Then update templates, Tailwind classes, screenshots, or docs that rely on the old system.

## Agent-neutral workflow

Do not make this file specific to one AI tool. Keep it useful for humans and any coding agent by describing project conventions, token names, component rules, and file paths in plain language.

Good guidance:

- "Use `primary` for the single most important action per screen."
- "Forms should include labels, helper/error text, and visible focus states."
- "Update `DESIGN.md` before broad UI redesigns."

Avoid guidance like:

- "Cursor should..."
- "Claude must..."
- "Codex only..."

The goal is a portable design contract that survives across tools.
