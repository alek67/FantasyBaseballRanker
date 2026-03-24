# TLDR
Draft based on your team's current category needs rather than blindly taking the highest z-score every time. I.e If you already have stolen bases covered, a player's SB contribution is less valuable to you than it appears on paper. Focus on the categories you're still in need of.

# 2026 Fantasy Baseball Ranker

This ranker pulls ATC projections from FanGraphs and ranks hitters, starting pitchers, and relievers for fantasy baseball drafts. The core idea came from this YouTube video: https://www.youtube.com/watch?v=vumd2oWYpLg&t=201s, though the methodology here differs in a few important ways explained below.

---

## How it works

The ranker fetches projection data directly from the FanGraphs API at runtime, so it always uses the latest ATC projections. From there it builds a baseline from the realistic pool of players that will actually get drafted, computes z-scores for each scoring category, and sums them to produce a single ranking number.

---

## Hitters

The hitter baseline is built from the top 150 players by OPS. This represents the realistic pool of players that get drafted in most leagues. The mean and standard deviation are both calculated from this pool, not the full player universe, so the baseline reflects what you are actually competing against on draft day.

The scoring categories are R, HR, RBI, SB, and AVG (or OBP if your league uses that format). For counting stats the z-score is straightforward:

z = (player stat - baseline average) / baseline standard deviation

A commenter named ereaven on the video above pointed out that the ratio method shown in the video undervalues rate stats like AVG because they have much less variance than counting stats, making it impossible to be 3x the average in batting average the way you could in stolen bases. Their suggested fix was a z-score approach, which is what this ranker uses.

AVG and OBP are treated differently from the counting stats because they are rate stats. The raw value does not reflect playing time at all a player hitting .320 in 200 plate appearances has the same AVG as a player hitting .320 in 600 plate appearances, but the second player is far more valuable because their at-bats have a much larger effect on your team's cumulative average. To account for this, AVG and OBP are converted to a marginal contribution before z-scoring:

marginal = (player rate - baseline rate) x player PA

This marginal is then z-scored against the top 150 players' marginals. The result is that playing time is baked into the rate stat ranking, which makes it comparable in scale to the counting stats.

The final score for each hitter is the sum of their z-scores across all five categories. Positive means above average, negative means they actively hurt your team in that category relative to the baseline.

---

## Starting Pitchers

Starters are classified as any pitcher projected for 100 or more innings. The baseline is the top 65 starters by IP, which represents roughly 6-7 starters per team in a 10-team league.

The scoring categories for starters are W, SO, ERA, and WHIP. Saves are excluded because starters almost never contribute saves and including it would drag every starter's score down unfairly.

ERA and WHIP are lower-is-better stats, so their z-scores are negated. A pitcher with a 3.00 ERA in a baseline where the average is 3.80 is above average, so negating the z-score makes that a positive contribution to their overall score.

---

## Relief Pitchers

Relievers are any pitcher projected for under 100 innings. The baseline is the top 20 relievers by saves, which represents the realistic pool of closers that get drafted.

The scoring categories for relievers are SV, SO, ERA, and WHIP. Wins are excluded for the same reason saves are excluded from starters they rarely accumulate in a meaningful way for relievers.

ERA and WHIP are handled the same way as with starters.

---

## Draft rounds

All three rankings group players by draft round based on league size. The default is a 12-team league, so every 12 players is a new round. This can be changed by setting LEAGUE_SIZE at the top of hitters.py, sp.py, or rp.py.

---

## Exporting

Running export_csv.py will produce three files: hitters_ranked.csv, sp_ranked.csv, and rp_ranked.csv. These include rank, round, the raw projected stats, the z-score for each category, and the total score.
