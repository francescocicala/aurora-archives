# Prior modern (post-1950) work on the 49 confirmed pre-1868 storms

Checked 2026-11-12. The storm list is `results/dossiers/catalogue_nights_pre1868_storms.tsv`, rows with confirmed=True. This note extends `literature_check_candidates.md` and `check_new_storms.md`, and corrects one of their findings (1839-09-03).

**Status key**
- **STUDIED**: a post-1950 paper analyses this storm specifically.
- **MENTIONED**: the date appears in a modern catalogue, list or review, or in an adjacent study, but nobody has analysed the storm itself.
- **NOT FOUND**: none of the checks below turned it up. This does not prove that no study exists.

"top15" marks the 15 storms with the lowest southernmost US latitude. They were checked more thoroughly.

**Result: 4 STUDIED, 4 MENTIONED, 41 NOT FOUND.**

## Method and coverage
- **Downloaded full texts, searched by regex for every storm date in several formats**:
  - Lockwood et al. 2025 MNRAS (full PDF from NORA)
  - Hayakawa et al. 2018 ApJ (arXiv:1811.02786) and 2019 Space Weather (arXiv:1908.10326)
  - Hayakawa et al. 2022 ApJ, Colaba (arXiv:2109.13020)
  - Vázquez, Vaquero & Gallego (arXiv:1309.1502)
  - Cliver & Svalgaard 2004 (DTIC ADA434906 copy)
  - Nevanlinna 2004 Ann. Geophys. 22:1691
  - Nevanlinna & Häkkinen 2010 Ann. Geophys. 28:917
  - Hejda et al. 2021 Ann. Geophys. 39:439
  - Hejda et al. 2023 HGSS 14:51
  - Shea & Smart 2006 ASR Loomis compendium (Zenodo 1258762)
  - Cliver et al. 2022 "Extreme solar events" review (arXiv:2205.09265)
  - Several 1859 papers (arXiv:2008.13180, 2010.15762, 2005.13453, 1608.07702)
- **PANGAEA**: the list of the 73 Clementinum (Prague) storms, 1839-1849.
- **Crossref**: DOI metadata and abstracts for Viljanen et al. 2014 (SWSC, doi:10.1051/swsc/2014008; Russian observatories 1850-62; the abstract names only Carrington), Knipp et al. 2021 (doi:10.1051/swsc/2021011), Valach et al. 2019, Wagner et al. 2023 and Hayakawa et al. 2026.
- **arXiv API**: abstract searches for "aurora" combined with 1837/39/47/51/52/60/62/65/66.
- **Web searches**: exact date phrases for the lowest-latitude storms.

**Not accessible (blocked or paywalled):**
- NASA ADS (WAF captcha, no token).
- SWSC full-text HTML (captcha).
- Silverman 2006 ASR 38:136 ("Comparison of the aurora of Sep 1/2 1859 with other great auroras").
- Vázquez et al. 2006 Sol. Phys. 238:405.
- Wagner, Neuhäuser & Arlt 2023, Astron. Nachr., doi:10.1002/asna.20220078. It reconstructs the oval for "nine historical storms 1716-1882", but the event list could not be read. **Check it**: it may contain one of our dates.
- Love 2014 Weatherwise (full text).
- OpenAlex and Semantic Scholar (rate-limited).

The "Boteler 2021 SWSC timelines" paper in the brief is actually **Knipp, Bernstein, Wahl & Hayakawa 2021**, doi:10.1051/swsc/2021011. It lists 14 great auroral storms over 500 years; only the abstract was readable this session. I could not identify the "Odagi et al. 2020" Helsinki paper. The Helsinki storm list used here is Nevanlinna 2004.

## Table
| storm (first-last) | south. lat / place | Ak_pct | priority | modern study? | citation(s) | note |
|---|---|---|---|---|---|---|
| 1827-08-28 | 37.5 Richmond, Va | - |  | **NOT FOUND** | Silliman, AJS 1st ser. 14:91 (1828) is a contemporary compilation, not a modern study. | Pre-magnetometer. Silverman's New England catalogue has 10 entries. |
| 1827-09-09 | 39.7 Wilmington, De | - |  | **NOT FOUND** | - |  |
| 1830-07-14 | 38.4 Charlestown, Wv | - |  | **NOT FOUND** | - |  |
| 1833-05-17 | 38.4 Charlestown, Wv | - |  | **NOT FOUND** | - |  |
| 1836-11-12 | 42.4 Cambridge, MA | - |  | **NOT FOUND** | - |  |
| 1837-01-25 | 37.5 Richmond, Va | - |  | **NOT FOUND** | Olmsted, AJS 32:176 (1837) is contemporary. | Olmsted called it a 'memorable' aurora. Not in Lockwood 2025 Table 2. |
| 1837-07-01 | 34.7 Cheraw, Sc | - | top15 | **NOT FOUND** | AJS 33:143ff (1838) is contemporary. | AJS reports a sighting at Columbus, GA (32.6N). |
| 1837-11-13 to 1837-11-15 | 33.8 Edgefield, Sc | - | top15 | **NOT FOUND (19th-c. text reprinted)** | Shea & Smart 2006, ASR 38:313, doi:10.1016/j.asr.2006.07.005 reprints Loomis's 1860s tables, which list the European times of maximum for 1837 Nov 13/14. | The reprint is not a modern analysis. Barnard (Tuscaloosa) and Haile & Herrick (needle disturbance) are in AJS 34:267-269. |
| 1839-09-03 | 30.0 New Orleans, La | - | top15 | **STUDIED** | Hejda, Valach & Revallo 2021, Ann. Geophys. 39:439, doi:10.5194/angeo-39-439-2021. Hejda et al. 2023, HGSS 14:51, doi:10.5194/hgss-14-51-2023. Data: PANGAEA doi:10.1594/PANGAEA.936848. | They analyse the Prague-Clementinum magnetogram, which starts suddenly on the evening of 3 Sep and shows two sharp H depressions early on 4 Sep. They read these as substorm or auroral-oval currents. **This corrects the earlier 'no modern study' note.** The paper does not analyse the US aurora reports. |
| 1840-02-09 | ?  | - |  | **MENTIONED (data catalogue)** | Clementinum storm data, 1839-1849: Hejda, Revallo & Valach 2021, PANGAEA doi:10.1594/PANGAEA.936921 (one of 73 storms). Described in Geosci. Data J. 10:39 (published online 2021), doi:10.1002/gdj3.141. | Listed as a digitised storm (1840-02-09; also 02-06 and 02-07). There is no event analysis. |
| 1846-10-19 | 38.9 Dc | 77.5 |  | **NOT FOUND** | Not among the 73 Clementinum storms. Not in the Lockwood 2025 text. |  |
| 1847-04-07 | 38.9 Washington, DC | 98.2 |  | **NOT FOUND** | Not in the Clementinum storm list (which has 1847-10-23 and 10-25). Not in Barlow 1849. Not in Lockwood 2025. | The well-studied 1847 storm is 24 Oct (Cliver & Dietrich 2013), not this one. |
| 1848-11-17 to 1848-11-18 | 32.8 Lake Providence, LA | 99.8 | top15 | **STUDIED** | Valach et al. 2019, SWSC 9:A11, doi:10.1051/swsc/2019008. Lockwood et al. 2025, MNRAS 540:3596, doi:10.1093/mnras/staf827 (Table 2, an extreme night; St Croix QD latitude 29.5). Clementinum dataset (PANGAEA.936921). | A control event. Well covered. |
| 1850-09-30 | 41.5 Cleveland, OH | 92.0 |  | **NOT FOUND** | - |  |
| 1851-02-18 | 38.9 Washington, DC | 92.6 |  | **NOT FOUND** | - |  |
| 1851-09-03 | 32.0 Savannah, GA coast | 99.8 | top15 | **NOT FOUND** | The only secondary source is Prescott 1860 / NRCan chronology ('September 1851'). | The telegraph anecdote may refer to 3 Sep or 29 Sep. |
| 1851-09-29 | 32.8 Charleston, SC | 99.3 | top15 | **NOT FOUND** | Gibbes and Winchell, AJS 2nd ser. 13 (1852), are contemporary. | Helsinki K=9 (own derivation). A strong candidate for a gap. |
| 1852-01-19 | 35.8 Raleigh, Nc | 95.5 | top15 | **NOT FOUND** | - |  |
| 1852-02-18 to 1852-02-20 | 38.2 Staunton, Va | 99.9 |  | **MENTIONED (review / list)** | Nevanlinna 2004, Ann. Geophys. 22:1691, doi:10.5194/angeo-22-1691-2004 lists '18 February 1852' among Helsinki days with Ak>150. Cliver & Dietrich 2013, SWSC 3:A31, doi:10.1051/swsc/2013053 assign the Boston paper-burning telegraph anecdote to 19 Feb 1852. | No dedicated modern study. Shea & Smart 2006 reprints the Loomis telegraph text for 19 Feb 1852. |
| 1853-09-01 | 40.1 St Clairsville, Oh | 99.8 |  | **NOT FOUND** | - |  |
| 1858-03-12 to 1858-03-14 | 38.8 Alexandria, VA | 99.2 |  | **NOT FOUND** | - | Nevanlinna 2004 lists 9 Apr 1858, not March. |
| 1859-02-22 | 38.9 Washington, DC | 95.5 |  | **NOT FOUND** | - |  |
| 1859-06-08 | 38.6 Sacramento, California | 98.3 |  | **NOT FOUND** | - |  |
| 1859-08-28 to 1859-08-29 | 29.3 Galveston, TX | 95.1 | top15 | **STUDIED** | Green & Boardsen 2006, ASR 38:130. Hayakawa et al. 2018, ApJ 869:57, doi:10.3847/1538-4357/aae47c. Hayakawa et al. 2019, Space Weather 17, doi:10.1029/2019SW002269 (arXiv:1908.10326). Cliver & Svalgaard 2004, Sol. Phys. 224:407. | Carrington precursor storm. Extensively studied, including from US newspapers. |
| 1859-09-01 to 1859-09-02 | 24.6 Key West, FL | 91.1 | top15 | **STUDIED** | Tsurutani et al. 2003, JGR 108:1268, doi:10.1029/2002JA009504. Cliver & Svalgaard 2004. Green et al. 2006. Hayakawa 2018, 2019. Hayakawa et al. 2022, ApJ, doi:10.3847/1538-4357/ac2601. Love et al. 2024, SWSC, doi:10.1051/swsc/2024015. | The Carrington storm. |
| 1859-10-03 | ?  | 97.5 |  | **NOT FOUND** | - |  |
| 1859-10-17 to 1859-10-18 | 37.8 San Francisco, California | 99.7 |  | **NOT FOUND (19th-c. text reprinted)** | Shea & Smart 2006 (Loomis reprint) mentions an 'Oct. 18, 1859' aurora. | Not a modern analysis. Hayakawa 2019 mentions Oct 1859 only as a sunspot-number peak. |
| 1859-12-12 | 42.4 Boston, MA | 99.4 |  | **NOT FOUND** | - |  |
| 1859-12-14 | 36.9 Norfolk, VA | 93.2 | top15 | **NOT FOUND** | - |  |
| 1860-03-26 to 1860-03-29 | 37.5 Richmond, Va | 100.0 |  | **NOT FOUND** | - | Nevanlinna 2004 lists '29 February 1860' (Ak>150). Our Helsinki derivation puts the large storm on 29 Mar 1860 UT. That could be the same event with a month misprint, but this is unverified. |
| 1860-04-09 to 1860-04-10 | 41.0 Bloomsburg, Pa | 99.3 |  | **NOT FOUND** | - |  |
| 1860-04-13 | 38.9 Washington, D.C. | 98.2 |  | **NOT FOUND** | - |  |
| 1860-07-04 | 37.3 Ca | 99.6 |  | **MENTIONED (adjacent study)** | Hayakawa, Hooper, Rodger, Ebihara, Nevanlinna & Willis 2026, JSWSC 16, doi:10.1051/swsc/2026003 ('Did Alfred Russel Wallace see an aurora near the equator?'). | That paper dates Wallace's Waigeo sighting to 4 Jul 1860 and says 'contemporaneous geomagnetic measurements showed no significant geomagnetic disturbances'. It does not discuss US/California reports. The claim conflicts with our Ak_pct of 99.6; this is probably a UT-day offset, since the California evening falls on 5 Jul UT. Check before relying on either. |
| 1860-07-11 | 42.3 Detroit, Michigan | 98.7 |  | **NOT FOUND** | - |  |
| 1860-07-18 to 1860-07-20 | 38.9 local | 96.8 |  | **NOT FOUND** | - |  |
| 1860-08-06 to 1860-08-09 | 31.2 Pike County, Mississippi | 99.8 | top15 | **NOT FOUND** | - | Silverman's New England catalogue records telegraph effects on 8 Aug. A strong gap candidate. |
| 1860-09-06 to 1860-09-07 | 30.0 New Orleans, La | 100.0 | top15 | **NOT FOUND** | - | Helsinki Ak(H)=186, the 8th highest day of 1844-1897 (own derivation). It is not in Nevanlinna's 2004 list of days with Ak>150, possibly because that list used a different component. **The strongest unstudied candidate.** |
| 1860-09-15 to 1860-09-16 | 38.2 Staunton, Va | 99.4 |  | **NOT FOUND** | - |  |
| 1860-12-15 | 38.0 Evansville, In | 99.3 |  | **NOT FOUND** | - |  |
| 1861-03-09 | 34.4 Oxford, Mississippi | 95.1 | top15 | **NOT FOUND** | Love 2014, Weatherwise 67(5):34, doi:10.1080/00431672.2014.939912 (Civil War aurorae) may be relevant. Only the abstract was read, and it does not mention March 1861. |  |
| 1862-08-04 to 1862-08-05 | 40.7 New York Ny, Ny | 99.8 |  | **NOT FOUND** | - |  |
| 1862-08-19 | 40.4 Keokuk, Ia | 97.3 |  | **NOT FOUND** | - |  |
| 1862-12-14 | 39.0 Offutt's Cross Roads, MD | 99.7 |  | **MENTIONED (popular / archive)** | solarstorms.org Space Weather Newspaper Archive: 'December 14, 1862 - The Civil War Aurora' (soldiers' letters, Fredericksburg). https://www.solarstorms.org/SRefStorms.html. Love 2014 (Weatherwise, popular magazine) is likely, but this was not verified from the full text. | No peer-reviewed geophysical analysis found. The aurora is well known in Civil War history. |
| 1863-04-09 | 39.8 Hanover, PA | 97.3 |  | **NOT FOUND** | - |  |
| 1864-08-24 | 44.6 Hyde Park, Vt | 98.2 |  | **NOT FOUND** | - |  |
| 1865-08-02 | 36.9 Norfolk, Va | 90.4 | top15 | **NOT FOUND** | - | Nevanlinna 2004 lists 5 Aug 1865 (Ak>150), three days later. It could be the same active interval but is not the same night. |
| 1866-02-20 to 1866-02-21 | 32.4 Meridian, Ms | 99.3 | top15 | **NOT FOUND** | - | Lowest-latitude US report (Meridian MS, 32.4N). Gap candidate. |
| 1866-03-07 | ?  | 97.5 |  | **NOT FOUND** | - |  |
| 1867-09-25 to 1867-09-27 | 38.8 Alexandria, Va | 97.8 |  | **NOT FOUND** | - |  |


## Key points
- **Correction: 1839-09-03 is STUDIED magnetically.** Hejda et al. 2021 (Ann. Geophys. 39:439) analyse the Prague magnetogram and interpret it as auroral-oval or substorm currents. The US/low-latitude aurora side is still unpublished in modern work. Their data and our New Orleans (30.0N) and Edgefield SC reports complement each other.
- **The only storms with real modern analyses are 1839-09, 1848-11 and the two 1859 Carrington-period storms.** Every other storm, including the lowest-latitude ones, lacks a modern study. The lowest-latitude unstudied storms are 1860-09-06/07 (30.0N), 1860-08-06/09 (31.2N), 1851-09-03 (32.0N), 1866-02-20 (32.4N), 1851-09-29 (32.8N) and 1837-11-13 (33.8N).
- **Nevanlinna 2004 lists the Helsinki days with daily Ak>150** as: 24 Sep 1847, 20 Dec 1847, 18 Feb 1852, 9 Apr 1858, 3 Sep 1859, 29 Feb 1860, 5 Aug 1865, 17 Oct 1870 and 24 Oct 1872. Only 18 Feb 1852 matches one of our storms. 29 Feb 1860 and 5 Aug 1865 are near our 1860-03-26/29 and 1865-08-02, but not the same nights.

## Prior newspaper-derived aurora index work
**Conclusion: I found no prior continuous aurora index or catalogue built from Chronicling America or American Stories, and no published LLM or NLP aurora extraction.** The only comparable work is the GitHub repo shmanubhav/aurora-catalog (1859 and 1872). This confirms and slightly extends `known_storms_and_prior_work.md`. The closest work falls into four groups.

**Newspapers as sources for single events, read by hand**
- Green & Boardsen 2006 and Green et al. 2006 (ASR 38) for 1859.
- Hayakawa et al. 2018/2019 cite many 1859 newspapers (for example *La Sociedad*, Mexico, and *El Mercurio de Valparaíso*).
- Carrasco & Vaquero 2025, Atmosphere 16:615 (Trove, 1950).

**OCR keyword searches**
- Sánchez Romero et al. 2025, HGSS 16:13 (hgss-2024-16). Keyword search of one Spanish newspaper, 1923-2017, yielding 31 articles. This is the nearest methodological analogue, but it covers a single title and finds few events.

**Curated archives that are not indices**
- solarstorms.org "Space Weather Newspaper Archives" (Odenwald; for example 1859 and 14 Dec 1862).
- Readex blog posts on 1859.

**Corpora and general NLP with no aurora application**
- American Stories (Dell et al. 2023, arXiv:2308.12477). A search for "American Stories" with aurora or space weather returned nothing beyond the dataset itself.
- Chronicling Germany (arXiv:2401.16845).

**Non-newspaper long catalogues (for comparison)**
- Silverman NE catalogue / SPDF.
- Vázquez et al. 2014 (1700-1905).
- Lockwood et al. 2025 (223,916 records, no text mining).
- The Clementinum and Helsinki magnetometer storm lists.
