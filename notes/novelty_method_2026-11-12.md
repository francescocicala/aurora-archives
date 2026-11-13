# Novelty check: the Aurora Archives method

Checked 2026-11-12. The method under test is Aurora Archives, Zenodo 10.5281/zenodo.24174471 (F. Cicala, released 2026-11-12). It has six steps:

1. Harvest aurora-related articles by keyword across all of American Stories / Chronicling America, 1800–1963, giving about 326k articles.
2. Have LLM agents label a stratified sample.
3. Score every article with a TF-IDF + logistic-regression classifier.
4. Build a nightly index: the share of active newspapers that report a sighting, with weeklies weighted by the gap between issues. Validate it against aaH (1868–1950) and Helsinki Ak (1844–1867).
5. Have LLM agents build an evidence dossier for each night, to confirm storms before 1868. This gives a catalogue of 49 storms, each with its southernmost US sighting.
6. Re-label blind with LLMs and measure agreement.

## (a) Verdict: PARTLY ANTICIPATED

The combination as a whole is new. I found no published work, preprint, dataset or repository that does any of the following:
- runs a full-corpus, multi-decade machine-reading pipeline for aurora reports in any newspaper corpus;
- turns newspaper reports into a **nightly index normalised by the number of active newspapers**;
- validates such an index against aa/aaH or Ak;
- uses LLM agents to build per-night evidence dossiers for a storm catalogue.

Several pieces are clearly anticipated, however:

- **The direct precursor is shmanubhav/aurora-catalog** (A. Sharma; Zenodo 10.5281/zenodo.23275918, v1.0.0-prereg, 2026-10-10). It already applies text classification to **American Stories** to find **aurora sighting reports**:
  - LLM agents label the articles (Claude Sonnet and Gemma), a blind Claude Opus adjudicates, and LLM checkers review flagged items.
  - Inter-labeller agreement is reported (raw 98.0%, kappa 0.94).
  - Keyword search (rg strict, loose and fuzzy patterns) is compared with the classifier.
  - Scope is limited to two windows: Aug–Sep 1859 (development, 1,544 labelled items) and Feb–Mar 1872 (a pre-registered test, not yet reported in the snapshot).
  - The classifier is a fine-tuned transformer (Laya). At the frozen cutoff it **failed** its own bar (precision 29.1%, recall 76.3%).
  - It builds no index, makes no comparison with magnetometer data and has no multi-year catalogue.
  - Zenodo shows only one version, and I found no paper from it on arXiv, ESS Open Archive or the web.
  - Overlap: steps 1 to 3 and step 6 exist in this repo as an idea and a two-window pilot. Aurora Archives differs in scale (the whole 1800–1963 corpus), in using TF-IDF/LR rather than a fine-tuned transformer, and in steps 4 and 5.
  - Aurora Archives should cite it as prior work.
  - **Limitation:** GitHub access to the live repo was denied in this session (API 403, robots-blocked commits page). I could see only the Zenodo snapshot and the GitHub landing page, which shows 3 commits. Commits made after 2026-10-10 could not be checked.
- **Newspapers as aurora sources** go back a long way and are routine. Examples include Silverman's catalogues and storm studies, Hayakawa et al. and Love et al. on the storms of 1872, 1909 and 1921, Carrasco & Vaquero with Trove, and Sánchez Romero et al. 2025 with one Spanish newspaper. All of these are manual or keyword-plus-manual reading of a limited set of sources, and they produce event descriptions rather than a time-series index.
- **Keyword search of digital text corpora for aurora candidates, with relevance grading**, already exists: Kawamura, Hayakawa et al. 2016 on the Qing chronicle. Neuhäuser et al. 2017 criticised it as "uncritical digital search". This is a methodological precedent, and a warning on false positives, for step 1.
- **Text classification of free-text public reports to define the equatorward extent of aurora visibility, compared with Kp**, exists for modern social media: Aurorasaurus (MacDonald et al. 2015; Case et al. 2016, using tweets). This is the conceptual analogue of steps 3–4 for the present day.
- **LLM or NLP extraction of hazard events from newspapers and archival reports** is now established in neighbouring fields: earthquake felt reports (Agrawal et al. 2026, SRL), droughts in Spanish newspapers (Vilas et al., EGU26), floods (Google Groundsource 2026), Turkish geohazards with TF-IDF and NMF (Avcıoğlu et al. 2025), and weather impacts (WXImpactBench, WeatherArchive-Bench). None of these concern space weather.
- **Indices or reconstructions built from aurora catalogues**, such as Lockwood et al. 2025 (MNRAS) on 375 years of auroral activity, the Wagner/Neuhäuser oval reconstructions and Vázquez et al. 2014, use existing compiled catalogues. They do not mine newspapers.

The defensible novelty claims are:
1. The first full-corpus (1800–1963), machine-read aurora record from US newspapers.
2. The first nightly newspaper-share aurora index, with weekly-gap weighting, validated against aaH and Ak.
3. The first use of LLM-agent evidence dossiers to confirm storms in a historical geomagnetic-storm catalogue.

Claims like "first to apply ML/LLMs to newspaper aurora reports" or "first to use American Stories for aurora" would be **false** because of the Sharma repo.

## (b) Closest prior works

| Citation | What they did | How it differs from Aurora Archives |
|---|---|---|
| Sharma, A. (2026). *Machine reading of aurora sighting reports in historical US newspapers*, software v1.0.0-prereg. Zenodo [10.5281/zenodo.23275918](https://doi.org/10.5281/zenodo.23275918); https://github.com/shmanubhav/aurora-catalog | American Stories, keyword pools, LLM labellers (Sonnet, Gemma) with an Opus adjudicator, a fine-tuned Laya classifier with LLM checkers, and kappa 0.94. Covers 1859 (dev) and a pre-registered Feb 1872 holdout. | Two short windows only. A transformer classifier that failed its pass bar. No index, no aa/Ak validation, no catalogue, no dossiers, no paper. The closest anticipation of steps 1–3 and 6. |
| Sánchez Romero, C. et al. (2025). Aurora records in the Spanish newspaper *Extremadura* for 1923–2017. HGSS 16:13–22. [10.5194/hgss-16-13-2025](https://doi.org/10.5194/hgss-16-13-2025) | OCR keyword search of one regional newspaper, then manual reading: 31 articles, 12 observation reports. Cites published Kp and Dst. | One newspaper, manual classification, no ML, no index, no catalogue of new storms. |
| Vilas, D., Vaquero, J. M. et al. (2026). Benchmarking open-source LLMs for drought impact extraction in historical newspapers. EGU26-23012. https://meetingorganizer.copernicus.org/EGU26/EGU26-23012.html | LLM extraction pipeline (CienaLLM, Qwen, DeepSeek) on about 1M pages of OCR text from Spanish newspapers, 1923–1993. Proposes an OCR-quality threshold. | Drought, not aurora. Same group (Vaquero) as the Extremadura aurora paper, so a natural future competitor. |
| Kawamura, A. D., Hayakawa, H. et al. (2016). Aurora candidates from the chronicle of Qīng dynasty in several degrees of relevance. PASJ. [10.1093/pasj/psw074](https://doi.org/10.1093/pasj/psw074); arXiv:1608.02739 | Keyword search of a digital chronicle corpus: 111 candidates graded by relevance and cross-matched with Western records. | Chronicles, not newspapers. Keyword search only, no ML. No index. |
| Neuhäuser, D. L., Neuhäuser, R., Chapman, J. (2017). New sunspots and aurorae in the historical Chinese text corpus? Comments on uncritical digital search applications. arXiv:[1711.05132](https://arxiv.org/abs/1711.05132) | Critique of keyword or digital searching for aurorae: false positives and dating errors. | A methodological caution relevant to steps 1–2. It argues for human-verified evidence, which the step-5 dossiers address. |
| MacDonald, E. A. et al. (2015). Aurorasaurus: a citizen science platform for viewing and reporting the aurora. Space Weather. [10.1002/2015SW001214](https://doi.org/10.1002/2015SW001214) | Keyword-filtered tweets, verified by humans or crowd, mapped as aurora sightings in real time. | Modern social media, not historical newspapers. No historical index. |
| Case, N. A., MacDonald, E. A., Viereck, R. (2016). Using citizen science reports to define the equatorial extent of auroral visibility. Space Weather. [10.1002/2015SW001320](https://doi.org/10.1002/2015SW001320) | Equatorward visibility boundary from public reports, compared with Kp and the NOAA OVATION model. | The conceptual analogue of "text reports → geomagnetic proxy validated against an index", but for 2014–15 only. |
| Lockwood, M., Owens, M. J. et al. (incl. Vázquez, M.) (2025). The 2024 May event in the context of auroral activity over the past 375 yr. MNRAS 540:3596. [10.1093/mnras/staf827](https://doi.org/10.1093/mnras/staf827) | Long-term auroral activity and the lowest-latitude events, using compiled aurora catalogues and geomagnetic data. | No newspaper mining or ML. Event cutoff at QD latitude ≤31°, so most US mid-latitude storms are excluded. |
| Silverman, S. M. — New England auroral observations 1720–1948 and related catalogues. NASA SPDF https://spdf.gsfc.nasa.gov/pub/data/aaa_special-purpose-datasets/aaa_historical_aurora/00readme ; Silverman & Cliver (2001) JASTP 63:523 (May 1921) | Hand-compiled aurora catalogues drawing on diaries, newspapers and weather reviews, plus storm studies that use newspaper accounts. | Manual, regional, no ML, no normalised index. Useful as validation for Aurora Archives. |
| Love, J. J., Hayakawa, H., Cliver, E. W. (2019). Intensity and impact of the New York Railroad superstorm of May 1921. Space Weather. [10.1029/2019SW002250](https://doi.org/10.1029/2019SW002250); Hayakawa, H. et al. (2023). The extreme space weather event of 1872 February. ApJ. [10.3847/1538-4357/acc6cc](https://doi.org/10.3847/1538-4357/acc6cc) | Single-storm studies that compile many newspaper reports by hand to find the lowest-latitude aurora and the storm's impacts. | One storm each, manual. Aurora Archives automates this at scale and for every night. |
| Carrasco, V. M. S., Vaquero, J. M. (2025). A forgotten aurora: revisiting the 19 March 1950 aurora australis. Atmosphere 16:615. [10.3390/atmos16050615](https://doi.org/10.3390/atmos16050615) | Trove newspapers combined with geomagnetic data for one event. | One event, manual. |
| Agrawal, A., Hough, S. E., Mousavi, S. M., Hellweg, M. (2026). The digital archivist: automating legacy macroseismic data processing using LLMs. SRL. [10.1785/0220250362](https://doi.org/10.1785/0220250362) | Gemini 2.5 Pro extracts felt reports and intensities from 1957 USCGS abstracts; the resulting shake map matches instrumental data. | Earthquakes, archival survey reports rather than newspapers. Closest analogue for "LLM extraction validated against instruments". |
| Avcıoğlu, A., Demir, O., Görüm, T. (2025). An automated approach for developing geohazard inventories using news. NHESS 25:2421. [10.5194/nhess-25-2421-2025](https://doi.org/10.5194/nhess-25-2421-2025) | TF-IDF, NMF and NER on Turkish news (1997–2023) to build an inventory of 13,940 hazard events. | Modern news, ground hazards. A TF-IDF pipeline analogue. |
| Google Research (2026-03-12). Introducing Groundsource: turning news reports into data with Gemini. https://research.google/blog/introducing-groundsource-turning-news-reports-into-data-with-gemini/ | Gemini classifies news as real flood events and resolves dates and places, giving 2.6M flash-flood records from 2000 onward. | Floods, modern news. Analogue of LLM event-dating and location resolution. |
| Yu, Y. et al. (2025). WXImpactBench. arXiv:[2505.20249](https://arxiv.org/abs/2505.20249); Yu, Y. et al. (2025). WeatherArchive-Bench. arXiv:[2510.05336](https://arxiv.org/abs/2510.05336) | Benchmarks of LLMs on disruptive-weather impacts in historical newspaper archives. | Weather, not aurora. Benchmarks rather than a geophysical index. |
| Dell, M. et al. (2023). American Stories: a large-scale structured text dataset of historical U.S. newspapers. NeurIPS Datasets & Benchmarks. arXiv:[2308.12477](https://arxiv.org/abs/2308.12477) | The underlying corpus. | Not a space-weather study. Cite it as the data source. |
| SolarStorms.org (Odenwald et al.), Space Weather Newspaper Archives. https://www.solarstorms.org/SRefStorms.html | A hand-curated archive of about 306 newspaper articles on storms from 1859 to 2003. | Manual. Not an index. |

## (c) What I searched

- **WebSearch (standard and extended):**
  - newspaper aurora catalogues and Chronicling America
  - LLMs on historical newspapers for aurora and geomagnetic storms
  - "American Stories" with aurora, geomagnetic or space weather
  - ML and text mining of historical aurora reports
  - Sánchez Romero 2025 HGSS
  - shmanubhav/aurora-catalog
  - Hayakawa newspaper studies (1872, 1882, 1903, 1909, 1921)
  - Silverman newspaper catalogues
  - LLM felt-report extraction (SSA)
  - Trove and aurora australis
  - auroral indices vs aa
  - "Machine reading of aurora sighting reports"
  - Aurorasaurus and Case 2016
  - AGU Fall Meeting ML / historical newspaper abstracts
  - Japanese (新聞 オーロラ 記録 明治), Chinese (报纸 极光 记录) and Spanish (prensa histórica aurora catálogo) queries
  - LLM newspaper hazard extraction (floods, earthquakes, drought)
  - a 2026 preprint query for US newspaper aurora classifiers
- **WebFetch:**
  - HGSS 16:13 2025; HGSS 9:133 2018
  - EGU26-23012; EGU2018-3368 (Wagner/Neuhäuser)
  - ESS Open Archive 10.1002/essoar.10506581.1 (Bayesian oval)
  - SSA press releases (Agrawal)
  - NHESS 25:2421; Google Groundsource blog
  - MDPI Atmosphere 16:615
  - Kyoto Univ. 2022 press release (Ebihara et al., GDJ 10.1002/gdj3.140)
  - NASA SPDF historical-aurora readme
  - SolarStorms newspaper archive
  - stdaily 2026-10 (HIT Shenzhen, 1770 gazetteer)
  - github.com/shmanubhav/aurora-catalog (landing page; the commits page was robots-blocked)
- **arXiv export API:**
  - abs/all/ti boolean queries for aurora AND newspaper(s), geomagnetic AND newspaper, aurora AND "language model", "Chronicling America", "American Stories", ti:aurora AND historical, and others
  - abstracts pulled for 1608.02739, 1711.05132, 2603.25051, 2512.11635, 2603.22906, 1302.2190, 2510.05336 and 2505.20249
  - no aurora/newspaper ML paper found
- **Zenodo API:**
  - title:aurora AND newspaper(s); "American Stories" aurora; aurora chronicling america; geomagnetic storm newspapers; creator "Sharma, Anubhav"
  - concept record 23275917, versions: only v1.0.0-prereg
  - downloaded and read the repo snapshot: README, results/1859-results.md, prereg/1872_preregistration.md, CITATION.cff (in /tmp/novelty_method/dl/z1/)
- **Crossref:** bibliographic queries (noisy, nothing new), plus DOI verification of every DOI cited above.
- **Failed:**
  - OpenAlex: HTTP 429 on every query
  - Semantic Scholar: rate-limited, 1 of 8 queries returned
  - GitHub API and gh: 403, repo not enabled for this session; the add_repo permission request went unanswered
  - ESS Open Archive PDF 10.22541/essoar.173385818.81784736: client error, content unknown

These gaps mean coverage of ESS Open Archive, AGU 2023–2025 abstracts (confex pages were not fetched directly) and recent commits to the live GitHub repo is incomplete.
