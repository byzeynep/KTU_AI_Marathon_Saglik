"""Shared image features and portable inference. No pickle loading."""
import csv, json, pathlib, time
import numpy as np
from PIL import Image
def read_rows(path):
    with open(path,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def features(path):
    # Educational minimum: no spatial features, histograms or deep model.
    with Image.open(path) as image:
        pixels=np.asarray(image.convert('L'),dtype=np.float32)/255
    return np.array([pixels.mean(),pixels.std()],dtype=np.float32)

def load_model(path):
    with np.load(path,allow_pickle=False) as z:return {k:z[k] for k in z.files}
def probabilities(model,x):
    x=(np.asarray(x)-model['mean'])/model['scale']
    scores=x@model['weights'].T+model['bias']
    if str(model['task'].item())=='multilabel' or scores.shape[-1]==1:
        p=1/(1+np.exp(-np.clip(scores,-50,50)))
        return p if str(model['task'].item())=='multilabel' else np.concatenate([1-p,p],axis=-1)
    scores-=scores.max(axis=-1,keepdims=True);p=np.exp(scores);return p/p.sum(axis=-1,keepdims=True)
def predict(model,path):
    start=time.perf_counter();p=probabilities(model,features(path)[None])[0];ms=(time.perf_counter()-start)*1000
    pred='|'.join(str(int(v)) for v in p>=.5) if str(model['task'].item())=='multilabel' else str(int(p.argmax()))
    return p,pred,ms
