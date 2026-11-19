"""Streak card. Mini is the current run. The current number is the dot grid."""

import sys
from pathlib import Path

from frame import dots, label, open_svg
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
    scale = 4
    name, _ = dots("STREAK", 28, 12, colors["fg"], scale=1.15)
    figure, _width = dots(str(data["current"]), 16, 76, colors["figure"], scale=scale)
    return "\n".join([
        open_svg(mode, 220, 148, f"{data['login']} streak", mark=6, margin=14),
        name,
        figure,
        label(16, 130, "Current", colors["muted"], 11, 0.3),
        "</svg>",
    ])


def _compact(mode, colors, data):
    return _stats(mode, colors, data, 495, 168, 22, 11, 10, 96, 124, 140, 3.2, 52, 152)


def _regular(mode, colors, data):
    return _stats(mode, colors, data, 495, 195, 28, 12, 11, 108, 146, 164, 4.2, 56, 178)


def _wide(mode, colors, data):
    return _stats(mode, colors, data, 896, 220, 40, 13, 12, 120, 164, 184, 5.4, 56, 200)


def _glyph_figure(text, center, baseline, size, fill, scale):
    """Center a dot-grid number on the same line as a mono figure."""
    step = scale + 1.1
    height = 6 * step + scale
    top = baseline - size * 0.28 - height / 2
    _drawn, width = dots(text, 0, top, fill, scale=scale)
    drawn, _width = dots(text, center - (width - step) / 2, top, fill, scale=scale)
    return drawn


def _stats(mode, colors, data, width, height, number, label_size, range_size, number_y, label_y, range_y, scale, rule_top, rule_bottom):
    """Total, current, and longest. The current number is the dot grid."""
    name, _ = dots("STREAK", 40, 16, colors["fg"], scale=1.8)
    span = width / 3
    centers = tuple(round(span * (index + 0.5), 1) for index in range(3))
    columns = (
        (f"{data['total']:,}", "Contributions", data["total_range"], False),
        (str(data["current"]), "Current", data["current_range"], True),
        (str(data["longest"]), "Longest", data["longest_range"], False),
    )
    parts = [open_svg(mode, width, height, f"{data['login']} streak"), name]
    for rule_x in (round(span, 1), round(span * 2, 1)):
        parts.append(
            f'<line x1="{rule_x:.1f}" y1="{rule_top}" x2="{rule_x:.1f}" y2="{rule_bottom}" stroke="{colors["rule"]}"/>'
        )
    for center, (figure, caption, dates, glyph) in zip(centers, columns):
        if glyph:
            parts.append(_glyph_figure(figure, center, number_y, number, colors["figure"], scale))
        else:
            parts.append(label(center, number_y, figure, colors["figure"], number, -0.6, anchor="middle"))
        parts.append(label(center, label_y, caption, colors["muted"], label_size, 0.2, anchor="middle"))
        parts.append(label(center, range_y, dates, colors["fg"], range_size, 0, anchor="middle"))
    parts.append("</svg>")
    return "\n".join(parts)


def _variant(card, login, mode, size, filename):
    url = f"https://github.com/itsrealkaran/nothing-github-streak?username={login}&theme={mode}&size={size}"
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
    lines = [f"# {data['login']}", "", "Mini is the current run, drawn in the dot grid. Compact, regular, and wide put contributions, the current run, and the longest run in three columns.", ""]
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
