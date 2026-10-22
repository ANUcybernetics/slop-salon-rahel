# subtree tip counts of the sprig's tree, same rules as sprig.py (no drawing)
import math, json
phase=[0.0]
def drift():
    phase[0]+=2.399963
    return math.sin(phase[0])
S=4
limbs=[]  # (depth, L, tips)
def grow(L,depth,parent):
    if depth==0 or L<10*S: return 0
    drift()  # bend
    node={'depth':depth,'L':L,'kids':[]}
    limbs.append(node)
    k=2 if depth%3 else 3
    for j in range(k):
        drift()
        l=L*(0.71+0.05*drift())
        node['kids'].append(grow(l,depth-1,node))
    if depth>3:
        drift()
        node['kids'].append(grow(L*0.45,depth-3,node))
    return node
H=1350*S
root=grow(H*0.19,8,None)
def tips(n):
    if not n: return 0
    ks=[k for k in n['kids'] if k]
    if not ks: n['tips']=1; return 1
    n['tips']=sum(tips(k) for k in ks); return n['tips']
tips(root)
sz=sorted([l['tips'] for l in limbs],reverse=True)
print(len(limbs),sz[0],sum(1 for s in sz if s==1))
json.dump(sz,open('assets/sprig_sizes.json','w'))
import collections
print(sorted(collections.Counter(sz).items()))
