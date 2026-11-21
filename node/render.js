"use strict";

const { dots, label, openSvg } = require("./frame");
const { theme } = require("./nothing");
const { commas, div, f, fixed, mul, pyRound, sub } = require("./format");

function render(mode, size, data, border = true) {
  const colors = theme(mode);
  if (size === "mini") return mini(mode, colors, data, border);
  if (size === "compact") {
    return stats(mode, colors, data, 495, 168, 22, 11, 10, 96, 124, 140, 3.2, 52, 152, true, data.current === 1 ? "DAY" : "DAYS", border);
  }
  if (size === "wide") {
    return stats(mode, colors, data, 896, 220, 40, 13, 12, 120, 164, 184, 5.4, 56, 200, false, data.current === 1 ? "DAY" : "DAYS", border);
  }
  return stats(mode, colors, data, 440, 195, 28, 12, 11, 108, 146, 164, 4.2, 56, 178, false, "D", border);
}

function mini(mode, colors, data, border) {
  const scale = 4;
  const step = scale + 1.1;
  const [name] = dots("STREAK", 28, 12, colors.fg, 1.15);
  const [fire] = dots("f", 14, 68, colors.mark, 1.5);
  const [figure, width] = dots(String(data.current), 52, 76, colors.figure, scale);
  const unitScale = 1.5;
  const unit = data.current === 1 ? "DAY" : "DAYS";
  const unitTop = 76 + (6 * step + scale) - (6 * (unitScale + 1.1) + unitScale);
  const [days] = dots(unit, 52 + width - step + 6, unitTop, colors.figure, unitScale);
  return [
    openSvg(mode, 220, 148, data.login + " streak", 6, 14, border),
    name,
    fire,
    figure,
    days,
    label(16, 130, "Current " + data.current_range, colors.muted, 11, 0.3),
    "</svg>",
  ].join("\n");
}

function currentMark(text, center, baseline, size, colors, scale, unit) {
  const step = scale + 1.1;
  const height = 6 * step + scale;
  const top = baseline - size * 0.28 - height / 2;
  const [, advance] = dots(text, 0, top, colors.figure, scale);
  const visual = advance - step;
  const fireScale = scale >= 5 ? 1.9 : scale >= 4 ? 1.5 : 1.15;
  const unitScale = scale >= 5 ? 2.0 : scale >= 4 ? 1.55 : 1.2;
  const fireStep = fireScale + 1.1;
  const unitStep = unitScale + 1.1;
  const [, fireAdvance] = dots("f", 0, 0, colors.mark, fireScale);
  const [, unitAdvance] = dots(unit, 0, 0, colors.figure, unitScale);
  const gap = 6;
  const fireVisual = fireAdvance - fireStep;
  const group = fireVisual + gap + visual + gap + (unitAdvance - unitStep);
  const left = center - group / 2;
  const fireTop = top + (height - (17 * fireStep + fireScale)) / 2;
  const unitTop = top + height - (6 * unitStep + unitScale);
  const [fire] = dots("f", left, fireTop, colors.mark, fireScale);
  const [figure] = dots(text, left + fireVisual + gap, top, colors.figure, scale);
  const [mark] = dots(unit, left + fireVisual + gap + visual + gap, unitTop, colors.figure, unitScale);
  return fire + figure + mark;
}

function stats(mode, colors, data, width, height, number, labelSize, rangeSize, numberY, labelY, rangeY, scale, ruleTop, ruleBottom, pair, unit = "D", border = true) {
  const [name] = dots("STREAK", 40, 16, colors.fg, 1.8);
  const columns = [
    [String(data.current), "Current", data.current_range, true],
    [String(data.longest), "Longest", data.longest_range, false],
  ];
  if (!pair) columns.unshift([commas(data.total), "Contributions", data.total_range, false]);
  const span = div(width, columns.length);
  const centers = columns.map((_, index) => pyRound(mul(span, index + 0.5), 1));
  const parts = [openSvg(mode, width, height, data.login + " streak", 8, 20, border), name];
  columns.slice(1).forEach((_, index) => {
    const ruleX = pyRound(mul(span, index + 1), 1);
    parts.push(
      `<line x1="${fixed(ruleX, 1)}" y1="${ruleTop}" x2="${fixed(ruleX, 1)}" y2="${ruleBottom}" stroke="${colors.rule}"/>`
    );
  });
  centers.forEach((center, index) => {
    const [figure, caption, dates, glyph] = columns[index];
    if (glyph) parts.push(currentMark(figure, center, numberY, number, colors, scale, unit));
    else parts.push(label(center, numberY, figure, colors.figure, number, -0.6, "middle"));
    parts.push(label(center, labelY, caption, colors.muted, labelSize, 0.2, "middle"));
    parts.push(label(center, rangeY, dates, colors.fg, rangeSize, 0, "middle"));
  });
  parts.push("</svg>");
  return parts.join("\n");
}

module.exports = { render };
