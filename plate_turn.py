import numpy as np, sys
from PIL import Image
N=96; C=6; m,n=2,5
x=(np.arange(N)+.5)/N; X,Y=np.meshgrid(x,x)
a=np.cos(m*np.pi*X)*np.cos(n*np.pi*Y); b=np.cos(n*np.pi*X)*np.cos(m*np.pi*Y)
i,j=np.meshgrid(np.arange(N),np.arange(N),indexing='ij')
Z=((i+j)%4)<2; S=((i-j)%4)<2
P=N*C; py,px=np.mgrid[0:P,0:P]; ci,cj=py//C,px//C
v=(py%C+.5)/C; u=(px%C+.5)/C
warp=np.array([22,36,78.]); weft=np.array([226,214,184.])
sw=((.55+.45*np.sin(np.pi*u))*(1-.35*(2*np.abs(v-.5))**3))[...,None]
sf=((.55+.45*np.sin(np.pi*v))*(1-.35*(2*np.abs(u-.5))**3))[...,None]
g=np.random.default_rng(1).normal(0,5,(P,P,1))
F=int(sys.argv[1]) if len(sys.argv)>1 else 180
for k in range(F):
    t=np.pi*k/F
    f=np.cos(t)*a+np.sin(t)*b
    w=np.where(f>0,Z,S)[ci,cj][...,None]
    img=np.where(w,warp*sw,weft*sf)+g
    Image.fromarray(np.clip(img,0,255).astype(np.uint8)).save(f'assets/t39/f/{k:03d}.png')
