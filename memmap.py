import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
N=512
def field(p,rng):
    st=np.zeros((N,N),bool); s=1
    while s<=N:
        f=rng.random((N//s,N//s))<p
        st^=np.kron(f,np.ones((s,s),bool)); s*=2
    return st
def acf(p,runs=24):
    rng=np.random.default_rng(11); acc=np.zeros((N,N))
    for _ in range(runs):
        x=2.0*field(p,rng)-1
        F=np.fft.fft2(x); acc+=np.fft.ifft2(F*np.conj(F)).real/N**2
    return np.fft.fftshift(acc/runs)
ps=[0.5,0.2,0.1,0.03]
fig,ax=plt.subplots(1,4,figsize=(16,4.4),facecolor='#14131a')
for a,p in zip(ax,ps):
    c=acf(p); h=60
    v=np.log10(np.clip(c,1e-4,1))
    sub=v[N//2-h:N//2+h+1,N//2-h:N//2+h+1]
    a.imshow(sub,cmap='magma',vmin=-3,vmax=0,interpolation='nearest')
    a.set_title(f'p = {p}',color='#ddd',fontsize=13); a.axis('off')
plt.tight_layout(); plt.savefig('assets/memmap.png',dpi=110,facecolor='#14131a')
