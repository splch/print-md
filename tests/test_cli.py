"""Tests for the print_md CLI."""

from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from print_md.cli import main


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def sample_md(tmp_path):
    md = tmp_path / "test.md"
    md.write_text("# Hello\n\nThis is a test.\n")
    return md


def test_version(runner):
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "print_md" in result.output
    assert "0.1.0" in result.output


def test_help(runner):
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Beautiful PDFs from Markdown" in result.output


def test_no_files(runner):
    result = runner.invoke(main, [])
    assert result.exit_code != 0
    assert "No input files" in result.output


def test_check_deps(runner):
    result = runner.invoke(main, ["--check-deps"])
    assert result.exit_code == 0
    assert "pandoc:" in result.output
    assert "typst:" in result.output


def test_list_themes(runner):
    result = runner.invoke(main, ["--list-themes"])
    assert result.exit_code == 0
    assert "default" in result.output
    assert "academic" in result.output
    assert "minimal" in result.output


@patch("print_md.cli.convert")
def test_single_file_default_output(mock_convert, runner, sample_md):
    result = runner.invoke(main, [str(sample_md)])
    assert result.exit_code == 0
    mock_convert.assert_called_once()
    call_args = mock_convert.call_args
    assert call_args.args[0] == [sample_md]
    assert call_args.args[1] == sample_md.with_suffix(".pdf")


@patch("print_md.cli.convert")
def test_single_file_custom_output(mock_convert, runner, sample_md, tmp_path):
    out = tmp_path / "out.pdf"
    result = runner.invoke(main, [str(sample_md), "-o", str(out)])
    assert result.exit_code == 0
    mock_convert.assert_called_once()
    assert mock_convert.call_args.args[1] == out


@patch("print_md.cli.convert")
def test_batch_mode(mock_convert, runner, tmp_path):
    f1 = tmp_path / "a.md"
    f2 = tmp_path / "b.md"
    f1.write_text("# A\n")
    f2.write_text("# B\n")
    result = runner.invoke(main, [str(f1), str(f2)])
    assert result.exit_code == 0
    assert mock_convert.call_count == 2


@patch("print_md.cli.convert")
def test_merge_mode(mock_convert, runner, tmp_path):
    f1 = tmp_path / "a.md"
    f2 = tmp_path / "b.md"
    f1.write_text("# A\n")
    f2.write_text("# B\n")
    out = tmp_path / "merged.pdf"
    result = runner.invoke(main, [str(f1), str(f2), "--merge", "-o", str(out)])
    assert result.exit_code == 0
    mock_convert.assert_called_once()
    assert mock_convert.call_args.args[0] == [f1, f2]
    assert mock_convert.call_args.args[1] == out


@patch("print_md.cli.convert")
def test_theme_option(mock_convert, runner, sample_md):
    result = runner.invoke(main, [str(sample_md), "--theme", "academic"])
    assert result.exit_code == 0
    assert mock_convert.call_args.kwargs["theme"] == "academic"


@patch("print_md.cli.convert")
def test_engine_option(mock_convert, runner, sample_md):
    result = runner.invoke(main, [str(sample_md), "--engine", "latex"])
    assert result.exit_code == 0
    assert mock_convert.call_args.kwargs["engine"] == "latex"


@patch("print_md.cli.convert")
def test_toc_options(mock_convert, runner, sample_md):
    result = runner.invoke(main, [str(sample_md), "--toc", "--toc-depth", "2"])
    assert result.exit_code == 0
    assert mock_convert.call_args.kwargs["toc"] is True
    assert mock_convert.call_args.kwargs["toc_depth"] == 2


@patch("print_md.cli.convert")
def test_font_options(mock_convert, runner, sample_md):
    result = runner.invoke(main, [
        str(sample_md),
        "--font", "Times New Roman",
        "--code-font", "Fira Code",
        "--font-size", "12pt",
    ])
    assert result.exit_code == 0
    assert mock_convert.call_args.kwargs["font"] == "Times New Roman"
    assert mock_convert.call_args.kwargs["code_font"] == "Fira Code"
    assert mock_convert.call_args.kwargs["font_size"] == "12pt"


@patch("print_md.cli.convert")
def test_paper_and_margin(mock_convert, runner, sample_md):
    result = runner.invoke(main, [str(sample_md), "--paper", "letter", "--margin", "1in"])
    assert result.exit_code == 0
    assert mock_convert.call_args.kwargs["paper"] == "letter"
    assert mock_convert.call_args.kwargs["margin"] == "1in"


@patch("print_md.cli.convert")
def test_quiet_mode(mock_convert, runner, sample_md):
    result = runner.invoke(main, [str(sample_md), "-q"])
    assert result.exit_code == 0
    assert mock_convert.call_args.kwargs["quiet"] is True


@patch("print_md.cli.convert")
def test_verbose_mode(mock_convert, runner, sample_md):
    result = runner.invoke(main, [str(sample_md), "-v"])
    assert result.exit_code == 0
    assert mock_convert.call_args.kwargs["verbose"] is True
