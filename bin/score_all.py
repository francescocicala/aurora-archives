"""Score every harvested candidate with the trained classifier.

Usage: python -I bin/score_all.py MODEL.pkl HARVEST_DIR OUT.tsv.gz
"""
import glob, gzip, json, pickle, re, sys
import pandas as pd

mp, hdir, out = sys.argv[1:4]
PAT = re.compile(r"\baurora|\bborealis\b|\bnorthern\s+lights?\b|\bpolar\s+lights?\b|\bauroral\b", re.I)

def window(t):
    ms = list(PAT.finditer(t))
    if not ms:
        return t[:2500]
    a, b = max(0, ms[0].start() - 900), ms[-1].end() + 900
    return t[a:min(b, a + 3000)]

D = r"(sun|mon|tues|wednes|thurs|fri|satur)day"
CUE = re.compile(rf"last\s+(night|evening)|yester(day|night)|this\s+morning|night\s+before\s+last|{D}\s+(night|evening|last)|(evening|night)\s+of\s+{D}|on\s+{D}|(evening|night)\s+last|to-?night|this\s+evening", re.I)
m = pickle.load(open(mp, "rb"))["model"]
parts = []
for f in sorted(glob.glob(f"{hdir}/hits/*.jsonl.gz")):
    rs = [json.loads(l) for l in gzip.open(f, "rt")]
    if not rs:
        continue
    d = pd.DataFrame({"id": [r["id"] for r in rs], "date": [r["date"] for r in rs], "paper": [r["paper"] for r in rs]})
    w = [window((r["headline"] + " " + r["text"]).replace("\n", " ")) for r in rs]
    d["p"] = m.predict_proba(w)[:, 1].round(4)
    d["cue"] = [int(bool(CUE.search(x))) for x in w]
    parts.append(d)
    print(f, len(d), round(d.p.sum(), 1), flush=True)
pd.concat(parts).to_csv(out, sep="\t", index=False, compression="gzip")
