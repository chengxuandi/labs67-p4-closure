# REOPEN：Certified PB 路线（本轮停止，未排除 N=67 目标）

`B_CAN_PRODUCE_CERTIFICATE = YES`。工具链和全局同词编码已实际打通。
`N67_E237_CERTIFICATE = NONE`。本轮唯一目标运行到限 UNKNOWN，不能报告 UNSAT。

## 1. 从项目锁定的范围

权威目标是完整 `{±1}^67` 上的非周期能量 `E=sum C_k²`，不是周期能量。
当前 run-length incumbent 由独立 `verify_sequence.py` 再算得到 E=241、P=P'=26、DC=9。
`E=33+4(P+P')` 使 E<=240 等价于 E<=237。完整定义及已读文件见 `STATE.md`。

normalized skew/DC9 family 为 s0=s33=1，s_(66-i)=(-1)^(33-i)s_i，DC=9。
它含 524812288 个词，只是压力测试子族。旧的 degree<=4/local-slice/correlation-Gram
伪矩障碍只反驳那个证书锥，不反驳 PB。没有使用“该 family 覆盖所有低能候选”的假设。

| 实例范围 | 覆盖标签 | 本轮状态 |
|---|---|---|
| 67 位完整 word，无任何结构或对称性限制 | GLOBAL_EQUIVALENT | 已生成精确 OPB 并核验编码，未做目标求解 |
| normalized skew/DC9，无 fixed 前缀 | FAMILY_ONLY | E<=237 唯一带日志运行 UNKNOWN |
| 已固定全部 incumbent 位，E<=241 | FAMILY_ONLY / 正控制 | 四编码 SAT，独立序列与两级 proof checker 通过 |
| normalized skew/DC9，E<=32 | FAMILY_ONLY / 负控制 | 简单奇偶下界 UNSAT，两级 checker 通过；不是237结论 |
| N=2,...,15 全空间、小 skew/DC families | 对各自 N 的准确范围 | 用于编码、最优值及 proof 审计，不外推 N=67 |

不存在完整的“已排除其它 families，只剩 skew/DC9”的 coverage table。
因此即使当前 family 将来 UNSAT，也不能据此宣布 LABS(67) 全局最优性。

## 2. 新 direct PB 编码与正确性

`pb_model.py` 不导入旧 SAT/CEGAR 或矩松弛代码。
同一组 Boolean x_i 表示 s_i=1-2x_i。对每一对 i<i+k，四条线性 PB 不等式
双向定义 d_(i,k)=x_i XOR x_(i+k)。因此 D_k=sum d_(i,k) 且 C_k=(n-k)-2D_k。

令 m=n-k，

    q_m(d) = floor(m²/4)-m*d+d²,
    E = floor(n/2)+4 sum_k q_(n-k)(D_k)。

四种线性化都表示完整精确 Q=sum q_m，非下界近似：

- one-hot：sum q_d=1，D=sum d*q_d，权重 q_m(d)。
- order/unary：两条 PB 不等式双向定义 u_j=[D>=j]；用相邻代价差 2j-m-1 加常数 floor(m²/4)。
- binary/native PB：sum differences=sum 2^j*b_j，平方的交叉项由精确 AND 变量表示。
- balanced-adder：每个2/3输入节点用 sum inputs=s+2carry 双向定义计数位，再精确展开平方。

最后约束 Q<=floor((bound-floor(n/2))/4)，n=67,bound=237 恰为 Q<=51。
优化模式目标不带常数 offset，读 solver bound 时必须补回 offset 和能量缩放。

逐项双向证明和独立 converse 检验见 `PB_ENCODING_AUDIT.md`。
任何满足 OPB 的模型都唯一对应同一个真实 word 及其全部相关；每个合法 word 也有唯一辅助延拓。
这在编码层关闭了 pseudo-moment 的 global-realizability gap，但没有解决低阈值可满足性。

本轮发现并修复了 `global + fixed` 的范围标签风险：仅 family=global 且 fixed 为空
才标 GLOBAL_EQUIVALENT，其余一律 FAMILY_ONLY。最终入口还绑定 n、bound、实例哈希。

## 3. 编码比较

下列为同一个 N=67/skew/DC9/E<=237 实例的实际导出规模，全部使用线性 OPB。

| 编码 | 变量 | 约束 | 文件字节 | 最大系数绝对值 | 传播／证明特点 |
|---|---:|---:|---:|---:|---|
| one-hot + native PB count | 4555 | 9181 | 419903 | 1089 | 非负离散能量，直接加权PB预算；小规模日志最经济的候选 |
| order + native PB reification | 4489 | 15484 | 2130098 | 66 | 阈值双向传播、显式单调；长PB行及负目标系数 |
| binary + native PB weighted count | 3385 | 11344 | 396434 | 4096 | 变量少，但计数位和平方乘积传播较弱 |
| balanced binary-adder | 11547 | 20344 | 783042 | 16384 | 局部等式可证书化；节点多、可能含被强制为0的高carry位 |

字节数来自第一轮 profile 所用文件；扩展 OPB header 的最后格式/实际哈希以保留实例为准。
没有把 cardinality network/totalizer 与“原生PB”混作一个独立的神奇算法：
network/totalizer 将计数分解成大量短约束，具有较强的输入域传播，但增加辅助量及日志来源。
现有仓库已记录该成本，本轮未重新运行旧 CNF totalizer。新 one-hot/order/binary 的计数关系
已经直接用 solver 原生 PB cardinality/weighted constraints；不需另做 CNF 再回 PB。
因此实际比较四种 formulation，并评估了 network/totalizer 与原生PB的接口取舍；不捏造未测实现的性能。

## 4. 分阶段证据

### B0：编码与已知最优值

四种编码均对 N=2,...,15 的所有 words 检查原始能量和所有语义辅助量，共262128次 word/formulation 检查。
N<=10 还对每个 canonical assignment 逐条检查全部 OPB 约束；全部规模都独立重建完整约束多重集。
另外48个 N=2,3 小实例穷举全部主变量及辅助变量，不只 canonical extension；
100232个 order threshold converse 检查覆盖 m<=66；局部 XOR/AND/adder 真值表完备。
这些有限测试之外，双向编码数学证明覆盖任意合法 N。

独立穷举最优值（N=2..15）：

    1,1,2,2,7,3,8,12,13,5,10,6,19,15。

实际 solver 在最优值上 SAT、在最优值减1上 UNSAT。
N=2..8 对四编码，N=9..15 对 one-hot，共70个案例；SAT 模型全部逐辅助变量核验。
70份高层日志和 elaborated kernel 均通过 VeriPB 和 CakePB，而不是只相信 solver 文本。

### B1：family 与 incumbent 正负控制

四个小 skew/DC family 的 optimum 由完备穷举获得，在 optimum 与 optimum-1 处运行并验证8份日志。
四种 N=67 编码均接受固定 incumbent 的 E<=241 实例；独立重算 E=241。
N=67/skew/DC9 的 E<=32 控制被严格拒绝。上述共13份日志都通过两级 checker。
另84种 OPB/metadata/witness mutation 和1个伪全局 scope mutation 均被拒绝。

### B2：四次固定短时 profile

各编码预设5秒内部时限；solver 粗粒度时钟实际约6秒退出。均无 proof logging，不用于任何数学结论。

| 编码 | 实际墙钟秒 | 冲突 | 决策 | 传播 | 可见 bound progress |
|---|---:|---:|---:|---:|---|
| one-hot | 6.015 | 14725 | 44613 | 4481494 | 只有初始 Q>=0，无改善 |
| order | 6.031 | 2536 | 21064 | 2006894 | 只有初始原始目标下界 -24497，无改善 |
| binary | 6.047 | 559 | 2858 | 460815 | 只有初始原始目标下界 -67437，无改善 |
| adder | 6.297 | 99 | 280 | 234876 | 只有初始原始目标下界 -67437，无改善 |

无一得到满足阈值的 word 或最终排除。统计不能比较成平均排除率或复杂性突破。
未单独采集进程峰值内存，故不报告臆测内存数字。输入、日志实际字节数均保留。

### B3：唯一目标 certified attempt

选择 one-hot（非负目标、最小约束量、当前最好的短时吞吐），固定15秒内部时限，打开 proof logging：

    --lp=0 --print-sol=1 --time-limit=15 --proof-log=...pbp

实际约16.031秒退出 TIMELIMIT：9818冲突、33562决策、4490380传播。
日志62397470字节，结尾明确为 `conclusion NONE`。
结果 **UNKNOWN**，不是 UNSAT，未接受该文件为完整 proof。
没有增加时限、没有扩批 CEGAR，也没有改用无证书 heuristic search。

## 5. 工具、真实缺陷与独立检查

固定版本/源码提交、二进制哈希、Windows构建及信任边界详见 `TOOLCHAIN_AUDIT.md`。
组合是 RoundingSat d4edbf7 → VeriPB 3.0.2 a08a1a72 → CakePB 438b8f8。
VeriPB 原源码无修改；CakePB 只修 Windows exit 参数寄存器胶水，没有改动生成的数学checker机器码。
本轮未在本地重建HOL4/CakeML全部形式化开发；这一点与编译器/FFI均明确列入工程可信边界。

实际捕获 solver 的输入边界日志缺陷：对于自身已矛盾的单个 PB 行，它可能输出 `rup >=0`
再把该恒真式引用为矛盾。独立 VeriPB 拒绝，未被当作成功。
保留的最小回归是 `toolchain_smoke/zero_coeff_contradiction.opb`，主侧也观察了
`-x6-x8>=1` 的同类缺陷。修正不修改 solver 的证明，也不放宽 checker：
若某线性行的 Boolean 最大值 sum max(0,a_i) 小于右端，就用等价的
`x1>=1` 与 `-x1>=0` 替代；常数真行省略。生成器与独立 verifier 都检查此精确转换。
修正后的70+13份日志重新生成，并全部通过两个 checker。

[Koops 等 CP2025](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CP.2025.21)
提供这种 solver→VeriPB→CakePB 证明链的背景；本项目兼容性来自实际 pinned 版本测试。
[VeriPB](https://gitlab.com/MIAOresearch/software/VeriPB)、
[RoundingSat](https://gitlab.com/MIAOresearch/software/roundingsat)、
[CakePB](https://gitlab.com/MIAOresearch/software/cakepb) 均取官方来源。
没有依赖文献中的LABS计算结果。

## 6. 重放与结果含义

```powershell
python <original-research-workspace>/verify_sequence.py
python <original-research-workspace>/verify_pb_encoding.py --audit-directory <original-research-workspace>/instances
python <original-research-workspace>/pb_mutation_tests.py
python <original-research-workspace>/check_pb_proofs.py --cake
python <original-research-workspace>/check_pb_proofs.py --cake --glob 'control_*.run.json'
python <original-research-workspace>/check_pb_proofs.py --glob 'certified_*.run.json'
```

最后一条只记录 UNKNOWN，明确不作证书接受。
`check_pb_proofs.py` 先独立核验 OPB、n、bound、coverage与生成时哈希，再要求 proof 的 SAT/UNSAT
结论与运行声明一致，最后检查独立checker明确 `VERIFIED` 输出；不能只检查进程exit0。
SAT另由原始word重算。不要用 `python -O` 禁用部分审计脚本中的断言。

小规模与控制证书逻辑结论只针对各自具体N、bound、family、fixed定义。
当前没有任何 N=67、E<=237 的已完成 PB UNSAT certificate，也没有 E<=237 真实序列。
PB 路线本轮 **STOP**。新的同词可证书编码可复用，但继续加时间不是本轮允许的下一步。

上述PB工具链、第三方二进制和大型不完整日志不属于本公开P=4重放包；命令仅记录原研究环境中的审计入口。
