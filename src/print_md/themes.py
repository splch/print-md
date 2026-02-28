"""Theme registry and resolution."""

from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent / "templates"

BUILTIN_THEMES = {
    "default": TEMPLATES_DIR / "default.typ",
    "academic": TEMPLATES_DIR / "academic.typ",
    "minimal": TEMPLATES_DIR / "minimal.typ",
}


def resolve_theme(name: str) -> Path:
    """Resolve a theme name to a template file path.

    Checks built-in names first, then treats as a file path.
    """
    if name in BUILTIN_THEMES:
        path = BUILTIN_THEMES[name]
        if not path.exists():
            raise SystemExit(f"Error: built-in theme '{name}' template not found at {path}")
        return path

    # Treat as file path
    path = Path(name)
    if not path.exists():
        available = ", ".join(sorted(BUILTIN_THEMES))
        raise SystemExit(
            f"Error: theme '{name}' not found.\n"
            f"  Built-in themes: {available}\n"
            f"  Or provide a path to a custom .typ file."
        )
    return path


def list_themes() -> str:
    """Return a formatted string listing available themes."""
    lines = ["Available themes:\n"]
    descriptions = {
        "default": "Modern, clean — sans-serif, gray code blocks, subtle rules",
        "academic": "Formal — serif, numbered sections, running headers",
        "minimal": "Sparse — small font, narrow margins, no decoration",
    }
    for name in sorted(BUILTIN_THEMES):
        desc = descriptions.get(name, "")
        lines.append(f"  {name:12s} {desc}")
    lines.append("\n  You can also pass a path to a custom .typ template file.")
    return "\n".join(lines)
