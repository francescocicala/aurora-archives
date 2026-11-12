"""Draw a labeling sample from harvested hits and write agent batch files.

Usage: python -I bin/make_batches.py HARVEST_DIR[,DIR2...] OUT_DIR N_RANDOM N_STORM BATCH_SIZE SEED [IDS_FILE SID_START]
Random part: stratified by decade (equal per decade). Storm part: articles published within 10 days after
a date with aaH_max >= 400 or a known storm start. Writes OUT_DIR/sample.tsv and OUT_DIR/batches/bNNN.txt.
"""
import csv, glob, gzip, json, os, random, re, sys
from collections import defaultdict
from datetime import date, timedelta

hdirs, odir, n_rand, n_storm, bs, seed = sys.argv[1].split(","), sys.argv[2], *map(int, sys.argv[3:7])
ids_file, start = (sys.argv[7], int(sys.argv[8])) if len(sys.argv) > 8 else (None, 0)
want = set(open(ids_file).read().split()) if ids_file else set()
rng = random.Random(seed)
PAT = re.compile(r"\baurora|\bborealis\b|\bnorthern\s+lights?\b|\bpolar\s+lights?\b|\bauroral\b", re.I)
ref = os.path.join(os.path.dirname(__file__), "..", "data", "ref")

storm_days = {r["date"] for r in csv.DictReader(open(f"{ref}/aaH_daily_1868_2017.csv")) if float(r["aaH_max"]) >= 400}
storm_days |= {r["start_date"] for r in csv.DictReader(open(f"{ref}/known_storms.tsv"), delimiter="\t")}
near = {(date.fromisoformat(d) + timedelta(k)).isoformat() for d in storm_days for k in range(11)}

papers = {}
for f in [f for h in hdirs for f in glob.glob(f"{h}/papers/*.jsonl")]:
    for l in open(f):
        p = json.loads(l); papers[p["key"]] = p["title"]

def window(t):
    ms = list(PAT.finditer(t))
    if not ms:
        return t[:2500]
    a, b = max(0, ms[0].start() - 900), ms[-1].end() + 900
    return t[a:min(b, a + 3000)]

by_dec, storm, pick = defaultdict(list), [], {}
for f in sorted(f for h in hdirs for f in glob.glob(f"{h}/hits/*.jsonl.gz")):
    for l in gzip.open(f, "rt"):
        r = json.loads(l)
        rec = (r["id"], r["date"], r["paper"])
        if r["id"] in want:
            pick[r["id"]] = ("active", 1.0)
        by_dec[r["date"][:3]].append(rec)
        if r["date"] in near:
            storm.append(rec)

per = n_rand // len(by_dec)
for dec, rs in by_dec.items():
    for rec in rng.sample(rs, min(per, len(rs))):
        pick[rec[0]] = ("random", len(rs) / min(per, len(rs)))
for rec in rng.sample(storm, min(n_storm, len(storm))):
    pick.setdefault(rec[0], ("storm", len(storm) / min(n_storm, len(storm))))

texts = {}
for f in sorted(f for h in hdirs for f in glob.glob(f"{h}/hits/*.jsonl.gz")):
    for l in gzip.open(f, "rt"):
        r = json.loads(l)
        if r["id"] in pick:
            texts[r["id"]] = r

os.makedirs(f"{odir}/batches", exist_ok=True)
ids = list(texts); rng.shuffle(ids)
with open(f"{odir}/sample{'_' + str(start) if start else ''}.tsv", "w") as s:
    s.write("sid\tid\tdate\tpaper\tstratum\tweight\n")
    for i, k in enumerate(ids):
        r = texts[k]; sid = f"s{i + start:05d}"
        s.write(f"{sid}\t{k}\t{r['date']}\t{r['paper']}\t{pick[k][0]}\t{pick[k][1]:.3f}\n")
        b = (i + start) // bs
        with open(f"{odir}/batches/b{b:03d}.txt", "a") as out:
            body = window((r["headline"] + " " + r["text"]).replace("\n", " "))
            out.write(f"===== {sid} =====\nPublished {r['date']} in {papers.get(r['paper'], r['paper'])}\n{body}\n===== end {sid} =====\n\n")
print(len(ids), "articles,", (len(ids) + bs - 1) // bs, "batches; decades:", {d: len(v) for d, v in sorted(by_dec.items())})
