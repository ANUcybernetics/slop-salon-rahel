import numpy as np, subprocess, os
from PIL import Image
from scipy.ndimage import gaussian_filter1d
X=Y=1024
col=np.load('assets/colmean.npy')
x=np.linspace(0,255,X); prof=gaussian_filter1d(np.interp(x,np.arange(256),col),6)
grad=np.gradient(prof); grad/=np.abs(grad).max()
yy=np.linspace(0,1,Y)[:,None]; xx=np.arange(X)[None,:]
lit=0.55+0.45*grad[None,:]*(0.6+0.4*yy)
v=np.clip(lit*(0.45+0.6*np.exp(-(((yy-0.3)/0.9)**2))),0,1)
cur=np.stack([v**1.1*0.85+0.1,v**1.6*0.18,v**1.4*0.22+0.04],-1)
# stage: plume lit by a spot, dark floor
p=Image.open('assets/stage_plume.png').convert('RGB')
sw=860; p=p.resize((sw,int(p.height*sw/p.width)),Image.LANCZOS)
back=np.zeros((Y,X,3)); back[:]=np.array([10,8,14])/255
ph=p.height; y0=Y-90-ph; x0=(X-sw)//2
back[y0:y0+ph,x0:x0+sw]+=np.clip(np.asarray(p)/255-np.array([14,12,20])/255,0,1)*1.3
glow=np.exp(-(((xx-512)/380)**2+((yy-0.55)/0.55)**2))[...,None]
back=np.clip(back*(0.35+0.9*glow),0,1)
fl=(yy>(Y-90)/Y)[...,None]*np.ones((1,X,1))
floor=np.stack([0.22*glow[...,0]+0.03]*3,-1)*np.array([1,0.8,0.7])
back=np.where(fl>0,floor*(1-(yy-(Y-90)/Y)[...,None]*3),back)
os.makedirs('assets/stg',exist_ok=True)
T=96
for f in range(T):
    t=min(1,max(0,(f-8)/(T-24))); o=0.93*(3*t*t-2*t**3)
    img=back.copy()
    h=X//2; w=int(h*(1-o))
    if w>0:
        src=np.clip((np.arange(w)/(1-o)).astype(int),0,h-1)
        sh=(1-0.35*o*(np.arange(w)/w))[None,:,None]
        img[:,:w]=cur[:,src]*sh
        img[:,X-w:]=cur[:,::-1][:,src][:,::-1]*sh[:,::-1]
    # valance across the top
    img[:70]=cur[:70,:]*0.55
    Image.fromarray((np.clip(img,0,1)*255).astype(np.uint8)).save(f'assets/stg/{f:03d}.png')
