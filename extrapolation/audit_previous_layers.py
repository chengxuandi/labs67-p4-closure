"""Pin which apparent easy closures were already known; no credit as new layers."""
from pathlib import Path
import json,sys,math
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent));import verify_cm_coverage as a
from verify_new_lemmas import independent_types,need
T,psi=a.real_polynomials();norm=a.norm_real(a.plus([17],T[1]),psi);p=47569
need(all(p%d for d in range(2,math.isqrt(p)+1)) and p%67==66,'P1 prime')
need(norm%p==0 and (norm//p)%p!=0,'P1 valuation')
need(independent_types(1)=={(1,0,0,0,0,0)} and not independent_types(2),'P1/2 coverage')
words={0:''.join('-' if i in {j*j%67 for j in range(1,67)} else '+' for i in range(67)),
       18:'+++++++++-+-+-++--+++-++----+-+-+++----+-+-++-++-++--+-++-----+++--',
       20:'+++++++++-+--++---+-+-+-+--+++-+--+--+--+-+++------++-+-+--+--++---'}
controls=[]
for P,word in words.items():
    need(len(word)==67,'word length');s=[1 if c=='+' else -1 for c in word]
    R=[sum(s[i]*s[(i+k)%67] for i in range(67)) for k in range(1,34)]
    z=[(r+1)//4 for r in R];need(all(r%4==3 for r in R),'periodic parity')
    need(sum(v*(2*v-1) for v in z)==P,'wrong true-word penalty')
    controls.append(dict(P=P,word=word,z=z))
out=dict(status='PASS',P1='PREVIOUSLY_CLOSED',P2='PREVIOUSLY_CLOSED',
         P1_norm=norm,P1_prime=p,actual_words=controls,new_layer_closures=0)
(ROOT/'verifier_logs/previous_layers.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: oldP1/2 exclusions, actualP0/18/20 words; none is a new closure')
