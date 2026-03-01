"""Tests for the print_md converter module."""

from pathlib import Path
from unittest.mock import patch

import pytest

from print_md.converter import MARKDOWN_FORMAT, build_pandoc_command


@pytest.fixture
def sample_md(tmp_path):
    md = tmp_path / "test.md"
    md.write_text("# Hello\n")
    return md


@patch("print_md.converter.require_pandoc", return_value="/usr/bin/pandoc")
@patch("print_md.converter.require_engine", return_value="/usr/bin/typst")
def test_basic_command(mock_engine, mock_pandoc, sample_md, tmp_path):
    output = tmp_path / "test.pdf"
    cmd = build_pandoc_command([sample_md], output)
    assert cmd[0] == "/usr/bin/pandoc"
    assert f"--from={MARKDOWN_FORMAT}" in cmd
    assert "-o" in cmd
    assert str(output) in cmd
    assert "--pdf-engine=typst" in cmd
    assert "--standalone" in cmd
    assert str(sample_md) in cmd


@patch("print_md.converter.require_pandoc", return_value="/usr/bin/pandoc")
@patch("print_md.converter.require_engine", return_value="/usr/bin/typst")
def test_template_included(mock_engine, mock_pandoc, sample_md, tmp_path):
    output = tmp_path / "test.pdf"
    cmd = build_pandoc_command([sample_md], output, theme="default")
    template_args = [a for a in cmd if a.startswith("--template=")]
    assert len(template_args) == 1
    assert "default.typ" in template_args[0]


@patch("print_md.converter.require_pandoc", return_value="/usr/bin/pandoc")
@patch("print_md.converter.require_engine", return_value="/usr/bin/typst")
def test_toc_options(mock_engine, mock_pandoc, sample_md, tmp_path):
    output = tmp_path / "test.pdf"
    cmd = build_pandoc_command([sample_md], output, toc=True, toc_depth=2)
    assert "--toc" in cmd
    assert "--toc-depth=2" in cmd


@patch("print_md.converter.require_pandoc", return_value="/usr/bin/pandoc")
@patch("print_md.converter.require_engine", return_value="/usr/bin/typst")
def test_number_sections(mock_engine, mock_pandoc, sample_md, tmp_path):
    output = tmp_path / "test.pdf"
    cmd = build_pandoc_command([sample_md], output, number_sections=True)
    assert "--number-sections" in cmd


@patch("print_md.converter.require_pandoc", return_value="/usr/bin/pandoc")
@patch("print_md.converter.require_engine", return_value="/usr/bin/typst")
def test_font_options(mock_engine, mock_pandoc, sample_md, tmp_path):
    output = tmp_path / "test.pdf"
    cmd = build_pandoc_command(
        [sample_md], output,
        font="Georgia", code_font="Fira Code", font_size="12pt",
    )
    assert "--variable=mainfont:Georgia" in cmd
    assert "--variable=monofont:Fira Code" in cmd
    assert "--variable=fontsize:12pt" in cmd


@patch("print_md.converter.require_pandoc", return_value="/usr/bin/pandoc")
@patch("print_md.converter.require_engine", return_value="/usr/bin/typst")
def test_paper_and_margin(mock_engine, mock_pandoc, sample_md, tmp_path):
    output = tmp_path / "test.pdf"
    cmd = build_pandoc_command([sample_md], output, paper="letter", margin="1in")
    assert "--variable=papersize:us-letter" in cmd
    assert "--variable=margin-x:1in" in cmd
    assert "--variable=margin-y:1in" in cmd


@patch("print_md.converter.require_pandoc", return_value="/usr/bin/pandoc")
@patch("print_md.converter.require_engine", return_value="/usr/bin/typst")
def test_highlight_style(mock_engine, mock_pandoc, sample_md, tmp_path):
    output = tmp_path / "test.pdf"
    cmd = build_pandoc_command([sample_md], output, highlight_style="monokai")
    assert "--syntax-highlighting=monokai" in cmd


@patch("print_md.converter.require_pandoc", return_value="/usr/bin/pandoc")
@patch("print_md.converter.require_engine", return_value="/usr/bin/xelatex")
def test_latex_engine(mock_engine, mock_pandoc, sample_md, tmp_path):
    output = tmp_path / "test.pdf"
    cmd = build_pandoc_command([sample_md], output, engine="latex")
    assert "--pdf-engine=xelatex" in cmd
    # No template for latex
    template_args = [a for a in cmd if a.startswith("--template=")]
    assert len(template_args) == 0


@patch("print_md.converter.require_pandoc", return_value="/usr/bin/pandoc")
@patch("print_md.converter.require_engine", return_value="/usr/bin/typst")
def test_root_option_for_typst(mock_engine, mock_pandoc, sample_md, tmp_path):
    output = tmp_path / "test.pdf"
    cmd = build_pandoc_command([sample_md], output)
    root_args = [a for a in cmd if a.startswith("--pdf-engine-opt=--root=")]
    assert len(root_args) == 1


@patch("print_md.converter.require_pandoc", return_value="/usr/bin/pandoc")
@patch("print_md.converter.require_engine", return_value="/usr/bin/typst")
def test_lua_filter_included(mock_engine, mock_pandoc, sample_md, tmp_path):
    output = tmp_path / "test.pdf"
    cmd = build_pandoc_command([sample_md], output)
    filter_args = [a for a in cmd if a.startswith("--lua-filter=")]
    assert len(filter_args) == 2
    assert any("task-list.lua" in a for a in filter_args)
    assert any("mermaid.lua" in a for a in filter_args)


@patch("print_md.converter.require_pandoc", return_value="/usr/bin/pandoc")
@patch("print_md.converter.require_engine", return_value="/usr/bin/xelatex")
def test_mermaid_filter_included_latex(mock_engine, mock_pandoc, sample_md, tmp_path):
    """Mermaid filter is included for LaTeX engine (engine-agnostic)."""
    output = tmp_path / "test.pdf"
    cmd = build_pandoc_command([sample_md], output, engine="latex")
    filter_args = [a for a in cmd if "mermaid.lua" in a]
    assert len(filter_args) == 1


@patch("print_md.converter.require_pandoc", return_value="/usr/bin/pandoc")
@patch("print_md.converter.require_engine", return_value="/usr/bin/xelatex")
def test_task_list_filter_not_included_latex(mock_engine, mock_pandoc, sample_md, tmp_path):
    """Task-list filter is Typst-specific and should not appear for LaTeX."""
    output = tmp_path / "test.pdf"
    cmd = build_pandoc_command([sample_md], output, engine="latex")
    filter_args = [a for a in cmd if "task-list.lua" in a]
    assert len(filter_args) == 0


@patch("print_md.converter.require_pandoc", return_value="/usr/bin/pandoc")
@patch("print_md.converter.require_engine", return_value="/usr/bin/typst")
def test_extra_pandoc_args(mock_engine, mock_pandoc, sample_md, tmp_path):
    output = tmp_path / "test.pdf"
    cmd = build_pandoc_command(
        [sample_md], output,
        pandoc_args=["--shift-heading-level-by=-1", "--wrap=none"],
    )
    assert "--shift-heading-level-by=-1" in cmd
    assert "--wrap=none" in cmd


@patch("print_md.converter.require_pandoc", return_value="/usr/bin/pandoc")
@patch("print_md.converter.require_engine", return_value="/usr/bin/typst")
def test_multiple_inputs(mock_engine, mock_pandoc, tmp_path):
    f1 = tmp_path / "a.md"
    f2 = tmp_path / "b.md"
    f1.write_text("# A\n")
    f2.write_text("# B\n")
    output = tmp_path / "merged.pdf"
    cmd = build_pandoc_command([f1, f2], output)
    assert str(f1) in cmd
    assert str(f2) in cmd


def test_markdown_format_extensions():
    """Verify all expected extensions are present."""
    assert "+pipe_tables" in MARKDOWN_FORMAT
    assert "+task_lists" in MARKDOWN_FORMAT
    assert "+tex_math_dollars" in MARKDOWN_FORMAT
    assert "+footnotes" in MARKDOWN_FORMAT
    assert "+strikeout" in MARKDOWN_FORMAT
    assert "+emoji" in MARKDOWN_FORMAT
    assert "+definition_lists" in MARKDOWN_FORMAT
    assert "+superscript" in MARKDOWN_FORMAT
    assert "+subscript" in MARKDOWN_FORMAT
