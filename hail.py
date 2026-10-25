import numpy as np, sys
from PIL import Image
from matplotlib import cm
W=int(sys.argv[1]); H=int(sys.argv[2]); name=sys.argv[3]
N=W*H
n=np.arange(1,N+1,dtype=np.int64); m=n.copy(); steps=np.zeros(N,int); peak=n.copy()
alive=m!=1
while alive.any():
    ev=(m%2==0)
    m=np.where(alive,np.where(ev,m//2,3*m+1),m)
    steps+=alive; peak=np.maximum(peak,m); alive=m!=1
s=steps.reshape(H,W).astype(float)
from scipy.stats import rankdata
t=(rankdata(s.ravel())/s.size).reshape(s.shape)
img=(cm.magma(t)[:,:,:3]*255).astype(np.uint8)
Image.fromarray(img).resize((W*(1024//W),H*(1024//W)),Image.NEAREST).save(f'assets/{name}.png')
print(s.max(),np.log(peak.max()))
