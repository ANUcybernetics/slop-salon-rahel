import numpy as np
from PIL import Image
def stern(n):
    s=np.zeros(n+1,np.int64); s[1]=1
    for i in range(2,n+1): s[i]=s[i//2] if i%2==0 else s[i//2]+s[i//2+1]
    return s
N=256
s=stern(2*N*N+5)
i,j=np.meshgrid(np.arange(1,N+1),np.arange(1,N+1),indexing='ij')
cands={'sum_m3':s[i+j]%3,'prod_m3':s[i*j]%3,'xor_m3':s[i^j]%3,'sij_m3':(s[i]*s[j])%3,'sum_m5':s[i+j]%5,'sumsq_m2':(s[i]+s[j])%2, 'sij_m4':(s[i]*s[j])%4,'cw':s[i*N+j]%4}
tiles=[]
for k,v in cands.items():
    v=(v*255//max(v.max(),1)).astype(np.uint8)
    tiles.append(Image.fromarray(v).resize((256,256),Image.NEAREST))
W=Image.new('L',(256*4,256*2))
for n,t in enumerate(tiles): W.paste(t,((n%4)*256,(n//4)*256))
W.save('assets/s3_probe.png'); print(list(cands))
