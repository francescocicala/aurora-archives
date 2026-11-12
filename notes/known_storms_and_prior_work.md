# Known storms (1800-1963) and prior work

Catalogue: `data/ref/known_storms.tsv` has 20 rows. Every row was checked against a paper abstract, a publisher page or a published table during this session (Nov 2026).

## Catalogue notes and caveats
- **Main ranking source.** Lockwood, Owens, Brown & Vazquez 2025, MNRAS 540:3596 (doi:10.1093/mnras/staf827). They surveyed 223,916 Northern Hemisphere aurora records from 1650 to 2024. Their Table 2 ranks 21 extreme nights by the lowest quasi-dipole (QD) geomagnetic latitude. An extreme night has an observation at QD latitude 31 deg or lower, plus a second sample within 10 deg. The pre-1964 entries are 1848-11-17, 1859-08-28, 1859-09-01/02, 1870-10-24, 1872-02-04/05, 1909-09-25, 1921-05-14, 1938-01-25, 1941-09-18, 1950-08-19, 1957-01-21 and 1958-02-11. For Table 4, 32 of the 56 low-latitude observations came from Silverman's collection.
- **Latitude conventions differ between sources and are not comparable without conversion.** Hayakawa et al. give the equatorward boundary of the auroral oval in invariant latitude (ILAT). Lockwood gives the lowest QD latitude where aurora was *seen*, which is often far below the oval because aurora on the horizon counts. Silverman & Cliver give geomagnetic latitude for overhead aurora versus horizon aurora.
- **Intensity values come from different indices:** Dst estimates from the literature, Dcx (Oulu's reconstructed Dst), aa/aaH, and Kyoto Dst (1957 onward). They are not directly comparable.
- **The `us_sightings` column.** It is "yes" only where a source I read documents sightings in the contiguous US: 1848, both 1859 storms, 1921 and Sep 1941. Everywhere else it is "unknown". For most of those storms (1872, 1882, 1903, 1909, 1938, 1940, 1946, 1958, 1960) US sightings are very likely, but I did not confirm them here. Silverman 2008 (JASTP) for 1872 and Love 2018 for 1882 are the first places to check.
- **Pre-1848 storms are not covered.** I found no peer-reviewed reconstruction for 1837, 1839, 1847, 1851 or 1852, and none of these dates is in Lockwood's extreme list. I left them out rather than guess. The Vazquez, Vaquero & Gallego catalogue (arXiv:1309.1502; about 15,600 North American auroral days from 1700 to 1905) and Silverman's files would be the place to look.
- **Two rows are weaker than the rest:**
  - 1960-11-13 has only a Kyoto Dst value, taken from a non-peer-reviewed site.
  - 1946-09-21 is "strong" (Dcx -163 nT), not great.
- **Authors of the 2021 timelines paper.** The JSWSC 11:29 (2021) "Timelines as a tool..." tables are cited by title because I did not confirm the author list.
- **1859 eyewitness list.** SPDF also hosts a separate 1859 eyewitness event list at `spdf.gsfc.nasa.gov/pub/event_lists/carrington_event_1859_auroral_sightings/`. I did not inspect it.

## SPDF historical aurora directory (Silverman collection) - readme summary
Source: `.../aaa_special-purpose-datasets/aaa_historical_aurora/00readme`, last updated 2005. The top readme lists five datasets **and does not describe any column formats**.
1. `cat_ancient_auroral_obs_666bce_1951` (GE-11D)
   - Silverman's catalogue of aurora observations from 666 BCE to 1951, plus reports from Greenland, Iceland and the Faroes for 1840-1967.
   - Notes, a bibliography and site coordinates are included.
   - Files are dBase III (.DBF) with ASCII .TXT copies, plus WordPerfect notes such as SILV1.NTS (1704-1914 annotations), ABBREV and BIBLIO.
   - About 75,000 observations in total. The field layout is not documented online and has to be read from the files themselves.
2. `auroral_notes_us_climat_data` (GE-11E)
   - Aurora notes taken from *Climatological Data of the United States*, 1914-1948, in four blocks (1914-23, 1924-32, 1933-40, 1941-48).
   - Per block:
     - `cldNNNN.txt` gives place names and observation dates.
     - `plNNNN.txt` gives place names and coordinates.
     - `notesusN.txt` holds notes.
     - `co2432.txt` gives city, state and county (1924-32 only).
   - Also included: event tables for the 7 Mar 1918 and 11 Aug 1919 aurorae. **This is the most directly useful US dataset for 1914-1948.**
3. `auroral_notes_canadian_monthly_weather_review` (GE-11F): 1880-1928.
4. `new_england_auroral_obs_1720_1948` (GE-11C). Each record is one fixed-width line: year, month, day, town, state, then a bracketed source code (e.g. [LOV], [PR]) or free-text description.
5. `daily_auroral_repts_se_canada_ne_us_1848_1853` (GE-11B)
   - About 1,900 handwritten pages of nightly logs, January 1848 to April 1853. The Canadian military posts reported every night except April-July 1850; US volunteers mostly reported on aurora nights.
   - Only four pages have been scanned. The rest is hard copy that has to be requested from NSSDC.

## Prior work on newspaper-derived or NLP aurora indices
**I found no published continuous, multi-decade daily or monthly aurora index built from US newspapers (Chronicling America or American Stories), and no use of LLMs or NLP for this.** The closest work:
- **Single-event newspaper studies.**
  - Green & Boardsen 2006 and Green et al. 2006 (Adv Space Res 38) used newspapers and other eyewitness accounts for 1859.
  - Carrasco & Vaquero 2025 (Atmosphere 16:615) used two Trove (Australian) articles for 19 Mar 1950.
- **One-newspaper catalogue.** Sanchez Romero et al. 2025, HGSS 16:13: an OCR keyword search of the Spanish newspaper *Extremadura*, 1923-2017, which found 31 aurora articles.
- **Curated archive.** solarstorms.org (Odenwald) runs a "Space Weather Newspaper Archives" collection of excerpts and Library of Congress PDFs for major storms since the 1800s. It is an archive, not an index.
- **Non-newspaper long series.** Vazquez et al. (arXiv:1309.1502) built annual series for 1700-1905 from the Fritz, Silverman and Angot catalogues. Lockwood et al. 2025 combined 223,916 records but did not use newspaper text mining.
- **Related NLP work that is not about aurora:**
  - American Stories (Dell et al., NeurIPS 2023) and Newswire (2024) are the text corpora themselves.
  - LLM post-OCR correction on British newspapers (Sheffield BLN600).
  - WXImpactBench (2025): an LLM benchmark built from Quebec newspapers, about terrestrial weather.
- **Conclusion.** A multi-decade, newspaper-derived US aurora index built with NLP or LLMs looks like a gap. Besides shmanubhav/aurora-catalog, I found nothing comparable.
