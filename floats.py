import numpy as np
from PIL import Image
N=96
x=(np.arange(N)+.5)/N; X,Y=np.meshgrid(x,x)
a=np.cos(2*np.pi*X)*np.cos(5*np.pi*Y); b=np.cos(5*np.pi*X)*np.cos(2*np.pi*Y)
i,j=np.meshgrid(np.arange(N),np.arange(N),indexing='ij')
Z=((i+j)%4)<2; S=((i-j)%4)<2
def draft(t):
    f=np.cos(t)*a+np.sin(t)*b
    return np.where(f>0,Z,S)
def runs(v):  # per-cell length of the run of equal values along axis 1 (no wrap)
    L=np.zeros(v.shape,int)
    for r in range(v.shape[0]):
        row=v[r]; s=0
        for c in range(1,len(row)+1):
            if c==len(row) or row[c]!=row[s]:
                L[r,s:c]=c-s; s=c
    return L
def floats(over):
    wf=runs(over)*over            # warp floats: along a row? no: warp float runs down a column
    return wf
def stats(over):
    colruns=runs(over.T).T        # down columns
    rowruns=runs(over)            # along rows
    warpf=np.where(over,colruns,0)   # warp thread over, length down the column
    weftf=np.where(~over,rowruns,0)  # weft over, length along the row
    return warpf,weftf
if __name__=='__main__':
    ts=np.linspace(0,np.pi,181)
    mx=[];frac=[]
    for t in ts:
        o=draft(t); wf,ef=stats(o)
        mx.append((wf.max(),ef.max()))
        frac.append(((wf>2).mean()+(ef>2).mean()))
    mx=np.array(mx)
    for k in range(0,181,15): print(round(np.degrees(ts[k])),mx[k],round(frac[k],4))
    print('overall max',mx.max(0))
    o=draft(0); wf,ef=stats(o)
    print('hist t=0 warp',np.bincount(wf.ravel()),'weft',np.bincount(ef.ravel()))
