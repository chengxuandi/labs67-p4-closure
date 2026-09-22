# REOPEN CM 路线：P=4 全层由有限 exact GS-chain 证书闭合

初始实验：2026-09-19；最终覆盖验证：2026-09-22。
`verify_p4_closure.py` 已实际输出 **P4_CLOSED**：32/32 支撑轨道排除。
其中20项由重新验证的惰性局部赋值证书排除；其余12项的54个候选极化理想
由27份共轭代表的完整整数反证链排除。全局 LABS(67) 最优性仍未证明。

## 状态与定理接口

```text
GLOBAL_TARGET = 对完整 ±1^67 证明 E=sum_(k=1)^66 C_k^2 >=241
CURRENT_INCUMBENT = LABS_N67_problem.md 的 run-length 见证，E=241
TARGET_UNSAT_THRESHOLD = E<=237，因 E=1 mod4
HARD_FAMILY = s0=s33=1，s_(66-i)=(-1)^(33-i)s_i；16个奇位中6个负号，DC=9
A_CURRENT_BLOCKER (旧CM路线) = 普通迹球触顶，未判定 b=13
B_CURRENT_BLOCKER (旧能量路线) = 特定 local4/slice/correlation-Gram cone 有精确低目标伪矩，非真实词
A_THEOREM_APPLIES = YES
CM_IMPLEMENTATION_PATH_EXISTS = YES
GLOBAL_PROGRESS = 尚无全空间最优性证明
PARTIAL_FAMILY_PROGRESS = 剩余54个极化理想全部排除；P=4完整闭合
```

完整定义与旧 STOP 已从问题文件、A_REPORT/A_verify/A_twisted_probe、B_REPORT/B_probe 和 DECISION 读取。normalized skew/DC9 是压力测试子族，不是全局等价限制。本路线只针对 P=4 的理想问题；E<=237 只推出 min(P,P')<=25。

| 文献输入 | 本项目对象及接口判断 |
|---|---|
| CM-order A | O=Z[zeta_67]，次数66的圆分整数环；也是 maximal order，非极大order障碍不存在 |
| involution | zeta -> zeta^-1，对所有嵌入正是复共轭 |
| fractional ideal I | 整理想 (R,zeta-rho)，显式66阶整数基；当然也是可逆fractional ideal |
| polarization w | alpha_b=17+zeta+zeta^-1-zeta^b-zeta^-b 属于实子order；先测试b=13再扩展有限清单 |
| total positivity | 每个嵌入值位于[13,21]，严格全正 |
| I bar(I)=Aw | b=13的R为素数；一般输入的R平方自由，每个素因子上互逆根赋值各1，完整Norm(alpha)=R²；全部由新覆盖checker重建 |
| requested v | beta，要求 I=O beta 且 beta bar(beta)=alpha；与本项目完全相同 |
| ambiguity | 同极化生成元仅相差 ±zeta^j；NO证书无须选定代表 |

[Lenstra–Silverberg Theorem 1.3](https://arxiv.org/html/1706.07373) 无条件适用。输入是整数乘法表、共轭矩阵、理想有理基和w，不要求单位群或DLP oracle。实际算法17.3/17.5/18.1使用辅助理想、约化张量幂、有限环陪集恢复，以及14.5的graded-order单位根处理；最终指数的素因子有界，分解不要求一般大整数factorization oracle。本轮没有声称实现整套LS通用算法。

[Kirchner 3.48/3.62](https://arxiv.org/html/1602.09037) 的圆分分支也覆盖此域；一般域中的GRH/随机性限定不应错误套在这里。它需要精确order运算、约化、模素数多项式分解、形式乘积及域中开根；其3.6提醒黑盒范数模型的常数必须显式化。本轮证书不依赖其未显式常数。

## 实际代码发现、版本与信任边界

此前 Espitau/Kirchner `ideaux.gp` 是二次幂结构，仍不能直接替换模多项式。
本轮从[作者 Wallet 代码页面](https://awallet.github.io/pages/works-and-presentations.html)找到另一实现：
[原始 Inria 仓库](https://gitlab.inria.fr/capsule/code-for-module-lip)，固定提交
`60df7fd5e81003db5eeead3ee8ce11eec47ecdd0`。

其 `attack/Gentry_Szydlo/gp` 是 Bill Allombert 的纯GP实现（README标记2025-08更新）。必须区分外层Module-LIP要求4整除导子与内层GS：后者显式处理奇导子m->2m，自带导子65测试，conjugate用x->1/x而非二次幂专用替换。因此导子67不需重发明算法。

采用[PARI官方Windows快照](https://pari.math.u-bordeaux.fr/download.html)便携二进制：
`GP/PARI 2.19.0 development 31261-9397d772d8`，编译日期2026-09-18。
SHA256：`6601312aae637523592b601e5c786c442b412f69e96cf62c266b7a186cc3baa3`。
仅在本任务文件夹下载，无系统安装。

原GS使用浮点Vandermonde估计和heuristic LLL尺度。正控制约14秒恢复生成元，独立YES verifier验证。原b13约34秒返回“no solution”，该消息单独只记UNKNOWN，不作为证明。随后只复用其8步理想约化链，导出精确整数成员等式，建立下面的独立NO证书。LLL、HNF、浮点数、GP自身结论都不属于NO证明的信任边界。

## 新 exact lemma：Fermat–norm transcript contradiction

固定 O=Z[zeta_67]。设 I 是整理想，alpha非零，p为素数、p=1 mod67，alpha mod p为单位。假定存在 beta，使I=beta O、beta bar(beta)=alpha。

证书给出初始整数多项式列表G0，其每项属于I，及二进制p-1（删除最高位1）的digits c1,...,cr。置eta0=alpha，v0=beta，k0=1。第i步给出w_i、eta_i、列表G_i和全部O线性组合。令H_i是由G_(i-1)两两乘积张成的O模；若c_i=1，再乘G0。独立检查：

1. w_i属于H_i（提供显式整数多项式组合）；
2. d_i=alpha^(c_i) eta_(i-1)^2，且 eta_i d_i=w_i bar(w_i)；
3. 对每个g属于G_i，给出h属于H_i的显式组合，验证d_i g=bar(w_i)h；
4. eta_i mod p均为单位。

这些条件只维持包含关系，不声称G_i生成整个中间理想。
若G_(i-1)包含于v_(i-1)O，则H_i包含于u_i O，其中u_i=beta^(c_i)v_(i-1)^2。
因此w_i=u_i a_i，a_i属于O。定义v_i=bar(a_i)，便有eta_i=v_i bar(v_i)，并且
g=bar(w_i)h/d_i属于v_i O。归纳得到所有v_i整性及范数等式。单位条件保证所有模运算分母可逆，且v_i非零。

令F0=alpha，递推

    F_i = F_(i-1)^2 w_i / eta_(i-1)^2  (mod p)。

直接归纳，F_i=beta^(k_i)bar(v_i)，k_i=2k_(i-1)+c_i。
O/pO是66个F_p的积；beta的范数alpha模p可逆，故beta^(p-1)=1。
于是F_r=bar(v_r) mod p。这已经消除单位根歧义，不需要第二素数或134次开根。

任一整元a=sum_(j=0)^65 a_j zeta^j的迹范数矩阵为T0=67Id-J。
其逆为(Id+J)/67，所以对每个j，由Cauchy–Schwarz有

    67 a_j^2 <= 2 Tr(a bar(a))。

设t=Tr(eta_r)，将F_r各系数取模p的最小绝对值代表r_j。
任何对应整数系数a_j都满足|a_j|>=|r_j|。因此若某j满足

    67 r_j^2 > 2t，

则假定生成元不存在。此版本甚至不需要“中心提升唯一”的附加界。
全部证明条件只涉及有限整数多项式等式、模乘幂、整数整除和一个严格整数不等式。

## b=13 的实际证书

```text
R = 31806854896213121365583994489006030403217
rho = 8770007768055987343447361867465775146418
p = 269
binary exponent = 268
steps = 8
terminal trace = 660
contradiction coefficient index = 0
centered residue = -70
67 * 70^2 = 328300 > 1320 = 2 * 660
```

`cm_outputs/b13_certificate.json`保存8步完整组合，约2.14 MB；不是搜索进度或截断日志。
`verify_cm_result.py`完全标准库、重新执行全部多项式等式与模递推，不导入生成器。
它输出PASS_NO，严格证明这个I没有要求的极化生成元。复共轭保持alpha，因此共轭I也不存在生成元；结合旧b13完整理想分类，b13两个理想均排除。

正控制除了真实GS恢复的beta通过YES检查，还由同一证书生成接口导出8步链。
独立checker得到终迹66和正确终范数，拒绝把它当NO。YES变异5项、链变异7项均被拒绝。

## 完成全部54个候选理想，而非只验证b=13

| b | 原未决理想 | 共轭代表/NO链 | 结果 |
|---|---:|---:|---|
| 5 | 4 | 2 | 全部排除 |
| 6 | 4 | 2 | 全部排除 |
| 7 | 4 | 2 | 全部排除 |
| 11 | 4 | 2 | 全部排除 |
| 13 | 2 | 1 | 全部排除 |
| 16 | 4 | 2 | 全部排除 |
| 17 | 4 | 2 | 全部排除 |
| 19 | 4 | 2 | 全部排除 |
| 28 | 8 | 4 | 全部排除 |
| 29 | 8 | 4 | 全部排除 |
| 30 | 4 | 2 | 全部排除 |
| 32 | 4 | 2 | 全部排除 |
| 合计 | 54 | 27 | 无UNKNOWN |

每个代表的运行上限固定为120秒，未提高上限或做格球枚举。23份链用p=269和8步；
b=6、11的四份链因269不适用而用p=1609和10步。素性、完全分裂、分母可逆
均由独立checker检查，不把改参数本身当作论证。
27份完整NO证书共60,769,155字节；逐例终迹、残数及输入哈希在
`p4_closure_verification.json`。这不是逐点枚举二元序列。

覆盖验证另外重建32个33阶整数范数、20项局部惰性排除、12个完整分解、
270个递归n-1 Lucas素性节点，以及所有CRT根选择和27对共轭配对。
`CM_COVERAGE_AUDIT.md`给出其数学正确性证明。
组合入口不信任保存的PASS文字：它绑定实际(b,R,rho)输入，重放全部27条链，
并再次要求实际GS正控制和正控制链通过。最终完整重放耗时约18.36秒。

对抗验证包括11类覆盖变异、7类组合层变异，以及8条用另一种多项式乘法
实现构造的已知生成元链；伪造NO、漏代表、错输入、UNKNOWN及截断链均被拒绝。
这些测试不替代引理证明；它们用于检查实现是否遵循引理。

因此新增严格定理是：

    对每个S属于{±1}^67，P(S)!=4，且P'(S)!=4。

后一结论把前一定理用于交替变号后的真实二元词即可。
这使P=4层从54个未判定理想变为0个，确有该层的完整规模闭合；
没有证明其余P层的规模下降，没有给出全局剩余维数降低的结论。

## 精确运行入口与文件格式

输入JSON：conductor=67、modulus=[1,...,1]（67项）、involution固定字符串、case、alpha66整数系数、basis66x66整数行基、ideal_index；P4输入另含rho，case=p4时还含b。
YES结果为`status=YES,beta=[66整数]`。独立验证完整范数、理想成员、zeta闭合和主理想指数。
NO_CHAIN结果给出prime、base_generators和steps。每个step是
`[digit,w,eta,w_coefficients,next_generators,next_coefficients]`；所有多项式均为66个整数。
raw生成元顺序为旧列表的i<=j乘积；若digit=1，内循环再乘初始列表。
`w_coefficients`与各`next_coefficients`按此raw顺序组成O线性组合。
bare NO、UNKNOWN及不完整链均不被接受。

```powershell
python verify_cm_result.py certificates/cm_inputs/positive67.json certificates/cm_outputs/control.json --mutations
python verify_cm_result.py certificates/cm_inputs/positive67.json certificates/cm_outputs/control_certificate.json --mutations
python verify_cm_result.py certificates/cm_inputs/b13.json certificates/cm_outputs/b13_certificate.json --mutations
python verify_p4_closure.py
python p4_closure_mutation_tests.py
```

公开仓库保留无机器路径的最终重放记录；最终SHA256清单在`hashes/FINAL_SHA256.json`。
本证明不要求相信GS实现或其NO分支正确；它们只生成可拒绝的整数证书。
数学归约、输入覆盖和反证链三部分共同证明P=4排除；不是E<=237全空间排除。
本轮到此停止。CM机制值得将来做单独、有覆盖表的有限扩展，但没有在本轮启动P=3/5或更高层。
