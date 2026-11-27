"""Uso: python3 align.py PROYECTO GUION.txt
GUION con capítulos separados por líneas '=== CAP N: ... ==='. Necesita PROYECTO/assets/c0.mp3 ... cN.mp3.
Escribe PROYECTO/timing.json (chapters, cues, total), PROYECTO/assets/voz.mp3 y PROYECTO/assets/musica_larga.mp3.
Revisa los cues impresos: si una frase quedó mal partida, corrige timing.json a mano."""
import json, re, subprocess, math, sys, os
P=sys.argv[1]
parts=[p.strip() for p in re.split(r'=== .*? ===', open(sys.argv[2]).read()) if p.strip()]
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
def segs(f, D):
    out=subprocess.run(['ffmpeg','-i',f,'-af','silencedetect=noise=-38dB:d=0.3','-f','null','-'],capture_output=True,text=True).stderr
    ev=re.findall(r'silence_(start|end): ([0-9.]+)',out)
    S=[];cur=0.0
    for k,v in ev:
        v=float(v)
        if k=='start':
            if v-cur>0.12: S.append((cur,v))
        else: cur=v
    if D-cur>0.12: S.append((cur,D))
    return S
def phrases(txt):
    txt=re.sub(r'\[[a-z ]+\]','',txt)
    txt=' '.join(txt.split())
    ps=re.findall(r'[^.,:;?¿…!]+[.,:;?…!]*',txt)
    out=[]
    for p in ps:
        p=p.strip()
        if not p: continue
        if p in ('.','…') and out: out[-1]+=p; continue
        out.append(p)
    # attach leading ¿
    res=[]
    for p in out:
        if res and res[-1].endswith('¿'): res[-1]=res[-1][:-1].strip(); p='¿'+p
        res.append(p)
    return [p for p in res if p]
GAP_START=0.6; GAP=2.0; TAIL=5.0
t0=GAP_START; chapters=[]; cues=[]
for i,txt in enumerate(parts):
    f=f'{P}/assets/c{i}.mp3'; D=dur(f); S=segs(f,D); ph=phrases(txt)
    L=[len(p) for p in ph]; rate=sum(L)/sum(b-a for a,b in S)
    n,m=len(ph),len(S); INF=1e9
    best=[[INF]*(m+1) for _ in range(n+1)]; bk=[[None]*(m+1) for _ in range(n+1)]
    best[0][0]=0
    for a in range(n+1):
        for b in range(m+1):
            if best[a][b]>=INF: continue
            for da in (1,2,3):
                for db in (1,2,3):
                    if a+da>n or b+db>m: continue
                    if da>1 and db>1: continue
                    ch=sum(L[a:a+da]); d=S[b+db-1][1]-S[b][0]
                    c=abs(math.log((ch/rate+0.15)/(d+0.15)))+0.25*(da-1)+0.35*(db-1)
                    if best[a][b]+c<best[a+da][b+db]: best[a+da][b+db]=best[a][b]+c; bk[a+da][b+db]=(a,b)
    a,b=n,m; groups=[]
    while (a,b)!=(0,0):
        pa,pb=bk[a][b]; groups.append((pa,a,pb,b)); a,b=pa,pb
    groups.reverse()
    for pa,a2,pb,b2 in groups:
        txtg=' '.join(ph[pa:a2]); s0=S[pb][0]; s1=S[b2-1][1]
        # split long groups spanning multiple segments
        if b2-pb>1 and len(txtg)>60:
            w=txtg.split(); tot=sum(S[k][1]-S[k][0] for k in range(pb,b2)); acc=0; wi=0
            for k in range(pb,b2):
                acc+=S[k][1]-S[k][0]; wj=round(len(w)*acc/tot) if k<b2-1 else len(w)
                if wj>wi: cues.append((round(t0+S[k][0],2),round(t0+S[k][1],2),' '.join(w[wi:wj]))); wi=wj
        else:
            cues.append((round(t0+s0,2),round(t0+s1,2),txtg))
    chapters.append(dict(i=i,start=round(t0,3),dur=D))
    t0+=D+(GAP if i<len(parts)-1 else TAIL)
TOTAL=math.ceil(t0*24)/24
json.dump(dict(chapters=chapters,cues=cues,total=TOTAL),open(f'{P}/timing.json','w'),ensure_ascii=False,indent=0)
for c in chapters: print(c)
print('TOTAL',TOTAL,len(cues))
for c in cues: print(c)

# voz completa y música larga
inp=[];flt=[]
for c in chapters:
    inp+=['-i',f"{P}/assets/c{c['i']}.mp3"]; ms=int(round(c['start']*1000))
    flt.append(f"[{c['i']}]aresample=44100,aformat=channel_layouts=mono,adelay={ms}[a{c['i']}]")
n=len(chapters)
f=';'.join(flt)+';'+''.join(f'[a{i}]' for i in range(n))+f"amix=inputs={n}:normalize=0:duration=longest,apad,atrim=0:{TOTAL}[o]"
subprocess.run(['ffmpeg','-y','-v','error']+inp+['-filter_complex',f,'-map','[o]','-c:a','libmp3lame','-b:a','192k',f'{P}/assets/voz.mp3'],check=True)
M=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','assets','musica.mp3')
k=int(TOTAL//60)+2
args=[]; 
for _ in range(k): args+=['-i',M]
chain=''.join(f'[{"0" if j==1 else "x"+str(j-1)}][{j}]acrossfade=d=5[x{j}];' for j in range(1,k))
subprocess.run(['ffmpeg','-y','-v','error']+args+['-filter_complex',chain+f'[x{k-1}]atrim=0:{TOTAL+10}[o]','-map','[o]',f'{P}/assets/musica_larga.mp3'],check=True)
print('voz.mp3 y musica_larga.mp3 listos')
