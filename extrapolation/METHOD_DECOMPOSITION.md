# 方法分解：先抽象，再选择新层

冻结来源为本仓库P=4 theorem。所有新工作仅在extrapolation；不改旧证书或checker。

## GENERAL_LEMMA：真实周期词的完整相对范数接口

令n=67，R_k=4z_k-1，sigma=sum z_k，P=sum z_k(2z_k-1)。
真实词的总和A满足A²=1+8sigma。取补码使A>=0，负号集合D的大小d=(67-A)/2。
由R_k=67-4d+4lambda_k得lambda_k=d-17+z_k，因此

    beta=sum_(i in D) zeta^i,
    beta*bar(beta)=alpha_z=17+sum_(k=1)^33 z_k(zeta^k+zeta^-k).

这个常数17不依赖P、d或sigma。Tr(alpha_z)=1122-2sigma=d(67-d)。
反向也成立：如果整数beta的完整相对范数为alpha_z，
写beta=sum_(i=0)^66 a_i zeta^i，则67sum a_i²-(sum a_i)²=d(67-d)。
系数和模67必为d或67-d（67是素数）；整体平移所有系数，使和规范为r=d或67-d。
于是sum a_i²=sum a_i=r；各整数a_i(a_i-1)>=0强制每项为0。
故恢复重量d或67-d的真正二元词。只要alpha_z满足上述sigma恒等式，该论证不限定P=4。
完整范数系数再由Phi_67的唯一线性关系恢复全部周期交数。

## GENERAL_LEMMA：极化理想与有限整数反证链

同一O_K、共轭、迹Gram矩阵、模完全分裂素数的Fermat指数恢复、
显式模块包含与相对范数递推，均不依赖P。旧链的soundness证明可直接参数化alpha与I。
整数解必产生I=(beta)且I*bar(I)=(alpha)。枚举全部这类I，再逐个证书排除即可。
共轭理想可配对；sigma和alpha同时作Galois作用时存在性保持。

## PARAMETER_DEPENDENT_STEP

- 精确signature及其支撑轨道：必须从P与sum恒等式重新覆盖，不能复用P4清单。
- alpha的全正性：容易时用17-2sum|z|>0；该充分界失败不能判负，必须另作精确符号检验。
- 完整理想分解：要保留所有素理想及各自赋值。
- 若共轭素理想对的alpha赋值为e，则beta的两边赋值为a,e-a，a=0,...,e；
  惰性自共轭素理想赋值必须偶数。重因子、高剩余次数及67处的分歧均不可照搬CRT线性根。
- 模素数p与指数p-1依赖选择的可逆条件，不是P的函数。
- w、eta、模块成员系数及最终矛盾必须重新验证；同拓扑不意味相同数值可复用。

## P4_ONLY_STEP

P4只容许一个+1和一个-1；其和为0。规范后32支撑。
旧20项惰性排除、12个剩余alpha、其平方自由完全分裂范数、54个理想、
27份数值反证链和各自终迹/残数都是P4专有事实。

## 为什么P4闭合

不是因为任意低P都会给出小终迹，也不是因为GS失败即无解。
关键组合是：小而完备的支撑覆盖；剩余理想分解简单；有限链实际产生低迹终点；
最终残数违反严格迹坐标界。最后两点尚没有只由P保证的统一定理。

## signature计数的语义边界

整数预算、相关和平方、轨道及局部必要条件给出的是candidate signatures。
只有经过完整范数存在性判定或真实二元词见证，才可标REALIZABLE。
“枚举全部真正可实现signature”本身包含待解的范数问题，不能把必要条件清单改名为可实现清单。
高层必须明确报告未判定；若清单规模触发停止条件，不会制造一个伪完整列表。

本轮验证状态：相应有限反例测试与正控制通过；详见verifier_logs/new_lemma_audit.json和general_chain_controls.json。
