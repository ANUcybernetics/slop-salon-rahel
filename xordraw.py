import numpy as np
from PIL import Image, ImageDraw
exec(open('stern3.py').read().split('N=256')[0])
N=512;s=stern(2*N+5)
i,j=np.meshgrid(np.arange(1,N+1),np.arange(1,N+1),indexing='ij')
v=np.minimum(s[i^j],5)
pal=np.array([[10,12,24],[245,236,214],[226,130,50],[176,44,40],[40,120,125],[24,36,84]],np.uint8)
img=(pal[v]*0.35+10).astype(np.uint8)
k=3;S=2
im=Image.fromarray(img).resize((N*S,N*S),Image.NEAREST);d=ImageDraw.Draw(im)
for dd in (1<<k,-(1<<k)):
    run=[]
    def flush():
        if run:
            col=(240,200,60) if len(run)==1<<k else (230,50,50)
            for a,b in run: d.rectangle([(b-1)*S,(a-1)*S,(b-1)*S+S-1,(a-1)*S+S-1],fill=col)
        run.clear()
    for a in range(1,N+1):
        b=a+dd
        if 1<=b<=N and (a^b)==(1<<k): run.append((a,b))
        else: flush()
    flush()
im.convert('RGB').save('assets/t51_strokes.jpg',quality=90)
im.crop((0,0,256,256)).resize((1024,1024),Image.NEAREST).convert('RGB').save('assets/t51_corner.jpg',quality=90)
