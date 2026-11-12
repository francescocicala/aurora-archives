#!/bin/sh
# Harvest every year 1800-1963 into data/harvest (resumable; JOBS parallel workers, ~2 GB streamed per year).
cd "$(dirname "$0")/.."
seq 1800 1963 | xargs -P "${JOBS:-2}" -I{} sh -c '[ -f data/harvest/hits/{}.jsonl.gz ] || python3 -I bin/harvest.py {} data/harvest'
