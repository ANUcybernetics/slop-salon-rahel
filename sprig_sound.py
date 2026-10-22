# the growth, heard: each limb is a voice that glides with its tip's height while it grows, panned by tip x
import numpy as np, wave, math
src=open("sprig_grow.py").read().split("T=max(")[0]
exec(src)
T=max(s[3] for s in segs); DUR=11.0; hold=1.5; GROW=DUR-hold
SR=44100; n=int(DUR*SR); L=np.zeros(n); R=np.zeros(n)
pent=[0,2,4,7,9]
def hz(h):  # h in 0..1 (0 low) -> pentatonic-quantised-ish, continuous glide
    return 110*2**(h*3.2)
for pts,ws,t0,t1 in segs:
    a=t0/T*GROW; b=t1/T*GROW; tail=1.2
    i0=int(a*SR); i1=min(n,int((b+tail)*SR))
    t=np.arange(i1-i0)/SR
    # tip height along growth
    ys=np.array([1-(p[1]/H) for p in pts]); xs=np.array([p[0]/W for p in pts])
    u=np.clip(t/(b-a),0,1); k=u*(len(pts)-1)
    h=np.interp(k,np.arange(len(pts)),ys); x=float(np.mean(xs))
    # quantise starting pitch to pentatonic, glide by relative height
    oct_=h[0]*3.2; st=round(oct_*12); deg=st//12*12+min(pent,key=lambda p:abs(p-st%12))
    f=110*2**(deg/12)*2**((h-h[0])*3.2)
    ph=2*np.pi*np.cumsum(f)/SR
    wv=np.sin(ph)+0.3*np.sin(2*ph)
    amp=np.where(t<b-a,np.minimum(1,t/0.05),np.exp(-(t-(b-a))*3.5))
    w=float(ws[0])/(13*S)
    sig=wv*amp*(0.04+0.08*w)
    pan=min(1,max(0,x)); 
    L[i0:i1]+=sig*math.cos(pan*math.pi/2); R[i0:i1]+=sig*math.sin(pan*math.pi/2)
m=max(abs(L).max(),abs(R).max()); L/=m*1.1; R/=m*1.1
fade=np.minimum(1,np.arange(n)[::-1]/(SR*1.0)); L*=fade; R*=fade
st=(np.stack([L,R],1)*32767).astype('<i2')
w_=wave.open("assets/sprig_grow.wav","wb"); w_.setnchannels(2); w_.setsampwidth(2); w_.setframerate(SR); w_.writeframes(st.tobytes()); w_.close()
print(len(segs))
