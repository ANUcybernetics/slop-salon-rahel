# three trees grown by the same coin; only the weight on a leaf differs: (tips of its parent limb)**beta
import math, random
from PIL import Image, ImageDraw
def grow(N,beta,seed):
    r=random.Random(seed)
    par=[-1]; kids=[[]]; size=[1]
    leaves=[0]
    while len(leaves)<N:
        ws=[(size[par[l]] if par[l]>=0 else 1)**beta for l in leaves]
        l=r.choices(leaves,ws)[0]
        leaves.remove(l)
        for _ in range(2):
            par.append(l); kids.append([]); size.append(1); kids[l].append(len(par)-1); leaves.append(len(par)-1)
        a=l
        while a>=0: size[a]+=1; a=par[a]   # each fork adds one tip along the whole chain
    return par,kids,size
def tips(kids):
    n=[0]*len(kids)
    def f(i):
        n[i]=1 if not kids[i] else sum(f(k) for k in kids[i]); return n[i]
    import sys; sys.setrecursionlimit(10000); f(0); return n
S=3; PW=700; PH=860
ink=(196,72,52); paper=(238,231,216)
def draw(beta,seed,N=420):
    par,kids,_=grow(N,beta,seed); n=tips(kids)
    img=Image.new("RGB",(PW*S,PH*S),paper); d=ImageDraw.Draw(img)
    segs=[]
    def go(i,x,y,a,depth):
        L=(34-min(depth,40)*0.3)*S
        w=(1.2+1.15*math.sqrt(n[i]))*S*0.55
        ex,ey=x+math.cos(a)*L,y+math.sin(a)*L
        segs.append((x,y,ex,ey,w))
        k=kids[i]
        if not k: return
        k=sorted(k,key=lambda c:-n[c])
        big,small=k[0],k[1]
        share=n[small]/n[i]
        spread=0.28+0.9*share
        up=-math.pi/2
        def pull(t): return t+(up-t)*0.06
        go(big,ex,ey,pull(a-spread*share*(1 if depth%2 else -1)),depth+1)
        go(small,ex,ey,pull(a+spread*(1 if depth%2 else -1)),depth+1)
    go(0,PW*S/2,PH*S*0.97,-math.pi/2,0)
    xs=[p for s in segs for p in (s[0],s[2])]; ys=[p for s in segs for p in (s[1],s[3])]
    sx=(PW*S*0.9)/(max(xs)-min(xs)); sy=(PH*S*0.93)/(max(ys)-min(ys)); sc=min(sx,sy)
    cx=(max(xs)+min(xs))/2; by=max(ys)
    for (x,y,ex,ey,w) in segs:
        P=lambda x,y:(PW*S/2+(x-cx)*sc, PH*S*0.97+(y-by)*sc)
        p,q=P(x,y),P(ex,ey); ww=max(1,w*sc**0.5)
        d.line([p,q],fill=ink,width=int(ww)); d.ellipse([q[0]-ww/2,q[1]-ww/2,q[0]+ww/2,q[1]+ww/2],fill=ink)
    return img.resize((PW,PH),Image.LANCZOS), sorted(n[1:],reverse=True)[:5]
if __name__=="__main__":
    out=Image.new("RGB",(PW*3+40*2,PH),paper)
    for j,b in enumerate([-3.0,0.0,3.0]):
        im,top=draw(b,7); print(b,top); out.paste(im,(j*(PW+40),0))
    out.save("assets/sizetree.png"); out.convert("RGB").save("assets/sizetree.jpg",quality=90)
