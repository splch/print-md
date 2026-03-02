// default.typ — Modern, clean theme for print_md
// Sans-serif, gray code blocks, subtle rules, comfortable spacing

// --- Pandoc compatibility ---

// Horizontal rules: Pandoc outputs #horizontalrule for ---
#let horizontalrule = line(length: 100%, stroke: 0.5pt + luma(200))

// Block quotes: Pandoc outputs #blockquote for > syntax
#let blockquote(body) = quote(block: true, body)

// Callout boxes for fenced divs (::: note, ::: tip)
#let callout-note(body) = block(
  width: 100%,
  stroke: (left: 3pt + rgb("#3b82f6")),
  fill: rgb("#eff6ff"),
  inset: (left: 14pt, right: 12pt, y: 10pt),
  above: 1.2em,
  below: 1.2em,
  body,
)

#let callout-tip(body) = block(
  width: 100%,
  stroke: (left: 3pt + rgb("#22c55e")),
  fill: rgb("#f0fdf4"),
  inset: (left: 14pt, right: 12pt, y: 10pt),
  above: 1.2em,
  below: 1.2em,
  body,
)

// Definition lists
#show terms.item: it => block(breakable: false)[
  #text(weight: "bold")[#it.term]
  #block(inset: (left: 1.5em, top: -0.4em))[#it.description]
]

// Table/figure captions
#show figure.where(kind: table): set figure.caption(position: top)
#show figure.where(kind: image): set figure.caption(position: bottom)

// Syntax highlighting (injected by pandoc)
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
  margin: (x: $if(margin-x)$$margin-x$$else$2.5cm$endif$, y: $if(margin-y)$$margin-y$$else$2.5cm$endif$),
  header: context {
    if counter(page).get().first() > 1 [
      #set text(size: 0.85em, fill: luma(140))
      $if(title)$$title$$endif$
      #h(1fr)
      $if(date)$$date$$endif$
    ]
  },
  footer: context {
    set text(size: 0.85em, fill: luma(140))
    h(1fr)
    counter(page).display("1 / 1", both: true)
    h(1fr)
  },
)

// --- Typography ---

#set text(
  size: $if(fontsize)$$fontsize$$else$11pt$endif$,
  lang: "$if(lang)$$lang$$else$en$endif$",
$if(mainfont)$
  font: "$mainfont$",
$endif$
)

#set par(
  leading: 0.7em,
  first-line-indent: 0pt,
  justify: true,
)

$if(monofont)$
#show raw: set text(font: "$monofont$")
$endif$

// --- Heading styles ---

#show heading.where(level: 1): it => {
  set text(size: 1.5em, weight: "bold")
  v(1.2em)
  it
  v(0.4em)
  line(length: 100%, stroke: 0.5pt + luma(200))
  v(0.3em)
}

#show heading.where(level: 2): it => {
  set text(size: 1.25em, weight: "bold")
  v(1em)
  it
  v(0.3em)
}

#show heading.where(level: 3): it => {
  set text(size: 1.1em, weight: "bold")
  v(0.8em)
  it
  v(0.2em)
}

#show heading.where(level: 4): it => {
  set text(size: 1em, weight: "bold", style: "italic")
  v(0.6em)
  it
  v(0.2em)
}

$if(number-sections)$
#set heading(numbering: "1.1.1")
$endif$

// --- Code blocks ---

#show raw.where(block: true): it => {
  block(
    width: 100%,
    fill: luma(245),
    stroke: 0.5pt + luma(220),
    radius: 3pt,
    inset: (x: 10pt, y: 8pt),
    it,
  )
}

// Inline code
#show raw.where(block: false): it => {
  box(
    fill: luma(240),
    outset: (x: 2pt, y: 2.5pt),
    radius: 2pt,
    it,
  )
}

// --- Links ---

#show link: it => {
  set text(fill: rgb("#2563eb"))
  underline(offset: 2pt, stroke: 0.5pt + rgb("#93bbfc"), it)
}

// --- Tables ---

#set table(
  stroke: 0.5pt + luma(180),
  inset: (x: 8pt, y: 5pt),
)
#show table.cell.where(y: 0): set text(weight: "bold")

// --- Block quotes ---

#show quote.where(block: true): it => {
  block(
    width: 100%,
    inset: (left: 12pt, y: 6pt),
    stroke: (left: 3pt + luma(180)),
    fill: luma(250),
    it,
  )
}

// --- Lists ---

#set list(indent: 1.2em, body-indent: 0.5em)
#set enum(indent: 1.2em, body-indent: 0.5em)

// Footnotes
#show footnote.entry: set text(size: 0.85em)

// === Title block ===
$if(title)$
#v(2em)
#align(center)[
  #text(size: 2em, weight: "bold")[$title$]
  $if(author)$
  #v(0.5em)
  #text(size: 1.1em, fill: luma(80))[#pm-authors.join(", ")]
  $endif$
  $if(date)$
  #v(0.3em)
  #text(size: 0.95em, fill: luma(100))[$date$]
  $endif$
]
#v(2em)
$endif$

// === Table of contents ===
$if(toc)$
#outline(
  title: auto,
  depth: $toc-depth$,
  indent: 1.5em,
)
#v(1em)
$endif$

// === Body ===
$body$
