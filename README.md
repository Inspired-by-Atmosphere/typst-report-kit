# typst-report-kit

A small, opinionated **Typst theme for formal reports and books** — warm off-white
paper, ink text, one green accent, hairline borders, restrained editorial
typography. Ships the reusable theme, five alternative palettes for comparison,
and copy-paste examples (cover, callouts, verdict strip, badges, checklist,
timeline, flowchart).

## Why

Most "nice-looking PDF" pipelines for Chinese/English mixed reports end up either
in a heavy HTML-to-PDF toolchain or in hand-rolled Typst files that get copy-pasted
and slowly diverge. This kit is the extraction of one such file into:

- **one token block** — change eleven color values and the whole document re-skins,
- **parameterized components** — cover, callout card, verdict strip, badge,
  checkbox item, timeline, flowchart,
- **one `report()` template** — A4 geometry, running header/footer that
  automatically hide on the cover page, numbered headings, styled tables and
  code blocks.

It is deliberately not a general-purpose design system: it does one look well.

## Layout

```
typst-report-kit/
├── theme.typ                  # design tokens + components + report() template
├── showcase.typ               # 5 candidate palettes, one page each
├── examples/
│   ├── generic-report.typ     # uses every component (placeholder content)
│   └── book/
│       ├── book.typ           # book-style wrapper (unnumbered, book leading)
│       └── body.typ           # placeholder body
├── scripts/
│   ├── check_secrets.py       # stdlib-only leak scanner
│   └── md_to_typst.py         # markdown -> pandoc -> typst -> PDF pipeline
├── docs/SANITIZE_LOG.md
└── CHANGELOG.md
```

## Quickstart

1. **Install Typst ≥ 0.15** — download the binary for your platform from the
   official releases page (`https://github.com/typst/typst/releases`), or use
   `cargo install typst-cli`. No npm, no Node.
2. **Compile the example** (the first run downloads the `codly` and `fletcher`
   packages from the Typst universe, so it needs network access once):

   ```bash
   export HTTPS_PROXY=http://127.0.0.1:7897   # only if you are behind a proxy
   typst compile --root . examples/generic-report.typ
   ```

3. **Write your report** — copy `examples/generic-report.typ`, replace the
   placeholder text, and adjust the tokens at the top of `theme.typ` if you want
   a different accent color.

To see the five palettes side by side:

```bash
typst compile showcase.typ
```

## Configuration

There is no config file. Everything is a named argument.

| Where | Argument | Default | Meaning |
|---|---|---|---|
| `#report(...)` | `doc-title` | `none` | Running header, left. Hidden on page 1. |
| | `doc-date` | `none` | Running header, right. |
| | `doc-footer` | `none` | Running footer, left. `none` = no footer text. |
| | `numbered` | `true` | Number level-1 headings `01`, `02`, … |
| | `leading` | `0.75em` | Paragraph leading (books read better at `0.55em`). |
| | `quote-style` | `"amber"` | `"amber"` cream left-bar quote, or `"green"` callout quote. |
| `#cover(...)` | `kicker` / `title` / `sub` | `none` | Cover text block. |
| | `core-label` / `core` | `none` | The white "positioning" card on the cover. |
| | `meta` | `none` | Bottom-left meta line. |
| | `decoration` | `"lines"` | `"lines"` = three accent rules, `"disc"` = pale disc. |
| `#card(...)` | `title` / `type` | `none` / `"gray"` | `type` ∈ `gray`, `green`, `blue`, `cream`, `red`. |
| `#badge(...)` | `level` | `"ok"` | `ok`, `warn`, `red`, `unk`, or anything else (blue info). |
| `#check-item(...)` | `checked` | `false` | Renders a filled or empty checkbox. |
| `#timeline(...)` | — | — | Takes `((date, label), ...)`. |

Environment variables used by the scripts:

| Variable | Used by | Meaning |
|---|---|---|
| `HTTPS_PROXY` / `HTTP_PROXY` | `typst` | Proxy for the one-time package download. |
| `TYPST_PATH` | `scripts/md_to_typst.py` | Absolute path to the `typst` binary. |
| `PANDOC_PATH` | `scripts/md_to_typst.py` | Absolute path to the `pandoc` binary. |

## Markdown pipeline (optional)

`scripts/md_to_typst.py` converts a markdown file into a themed PDF. It needs
`pandoc` (for markdown → Typst) and `typst` (for Typst → PDF); both are resolved
from `--typst`/`--pandoc`, then `$TYPST_PATH`/`$PANDOC_PATH`, then `PATH`.
Python 3 with the standard library is enough.

```bash
python scripts/md_to_typst.py notes.md notes.pdf \
  --title "Document title" --date 2026-01-01 --footer "Running footer" \
  --numbered
```

A `YAML`-ish `---` frontmatter block (`title:`, `created:`, `source:`) is read if
present and stripped before pandoc sees the file. The script also rewrites a few
pandoc math-writer artifacts (see `fix_body()`) that would otherwise glue
symbols to neighbouring identifiers.

## Known limitations

- **Fonts**: the theme asks for `Microsoft YaHei` with `Segoe UI` as fallback.
  On Linux/macOS you will want to edit that `set text(font: ...)` line — a
  reasonable substitute is `Noto Sans CJK SC` or `Source Han Sans`.
- **Universe packages** (`codly` for code blocks, `fletcher` for the timeline and
  flowchart) are fetched on first compile. Offline machines need them pre-vendored
  under the local Typst package directory.
- **docx is a separate path.** Pandoc's Typst *reader* cannot resolve
  `@preview/...` imports, so a `.docx` built from the compiled `.typ` will not
  work. Keep the markdown source as the docx source and treat Typst as a
  presentation target only.
- The palette is tuned for low-saturation editorial output. It is not designed
  for high-contrast slide decks or print-on-demand color accuracy.
- Verified against Typst **0.15.1**.

## Component notes

- Tables: rows are written flat (every `columns` count of cells is one row) —
  Typst 0.15 does not accept a tuple/array as a row. Use `1fr` for the first
  column, not `auto`; an `auto` first column swallows the remaining width.
- `block` uses `inset`, not `padding`. `letter-spacing` was removed in Typst 0.13.
- `include` does **not** inherit the caller's scope: an included file must
  `#import` the theme itself if it wants to use the components. A body file
  generated by pandoc is fine without an import, because pandoc output only uses
  built-in functions.
- Inside a Typst code-mode expression, nested calls do not take a leading `#`
  (`#grid(columns: ..., card(...))`).
- Prefer passing `[...]` content over `"..."` strings for arguments that contain
  text: Chinese full-width quotes inside a Typst string need escaping otherwise.

## Credits

Palette and component ideas follow the Notion design language (warm off-white,
low-saturation, editorial). Typesetting is done by Typst; code highlighting by
`codly`; diagrams by `fletcher` (built on CeTZ).

## License

MIT — see `LICENSE`. Author: Inspired-by-Atmosphere.
