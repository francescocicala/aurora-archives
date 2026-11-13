# Data dictionary

Code is MIT-licensed (`LICENSE`). All data files produced by this project are CC BY 4.0. They derive from *American Stories* (Dell et al. 2023, CC BY 4.0), which is built from the Library of Congress's *Chronicling America*. Third-party reference data (Helsinki K/Ak, aaH, Census gazetteer) is not redistributed: `bin/fetch_ref.sh` downloads it.

## Catalogue (main result)

`results/storms_pre1868_with_literature.tsv` lists the 49 confirmed storms with their literature status:
- `modern_study`: STUDIED, MENTIONED or NONE_FOUND.
- `modern_refs`: the modern references found.
- `nineteenth_century_refs`: contemporary accounts in the *American Journal of Science* (AJS) and the *Proceedings of the American Philosophical Society* (APS).
- `silverman_new_england`: whether the storm appears in Silverman's New England aurora catalogue.
- `magnetometer_storm_lists`: the matching entry in the storm tables of Eapen et al. (2026, preprint), with Greenwich class and estimated Dst. Rows marked "to confirm" differ by a day or more.

`results/undocumented_storms_pre1868.tsv` is the subset marked NONE_FOUND (no dedicated modern study), sorted by southern extent. The searches behind these columns are described in `notes/prior_work_49_storms.md` and `notes/loomis_check.md`. NONE_FOUND means our searches found nothing, not that no study exists.

`results/dossiers/catalogue_nights_pre1868_storms.tsv` has one row per storm, where consecutive nights are merged.

| column | meaning |
| --- | --- |
| first, last | first and last night (evening date, local) with sighting reports |
| reports | sighting reports after removing reprints (same paper, place and note) |
| papers | distinct newspapers reporting, summed over the storm's nights |
| lat, southernmost_us | southernmost contiguous-US sighting (geographic latitude, approximate) |
| Ak_pct | percentile of the Helsinki Ak index (larger of the two UT days spanning the night) among all Helsinki days 1844–1897; empty before 1844 or where data are missing |
| confirmed | True when at least one night has 3 or more reports from 2 or more papers |

`results/dossiers/catalogue_nights_pre1868.tsv` holds the same information per night, adding `verdict` (CONFIRMED or WEAK), `events` (the dossier files that contributed) and `storm` (the storm id).

`results/dossiers/roundN/<candidate>.{txt,tsv,md}`, one set per candidate window:
- `.txt` holds the source articles: OCR text, publication date, paper and location.
- `.tsv` holds the agent's per-article reading: ID, sighting, obs_date, place, lat, note.
- `.md` holds the agent's dossier summary and verdict.

`results/dossiers/prior_work.md` and `notes/*.md` record the literature checks.

## Index

`results/final/nights.tsv` has one row per night, 1800–1963:

| column | meaning |
| --- | --- |
| papers_reporting | weighted count of papers whose issue covering this night carries a sighting (score ≥ 0.3); a paper with a gap of g days between issues counts 1/g |
| papers_active | the same weighting over all papers with an issue covering the night |
| share | papers_reporting / papers_active, the index |
| aaH_mean, aaH_max, aaH_night | aaH (nT) for the UT day, and the larger of the two UT days spanning the night |
| Ak, Ak_night | Helsinki Ak, and the larger of the two UT days spanning the night |

The aaH and Ak columns are third-party values (Lockwood et al.; Finnish Meteorological Institute), included for convenience; cite their sources if you use them.

`results/final/daily.tsv` holds per-publication-day totals. `results/final/peaks_1868_1963.tsv` lists the top 300 local maxima. `results/final/validation*.txt` holds the validation statistics.

## Harvest

- `data/harvest/volume/YYYY.tsv.gz`: date, paper (LCCN), number of articles, for every paper and day in American Stories. This is the denominator of the index.
- `data/harvest/papers/all.jsonl`: newspaper metadata (title, place, state) from American Stories.
- `data/harvest/hits/YYYY.jsonl.gz` (separate archive, 292 MB): the 326,123 candidate articles, with id, date, paper, page, headline and text.

## Article-level data

- `results/final/scores.tsv.gz`: id, date, paper (LCCN), p (classifier probability of a sighting report) and cue (contains a recency phrase such as "last night"), for all 326,123 candidate articles.
- `data/labels/`: agent labels used to train the classifier.
  - `sample*.tsv`: the sampled article ids and their sampling stratum.
  - `batches/*.txt`: the text the agents read.
  - `labels/*.tsv`: sid, sighting, obs_date, place, foreign.
- `data/review/`: independent blind re-labelling of a stratified subsample, and the agreement statistics.
- `data/ref/papers_geo.tsv`: newspaper location (Library of Congress coordinates where available, otherwise the Census gazetteer city or state).

## Model

`results/final/model.pkl` is a scikit-learn 1.9.1 pipeline: TF-IDF word 1–2-grams plus char 3–5-grams, then logistic regression. It expects the keyword window that `bin/score_all.py` extracts. Only load pickles from a source you trust.
