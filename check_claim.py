from itertools import permutations, product
def reduce_word(w):
    st=[]
    for (i,e) in w:
        if st and st[-1][0]==i and st[-1][1]==-e: st.pop()
        else: st.append((i,e))
    return st
def compose(outer, inner, n):
    out=[]
    for word in inner:
        nw=[]
        for (j,e) in word:
            w2=outer[j]
            if e>0:
                for (k,f) in w2: nw.append((k,f))
            else:
                for (k,f) in reversed(w2): nw.append((k,-f))
        out.append(reduce_word(nw))
    return out
def sigma(k,n):
    im=[[(i,1)] for i in range(n)]
    im[k]=reduce_word([(k,1),(k+1,1),(k,-1)]); im[k+1]=[(k,1)]
    return im
def sigma_inv(k,n):
    im=[[(i,1)] for i in range(n)]
    im[k]=[(k+1,1)]; im[k+1]=reduce_word([(k+1,-1),(k,1),(k+1,1)])
    return im
def braid_aut(word,n):
    im=[[(i,1)] for i in range(n)]
    for g in word:
        im = compose(sigma(g-1,n) if g>0 else sigma_inv(-g-1,n), im, n)
    return im
def count(word,n,E,mul,inv):
    im=braid_aut(word,n)
    def ev(w,g):
        r=None
        for (i,e) in w:
            el=g[i] if e==1 else inv(g[i])
            r=el if r is None else mul(r,el)
        return r
    tot=0
    for g in product(E,repeat=n):
        ok=True
        for i in range(n):
            if ev(im[i],g)!=g[i]: ok=False;break
        if ok: tot+=1
    return tot
def alt4():
    def parity(p):
        s=0;vis=[False]*4
        for i in range(4):
            if not vis[i]:
                j=i;c=0
                while not vis[j]: vis[j]=True;j=p[j];c+=1
                s+=c-1
        return s%2
    E=[p for p in permutations(range(4)) if parity(p)==0]
    def mul(p,q): return tuple(p[q[i]] for i in range(4))
    def inv(p):
        r=[0]*4
        for i,x in enumerate(p): r[x]=i
        return tuple(r)
    return E,mul,inv
E,mul,inv=alt4()
fig8=[1,-2,1,-2]
true_inv=[-1,2,-1,2]   # reverse+negate of fig8 -> sigma2 sigma1^-1 sigma2 sigma1^-1? let's see: [1,-2,1,-2] reversed = [-2,1,-2,1], negate = [2,-1,2,-1]
blind=[-1,2,-1,2]       # negate only: [1,-2,1,-2] -> [-1,2,-1,2]
# wait true_inv should be reverse+negate. reversed(fig8)=[-2,1,-2,1], negate=[2,-1,2,-1]
true_inv2=[2,-1,2,-1]
print("fig8 closure A4:", count(fig8,3,E,mul,inv))
print("true_inv (rev+neg) [2,-1,2,-1] A4:", count(true_inv2,3,E,mul,inv))
print("blind (neg only) [-1,2,-1,2] A4:", count(blind,3,E,mul,inv))
print("if blind=|A4|=12 -> unknot signature")
