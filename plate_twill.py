import numpy as np
from PIL import Image
N=96; C=10; m,n=2,5
def field(eps):
    x=(np.arange(N)+.5)/N; X,Y=np.meshgrid(x,x)
    a=np.cos(m*np.pi*X)*np.cos(n*np.pi*Y); b=np.cos(n*np.pi*X)*np.cos(m*np.pi*Y)
    return a+eps*b
def cloth(f):
    i,j=np.meshgrid(np.arange(N),np.arange(N),indexing='ij')  # i=row, j=col
    Z=((i+j)%4)<2; S=((i-j)%4)<2
    over=np.where(f>0,Z,S)            # warp over
    # pixel shading
    P=N*C
    py,px=np.mgrid[0:P,0:P]
    ci,cj=py//C,px//C; v=(py%C+.5)/C; u=(px%C+.5)/C
    w=over[ci,cj]
    warp=np.array([22,36,78.]); weft=np.array([226,214,184.])
    sw=(.55+.45*np.sin(np.pi*u))*(1-.35*(2*np.abs(v-.5))**3)
    sf=(.55+.45*np.sin(np.pi*v))*(1-.35*(2*np.abs(u-.5))**3)
    img=np.where(w[...,None],warp*sw[...,None],weft*sf[...,None])
    g=np.random.default_rng(1).normal(0,5,(P,P,1))
    return np.clip(img+g,0,255).astype(np.uint8)
ims=[cloth(field(e)) for e in (0,0.35,-0.35)]
gap=np.full((N*C,24,3),245,np.uint8)
row=np.concatenate([ims[0],gap,ims[1],gap,ims[2]],1)
Image.fromarray(row).save('assets/t38/plate_twill.png')
for k,e in enumerate((0,.35,-.35)): Image.fromarray(ims[k]).save(f'assets/t38/p{k}.png')
