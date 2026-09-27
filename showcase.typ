// ============================================================
// Style showcase — five candidate palettes, one page each.
// Same content skeleton so the only variable is the color system.
// Swap the tokens at the top of theme.typ to adopt one of these.
//
// Compile: typst compile showcase.typ showcase.pdf
// ============================================================

#set text(font: ("Microsoft YaHei", "Segoe UI"), size: 9.5pt)
#set par(leading: 0.5em)

// A single color chip
#let chip(color) = {
  let c = if type(color) == color { color } else { rgb(color) }
  grid(
    columns: (1fr,), row-gutter: 1mm,
    block(height: 8mm, fill: c, radius: 2mm),
    text(size: 7pt, fill: rgb("#555"))[#c],
  )
}

// One showcase page
#let spec(no: "", name: "", en: "", tagline: "", cb: rgb("#000"), cf: rgb("#fff"), accent: rgb("#c00"), ink: rgb("#000"), tablebg: rgb("#333"), cardbg: rgb("#eee"), lightbg: rgb("#f5f5f5"), title-font: "Microsoft YaHei") = page(
  paper: "a4", margin: (top: 10mm, bottom: 10mm, left: 12mm, right: 12mm),
  fill: white, header: none, footer: none,
  [
    // ---- cover band (simulates the cover mood) ----
    #block(fill: cb, inset: (x: 12mm, y: 11mm), radius: 5mm, width: 100%, [
      #text(size: 9pt, fill: cf.lighten(25%))[STYLE #no · #en]
      #v(4mm)
      #text(size: 30pt, weight: "bold", fill: cf, font: title-font)[#name]
      #v(3mm)
      #text(size: 11pt, fill: cf.lighten(12%))[#tagline]
    ])
    #v(4mm)

    // ---- palette ----
    #text(size: 10pt, weight: "bold", fill: ink)[Palette]
    #grid(columns: 5 * (1fr,), column-gutter: 3mm,
      chip(cb), chip(accent), chip(ink), chip(cardbg), chip(lightbg),
    )
    #v(4mm)

    // ---- heading hierarchy ----
    #block(width: 100%, below: 3mm, [
      #grid(columns: (auto, 1fr), column-gutter: 3.5mm, align: (center, start),
        block(fill: accent, inset: (x: 3mm, y: 1mm), radius: 1.5mm,
          text(fill: white, weight: "bold", size: 10pt)[01]),
        text(size: 15pt, weight: "bold", fill: ink, font: title-font)[Section title])
      #v(1.5mm)
      #line(length: 100%, stroke: 1.8pt + ink)
    ])
    #text(size: 10.5pt, weight: "bold", fill: ink)[Subsection title]
    #v(1.5mm)

    // ---- callout card ----
    #block(
      width: 100%, fill: cardbg,
      stroke: (left: 2.5pt + accent, top: 0.4pt + rgb("#DDD"), right: 0.4pt + rgb("#DDD"), bottom: 0.4pt + rgb("#DDD")),
      radius: 3mm, inset: (x: 4mm, y: 2.5mm), below: 2mm,
      [
        #text(size: 10.5pt, weight: "bold", fill: accent)[Callout title]
        #v(1mm)
        #text(fill: ink)[Placeholder callout body used for grouping and emphasis.]
      ]
    )

    // ---- table ----
    #table(
      columns: (1.4fr, 1fr),
      fill: (x, y) => if y == 0 { tablebg } else if calc.odd(y) { lightbg } else { white },
      stroke: (x, y) => if y == 0 { (bottom: 1.2pt + accent) } else { 0.3pt + rgb("#DDD") },
      inset: (x: 2mm, y: 1.2mm),
      [Item], [Status],
      [Example row one], box(fill: accent, inset: (x: 2mm, y: 0.3mm), radius: 1.5mm, text(fill: white, size: 8pt, weight: "bold")[Confirmed]),
      [Example row two], [Pending],
    )
    #v(3mm)
    #text(size: 8pt, fill: rgb("#666"))[Body sample: low contrast, low saturation, 9.5pt body text with 1.5 line height for continuous reading.]
  ]
)

// ============ Five palettes ============

#spec(
  no: "01", name: "Graphite × Gold", en: "Graphite × Gold",
  tagline: "Near-black cover + warm gold accent · hardcore engineering report",
  cb: rgb("#0E1116"), cf: rgb("#F5E9D0"), accent: rgb("#C9A227"),
  ink: rgb("#1C1F24"), tablebg: rgb("#232830"), cardbg: rgb("#FAF6EC"), lightbg: rgb("#F2F2F0"),
  title-font: "Microsoft YaHei",
)

#spec(
  no: "02", name: "Teal × Ivory", en: "Teal × Ivory",
  tagline: "Deep teal cover + ivory body · academic and calm",
  cb: rgb("#1E4D3E"), cf: rgb("#F4F1E8"), accent: rgb("#2E7D5B"),
  ink: rgb("#29261F"), tablebg: rgb("#1E4D3E"), cardbg: rgb("#F2EEE3"), lightbg: rgb("#F6F4EE"),
  title-font: "Microsoft YaHei",
)

#spec(
  no: "03", name: "Ember × Charcoal", en: "Ember × Charcoal",
  tagline: "Charcoal cover + saturated ember orange · high impact",
  cb: rgb("#17181A"), cf: rgb("#FFFFFF"), accent: rgb("#E8590C"),
  ink: rgb("#1F2022"), tablebg: rgb("#232426"), cardbg: rgb("#FFF4EC"), lightbg: rgb("#F5F4F2"),
  title-font: "Microsoft YaHei",
)

#spec(
  no: "04", name: "Glacier Blue", en: "Glacier Blue",
  tagline: "Deep glacier cover + sky accent · institutional analysis",
  cb: rgb("#0E3A5C"), cf: rgb("#EAF6FF"), accent: rgb("#2E86C1"),
  ink: rgb("#15222E"), tablebg: rgb("#0E3A5C"), cardbg: rgb("#EFF7FC"), lightbg: rgb("#F2F6F9"),
  title-font: "Microsoft YaHei",
)

#spec(
  no: "05", name: "Warm Minimal", en: "Warm Minimal",
  tagline: "Warm off-white cover + ink text + one green accent · editorial, quiet",
  cb: rgb("#F7F6F3"), cf: rgb("#37352F"), accent: rgb("#448361"),
  ink: rgb("#37352F"), tablebg: rgb("#E9E9E7"), cardbg: rgb("#F7F6F3"), lightbg: rgb("#F2F1EE"),
  title-font: "Microsoft YaHei",
)
