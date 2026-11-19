"use strict";

const { dots, label, openSvg } = require("./frame");
const { theme } = require("./nothing");
const { commas, div, f, fixed, mul, pyRound, sub } = require("./format");

function render(mode, size, data) {
  const colors = theme(mode);
  if (size === "mini") return mini(mode, colors, data);
  if (size === "compact") return stats(mode, colors, data, 495, 168, 22, 11, 10, 96, 124, 140, 3.2, 52, 152);
  if (size === "wide") return stats(mode, colors, data, 896, 220, 40, 13, 12, 120, 164, 184, 5.4, 56, 200);
  return stats(mode, colors, data, 495, 195, 28, 12, 11, 108, 146, 164, 4.2, 56, 178);
}

function mini(mode, colors, data) {
  const scale = 4;
  const [name] = dots("STREAK", 28, 12, colors.fg, 1.15);
  const [figure] = dots(String(data.current), 16, 76, colors.figure, scale);
  return [
    openSvg(mode, 220, 148, data.login + " streak", 6, 14),
    name,
    figure,
    label(16, 130, "Current", colors.muted, 11, 0.3),
    "</svg>",
  ].join("\n");
}

function glyphFigure(text, center, baseline, size, fill, scale) {
  const step = scale + 1.1;
  const height = 6 * step + scale;
  const top = baseline - size * 0.28 - height / 2;
  const [, width] = dots(text, 0, top, fill, scale);
  const [drawn] = dots(text, sub(center, div(sub(f(width), step), 2)), top, fill, scale);
  return drawn;
}

function stats(mode, colors, data, width, height, number, labelSize, rangeSize, numberY, labelY, rangeY, scale, ruleTop, ruleBottom) {
  const [name] = dots("STREAK", 40, 16, colors.fg, 1.8);
  const span = div(width, 3);
  const centers = [0, 1, 2].map((index) => pyRound(mul(span, index + 0.5), 1));
  const columns = [
    [commas(data.total), "Contributions", data.total_range, false],
    [String(data.current), "Current", data.current_range, true],
    [String(data.longest), "Longest", data.longest_range, false],
  ];
  const parts = [openSvg(mode, width, height, data.login + " streak"), name];
  [pyRound(span, 1), pyRound(mul(span, 2), 1)].forEach((ruleX) => {
    parts.push(
      `<line x1="${fixed(ruleX, 1)}" y1="${ruleTop}" x2="${fixed(ruleX, 1)}" y2="${ruleBottom}" stroke="${colors.rule}"/>`
    );
  });
  centers.forEach((center, index) => {
    const [figure, caption, dates, glyph] = columns[index];
    if (glyph) parts.push(glyphFigure(figure, center, numberY, number, colors.figure, scale));
    else parts.push(label(center, numberY, figure, colors.figure, number, -0.6, "middle"));
    parts.push(label(center, labelY, caption, colors.muted, labelSize, 0.2, "middle"));
    parts.push(label(center, rangeY, dates, colors.fg, rangeSize, 0, "middle"));
  });
  parts.push("</svg>");
  return parts.join("\n");
}

module.exports = { render };
