"""Builds and runs pandoc commands for Markdown → PDF conversion."""

import subprocess
from pathlib import Path

from print_md.deps import require_engine, require_pandoc
from print_md.themes import resolve_theme

FILTERS_DIR = Path(__file__).parent / "filters"

# Map common paper size names to Typst-compatible values
PAPER_SIZE_MAP = {
    "a4": "a4",
    "a5": "a5",
    "a3": "a3",
    "letter": "us-letter",
    "legal": "us-legal",
    "tabloid": "us-tabloid",
    "executive": "us-executive",
}

# Explicit markdown extensions for full GFM support
MARKDOWN_FORMAT = (
    "markdown"
    "+pipe_tables"
    "+strikeout"
    "+task_lists"
    "+tex_math_dollars"
    "+footnotes"
    "+smart"
    "+yaml_metadata_block"
    "+fenced_code_blocks"
    "+emoji"
    "+backtick_code_blocks"
    "+fenced_divs"
    "+bracketed_spans"
    "+definition_lists"
    "+superscript"
    "+subscript"
    "+raw_attribute"
)


def build_pandoc_command(
    inputs: list[Path],
    output: Path,
    *,
    engine: str = "typst",
    theme: str = "default",
    toc: bool = False,
    toc_depth: int = 3,
    number_sections: bool = False,
    highlight_style: str | None = None,
    font: str | None = None,
    code_font: str | None = None,
    font_size: str | None = None,
    paper: str = "a4",
    margin: str | None = None,
    pandoc_args: list[str] | None = None,
) -> list[str]:
    """Build the pandoc command line as a list of strings."""
    pandoc = require_pandoc()
    require_engine(engine)

    cmd = [pandoc]

    # Input format with extensions
    cmd += [f"--from={MARKDOWN_FORMAT}"]

    # Output
    cmd += ["-o", str(output)]

    # Engine
    if engine == "typst":
        cmd += ["--pdf-engine=typst"]

        # Template
        template_path = resolve_theme(theme)
        cmd += [f"--template={template_path}"]

        # Typst needs --root to resolve images. Pandoc creates a temp .typ
        # file outside the input dir, so we use "/" to allow access to both.
        cmd += ["--pdf-engine-opt=--root=/"]

        # Task list filter
        task_list_filter = FILTERS_DIR / "task-list.lua"
        if task_list_filter.exists():
            cmd += [f"--lua-filter={task_list_filter}"]

    elif engine == "latex":
        cmd += ["--pdf-engine=xelatex"]

    # Table of contents
    if toc:
        cmd += ["--toc", f"--toc-depth={toc_depth}"]

    # Number sections
    if number_sections:
        cmd += ["--number-sections"]

    # Highlight style — pandoc 3.9+ uses --syntax-highlighting, older uses --highlight-style
    if highlight_style:
        cmd += [f"--syntax-highlighting={highlight_style}"]

    # Font overrides via metadata
    if font:
        cmd += [f"--variable=mainfont:{font}"]
    if code_font:
        cmd += [f"--variable=monofont:{code_font}"]
    if font_size:
        cmd += [f"--variable=fontsize:{font_size}"]

    # Paper size — map common names to Typst-compatible values
    if paper:
        typst_paper = PAPER_SIZE_MAP.get(paper, paper) if engine == "typst" else paper
        cmd += [f"--variable=papersize:{typst_paper}"]

    # Margins
    if margin:
        cmd += [f"--variable=margin-x:{margin}", f"--variable=margin-y:{margin}"]

    # Standalone (needed for templates)
    cmd += ["--standalone"]

    # Extra pandoc args
    if pandoc_args:
        cmd += pandoc_args

    # Input files
    cmd += [str(p) for p in inputs]

    return cmd


def convert(
    inputs: list[Path],
    output: Path,
    *,
    verbose: bool = False,
    quiet: bool = False,
    **kwargs,
) -> None:
    """Run pandoc to convert markdown files to PDF."""
    cmd = build_pandoc_command(inputs, output, **kwargs)

    if verbose:
        import click

        click.secho(f"Running: {' '.join(cmd)}", fg="cyan", err=True)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        raise SystemExit("Error: pandoc timed out after 120 seconds.")
    except FileNotFoundError:
        raise SystemExit("Error: pandoc not found. Install it first.")

    if result.returncode != 0:
        stderr = result.stderr.strip()
        raise SystemExit(f"Error: pandoc failed (exit {result.returncode}):\n{stderr}")

    if not quiet:
        import click

        click.secho(f"  {output}", fg="green", err=True)
