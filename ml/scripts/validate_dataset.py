import pandas as pd, json, numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
df = pd.read_csv("ml/data/sms_dataset.csv")
req = ["message_id","text","label","scam_type","source_type","source_reference","review_status","explanation"]
rep = {"rows":len(df),"missing_columns":[c for c in req if c not in df],"null_counts":df.isna().sum().to_dict(),
 "bad_labels":int((~df.label.isin(["scam","legitimate"])).sum()),"exact_duplicates":int(df.text.duplicated().sum()),
 "class_counts":df.label.value_counts().to_dict(),"source_counts":df.source_type.value_counts().to_dict(),
 "scam_types":df.scam_type.value_counts().to_dict(),"review_status":df.review_status.value_counts().to_dict(),
 "contradictory_labels":int((df.groupby("text").label.nunique()>1).sum())}
s = df.sample(min(1500,len(df)),random_state=0)
M = cosine_similarity(TfidfVectorizer().fit_transform(s.text)); np.fill_diagonal(M,0)
rep["near_duplicate_pairs_in_sample_gt_0.95"]=int((M>0.95).sum()//2)
rep["note"]="All data is synthetic. Near-duplicates are expected within template families and are handled by a grouped split."
json.dump(rep,open("ml/reports/dataset_report.json","w"),indent=2); print(json.dumps(rep,indent=1))
