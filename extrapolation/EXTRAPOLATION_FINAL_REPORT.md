# EXTRAPOLATION：ONE_MORE_LAYER_SUCCESS

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
8. 复杂度：P3链仍为8/10步，证书402544197字节，整数位长9522..34021。
   相对P4主要增长来自case数192/27；没有发现链深随P3爆炸。
9. 统一模板：确有两种prime/exponent拓扑，但不等于两份可替代全部输入的数值反证。
10. 参数化定理：完整范数解自动恢复二元词；新增精确coset最小迹M_67(r,p)只需至多67个切口。
    该界严格强于单坐标界，但本批次新增的独占排除数是0。
    另有明确缩放反机制，否定仅由P控制所有合法链终迹的泛化；不否定未来对指定约化算法的界。
11. 停止原因：P5预计至少431个简单共轭代表，已超过P4十倍；还含两个重复素数输入。
    当前没有足以减少这批数值证书的共享机制；其余层的候选轨道数更大。遵守规模止损，不把它称为数学不可能。
12. LABS(67) global optimality是否已证明？**NO**。

## 最强新增结论与剩余障碍

结合此前P1、P2、P4排除，现有严格结论为

    P(S), Pprime(S)不属于{1,2,3,4}。

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
所有公开重放所需输入、coverage及源码保留在extrapolation；192份大型链证书由
v1.1.0 GitHub Release asset发布。含本机命令路径的原始discovery日志不是证明依赖，
不进入公开仓库。最终哈希清单位于hashes/EXTRAPOLATION_SHA256.json。

决策：本轮ONE_MORE_LAYER_SUCCESS；当前逐理想外推在下一层停止。
值得继续研究的是同一路线中的批量/共享证书机制，不是原样启动更大逐例批次。
