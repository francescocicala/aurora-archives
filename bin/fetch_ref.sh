#!/bin/sh
# Downloads third-party reference data that this repository does not redistribute.
set -e
cd "$(dirname "$0")/../data/ref"
curl -sLO https://space.fmi.fi/MAGN/K-index/HELSINKI/Hels_H_K1844-97_05
curl -sLO https://space.fmi.fi/MAGN/K-index/HELSINKI/Hels_D_K1844-80_06
curl -sL -o aaH_data.txt https://raw.githubusercontent.com/Carl-Haines/SVM_for_aaH/main/aaH_data.txt
curl -sL -o pl.zip https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2020_Gazetteer/2020_Gaz_place_national.zip && unzip -o -q pl.zip && rm pl.zip
python3 - <<'P'
import pandas as pd
a = pd.read_csv("aaH_data.txt", sep=r"\s+", header=None, usecols=[0, 1, 2, 3, 5], names=["y", "m", "d", "h", "aaH"])
a["date"] = pd.to_datetime(dict(year=a.y, month=a.m, day=a.d))
a.groupby("date").aaH.agg(aaH_mean="mean", aaH_max="max").round(1).to_csv("aaH_daily_1868_2017.csv")
r = []
for l in open("Hels_H_K1844-97_05"):
    p = l.split()
    if len(p) >= 3 and p[0].isdigit():
        r.append((pd.to_datetime(p[0]), p[1], int(p[-1])))
d = pd.DataFrame(r, columns=["date", "K", "Ak"]); d.loc[d.Ak >= 999, "Ak"] = None
d.to_csv("helsinki_H_Ak_1844_1897.csv", index=False)
P
