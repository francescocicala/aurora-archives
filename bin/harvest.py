"""Stream one American Stories year archive and keep aurora-candidate articles.

Usage: python -I bin/harvest.py YEAR OUTDIR
Writes OUTDIR/hits/YEAR.jsonl.gz (candidate articles), OUTDIR/volume/YEAR.tsv (articles per date x paper),
OUTDIR/papers/YEAR.jsonl (lccn metadata, once per paper).
"""
import gzip, json, os, re, sys, tarfile, requests

REV = os.environ.get("AS_REV", "77e27fa69c4788dfaad1c9efd8a226d5a32d3e9a")
URL = "https://huggingface.co/datasets/dell-research-harvard/AmericanStories/resolve/{}/faro_{}.tar.gz"
PAT = re.compile(r"\baurora|\bborealis\b|\bnorthern\s+lights?\b|\bpolar\s+lights?\b|\bauroral\b|\baurore\b", re.I)

year, out = sys.argv[1], sys.argv[2]
for d in ("hits", "volume", "papers"):
    os.makedirs(f"{out}/{d}", exist_ok=True)

volume, papers, n_scans, n_bad = {}, {}, 0, 0
with requests.get(URL.format(REV, year), stream=True, timeout=120) as r:
    r.raise_for_status()
    r.raw.decode_content = True
    with tarfile.open(fileobj=r.raw, mode="r|gz") as tf, gzip.open(f"{out}/hits/{year}.jsonl.gz.part", "wt") as hits:
        for m in tf:
            if not (m.isfile() and m.name.endswith(".json")):
                continue
            n_scans += 1
            fn = m.name.rsplit("/", 1)[-1]
            try:
                raw = tf.extractfile(m).read()
                data = json.loads(raw)
                lccn = data["lccn"]
            except Exception:
                n_bad += 1
                continue
            key = lccn.get("lccn") or lccn.get("title")
            papers.setdefault(key, lccn)
            date = fn.split("_")[0]
            arts = data.get("full articles", [])
            volume[(date, key)] = volume.get((date, key), 0) + len(arts)
            low = raw.lower()
            if not any(w in low for w in (b"auror", b"boreal", b"northern", b"polar")):
                continue
            for a in arts:
                text = a.get("article") or ""
                head = a.get("headline") or ""
                if PAT.search(text) or PAT.search(head):
                    hits.write(json.dumps({"id": f"{a.get('full_article_id')}_{fn[:-5]}", "date": date, "paper": key,
                                           "page": fn.split("_")[1], "headline": head, "text": text}) + "\n")

os.replace(f"{out}/hits/{year}.jsonl.gz.part", f"{out}/hits/{year}.jsonl.gz")
with open(f"{out}/volume/{year}.tsv", "w") as f:
    f.writelines(f"{d}\t{p}\t{n}\n" for (d, p), n in sorted(volume.items()))
with open(f"{out}/papers/{year}.jsonl", "w") as f:
    f.writelines(json.dumps({"key": k, **v}) + "\n" for k, v in papers.items())
print(json.dumps({"year": year, "scans": n_scans, "bad": n_bad, "papers": len(papers), "articles": sum(volume.values())}))
