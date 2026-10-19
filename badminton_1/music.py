import numpy as np, wave, sys
sr=44100; total=float(sys.argv[1]); bpm=96; beat=60/bpm; bar=4*beat
def f(n): return 440*2**((n-69)/12)
prog=[[48,55,60,64,67],[45,52,57,60,64],[41,48,53,57,60],[43,50,55,59,62]]  # C Am F G
N=int(total*sr); out=np.zeros((N,2))
t_all=np.arange(N)/sr
nb=int(total/bar)+1
for b in range(nb):
    ch=prog[b%4]; s0=int(b*bar*sr); L=int(bar*sr*1.05)
    t=np.arange(L)/sr; env=np.minimum(t/0.6,1)*np.exp(-t*0.35)*np.minimum(1,(bar*1.05-t)/0.3).clip(0)
    pad=sum(np.sin(2*np.pi*f(n)*t+0.3*np.sin(2*np.pi*0.25*t))+0.3*np.sin(4*np.pi*f(n)*t) for n in ch[1:4])*0.05*env
    bass=np.sin(2*np.pi*f(ch[0]-12)*t)*0.12*np.exp(-t*1.2)
    seg=pad+bass
    e=min(N,s0+L); out[s0:e,0]+=seg[:e-s0]; out[s0:e,1]+=seg[:e-s0]
    # arpeggio pluck 8ths
    arp=[ch[1]+12,ch[2]+12,ch[3]+12,ch[4]+12,ch[3]+12,ch[2]+12,ch[4]+12,ch[3]+12]
    for i,n in enumerate(arp):
        s=s0+int(i*beat/2*sr); Lp=int(0.9*sr); tp=np.arange(Lp)/sr
        p=(np.sin(2*np.pi*f(n)*tp)+0.25*np.sin(4*np.pi*f(n)*tp))*np.exp(-tp*5)*0.07
        pan=0.5+0.3*np.sin(i)
        e=min(N,s+Lp)
        if s<N: out[s:e,0]+=p[:e-s]*(1-pan)*2*0.6; out[s:e,1]+=p[:e-s]*pan*2*0.6
    # soft hats
    for i in range(8):
        s=s0+int((i+0.5)*beat/2*sr); Lh=int(0.05*sr)
        if s+Lh<N: h=np.random.randn(Lh)*np.exp(-np.arange(Lh)/sr*80)*0.012; out[s:s+Lh]+=h[:,None]
fade=np.minimum(1,np.minimum(t_all/2.0,(total-t_all)/3.0)).clip(0)
out*=fade[:,None]; out/=np.abs(out).max()*1.1
w=wave.open('./out/music.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
