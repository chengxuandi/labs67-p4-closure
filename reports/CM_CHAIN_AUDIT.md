# CM 有限反证链独立审计（2026-09-19）

## 结论与实际复核

本链给出严格的必要条件矛盾，而不是“GS 没找到生成元”。对当前固定 b=13 输入，独立检查器实际返回：

```
PASS_NO; prime=269; exponent=268; steps=8;
trace=660; coefficient_index=0; centered_residue=-70.
```

由于 `67*70²=328300 > 2*660=1320`，不存在生成该输入理想且完整相对范数为 alpha 的 beta。七个现有链变异（alpha、involution、membership、norm、next-generator、missing-step、prime）均被拒绝。本审计逐行检查了 `verify_cm_result.py` 的 `verify_chain` 分支，并亲自重跑了上述结果及变异测试。

另用独立的普通多项式卷积及 Phi_67 长除法（不同于 checker 的循环卷积实现）构造8条已知导子67生成元的透明正控制链。全部被接受为 CONTROL_CHAIN；强行标为 NO_CHAIN 时全部被拒绝。脚本和结果为 `cm_chain_adversarial_tests.py`、`cm_chain_adversarial_results.json`。这些控制审计链引理与检查器，不冒称新的 GS 算法运行。

单个输入的 NO 不自动证明54个理想覆盖或全局 LABS 最优性；输入覆盖是另外的算术接口。

## 1. 证书所需内容

设 O=Z[zeta_67]，alpha 为指定完整相对范数，I 为指定整数理想。假设存在 beta 满足 `I=beta O` 与 `beta*bar(beta)=alpha`。以下从该假设推出矛盾。

证书给定一组初始整数生成元，生成 L_0，且逐一证明它们属于 I；不必证明 L_0=I。
取 `v_0=beta`、`eta_0=alpha`、`F_0=alpha`、`k_0=1`，所以

```
L_0 subset v_0 O,
eta_0 = v_0 bar(v_0),
F_0 = beta^k_0 bar(v_0).
```

每一步的位 c 属于 {0,1}。若初始生成元只生成 I 的子理想 L_0，则证书中实际使用的乘积模块是 `L_0^c L_prev²`，它包含于 `I^c L_prev²`，这已经足够。显式整数多项式系数为 w 及每个 h 提供此乘积模块的成员等式。

证书另给整数 `eta_new` 与整数生成元 g，并检查等式

```
eta_new * (alpha^c eta_prev²) = w bar(w),
(alpha^c eta_prev²) * g = bar(w) h.
```

这两式采用乘法交叉验证，不信任浮点除法、HNF、LLL 或上游的理想相等性声明。

## 2. 包含关系的正确方向

假设上一步 `L_prev subset v_prev O`，并令

```
q = beta^c v_prev²,
delta = w/q,
xi = h/q.
```

成员证书及 `I=beta O` 推出 delta、xi 都是 O 中的整数。令 `v_new=bar(delta)`。
由于 `q bar(q)=alpha^c eta_prev²`，得到

```
eta_new = delta bar(delta) = v_new bar(v_new),
g = bar(delta) xi = v_new xi.
```

于是新生成元生成的 L_new 确实包含于 `v_new O`。不需要相反包含，也不需要新理想等于该主理想。把“只知道子理想”当作本链缺口是不正确的。

所有分母必须非零。当前 checker 验证每个 eta 在模 P 商环中为单位，故所有 eta 非零；范数递推随即保证 w 非零。

## 3. F 递推没有缺少 alpha 因子

设 `F_prev=beta^k bar(v_prev)`。则

```
F_new = F_prev² w / eta_prev²
      = beta^(2k) w / v_prev²
      = beta^(2k+c) delta
      = beta^(2k+c) bar(v_new).
```

更新指数 `k_new=2k+c`。268 的二进制为100001100，去掉首位后为00001100；八步后指数恰为268。
首步 `F_0=eta_0=alpha`，所以 `F_1=w_1`；代码用此消去而不是显式求首步除法，正确。

本归纳对每一个满足假设的 beta 都成立，不依赖唯一生成元、预选根或单位群枚举。单位根歧义不导致漏解。

## 4. 有限域模逆与指数

P=269 是素数，且 P=1 mod67。Phi_67 在 F_P 中分裂为66个互异线性因子，故

```
O/P O = product of 66 copies of F_P.
```

alpha 在该商环为单位，`beta bar(beta)=alpha` 因而使 beta 也为单位；所以 `beta^(P-1)=1`。
必须证明实际递推的分母可逆，不能因为 beta 可逆就自动假设所有 eta 可逆。当前 checker 对 alpha 及每一步 eta 逐一检查 `eta^(P-1)=1`，并使用 `eta^(P-2)` 作为逆，已补全此接口。

因此最终计算的 F 模 P 恰等于 `bar(v_final)` 模 P。

## 5. 精确坐标下界与中心残数

对 `u=sum_(j=0)^65 a_j zeta^j`，

```
Tr(u bar(u)) = a^T G a,
G = 67 Id_66 - J_66,
G^-1 = (Id_66 + J_66)/67.
```

G 正定。对第 j 个坐标作 G 内积的 Cauchy–Schwarz：

```
a_j² <= (e_j^T G^-1 e_j)*(a^T G a) = 2*T/67.
```

将 u 取为 `bar(v_final)`，其 T 与 `v_final` 相同，等于证书最后 eta 的精确迹 `67*eta[0]-sum eta`。

令 r_j 为 F 的第 j 个系数的中心整数残数。每个可能的整数提升 a_j 都满足 `|a_j|>=|r_j|`。
因此只要某个 j 满足

```
67*r_j² > 2*T,
```

就已矛盾。NO 结论不需要 `67*P²>8*T` 的唯一提升假设。
该更强大小条件只有在要断言“所有坐标的整数提升唯一就是中心残数”时才需要；当前 NO 分支不检查它是合法的。当前实例事实上也满足该条件。

## 6. 信任边界与覆盖

有限 NO 证书仅依赖：指定输入、O 中的精确多项式算术、初始成员关系、全部链等式、P 的素性/分裂、模逆及上述坐标界。上游选择 w 的启发式、LLL 结果和完整 GS 实现正确性均不被信任；它们只负责提供可以逐式重放的数据。

对 b=13，checker 验证输入 basis 与给定 R、rho 的标准基相同，并检查初始生成元在其模 R 评价核中。因此其 NO 命题对于该明确 Z-module 已成立。若要称为原 P=4/b=13 分类的整个层排除，仍须把 rho 与已验证的两根、R 的素性、完整范数及共轭覆盖接口连接；这些不是链本身自动给出的结论。

若两个候选理想严格互为共轭，alpha 为实数，则任一理想的范数 alpha 生成元通过共轭给出另一个的范数 alpha 生成元；所以一侧的 NO 可以排除整个共轭对。但“候选理想只有这一对”仍是独立覆盖事实。

## 运行入口

```
python verify_cm_result.py certificates/cm_inputs/b13.json certificates/cm_outputs/b13_certificate.json --mutations
```
