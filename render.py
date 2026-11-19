"""Streak card. Five Nothing modes."""

import json
from pathlib import Path

from frame import dots, label, open_svg
from nothing import MODES, theme

ROOT = Path(__file__).resolve().parent


def render(mode, data):
    colors = theme(mode)
    name, _ = dots("STREAK", 46, 22, colors["fg"], scale=2.2)
    parts = [
        open_svg(mode, 640, 250, "Contribution streak, including private days"),
        name,
        label(28, 150, f'{data["current"]}', colors["figure"], 54, -1),
        label(220, 150, f'{data["longest"]}', colors["figure"], 54, -1),
        label(420, 150, f'{data["total"]:,}', colors["figure"], 36, -0.6),
        label(28, 180, "Current", colors["muted"], 13, 0.6),
        label(220, 180, "Longest", colors["muted"], 13, 0.6),
        label(420, 180, "Total", colors["muted"], 13, 0.6),
        f'<line x1="28" y1="204" x2="612" y2="204" stroke="{colors["rule"]}"/>',
        label(28, 230, data["longest_range"], colors["fg"], 14, 0.3),
        "</svg>",
    ]
    return "\n".join(parts)


def main():
    data = json.loads((ROOT / "sample.json").read_text())
    out = ROOT / "dist"
    out.mkdir(exist_ok=True)
    for mode in MODES:
        (out / f"{mode}.svg").write_text(render(mode, data))
        print(mode)


if __name__ == "__main__":
    main()
