// Tests for the page's pure calculations (site/core.js).
//   node --test pipeline/tests/test_core.mjs
// Also run from the Python suite when Node is available.
import { test } from "node:test";
import assert from "node:assert/strict";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const core = require("../../site/core.js");
const close = (a, b, tol = 1e-9) => assert.ok(Math.abs(a - b) <= tol * Math.max(1, Math.abs(b)), `${a} vs ${b}`);

test("decomposition adds up and uses average weights", () => {
  // Share 10% → 6%, total 100 → 300: holdings 10 → 18.
  const d = core.decompose(0.10, 0.06, 100, 300);
  close(d.w0, 10); close(d.w1, 18); close(d.net, 8);
  close(d.growth, 0.08 * 200);        // average share × change of total = 16
  close(d.share, -0.04 * 200);        // change of share × average total = −8
  close(d.growth + d.share, d.net);
});

test("decomposition is symmetric: swapping years flips every term", () => {
  const a = core.decompose(0.2, 0.3, 50, 80), b = core.decompose(0.3, 0.2, 80, 50);
  close(a.growth, -b.growth); close(a.share, -b.share); close(a.net, -b.net);
});

test("annuity matches the textbook formula and the zero-rate limit", () => {
  // 25 yearly payments at 4%: 0.0640120 per euro borrowed.
  close(core.annuity(0.04, 25), 0.064012, 1e-5);
  close(core.annuity(0, 25), 1 / 25);
  close(core.annuity(1e-6, 25), 1 / 25, 1e-4);   // continuous at r → 0
});

test("poorest holding: uniform distribution, negative bins", () => {
  // Uniform: the poorest x% hold x%.
  const bins = Array.from({ length: 100 }, (_, i) => ({ lo: i, hi: i + 1, m: 1 }));
  close(core.poorestHolding(bins, 0.25), 0.25);
  // A negative first bin must be offset before the target is reached.
  const neg = [{ lo: 0, hi: 10, m: -5 }, ...Array.from({ length: 90 }, (_, i) => ({ lo: 10 + i, hi: 11 + i, m: 1 }))];
  // total = 85; target 10% = 8.5 → need 13.5 units of positive mass after −5.
  close(core.poorestHolding(neg, 0.10), (10 + 13.5) / 100);
});

test("smoothing uses existing neighbouring years only", () => {
  const out = core.smooth([1900, 1910, 1911, 1912], [1, 10, 20, 30]);
  assert.equal(out[0], 1);              // no neighbour within a year
  close(out[1], 15); close(out[2], 20); close(out[3], 25);
});

test("CPI factor holds the 1950 ratio before 1950", () => {
  const deflator = { 1950: 0.05, 1960: 0.1 }, years = [1950, 1960], vals = [0.04, 0.1];
  close(core.cpiFactor(1949, deflator, years, vals), 1.25);
  close(core.cpiFactor(1950, deflator, years, vals), 1.25);
  close(core.cpiFactor(1960, deflator, years, vals), 1);
});

test("slider steps over gaps in both directions", () => {
  const years = [1900, 1902, 1905, 1910];
  assert.equal(core.stepYear(years, 1900, 1901), 1902);
  assert.equal(core.stepYear(years, 1905, 1904), 1902);
  assert.equal(core.stepYear(years, 1910, 1911), 1910);
});
