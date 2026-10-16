// Pure calculations used by the page, kept separate so they can be tested
// (pipeline/tests/test_core.mjs runs them with Node against hand-computed cases).
(function (root) {
  "use strict";

  // Change of a slice between two years, split exactly into a growth effect
  // (average share × change of the total) and a share effect (change of share
  // × average total): a two-factor Shapley decomposition.
  function decompose(s0, s1, T0, T1) {
    return {
      w0: s0 * T0, w1: s1 * T1,
      growth: (s0 + s1) / 2 * (T1 - T0),
      share: (s1 - s0) * (T0 + T1) / 2,
      net: s1 * T1 - s0 * T0
    };
  }

  // Yearly payment per euro borrowed, rate r, n yearly instalments.
  function annuity(r, n) {
    return r === 0 ? 1 / n : r / (1 - Math.pow(1 + r, -n));
  }

  // Share of the population, counted from the poorest, whose combined
  // holdings equal `target` (a share of the total). bins: [{lo, hi, m}] with
  // lo/hi in percent ranks and m = average × width; negative bins lower the
  // running total.
  function poorestHolding(bins, target) {
    const total = bins.reduce((s, b) => s + b.m, 0);
    let cum = 0;
    for (const b of bins) {
      if (b.m <= 0) { cum += b.m; continue; }
      if ((cum + b.m) / total >= target) return (b.lo + (target * total - cum) / b.m * (b.hi - b.lo)) / 100;
      cum += b.m;
    }
    return 1;
  }

  // Centred average over the years that exist within ±1 year; ends use the
  // two available years.
  function smooth(years, arr) {
    return arr.map((v, i) => {
      if (v == null) return v;
      const w = [];
      for (let j = Math.max(0, i - 2); j <= Math.min(arr.length - 1, i + 2); j++) {
        if (Math.abs(years[j] - years[i]) <= 1 && arr[j] != null) w.push(arr[j]);
      }
      return w.length >= 2 ? w.reduce((a, b) => a + b, 0) / w.length : v;
    });
  }

  // Ratio that converts WID constant euros to consumer-price euros: deflator /
  // CPI, both 1 in the base year; years before 1950 keep the 1950 ratio.
  function cpiFactor(y, deflator, cpiYears, cpiValues) {
    const yy = Math.max(y, 1950), j = cpiYears.indexOf(yy);
    return j < 0 ? 1 : deflator[yy] / cpiValues[j];
  }

  // Next year with data in the direction of travel (keyboard-friendly slider).
  function stepYear(years, current, requested) {
    if (requested > current) return years.find(y => y >= requested) ?? current;
    if (requested < current) return [...years].reverse().find(y => y <= requested) ?? current;
    return current;
  }

  const api = { decompose, annuity, poorestHolding, smooth, cpiFactor, stepYear };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.PieCore = api;
})(typeof window !== "undefined" ? window : globalThis);
