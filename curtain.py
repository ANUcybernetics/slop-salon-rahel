import numpy as np, sys
from PIL import Image
from scipy.ndimage import gaussian_filter1d
W=256; H=int(sys.argv[1]) if len(sys.argv)>1 else 2048
N=W*H
n=np.arange(1,N+1,dtype=np.int64); m=n.copy(); steps=np.zeros(N,int)
alive=m!=1
while alive.any():
    m=np.where(alive,np.where(m%2==0,m//2,3*m+1),m); steps+=alive; alive=m!=1
s=steps.reshape(H,W).astype(float)
col=s.mean(0); col=(col-col.mean())/col.std()
np.save('assets/colmean.npy',col)
# fold surface: depth from column mean, interpolated to 1024 px, softened to cloth
X=1024; Y=1024
x=np.linspace(0,W-1,X)
prof=np.interp(x,np.arange(W),col)
prof=gaussian_filter1d(prof,6)
grad=np.gradient(prof)
grad/=np.abs(grad).max()
yy=np.linspace(0,1,Y)[:,None]
# folds gather toward the top, hang straight below; hem scallops follow the profile
lit=0.55+0.45*grad[None,:]*(0.6+0.4*yy)
spot=np.exp(-(((np.arange(X)[None,:]-X*0.5)/(X*0.45))**2+((yy-0.35)/0.7)**2))
v=np.clip(lit*(0.35+0.75*spot),0,1)
hem=(0.90+0.04*prof[None,:]/np.abs(prof).max())
v=np.where(yy>hem,0.06,v)
r=v**1.1*0.85+0.1; g=v**1.6*0.18; b=v**1.4*0.22+0.04
img=np.stack([r,g,b],-1)
img=(np.clip(img,0,1)*255).astype(np.uint8)
Image.fromarray(img).save('assets/curtain.png')
