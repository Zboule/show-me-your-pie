"""Scenarios for the top of the wealth distribution.

WID's top g-percentile (p99.999–p100, ~530 adults) is lifted to the Forbes
billionaire total when WID's model is lower, from 1988 on (WIL Technical Note
2025/01). The scenarios below test that estimate against other evidence, in
both directions.

Rich-list scenarios (Challenges "500 fortunes")
-----------------------------------------------
Parameters are inspired by Garbinti, Goupille-Lebret & Piketty (2016, rev.
2017, WID WP 2016/6, appendix H), who compare the list with the top 0.001%:
families of 1, 10 or 15 members, 80% of members married (so one member is
1.8 equal-split adults on average), about 20% of the list's wealth held by
non-residents. For each year with a Challenges total RL (real euros):

    n      = 500 × members × 1.8      equal-split adults covered by the list
    RL_adj = RL × (1 − c)             wealth of resident adults
    W_n    = WID wealth of the richest n adults
    if RL_adj > W_n: the richest n get RL_adj, every other adult is scaled by
       s = (T − RL_adj) / (T − W_n), so total wealth T is unchanged (the same
       proportional rule WID uses for its own Forbes top-up)
    else: WID is kept.

The rule is one-sided on purpose: a list of the largest fortunes it could
identify is a lower bound on what the richest n adults own (unlisted assets,
fortunes it missed), so a list *below* WID says nothing about WID being too
high. Evidence that WID is too high comes from the ECB / Banque de France
scenario in build_data.py instead. `W_n` and `RL_adj` are exported every year
so the reader can see when the list is below WID.

W_n is read from WID's g-percentile averages. If the list covered fewer
adults than WID's top g-percentile (~530), that bin would be split with a
Pareto rule whose alpha comes from WID's threshold chain p99.99 → p99.998
(the bin's own entry threshold jumps far above the chain, e.g. €95M → €799M
in 2024, implying an alpha below 1). With the scenarios defined here the list
always covers at least 900 adults, so the top bin is taken whole and the
Pareto rule is not used.
"""
import math

ADULTS_PER_MEMBER = 1.8  # 80% of members married, equal split: 0.2 × 1 + 0.8 × 2
SCENARIOS = {
    "ggp_central": {"members_per_family": 10, "non_resident_share": 0.2,
                    "label": "Rich list, central assumptions (10 members per family, 20% non-resident)"},
    "ggp_low": {"members_per_family": 1, "non_resident_share": 0.2,
                "label": "Rich list, one member per family, 20% non-resident"},
    "no_cut": {"members_per_family": 1, "non_resident_share": 0.0,
               "label": "Rich list, one member per family, no non-resident cut (beyond published assumptions)"},
}
LIST_SIZE = 500


def adults_covered(params):
    return LIST_SIZE * params["members_per_family"] * ADULTS_PER_MEMBER


def chain_alpha(t_low, t_high, rank_ratio):
    """Local Pareto alpha between two thresholds: the top share falls by
    `rank_ratio` while the threshold rises from t_low to t_high."""
    if not (0 < t_low < t_high):
        raise ValueError(f"thresholds must increase: {t_low}, {t_high}")
    alpha = math.log(rank_ratio) / math.log(t_high / t_low)
    if alpha <= 1:
        raise ValueError(f"alpha {alpha:.2f} ≤ 1 implies an infinite mean")
    return alpha


def top_n_wealth(n_share, bins, alpha):
    """Sum of avg × width over the richest `n_share` percent of adults.

    bins: (lo, hi, avg) g-percentiles ordered from the top down, lo/hi in
    percent ranks, avg in euros per adult. Multiply the result by
    adults / 100 to get euros. Inside the top bin the richest fraction f holds
    f^(1 − 1/alpha) of the bin's wealth (Pareto); thinner bins are split
    uniformly.
    """
    if any(later[0] > earlier[0] for earlier, later in zip(bins, bins[1:])):
        raise ValueError("bins must be ordered from the top down")
    if n_share > sum(hi - lo for lo, hi, _ in bins) + 1e-9:
        raise ValueError(f"top {n_share}% exceeds the bins provided")
    remaining, total = n_share, 0.0
    for lo, hi, avg in bins:
        if remaining <= 0:
            break
        width = hi - lo
        if hi == 100 and remaining < width:
            # Only when fewer adults than the top g-percentile are covered.
            if alpha is None or alpha <= 1:
                raise ValueError("a Pareto alpha above 1 is needed to split the top g-percentile")
            return total + avg * width * (remaining / width) ** (1 - 1 / alpha)
        take = min(width, remaining)
        total += avg * take
        remaining -= take
    return total


def scenario_shares(layer_shares, layer_bounds, top_bins, alpha, mean, adults, rich_list_real, params):
    """(corrected layer shares or None, W_n, RL_adj) for one year.

    layer_shares: WID shares of the layers (sum 1) for layer_bounds
    [(lo, hi), ...] in percent ranks.
    """
    n_pct = adults_covered(params) / adults * 100
    total = mean * adults
    rl_adj = rich_list_real * (1 - params["non_resident_share"])
    w_n = top_n_wealth(n_pct, top_bins, alpha) / 100 * adults
    if rl_adj <= w_n:
        return None, w_n, rl_adj
    scale = (total - rl_adj) / (total - w_n)
    ratio = rl_adj / w_n
    cutoff = 100 - n_pct
    above = sum(sh * total for (lo, _), sh in zip(layer_bounds, layer_shares) if lo >= cutoff)
    out = []
    for (lo, hi), share in zip(layer_bounds, layer_shares):
        wealth = share * total
        if lo >= cutoff:  # entirely inside the listed group
            new = wealth * ratio
        elif hi > cutoff:  # straddles the cutoff: listed part rescaled, rest scaled down
            listed = w_n - above
            new = listed * ratio + (wealth - listed) * scale
        else:
            new = wealth * scale
        out.append(new / total)
    return out, w_n, rl_adj
