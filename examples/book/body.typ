// Placeholder body for the book example.
// In a real build this file is generated from markdown by
// scripts/md_to_typst.py (pandoc -t typst).
//
// NOTE: Typst's `include` does not inherit the caller's scope, so an included
// file must import the theme itself if it wants to use the components.
#import "../../theme.typ": *

= Chapter one

== Section title

这里是占位正文，Lorem ipsum dolor sit amet, consectetur adipiscing elit。用于演示书刊版式的正文排版。

== Checklist

#check-item(checked: true)[Placeholder task one]
#check-item(checked: false)[Placeholder task two]

== Table

#table(
  columns: (1.6fr, 1fr),
  [Item], [Status],
  [Placeholder row one], [#badge(level: "ok")[Confirmed]],
  [Placeholder row two], [#badge(level: "warn")[Pending]],
)

= Chapter two

== Section title

#card(title: [Callout title], type: "green")[
  Placeholder callout body 占位文本。
]

#quote[Placeholder quote body — 引用样式占位。]

== Flowchart

#diagram(
  spacing: (16mm, 10mm),
  node((0, 0), [Start], stroke: 0.6pt + border, fill: surface-2, corner-radius: 1.5mm, inset: 2.5mm),
  node((1, 0), [Process], stroke: 0.6pt + border, fill: surface-2, corner-radius: 1.5mm, inset: 2.5mm),
  node((2, 0), [End], stroke: 0.6pt + accent, fill: accent-soft, corner-radius: 1.5mm, inset: 2.5mm),
  edge((0, 0), (1, 0), "->"),
  edge((1, 0), (2, 0), "->"),
)

== Timeline

#timeline((
  ("2026-01", "Placeholder milestone"),
  ("2026-06", "Placeholder milestone"),
))
