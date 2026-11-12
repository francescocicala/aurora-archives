"""Fetch place of publication (lat/long, city, state) for each newspaper LCCN from the loc.gov item API.

Usage: python bin/fetch_paper_geo.py HARVEST_DIR CACHE.jsonl   (resumable; ~1 request/s)
"""
import glob, json, os, sys, time, requests

hdir, cache = sys.argv[1:3]
done = {json.loads(l)["paper"] for l in open(cache)} if os.path.exists(cache) else set()
keys = sorted({json.loads(l)["key"] for f in glob.glob(f"{hdir}/papers/*.jsonl") for l in open(f)} - done)
s = requests.Session()
with open(cache, "a") as out:
    for k in keys:
        rec = {"paper": k}
        for attempt in range(4):
            try:
                r = s.get(f"https://www.loc.gov/item/{k}/", params={"fo": "json"}, timeout=30)
                if r.status_code == 429:
                    time.sleep(30 * (attempt + 1)); continue
                i = r.json().get("item", {}) if r.ok else {}
                rec |= {"latlong": i.get("latlong"), "city": (i.get("location_city") or [None])[0],
                        "state": (i.get("location_state") or [None])[0], "status": r.status_code}
                break
            except Exception as e:
                rec["error"] = str(e)[:100]; time.sleep(5)
        out.write(json.dumps(rec) + "\n"); out.flush()
        time.sleep(1)
print(len(keys), "fetched")
