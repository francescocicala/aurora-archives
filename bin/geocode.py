"""Geocode newspapers from their LoC title '(City, State)' with the 2020 Census place gazetteer.

Usage: python bin/geocode.py HARVEST_DIR OUT.tsv   (falls back to the state's median place coordinates)
"""
import glob, json, re, sys, unicodedata
import pandas as pd, us

hdirs, out = sys.argv[1].split(","), sys.argv[2]
g = pd.read_csv(f"{__file__.rsplit('/bin/', 1)[0]}/data/ref/2020_Gaz_place_national.txt", sep="\t", dtype=str)
g.columns = g.columns.str.strip()
g["lat"], g["lon"] = g.INTPTLAT.astype(float), g.INTPTLONG.astype(float)
norm = lambda s: re.sub(r"[^a-z ]", "", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()).strip()
g["NAME"] = g.NAME.str.replace(r"\s*\(balance\)", "", regex=True).str.split("-").str[0].str.split("/").str[0]
g["key"] = g.NAME.str.replace(r" (city|town|village|CDP|borough|municipality|city and borough|urban county|consolidated government.*|metropolitan government.*|unified government.*)$", "", regex=True).map(norm)
cent = g.groupby("USPS")[["lat", "lon"]].median()
idx = g.drop_duplicates(["USPS", "key"]).set_index(["USPS", "key"])[["lat", "lon"]]

papers = {}
for f in [f for h in hdirs for f in glob.glob(f"{h}/papers/*.jsonl")]:
    for l in open(f):
        p = json.loads(l); papers.setdefault(p["key"], p)

import os
loc = {}
lc = f"{__file__.rsplit('/bin/', 1)[0]}/data/ref/loc_paper_geo.jsonl"
if os.path.exists(lc):
    for l in open(lc):
        r = json.loads(l)
        if r.get("latlong"):
            loc[r["paper"]] = r
rows = []
for k, p in papers.items():
    st = us.states.lookup(p.get("state") or "")
    t = re.sub(r"\[i\.\s?e\.?,?\s*([^\]]*)\]", r"\1", p["title"]).replace("[", "").replace("]", "").replace("-", " ")
    m = re.findall(r"\(([^()]*)\)", t)
    city = norm(m[0].split(",")[0]) if m else ""
    city = re.sub(r"^(saint|st) ", "st ", city)
    lat = lon = None; how = "none"
    if k in loc:
        lat, lon = loc[k]["latlong"]; rows.append((k, p["title"], st.abbr if st else "", loc[k].get("city") or city, lat, lon, "loc")); continue
    if st:
        w = city.split()
        cands = [" ".join(w[:n]) for n in range(len(w), 0, -1)]
        for c in [x for c0 in cands for x in (c0, c0.replace("st ", "saint "))]:
            if (st.abbr, c) in idx.index:
                lat, lon = idx.loc[(st.abbr, c)]; how = "city"; break
        if how == "none" and st.abbr in cent.index:
            lat, lon = cent.loc[st.abbr]; how = "state"
    rows.append((k, p["title"], st.abbr if st else "", city, lat, lon, how))
d = pd.DataFrame(rows, columns=["paper", "title", "state", "city", "lat", "lon", "how"])
d.to_csv(out, sep="\t", index=False)
print(d.how.value_counts().to_dict())
