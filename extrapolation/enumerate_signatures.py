"""Exact symbolic candidate cover, not a declaration of realizability.

Position-specific vectors are materialized only for <=20000 candidates.
All larger sets have a finite histogram grammar and exact Burnside counts.
"""
from pathlib import Path
from math import factorial,isqrt
from itertools import combinations
import json
ROOT=Path(__file__).resolve().parent
VALUES=(1,-1,2,-2,3,-3)
COST=tuple(z*(2*z-1) for z in VALUES)

def types(P,i=0):
    if i==len(VALUES):
        if P==0:yield ()
        return
    for count in range(P//COST[i]+1):
        for tail in types(P-count*COST[i],i+1):yield (count,)+tail

def multinomial(counts):
    a=factorial(sum(counts))
    for c in counts:a//=factorial(c)
    return a

def counts(hist):
    full=(33-sum(hist),)+hist
    raw=multinomial(full)
    # F67*/{+1,-1} is cyclic of order33, acting regularly on33 shifts.
    fixed=[]
    for d,phi in ((1,1),(3,2),(11,10),(33,20)):
        fixed.append(phi*multinomial(tuple(c//d for c in full)) if all(c%d==0 for c in full) else 0)
    assert sum(fixed)%33==0
    return raw,sum(fixed)//33

def canon(support):
    return min(tuple(sorted((z,min(k*a%67,67-k*a%67)) for z,k in support)) for a in range(1,34))

def assignments(hist,index=0,remaining=tuple(range(1,34)),support=()):
    if index==len(VALUES):
        yield tuple(sorted(support));return
    for chosen in combinations(remaining,hist[index]):
        chosen_set=set(chosen)
        yield from assignments(hist,index+1,tuple(k for k in remaining if k not in chosen_set),
                               support+tuple((VALUES[index],k) for k in chosen))

def main():
    table=[]
    for P in range(26):
        raw=list(types(P));legal=[];rows=0;orbits=0
        for h in raw:
            sigma=sum(a*z for a,z in zip(h,VALUES));square=1+8*sigma
            if square<1 or isqrt(square)**2!=square:continue
            n,o=counts(h);rows+=n;orbits+=o
            legal.append(dict(counts=list(h),sigma=sigma,DC_abs=isqrt(square),
                              support=sum(h),raw_vectors=n,orbits=o))
        doc=dict(schema='candidate-signature-cover-v1',P=P,values=list(VALUES),
                 value_costs=list(COST),raw_partition_count=len(raw),histograms=legal,
                 candidate_vector_count=rows,candidate_orbit_count=orbits,
                 realizable_signature_count=None,
                 semantics='NECESSARY-CONDITION COVER, NOT ASSERTED REALIZABLE',
                 grammar='Assign listed multiplicities to distinct shifts1..33; all remaining z=0.',
                 constraints=['sum z(2z-1)=P','1+8sum z is an odd square',
                              'R=4z-1','lambda=d-17+z in [0,d]'],
                 frozen_P4_excluded=P==4)
        explicit=rows<=20000
        if explicit:
            representatives=sorted({canon(s) for h in legal for s in assignments(h['counts'])})
            assert len(representatives)==orbits
            doc['orbit_representatives']=[list(map(list,s)) for s in representatives]
        else:
            doc['orbit_representatives']=None
            doc['nonmaterialization_reason']='STRUCTURAL SIZE GUARD; exact symbolic cover only'
        (ROOT/'signatures'/f'P{P:02}.json').write_text(json.dumps(doc,indent=2)+'\n')
        table.append(dict(P=P,partitions=len(raw),types=len(legal),candidates=rows,orbits=orbits,
                          support=sorted({r['support'] for r in legal}),
                          max_z=max([abs(z) for h in legal for z,c in zip(VALUES,h['counts']) if c]+[0]),
                          explicit=explicit,expected_ideal_cases=None))
        print(P,len(raw),len(legal),rows,orbits,flush=True)
    (ROOT/'signatures/table.json').write_text(json.dumps(table,indent=2)+'\n')
    lines=['# P<=25 signature精确覆盖表','',
           '下表是全部满足预算、整数相关及总和平方恒等式的候选；不是已判定可实现的词。',
           'feasible/REALIZABLE count除有见证或完整排除的层外均为UNKNOWN。',
           'exceptional correlation count等于支撑大小。群商最大因子为33，存在稳定子时不能直接除33。',
           '大层使用完整有限语法和Burnside精确计数，没有逐点物化；此处不宣称完成用户所要求的全部真实可实现signature枚举。','',
           '|P|raw partitions|必要条件类型|候选向量|支撑/异常位数|轨道数|max abs(z)|显式轨道|',
           '|---|---:|---:|---:|---|---:|---:|---|']
    for r in table:lines.append(f"|{r['P']}|{r['partitions']}|{r['types']}|{r['candidates']}|{r['support']}|{r['orbits']}|{r['max_z']}|{r['explicit']}|")
    lines+=['','expected ideal cases: UNKNOWN，必须对所选层完成精确素理想分解后才填写；不从支撑数捏造理想数。',
            'alpha的完全正性及其范数可实现性仍依赖位置。P<=5显式候选均有17-2sum|z|>0。',
            'P/Pprime交替对偶不会把多个P压成一个P；decimation仅用于周期层，不保持非周期能量。']
    (ROOT/'SIGNATURE_TABLE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    priority=[r for r in table if r['P'] not in (0,1,2,4,18,20)]
    priority.sort(key=lambda r:(r['P']==0,r['orbits'],max(r['support'] or [0]),r['max_z']))
    (ROOT/'signatures/priority.json').write_text(json.dumps(priority,indent=2)+'\n')
    lines=['# 透明tractability ranking','',
           '排除旧闭合层及已有真实词的层后，排序键为：(候选Galois轨道数，最大支撑，max|z|)。',
           '这是进入算术审计前的精确结构排序；未分解的ideal cases和未知终迹不作为假数值评分。',
           '旧研究已有P1的47569惰性素数排除及P2整数恒等式排除；二者不计为新增闭合。',
           'BEST_NEXT_P=3（166轨道）；其次P5（496轨道）；执行前先测理想覆盖规模。',
           'P0有正控制，P18和P20已有真实词，不能把这些整层列为可排除目标。','',
           '|次序|P|候选轨道|支撑|初步决定|','|---|---:|---:|---|---|']
    for j,r in enumerate(priority):
        decision='control / not excludable' if r['P']==0 else ('arithmetic-empty' if not r['orbits'] else ('audit' if r['explicit'] else 'symbolic scaling wall'))
        lines.append(f"|{j+1}|{r['P']}|{r['orbits']}|{r['support']}|{decision}|")
    (ROOT/'P_PRIORITY_TABLE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
if __name__=='__main__':main()
