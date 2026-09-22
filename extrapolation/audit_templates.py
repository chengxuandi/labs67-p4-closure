"""Parse every frozen chain and classify topology; no solver is run."""
from pathlib import Path
from fractions import Fraction
import json,sys,csv
sys.set_int_max_str_digits(100000)
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent
def ints(obj):
    if type(obj) is int:yield obj
    elif isinstance(obj,list):
        for value in obj:yield from ints(value)
def main():
    rows=json.loads((BASE/'certificates/cm_batch_results.json').read_text());groups={};stats=[]
    checked=json.loads((ROOT/'verifier_logs/p4_replay.json').read_text())
    ends={r['case_id']:r for r in checked['cases']}
    for row in rows:
        path=BASE/row['certificate'].replace('\\','/');doc=json.loads(path.read_text())
        topology=tuple((s[0],len(s[3]),len(s[4]),tuple(len(q) for q in s[5])) for s in doc['steps'])
        key=(doc['prime'],topology)
        group=groups.setdefault(key,[]);group.append(row['case_id'])
        e=ends[row['case_id']]
        stats.append(dict(case_id=row['case_id'],prime=doc['prime'],steps=len(doc['steps']),
                          coefficient_max_bits=max(abs(x).bit_length() for s in doc['steps'] for x in ints(s)),
                          bytes=path.stat().st_size,trace=e['trace'],residue=e['residue'],
                          contradiction_margin=67*e['residue']**2-2*e['trace']))
    result=dict(templates=[dict(prime=k[0],topology=k[1],cases=v) for k,v in groups.items()],cases=stats)
    (ROOT/'certificates/p4_templates.json').write_text(json.dumps(result,indent=2)+'\n')
    lines=['# 冻结P4的模板抽取','',
           '逐项完整解析27份证书，按prime+所有step拓扑分组。相同拓扑不是相同数值证书。',
           '共同内核：二进制p-1链；两生成元模的平方/乘法；显式成员等式；最终迹—残数矛盾。','',
           '|模板|p|深度|代表数|最大整数位长范围|','|---|---:|---:|---:|---|']
    for j,((p,top),cases) in enumerate(groups.items()):
        bits=[r['coefficient_max_bits'] for r in stats if r['case_id'] in cases]
        lines.append(f'|{j+1}|{p}|{len(top)}|{len(cases)}|{min(bits)}..{max(bits)}|')
    lines+=['','CRT：每个范数素因子上选一对共轭根的一侧；终止均为某一坐标残数违界。',
            '可复用的是代数证书格式、指数拓扑和checker，而不是27组w/eta的整数值。',
            '不存在已经证明的“任意输入匹配拓扑就必有NO证书”定理。']
    (ROOT/'P4_CERTIFICATE_TEMPLATES.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    # Read old factor proposals for ranking ONLY. No primality/NO accepted here.
    old=Path('D:/ai4sc/LABS_N67/low_periodic_classification')
    with (old/'lowp_orbit_norm_certificate.csv').open() as f:allrows=list(csv.DictReader(f))
    ranks=[]
    for P in (3,5):
        supports={r['support'] for r in allrows if int(r['penalty'])==P and r['status']=='survivor'}
        with (old/f'p{P}_survivor_full_factorization.csv').open() as f:fs=list(csv.DictReader(f))
        chosen=[r for r in fs if r['support'] in supports]
        details=[]
        for r in chosen:
            factors=[tuple(map(int,item.split('^'))) for item in r['prime_factorization'].split(';')]
            simple=all(e==1 and p%67==1 for p,e in factors)
            details.append(dict(support=r['support'],norm=int(r['abs_norm']),factors=factors,
                                simple_split_proposal=simple,ideal_count_proposal=2**len(factors) if simple else None))
        record=dict(P=P,all_orbits=sum(int(r['penalty'])==P for r in allrows),
                    existing_local_exclusions=sum(int(r['penalty'])==P and r['status']=='obstructed' for r in allrows),
                    survivor_supports=len(supports),factor_rows=len(chosen),
                    simple_supports=sum(r['simple_split_proposal'] for r in details),
                    ideal_proposal_total=sum(r['ideal_count_proposal'] or 0 for r in details),details=details,
                    trust='UNVERIFIED FACTOR PROPOSALS; ranking only, not accepted exclusions')
        ranks.append(record)
        print({k:v for k,v in record.items() if k!='details'})
    (ROOT/'inputs/legacy_factor_proposals.json').write_text(json.dumps(ranks,indent=2)+'\n')
    print('templates',len(groups),'bit range',min(r['coefficient_max_bits'] for r in stats),max(r['coefficient_max_bits'] for r in stats))
if __name__=='__main__':main()
