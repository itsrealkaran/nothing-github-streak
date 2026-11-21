"""Streak card. Mini is the current run. The current number is the dot grid."""

import sys
from pathlib import Path

from frame import dots, label, open_svg
from github_user import streak
from nothing import MODES, SIZES, theme

ROOT = Path(__file__).resolve().parent


def render(mode, size, data, border=True):
    colors = theme(mode)
    if size == "mini":
        return _mini(mode, colors, data, border)
    if size == "compact":
        return _compact(mode, colors, data, border)
    if size == "wide":
        return _wide(mode, colors, data, border)
    return _regular(mode, colors, data, border)


def _mini(mode, colors, data, border):
    scale = 4
    step = scale + 1.1
    name, _ = dots("STREAK", 28, 12, colors["fg"], scale=1.15)
    fire, _width = dots("f", 14, 68, colors["mark"], scale=1.5)
    figure, width = dots(str(data["current"]), 52, 76, colors["figure"], scale=scale)
    unit_scale = 1.5
    unit = "DAY" if data["current"] == 1 else "DAYS"
    unit_top = 76 + (6 * step + scale) - (6 * (unit_scale + 1.1) + unit_scale)
    days, _width = dots(unit, 52 + width - step + 6, unit_top, colors["figure"], scale=unit_scale)
    return "\n".join([
        open_svg(mode, 220, 148, f"{data['login']} streak", mark=6, margin=14, border=border),
        name,
        fire,
        figure,
        days,
        label(16, 130, f"Current {data['current_range']}", colors["muted"], 11, 0.3),
        "</svg>",
    ])


def _compact(mode, colors, data, border):
    unit = "DAY" if data["current"] == 1 else "DAYS"
    return _stats(mode, colors, data, 495, 168, 22, 11, 10, 96, 124, 140, 3.2, 52, 152, pair=True, unit=unit, border=border)


def _regular(mode, colors, data, border):
    return _stats(mode, colors, data, 408, 195, 22, 12, 11, 108, 146, 164, 4.2, 56, 178, border=border)


def _wide(mode, colors, data, border):
    unit = "DAY" if data["current"] == 1 else "DAYS"
    return _stats(mode, colors, data, 896, 220, 40, 13, 12, 120, 164, 184, 5.4, 56, 200, unit=unit, border=border)


def _current(text, center, baseline, size, colors, scale, unit="D"):
    """Flame, the current count, and the day mark, centered as one group."""
    step = scale + 1.1
    height = 6 * step + scale
    top = baseline - size * 0.28 - height / 2
    _drawn, advance = dots(text, 0, top, colors["figure"], scale=scale)
    visual = advance - step
    fire_scale, unit_scale = (1.9, 2.0) if scale >= 5 else (1.5, 1.55) if scale >= 4 else (1.15, 1.2)
    fire_step = fire_scale + 1.1
    unit_step = unit_scale + 1.1
    _fire, fire_advance = dots("f", 0, 0, colors["mark"], scale=fire_scale)
    _unit, unit_advance = dots(unit, 0, 0, colors["figure"], scale=unit_scale)
    gap = 6
    group = (fire_advance - fire_step) + gap + visual + gap + (unit_advance - unit_step)
    left = center - group / 2
    fire_top = top + (height - (17 * fire_step + fire_scale)) / 2
    unit_top = top + height - (6 * unit_step + unit_scale)
    fire, _width = dots("f", left, fire_top, colors["mark"], scale=fire_scale)
    figure, _width = dots(text, left + (fire_advance - fire_step) + gap, top, colors["figure"], scale=scale)
    unit_drawn, _width = dots(unit, left + (fire_advance - fire_step) + gap + visual + gap, unit_top, colors["figure"], scale=unit_scale)
    return fire + figure + unit_drawn


def _stats(mode, colors, data, width, height, number, label_size, range_size, number_y, label_y, range_y, scale, rule_top, rule_bottom, pair=False, unit="D", border=True):
    """Current and longest on compact. Regular and wide add the total."""
    name, _ = dots("STREAK", 40, 16, colors["fg"], scale=1.8)
    columns = (
        (str(data["current"]), "Current", data["current_range"], True),
        (str(data["longest"]), "Longest", data["longest_range"], False),
    )
    if not pair:
        columns = ((f"{data['total']:,}", "Contributions", data["total_range"], False),) + columns
    span = width / len(columns)
    centers = tuple(round(span * (index + 0.5), 1) for index in range(len(columns)))
    parts = [open_svg(mode, width, height, f"{data['login']} streak", border=border), name]
    for index in range(1, len(columns)):
        rule_x = round(span * index, 1)
        parts.append(
            f'<line x1="{rule_x:.1f}" y1="{rule_top}" x2="{rule_x:.1f}" y2="{rule_bottom}" stroke="{colors["rule"]}"/>'
        )
    for center, (figure, caption, dates, glyph) in zip(centers, columns):
        if glyph:
            parts.append(_current(figure, center, number_y, number, colors, scale, unit))
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
    lines = [f"# {data['login']}", "", "Mini is the current run, drawn in the dot grid. Compact puts the current run and the longest run side by side. Regular and wide add the total.", ""]
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
