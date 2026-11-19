"""Streak card for any GitHub username."""

import sys
from pathlib import Path

from frame import dots, label, open_svg
from github_user import streak
from nothing import MODES, SCALE, SIZES, theme

ROOT = Path(__file__).resolve().parent


def render(mode, size, data):
    scale = SCALE[size]
    colors = theme(mode)
    width = int(640 * scale)
    height = int(260 * scale)

    def n(value):
        return round(value * scale, 1)

    name, _ = dots("STREAK", n(46), n(22), colors["fg"], scale=2.2 * scale)
    parts = [
        open_svg(mode, width, height, f"{data['login']} streak"),
        name,
        label(n(28), n(150), f"{data['current']}", colors["figure"], n(54), -1),
        label(n(210), n(150), f"{data['longest']}", colors["figure"], n(54), -1),
        label(n(400), n(150), f"{data['total']:,}", colors["figure"], n(36), -0.6),
        label(n(28), n(180), "Current", colors["muted"], n(13), 0.6),
        label(n(210), n(180), "Longest", colors["muted"], n(13), 0.6),
        label(n(400), n(180), "Total", colors["muted"], n(13), 0.6),
        f'<line x1="{n(28)}" y1="{n(206)}" x2="{width - n(28)}" y2="{n(206)}" stroke="{colors["rule"]}"/>',
        label(n(28), n(234), f"@{data['login']} · {data['longest_range']}", colors["fg"], n(14), 0.3),
        "</svg>",
    ]
    return "\n".join(parts)


def main():
    login = sys.argv[1] if len(sys.argv) > 1 else "itsrealkaran"
    data = streak(login)
    out = ROOT / "dist" / data["login"]
    out.mkdir(parents=True, exist_ok=True)
    lines = [f"# {data['login']}", "", "Username, mode, and size.", ""]
    for mode in MODES:
        lines += [f"## {mode}", ""]
        for size in SIZES:
            filename = f"{mode}-{size}.svg"
            (out / filename).write_text(render(mode, size, data))
            lines += [f"### {size}", "", f"![{mode} {size}](dist/{data['login']}/{filename})", ""]
            print(data["login"], mode, size)
    (ROOT / "DUMMY.md").write_text("\n".join(lines))


if __name__ == "__main__":
    main()
