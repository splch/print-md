// academic.typ — Formal theme for print_md
// Serif font, numbered sections, running headers, formal spacing

// --- Pandoc compatibility ---

#let horizontalrule = line(length: 100%, stroke: 0.5pt + luma(160))

// Block quotes: Pandoc outputs #blockquote for > syntax
#let blockquote(body) = quote(block: true, body)

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
  margin: (x: $if(margin-x)$$margin-x$$else$3cm$endif$, y: $if(margin-y)$$margin-y$$else$3cm$endif$),
  header: context {
    if counter(page).get().first() > 1 [
      #set text(size: 0.8em, fill: luma(100), style: "italic")
      $if(title)$$title$$endif$
      #h(1fr)
      $if(author)$#pm-authors.join(", ")$endif$
    ]
  },
  footer: context {
    set text(size: 0.85em, fill: luma(100))
    h(1fr)
    counter(page).display("1")
    h(1fr)
  },
)

// --- Typography (serif) ---

#set text(
  size: $if(fontsize)$$fontsize$$else$11pt$endif$,
  lang: "$if(lang)$$lang$$else$en$endif$",
$if(mainfont)$
  font: "$mainfont$",
$else$
  font: "New Computer Modern",
$endif$
)

#set par(
  leading: 0.75em,
  first-line-indent: 1.5em,
  justify: true,
)

$if(monofont)$
#show raw: set text(font: "$monofont$")
$endif$

// Numbered headings (off by default; use --number-sections to enable)
// #set heading(numbering: "1.1.1")

// --- Heading styles ---

#show heading.where(level: 1): it => {
  set text(size: 1.4em, weight: "bold")
  set par(first-line-indent: 0pt)
  v(1.5em)
  it
  v(0.6em)
}

#show heading.where(level: 2): it => {
  set text(size: 1.2em, weight: "bold")
  set par(first-line-indent: 0pt)
  v(1.2em)
  it
  v(0.4em)
}

#show heading.where(level: 3): it => {
  set text(size: 1.05em, weight: "bold", style: "italic")
  set par(first-line-indent: 0pt)
  v(1em)
  it
  v(0.3em)
}

#show heading.where(level: 4): it => {
  set text(size: 1em, style: "italic")
  set par(first-line-indent: 0pt)
  v(0.8em)
  it
  v(0.2em)
}

// --- Code blocks ---

#show raw.where(block: true): it => {
  block(
    width: 100%,
    fill: luma(248),
    stroke: (left: 2pt + luma(160)),
    inset: (x: 10pt, y: 8pt),
    it,
  )
}

#show raw.where(block: false): it => {
  box(
    fill: luma(243),
    outset: (x: 2pt, y: 2.5pt),
    radius: 2pt,
    it,
  )
}

// --- Links (subdued) ---

#show link: it => {
  set text(fill: rgb("#1a4d8f"))
  underline(offset: 2pt, stroke: 0.4pt + rgb("#7ba3d4"), it)
}

// --- Tables ---

#set table(
  stroke: 0.5pt + luma(150),
  inset: (x: 8pt, y: 5pt),
)
#show table.cell.where(y: 0): set text(weight: "bold")

// --- Block quotes ---

#show quote.where(block: true): it => {
  set text(style: "italic")
  block(
    width: 100%,
    inset: (left: 15pt, y: 6pt),
    stroke: (left: 2pt + luma(160)),
    it,
  )
}

// --- Lists ---

#set list(indent: 1.5em, body-indent: 0.5em)
#set enum(indent: 1.5em, body-indent: 0.5em)

#show footnote.entry: set text(size: 0.8em)

// === Title page ===
$if(title)$
#v(4em)
#align(center)[
  #text(size: 1.8em, weight: "bold")[$title$]
  $if(author)$
  #v(1em)
  #text(size: 1.15em)[#pm-authors.join(" · ")]
  $endif$
  $if(date)$
  #v(0.5em)
  #text(size: 1em, fill: luma(80))[$date$]
  $endif$
]
#v(1em)
#align(center)[#line(length: 40%, stroke: 0.5pt + luma(160))]
#v(2em)
$endif$

// === Table of contents ===
$if(toc)$
#outline(
  title: auto,
  depth: $toc-depth$,
  indent: 1.5em,
)
#pagebreak()
$endif$

// === Body ===
$body$
