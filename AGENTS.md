# AgentsMeetRL

An "awesome list" repository. The content is a curated list in `README.md`, plus a self-contained interactive dashboard in `index.html` and a `logo.png`.

## Cursor Cloud specific instructions

### What this repo is
- Static site only. There is **no** package manager, build step, lint config, or automated test suite.
- `index.html` is a single self-contained page (inline CSS/JS). It loads Chart.js from a CDN and fetches live data (GitHub star badges via `img.shields.io` and the repo `README.md`) at runtime, so charts/counters require outbound internet access.

### Run it (dev)
- Serve the repo root with any static server and open `index.html`, e.g. `python3 -m http.server 8000` then visit `http://localhost:8000/index.html`.
- Do not use `file://` — the runtime `fetch()` calls behave better over `http://`.

### Lint / test / build
- None exist. There is nothing to build; edits to `README.md` / `index.html` are reflected on next page reload.
