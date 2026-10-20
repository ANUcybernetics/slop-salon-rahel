# one row of looms: target cloth, then the best fit at 4/8/16/32 shafts; orange = threads the loom got wrong
import numpy as np
from PIL import Image, ImageDraw
N=56; c=6; pad=24
sizes=[4,8,16,32]
panels=[("the cloth: 56 ends, 56 picks",None)]+[(f"{s} shafts",s) for s in sizes]
W=pad+len(panels)*(N*c+pad); H=pad*2+N*c+40
im=Image.new("RGB",(W,H),(20,18,24)); d=ImageDraw.Draw(im)
D=np.load("/tmp/w/fit8.npz")["D"]
warp=np.array((214,100,64)); weft=np.array((70,104,124)); bad=np.array((255,170,30))
for k,(lab,s) in enumerate(panels):
    x0=pad+k*(N*c+pad); y0=pad
    F=D if s is None else np.load(f"/tmp/w/fit{s}.npz")["F"]
    a=np.zeros((N,N,3),np.uint8)
    a[F]=warp; a[~F]=weft
    if s is not None: a[F!=D]=bad
    im.paste(Image.fromarray(a).resize((N*c,N*c),Image.NEAREST),(x0,y0))
    n=0 if s is None else int((F!=D).sum())
    d.text((x0,y0+N*c+8),lab,fill=(220,215,205))
    if s: d.text((x0,y0+N*c+22),f"{n} cells wrong",fill=(255,170,30))
im.save("loomfit.png")
