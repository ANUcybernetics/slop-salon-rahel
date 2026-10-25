import numpy as np
from PIL import Image
from matplotlib import cm
from scipy.stats import rankdata
K=8; W=2**K; H=512; N=W*H
n=np.arange(1,N+1,dtype=np.int64); m=n.copy(); steps=np.zeros(N,int); alive=m!=1
odd8=np.zeros(N,int)
while alive.any():
    ev=(m%2==0)
    if steps.max()<K: pass
    odd8+=((~ev)&alive&(steps<K))
    m=np.where(alive,np.where(ev,m//2,3*m+1),m); steps+=alive; alive=m!=1
S=steps.reshape(H,W).astype(float)
rev=np.array([int(format(r,f'0{K}b')[::-1],2) for r in range(W)])
# column c of row j holds n=j*W+c+1 -> residue (n mod W); reorder by bit-reversed residue
res=(np.arange(1,N+1)%W).reshape(H,W)
order=np.argsort(rev[res[0]])
S2=S[:,order]
def paint(A):
    t=(rankdata(A.ravel())/A.size).reshape(A.shape); return (cm.magma(t)[:,:,:3]*255).astype(np.uint8)
a=paint(S); b=paint(S2)
g=np.zeros((H,16,3),np.uint8)+14
im=Image.fromarray(np.hstack([a,g,b])); im=im.resize((im.width*2,im.height*2),Image.NEAREST); im.save('assets/hail_e.png'); print(im.size)
