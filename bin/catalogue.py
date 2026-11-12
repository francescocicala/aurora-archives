"""Merge all dossier .tsv files into a per-night catalogue (pre-1868) with Helsinki Ak percentiles.

Usage: python bin/catalogue.py OUT.tsv DOSSIER_DIR...
A night counts as CONFIRMED with >=3 sighting reports from >=2 distinct places, WEAK with 1-2 reports.
Reports of the same night found under several candidate windows are merged (deduplicated by article text id).
"""
import glob, re, sys
import pandas as pd

out, *dirs = sys.argv[1:]
ref = __file__.rsplit("/bin/", 1)[0] + "/data/ref"
rows = []
for d in dirs:
    for f in sorted(glob.glob(f"{d}/*.tsv")):
        ev = f.rsplit("/", 1)[1][:-4]
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", ev):
            continue
        txt = open(f.replace(".tsv", ".txt")).read() if glob.glob(f.replace(".tsv", ".txt")) else ""
        heads = dict(re.findall(r"===== (\S+) =====\nPublished \S+ in ([^\n]*)", txt))
        for l in open(f):
            p = l.rstrip("\n").split("\t")
            if len(p) < 5 or p[1].strip().upper() != "YES" or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", p[2].strip()):
                continue
            head = heads.get(p[0], "")
            paper = head[:60]
            loc = re.search(r"paper location: ([^;]*);", head)
            if p[3].strip().lower() == "local" and loc:
                p[3] = loc.group(1).strip().title()
            rows.append({"event": ev, "id": p[0], "night": p[2].strip(), "place": p[3].strip(), "paper": paper,
                         "lat": pd.to_numeric(p[4], errors="coerce"), "note": p[5] if len(p) > 5 else ""})
r = pd.DataFrame(rows)
r["place"] = r.place.str.replace(r", ([A-Za-z]{2})$", lambda m: ", " + m.group(1).upper(), regex=True)
foreign = r.place.str.contains(r"Canada|England|London|Europe|Ireland|Scotland|France|Germany|Sweden|Norway|Lapland|"
                               r"Cuba|Havana|Jamaica|Bermuda|Bahamas|Nassau|Honolulu|Hawaii|Maui|at sea|Mexico|Panama", case=False, na=False)
r["us"] = ~foreign
# the same report text appears under overlapping windows: key on paper + place + note
r = r.drop_duplicates(["night", "paper", "place", "note"])
r = r[r.night < "1868-01-01"]
g = r.groupby("night").agg(reports=("id", "size"), places=("place", lambda s: s[~s.isin(["?"])].nunique()),
                           papers=("paper", "nunique"), events=("event", lambda s: ",".join(sorted(set(s)))))
us = r[r.us & r.lat.notna()].sort_values(["lat", "place"], kind="stable").groupby("night").first()
g["southernmost_us"] = us.place
g["lat"] = us.lat
g["verdict"] = ["CONFIRMED" if n >= 3 and pa >= 2 else "WEAK" for n, pa in zip(g.reports, g.papers)]
h = pd.read_csv(f"{ref}/helsinki_H_Ak_1844_1897.csv", parse_dates=["date"], index_col="date").Ak
h = h[h < 300].dropna()
def ak(n):
    t = pd.Timestamp(n); v = [h.get(t), h.get(t + pd.Timedelta(days=1))]; v = [x for x in v if x is not None and x == x]
    return max(v) if v else None
g["Ak"] = [ak(n) for n in g.index]
g["Ak_pct"] = [round((h < a).mean() * 100, 1) if pd.notna(a) else None for a in g.Ak]
g["southernmost_us"] = g.southernmost_us.str.replace(r"^(\?|Nan), ", "", regex=True)
# merge consecutive nights into storms
g = g.sort_index()
sid, prev = [], None
for n in pd.to_datetime(g.index):
    sid.append(sid[-1] if prev is not None and (n - prev).days <= 1 else (sid[-1] + 1 if sid else 0)); prev = n
g["storm"] = sid
g.to_csv(out, sep="\t")
st = g.groupby("storm").agg(first=("reports", lambda s: s.index[0]), last=("reports", lambda s: s.index[-1]),
                            reports=("reports", "sum"), papers=("papers", "sum"), lat=("lat", "min"), Ak_pct=("Ak_pct", "max"),
                            confirmed=("verdict", lambda s: (s == "CONFIRMED").any()))
st["southernmost_us"] = [g[(g.storm == k)].sort_values("lat").southernmost_us.iloc[0] for k in st.index]
st.to_csv(out.replace(".tsv", "_storms.tsv"), sep="\t", index=False)
cs = st[st.confirmed]
base = pd.Series([(h < max(a, b)).mean() * 100 for a, b in zip(h.values[:-1], h.values[1:])]).median()
print(f"storms: {len(st)}; confirmed storms {len(cs)}; with Helsinki {cs.Ak_pct.notna().sum()}, median pct {cs.Ak_pct.median()}, "
      f">=95th {(cs.Ak_pct >= 95).sum()}; random-night baseline pct {base:.1f}")
c = g[g.verdict == "CONFIRMED"]
print(f"nights with any sighting: {len(g)}; CONFIRMED {len(c)} (with Helsinki: {c.Ak.notna().sum()}, "
      f"median pct {c.Ak_pct.median()}, >=95th: {(c.Ak_pct >= 95).sum()}); WEAK {len(g) - len(c)} "
      f"(median pct {g[g.verdict == 'WEAK'].Ak_pct.median()})")
