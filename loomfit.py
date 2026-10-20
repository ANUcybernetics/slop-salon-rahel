# rahel's cloth (weave2 rule) fitted to a loom: S shafts, R treadles, then greedy float repair
import numpy as np, sys
from PIL import Image, ImageDraw
N=56; S=int(sys.argv[1]) if len(sys.argv)>1 else 8; R=S; LIM=4; SNAP=(33,27)
rng=np.random.default_rng(3)
def over(i,j): return ((i+j+(j*i)//90)%4)<2
D=np.array([[over(i,j) for i in range(N)] for j in range(N)])      # D[row j, col i], True = warp up
D[SNAP[1]:,SNAP[0]]=False                                           # the snapped warp never lifts again
def runs_excess(M):
    ex=0; mx=0
    for line in list(M)+list(M.T):
        # float = run of same state along a thread
        k=0
        for a in range(1,len(line)+1):
            if a==len(line) or line[a]!=line[k]:
                L=a-k; mx=max(mx,L); ex+=max(0,L-LIM); k=a
    return ex,mx
def draw(T,th,tr): return T[np.ix_(tr,th)]                          # rows=picks via treadle, cols=ends via shaft
best=None
for rs in range(12):
    th=rng.integers(0,S,N); tr=rng.integers(0,R,N); T=rng.random((R,S))<.5
    for it in range(30):
        for i in range(N): th[i]=np.argmin([(T[tr,s]!=D[:,i]).sum() for s in range(S)])
        for j in range(N): tr[j]=np.argmin([(T[r,th]!=D[j]).sum() for r in range(R)])
        for r in range(R):
            for s in range(S):
                m=D[np.ix_(tr==r,th==s)]
                if m.size: T[r,s]=m.mean()>=.5
    err=(draw(T,th,tr)!=D).sum()
    if best is None or err<best[0]: best=(err,T.copy(),th.copy(),tr.copy())
err,T,th,tr=best
F=draw(T,th,tr); e0,m0=runs_excess(F)
print("shafts",S,"mismatch",err,"of",N*N,"float excess",e0,"max",m0, "target excess",runs_excess(D))
T0=T.copy(); flips=0
while runs_excess(draw(T,th,tr))[0]>0:
    bs=None
    for r in range(R):
        for s in range(S):
            T[r,s]^=True; e=runs_excess(draw(T,th,tr))[0]; T[r,s]^=True
            if bs is None or e<bs[0]: bs=(e,r,s)
    if bs[0]>=runs_excess(draw(T,th,tr))[0]: print("stuck at",bs[0]); break
    T[bs[1],bs[2]]^=True; flips+=1
G=draw(T,th,tr); e1,m1=runs_excess(G)
print("flips",flips,"excess",e1,"max",m1,"cells differing from cloth",(G!=D).sum())
np.savez(f"/tmp/w/fit{S}.npz",D=D,F=F,G=G,T0=T0,T=T,th=th,tr=tr)
