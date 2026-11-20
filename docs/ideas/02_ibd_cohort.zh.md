# 群体规模的同源相同（IBD）

现有目录已有 KING、GCTA、ngsRelate、hapROH 等。本章补充本组教学章节打开的、面向大规模队列的 IBD 片段检测工具。没有在葡萄数据上运行。本章不涉及用 IBD 片段推断历史有效种群大小。

在用于 Vitis 之前至少有三条前提（不是已经验证的结论）：按克隆合并（直播主分支 `docs/WORKFLOW.md` 第 3 步，commit `eb29b98c…`：KING kinship 大于 0.354 视为同一克隆或重复，对应已打开的 KING 手册 duplicate/MZ 级别；一级亲缘不当克隆去掉），否则克隆对可能几乎全基因组 IBD（本仓库推理，[待确认]）；必须有葡萄遗传图谱，hap-IBD 的 2–4 cM 阈值来自人类图谱下的 UK Biobank，选哪张葡萄图谱标为 [待确认]；数据要已分相，分相误差可能切碎长片段（本仓库推理，[待确认]）。用片段长度换算时间的前提是有性世代，无性繁殖预期会使换算失真（本仓库推理，[待确认]）。

Zhou、Browning 和 Browning（2020，摘要；AJHG 的 PMC XML 没有正文，doi:10.1016/j.ajhg.2020.02.010）介绍 hap-IBD：在已分相的基因型上，用压缩的单倍型表示、PBWT 和多线程做检测，并在 UK Biobank 20 号染色体和模拟数据上与 GERMLINE、iLASH、RaPID、TRUFFLE 比较；摘要写它是唯一能在完整 UK Biobank 数据里又快又准地检出 2–4 cM 短片段的方法，并给出 485,346 个样本、≥2 cM 片段的用时。GitHub README（https://github.com/browning-lab/hap-ibd）写明输入是已分相数据，可处理数十万样本。这些速度和精度都来自人类队列，不是 Vitis。

本次追加还打开了 RaPID2（Tang 等 2026，全文）和 RZooRoH 的 2026 年更新（Forneris 等 2026，全文，分析近交、IBD 和亲缘）。不要把它们写成已经在葡萄上做过的结果。

论断—出处表见 [02_ibd_cohort.md](02_ibd_cohort.md)。
