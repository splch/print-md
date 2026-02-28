"""Dependency checking for external binaries (pandoc, typst, latex)."""

import shutil
import subprocess


def _run_version(cmd: str) -> str | None:
    """Run `cmd --version` and return the first line, or None."""
    path = shutil.which(cmd)
    if path is None:
        return None
    try:
        result = subprocess.run(
            [path, "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        first_line = result.stdout.strip().splitlines()[0] if result.stdout.strip() else None
        return first_line
    except (subprocess.TimeoutExpired, OSError, IndexError):
        return None


def check_pandoc() -> tuple[bool, str | None]:
    """Return (available, version_string) for pandoc."""
    ver = _run_version("pandoc")
    return (ver is not None, ver)


def check_typst() -> tuple[bool, str | None]:
    """Return (available, version_string) for typst."""
    ver = _run_version("typst")
    return (ver is not None, ver)


def check_latex() -> tuple[bool, str | None]:
    """Return (available, version_string) for xelatex."""
    ver = _run_version("xelatex")
    return (ver is not None, ver)


def require_pandoc() -> str:
    """Return pandoc path or raise SystemExit."""
    path = shutil.which("pandoc")
    if path is None:
        raise SystemExit(
            "Error: pandoc is not installed.\n"
            "  Install: https://pandoc.org/installing.html\n"
            "  macOS:   brew install pandoc"
        )
    return path


def require_engine(engine: str) -> str:
    """Return engine binary path or raise SystemExit."""
    if engine == "typst":
        path = shutil.which("typst")
        if path is None:
            raise SystemExit(
                "Error: typst is not installed.\n"
                "  Install: https://github.com/typst/typst#installation\n"
                "  macOS:   brew install typst"
            )
        return path
    elif engine == "latex":
        path = shutil.which("xelatex")
        if path is None:
            raise SystemExit(
                "Error: xelatex is not installed.\n"
                "  Install a TeX distribution:\n"
                "  macOS:   brew install --cask mactex"
            )
        return path
    else:
        raise SystemExit(f"Error: unknown engine '{engine}'. Use 'typst' or 'latex'.")


def format_check_deps() -> str:
    """Return a formatted status string for --check-deps."""
    lines = ["Dependency status:\n"]

    pandoc_ok, pandoc_ver = check_pandoc()
    if pandoc_ok:
        lines.append(f"  pandoc:  OK  ({pandoc_ver})")
    else:
        lines.append("  pandoc:  MISSING  (brew install pandoc)")

    typst_ok, typst_ver = check_typst()
    if typst_ok:
        lines.append(f"  typst:   OK  ({typst_ver})")
    else:
        lines.append("  typst:   MISSING  (brew install typst)")

    latex_ok, latex_ver = check_latex()
    if latex_ok:
        lines.append(f"  xelatex: OK  ({latex_ver})")
    else:
        lines.append("  xelatex: not found (optional, for --engine=latex)")

    return "\n".join(lines)
