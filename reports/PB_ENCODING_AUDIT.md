# PB 编码独立对抗审计（2026-09-19）

## 判定

四种编码 one-hot、order、binary、balanced-adder 在声明的 word family 上均与原始非周期 LABS decision 严格等价；没有发现辅助变量伪解或遗漏真实 word 的数学漏洞。该结论是编码正确性，不是 N=67 的 UNSAT 结论。

本审计发现并推动修复了一处范围标签风险：原版允许 `family=global` 与非空 `fixed` 同时存在，却只返回 `family=global`。新版本增加并严格检查派生字段：

```
coverage = GLOBAL_EQUIVALENT  iff family=global and fixed={}
coverage = FAMILY_ONLY       otherwise
```

固定前缀即使碰巧是合法能量对称规范，新接口也保守标为 FAMILY_ONLY；如果需要更强的覆盖声明，必须另给覆盖证明。

## 1. 原始 word 与 XOR 的双向对应

使用 `s_i=1-2*x_i`。对 Boolean `a,b,d`，四条约束

```
a+b-d >= 0
-a-b-d >= -2
d-a+b >= 0
d+a-b >= 0
```

在 `(a,b)=(0,0),(0,1),(1,0),(1,1)` 上分别强制唯一 `d=0,1,1,0`。因此每个 lag 的 `D=sum(d)` 恰为真实 Hamming difference count，且 `C=m-2D`，`m=n-k`。所有 lag 共享同一组原始 `x_i`，不存在不同 correlation 使用不同 word 的漏洞。

## 2. 统一缩放目标

对任意整数 `D`，

```
(m-2D)^2 = (m mod 2) + 4*q_m(D)
q_m(D) = floor(m^2/4) - m*D + D^2.
```

`m=1,...,n-1` 中恰有 `floor(n/2)` 个奇数。因此

```
E = floor(n/2) + 4*Q,   Q=sum_m q_m(D_m).
```

设程序中 `Q=offset+sum c_v*v`，则最后一条不等式为

```
-sum c_v*v >= offset - floor((bound-floor(n/2))/4),
```

恰等价于整数 `E<=bound`，不要求 bound 预先落在正确同余类。
特别地，n=67、bound=237 时要求 Q<=51；没有误用 240/241。

优化模式的 OPB objective 只包含 `sum c_v*v`，没有常数 offset。外部 optimum 必须转换成 `floor(n/2)+4*(offset+optimum)`，不能直接把原始 PB objective 当 E。此外，当前优化模式仍保留 decision bound，故它优化的是带上界的实例；若上界低于真最优，会返回 UNSAT 而非无约束最优。

## 3. 四种计数与平方线性化

### One-hot

Boolean q_0,...,q_m 满足 `sum q=1` 与 `D=sum d*q_d`。恰有一个位置为1，且只能是 d=D；每个 D 都有此唯一延拓。赋予该位置 `q_m(d)` 的系数，得到精确 Q。

### Order

每个 j=1,...,m 使用

```
D-j*u_j >= 0
-D+(m-j+1)*u_j >= 1-j.
```

若 u_j=1，则第一式要求 D>=j，第二式仅要求 D<=m。
若 u_j=0，则第二式要求 D<=j-1，第一式仅要求 D>=0。
故 `u_j=[D>=j]`，两个方向均存在；邻接单调约束是冗余且安全的。
由于 `q_m(j)-q_m(j-1)=2j-m-1`，使用 offset `floor(m²/4)` 与这些系数精确恢复 q_m(D)，负系数不是 relaxation。

### Binary

`D=sum 2^j*b_j` 使用 `bit_length(m)` 位，覆盖0到m，超过m的编码值被计数等式排除。二进制展开唯一。
每个 `z=b_j AND b_h` 由 `b_j-z>=0`、`b_h-z>=0`、`z-b_j-b_h>=-1` 双向强制。
利用 Boolean b²=b，D² 的系数为单项 `4^j` 与交叉项 `2^(j+h+1)`；减去 mD 后与程序一致。

### Balanced-adder

每个局部节点的输入数为2或3，Boolean 输出 `(s,c)` 满足 `sum inputs=s+2c`。
四种可能输入总数0、1、2、3分别只有输出00、10、01、11。
未发生加法的一位直接保留原输入；最后的 carry 被追加到高位。
按树归纳，最终 bits 唯一表示所有 XOR 输入的和。没有丢失溢出位。之后平方使用与 binary 相同的 AND 线性化。

上述唯一局部延拓，加上 acyclic adder 的输入编号先于输出编号，证明每个 word 有唯一完整辅助赋值。反过来每个满足 OPB 的赋值必定是该 word 的真实语义赋值。

## 4. Family 与覆盖

全空间实例不添加 skew、DC 或 decimation。`global, fixed={}` 的投影恰是完整 Boolean cube。

`skew_dc` 则是字面上的受限 family：n=4r+3，h=n//2，x_0=x_h=0，
`x_i XOR x_(n-1-i)=(h-i) mod 2`，且 `sum x_i=(n-dc)/2`。
这是题目所给 skew 关系及 DC 的精确翻译。没有宣称它覆盖全部低能 word。

n=67、DC=9 时，中心符号1，偶位置镜像对贡献0，16个奇位置镜像对贡献2*s_i。
故 `sum_(odd i<33) s_i=4`，即恰6个负号；另外16个偶位置自由，计数恰 `C(16,6)*2^16=524812288`。

任何 `fixed` 都按其原样进一步取交集。整个 family 的 UNSAT 不自动覆盖其他 family；固定前缀的 UNSAT 也不自动覆盖整个 skew/DC9。

## 5. 独立验证边界

`verify_pb_encoding.py` 不导入生成器，也不调用 solver。它独立重建全部变量语义、全部约束多重集及目标；与 `.opb` 逐项比较。因此删除约束、增加未授权约束、系数错误、目标错误均被拒绝。SAT witness 则从原始 word 重算 C、E、全部辅助变量并比对 solver assignment。

但 metadata 是其声明输入，不是独立于问题的公理。最终证书入口必须另外核对 `n=67`、`bound=237`、`coverage`、family/fixed 以及 OPB/proof/checker 日志的散列关联。把另一个正确实例与其正确 metadata 一起替换，当然不由一般编码验证器识别成“目标错误”。

该脚本使用 Python assert；须使用普通 `python`，不得使用 `python -O` / `-OO`。UNSAT 的证明验证仍须独立 PB proof checker；编码检查或找到某个 SAT 辅助赋值绝不能替代 UNSAT proof trace。

## 6. 实际对抗检验

运行：

```
python <original-research-workspace>/pb_mutation_tests.py
```

本次对新版本独立重跑得到：

- 84 个 OPB、metadata、witness 变异全部被拒绝；另有一个伪造 GLOBAL_EQUIVALENT scope 变异被拒绝。
- 48 个 n=2,3 的实例，枚举全部原始与辅助 Boolean 变量（不是仅枚举 canonical auxiliary），在六种 bound 上检验精确 converse、唯一延拓与 SAT 数量。
- 对 m=1,...,66 所有 D,j，完成100232个 order 双向重化 converse 检验；另穷举小 one-hot 的所有合法及非法 pattern，并检查 binary count。
- 四种编码均接受当前 E=241 incumbent 的 bound=241 正控制，并在 bound=237 时判其不可行。没有将 incumbent 当作低能反例。
- 原来 n=3、`global+fixed={0:0,1:0}` 的 2/8 子立方体现在正确返回 FAMILY_ONLY；强行改成 GLOBAL_EQUIVALENT 会被拒绝。

生成结果保存在 `pb_mutation_results.json`。主侧另有 `encoding_audit_results.json`，记录四种编码 n=2,...,15 全 word 的目标一致性；本对抗审计读取了该记录，但没有把它冒称为自己重跑的全部辅助变量穷举。

## 最终结论

PB common-word 编码的 global-realizability 接口已闭合：可满足 PB 赋值恰对应一个真实二元 word，而非 pseudo-moment。
这并不解决全局最优性；是否存在满足低能阈值的赋值，仍须真实 SAT witness 或完整且独立检查通过的 UNSAT proof。
