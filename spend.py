import numpy as np, sys
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from PIL import Image, ImageDraw
N=512
def tiles(ps,seed):
    rng=np.random.default_rng(seed); st=np.zeros((N,N),bool); s=1;k=0
    while s<=N:
        f=rng.random((N//s,N//s))<ps(k)
        st^=np.kron(f,np.ones((s,s),bool)); s*=2;k+=1
    return st
def curves(t):
    up=np.roll(t,1,0); lf=np.roll(t,1,1)
    h=up!=t   # h[i,j]: edge right of vertex (i,j)
    v=lf!=t   # v[i,j]: edge below vertex (i,j)
    idh=np.arange(N*N).reshape(N,N); idv=idh+N*N
    R=h; L=np.roll(h,1,1); D=v; U=np.roll(v,1,0)
    iR=idh; iL=np.roll(idh,1,1); iD=idv; iU=np.roll(idv,1,0)
    a=[];b=[]
    n=R.astype(int)+L+D+U
    two=n==2
    # degree 2: join the two present; degree 4: R-D, L-U
    pairs=[(R,L,iR,iL),(R,D,iR,iD),(R,U,iR,iU),(L,D,iL,iD),(L,U,iL,iU),(D,U,iD,iU)]
    for A,B,ia,ib in pairs:
        m=two&A&B; a.append(ia[m]);b.append(ib[m])
    f=n==4
    for ia,ib in [(iR,iD),(iL,iU)]:
        a.append(ia[f]);b.append(ib[f])
    a=np.concatenate(a);b=np.concatenate(b)
    M=2*N*N
    g=coo_matrix((np.ones(len(a)),(a,b)),shape=(M,M))
    _,lab=connected_components(g,directed=False)
    present=np.concatenate([h.ravel(),v.ravel()])
    lab=np.where(present,lab,-1)
    ids,cnt=np.unique(lab[lab>=0],return_counts=True)
    return lab,ids,cnt
rules={
 'coin':lambda k:.5 if k==0 else 0,
 'stacked .2':lambda k:.2,
 'coarse only':lambda k:0 if k<5 else .2,
 'fine light':lambda k:.2*min(1,(k+1)/9)**2,
}
if __name__=='__main__':
    for name,ps in rules.items():
        t=tiles(ps,3); lab,ids,cnt=curves(t)
        o=np.sort(cnt)[::-1]
        print(name,len(ids),'total',cnt.sum(),'longest',o[:5],'share',o[0]/cnt.sum())
