"""README figures. Usage: python bin/figures.py OUTDIR (needs data/ref from bin/fetch_ref.sh)"""
import sys
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

out = sys.argv[1]
root = __file__.rsplit("/bin/", 1)[0]
plt.rcParams.update({"font.family": "Inter", "font.size": 10.5, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#9a9893", "axes.labelcolor": "#4a4945", "xtick.color": "#4a4945",
                     "ytick.color": "#4a4945", "axes.titlelocation": "left", "axes.titlesize": 13, "figure.dpi": 160})
BLUE, GREY, INK = "#2a6fdb", "#b9b7b0", "#2b2a27"

# 1. newspaper index vs aaH, 1868-1950
n = pd.read_csv(f"{root}/results/final/nights.tsv", sep="\t", index_col=0, parse_dates=True)
v = n.loc["1868":"1950"]; v = v[v.papers_active >= 10]
fig, ax = plt.subplots(2, 1, figsize=(10, 5.2), sharex=True, gridspec_kw={"hspace": 0.15})
ax[0].vlines(v.index, 0, v.share * 100, color=BLUE, lw=0.7)
ax[0].set_ylabel("% of papers\nreporting aurora"); ax[0].set_ylim(0, v.share.max() * 100 * 1.15)
ax[1].vlines(v.index, 0, v.aaH_night, color=GREY, lw=0.7)
ax[1].set_ylabel("aaH (nT)")
for d, lab in [("1872-02-04", "Feb 1872"), ("1882-11-17", "Nov 1882"), ("1903-10-31", "Oct 1903"), ("1909-09-25", "Sep 1909"),
               ("1921-05-14", "May 1921"), ("1938-01-25", "Jan 1938"), ("1941-09-18", "Sep 1941")]:
    t = pd.Timestamp(d); w = v.loc[t - pd.Timedelta(days=2): t + pd.Timedelta(days=2)]
    if len(w):
        ax[0].annotate(lab, (w.share.idxmax(), w.share.max() * 100), xytext=(0, 4), textcoords="offset points",
                       ha="center", fontsize=8.5, color=INK)
ax[0].set_title("Newspaper aurora reports (top) line up with the magnetometer storm record (bottom)", pad=14)
fig.text(0.01, 0.005, "One bar per night, 1868-1950. aaH: Lockwood et al. (larger of the two UT days spanning the night).",
         fontsize=8, color="#7a7873")
fig.savefig(f"{out}/index_vs_aaH.png", bbox_inches="tight"); plt.close(fig)

# 2. pre-1868 storms: southernmost US sighting by date
s = pd.read_csv(f"{root}/results/storms_pre1868_with_literature.tsv", sep="\t", parse_dates=["first"]).dropna(subset=["lat"])
yr = s["first"].dt.year + (s["first"].dt.dayofyear - 1) / 365
fig, ax = plt.subplots(figsize=(10, 4.8))
new = s.modern_study.eq("NONE_FOUND")
ax.scatter(yr[~new], s.lat[~new], s=12 + s.reports[~new] * 4, facecolor="white", edgecolor=INK, lw=1, zorder=3, label="studied / mentioned in modern work")
ax.scatter(yr[new], s.lat[new], s=12 + s.reports[new] * 4, color=BLUE, alpha=0.55, lw=0, zorder=2, label="no modern study found")
for d, lab, dx, dy in [("1860-09-06", "6 Sep 1860, New Orleans", 14, -14), ("1860-08-06", "6 Aug 1860, Pike Co. MS", -16, 24),
                       ("1859-09-01", "Sep 1859 (Carrington)", -14, -4), ("1859-08-28", "Aug 1859", -14, 2),
                       ("1866-02-20", "Feb 1866, Meridian MS", 8, 14), ("1851-09-29", "Sep 1851, Charleston", -12, 10),
                       ("1839-09-03", "Sep 1839", 10, -10), ("1848-11-17", "Nov 1848", -12, -8)]:
    r = s[s["first"] == d]
    if len(r):
        x = float(yr[r.index[0]]); y = float(r.lat.iloc[0])
        ax.annotate(lab, (x, y), xytext=(dx, dy), textcoords="offset points", ha="left" if dx > 0 else "right",
                    fontsize=8.5, color=INK, arrowprops={"arrowstyle": "-", "color": "#9a9893", "lw": 0.6})
ax.set_ylim(23, 46); ax.set_xlim(1825, 1869)
ax.set_ylabel("southernmost US sighting (°N)")
ax.set_title("49 confirmed storms before 1868, and how far south each was seen")
ax.legend(frameon=False, loc="upper left", fontsize=9, markerscale=0.6)
ax.grid(axis="y", color="#e6e4df", lw=0.8); ax.set_axisbelow(True)
fig.text(0.01, -0.01, "Dot size = number of independent newspaper reports. 46 of 49 storms have a located sighting.", fontsize=8, color="#7a7873")
fig.savefig(f"{out}/pre1868_storms.png", bbox_inches="tight"); plt.close(fig)

# 3. blind check: Helsinki percentile of confirmed storms vs random nights
h = pd.read_csv(f"{root}/data/ref/helsinki_H_Ak_1844_1897.csv", parse_dates=["date"], index_col="date").Ak
h = h[h < 300].dropna()
rng = np.random.default_rng(0)
night_max = np.maximum(h.values[:-1], h.values[1:])
hs = np.sort(h.values)
allp = np.searchsorted(hs, night_max, side="left") / len(hs) * 100
rand = rng.choice(allp, 2000)
c = pd.read_csv(f"{root}/results/dossiers/catalogue_nights_pre1868_storms.tsv", sep="\t")
c = c[c.confirmed & c.Ak_pct.notna()].Ak_pct.values
fig, ax = plt.subplots(figsize=(10, 3.4))
for k, (vals, col) in enumerate([(rand, GREY), (c, BLUE)]):
    ys = k + rng.uniform(-0.18, 0.18, len(vals))
    ax.scatter(vals, ys, s=10 if k == 0 else 26, color=col, alpha=0.35 if k == 0 else 0.85, lw=0)
    med = np.median(allp if k == 0 else vals)
    ax.plot([med, med], [k - 0.3, k + 0.3], color=INK, lw=2)
    ax.text(med, k + 0.36, f"median {med:.0f}", ha="center", fontsize=9, color=INK)
ax.set_yticks([0, 1], ["random nights", f"confirmed storms\n(n={len(c)})"])
ax.set_xlim(0, 101); ax.set_ylim(-0.6, 1.75)
ax.set_xlabel("percentile of Helsinki magnetic disturbance (Ak), 1844-1897")
ax.set_title("Storms dated from newspapers alone land on Helsinki's most disturbed days")
fig.text(0.01, -0.1, "The agents never saw magnetometer data. Percentile = the larger of the two UT days spanning the night, against all Helsinki days.",
         fontsize=8, color="#7a7873")
fig.savefig(f"{out}/blind_check_helsinki.png", bbox_inches="tight"); plt.close(fig)
print("ok", len(c), np.median(c), np.median(rand))
