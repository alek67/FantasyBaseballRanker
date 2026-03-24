import pandas as pd
from data import getHitters

LEAGUE_FORMAT = "AVG"  # "AVG" or "OBP"
TOP_N_HIT = 150
LEAGUE_SIZE = 12

STATS_AVG = ["R", "HR", "RBI", "SB", "AVG"]
STATS_OBP = ["R", "HR", "RBI", "SB", "OBP"]
SCORING_STATS = STATS_OBP if LEAGUE_FORMAT == "OBP" else STATS_AVG

RATE_STATS = {"AVG", "OBP"}
WEIGHTS = {"R": 1.0, "HR": 1.0, "RBI": 1.0, "SB": 1.0, "AVG": 1.0, "OBP": 1.0}


def rankHitters(df):
    df = df.dropna(subset=SCORING_STATS + ["OPS", "PA", "PlayerName"])
    df = df[df["PA"] > 0].copy()

    top_n = df.nlargest(TOP_N_HIT, "OPS")
    baseline_mean = top_n[SCORING_STATS].mean()
    baseline_std = top_n[SCORING_STATS].std()

    marginal_stds = {
        stat: ((top_n[stat] - baseline_mean[stat]) * top_n["PA"]).std()
        for stat in SCORING_STATS if stat in RATE_STATS
    }

    print(f"\n--- Hitter Baseline (Top {TOP_N_HIT} by OPS) ---")
    for stat in SCORING_STATS:
        if stat in RATE_STATS:
            print(f"  {stat:>4}: avg={baseline_mean[stat]:.3f}  marginal_std={marginal_stds[stat]:.3f}")
        else:
            print(f"  {stat:>4}: avg={baseline_mean[stat]:.3f}  std={baseline_std[stat]:.3f}")

    # counting stats
    for stat in [s for s in SCORING_STATS if s not in RATE_STATS]:
        df[f"z_{stat}"] = (df[stat] - baseline_mean[stat]) / baseline_std[stat]

    # rate stats: PA-weighted marginal so a .300 hitter with 600 PA ranks above .300 with 200 PA
    for stat in [s for s in SCORING_STATS if s in RATE_STATS]:
        marginal = (df[stat] - baseline_mean[stat]) * df["PA"]
        df[f"z_{stat}"] = marginal / marginal_stds[stat]

    df["score_zscore"] = sum(df[f"z_{stat}"] * WEIGHTS.get(stat, 1.0) for stat in SCORING_STATS)

    df["z_PA"] = (df["PA"] - top_n["PA"].mean()) / top_n["PA"].std()

    ranked = df.sort_values("score_zscore", ascending=False).reset_index(drop=True)
    ranked["rank"] = ranked.index + 1
    return ranked


def printRanking(ranked, n=30):
    sorted_df = ranked.sort_values("score_zscore", ascending=False).head(n)

    z_cols = [f"z_{s}" for s in SCORING_STATS]
    display_cols = ["rank", "PlayerName", "Team", "Pos", "PA", "z_PA"] + SCORING_STATS + z_cols + ["score_zscore"]
    display_cols = [c for c in display_cols if c in sorted_df.columns]

    print(f"\n{'='*70}")
    print(f"  Top {n} Hitters — Z-Score  [{LEAGUE_FORMAT} league]")
    print(f"{'='*70}")

    lines = sorted_df[display_cols].to_string(index=False).split("\n")
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

    df = getHitters()
    printRanking(rankHitters(df), n=150)