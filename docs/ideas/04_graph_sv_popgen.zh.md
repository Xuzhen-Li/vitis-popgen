# 基于图的结构变异群体遗传

当前 README 第 11 节主要指向 vitis-pangenome，并列了 PanGenie、vg（Giraffe + vg call）等。本章补充本组教学章节打开的方法论文和一份葡萄泛基因组变异图谱，不代替 vitis-pangenome。

Ebler 等（2022，全文）是 PanGenie 的论文，题为基于泛基因组的基因组推断，可在很广的变异类型上做基因分型。Sirén 等（2021，全文）用泛基因组在 5,202 个多样的基因组中对已知结构变异分型（Giraffe / vg）。这两篇都是方法或人类数据，不是葡萄结果。

Liu 等（2024，全文）用 18 个新产生的分相端粒到端粒组装和 11 个已发表组装构建图泛基因组参考 Grapepan v.1.0，并得到 9,105,787 个短变异和 236,449 个 SV。结果中写：“On average, 88.6% of the SVs overlapped TEs, whereas 30.9% intersected gene structures (Supplementary Fig. 7c,d)。”同一篇还写：“The estimated heritability improves by 22.78% on average when including SVs。”这两个数字都是该研究的结果，不是普遍定律。Guo 等（2025，仅摘要）报道 72 份全球葡萄单倍型解析基因组（野生 25、栽培 47，其中 60 份新发布），欧洲栽培品种的 NLR 抗性基因库更小，并写有 63 个以上与霜霉病抗性显著相关的 SV。

论断—出处表见 [04_graph_sv_popgen.md](04_graph_sv_popgen.md)。
