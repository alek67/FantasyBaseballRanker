import pandas as pd
from data import getHitters, getPitchers
from hitters import rankHitters, printRanking
from sp import rankSP, printSPRanking
from rp import rankRP, printRPRanking

if __name__ == "__main__":
    pd.set_option("display.float_format", "{:.3f}".format)
    pd.set_option("display.max_columns", 20)
    pd.set_option("display.width", 200)

    hit_df = getHitters()
    printRanking(rankHitters(hit_df), n=150)

    pit_df = getPitchers()
    printSPRanking(rankSP(pit_df), n=65)
    printRPRanking(rankRP(pit_df), n=20)