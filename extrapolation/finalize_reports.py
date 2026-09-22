"""Summarize only actual checked results; seal new files and verify frozen ones."""
from pathlib import Path
import hashlib,json,sys
from fractions import Fraction
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent
sys.set_int_max_str_digits(100000)

def main():
    final=json.loads((ROOT/'verifier_logs/p03_closure.json').read_text())
    if final['status']!='P3_CLOSED':raise RuntimeError('No layer closure to report')
    scale=json.loads((ROOT/'verifier_logs/p05_scaling.json').read_text())
    batch=json.loads((ROOT/'verifier_logs/p03_batch.json').read_text())
    templates=json.loads((ROOT/'certificates/p4_templates.json').read_text())
    frozen=json.loads((ROOT/'hashes/FROZEN_P4.json').read_text())
    for relative,digest in frozen.items():
        if hashlib.sha256((BASE/relative).read_bytes()).hexdigest()!=digest:raise RuntimeError('Frozen P4 changed: '+relative)
    cases=final['results'];counts={}
    bitmax=[]
    def integers(v):
        if type(v) is int:yield v
        elif isinstance(v,list):
            for x in v:yield from integers(x)
    for r in cases:
        p=r['result']['prime'];counts[p]=counts.get(p,0)+1
    for rec in batch['records']:
        doc=json.loads((ROOT/rec['certificate']).read_text())
        bitmax.append(max(abs(x).bit_length() for x in integers(doc['steps'])))
    stats=dict(status='ONE_MORE_LAYER_SUCCESS',new_closed_layers=[3],new_dual_closed_layers=[3],
               frozen_P4_unchanged=True,P3_certificate_bytes=scale['P3_certificate_bytes'],
               P3_representatives=192,P3_prime_templates=counts,
               P3_coefficient_bits_range=[min(bitmax),max(bitmax)],
               P3_trace_range=[min(r['result']['trace'] for r in cases),max(r['result']['trace'] for r in cases)],
               new_coset_only_exclusions=sum(not r['result']['old_scalar_would_close'] for r in cases),
               P3_discovery_batch_seconds=batch['elapsed'],P3_replay_seconds=final['replay_seconds'],
               stop_reason='SCALING_GUARD_AT_NEXT_LAYER',global_optimality_proved=False)
    (ROOT/'verifier_logs/final_metrics.json').write_text(json.dumps(stats,indent=2)+'\n')
    (ROOT/'P03_REPORT.md').write_text(f'''# P3_CLOSED / Pprime3_CLOSED

完整空间中的定理：对每个S属于{{±1}}^67，P(S)!=3且Pprime(S)!=3。
不假设skew，不将周期decimation当作非周期能量对称。

覆盖：5456个位置支撑 -> 166个Galois轨道 -> 100个精确局部排除 + 66个待判定谱。
剩余谱的完整平方自由分解和逐素数二次gcd，经1055个递归素性节点检查，
给出384个极化理想、192对共轭。全部192份有限NO_CHAIN重放通过。

正确性链：METHOD_DECOMPOSITION.md的范数等价，COVERAGE_AND_DUALITY.md的
完整轨道/理想覆盖，冻结CM_CHAIN_AUDIT.md的参数化链归纳，
GENERAL_COORDINATE_BOUND.md的终迹反证。所有新checker均与GP生成器独立。

证书字节：{stats['P3_certificate_bytes']}；模板计数：{counts}；
最大整数位长范围：{min(bitmax)}..{max(bitmax)}；终迹范围：{stats['P3_trace_range']}。
发现批次约{batch['elapsed']:.2f}秒；独立整层重放约{final['replay_seconds']:.2f}秒。
仅由新coset界、而旧单坐标界不能排除的个案：{stats['new_coset_only_exclusions']}。
因此不把更强引理自动宣称为本批次的性能突破。

每份证书发现上限120秒，无扩限、无普通格球枚举、无裸NO接受。
对外暴露的是整数恒等式和完整覆盖，不是GS实现的结论。

运行：`python -B extrapolation/verify_p03_closure.py`。
实际终止行：`P3_CLOSED: all166 support orbits excluded; NOT global LABS optimality.`
组合变异、覆盖变异、已知生成元及伪NO控制结果均在verifier_logs。
冻结P4的{len(frozen)}个文件哈希全部保持不变。
''',encoding='utf-8')
    (ROOT/'P05_REPORT.md').write_text(f'''# P5_OPEN：下一层审计后停止扩批

P5在去掉已闭P3之后仍是最容易的新非空层；其完整位置支撑有496个Galois轨道。
旧算术提案中有332个局部排除、164个剩余谱。本轮没有重新认证全部P5素性/局部证书，
所以这些数字只作为有来源的下一层预测，不冒充新的排除结果。

162个简单谱的因子提案对应862个理想、至少431个共轭代表，
尚未计入两个含269²的例外。单是这部分已为P4的431/27倍。
该预测没有被当作P5不可实现证明，也不是已认证的完整理想计数。

两个例外在269上的gcd/根数据已精确计算，见verifier_logs/p05_scaling.json。
必须先按真实素理想赋值重建覆盖；不能套用P4的“每个有理素数选一个线性根”。
进一步独立局部checker证明：这两个269²各对应两对共轭线性素理想，四者赋值都为1，
不是同一对赋值2。269处各有4种理想选择，其模269生成多项式为二次式。
这是已有CM框架内可处理的输入变化，不是“不适用”或需要新理论的证明。

用实际P3平均证书大小估算，这部分P5链至少约{scale['predicted_P5_certificate_bytes_lower']}字节。
这只是规划估计，不是数学下界。P3的{scale['P3_transitions']}个完整转移中，
字面相同可复用转移为{scale['literal_DAG_reuse']}；两种拓扑没有自动变成少数数值证书。

触发用户指定的十倍级规模止损检查，且没有已验证的共享数值DAG或批量排除机制。
因此不运行P5的数百条新链；P5_OPEN。更后层最小候选轨道数为P8的7440，
没有更容易的层可绕过这一瓶颈。此判断针对当前逐理想证书部署，不证明CM方法原则上失败。

`python -B extrapolation/verify_p05_closure.py`明确返回P5_OPEN，退出码2；
这是状态入口，不是伪造的P5闭合checker。
''',encoding='utf-8')
    report=f'''# EXTRAPOLATION：ONE_MORE_LAYER_SUCCESS

本轮新增严格闭合P=3及Pprime=3。P=4冻结结果未修改。全局E>=241仍未证明。
到P5规模审计后停止，不自动扩批、不增加时限、不启动第三条路线。

## 十二项结论

1. 通用部分：完整alpha_z范数/二元词等价、CM理想接口、共轭配对、有限域指数恢复、
   精确模块包含递推和迹—残数界；本轮新checker将P4固定输入解除为带严格绑定的signature参数。
2. P4特性：两点有符号支撑、32轨道、20项旧排除、12个平方自由完全分裂谱、54理想和具体终点数据。
3. 下一步选择P3，因为旧P1/2已闭、P0已有正控制；P3的166轨道是剩余非空层最少。
4. 实际执行：重放P4，复核旧P1/2及真实P0/18/20，完整求解P3；P5仅作下一层结构/规模审计，没有GS批次。
5. 新闭合的完整层：P3、Pprime3。P1/2不计新成果，P5未闭；不是MULTI_LAYER_SUCCESS。
6. P3覆盖完整：166支撑轨道，100局部排除，384理想，192共轭代表。
   P<=25的大层只给完整候选语法与精确轨道计数；没有完成所有真正可实现signature的枚举。
7. independent replay：P4_CLOSED与P3_CLOSED均实际通过；正控制、伪NO、覆盖与输入绑定变异通过。
8. 复杂度：P3链仍为8/10步，证书{stats['P3_certificate_bytes']}字节，整数位长{min(bitmax)}..{max(bitmax)}。
   相对P4主要增长来自case数192/27；没有发现链深随P3爆炸。
9. 统一模板：确有两种prime/exponent拓扑，但不等于两份可替代全部输入的数值反证。
10. 参数化定理：完整范数解自动恢复二元词；新增精确coset最小迹M_67(r,p)只需至多67个切口。
    该界严格强于单坐标界，但本批次新增的独占排除数是{stats['new_coset_only_exclusions']}。
    另有明确缩放反机制，否定仅由P控制所有合法链终迹的泛化；不否定未来对指定约化算法的界。
11. 停止原因：P5预计至少431个简单共轭代表，已超过P4十倍；还含两个重复素数输入。
    当前没有足以减少这批数值证书的共享机制；其余层的候选轨道数更大。遵守规模止损，不把它称为数学不可能。
12. LABS(67) global optimality是否已证明？**NO**。

## 最强新增结论与剩余障碍

结合此前P1、P2、P4排除，现有严格结论为

    P(S), Pprime(S)不属于{{1,2,3,4}}。

其中本轮新增只有3。P0真实存在。E<=237仍只给P+Pprime<=51；
本轮没有对其余P层建立完整不可满足证书，更没有证明E>=241。

signature表中数万至数百亿的轨道数是必要条件超集规模，不能当作真实可实现空间维数。
P18、20的真实词被作为反例控制，明确禁止泛化为所有低P均无词。

## 文件与重放

先在仓库根目录运行：

```text
python -B verify_p4_closure.py
python -B extrapolation/verify_new_lemmas.py
python -B extrapolation/verify_layer_coverage.py 3
python -B extrapolation/verify_p03_closure.py
python -B extrapolation/audit_layer_coverage_mutations.py
python -B extrapolation/audit_p03_composition.py
```

上述验证只需Python3.12标准库，不调用GP、LLL、SAT或数值优化。
生成器的GP路径仅用于重新发现证书；重放不需要这些外部程序。
所有原始输入、192份证书、coverage、日志及源码保留在extrapolation。
最终哈希清单位于hashes/EXTRAPOLATION_SHA256.json。

决策：本轮ONE_MORE_LAYER_SUCCESS；当前逐理想外推在下一层停止。
值得继续研究的是同一路线中的批量/共享证书机制，不是原样启动更大逐例批次。
'''
    (ROOT/'EXTRAPOLATION_FINAL_REPORT.md').write_text(report,encoding='utf-8')
    (ROOT/'EXTRAPOLATION_LOG.md').write_text('''# 执行记录

1. 读取公开仓库和本地冻结报告、checker、完整链数据及实际GS发现内核。
2. 独立P4重放通过，93个冻结文件哈希未变。
3. 写出方法分解、范数等价、坐标/coset引理及链缩放反机制。
4. 完整重建113边际类型，按位置赋值给出精确C33轨道数；小层完整物化、大层明确仅符号覆盖。
5. 发现P1/2是旧闭合，不计新增；确认真实P0/18/20阻止错误正惩罚普遍排除。
6. 选P3，独立重建166轨道、100局部排除、384理想/192共轭代表及1055素性节点。
7. 先做最简单单素因子和p=1609模板迁移测试，均产生可重放整数NO。
8. 完成固定192项有限清单；任一未证结果本应停止派发。没有发生超时或裸NO接受。
9. 独立组合重放P3_CLOSED；正控制、层覆盖及绑定变异通过。
10. 再排序后P5最容易；只做重复269及数值DAG复用/规模诊断，触发止损，不求P5链。
11. 保存ONE_MORE_LAYER_SUCCESS报告，确认冻结P4未改动，结束本轮。
''',encoding='utf-8')
    with (ROOT/'P_PRIORITY_TABLE.md').open('a',encoding='utf-8') as f:
        f.write('\n## P3闭合后的再排序\n\nP3_CLOSED；NEXT_P=5，但本轮停止于规模审计。P5仍OPEN；随后是P8（7440候选轨道），不能通过换层得到更小清单。\n')
    with (ROOT/'SIGNATURE_TABLE.md').open('a',encoding='utf-8') as f:
        f.write('\n## 最终可实现性状态\n\nP0的完整profile唯一且有见证；P1/2为旧排除，P3为本轮排除，P4为冻结排除，故这些四个非零层的真实signature数为0。P18/20至少有一个真实signature。其余层的真实可实现计数UNKNOWN；不把候选数当作真实数量。\n')
    for name in ('METHOD_DECOMPOSITION.md','GENERAL_COORDINATE_BOUND.md'):
        with (ROOT/name).open('a',encoding='utf-8') as f:f.write('\n本轮验证状态：相应有限反例测试与正控制通过；详见verifier_logs/new_lemma_audit.json和general_chain_controls.json。\n')
    files=[p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='EXTRAPOLATION_SHA256.json']
    def digest(p):
        with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
    hashes={p.relative_to(BASE).as_posix():digest(p) for p in sorted(files)}
    (ROOT/'hashes/EXTRAPOLATION_SHA256.json').write_text(json.dumps(hashes,indent=2)+'\n')
    print(json.dumps(stats));print('SEALED',len(hashes),'new files; frozenP4 unchanged')
if __name__=='__main__':main()
