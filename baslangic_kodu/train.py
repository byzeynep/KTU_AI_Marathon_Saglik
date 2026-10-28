"""CPU baseline using training data only, reports validation score."""
import argparse,json,pathlib,sys,time
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import f1_score
from common import features,read_rows,probabilities
def main():
    p=argparse.ArgumentParser();p.add_argument('--data',required=True);p.add_argument('--output',required=True);p.add_argument('--seed',type=int,default=20261023);a=p.parse_args()
    d=pathlib.Path(a.data);out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=True);card=json.loads((d/'dataset_card.json').read_text(encoding='utf-8'));task=card['task'];k=len(card['classes'])
    train=read_rows(d/'train.csv');val=read_rows(d/'val.csv');x=np.stack([features(d/r['path']) for r in train]);v=np.stack([features(d/r['path']) for r in val]);scaler=StandardScaler().fit(x);xs=scaler.transform(x)
    if task=='multilabel':
        y=np.array([[int(b) for b in r['label'].split('|')] for r in train]);yv=np.array([[int(b) for b in r['label'].split('|')] for r in val]);models=[]
        for c in range(k):models.append(SGDClassifier(loss='log_loss',alpha=.001,max_iter=1000,tol=1e-4,class_weight='balanced',random_state=a.seed).fit(xs,y[:,c]))
        weights=np.concatenate([m.coef_ for m in models]);bias=np.concatenate([m.intercept_ for m in models])
    else:
        y=np.array([int(r['label']) for r in train]);yv=np.array([int(r['label']) for r in val]);m=SGDClassifier(loss='log_loss',alpha=.001,max_iter=1000,tol=1e-4,class_weight='balanced',random_state=a.seed).fit(xs,y);assert list(m.classes_)==list(range(k));weights=m.coef_;bias=m.intercept_
    model={'weights':weights,'bias':bias,'mean':scaler.mean_,'scale':scaler.scale_,'task':np.array(task),'classes':np.array(card['classes'])};np.savez_compressed(out/'model.npz',**model)
    prob=probabilities(model,v);pred=(prob>=.5).astype(int) if task=='multilabel' else prob.argmax(axis=1)
    result={'track':card['track'],'split':'val','macro_f1':float(f1_score(yv,pred,average='macro',zero_division=0)),'train_count':len(train),'val_count':len(val),'seed':a.seed,'note':'Classical CPU baseline; not a deep learning result or clinical model.'}
    (out/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result))
if __name__=='__main__':main()
