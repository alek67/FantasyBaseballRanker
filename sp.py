import pandas as pd
from data import getPitchers

TOP_SP = 65
SP_IP_MIN = 100
LEAGUE_SIZE = 12

SP_STATS = ["W", "SO", "ERA", "WHIP"]
LOWER_IS_BETTER = {"ERA", "WHIP"}
SP_WEIGHTS = {"W": 1.0, "SO": 1.0, "ERA": 1.0, "WHIP": 1.0}


def rankSP(df):
    df = df.dropna(subset=SP_STATS + ["IP", "PlayerName"])
    df = df[df["IP"] >= SP_IP_MIN].copy()
    top_n = df.nlargest(TOP_SP, "IP")

    baseline_mean = top_n[SP_STATS].mean()
    baseline_std = top_n[SP_STATS].std()

    # ERA and WHIP are rate stats, so weight by IP like AVG is weighted by PA
    marginal_stds = {
        stat: ((top_n[stat] - baseline_mean[stat]) * top_n["IP"]).std()
        for stat in SP_STATS if stat in LOWER_IS_BETTER
    }

    print(f"\n--- SP Baseline (Top {TOP_SP} by IP) ---")
    for stat in SP_STATS:
        if stat in LOWER_IS_BETTER:
            print(f"  {stat:>5}: avg={baseline_mean[stat]:.3f}  marginal_std={marginal_stds[stat]:.3f}")
        else:
            print(f"  {stat:>5}: avg={baseline_mean[stat]:.3f}  std={baseline_std[stat]:.3f}")

    # counting stats
    for stat in [s for s in SP_STATS if s not in LOWER_IS_BETTER]:
        df[f"z_{stat}"] = (df[stat] - baseline_mean[stat]) / baseline_std[stat]

    # rate stats: IP-weighted marginal, negated so lower ERA/WHIP = positive z
    for stat in LOWER_IS_BETTER:
        marginal = (df[stat] - baseline_mean[stat]) * df["IP"]
        df[f"z_{stat}"] = -marginal / marginal_stds[stat]

    df["score_zscore"] = sum(df[f"z_{stat}"] * SP_WEIGHTS.get(stat, 1.0) for stat in SP_STATS)

    ranked = df.sort_values("score_zscore", ascending=False).reset_index(drop=True)
    ranked["rank"] = ranked.index + 1
    return ranked


def printSPRanking(ranked, n=65):
    sorted_df = ranked.sort_values("score_zscore", ascending=False).head(n)

    z_cols = [f"z_{s}" for s in SP_STATS]
    display_cols = ["rank", "PlayerName", "Team", "IP"] + SP_STATS + z_cols + ["score_zscore"]
    display_cols = [c for c in display_cols if c in sorted_df.columns]

    print(f"\n{'='*70}")
    print(f"  Top {n} Starting Pitchers — Z-Score")
    print(f"{'='*70}")

    lines = sorted_df[display_cols].rename(columns={"SO": "K", "z_SO": "z_K"}).to_string(index=False).split("\n")
    header, data_lines = lines[0], lines[1:]

    print(header)
    for i, line in enumerate(data_lines):
        rank = i + 1
        if rank > 1 and (rank - 1) % LEAGUE_SIZE == 0:
            rnd = (rank - 1) // LEAGUE_SIZE + 1
            print(f"\n  --- Round {rnd} ---")
        print(line)


if __name__ == "__main__":
    pd.set_option("display.float_format", "{:.3f}".format)
    pd.set_option("display.max_columns", 20)
    pd.set_option("display.width", 200)

    df = getPitchers()
    printSPRanking(rankSP(df), n=65)