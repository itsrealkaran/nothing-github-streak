"""SVG frame shared by one card. The dot grid never sets body copy."""

from nothing import GLYPHS, theme


def dots(text, x, y, fill, scale=2.4):
    step = scale + 1.1
    parts = []
    cursor = x
    for char in text:
        grid = GLYPHS[char]
        for row, bits in enumerate(grid):
            for col, bit in enumerate(bits):
                if bit == "1":
                    cx = cursor + col * step + scale / 2
                    cy = y + row * step + scale / 2
                    parts.append(
                        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{scale / 2:.2f}" fill="{fill}"/>'
                    )
        cursor += 5 * step + scale
    return "".join(parts), cursor - x


def open_svg(mode, width, height, title):
    colors = theme(mode)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img">'
        f"<title>{title}</title>"
        f'<rect width="{width}" height="{height}" fill="{colors["bg"]}"/>'
        f'<rect x="28" y="26" width="8" height="8" fill="{colors["mark"]}"/>'
    )


def label(x, y, text, fill, size=13, tracking=0.4):
    return (
        f'<text x="{x}" y="{y}" fill="{fill}" '
        f'font-family="ui-monospace, Geist Mono, monospace" '
        f'font-size="{size}" letter-spacing="{tracking}">{text}</text>'
    )
