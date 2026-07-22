# Abu Auf — static storefront

A static, Arabic-first (RTL) storefront for **Abu Auf**, rebuilt from an
OrderBase static export against the client's Figma and their live site.

**31 core pages + a generated page per catalogue product (130 HTML files).**
No framework and no server — plain HTML, a build-time Tailwind stylesheet, and
vanilla JS.

> **This is a staging/demo build, not the client's live shop.**
> The real store is abuauf.com. Every page here ships
> `<meta name="robots" content="noindex, nofollow">` so this build cannot
> compete with the client's own site in search or be mistaken for it. The three
> legal pages are in-house placeholder, and the homepage reviews and the
> product-page rating are invented placeholder — all tracked in
> `DESIGN-NOTES.md`. Do not treat this as production content.

## Running it

```bash
npm install                 # once — Tailwind CLI (v3) for the stylesheet
python3 build/build.py      # generates all 130 pages + static-export/tailwind.css
python3 build/serve.py      # http://localhost:8000
```

Use `build/serve.py`, not `python3 -m http.server` — the latter sends no cache
headers, so browsers hold `scripts.js`/`styles.css` and a refresh keeps showing
the old file.

## Layout

```
build/            page generators; components.py is the source of truth for
                  shared markup, catalog.py for data
static-export/    the built site — this directory is what gets published
tailwind.config.js  design tokens, taken from the Figma variables
```

Three editing layers, and it matters which one you are in:

| Layer | Files | Rebuild needed? |
|---|---|---|
| Runtime | `static-export/styles.css`, `static-export/scripts.js` | no, just refresh |
| Design tokens | `tailwind.config.js` | yes (`npm run css`) |
| Page content | `build/**` | yes (`python3 build/build.py`) |

**Never hand-edit `static-export/*.html`** — they are generated and the next
build silently overwrites them.

## Deployment

Pushing to `main` triggers `.github/workflows/deploy.yml`, which installs
Tailwind, runs the build and publishes `static-export/` to GitHub Pages. The
build fails the deploy on a missing asset, a template-literal hazard in
`scripts.js`, or a Tailwind failure, so a broken site cannot ship.

## Docs

- **`CLAUDE.md`** — the operating brief. Read before changing anything.
- **`HANDOFF.md`** — history, rationale, and the verification sweep.
- **`DESIGN-NOTES.md`** — every deviation, placeholder and open question.
