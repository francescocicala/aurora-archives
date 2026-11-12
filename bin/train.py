"""Train the sighting classifier on agent labels and report cross-validated precision/recall.

Usage: python bin/train.py LABEL_DIR OUT_MODEL.pkl
LABEL_DIR holds sample.tsv, batches/*.txt and labels/*.tsv (id, sighting, obs_date, place, foreign).
"""
import glob, pickle, re, sys
import numpy as np, pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold, cross_val_predict
from sklearn.pipeline import make_pipeline, make_union
from sklearn.metrics import precision_recall_curve, roc_auc_score

ldir, out = sys.argv[1:3]
texts = {}
for f in glob.glob(f"{ldir}/batches/*.txt"):
    for sid, body in re.findall(r"===== (s\d+) =====\n(.*?)\n===== end \1 =====", open(f).read(), re.S):
        texts[sid] = body.split("\n", 1)[1] if "\n" in body else body
lab = pd.concat([pd.read_csv(f, sep="\t", header=None, names=["sid", "sighting", "obs_date", "place", "foreign"], dtype=str)
                 for f in glob.glob(f"{ldir}/labels/*.tsv") if "_" not in f.rsplit("/", 1)[-1]])
s = pd.concat([pd.read_csv(f, sep="\t", dtype=str) for f in glob.glob(f"{ldir}/sample*.tsv")]).merge(lab, on="sid")
s["text"] = s.sid.map(texts)
s = s.dropna(subset=["text"])
y = (s.sighting.str.upper() == "YES").astype(int).values

model = make_pipeline(
    make_union(TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True, lowercase=True),
               TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=3, sublinear_tf=True, max_features=200000)),
    LogisticRegression(C=4, class_weight="balanced", max_iter=3000))
groups = s.date.str[:4].astype(int) // 5
p = cross_val_predict(model, s.text, y, groups=groups, cv=GroupKFold(5), method="predict_proba")[:, 1]
r1 = (s.stratum != "active").values
print(f"metrics on round-1 (random+storm) items only: n={r1.sum()} pos={y[r1].sum()} AUC={roc_auc_score(y[r1], p[r1]):.3f}")
for t in (0.3, 0.5):
    k = (p >= t) & r1
    print(f"  t={t}: P={y[k].mean():.3f} R={k[(y == 1) & r1].sum() / ((y == 1) & r1).sum():.3f}")
pr, rc, th = precision_recall_curve(y, p)
f1 = 2 * pr * rc / (pr + rc + 1e-9)
i = f1[:-1].argmax()
print(f"n={len(y)} pos={y.sum()} AUC={roc_auc_score(y, p):.3f} best-F1={f1[i]:.3f} at t={th[i]:.2f} (P={pr[i]:.3f}, R={rc[i]:.3f})")
for t in (0.3, 0.5, 0.7):
    k = p >= t
    print(f"t={t}: P={y[k].mean():.3f} R={k[y == 1].mean():.3f}")
s.assign(p_cv=p).drop(columns="text").to_csv(f"{ldir}/cv_predictions.tsv", sep="\t", index=False)
model.fit(s.text, y)
pickle.dump({"model": model, "threshold": float(th[i])}, open(out, "wb"))
