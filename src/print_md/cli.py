"""Click CLI entry point for print_md."""

from pathlib import Path

import click

from print_md import __version__
from print_md.converter import convert
from print_md.deps import format_check_deps
from print_md.themes import list_themes


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("files", nargs=-1, type=click.Path(exists=True, path_type=Path))
@click.option("-o", "--output", type=click.Path(path_type=Path), help="Output file path.")
@click.option("--merge", is_flag=True, help="Merge multiple inputs into one PDF.")
@click.option("--theme", default="default", show_default=True, help="Theme: default, academic, minimal, or path to .typ file.")
@click.option("--engine", default="typst", show_default=True, type=click.Choice(["typst", "latex"]), help="PDF engine.")
@click.option("--toc/--no-toc", default=False, help="Include table of contents.")
@click.option("--toc-depth", default=3, show_default=True, type=click.IntRange(1, 6), help="TOC depth.")
@click.option("--number-sections", is_flag=True, help="Number headings (1.1, 1.1.1).")
@click.option("--highlight-style", default=None, help="Code highlight theme (pygments, tango, espresso, kate, etc.).")
@click.option("--font", default=None, help="Body font.")
@click.option("--code-font", default=None, help="Monospace font for code.")
@click.option("--font-size", default=None, help='Font size, e.g. "11pt", "12pt".')
@click.option("--paper", default="a4", show_default=True, help="Paper size: a4, letter, a5.")
@click.option("--margin", default=None, help='Margin, e.g. "2.5cm", "1in".')
@click.option("--check-deps", is_flag=True, help="Show dependency status and exit.")
@click.option("--list-themes", "list_themes_flag", is_flag=True, help="List available themes and exit.")
@click.option("-v", "--verbose", is_flag=True, help="Show pandoc command being run.")
@click.option("-q", "--quiet", is_flag=True, help="Suppress output except errors.")
@click.option("--pandoc-args", default=None, help="Extra arguments to pass to pandoc (quoted string).")
@click.version_option(__version__, prog_name="print_md")
def main(
    files,
    output,
    merge,
    theme,
    engine,
    toc,
    toc_depth,
    number_sections,
    highlight_style,
    font,
    code_font,
    font_size,
    paper,
    margin,
    check_deps,
    list_themes_flag,
    verbose,
    quiet,
    pandoc_args,
):
    """Beautiful PDFs from Markdown.

    Convert one or more Markdown files to beautifully styled PDFs.

    \b
    Examples:
      print_md document.md                       # → document.pdf
      print_md document.md -o report.pdf         # → custom output
      print_md *.md                              # → batch conversion
      print_md ch1.md ch2.md --merge -o book.pdf # → merged PDF
    """
    if check_deps:
        click.echo(format_check_deps())
        return

    if list_themes_flag:
        click.echo(list_themes())
        return

    if not files:
        raise click.UsageError("No input files provided. Run with --help for usage.")

    files = list(files)

    # Parse extra pandoc args
    extra_args = pandoc_args.split() if pandoc_args else None

    # Common kwargs for converter
    kwargs = dict(
        engine=engine,
        theme=theme,
        toc=toc,
        toc_depth=toc_depth,
        number_sections=number_sections,
        highlight_style=highlight_style,
        font=font,
        code_font=code_font,
        font_size=font_size,
        paper=paper,
        margin=margin,
        verbose=verbose,
        quiet=quiet,
        pandoc_args=extra_args,
    )

    if merge or output:
        # Single output from one or more inputs
        if output is None:
            output = files[0].with_suffix(".pdf")
        if not quiet:
            click.secho(f"Converting → {output}", bold=True, err=True)
        convert(files, output, **kwargs)
    else:
        # Batch mode: one PDF per input
        for f in files:
            out = f.with_suffix(".pdf")
            if not quiet:
                click.secho(f"Converting → {out}", bold=True, err=True)
            convert([f], out, **kwargs)
