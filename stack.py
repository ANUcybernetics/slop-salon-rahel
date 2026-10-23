import numpy as np
from PIL import Image
import colorsys
N=512; rng=np.random.default_rng(7); p=0.2
state=np.zeros((N,N),bool); top=np.zeros((N,N),int)
k=0;s=1
while s<=N:
    f=rng.random((N//s,N//s))<p
    F=np.kron(f,np.ones((s,s),bool))
    state^=F
    top=np.where(F,k,top)
    k+=1;s*=2
img=np.zeros((N,N,3))
pal=[colorsys.hsv_to_rgb(0.62-0.07*i,0.55,0.95) for i in range(k)]
for i in range(k):
    m=top==i
    for c in range(3):
        img[...,c][m]=pal[i][c]
img[state]*=0.28
img[...,2][state]+=0.08
Image.fromarray((img.clip(0,1)*255).astype(np.uint8)).resize((1024,1024),Image.NEAREST).save('assets/stack.png')
