# print_md

Beautiful PDFs from Markdown. One command, sensible defaults.

```
print_md document.md        # → document.pdf
```

`print_md` wraps [Pandoc](https://pandoc.org) + [Typst](https://typst.app) to convert Markdown files into professionally styled PDFs with zero configuration. Full GFM support — tables, syntax highlighting, math, images, task lists, footnotes, and more.

## Install

```bash
# Install print_md
pip install .

# External dependencies
brew install pandoc typst
```

Verify everything is set up:

```bash
print_md --check-deps
```

## Usage

```bash
# Single file
print_md document.md

# Custom output path
print_md document.md -o report.pdf

# Batch convert — one PDF per file
print_md *.md

# Merge multiple files into one PDF
print_md ch1.md ch2.md ch3.md --merge -o book.pdf
```

### Themes

Three built-in themes ship with `print_md`:

| Theme | Description |
|---|---|
| `default` | Modern, clean — sans-serif, gray code blocks, subtle rules |
| `academic` | Formal — serif, numbered sections, running headers |
| `minimal` | Sparse — small font, narrow margins, maximum density |

```bash
print_md document.md --theme academic
print_md document.md --theme minimal
print_md document.md --theme ./my-custom-template.typ
```

### Table of contents

```bash
print_md document.md --toc
print_md document.md --toc --toc-depth 2 --number-sections
```

### Typography

```bash
print_md document.md --font "Georgia" --code-font "Fira Code" --font-size 12pt
```

### Page layout

```bash
print_md document.md --paper letter --margin 1in
```

### Code highlighting

```bash
print_md document.md --highlight-style espresso
```

Available styles: `pygments`, `tango`, `espresso`, `zenburn`, `kate`, `monochrome`, `breezedark`, `haddock`.

### LaTeX engine

If you have a TeX distribution installed, you can use XeLaTeX instead of Typst:

```bash
print_md document.md --engine latex
```

### Passing extra pandoc options

```bash
print_md document.md --pandoc-args "--shift-heading-level-by=-1"
```

## Supported Markdown features

- **Headings** (H1–H6)
- **Emphasis** — bold, italic, strikethrough
- **Code** — fenced blocks with syntax highlighting, inline code
- **Tables** — pipe tables with alignment
- **Math** — inline `$...$` and display `$$...$$` (LaTeX syntax)
- **Task lists** — `- [x]` / `- [ ]` checkboxes
- **Footnotes**
- **Blockquotes**
- **Images**
- **Links**
- **Definition lists**
- **Superscript / subscript** — `H~2~O`, `mc^2^`
- **Emoji** — `:thumbsup:`
- **YAML metadata** — `title`, `author`, `date` in front matter
- **Horizontal rules**

## Full options

```
Usage: print_md [OPTIONS] [FILES]...

Options:
  -o, --output PATH          Output file path
  --merge                    Merge multiple inputs into one PDF
  --theme TEXT               default, academic, minimal, or path to .typ file
  --engine [typst|latex]     PDF engine (default: typst)
  --toc / --no-toc           Include table of contents
  --toc-depth INTEGER        TOC depth, 1–6 (default: 3)
  --number-sections          Number headings (1.1, 1.1.1)
  --highlight-style TEXT     Code highlight theme
  --font TEXT                Body font
  --code-font TEXT           Monospace font for code
  --font-size TEXT           e.g. "11pt", "12pt"
  --paper TEXT               a4, letter, a5 (default: a4)
  --margin TEXT              e.g. "2.5cm", "1in"
  --check-deps              Show dependency status and exit
  --list-themes             List available themes and exit
  -v, --verbose             Show pandoc command being run
  -q, --quiet               Suppress output except errors
  --pandoc-args TEXT         Extra arguments to pass to pandoc
  --version                 Show version and exit
  -h, --help                Show help and exit
```

## Custom templates

You can create your own Typst template and pass it directly:

```bash
print_md document.md --theme ./my-template.typ
```

Templates use [Pandoc's template syntax](https://pandoc.org/MANUAL.html#templates) mixed with [Typst](https://typst.app/docs). See the built-in templates in `src/print_md/templates/` for examples.

Key template variables available: `$title$`, `$author$`, `$date$`, `$body$`, `$toc$`, `$toc-depth$`, `$mainfont$`, `$monofont$`, `$fontsize$`, `$papersize$`, `$margin-x$`, `$margin-y$`, `$highlighting-definitions$`.

## Development

```bash
# Set up
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"

# Run tests
pytest tests/ -v
```

## Requirements

- Python >= 3.9
- [Pandoc](https://pandoc.org/installing.html) (required)
- [Typst](https://github.com/typst/typst#installation) (required for default engine)
- XeLaTeX (optional, for `--engine latex`)

## License

MIT
