import pandas as pd, numpy as np, json, joblib
from sklearn.model_selection import GroupShuffleSplit, GroupKFold, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, f1_score, confusion_matrix
SEED, MODEL_VERSION, DATA_VERSION = 42, "0.1.0", "synthetic-v1"
df = pd.read_csv("ml/data/sms_dataset.csv").drop_duplicates("text")
g = df.source_reference.str.extract(r"family=(.*)")[0].values
y = (df.label=="scam").astype(int).values; X = df.text.values
tr, te = next(GroupShuffleSplit(1,test_size=.25,random_state=SEED).split(X,y,g))
assert not set(g[tr]) & set(g[te]), "template family leakage"
vec = lambda: TfidfVectorizer(ngram_range=(1,2),sublinear_tf=True)
cands = {"MultinomialNB":MultinomialNB(alpha=.5),
 "LogisticRegression":LogisticRegression(max_iter=2000,C=5,class_weight="balanced"),
 "LinearSVC":CalibratedClassifierCV(LinearSVC(C=1,class_weight="balanced"),cv=3)}
def ev(yt,yp):
    p,r,f,_=precision_recall_fscore_support(yt,yp,average="binary",pos_label=1,zero_division=0)
    return dict(accuracy=accuracy_score(yt,yp),scam_precision=p,scam_recall=r,scam_f1=f,
      macro_f1=f1_score(yt,yp,average="macro"),confusion_matrix=confusion_matrix(yt,yp,labels=[0,1]).tolist())
cv = {n:ev(y[tr],cross_val_predict(make_pipeline(vec(),c),X[tr],y[tr],groups=g[tr],cv=GroupKFold(5))) for n,c in cands.items()}
best = max(cv,key=lambda k:cv[k]["macro_f1"])  # selection uses train-only grouped CV
fits = {n:make_pipeline(vec(),c).fit(X[tr],y[tr]) for n,c in cands.items()}
test = {n:ev(y[te],p.predict(X[te])) for n,p in fits.items()}
joblib.dump(fits[best],"ml/models/smsguard_pipeline.joblib")
info = dict(model_version=MODEL_VERSION,dataset_version=DATA_VERSION,model_type=best,language="en",seed=SEED,
  dataset_source="Synthetic English SMS (generated, fictional entities). UCI SMS Spam Collection not included: no network access in build environment.",
  split="GroupShuffleSplit 75/25 by template family; model chosen by GroupKFold(5) macro-F1 on train only",
  vectorizer="TF-IDF word 1-2gram, sublinear tf",n_train=int(len(tr)),n_test=int(len(te)),positive_class="scam")
json.dump(info,open("ml/models/model_info.json","w"),indent=2)
json.dump(dict(selected=best,test=test[best],test_all_models=test,cv_train=cv,
  caveat="Held-out SYNTHETIC data only. Not evidence of real-world fraud-detection accuracy."),open("ml/models/metrics.json","w"),indent=2)
print("selected:",best)
for k,d in test.items(): print(k,{m:round(v,3) for m,v in d.items() if m!="confusion_matrix"},d["confusion_matrix"])
