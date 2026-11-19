"use strict";

const { addDays, contributionTotals, dayKey, dateOnly, monthDay, monthDayYear, parseDay, utcNow } = require("./github");

async function load(login) {
  const data = await contributionTotals(login);
  const parsed = data.days.map(([day, count]) => [day, count]);
  parsed.sort((a, b) => (a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0));
  let longest = 0;
  let current = 0;
  let run = 0;
  let longestStart = null;
  let longestEnd = null;
  let runStart = null;
  let previous = null;
  for (const [day, count] of parsed) {
    if (count <= 0) {
      run = 0;
      runStart = null;
      previous = day;
      continue;
    }
    const yesterday = dayKey(addDays(parseDay(day), -1));
    if (previous === yesterday && run) run += 1;
    else {
      run = 1;
      runStart = day;
    }
    if (run > longest) {
      longest = run;
      longestStart = runStart;
      longestEnd = day;
    }
    previous = day;
  }
  const today = dayKey(dateOnly(utcNow()));
  const byDay = new Map(parsed);
  let cursor = (byDay.get(today) || 0) ? today : dayKey(addDays(parseDay(today), -1));
  let currentStart = null;
  let currentEnd = null;
  while ((byDay.get(cursor) || 0) > 0) {
    if (currentEnd == null) currentEnd = cursor;
    currentStart = cursor;
    current += 1;
    cursor = dayKey(addDays(parseDay(cursor), -1));
  }
  return {
    login: data.login,
    total: data.allTime,
    current,
    longest,
    current_range: daySpan(currentStart, currentEnd),
    longest_range: daySpan(longestStart, longestEnd),
    total_range: "Since " + monthDayYear(data.created),
    days: data.days,
  };
}

function daySpan(start, end) {
  if (!start || !end) return "No streak yet";
  const left = parseDay(start);
  const right = parseDay(end);
  if (start === end) return monthDay(left);
  if (left.getUTCFullYear() === right.getUTCFullYear()) return monthDay(left) + " to " + monthDay(right);
  return monthDayYear(left) + " to " + monthDayYear(right);
}

module.exports = { load };
