# 透明tractability ranking

排除旧闭合层及已有真实词的层后，排序键为：(候选Galois轨道数，最大支撑，max|z|)。
这是进入算术审计前的精确结构排序；未分解的ideal cases和未知终迹不作为假数值评分。
旧研究已有P1的47569惰性素数排除及P2整数恒等式排除；二者不计为新增闭合。
BEST_NEXT_P=3（166轨道）；其次P5（496轨道）；执行前先测理想覆盖规模。
P0有正控制，P18和P20已有真实词，不能把这些整层列为可排除目标。

|次序|P|候选轨道|支撑|初步决定|
|---|---:|---:|---|---|
|1|3|166|[3]|audit|
|2|5|496|[3]|audit|
|3|8|7440|[4]|symbolic scaling wall|
|4|6|33566|[6]|symbolic scaling wall|
|5|7|35992|[2, 5]|symbolic scaling wall|
|6|9|71952|[2, 5]|symbolic scaling wall|
|7|12|672252|[3, 6]|symbolic scaling wall|
|8|11|2733456|[4, 7]|symbolic scaling wall|
|9|13|4550800|[4, 7]|symbolic scaling wall|
|10|10|6206696|[5, 8, 10]|symbolic scaling wall|
|11|16|29738952|[2, 5, 8]|symbolic scaling wall|
|12|15|131815531|[1, 3, 6, 9, 15]|symbolic scaling wall|
|13|17|150277832|[3, 6, 9]|symbolic scaling wall|
|14|14|271206972|[4, 7, 9, 10, 12]|symbolic scaling wall|
|15|21|2909258012|[3, 5, 8, 11, 21]|symbolic scaling wall|
|16|19|3025547734|[3, 5, 8, 11, 14, 17]|symbolic scaling wall|
|17|24|11119992760|[4, 6, 9, 12]|symbolic scaling wall|
|18|25|36177666408|[2, 4, 5, 7, 10, 13, 20, 23]|symbolic scaling wall|
|19|23|41035517160|[4, 5, 7, 10, 13, 16, 19]|symbolic scaling wall|
|20|22|69371292840|[3, 5, 6, 7, 8, 10, 11, 13, 14, 16]|symbolic scaling wall|

## P3闭合后的再排序

P3_CLOSED；NEXT_P=5，但本轮停止于规模审计。P5仍OPEN；随后是P8（7440候选轨道），不能通过换层得到更小清单。
