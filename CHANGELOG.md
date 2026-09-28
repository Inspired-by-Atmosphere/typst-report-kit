# Changelog

All notable changes to this project are documented here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

## [0.1.0] - 2026-09-28

### Added
- `docs/preview/`: preview images (`preview.png`, `showcase.png`) rendered from
  this repo's own sources and used by the READMEs.
- `theme.typ`: warm-minimal design tokens (11 colors) and components —
  `card()`, `verdict()`, `badge()`, `check-item()`, `timeline()`,
  `cover()`, `report()`.
- `report()` parameters: `doc-title`, `doc-date`, `doc-footer`, `numbered`,
  `leading`, `quote-style`.
- `cover()` `decoration` option: three accent rules (`"lines"`) or a pale disc
  (`"disc"`).
- `showcase.typ`: five candidate palettes, one page each, for side-by-side
  comparison.
- `examples/generic-report.typ`: placeholder report exercising every component.
- `examples/book/`: book-style wrapper (`numbered: false`, tighter leading) plus
  a placeholder body.
- `scripts/md_to_typst.py`: markdown → pandoc → Typst → PDF pipeline with
  frontmatter parsing and pandoc math-writer fixes.
- `scripts/check_secrets.py`: dependency-free secret / path / identifier scanner.
- `README.md`, `README.zh-CN.md`, MIT `LICENSE`, `docs/SANITIZE_LOG.md`.

### Notes
- Verified with Typst 0.15.1.
- Universe dependencies: `@preview/codly:1.3.0`, `@preview/fletcher:0.5.8`.
