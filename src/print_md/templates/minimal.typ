// minimal.typ — Sparse theme for print_md
// Small font, narrow margins, no decoration, maximum content density

// --- Pandoc compatibility ---

#let horizontalrule = line(length: 100%, stroke: 0.4pt + luma(210))

#show terms.item: it => block(breakable: false)[
  #text(weight: "bold")[#it.term]
  #block(inset: (left: 1.5em, top: -0.4em))[#it.description]
]

#show figure.where(kind: table): set figure.caption(position: top)
#show figure.where(kind: image): set figure.caption(position: bottom)

$if(highlighting-definitions)$
$highlighting-definitions$
$endif$

// --- Template variables ---

$if(author)$
#let pm-authors = ($for(author)$"$author$", $endfor$)
$else$
#let pm-authors = ()
$endif$

// --- Page setup ---

#set document(
  title: [$if(title)$$title$$endif$],
$if(author)$
  author: ($for(author)$"$author$"$sep$, $endfor$),
$endif$
)

#set page(
  paper: "$if(papersize)$$papersize$$else$a4$endif$",
  margin: (x: $if(margin-x)$$margin-x$$else$1.8cm$endif$, y: $if(margin-y)$$margin-y$$else$1.8cm$endif$),
  footer: context {
    set text(size: 0.8em, fill: luma(160))
    h(1fr)
    counter(page).display("1")
    h(1fr)
  },
)

// --- Typography (clean sans-serif, small) ---

#set text(
  size: $if(fontsize)$$fontsize$$else$9.5pt$endif$,
  lang: "$if(lang)$$lang$$else$en$endif$",
$if(mainfont)$
  font: "$mainfont$",
$endif$
)

#set par(
  leading: 0.6em,
  first-line-indent: 0pt,
  justify: true,
)

$if(monofont)$
#show raw: set text(font: "$monofont$")
$endif$

$if(number-sections)$
#set heading(numbering: "1.1.1")
$endif$

// --- Heading styles (compact, no decoration) ---

#show heading.where(level: 1): it => {
  set text(size: 1.3em, weight: "bold")
  v(0.8em)
  it
  v(0.2em)
}

#show heading.where(level: 2): it => {
  set text(size: 1.15em, weight: "bold")
  v(0.6em)
  it
  v(0.15em)
}

#show heading.where(level: 3): it => {
  set text(size: 1em, weight: "bold")
  v(0.5em)
  it
  v(0.1em)
}

#show heading.where(level: 4): it => {
  set text(size: 0.95em, weight: "bold")
  v(0.4em)
  it
  v(0.1em)
}

// --- Code blocks (minimal styling) ---

#show raw.where(block: true): it => {
  block(
    width: 100%,
    fill: luma(248),
    inset: (x: 8pt, y: 6pt),
    it,
  )
}

#show raw.where(block: false): it => {
  box(
    fill: luma(243),
    outset: (x: 1.5pt, y: 2pt),
    radius: 1.5pt,
    it,
  )
}

// --- Links (simple color, no underline) ---

#show link: set text(fill: rgb("#2563eb"))

// --- Tables ---

#set table(
  stroke: 0.4pt + luma(200),
  inset: (x: 6pt, y: 4pt),
)
#show table.cell.where(y: 0): set text(weight: "bold")

// --- Block quotes ---

#show quote.where(block: true): it => {
  block(
    width: 100%,
    inset: (left: 10pt, y: 4pt),
    stroke: (left: 2pt + luma(200)),
    it,
  )
}

// --- Lists (tight) ---

#set list(indent: 1em, body-indent: 0.4em)
#set enum(indent: 1em, body-indent: 0.4em)

#show footnote.entry: set text(size: 0.8em)

// === Title (inline, if present) ===
$if(title)$
#text(size: 1.5em, weight: "bold")[$title$]
$if(author)$ · #text(size: 0.95em, fill: luma(80))[#pm-authors.join(", ")]$endif$
$if(date)$ · #text(size: 0.9em, fill: luma(100))[$date$]$endif$
#v(0.8em)
$endif$

// === Table of contents ===
$if(toc)$
#outline(
  title: auto,
  depth: $toc-depth$,
  indent: 1em,
)
#v(0.5em)
$endif$

// === Body ===
$body$
