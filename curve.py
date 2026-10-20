# error-vs-shafts curve: rahel's cloth, a coin-flip cloth, and the same cloth with a shifted drift
import numpy as np, json
N=56
def over(i,j,k=90): return ((i+j+(j*i)//k)%4)<2
def cloth(k=90): return np.array([[over(i,j,k) for i in range(N)] for j in range(N)])
def kmeans(X,S,rng):
    X=X.astype(int); c=X[rng.choice(len(X),min(S,len(X)),replace=False)].astype(float)
    if len(c)<S: c=np.vstack([c,rng.random((S-len(c),X.shape[1]))])
    for _ in range(20):
        d=((X[:,None,:]-c[None])**2).sum(2); a=d.argmin(1)
        for k in range(S):
            if (a==k).any(): c[k]=X[a==k].mean(0)
    return a
def fit(D,S,restarts=10,seed=0):
    rng=np.random.default_rng(seed); best=None
    for _ in range(restarts):
        th=kmeans(D.T,S,rng); tr=kmeans(D,S,rng); T=np.zeros((S,S),bool)
        for r in range(S):
            for s in range(S):
                m=D[np.ix_(tr==r,th==s)]
                if m.size: T[r,s]=m.mean()>=.5
        for it in range(40):
            Tt=T[tr].astype(int); th=np.argmin(D.T.astype(int)@(1-Tt)+(1-D.T.astype(int))@Tt,axis=1)
            Ts=T[:,th].astype(int); tr=np.argmin(D.astype(int)@(1-Ts).T+(1-D.astype(int))@Ts.T,axis=1)
            for r in range(S):
                for s in range(S):
                    m=D[np.ix_(tr==r,th==s)]
                    if m.size: T[r,s]=m.mean()>=.5
        err=(T[np.ix_(tr,th)]!=D).sum()
        if best is None or err<best[0]: best=(int(err),T.copy(),th.copy(),tr.copy())
    return best
Ss=[1,2,3,4,6,8,12,16,24,32,48,56]
rng=np.random.default_rng(9)
R=rng.random((N,N))<.5
out={}
for name,D in [("mine",cloth()),("coin",R)]:
    out[name]=[fit(D,S)[0] for S in Ss]; print(name,out[name],flush=True)
json.dump({"S":Ss,**out},open("/tmp/curve.json","w"))
