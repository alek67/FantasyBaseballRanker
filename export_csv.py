import pandas as pd
from data import getHitters, getPitchers
from hitters import rankHitters, SCORING_STATS, LEAGUE_SIZE
from sp import rankSP, SP_STATS
from rp import rankRP, RP_STATS

pd.set_option("display.float_format", "{:.3f}".format)

hit_df = getHitters()
ranked_hitters = rankHitters(hit_df)

pit_df = getPitchers()
ranked_sp = rankSP(pit_df)
ranked_rp = rankRP(pit_df)

# Hitters CSV
hit_z_cols = [f"z_{s}" for s in SCORING_STATS]
hit_cols = ["rank", "PlayerName", "Team", "Pos", "PA"] + SCORING_STATS + hit_z_cols + ["score_zscore"]
hit_cols = [c for c in hit_cols if c in ranked_hitters.columns]
ranked_hitters["round"] = ((ranked_hitters["rank"] - 1) // LEAGUE_SIZE + 1).astype(int)
hit_cols.insert(1, "round")
ranked_hitters[hit_cols].to_csv("hitters_ranked.csv", index=False)
print("Saved hitters_ranked.csv")

#SP CSV
sp_z_cols = [f"z_{s}" for s in SP_STATS]
sp_cols = ["rank", "PlayerName", "Team", "IP"] + SP_STATS + sp_z_cols + ["score_zscore"]
sp_cols = [c for c in sp_cols if c in ranked_sp.columns]
ranked_sp["round"] = ((ranked_sp["rank"] - 1) // LEAGUE_SIZE + 1).astype(int)
sp_cols.insert(1, "round")
ranked_sp[sp_cols].to_csv("sp_ranked.csv", index=False)
print("Saved sp_ranked.csv")

#RP CSV
rp_z_cols = [f"z_{s}" for s in RP_STATS]
rp_cols = ["rank", "PlayerName", "Team", "IP"] + RP_STATS + rp_z_cols + ["score_zscore"]
rp_cols = [c for c in rp_cols if c in ranked_rp.columns]
ranked_rp["round"] = ((ranked_rp["rank"] - 1) // LEAGUE_SIZE + 1).astype(int)
rp_cols.insert(1, "round")
ranked_rp[rp_cols].to_csv("rp_ranked.csv", index=False)
print("Saved rp_ranked.csv")
