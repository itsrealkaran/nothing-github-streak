"""Streak card. Compact is the current run. Regular is three numbers. Wide adds glyphs."""

import sys
from pathlib import Path

from frame import dots, label, open_svg, week_glyphs
from github_user import streak
from nothing import MODES, SIZES, theme

ROOT = Path(__file__).resolve().parent


def render(mode, size, data):
    colors = theme(mode)
    if size == "mini":
        return _mini(mode, colors, data)
    if size == "compact":
        return _compact(mode, colors, data)
    if size == "wide":
        return _wide(mode, colors, data)
    return _regular(mode, colors, data)


def _mini(mode, colors, data):
    name, _ = dots("STREAK", 28, 12, colors["fg"], scale=1.15)
    return "\n".join([
        open_svg(mode, 220, 148, f"{data['login']} streak", mark=6, margin=14),
        name,
        label(16, 108, str(data["current"]), colors["figure"], 36, -1),
        label(16, 130, "Current", colors["muted"], 11, 0.3),
        "</svg>",
    ])


def _compact(mode, colors, data):
    name, _ = dots("STREAK", 40, 16, colors["fg"], scale=1.8)
    return "\n".join([
        open_svg(mode, 495, 132, f"{data['login']} streak"),
        name,
        label(20, 108, str(data["current"]), colors["figure"], 42, -1),
        label(160, 96, "Current days", colors["muted"], 13, 0.4),
        label(160, 116, f"@{data['login']}", colors["fg"], 13, 0.2),
        "</svg>",
    ])


def _regular(mode, colors, data):
    name, _ = dots("STREAK", 40, 16, colors["fg"], scale=1.8)
    return "\n".join([
        open_svg(mode, 495, 195, f"{data['login']} streak"),
        name,
        label(20, 120, str(data["current"]), colors["figure"], 36, -1),
        label(150, 120, str(data["longest"]), colors["figure"], 36, -1),
        label(300, 120, f"{data['total']:,}", colors["figure"], 28, -0.6),
        label(20, 146, "Current", colors["muted"], 12, 0.4),
        label(150, 146, "Longest", colors["muted"], 12, 0.4),
        label(300, 146, "Total", colors["muted"], 12, 0.4),
        f'<line x1="20" y1="162" x2="475" y2="162" stroke="{colors["rule"]}"/>',
        label(20, 182, f"@{data['login']} · {data['longest_range']}", colors["fg"], 12, 0.2),
        "</svg>",
    ])


def _wide(mode, colors, data):
    name, _ = dots("STREAK", 40, 16, colors["fg"], scale=1.8)
    glyphs = week_glyphs(data["days"], 32, 310, 78, 12, 3, colors["figure"], colors["rule"])
    return "\n".join([
        open_svg(mode, 896, 240, f"{data['login']} streak"),
        name,
        label(20, 110, str(data["current"]), colors["figure"], 48, -1),
        label(20, 140, "Current", colors["muted"], 13, 0.4),
        label(20, 190, f"Longest {data['longest']} · {data['longest_range']}", colors["fg"], 13, 0.2),
        glyphs,
        "</svg>",
    ])


def _variant(card, login, mode, size, filename):
    url = f"https://github.com/itsrealkaran/{card}?username={login}&theme={mode}&size={size}"
    return [
        f"**{card}** · {mode} · {size}",
        "",
        f"`{url}`",
        "",
        f"![{card} {mode} {size}](dist/{login}/{filename})",
        "",
    ]


def main():
    login = sys.argv[1] if len(sys.argv) > 1 else "itsrealkaran"
    data = streak(login)
    out = ROOT / "dist" / data["login"]
    out.mkdir(parents=True, exist_ok=True)
    lines = [f"# {data['login']}", "", "Compact is the current run. Regular is three numbers. Wide adds the glyph weeks.", ""]
    for mode in MODES:
        lines += [f"## {mode}", ""]
        for size in SIZES:
            filename = f"{mode}-{size}.svg"
            (out / filename).write_text(render(mode, size, data))
            lines += _variant("streak", data["login"], mode, size, filename)
            print(data["login"], mode, size)
    (ROOT / "DUMMY.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
