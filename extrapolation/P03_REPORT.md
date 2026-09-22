# P3_CLOSED / Pprime3_CLOSED

完整空间中的定理：对每个S属于{±1}^67，P(S)!=3且Pprime(S)!=3。
不假设skew，不将周期decimation当作非周期能量对称。

覆盖：5456个位置支撑 -> 166个Galois轨道 -> 100个精确局部排除 + 66个待判定谱。
剩余谱的完整平方自由分解和逐素数二次gcd，经1055个递归素性节点检查，
给出384个极化理想、192对共轭。全部192份有限NO_CHAIN重放通过。

正确性链：METHOD_DECOMPOSITION.md的范数等价，COVERAGE_AND_DUALITY.md的
完整轨道/理想覆盖，冻结CM_CHAIN_AUDIT.md的参数化链归纳，
GENERAL_COORDINATE_BOUND.md的终迹反证。所有新checker均与GP生成器独立。

证书字节：402544197；模板计数：{269: 178, 1609: 14}；
最大整数位长范围：9522..34021；终迹范围：[430, 1378]。
发现批次约704.52秒；独立整层重放约83.92秒。
仅由新coset界、而旧单坐标界不能排除的个案：0。
因此不把更强引理自动宣称为本批次的性能突破。

每份证书发现上限120秒，无扩限、无普通格球枚举、无裸NO接受。
对外暴露的是整数恒等式和完整覆盖，不是GS实现的结论。

运行：`python -B extrapolation/verify_p03_closure.py`。
实际终止行：`P3_CLOSED: all166 support orbits excluded; NOT global LABS optimality.`
组合变异、覆盖变异、已知生成元及伪NO控制结果均在verifier_logs。
冻结P4的93个文件哈希全部保持不变。
