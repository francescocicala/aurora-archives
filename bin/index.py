"""Build the daily newspaper aurora index and validate it against aaH.

Usage: python bin/index.py SCORES.tsv.gz HARVEST_DIR... OUTDIR
Per publication day d: expected sighting reports R = sum p, papers reporting P = #papers with p >= t,
active papers A, articles V. Event signal for night n = reports published in (n, n+7] (weeklies lag),
expressed as the share of active papers reporting. Writes daily.tsv, nights.tsv, validation.txt.
"""
import glob, sys
import numpy as np, pandas as pd
from scipy.stats import spearmanr

sc, *hdirs, out = sys.argv[1:]
t = 0.3
s = pd.read_csv(sc, sep="\t", dtype={"date": str})
s = s[s.date.str.match(r"^\d{4}-\d{2}-\d{2}$")]
vol = pd.concat([pd.read_csv(f, sep="\t", header=None, names=["date", "paper", "n"], dtype={"date": str})
                 for h in hdirs for f in glob.glob(f"{h}/volume/*.tsv*")])
vol = vol[vol.date.str.match(r"^\d{4}-\d{2}-\d{2}$")]
vol["date"] = pd.to_datetime(vol.date, errors="coerce"); vol = vol.dropna()
s["date"] = pd.to_datetime(s.date, errors="coerce"); s = s.dropna(subset=["date"])

days = pd.DataFrame({"V": vol.groupby("date").n.sum(), "A": vol.groupby("date").paper.nunique()})
import os
variant = os.environ.get("VARIANT", "all")
pos = s[s.p >= t]
if variant in ("cue", "cue_first"):
    pos = pos[pos.cue == 1]
if variant in ("first", "cue_first"):
    # a paper's later coverage within 10 days of its first report is treated as echo
    pos = pos.sort_values(["paper", "date"])
    keep, last = [], {}
    for pa, d in zip(pos.paper, pos.date):
        keep.append(pa not in last or (d - last[pa]).days > 10)
        if keep[-1]:
            last[pa] = d
    pos = pos[keep]
days["R"] = s.groupby("date").p.sum()
days["P"] = pos.groupby("date").paper.nunique()
days = days.fillna(0).asfreq("D", fill_value=0)
days.to_csv(f"{out}/daily.tsv", sep="\t")

# night n gets reports printed on n+1..n+7, normalised by distinct papers active in that window
# each issue covers the nights since the paper's previous issue (capped at 7); weight 1/gap so a weekly
# counts as much as a daily in total but is spread over its week
iss = vol[["paper", "date"]].drop_duplicates().sort_values(["paper", "date"])
iss["gap"] = iss.groupby("paper").date.diff().dt.days.fillna(1).clip(1, 7).astype(int)
iss = iss.merge(pos[["paper", "date"]].drop_duplicates().assign(hit=1), how="left").fillna({"hit": 0})
ex = iss.loc[iss.index.repeat(iss.gap)].copy()
ex["night"] = ex.date - pd.to_timedelta(ex.groupby(level=0).cumcount() + 1, unit="D")
ex["w"] = 1 / ex.gap
g = ex.groupby("night")
rep = (ex.w * ex.hit).groupby(ex.night).sum().reindex(days.index, fill_value=0)
act = g.w.sum().reindex(days.index, fill_value=0)
nights = pd.DataFrame({"papers_reporting": rep.round(2), "papers_active": act.round(2)})
nights["share"] = (nights.papers_reporting / nights.papers_active.replace(0, np.nan)).fillna(0)
aa = pd.read_csv(f"{__file__.rsplit('/bin/', 1)[0]}/data/ref/aaH_daily_1868_2017.csv", parse_dates=["date"], index_col="date")
nights = nights.join(aa)

# US evening of night n is UT n..n+1, so compare with the larger reference value of the two UT days
ref = f"{__file__.rsplit('/bin/', 1)[0]}/data/ref"
hel = pd.read_csv(f"{ref}/helsinki_H_Ak_1844_1897.csv", parse_dates=["date"], index_col="date").Ak
hel = hel[hel < 300]  # 400 = saturated/flagged days
nights = nights.join(hel)
nights["aaH_night"] = nights.aaH_max.combine(nights.aaH_max.shift(-1), max)
nights["Ak_night"] = nights.Ak.combine(nights.Ak.shift(-1), max)

def validate(col, start, end, thr, min_active=10):
    v = nights.loc[start:end].dropna(subset=[col])
    v = v[v.papers_active >= min_active]
    peak = v[v.share == v.share.rolling(7, center=True, min_periods=1).max()].sort_values("share", ascending=False)
    storm = v[col] >= thr
    out = [f"== {col} {start}-{end}: {len(v)} nights with >={min_active} active papers; Spearman(share,{col}) = {spearmanr(v.share, v[col])[0]:.3f}; "
           f"storm threshold {thr} (top {storm.mean():.2%} of nights)"]
    for k in (10, 25, 50, 100):
        top = peak.head(k)
        out.append(f"top-{k} peaks: {(top[col] >= thr).mean():.0%} storm nights; median {col} {top[col].median():.0f} (all nights {v[col].median():.0f})")
    runs = []
    for d in v.index[storm]:
        if runs and (d - runs[-1][1]).days <= 3:
            runs[-1][1] = d
        else:
            runs.append([d, d])
    for k in (25, 50, 100, 200):
        pk = peak.head(k).index
        hit = sum(((pk >= a - pd.Timedelta(days=1)) & (pk <= b + pd.Timedelta(days=1))).any() for a, b in runs)
        out.append(f"recall: {hit}/{len(runs)} storm events have a top-{k} peak within their nights +-1")
    return out, peak

lines, peak = validate("aaH_night", "1868", "1963", 400)
peak.head(300).to_csv(f"{out}/peaks_1868_1963.tsv", sep="\t")
for args in (("Ak_night", "1844", "1867", 100, 5), ("Ak_night", "1868", "1897", 100)):
    l, p = validate(*args); lines += l
nights.to_csv(f"{out}/nights.tsv", sep="\t")
open(f"{out}/validation.txt", "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
