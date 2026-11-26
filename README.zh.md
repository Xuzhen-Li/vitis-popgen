# vitis-popgen

[English](README.md) | 中文

<!-- PROSE:INTRO -->
本仓库是面向公开或已发表数据的 *Vitis* 群体结构、基因流、驯化、选择、历史人口学及相关分析的方法目录。内容按任务分节，附有跳转链接，每种工具仅保留核对过的最新版本，流程页见 [`docs/WORKFLOW.zh.md`](docs/WORKFLOW.zh.md)。
<!-- /PROSE:INTRO -->

不包含未发表的基因型、私有坐标或样本级矩阵。

## 本仓库不包含

- 167K 从 FASTQ 到祖源的产品：[grapeancestry](https://github.com/Xuzhen-Li/grapeancestry)
- 理论笔记（一篇论文，一个文件夹）：[genomics-theory-book](https://github.com/Xuzhen-Li/genomics-theory-book)
- 芯片设计：[grapevine-chip](https://github.com/Xuzhen-Li/grapevine-chip)
- 泛基因组图构建和完整的图工具列表：[vitis-pangenome](https://github.com/Xuzhen-Li/vitis-pangenome)
- 古DNA从湿实验到鉴定：[grapevine-adna](https://github.com/Xuzhen-Li/grapevine-adna)（与本目录若干节的重叠是预期之中的）

<!-- PROSE:CATALOG_NOTE -->
**2026-11-14 目录，第 3.2 版。** 每节开头设有 **分组：** 列表，标明条目属于备选（择一）、互补（并用）还是按顺序执行。同一程序的不同版本合并为一条，并以 2026-11-14，Asia/Shanghai（CST，UTC+8）核对过的最新稳定版本命名。候选发布版和预发布版不作为目录版本。未经核对的版本或 DOI 标为 [待确认]；附加说明写在标记外侧，例如 [待确认]（numbering）。包含判断节点的流程见 [`docs/WORKFLOW.zh.md`](docs/WORKFLOW.zh.md)。
<!-- /PROSE:CATALOG_NOTE -->

---

## 目录

1. [变异检测与质量控制](#section-1) (32)
2. [群体结构、祖源混合与主成分分析](#section-2) (16)
3. [系统发育与网络](#section-3) (12)
4. [历史人口学](#section-4) (17)
5. [选择扫描](#section-5) (14)
6. [渗入与 f 统计](#section-6) (11)
7. [连锁不平衡与重组](#section-7) (5)
8. [纯合片段、近交、亲缘与无性系](#section-8) (12)
9. [全基因组关联、遗传-环境关联与景观基因组学](#section-9) (15)
10. [遗传负荷与有害突变](#section-10) (6)
11. [结构变异与泛基因组图群体遗传](#section-11) (6)
12. [模拟](#section-12) (8)
13. [可视化](#section-13) (4)
14. [工作流与流程](#section-14) (2)
15. [葡萄群体遗传研究与公开资源](#section-15) (15)
16. [在葡萄上仍少有充分测试的想法](#section-16) (4)
17. [亲本鉴定、系谱与名称核对](#section-17) (4)

本页共 183 条（其中工具 147 条；其余为流程、方案、文献、资源或想法）。表格形式见 [`ADDITIONS.tsv`](ADDITIONS.tsv) 和 [`catalog/CATALOG.tsv`](catalog/CATALOG.tsv)。

<a id="section-1"></a>
## 1. 变异检测与质量控制

<!-- PROSE:SECTION:P01 -->
面向公开重测序数据的变异检测、质控、身份核对、定相和基因型填充。下游分析前需先检出克隆和重复样本，一级亲缘则需另行处理（见流程页）。
<!-- /PROSE:SECTION:P01 -->

**分组：**
- *Joint genotyping (alternatives)*：GLnexus。
- *Mapping (alternatives)*：BWA (bwa mem / bwa aln), bwa-mem2。
- *BAM processing (complementary)*：samtools。
- *Phasing and imputation of modern data (in order)*：Beagle, GLIMPSE2, SHAPEIT5, WhatsHap。
- *Read QC (complementary)*：FastQC, MultiQC, fastp, seqkit。
- *Sample identity, before structure (complementary)*：KING, PLINK 1.9, peddy, plink2, somalier, verifybamid2, SNPRelate, Technical-replicate IBS or discordance cutoff (idea)。
- *BAM hygiene / post-mapping (complementary)*：Picard。
- *VCF QC and manipulation (complementary)*：bcftools, htslib, mosdepth, vcftools, vt。
- *Variant calling (alternatives)*：DeepVariant, GATK HaplotypeCaller / GenotypeGVCFs, Octopus, freebayes。
- *Somatic variants among clones (complementary)*：GATK Mutect2, L1/L2 chimerism validation design (idea)。

- **GLnexus**（工具）— 把 DeepVariant gVCF 联合分型成队列 VCF。 输入：gVCF。输出：VCF。版本：1.4.1（GitHub dnanexus-rnd/GLnexus + Bioconda, 2026-11-14 CST）。 [link](https://github.com/dnanexus-rnd/GLnexus)  
  注：AM03 alternative to GATK GenotypeGVCFs.
- **BWA (bwa mem / bwa aln)**（工具）— 现代数据用 bwa mem；古DNA默认用 bwa aln（见 grapevine-adna）。 输入：FASTQ, FASTA。输出：SAM/BAM。版本：0.7.19（GitHub lh3/bwa + Bioconda, 2026-11-14 CST）。 [doi:10.1093/bioinformatics/btp324](https://doi.org/10.1093/bioinformatics/btp324) · [link](https://github.com/lh3/bwa)
- **bwa-mem2**（工具）— 现代葡萄重测序的默认短读比对器（AM03）。 输入：FASTQ, FASTA。输出：SAM/BAM。版本：2.3（GitHub bwa-mem2/bwa-mem2 + Bioconda, 2026-11-14 CST）。 [link](https://github.com/bwa-mem2/bwa-mem2)  
  注：Use bwa aln for degraded aDNA; that route is in grapevine-adna.
- **samtools**（工具）— 排序、建索引、标记重复、过滤并汇报比对统计。 输入：SAM/BAM/CRAM。输出：BAM/CRAM, stats。版本：1.25（GitHub samtools/samtools + Bioconda, 2026-11-14 CST）。 [doi:10.1093/gigascience/giab008](https://doi.org/10.1093/gigascience/giab008) · [link](https://github.com/samtools/samtools)  
  注：Same 1.25 line as bcftools and htslib. samtools is not a mapper; it belongs with BAM processing, not under Mapping.
- **Beagle**（工具）— 相对于 SHAPEIT5 和 GLIMPSE2 的定相与补全备选。 输入：VCF。输出：phased or imputed VCF。版本：5.4_22Jul22.46e（Bioconda beagle, 2026-11-14 CST）。 [doi:10.1016/j.ajhg.2018.07.015](https://doi.org/10.1016/j.ajhg.2018.07.015) · [link](https://faculty.washington.edu/browning/beagle/beagle.html)  
  注：Bioconda build date is 22 July 2022. Check the author site before pinning a newer unlisted build [待确认]. Beagle 5 paper DOI (Browning et al. 2018) verified by Crossref in the literature review.
- **GLIMPSE2**（工具）— 用单倍型参考面板补全低覆盖度基因组。 输入：low-coverage BAM or genotype likelihoods, reference panel。输出：imputed VCF。版本：2.0.0（GitHub odelaneau/GLIMPSE tag v2.0.0 (latest stable), 2026-11-14 CST; v2.0.1 is a GitHub pre-release and is not used as the catalogue version）。 [doi:10.1038/s41588-023-01438-3](https://doi.org/10.1038/s41588-023-01438-3) · [link](https://github.com/odelaneau/GLIMPSE)  
  注：For aDNA, test accuracy on modern grapes downsampled to ancient depths first (AM17, project 20). GitHub v2.0.1 is marked pre-release (checked 2026-11-14 CST); Bioconda glimpse-bio may still list 2.0.1. This catalogue pins the latest stable tag, 2.0.0, consistent with not using RC or beta tags as the catalogue version.
- **SHAPEIT5**（工具）— 先对常见变异再对稀有变异定相。AM13 和 AM26 的默认工具，有已发表连锁图时使用该图。 输入：VCF, genetic map。输出：phased VCF。版本：5.1.1（GitHub odelaneau/shapeit5 + Bioconda, 2026-11-14 CST）。 [doi:10.1038/s41588-023-01415-w](https://doi.org/10.1038/s41588-023-01415-w) · [link](https://github.com/odelaneau/shapeit5)  
  注：Do not use a pyrho map for phasing (AM26).
- **WhatsHap**（工具）— 基于读段的定相，有长读或连锁读段时有用。 输入：BAM, VCF。输出：phased VCF。版本：2.8（GitHub whatshap/whatshap + Bioconda/PyPI, 2026-11-14 CST）。 [link](https://github.com/whatshap/whatshap)
- **FastQC**（工具）— 逐文件的读段质量、长度和接头含量。 输入：FASTQ。输出：HTML/zip QC。版本：0.13.0（GitHub s-andrews/FastQC + Bioconda, 2026-11-14 CST）。 [link](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
- **MultiQC**（工具）— 把多种工具的质控报告汇总成一份 HTML。 输入：tool QC files。输出：HTML report。版本：1.35（GitHub MultiQC/MultiQC + Bioconda, 2026-11-14 CST）。 [link](https://github.com/MultiQC/MultiQC)
- **fastp**（工具）— 修剪接头和低质量碱基，并写出质控报告。 输入：FASTQ。输出：trimmed FASTQ, HTML/JSON QC。版本：1.4.0（GitHub OpenGene/fastp + Bioconda, checked 2026-11-14 CST）。 [link](https://github.com/OpenGene/fastp)  
  注：GitHub release 2026-10-07. Also in vitis-open-directions AM02.
- **seqkit**（工具）— FASTQ/FASTA 统计、过滤和格式转换。 输入：FASTQ/FASTA。输出：tables, filtered files。版本：2.14.0（GitHub shenwei356/seqkit + Bioconda, 2026-11-14 CST）。 [link](https://github.com/shenwei356/seqkit)
- **KING**（工具）— 用于区分克隆/重复与一级亲缘的稳健亲缘估计。克隆和重复（亲缘系数高于 0.354）每组只留一个样本；一级亲缘（0.177-0.354）只登记，不当作同一基因型删掉。 输入：hard-called diploid genotypes (BED)。输出：kinship tables。版本：2.3.2（Bioconda king, 2026-11-14 CST）。 [doi:10.1093/bioinformatics/btq559](https://doi.org/10.1093/bioinformatics/btq559) · [link](https://www.kingrelatedness.com/)  
  注：Thresholds follow the KING manual (https://www.kingrelatedness.com/manual.shtml): kinship above 0.354 is the duplicate/MZ class; 0.177-0.354 is first-degree. Paper: Manichaikul et al. 2010, 10.1093/bioinformatics/btq559. AM26 used 0.177 as the first-degree lower cutoff. Input should be hard-called diploid genotypes (BED). For low-coverage or ancient samples use ngsRelate, READv2, KIN or BREADR instead. Handling of first-degree relatives is analysis-specific; see docs/WORKFLOW.md.
- **PLINK 1.9**（工具）— 旧版 PLINK，部分 ROH 和格式转换仍会用到。 输入：BED/PED。输出：IBD, ROH, association。版本：1.90b6.21（Bioconda plink, 2026-11-14 CST）。 [doi:10.1086/519795](https://doi.org/10.1086/519795) · [link](https://www.cog-genomics.org/plink/1.9/)  
  注：DOI is Purcell et al. 2007. Chang et al. 2015 (doi:10.1186/s13742-015-0047-8) describes 1.9.
- **peddy**（工具）— 亲缘和祖源离群点质控。哺乳动物式的性别检查不能照搬到葡萄。 输入：VCF, PED。输出：HTML QC。版本：0.4.8（GitHub brentp/peddy + Bioconda/PyPI, 2026-11-14 CST）。 [link](https://github.com/brentp/peddy)
- **plink2**（工具）— 把 VCF 转成分析文件，并做 PCA、亲缘和基础关联。 输入：VCF, PGEN/BED。输出：PGEN, PCA, kinship, association。版本：2.0.0-b.1.4（GitHub chrchang/plink-ng 2026-11-07; Bioconda 2.00a5.10）。 [doi:10.1186/s13742-015-0047-8](https://doi.org/10.1186/s13742-015-0047-8) · [link](https://www.cog-genomics.org/plink/2.0/)  
  注：Newest GitHub tag uses pre-release-style numbering. Bioconda still 2.00a5.10. The DOI is Chang et al. 2015 (PLINK 1.9); a separate paper for this exact 2.0 tag was not confirmed.
- **somalier**（工具）— 从 BAM 或 VCF 快速检查亲缘和样本是否拿错。 输入：BAM/VCF。输出：relatedness, QC plots。版本：0.3.7（GitHub brentp/somalier + Bioconda, 2026-11-14 CST）。 [link](https://github.com/brentp/somalier)  
  注：Like peddy and verifybamid2, this tool ships with human site lists. Build a grape site set before using it on Vitis; off-the-shelf human sites are not appropriate.
- **verifybamid2**（工具）— 估计 BAM 与 VCF 之间的污染和样本对调。原为人类设计，葡萄上的数值只作探索。 输入：BAM, VCF。输出：contamination estimate。版本：2.0.3（GitHub Griffan/VerifyBamID + Bioconda, 2026-11-14 CST）。 [link](https://github.com/Griffan/VerifyBamID)  
  注：See grapevine-adna for plant contamination.
- **SNPRelate**（工具）— 在 R 中计算 IBS、IBD（矩估计/极大似然）和 PCA，可作为 KING 的交叉核对。 输入：GDS (from VCF)。输出：IBS matrix, IBD estimates, PCs。版本：1.46.0（Bioconductor release package SNPRelate 1.46.0, checked 2026-11-14 CST）。 [doi:10.1093/bioinformatics/bts606](https://doi.org/10.1093/bioinformatics/bts606) · [link](https://bioconductor.org/packages/SNPRelate/)  
  注：Version is the Bioconductor release page value on 2026-11-14 CST.
- **Technical-replicate IBS or discordance cutoff (idea)**（想法）— 用同一 DNA 的重复测序和已知克隆对，校准“同一基因型”可接受的 IBS 或基因型不一致率，避免把测序误差和体细胞变异当成不同品种。 输入：VCF。输出：pairwise discordance distribution and a cutoff。版本：n/a（methods review, 2026-11-14 CST）。  
  注：Complements the KING 0.354 rule; it does not replace it.
- **Picard**（工具）— MarkDuplicates、读组、CleanSam 等 BAM 整理。 输入：BAM/SAM。输出：BAM, metrics。版本：3.5.0（GitHub broadinstitute/picard + Bioconda, 2026-11-14 CST）。 [link](https://github.com/broadinstitute/picard)  
  注：Picard works on BAM (MarkDuplicates, read groups, CleanSam), not on VCF. GitHub release 2026-07-31 CST-relative: 2026-08-01 02:56 CST.
- **bcftools**（工具）— 过滤、规范化、注释、统计，以及 ROH 检测（见第 8 节）。 输入：VCF/BCF or BAM。输出：VCF/BCF, tables。版本：1.25（GitHub samtools/bcftools + Bioconda, 2026-11-14 CST）。 [doi:10.1093/gigascience/giab008](https://doi.org/10.1093/gigascience/giab008) · [link](https://github.com/samtools/bcftools)
- **htslib**（工具）— samtools 和 bcftools 的底层库，应与 1.25 同一条线钉死。 输入：BAM/VCF streams。输出：same。版本：1.25（GitHub samtools/htslib + Bioconda, 2026-11-14 CST）。 [doi:10.1093/gigascience/giab008](https://doi.org/10.1093/gigascience/giab008) · [link](https://github.com/samtools/htslib)
- **mosdepth**（工具）— 快速计算逐碱基和窗口深度，用来做可检测位点掩膜。 输入：BAM/CRAM。输出：depth BED/txt。版本：0.3.15（GitHub brentp/mosdepth 2026-10-29; Bioconda still 0.3.14）。 [link](https://github.com/brentp/mosdepth)  
  注：Newest is GitHub 0.3.15; Bioconda lagged at 0.3.14 on 2026-11-14.
- **vcftools**（工具）— 经典 VCF 过滤和窗口统计。全位点 VCF 上的 pi 和 dxy 更建议用 pixy。 输入：VCF。输出：filtered VCF, window stats。版本：0.1.17（GitHub vcftools/vcftools + Bioconda, 2026-11-14 CST）。 [doi:10.1093/bioinformatics/btr330](https://doi.org/10.1093/bioinformatics/btr330) · [link](https://github.com/vcftools/vcftools)  
  注：No newer tagged release than 0.1.17.
- **vt**（工具）— 在队列质控前规范化并拆分复杂变异。 输入：VCF。输出：normalised VCF。版本：0.57721（GitHub atks/vt + Bioconda, 2026-11-14 CST）。 [link](https://github.com/atks/vt)
- **DeepVariant**（工具）— AM03 草图中现代 SNP/indel 的默认检测器（WGS 模型）。 输入：BAM/CRAM, FASTA。输出：VCF/gVCF。版本：1.10.0（GitHub google/deepvariant, 2026-11-14 CST）。 [doi:10.1038/nbt.4235](https://doi.org/10.1038/nbt.4235) · [link](https://github.com/google/deepvariant)  
  注：Joint-genotype gVCFs with GLnexus. Record whether a plant-trained model is used.
- **GATK HaplotypeCaller / GenotypeGVCFs**（工具）— 短读 SNP 和 indel 的备选检测与联合分型路径。 输入：BAM, FASTA。输出：gVCF, joint VCF。版本：4.7.0.0（GitHub broadinstitute/gatk, 2026-11-14 CST）。 [doi:10.1101/gr.107524.110](https://doi.org/10.1101/gr.107524.110) · [link](https://github.com/broadinstitute/gatk)
- **Octopus**（工具）— 对 indel 和局部单倍型建模较强的检测器。 输入：BAM, FASTA。输出：VCF。版本：0.7.4（GitHub luntergroup/octopus + Bioconda, 2026-11-14 CST）。 [link](https://github.com/luntergroup/octopus)
- **freebayes**（工具）— 基于单倍型的贝叶斯检测器，适用于葡萄高杂合区域。 输入：BAM, FASTA。输出：VCF。版本：1.3.10（GitHub freebayes/freebayes + Bioconda, 2026-11-14 CST）。 [link](https://github.com/freebayes/freebayes)
- **GATK Mutect2**（工具）— 把同一品种的不同克隆按配对样本比较，寻找体细胞变异。 输入：paired BAM。输出：somatic VCF。版本：4.7.0.0（same GATK 4.7.0.0 already listed for HaplotypeCaller in this catalogue）。 [link](https://github.com/broadinstitute/gatk)  
  注：The tool exists. Power and false-positive rate under grape L1/L2 chimerism remain [待确认] and need independent validation. DOI of a Mutect2 methods paper [待确认].
- **L1/L2 chimerism validation design (idea)**（想法）— 等位比例低的体细胞变异需要高深度、生物学重复，最好分层取材，并用独立方法验证。L1/L2 混合组织里的等位比例，不能当成可遗传变异的证据。 输入：high-depth BAM。输出：validated somatic variants。版本：n/a（methods and genetics reviews, 2026-11-14 CST）。  
  注：Biological interpretation of grape chimerism is outside the methods review; this is a design reminder.

<a id="section-2"></a>
## 2. 群体结构、祖源混合与主成分分析

<!-- PROSE:SECTION:P02 -->
全局祖源、PCA、局部祖源和空间结构。每个克隆或重复组仅保留一个样本；一级亲缘需根据具体分析采取相应处理（使用无亲缘子集后投影，或做敏感性分析），不可当作同一基因型剔除。
<!-- /PROSE:SECTION:P02 -->

**分组：**
- *Chromosome painting and local ancestry (in order)*：Loter, RFMix, fineSTRUCTURE / ChromoPainter。
- *Global ancestry (alternatives)*：ADMIXTURE, fastSTRUCTURE, sNMF (LEA)。
- *Low-coverage genotype-likelihood methods (alternatives)*：ANGSD, PCAngsd。
- *ADMIXTURE fit check (complementary)*：evalAdmix。
- *PCA (alternatives)*：flashpca, smartpca (EIGENSOFT)。
- *Q-matrix display (complementary)*：pophelper。
- *Spatial or inversion-aware structure (complementary)*：lostruct。
- *Spatial structure (alternatives)*：FEEMS, conStruct。
- *Key low-coverage references (complementary)*：Lou et al. 2021 lcWGS guide。

- **Loter**（工具）— 无需预先定相的二源或多源局部祖源。 输入：diploid genotypes。输出：local ancestry。版本：1.0.1（GitHub bcm-uga/Loter + Bioconda, 2026-11-14 CST）。 [link](https://github.com/bcm-uga/Loter)
- **RFMix**（工具）— SHAPEIT5 定相后的局部祖源，AM13 默认工具。 输入：phased VCF, reference panels。输出：local-ancestry tracts。版本：2.03.r0.9505bfa（Bioconda rfmix, 2026-11-14 CST (same string as AM13)）。 [link](https://github.com/slowkoni/rfmix)
- **fineSTRUCTURE / ChromoPainter**（工具）— 把染色体画成供体单倍型马赛克，比单一 ADMIXTURE K 更细。 输入：phased haplotypes。输出：painting, coancestry。版本：[待确认]（Vendor site; version not checked in this build）。 [doi:10.1371/journal.pgen.1002453](https://doi.org/10.1371/journal.pgen.1002453) · [link](https://people.maths.bris.ac.uk/~madjl/finestructure/)  
  注：Version [待确认].
- **ADMIXTURE**（工具）— 最大似然祖源比例，AM13 的默认工具。 输入：BED, LD-pruned SNPs。输出：Q and P matrices。版本：1.3.0（Bioconda admixture, 2026-11-14 CST）。 [doi:10.1101/gr.094052.109](https://doi.org/10.1101/gr.094052.109) · [link](https://dalexander.github.io/admixture/)  
  注：Clone-prune first (one sample per clone or duplicate group). First-degree relatives should not be dropped as if they were the same genotype; for ADMIXTURE use an unrelated subset or report a sensitivity analysis (see docs/WORKFLOW.md). Choose K with cross-validation and inspect fit with evalAdmix.
- **fastSTRUCTURE**（工具）— 面向大型 SNP 集的变分 STRUCTURE 类模型。 输入：STRUCTURE or BED-like files。输出：Q matrix。版本：1.0（GitHub rajanil/fastStructure + Bioconda, 2026-11-14 CST）。 [doi:10.1534/genetics.114.164350](https://doi.org/10.1534/genetics.114.164350) · [link](https://github.com/rajanil/fastStructure)  
  注：Last tagged release remains 1.0.
- **sNMF (LEA)**（工具）— 快速稀疏 NMF 祖源，对缺失数据往往比 ADMIXTURE 更宽容。 输入：genotype matrix。输出：Q matrix。版本：sNMF 1.2; LEA package version [待确认]（Bioconda snmf 1.2; LEA is Bioconductor）。 [link](https://bcm-uga.github.io/LEA/)
- **ANGSD**（工具）— 从 BAM 计算基因型似然、等位基因频率、SFS、关联和单倍型调用。 输入：BAM, reference。输出：genotype likelihoods, SFS, MAF, haploid calls。版本：0.940（GitHub ANGSD/angsd + Bioconda, 2026-11-14 CST）。 [doi:10.1186/s12859-014-0356-4](https://doi.org/10.1186/s12859-014-0356-4) · [link](https://github.com/ANGSD/angsd)  
  注：Central for aDNA and low-coverage modern data. Human X-chromosome contamination utilities do not transfer to grape.
- **PCAngsd**（工具）— 用基因型似然做 PCA 和类混合结构分析，适用于低覆盖度。 输入：ANGSD-style genotype likelihoods。输出：principal components, admixture。版本：1.37.0（GitHub Rosemeis/pcangsd 2026-10-23; Bioconda/PyPI 1.36.4）。 [doi:10.1534/genetics.118.301336](https://doi.org/10.1534/genetics.118.301336) · [link](https://github.com/Rosemeis/pcangsd)  
  注：Newest GitHub tag is 1.37.0; Bioconda lagged at 1.36.4.
- **evalAdmix**（工具）— 检查 ADMIXTURE 或 NGSadmix 的 Q 矩阵是否真的拟合数据。 输入：genotype likelihoods or genotypes, Q matrix。输出：residuals, plots。版本：1.0（GitHub GenisGE/evalAdmix + Bioconda, 2026-11-14 CST）。 [doi:10.1111/1755-0998.13171](https://doi.org/10.1111/1755-0998.13171) · [link](https://github.com/GenisGE/evalAdmix)  
  注：DOI（Garcia-Erill and Albrechtsen 2020）已在 2026-11-14 的文献核对中经 Crossref 核实。
- **flashpca**（工具）— 大型 SNP 矩阵上的快速 PCA。 输入：BED。输出：principal components。版本：2.0（GitHub gabraham/flashpca + Bioconda, 2026-11-14 CST）。 [link](https://github.com/gabraham/flashpca)
- **smartpca (EIGENSOFT)**（工具）— 带收缩和 lsqproject 的 PCA，通常用来把古DNA投射到现代 PCA 上。 输入：EIGENSTRAT。输出：eigenvectors, projected PCs。版本：9.0.0 (Bioconda); GitHub tag v8.0.0 [待确认] (numbering)（Bioconda eigensoft 9.0.0; DReichLab/EIG GitHub tag v8.0.0）。 [doi:10.1371/journal.pgen.0020190](https://doi.org/10.1371/journal.pgen.0020190) · [link](https://github.com/DReichLab/EIG)  
  注：Pin the exact binary. Bioconda and GitHub numbers disagree.
- **pophelper**（工具）— 对齐并绘制不同 K 下的 ADMIXTURE 或 STRUCTURE Q 矩阵。 输入：Q files。输出：plots, aligned Q。版本：2.3.1（GitHub royfrancis/pophelper, 2026-11-14 CST）。 [link](https://github.com/royfrancis/pophelper)
- **lostruct**（工具）— 窗口局部 PCA，用来找倒位和局部祖源区段。 输入：genotypes。输出：local-PCA MDS, outlier windows。版本：[待确认]（GitHub petrelharp/local_pca; no release tag in this check）。 [link](https://github.com/petrelharp/local_pca)  
  注：Useful on grape inversion candidates; see also vitis-pangenome and vitis-open-directions project 17.
- **FEEMS**（工具）— 根据样本地理坐标估计有效迁移表面。 输入：genotypes, public coordinates。输出：migration surfaces。版本：2.0.1（GitHub NovembreLab/feems + PyPI, 2026-11-14 CST）。 [link](https://github.com/NovembreLab/feems)  
  注：This repository does not accept private site coordinates.
- **conStruct**（工具）— 把距离隔离和混合分开的空间结构模型。 输入：allele frequencies, coordinates。输出：layer contributions。版本：1.0.3（GitHub gbradburd/conStruct, 2026-11-14 CST）。 [link](https://github.com/gbradburd/conStruct)
- **Lou et al. 2021 lcWGS guide**（文献）— 关于低覆盖全基因组数据上用基因型似然做群体遗传的实用指南。 输入：n/a。输出：n/a。版本：n/a（Crossref-verified in the literature review, 2026-11-14 CST）。 [doi:10.1111/mec.16077](https://doi.org/10.1111/mec.16077) · [link](https://doi.org/10.1111/mec.16077)

<a id="section-3"></a>
## 3. 系统发育与网络

<!-- PROSE:SECTION:P03 -->
基于 LD 修剪后 SNP 或基因树构建系统发育树和网络。相互冲突的演化历史应通过网络呈现，而非仅依赖单一树形结构。质体单倍型可补充母系证据（见 grapevine-plastid），但在葡萄属内的分辨率较低。
<!-- /PROSE:SECTION:P03 -->

**分组：**
- *Bayesian or dated trees (alternatives)*：BEAST 2。
- *Fast trees (alternatives)*：FastTree。
- *Maximum-likelihood trees (alternatives)*：IQ-TREE 2, IQ-TREE 3, RAxML-NG。
- *Networks and mixtures (alternatives)*：TreeMix。
- *Networks and mixtures (complementary)*：OptM, Twisst。
- *Species or multi-locus trees (alternatives)*：ASTRAL。
- *Splits and haplotype networks (alternatives)*：SplitsTree。
- *Tree display (complementary)*：ggtree。
- *Plastid maternal haplotypes (complementary)*：Chloroplast haplotype as a maternal lineage (idea)。

- **BEAST 2**（工具）— 有时间校准时可做贝叶斯树和末端定年。 输入：alignment, priors。输出：trees, dates。版本：2.7.8（GitHub CompEvol/beast2 + Bioconda, 2026-11-14 CST）。 [link](https://www.beast2.org/)  
  注：For aDNA tip-dating use transversions or UDG-treated data.
- **FastTree**（工具）— 超大比对的近似最大似然树，适合先看一眼。 输入：alignment。输出：tree。版本：2.2.0（Bioconda fasttree, 2026-11-14 CST）。 [link](http://www.microbesonline.org/fasttree/)
- **IQ-TREE 2**（工具）— IQ-TREE 的上一主线，仍广泛使用。 输入：SNP alignment。输出：tree。版本：2.4.0（GitHub iqtree/iqtree2 + Bioconda, 2026-11-14 CST）。 [doi:10.1093/molbev/msaa015](https://doi.org/10.1093/molbev/msaa015) · [link](https://github.com/iqtree/iqtree2)  
  注：Listed because many published grape trees used v2; prefer v3 for new work unless a pipeline is pinned.
- **IQ-TREE 3**（工具）— AM23 中的默认最大似然建树工具。 输入：SNP alignment, partitions。输出：tree, model fit。版本：3.1.4（GitHub iqtree/iqtree3 + Bioconda, 2026-11-14 CST）。 [link](https://github.com/iqtree/iqtree3)  
  注：Do not put the IQ-TREE 2 DOI (10.1093/molbev/msaa015) in this row's DOI field. That DOI belongs to IQ-TREE 2 and is recorded only here as a cross-reference. An IQ-TREE 3 paper DOI was not confirmed [待确认].
- **RAxML-NG**（工具）— 备选最大似然搜索，适合较大 SNP 矩阵。 输入：alignment, partition。输出：tree。版本：2.0.4（GitHub amkozlov/raxml-ng + Bioconda, 2026-11-14 CST）。 [link](https://github.com/amkozlov/raxml-ng)
- **TreeMix**（工具）— 群体分裂加迁移边的图模型。 输入：allele counts。输出：graph, residuals。版本：1.12（GitHub joepickrell/treemix + Bioconda, 2026-11-14 CST）。 [doi:10.1371/journal.pgen.1002967](https://doi.org/10.1371/journal.pgen.1002967) · [link](https://github.com/joepickrell/treemix)  
  注：Choose the number of migration edges with OptM and residual plots; clone-prune first.
- **OptM**（工具）— 帮助选择 TreeMix 迁移边的数目。 输入：TreeMix outputs。输出：suggested edge number。版本：0.1.9（CRAN OptM, 2026-11-14 CST）。 [doi:10.1093/biomethods/bpab017](https://doi.org/10.1093/biomethods/bpab017) · [link](https://cran.r-project.org/package=OptM)  
  注：DOI (Fitak 2021) verified by Crossref in the literature review.
- **Twisst**（工具）— 沿基因组做拓扑加权，适合看渗入窗口。 输入：window trees。输出：weights along the genome。版本：0.2（GitHub simonhmartin/twisst, 2026-11-14 CST）。 [link](https://github.com/simonhmartin/twisst)
- **ASTRAL**（工具）— 在多物种溯祖下由无根基因树估计物种树。 输入：gene trees。输出：species tree。版本：5.7.1（GitHub smirarab/ASTRAL + Bioconda, 2026-11-14 CST）。 [link](https://github.com/smirarab/ASTRAL)  
  注：More relevant to Vitaceae family phylogeny than to cultivar SNPs.
- **SplitsTree**（工具）— NeighborNet 等分裂网络，用来表现相互冲突的历史。 输入：alignment or distances。输出：network。版本：[待确认]（Official site; version not checked in this build）。 [link](https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/lehrstuehle/algorithms-in-bioinformatics/software/splitstree/)  
  注：Version [待确认].
- **ggtree**（工具）— 用图形语法绘制树及相关数据。 输入：tree, annotations。输出：plots。版本：[待确认]（Bioconductor; GitHub path not resolved in this check）。 [link](https://bioconductor.org/packages/ggtree/)  
  注：Version [待确认].
- **Chloroplast haplotype as a maternal lineage (idea)**（想法）— 质体单倍型记录母系，是与核基因组独立的一条证据。组装方法见 grapevine-plastid。葡萄属内质体分辨率低，还可能发生叶绿体捕获。 输入：plastid reads or assemblies。输出：haplotype assignments。版本：n/a（genetics review, 2026-11-14 CST）。 [link](https://github.com/Xuzhen-Li/grapevine-plastid)  
  注：Representative Vitis plastid-haplotype papers were not re-checked in this revision [待确认].

<a id="section-4"></a>
## 4. 历史人口学

<!-- PROSE:SECTION:P04 -->
ARG、SMC、SFS 和近期有效种群大小（Ne）估算。克隆和重复样本必须每组仅保留一个。一级亲缘会扭曲近期 Ne 和 LD 估算，进行此类分析时需将其剔除或纳入模型。杂交起源品种在 PSMC 和 MSMC 分析中可能产生虚假的古老 Ne 峰。将结果换算为年份时，必须明确给出世代时间假设（即两次有性世代之间的时间间隔）。对于 ARG 和 SMC 方法，品种的样本时间应设定为其有性起源时间，而非 DNA 提取年份。由于多数品种的起源年代未知，应作为带不确定性的参数，或做敏感性分析，不能设为已知常数。克隆繁殖期间积累的体细胞突变对 SMC 影响甚微，但在 ARG 末端分支上可能表现为极少数过长的分支。
<!-- /PROSE:SECTION:P04 -->

**分组：**
- *ARG methods alternative to the tsinfer/tsdate pair (alternatives)*：Relate, SINGER。
- *tsinfer then tsdate (in order)*：tsdate, tsinfer。
- *Model and observation format (complementary)*：tskit。
- *Recent Ne from LD or IBD (alternatives)*：GONE2, currentNe。
- *SFS and ABC demography (alternatives)*：GADMA, dadi, fastsimcoal2, moments。
- *SFS and ABC demography (complementary)*：demes / demesdraw。
- *SMC-style histories (alternatives)*：MSMC2, PSMC, SMC++。
- *Parameters shared by demographic and ARG methods (complementary)*：Generation time and mutation rate as explicit assumptions (idea), Sexual-origin time as the sample date (idea)。

- **Relate**（工具）— 面向数千样本的全基因组谱系估计，也可供选择检验使用。 输入：phased haplotypes, genetic map。输出：genealogies, coalescence rates。版本：[待确认]（No public tag resolved in this check (MyersGroup/relate returned 404)）。 [doi:10.1038/s41588-019-0484-x](https://doi.org/10.1038/s41588-019-0484-x) · [link](https://myersgroup.github.io/relate/)  
  注：An alternative to the tsinfer-then-tsdate pair, not to tsinfer alone. Version and some setup details [待确认]. Sample time for a cultivar should be its sexual origin.
- **SINGER**（工具）— 带后验抽样的 ARG 推断，作为 tsinfer 加 tsdate 的备选。 输入：phased haplotypes。输出：sampled ARGs。版本：0.1.8-beta（GitHub popgenmethods/SINGER, 2026-11-14 CST (also AM14)）。 [link](https://github.com/popgenmethods/SINGER)  
  注：An alternative to the tsinfer-then-tsdate pair. The listed version string includes beta and is used only because no later stable tag was confirmed in the v1 check [待确认] (whether a later stable tag exists). Sample time for a cultivar should be its sexual origin.
- **tsdate**（工具）— 为 tsinfer 得到的树序列定年。 输入：tree sequence。输出：dated tree sequence。版本：0.2.7（PyPI tsdate, 2026-11-14 CST (also AM14)）。 [link](https://github.com/tskit-dev/tsdate)  
  注：Dates a tree sequence produced by tsinfer; it is the second step of that pair, not an alternative to tsinfer. Sample times should be sexual-origin dates for clonal cultivars.
- **tsinfer**（工具）— 从已定相的大样本推断树序列（ARG 的近似）。 输入：phased genotypes。输出：tree sequence。版本：0.5.1（conda-forge tsinfer, 2026-11-14 CST (also AM14)）。 [doi:10.1038/s41588-019-0483-y](https://doi.org/10.1038/s41588-019-0483-y) · [link](https://github.com/tskit-dev/tsinfer)  
  注：Run tsinfer first, then date the tree sequence with tsdate. Clone-prune and record close kinship first (AM14, project 10). For a cultivar, the sample time should be the sexual origin, not the extraction year.
- **tskit**（工具）— 处理 tsinfer、msprime 或 SLiM 产生的树序列的库。 输入：tree sequence。输出：statistics, subsets。版本：1.0.4（conda-forge/PyPI tskit, 2026-11-14 CST）。 [link](https://github.com/tskit-dev/tskit)
- **GONE2**（工具）— 用连锁不平衡谱推断近期有效种群大小，是 GONE 的后续版本。 输入：genotypes, map。输出：recent Ne。版本：v2.0.2（GitHub esrud/GONE2 release v2.0.2, checked 2026-11-14 CST）。 [link](https://github.com/esrud/GONE2)  
  注：Newest version of this lineage (GONE replaced by GONE2). The model assumes random mating and no strong structure; selfing, clones and population structure violate those assumptions, so clone-prune first and state the assumptions in the write-up. A related contemporary-Ne tool is currentNe.
- **currentNe**（工具）— 估计当代有效种群大小，可与 GONE2 互相对照。 输入：genotypes。输出：contemporary Ne。版本：v1.0.0-1（GitHub esrud/currentNe, only release tag v1.0.0-1, checked 2026-11-14 CST）。 [link](https://github.com/esrud/currentNe)  
  注：The only GitHub tag is v1.0.0-1. Model assumptions (random mating, limited structure) should be stated; clone-prune first. Method DOI [待确认].
- **GADMA**（工具）— 在 dadi、moments 或 fastsimcoal2 之上自动搜索人口学模型结构。 输入：SFS。输出：model, parameters。版本：2.0.3（GitHub ctlab/GADMA + Bioconda/PyPI, 2026-11-14 CST）。 [link](https://github.com/ctlab/GADMA)
- **dadi**（工具）— 用位点频率谱拟合人口学模型。 输入：SFS。输出：model parameters, likelihood。版本：2.0.5（GitHub kern-lab/dadi + Bioconda/PyPI, 2026-11-14 CST）。 [doi:10.1371/journal.pgen.1000695](https://doi.org/10.1371/journal.pgen.1000695) · [link](https://github.com/kern-lab/dadi)
- **fastsimcoal2**（工具）— 在复杂模型下用复合似然做人口学推断，包括位点频率谱。 输入：SFS, model。输出：parameter estimates。版本：[待确认] (Bioconda name not resolved)（Author site; no Bioconda hit in this check）。 [doi:10.1093/bioinformatics/btab468](https://doi.org/10.1093/bioinformatics/btab468) · [link](http://cmpg.unibe.ch/software/fastsimcoal2/)  
  注：Software version [待确认]; the 2021 Bioinformatics paper DOI was verified.
- **moments**（工具）— 基于 SFS 和 LD 的人口学推断，也包括 momentsLD。 输入：SFS or LD statistics。输出：model parameters。版本：1.7.0（GitHub apragsdale/moments + Bioconda/PyPI, 2026-11-14 CST）。 [doi:10.1534/genetics.117.200493](https://doi.org/10.1534/genetics.117.200493) · [link](https://github.com/apragsdale/moments)
- **demes / demesdraw**（工具）— 人口学模型的通用 YAML 格式，并附带绘图。 输入：demes YAML。输出：validated model, plots。版本：demes 0.2.3; demesdraw 0.4.1（PyPI/conda-forge, 2026-11-14 CST）。 [link](https://github.com/popsim-consortium/demes-python)
- **MSMC2**（工具）— 从少量已定相单倍型估计交叉溯祖和有效种群大小。 输入：phased haplotypes, mask。输出：Ne and cross-coalescence。版本：2.1.4（GitHub stschiff/msmc2 + Bioconda, 2026-11-14 CST）。 [doi:10.1038/ng.3015](https://doi.org/10.1038/ng.3015) · [link](https://github.com/stschiff/msmc2)  
  注：The catalogue DOI is Schiffels and Durbin 2014 (MSMC). MSMC2 is the later implementation, described in Schiffels and Wang 2020, 10.1007/978-1-0716-0199-0_7. Hybrid-origin cultivars can produce false old Ne peaks because the two haplotypes come from different source populations. For a clonal cultivar the sample time should be the sexual-origin date, treated as a parameter or a sensitivity analysis when that date is unknown.
- **PSMC**（工具）— 经典的单个二倍体 Ne 历史，可作为基线，但对葡萄的杂合度、ROH 和杂交起源都敏感。 输入：consensus diploid FASTA。输出：Ne trajectory。版本：[待确认] (repo has unusual latest tag fixed-max-t)（GitHub lh3/psmc; Bioconda psmc; tag is not a clean version number）。 [doi:10.1038/nature10231](https://doi.org/10.1038/nature10231) · [link](https://github.com/lh3/psmc)  
  注：Version tag is messy; pin a commit and record it. Highly homozygous lines such as PN40024 are a poor sole input. Hybrid-origin cultivars (for example crosses between eastern and western groups, or with sylvestris introgression) can show a false old Ne peak because the two haplotypes come from different sources. Convert to years only with an explicit generation-time assumption. Clonal propagation does not add meiotic generations; the sample time should be the sexual origin. Tag on GitHub is not a clean version number [待确认].
- **SMC++**（工具）— 从许多未定相基因组推断有效种群大小历史。 输入：VCF, population labels。输出：Ne trajectory。版本：1.15.2（GitHub popgenmethods/smcpp + Bioconda, 2026-11-14 CST）。 [doi:10.1038/ng.3748](https://doi.org/10.1038/ng.3748) · [link](https://github.com/popgenmethods/smcpp)  
  注：Reduce clones and duplicates to one sample per group. For recent Ne, also remove or model first-degree relatives (see docs/WORKFLOW.md). Clone-prune first. Convert to years only with an explicit generation-time assumption. For a clonal cultivar, the sample time should be the sexual origin, not the extraction year. Hybrid-origin diploids can distort the trajectory.
- **Generation time and mutation rate as explicit assumptions (idea)**（想法）— SMC、ARG 和 SFS 模型只有在写明世代时间和突变率之后，才能把结果换算成年份。克隆作物的世代是两次有性世代之间的间隔。种系速率和体细胞速率不是同一个量（见 vitis-open-directions 13 号）。 输入：model output in generations。输出：year-scaled results。版本：n/a（genetics review, 2026-11-14 CST）。  
  注：Numerical values are not recommended here; they need a genetics and statistics review, and a sensitivity analysis [待确认].
- **Sexual-origin time as the sample date (idea)**（想法）— 克隆繁殖的品种在起源之后不再增加减数分裂代数。对 tsdate、Relate、SINGER 和 MSMC2，样本时间应取品种的有性起源时间，而不是抽 DNA 的年份。同一克隆只保留一份。起源年代通常未知，应作为参数或做敏感性分析，不能当成已知常数。克隆期间的体细胞突变可能在 ARG 末端表现为极少数过长的分支。 输入：origin-date estimates。输出：sample-time table。版本：n/a（catalogue revision, 2026-11-14 CST）。  
  注：此处不编造默认的起源年代或突变率。具体数值仍为 [待确认]。

<a id="section-5"></a>
## 5. 选择扫描

<!-- PROSE:SECTION:P05 -->
窗口多样性、单倍型与 CLR 扫描，以及考虑群体结构的离群点扫描。葡萄驯化通常表现为选出单株实生苗后进行克隆繁殖——这属于单次抽样事件，而非经典的多代连续硬清扫；因此硬清扫信号未必出现，软清扫或来自 *sylvestris* 的基因流可能更为常见。驯化瓶颈与杂交起源均易产生假阳性，因此零假设需采用符合葡萄演化历史的模拟数据（diploS/HIC 中已提及这一点）。XP-CLR 和 FST 离群位点反映的是野生群与栽培群之间的分化，本身不能直接等同于选择信号。进行群体对比前需先去除克隆样本，一级亲缘则按流程规定处理。
<!-- /PROSE:SECTION:P05 -->

**分组：**
- *Diversity and differentiation windows (complementary)*：pixy, scikit-allel。
- *Environment and structure-aware outliers (alternatives)*：BayPass, BayeScan, LFMM 2, OutFLANK, pcadapt。
- *Sweep scans, haplotype (alternatives)*：hapFLK, rehh, selscan。
- *Sweep scans, machine learning (alternatives)*：diploS/HIC。
- *Sweep scans, site-frequency or CLR (alternatives)*：RAiSD, SweepFinder2, XP-CLR。

- **pixy**（工具）— 用包含不变位点的全位点 VCF 无偏估计 pi、dxy 和 Fst。 输入：all-sites VCF, population file。输出：window statistics。版本：2.2.5（GitHub ksamuk/pixy 2026-09-18; conda-forge still 2.2.4）。 [doi:10.1111/1755-0998.13326](https://doi.org/10.1111/1755-0998.13326) · [link](https://github.com/ksamuk/pixy)  
  注：Newest GitHub is 2.2.5; conda-forge lagged at 2.2.4. AM11 still recorded 2.2.4.
- **scikit-allel**（工具）— 用于窗口多样性、Fst、Patterson f 统计和绘图的 Python 库。 输入：VCF or zarr。输出：statistics, plots。版本：1.3.13（GitHub cggh/scikit-allel + Bioconda/PyPI, 2026-11-14 CST）。 [link](https://github.com/cggh/scikit-allel)
- **BayPass**（工具）— 贝叶斯 XtX 分化和基因型-环境关联。 输入：allele counts, covariates。输出：XtX, association。版本：3.1（Bioconda baypass, 2026-11-14 CST）。 [doi:10.1534/genetics.115.181453](https://doi.org/10.1534/genetics.115.181453) · [link](https://forgemia.inra.fr/gguirao/baypass)  
  注：Current official URL should be re-checked if the Forge moves [待确认].
- **BayeScan**（工具）— 较早的 Fst 离群贝叶斯扫描，仅作为对照保留。 输入：allele counts。输出：outlier q-values。版本：2.1（Bioconda bayescan, 2026-11-14 CST）。 [link](http://www.cmpg.unibe.ch/software/BayeScan/)  
  注：Prefer pcadapt, OutFLANK or BayPass for new work.
- **LFMM 2**（工具）— 用潜在因子混合模型做基因型-环境关联。 输入：genotypes, environmental variables。输出：association p-values。版本：1.1（GitHub bcm-uga/lfmm tag 1.1; Caye et al. 2019 paper verified）。 [doi:10.1093/molbev/msz008](https://doi.org/10.1093/molbev/msz008) · [link](https://github.com/bcm-uga/lfmm)  
  注：Also listed under section 9. Version source: GitHub bcm-uga/lfmm 1.1; also packaged in Bioconductor LEA.
- **OutFLANK**（工具）— 用位点之间修剪后的空分布做 Fst 离群检验。 输入：Fst per locus。输出：outliers。版本：[待确认]（GitHub whitlock/OutFLANK; no tag in this check）。 [link](https://github.com/whitlock/OutFLANK)  
  注：Version [待确认].
- **pcadapt**（工具）— 基于 PCA 的选择离群扫描，对部分群体结构较稳健。 输入：genotypes。输出：outlier p-values。版本：4.4.1（CRAN pcadapt, 2026-11-14 CST）。 [doi:10.1111/1755-0998.12592](https://doi.org/10.1111/1755-0998.12592) · [link](https://github.com/bcm-uga/pcadapt)
- **hapFLK**（工具）— 考虑群体结构的单倍型 Fst，适合品种组之间的对比。 输入：haplotypes, kinship or tree。输出：hapFLK scores。版本：2.1（PyPI hapflk 2.1 (2024-05-16), 2026-11-14 CST; official source INRAE Forge）。 [doi:10.1534/genetics.112.147231](https://doi.org/10.1534/genetics.112.147231) · [link](https://forgemia.inra.fr/bertrand.servin/hapflk)  
  注：The previous GitHub URL bioinfo-lessmieux/hapflk returned 404 (checked 2026-11-14). Version source is PyPI 2.1; the Forge page may require a login. Bioconda version [待确认]. DOI is Fariello et al. 2013.
- **rehh**（工具）— 基于 EHH 的扫描和作图的 R 实现。 输入：haplotypes。输出：iHS, XP-EHH, plots。版本：3.2.3（CRAN rehh, 2026-11-14 CST）。 [link](https://cran.r-project.org/package=rehh)
- **selscan**（工具）— iHS、nSL、XP-EHH 及相关单倍型扫描，2.0 以后也包括未定相扫描。 输入：haplotypes or unphased genotypes, map。输出：scan scores。版本：3.1.0（GitHub szpiech/selscan + Bioconda, 2026-11-14 CST）。 [doi:10.1093/bioinformatics/btae006](https://doi.org/10.1093/bioinformatics/btae006) · [link](https://github.com/szpiech/selscan)  
  注：DOI is Szpiech 2024 (selscan 2.0). Original 2014 paper is doi:10.1093/molbev/msu211. Newest tag is 3.1.0.
- **diploS/HIC**（工具）— 用窗口特征区分硬扫、软扫和连锁区域，需用模拟来训练。 输入：genotypes, trained model。输出：sweep classes。版本：1.1.0（GitHub kern-lab/diploSHIC + Bioconda, 2026-11-14 CST）。 [link](https://github.com/kern-lab/diploSHIC)  
  注：Train on grape-like demography and clonality; off-the-shelf human models are not appropriate.
- **RAiSD**（工具）— 由 mu、mu-var 和 mu-SFS 组成的复合选择扫描统计，已列入 AM11。 输入：VCF or FASTA-like。输出：outlier windows。版本：[待确认] (no tagged release)（GitHub alachins/raisd exists (updated 2026-11-04) but no tag in this check）。 [doi:10.1038/s42003-018-0085-8](https://doi.org/10.1038/s42003-018-0085-8) · [link](https://github.com/alachins/raisd)  
  注：Version remains [待确认], as in AM11.
- **SweepFinder2**（工具）— 可纳入人口学背景 SFS 的 CLR 选择扫描。 输入：allele frequencies, background SFS。输出：CLR scores。版本：1.0（Bioconda sweepfinder2, 2026-11-14 CST）。 [link](https://degiorgioroup.github.io/Website/computer.html)  
  注：Official URL should be confirmed against the current lab page [待确认] (if the URL moves).
- **XP-CLR**（工具）— 跨群体复合似然比扫描，例如去克隆后的野生与栽培对比。 输入：allele frequencies, map。输出：XP-CLR scores。版本：1.1.2（GitHub hardingnj/xpclr + Bioconda, 2026-11-14 CST (also AM11)）。 [doi:10.1101/gr.100545.109](https://doi.org/10.1101/gr.100545.109) · [link](https://github.com/hardingnj/xpclr)

<a id="section-6"></a>
## 6. 渗入与 f 统计

<!-- PROSE:SECTION:P06 -->
f 统计量、混合图和杂交检验，与 TreeMix 和局部祖源分析互为补充。D 统计量不等于 0 也可能源于祖先群体结构，未必代表基因流。f3 为负才是混合的证据；但 f3 非负并不能排除混合，因为目标群体自身的遗传漂变会掩盖信号。在检验混合之前，应先依据地理分布或利用类型定义群体，切勿根据待检验的混合信号来划分群体。当以伪单倍体古样本作为 f3 的目标群体时，杂合度项需另行处理。
<!-- /PROSE:SECTION:P06 -->

**分组：**
- *Admixture date and painting (complementary)*：TreeMix。
- *Hybrid detection (alternatives)*：HyDe。
- *f-statistics and graphs (alternatives)*：ADMIXTOOLS (qpDstat, qp3Pop, qpAdm, qpGraph), ADMIXTOOLS 2, Dsuite。
- *Foundational f-statistic papers (complementary)*：Green et al. 2010 D statistic, Durand et al. 2011 D statistic, Reich et al. 2009 f-statistics, Peter 2016 f-statistics, Haak et al. 2015 qpAdm, Harney et al. 2021 qpAdm performance。

- **TreeMix**（工具）— 群体树上的迁移边，与 f 统计图互为补充。 输入：allele counts。输出：graph, residuals。版本：1.12（see section 3）。 [doi:10.1371/journal.pgen.1002967](https://doi.org/10.1371/journal.pgen.1002967) · [link](https://github.com/joepickrell/treemix)  
  注：Same binary as section 3; listed here for the introgression workflow.
- **HyDe**（工具）— 用位点模式检验系统发育三元组中的杂交。 输入：alignment, triples。输出：hybridisation p-values。版本：1.0.2（GitHub pblischak/HyDe + Bioconda, 2026-11-14 CST）。 [link](https://github.com/pblischak/HyDe)
- **ADMIXTOOLS (qpDstat, qp3Pop, qpAdm, qpGraph)**（工具）— Patterson f 统计和混合图工具的原始 C 实现。 输入：EIGENSTRAT or PACKEDANCESTRYMAP。输出：f-statistics, qpAdm, graphs。版本：8.0.2（GitHub DReichLab/AdmixTools + Bioconda, 2026-11-14 CST）。 [doi:10.1534/genetics.112.145037](https://doi.org/10.1534/genetics.112.145037) · [link](https://github.com/DReichLab/AdmixTools)  
  注：DOI is Patterson et al. 2012. Prefer ADMIXTOOLS 2 for new analyses unless a pipeline is pinned to the C binary.
- **ADMIXTOOLS 2**（工具）— 在 R 中计算 f2、f3、f4、qpAdm 和 qpGraph，并做区组刀切。 输入：genotype or f2 blocks。输出：f-statistics, admixture graphs。版本：2.0.1（GitHub uqrmaie1/admixtools v2.0.1, 2026-11-14 CST (also AM13)）。 [doi:10.7554/elife.85492](https://doi.org/10.7554/elife.85492) · [link](https://github.com/uqrmaie1/admixtools)  
  注：Default alternative in AM13. Maier et al. 2023 eLife DOI verified.
- **Dsuite**（工具）— 快速计算 D、f4 比值和 f-branch，并做区组刀切。 输入：VCF, tree or trio file。输出：D, f4, f-branch tables。版本：[待确认] (no tagged release)（GitHub millanek/Dsuite; no tag or Bioconda package in this check (same as AM13)）。 [doi:10.1111/1755-0998.13265](https://doi.org/10.1111/1755-0998.13265) · [link](https://github.com/millanek/Dsuite)  
  注：Version remains [待确认], as in AM13. The 2021 paper DOI was verified.
- **Green et al. 2010 D statistic**（文献）— 介绍 ABBA-BABA 检验中 D 统计量的尼安德特基因组论文。 输入：n/a。输出：n/a。版本：n/a（Crossref-verified in the literature review, 2026-11-14 CST）。 [doi:10.1126/science.1188021](https://doi.org/10.1126/science.1188021) · [link](https://doi.org/10.1126/science.1188021)  
  注：Literature addition; wording is deliberately general.
- **Durand et al. 2011 D statistic**（文献）— D 统计量的形式性质。 输入：n/a。输出：n/a。版本：n/a（Crossref-verified in the literature review, 2026-11-14 CST）。 [doi:10.1093/molbev/msr048](https://doi.org/10.1093/molbev/msr048) · [link](https://doi.org/10.1093/molbev/msr048)  
  注：Literature addition; wording is deliberately general.
- **Reich et al. 2009 f-statistics**（文献）— 介绍 f3 和 f4 统计量。 输入：n/a。输出：n/a。版本：n/a（Crossref-verified in the literature review, 2026-11-14 CST）。 [doi:10.1038/nature08365](https://doi.org/10.1038/nature08365) · [link](https://doi.org/10.1038/nature08365)  
  注：Literature addition; wording is deliberately general.
- **Peter 2016 f-statistics**（文献）— 在群体结构和混合情形下如何解释 f2、f3 和 f4。 输入：n/a。输出：n/a。版本：n/a（Crossref-verified in the literature review, 2026-11-14 CST）。 [doi:10.1534/genetics.115.183913](https://doi.org/10.1534/genetics.115.183913) · [link](https://doi.org/10.1534/genetics.115.183913)  
  注：Literature addition; wording is deliberately general.
- **Haak et al. 2015 qpAdm**（文献）— 常被当作 qpAdm 来源引用的草原迁徙研究（方法在补充材料中，本次未重读）。 输入：n/a。输出：n/a。版本：n/a（Crossref-verified in the literature review, 2026-11-14 CST）。 [doi:10.1038/nature14317](https://doi.org/10.1038/nature14317) · [link](https://doi.org/10.1038/nature14317)  
  注：Literature addition; wording is deliberately general.
- **Harney et al. 2021 qpAdm performance**（文献）— 关于 qpAdm 检验力和假阳性的模拟研究。 输入：n/a。输出：n/a。版本：n/a（Crossref-verified in the literature review, 2026-11-14 CST）。 [doi:10.1093/genetics/iyaa045](https://doi.org/10.1093/genetics/iyaa045) · [link](https://doi.org/10.1093/genetics/iyaa045)  
  注：Literature addition; wording is deliberately general.

<a id="section-7"></a>
## 7. 连锁不平衡与重组

<!-- PROSE:SECTION:P07 -->
优先使用插值到工作参考基因组上的已发表葡萄连锁图。基于 LD 推断的遗传图仅作为 ARG 输入，不用于 SHAPEIT5 定相（AM26）。克隆繁殖本身不会改变 LD；真正导致估计偏倚的因素包括重复样本、亲缘关系、近交（有效重组率约为 r(1 − F)）以及群体混合。使用 est-sfs 进行等位基因极化归于第 10 节，因为它是遗传负荷、DFE 和 ARG 分析的前置步骤，而非连锁分析方法。
<!-- /PROSE:SECTION:P07 -->

**分组：**
- *LD decay and blocks (complementary)*：LDBlockShow, PopLDdecay。
- *LD-based recombination maps (alternatives, ARG input only)*：LDhelmet, ReLERNN, pyrho。

- **LDBlockShow**（工具）— 候选位点附近的 LD 热图和单倍型块。 输入：VCF, region。输出：plots, blocks。版本：1.41（GitHub BGI-shenzhen/LDBlockShow + Bioconda, 2026-11-14 CST）。 [link](https://github.com/BGI-shenzhen/LDBlockShow)
- **PopLDdecay**（工具）— 按群体画 LD 衰减曲线，去克隆后的标准第一张图。 输入：VCF。输出：decay tables, plots。版本：3.45（GitHub BGI-shenzhen/PopLDdecay + Bioconda, 2026-11-14 CST）。 [link](https://github.com/BGI-shenzhen/PopLDdecay)
- **LDhelmet**（工具）— 备选的基于 LD 的图谱，速度较慢，仅在 pyrho 不合适时使用。 输入：phased haplotypes。输出：recombination map。版本：1.10（Bioconda ldhelmet, 2026-11-14 CST (also AM26)）。 [link](https://sourceforge.net/projects/ldhelmet/)  
  注：AM26 alternative to pyrho.
- **ReLERNN**（工具）— 用模拟训练的循环网络估计重组；在葡萄上视为试验性方法。 输入：genotypes, simulations。输出：recombination map。版本：2.0.0（GitHub kr-colab/ReLERNN + Bioconda, 2026-11-14 CST）。 [link](https://github.com/kr-colab/ReLERNN)  
  注：Train on grape-like demography; do not reuse a human model.
- **pyrho**（工具）— 基于 LD 的重组率。AM26 中只把它当作 ARG 的输入，不用来给 SHAPEIT5 定相。 输入：phased haplotypes, Ne history。输出：recombination map。版本：0.2.1（Bioconda pyrho, 2026-11-14 CST (also AM26)）。 [doi:10.1126/sciadv.aaw9206](https://doi.org/10.1126/sciadv.aaw9206) · [link](https://github.com/popgenmethods/pyrho)  
  注：Run per population after clone and first-degree pruning. See AM26 for why clonality and admixture LD bias rho.

<a id="section-8"></a>
## 8. 纯合片段、近交、亲缘与无性系

<!-- PROSE:SECTION:P08 -->
无性系并不仅仅是分析中的干扰项：基因型被冻结，不发生分离和重组，体细胞变异随时间逐步积累，嵌合体还可以在不同细胞层（L1/L2）中分层。ROH 长度的含义仍然成立：长 ROH 源于近期的近亲交配或自交（两性花品种可自交，PN40024 即为自交系），短 ROH 则反映古老的群体瓶颈。克隆繁殖本身不会产生 ROH。身份核对的结果会传递至后续每一节；克隆和一级亲缘的处理方式不同。
<!-- /PROSE:SECTION:P08 -->

**分组：**
- *Kinship, IBD and clonality (complementary)*：GCTA, KING, VIVC, ngsRelate。
- *ROH callers (alternatives)*：GARLIC, RZooRoH, bcftools roh。
- *ROH callers, low coverage (alternatives)*：hapROH, ROHan。
- *Low-coverage kinship (complementary)*：READv2, KIN (KINgaroo), BREADR。

- **GCTA**（工具）— 基于 GRM 的亲缘和 GBLUP，也可用于 GWAS（第 9 节）。 输入：BED。输出：GRM, heritability。版本：1.94.1（GitHub jianyangqt/gcta + Bioconda, 2026-11-14 CST）。 [link](https://yanglab.westlake.edu.cn/software/gcta/)
- **KING**（工具）— 用于区分克隆/重复与一级亲缘的稳健亲缘估计。克隆和重复（亲缘系数高于 0.354）每组只留一个样本；一级亲缘（0.177-0.354）只登记，不当作同一基因型删掉。 输入：hard-called diploid genotypes (BED)。输出：kinship。版本：2.3.2（see section 1）。 [doi:10.1093/bioinformatics/btq559](https://doi.org/10.1093/bioinformatics/btq559) · [link](https://www.kingrelatedness.com/)  
  注：Thresholds follow the KING manual (https://www.kingrelatedness.com/manual.shtml): kinship above 0.354 is the duplicate/MZ class; 0.177-0.354 is first-degree. Paper: Manichaikul et al. 2010, 10.1093/bioinformatics/btq559. AM26 used 0.177 as the first-degree lower cutoff. Input should be hard-called diploid genotypes (BED). For low-coverage or ancient samples use ngsRelate, READv2, KIN or BREADR instead. Handling of first-degree relatives is analysis-specific; see docs/WORKFLOW.md.
- **VIVC**（资源）— 公开的品种名称登记库，与 KING 一起把基因型对应到现用名称（AM04）。 输入：cultivar names。输出：accepted names, synonyms。版本：n/a (live database)（vivc.de, checked as the public cultivar name registry）。 [link](https://www.vivc.de/)  
  注：Not software. Do not upload unpublished genotype matrices to this repository.
- **ngsRelate**（工具）— 用基因型似然估计亲缘，适用于低覆盖度数据。 输入：ANGSD genotype likelihoods。输出：relatedness。版本：2.3.1（GitHub ANGSD/NgsRelate + Bioconda, 2026-11-14 CST）。 [doi:10.1093/gigascience/giz034](https://doi.org/10.1093/gigascience/giz034) · [link](https://github.com/ANGSD/NgsRelate)
- **GARLIC**（工具）— 显式建模长度类别的 ROH 检测器。 输入：BED or genotypes。输出：ROH classes。版本：1.1.6（GitHub szpiech/garlic + Bioconda, 2026-11-14 CST）。 [link](https://github.com/szpiech/garlic)
- **RZooRoH**（工具）— 用隐马尔可夫模型把基因组划分成多个同源结合（HBD）类别。 输入：genotypes。输出：ROH classes, inbreeding。版本：0.4.3（CRAN RZooRoH, 2026-11-14 CST）。 [link](https://cran.r-project.org/package=RZooRoH)
- **bcftools roh**（工具）— 用隐马尔可夫模型检测纯合片段。AM12 使用去克隆后按群体估计的等位基因频率，而不是默认频率文件。 输入：VCF, population AF file。输出：ROH tables。版本：1.25（same bcftools 1.25 as section 1; also AM12）。 [doi:10.1093/bioinformatics/btw044](https://doi.org/10.1093/bioinformatics/btw044) · [link](https://github.com/samtools/bcftools)  
  注：Default ROH tool in AM12. ROH method paper: Narasimhan et al. 2016, 10.1093/bioinformatics/btw044. The samtools/bcftools suite DOI 10.1093/gigascience/giab008 still applies to the package.
- **hapROH**（工具）— 借助单倍型参考面板，从低覆盖度数据检测 ROH。按人类数据（1240k / 千人基因组面板）开发和测试。不能用来推断无性系历史：克隆繁殖不产生 ROH。 输入：pseudo-haploid or low-coverage genotypes, reference panel。输出：ROH, inbreeding。版本：0.70（GitHub/PyPI hapROH 0.70; Bioconda 0.64）。 [doi:10.1038/s41467-021-25289-w](https://doi.org/10.1038/s41467-021-25289-w) · [link](https://github.com/hringbauer/hapROH)  
  注：Human-specific as distributed. Use on Vitis only after building a Vitis phased haplotype panel and validating on modern grapes downsampled to the target depth; unvalidated results must not be reported. ROH reflects inbreeding at the sexual origin of the sampled genotype, not centuries of clonal propagation. Prefer species-general ROHan, or bcftools roh when depth is sufficient. Newest is 0.70 on GitHub/PyPI; Bioconda lagged at 0.64.
- **ROHan**（工具）— 从单个 BAM 联合估计杂合度和 ROH，可做损伤校正，不依赖人类单倍型面板。可作为 hapROH 的物种通用替代。原文摘要给出的可用覆盖度为：现代样本低至 5−6 倍，有中等损伤的古代样本低至 7−8 倍。 输入：BAM。输出：heterozygosity and ROH tracts。版本：v1.0.7（GitHub grenaud/ROHan release v1.0.7, checked 2026-11-14 CST）。 [doi:10.1534/genetics.119.302057](https://doi.org/10.1534/genetics.119.302057) · [link](https://github.com/grenaud/ROHan)  
  注：ROH still reflects inbreeding at sexual origin, not clonal history.
- **READv2**（工具）— 用伪单倍型低覆盖数据的两两错配率估计亲缘（可到三级）。按人类数据开发，用于葡萄时要用降到相同深度的现代克隆对和亲缘对校准。Noraz 等 2026（doi:10.1038/s41467-026-70166-z）曾用 VIVC 为葡萄克隆做过校准，已在 2026-11-14 的文献复审中对照该文确认。 输入：pseudo-haploid PLINK or EIGENSTRAT。输出：relatedness class。版本：2.1.1（GitHub GuntherLab/READv2 release 2.1.1, checked 2026-11-14 CST）。 [doi:10.1186/s13059-024-03350-3](https://doi.org/10.1186/s13059-024-03350-3) · [link](https://github.com/GuntherLab/READv2)  
  注：This is the current READ lineage; the original READ paper (10.1371/journal.pone.0195491) is not a second tool entry.
- **KIN (KINgaroo)**（工具）— 用隐马尔可夫模型从低覆盖数据识别 IBD 片段（人类测试中可到约 0.05 倍），可选污染校正和 ROH 模型。用于葡萄需要校准。 输入：BAM via KINgaroo。输出：relatedness class and IBD segments。版本：v3.1.4（GitHub DivyaratanPopli/Kinship_Inference release v3.1.4, checked 2026-11-14 CST）。 [doi:10.1186/s13059-023-02847-7](https://doi.org/10.1186/s13059-023-02847-7) · [link](https://github.com/DivyaratanPopli/Kinship_Inference)
- **BREADR**（工具）— 针对极低覆盖伪单倍型数据，给出 identical/twins、一级、二级或无关的后验概率。校准后，identical 类可用于古籽与现存品种的克隆匹配。 输入：EIGENSTRAT。输出：relatedness-class posteriors。版本：1.1.0（CRAN BREADR 1.1.0, checked 2026-11-14 CST）。 [doi:10.32614/CRAN.package.BREADR](https://doi.org/10.32614/CRAN.package.BREADR) · [link](https://cran.r-project.org/package=BREADR)

<a id="section-9"></a>
## 9. 全基因组关联、遗传-环境关联与景观基因组学

<!-- PROSE:SECTION:P09 -->
混合模型 GWAS、作物平台、荟萃分析、基因组预测及基因型-环境关联分析。
<!-- /PROSE:SECTION:P09 -->

**分组：**
- *GEA and landscape genomics (alternatives)*：BayPass, LFMM 2, dartR, wingen。
- *Meta-analysis and prediction (complementary)*：BGLR, LDSC, METAL, metafor, rrBLUP。
- *Mixed-model GWAS (alternatives)*：GEMMA, SAIGE, regenie。
- *Plant GWAS platforms (alternatives)*：GAPIT, TASSEL, rMVP。

- **BayPass**（工具）— 贝叶斯遗传-环境关联和分化，与第 5 节为同一工具。 输入：allele counts, covariates。输出：XtX, association。版本：3.1（see section 5）。 [doi:10.1534/genetics.115.181453](https://doi.org/10.1534/genetics.115.181453) · [link](https://forgemia.inra.fr/gguirao/baypass)
- **LFMM 2**（工具）— 带潜在因子的基因型-环境关联。 输入：genotypes, environment。输出：association。版本：1.1（see section 5）。 [doi:10.1093/molbev/msz008](https://doi.org/10.1093/molbev/msz008) · [link](https://github.com/bcm-uga/lfmm)  
  注：Same tool as section 5. Same 1.1 line as the LFMM 2 row in section 5.
- **dartR**（工具）— 面向 SNP 群体遗传和部分景观分析的 R 工具包，最初围绕 DArT 数据。 输入：genotypes。输出：diversity, structure, plots。版本：2.7.2（GitHub green-striped-gecko/dartR, 2026-11-14 CST）。 [link](https://github.com/green-striped-gecko/dartR)
- **wingen**（工具）— 由带地理坐标的样本绘制基因组多样性和适应性变异。 输入：genotypes, public coordinates。输出：maps。版本：2.2.0（CRAN wingen, 2026-11-14 CST）。 [link](https://cran.r-project.org/package=wingen)  
  注：Public coordinates only.
- **BGLR**（工具）— 贝叶斯基因组预测。 输入：markers, phenotypes。输出：GEBV, accuracy。版本：1.1.4（CRAN BGLR, 2026-11-14 CST (also AM24)）。 [link](https://cran.r-project.org/package=BGLR)  
  注：AM24: one sample per clone or duplicate group; keep clones, and first-degree relatives, in the same cross-validation fold.
- **LDSC**（工具）— 用 LD score 截距看膨胀和样本重叠（AM24）。 输入：summary statistics, LD scores。输出：intercepts, heritability。版本：1.0.1（Bioconda ldsc 1.0.1; GitHub tag still v1.0.0）。 [link](https://github.com/bulik/ldsc)  
  注：AM24: use only above a minimum number of SNPs and samples fixed in advance. Human-style LD scores are not a grape map.
- **METAL**（工具）— 固定效应 GWAS 荟萃分析，AM24 默认工具。 输入：summary statistics。输出：meta-analysis table。版本：2020-05-05（GitHub statgen/METAL, 2026-11-14 CST (also AM24)）。 [link](https://github.com/statgen/METAL)
- **metafor**（工具）— 研究数目较少时用的随机效应荟萃分析（REML，Hartung–Knapp）。 输入：effect sizes。输出：pooled estimates。版本：5.2-1（CRAN metafor, 2026-11-14 CST (also AM24)）。 [link](https://cran.r-project.org/package=metafor)  
  注：AM24 uses this when fewer than five studies.
- **rrBLUP**（工具）— 岭回归 / GBLUP 基因组预测，AM24 备选。 输入：markers, phenotypes。输出：GEBV, accuracy。版本：4.6.3（CRAN rrBLUP, 2026-11-14 CST (also AM24)）。 [link](https://cran.r-project.org/package=rrBLUP)
- **GEMMA**（工具）— 线性混合模型 GWAS，AM24 中每个研究的默认工具。 输入：BED, phenotypes, relatedness。输出：association, PVE。版本：0.98.5（GitHub genetics-statistics/GEMMA + Bioconda, 2026-11-14 CST (also AM24)）。 [doi:10.1038/ng.2310](https://doi.org/10.1038/ng.2310) · [link](https://github.com/genetics-statistics/GEMMA)  
  注：Keep clones in the same cross-validation fold (AM24).
- **SAIGE**（工具）— 鞍点近似混合模型 GWAS，主要用于二元性状。 输入：genotypes, phenotypes。输出：association。版本：0.29.5（GitHub weizhouUMICH/SAIGE, 2026-11-14 CST）。 [link](https://github.com/weizhouUMICH/SAIGE)  
  注：More common in human data; usable if a grape trait is binary and sample size is large.
- **regenie**（工具）— 快速全基因组回归 GWAS，AM24 中 GEMMA 的备选。 输入：BED/PGEN, phenotypes。输出：association。版本：4.1.3.1（Bioconda regenie 4.1.3.1; GitHub tag v4.1.3 (2026-09-08)）。 [doi:10.1038/s41588-021-00870-7](https://doi.org/10.1038/s41588-021-00870-7) · [link](https://github.com/rgcgithub/regenie)  
  注：Bioconda has a patch letter (4.1.3.1) on top of GitHub v4.1.3.
- **GAPIT**（工具）— 封装 FarmCPU、BLINK、MLMM 等作物 GWAS 方法的 R 平台。 输入：genotypes, phenotypes。输出：association, plots。版本：GAPIT4 (GitHub tag GAPIT4)（GitHub jiabowang/GAPIT3 tag GAPIT4, 2026-11-14 CST）。 [link](https://github.com/jiabowang/GAPIT3)  
  注：Repository name still says GAPIT3; newest tag is GAPIT4. Record the exact tag you run.
- **TASSEL**（工具）— 沿用已久的作物图形界面和命令行 GWAS 与多样性工具。 输入：genotypes, phenotypes。输出：association, PCA, Kinship。版本：[待确认]（Official site; version not checked in this build）。 [link](https://www.maizegenetics.net/tassel)  
  注：Version [待确认].
- **rMVP**（工具）— 省内存的作物 GWAS 和曼哈顿图。 输入：genotypes, phenotypes。输出：association, plots。版本：1.0.4（CRAN rMVP, 2026-11-14 CST）。 [link](https://github.com/xiaolei-lab/rMVP)

<a id="section-10"></a>
## 10. 遗传负荷与有害突变

<!-- PROSE:SECTION:P10 -->
变异效应注释、向衍生等位基因极化，以及分别报告纳入和不纳入 ROH 协变量的遗传负荷（AM12）。遗传负荷应按衍生等位基因统计，而不是按非参考等位计，因为参考等位基因并不等同于祖先等位基因。参考基因组是一个个体的单倍型，若按非参考等位基因统计，该个体自身携带的有害衍生等位基因就会被遗漏。这一逻辑并不依赖于 PN40024 接近纯合的事实；纯合仅说明该参考基因组近似于单一单倍型。群体数据测得的主要是有性起源时遗传下来的种系负荷，而克隆繁殖期间积累的体细胞负荷属于另一独立指标（见 vitis-open-directions 13 号、16 号）。半合子和杂合（被掩盖）的隐性负荷应分开报告。
<!-- /PROSE:SECTION:P10 -->

**分组：**
- *Polarisation (before DFE, load and ARG) (in order)*：est-sfs。
- *Distribution of fitness effects (alternatives)*：Grapes (DFE), polyDFE。
- *Variant-effect annotation (alternatives)*：Ensembl VEP, PlantCaduceus, SnpEff。

- **est-sfs**（工具）— 用多个外类群做祖先状态的概率估计。 输入：outgroup bases, site counts。输出：ancestral probabilities。版本：2.04（AM26 (2026-11-14); not re-checked against a public tag in this session）。 [link](https://sourceforge.net/projects/est-usfs/)  
  注：Polarisation is a prerequisite for unfolded DFE, load and ARG work, not an LD tool. Use two or more outgroups, never Muscadinia alone (AM26).
- **Grapes (DFE)**（工具）— 用 SNP 计数拟合 gamma 等 DFE 模型。软件名不是作物葡萄。 输入：site counts。输出：DFE parameters。版本：v1.1.1（GitHub BioPP/grapes release v1.1.1, checked 2026-11-14 CST）。 [doi:10.1371/journal.pgen.1005774](https://doi.org/10.1371/journal.pgen.1005774) · [link](https://github.com/BioPP/grapes)  
  注：Official repository is BioPP/grapes (Galtier 2016). The previous GitHub URL bioinfo-lessmieux/grapes returned 404. Whether conda-forge package grapes 0.10.4 is the same software remains [待确认]; it is not used as the catalogue version.
- **polyDFE**（工具）— 从折叠或未折叠的 SFS 估计适应度效应分布。 输入：SFS, optionally polarised。输出：DFE parameters。版本：2.0（GitHub paula-tataru/polyDFE tag v2.0, 2026-11-14 CST）。 [link](https://github.com/paula-tataru/polyDFE)  
  注：Polarise as in AM26 before unfolded analyses.
- **Ensembl VEP**（工具）— 备选效应预测器；Ensembl Plants 缓存必须与所选葡萄组装一致。 输入：VCF, cache。输出：annotated VCF or TSV。版本：116.3（GitHub Ensembl/ensembl-vep release/116.3, 2026-11-14 CST）。 [link](https://github.com/Ensembl/ensembl-vep)  
  注：Confirm that a Vitis cache exists for the assembly you use [待确认] (cache).
- **PlantCaduceus**（工具）— 可选的植物变异效应打分，AM12 中列为试验性方法。 输入：variants, model。输出：scores。版本：[待确认]（plantcad/plantcad-dev exists (updated 2026-04-23); no stable tag in this check (also AM12)）。 [link](https://github.com/plantcad/plantcad-dev)  
  注：Version [待确认]. Do not treat unpublished model weights as a repo file.
- **SnpEff**（工具）— 用所选葡萄注释构建的本地数据库给变异做注释（AM12：DS01）。 输入：VCF, SnpEff database。输出：annotated VCF。版本：5.4.0c（Bioconda snpeff 5.4.0c; GitHub tag v5.4c (also AM12)）。 [doi:10.4161/fly.19695](https://doi.org/10.4161/fly.19695) · [link](https://pcingola.github.io/SnpEff/)  
  注：Count load on derived alleles after polarisation (AM26), not on non-reference alleles, because the reference allele is not the ancestral allele.

<a id="section-11"></a>
## 11. 结构变异与泛基因组图群体遗传

<!-- PROSE:SECTION:P11 -->
这里只放指针：图的构建和完整工具名单在 vitis-pangenome。长读长结构变异检测工具与检测后的合并步骤分开列出；本节不包含短读长结构变异目录。
<!-- /PROSE:SECTION:P11 -->

**分组：**
- *SV merging across samples (in order, after calling)*：Jasmine。
- *Long-read SV calling (alternatives)*：Sniffles2, cuteSV。
- *Graph genotyping (alternatives; details live in vitis-pangenome)*：PanGenie, vg (Giraffe + vg call)。
- *Graph statistics (complementary)*：odgi。

- **Jasmine**（工具）— 在各样本检测完成之后，合并多样本结构变异结果。 输入：per-sample SV VCF。输出：merged SV VCF。版本：1.1.5（GitHub mkirsche/Jasmine v1.1.5; Bioconda 1.1 (AM18 recorded 1.1)）。 [link](https://github.com/mkirsche/Jasmine)  
  注：This is a downstream merge step, not an alternative caller. Use it after Sniffles2 or cuteSV, not as a substitute for them. Short-read SV callers are not listed here; see vitis-pangenome.
- **Sniffles2**（工具）— 本节的默认长读结构变异检测器。 输入：long-read BAM。输出：SV VCF。版本：2.8.1（GitHub fritzsedlazeck/Sniffles + Bioconda, 2026-11-14 CST (also AM18)）。 [link](https://github.com/fritzsedlazeck/Sniffles)  
  注：Long-read caller, not a short-read tool. Details and short-read SV methods live in vitis-pangenome.
- **cuteSV**（工具）— 备选的长读结构变异检测器。 输入：long-read BAM。输出：SV VCF。版本：2.1.4（GitHub tjiangHIT/cuteSV + Bioconda, 2026-11-14 CST (also AM18)）。 [link](https://github.com/tjiangHIT/cuteSV)  
  注：Long-read caller, not a short-read tool. Details and short-read SV methods live in vitis-pangenome.
- **PanGenie**（工具）— 对已经在泛基因组图中的变异做 k-mer 分型。 输入：short reads, graph or haplotypes。输出：VCF。版本：4.2.2（GitHub eblerjana/pangenie, 2026-11-14 CST (also AM07)）。 [link](https://github.com/eblerjana/pangenie)  
  注：Pointer: vitis-pangenome section 5.
- **vg (Giraffe + vg call)**（工具）— 把读段比对到泛基因组图上，并对图中的变异分型。 输入：reads, graph。输出：BAM-like GAM, VCF。版本：1.78.0（GitHub vgteam/vg, 2026-11-14 CST (also AM07, AM17)）。 [link](https://github.com/vgteam/vg)  
  注：Do not duplicate the vitis-pangenome catalogue here. Use that repository for graph construction.
- **odgi**（工具）— 图统计和路径相似性，是面向图的群体遗传的起点。 输入：odgi/gfa graph。输出：stats, matrices。版本：0.9.4（GitHub pangenome/odgi + Bioconda, 2026-11-14 CST (also AM07)）。 [link](https://github.com/pangenome/odgi)  
  注：Pointer: vitis-pangenome. Projects 15–17 in vitis-open-directions develop graph introgression, SV load and inversions.

<a id="section-12"></a>
## 12. 模拟

<!-- PROSE:SECTION:P12 -->
溯祖模拟器与前向模拟器，涵盖 SLiM 中的克隆世代模拟。目前尚未确认存在正式的葡萄 stdpopsim 模型。本列表收录的 Python 前向模拟器为 fwdpy11（不存在 fwdpy2）。
<!-- /PROSE:SECTION:P12 -->

**分组：**
- *Coalescent simulators (alternatives to msprime)*：discoal, scrm。
- *Coalescent simulation (complementary)*：msprime, stdpopsim。
- *Forward or specialised simulation (alternatives)*：AlphaSimR, fwdpy11。
- *Forward simulation (alternatives)*：SLiM, pyslim。

- **discoal**（工具）— 带选择的溯祖模拟，用来训练选择扫描分类器。 输入：command-line model。输出：haplotypes。版本：0.1.7（GitHub kern-lab/discoal + Bioconda, 2026-11-14 CST）。 [link](https://github.com/kern-lab/discoal)
- **scrm**（工具）— 带重组的序贯溯祖，较快的 ms 类模拟器。 输入：command-line model。输出：haplotypes。版本：1.7.4（GitHub scrm/scrm + Bioconda, 2026-11-14 CST）。 [link](https://github.com/scrm/scrm)
- **msprime**（工具）— 树序列的溯祖模拟和 recapitation。 输入：demes model or Python demography。输出：tree sequence, VCF。版本：1.4.5（conda-forge msprime, 2026-11-14 CST (also AM14)）。 [doi:10.1093/genetics/iyab229](https://doi.org/10.1093/genetics/iyab229) · [link](https://github.com/tskit-dev/msprime)  
  注：Baumdicker et al. 2022 DOI verified (msprime 1.0).
- **stdpopsim**（工具）— 标准化模拟目录。AM14 写明：不要假定其中已有官方葡萄模型。 输入：species model id。输出：simulated genomes。版本：0.3.0（conda-forge stdpopsim, 2026-11-14 CST (also AM14)）。 [link](https://github.com/popsim-consortium/stdpopsim)  
  注：No Vitis model was confirmed in the catalogue [待确认] (same caveat as AM14).
- **AlphaSimR**（工具）— 育种计划模拟，适用于无性选择和基因组预测情景。 输入：R founder haplotypes, crossing scheme。输出：simulated phenotypes and genotypes。版本：2.1.0（CRAN/GitHub AlphaSimR, 2026-11-14 CST）。 [link](https://github.com/gaynorr/AlphaSimR)
- **fwdpy11**（工具）— 基于 fwdpp 的 Python 前向模拟器，可导出 tskit 树序列。 输入：Python model。输出：tree sequence。版本：0.24.7（PyPI fwdpy11 0.24.7 and GitHub molpopgen/fwdpy11 tag v0.24.7 (stable), 2026-11-14 CST; v0.24.8 releases are alpha/pre-release and are not used）。 [link](https://github.com/molpopgen/fwdpy11)  
  注：There is no fwdpy2 repository under molpopgen; the current tool is fwdpy11. It is not described as built on tskit; tskit is an export format. DOI [待确认].
- **SLiM**（工具）— 前向模拟，也可模拟与葡萄相关的无性世代。 输入：SLiM script, tree-seq option。输出：tree sequence, VCF, individuals。版本：5.2（conda-forge slim, 2026-11-14 CST (also AM14)）。 [doi:10.1086/723601](https://doi.org/10.1086/723601) · [link](https://github.com/messerlab/SLiM)  
  注：Verified DOI is Haller and Messer 2023 (SLiM 4). A paper specifically for SLiM 5 was not independently confirmed [待确认]. AM14 lists 5.2.
- **pyslim**（工具）— 把 SLiM 的树序列输出接到 msprime recapitation 和 tskit。 输入：SLiM tree sequence。输出：recapitated tree sequence。版本：1.1.1（PyPI and conda-forge 1.1.1; GitHub has 1.2.0b1 (beta, not used)）。 [link](https://github.com/tskit-dev/pyslim)  
  注：Latest stable is 1.1.1. GitHub 1.2.0b1 is beta and is not used as the catalog version. Bioconda pyslim 0.401 is stale.

<a id="section-13"></a>
## 13. 可视化

<!-- PROSE:SECTION:P13 -->
与上述分析配套的绘图工具。许多分析软件包本身已内置绘图功能。
<!-- /PROSE:SECTION:P13 -->

**分组：**
- *Association and ancestry plots (complementary)*：CMplot, ggtree, pophelper。
- *Maps and model drawings (complementary)*：demesdraw。

- **CMplot**（工具）— GWAS 的环形或矩形曼哈顿图和 QQ 图。 输入：association tables。输出：plots。版本：4.5.1（CRAN CMplot, 2026-11-14 CST）。 [link](https://github.com/YinLiLin/CMplot)
- **ggtree**（工具）— 树和注释图。 输入：tree。输出：plots。版本：[待确认]（see section 3）。 [link](https://bioconductor.org/packages/ggtree/)
- **pophelper**（工具）— 标准的 ADMIXTURE/STRUCTURE 柱状图。 输入：Q files。输出：plots。版本：2.3.1（see section 2）。 [link](https://github.com/royfrancis/pophelper)  
  注：Same tool as section 2.
- **demesdraw**（工具）— 绘制 demes 人口学模型。 输入：demes YAML。输出：plots。版本：0.4.1（conda-forge demesdraw, 2026-11-14 CST）。 [link](https://github.com/popsim-consortium/demesdraw)

<a id="section-14"></a>
## 14. 工作流与流程

<!-- PROSE:SECTION:P14 -->
端到端分析流程。本项目的默认分析草图仍是 AM03-AM26 模块，而非在本仓库中重新构建一套新流程。
<!-- /PROSE:SECTION:P14 -->

**分组：**
- *End-to-end workflows (alternatives)*：AM03–AM26 analysis modules, nf-core/sarek。

- **AM03–AM26 analysis modules**（流程）— 项目级模块，覆盖检测、身份、多样性、ROH、祖源、定相、GWAS 和古DNA。 输入：public data listed in that repository。输出：analysis notes。版本：vitis-open-directions v3_2, 2026-11-14（Local catalog in vitis-open-directions, not a GitHub release of this repo）。 [link](https://github.com/Xuzhen-Li/vitis-open-directions)  
  注：The public repository may not be online yet. Content used here is the v3_2 bundle already reviewed on 2026-11-14. grapeancestry remains the 167K product and is not replaced by this catalogue.
- **nf-core/sarek**（流程）— 社区 Nextflow 流程，用于种系短读变异检测。不是葡萄专用。 输入：FASTQ, reference。输出：VCF, QC。版本：[待确认]（Not version-checked in this build; listed as a well-known modern WGS workflow）。 [link](https://nf-co.re/sarek)  
  注：Version [待确认]. The AM03 sketch (bwa-mem2 + DeepVariant or GATK) is the project default if you do not use sarek.

<a id="section-15"></a>
## 15. 葡萄群体遗传研究与公开资源

<!-- PROSE:SECTION:P15 -->
公开面板与姐妹仓库。本仓库不存放未发表的基因型。
<!-- /PROSE:SECTION:P15 -->

**分组：**
- *Identity and living collections (complementary)*：grapeancestry。
- *Public Vitis resequencing panels (complementary)*：Dong et al. 2023 resequencing panel (DS11), Magris et al. 2021 and related public panels (DS10, DS12)。
- *Public Vitis resequencing or genotyping panels (complementary)*：Myles et al. 2011 SNP-array panel, Zhou et al. 2017 resequencing, Liang et al. 2019 472 accessions, Laucou et al. 2018 10K SNP panel, Freitas et al. 2021 wild hybridisation, Xiao et al. 2023 introgression, Morales-Cruz et al. 2021 North American wild Vitis, Emanuelli et al. 2013 germplasm SSR/SNP, Nicolas et al. 2016 diversity panel, Liu et al. 2024 pangenome panel, Guo et al. 2025 Vitis super-pangenome, Kim et al. 2020 high-depth resequencing。

- **grapeancestry**（资源）— 167K 从 FASTQ 到祖源的产品。本目录不替代它。 输入：n/a。输出：n/a。版本：n/a (separate product)（https://github.com/Xuzhen-Li/grapeancestry）。 [link](https://github.com/Xuzhen-Li/grapeancestry)  
  注：Out of scope for unpublished genotypes.
- **Dong et al. 2023 resequencing panel (DS11)**（资源）— 已发表的大型重测序面板，用于结构、驯化和负荷分析。 输入：public reads or VCF as published。输出：n/a。版本：n/a（vitis-open-directions DS11, recorded 2026-11-14）。 [doi:10.1126/science.add8655](https://doi.org/10.1126/science.add8655) · [link](https://doi.org/10.1126/science.add8655)  
  注：DOI 10.1126/science.add8655 verified by Crossref. Accessions include NGDC PRJCA009314 (as recorded in the literature review). Cite the original paper when used; the DS11 module in vitis-open-directions has further pointers.
- **Magris et al. 2021 and related public panels (DS10, DS12)**（资源）— 其他已发表的重测序面板，用于群体结构和多样性。 输入：public data。输出：n/a。版本：n/a（vitis-open-directions DS10 and DS12, recorded 2026-11-14）。 [doi:10.1038/s41467-021-27487-y](https://doi.org/10.1038/s41467-021-27487-y) · [link](https://doi.org/10.1038/s41467-021-27487-y)  
  注：Magris et al. 2021 DOI 10.1038/s41467-021-27487-y verified by Crossref. Related project IDs include PRJNA373967 (literature review). Pointers only; see the DS modules for accessions and sizes.
- **Myles et al. 2011 SNP-array panel**（资源）— 对一千多份栽培和野生材料的 SNP 芯片调查。 输入：public data。输出：n/a。版本：n/a（Crossref-verified in the literature review, 2026-11-14 CST）。 [doi:10.1073/pnas.1009363108](https://doi.org/10.1073/pnas.1009363108) · [link](https://doi.org/10.1073/pnas.1009363108)  
  注：Accession details were taken from the abstract in the literature review.
- **Zhou et al. 2017 resequencing**（资源）— 用于葡萄驯化基因组研究的野生和栽培重测序。 输入：public data。输出：n/a。版本：n/a（Crossref-verified in the literature review, 2026-11-14 CST）。 [doi:10.1073/pnas.1709257114](https://doi.org/10.1073/pnas.1709257114) · [link](https://doi.org/10.1073/pnas.1709257114)  
  注：DOI 和标题已对照 Crossref 核实（Evolutionary genomics of grape (Vitis vinifera ssp. vinifera) domestication）。重测序 reads：PRJNA388292（SRP108271；23 个全基因组测序 run）。Zhou 等还复用了公开的 RNA-seq 数据 SRP049306（维罗纳大学，浆果转录组）和 SRP041212（高等农学院 Instituto Superior de Agronomia，花转录组）做表达分析；这两个项目不是 Zhou 等 2017 的重测序 reads。PRJNA388292 由 Zhou 等 2017 提交；Liang 等 2019 后来复用了其中 23 份材料。
- **Liang et al. 2019 472 accessions**（资源）— 472 份材料，覆盖现存 60 个葡萄属物种中的 48 个。 输入：public data。输出：n/a。版本：n/a（Crossref-verified in the literature review, 2026-11-14 CST）。 [doi:10.1038/s41467-019-09135-8](https://doi.org/10.1038/s41467-019-09135-8) · [link](https://doi.org/10.1038/s41467-019-09135-8)  
  注：本文自己的数据为 PRJNA393611；另外还重新分析了 PRJNA388292 中的 23 份材料（由 Zhou 等 2017 提交）。
- **Laucou et al. 2018 10K SNP panel**（资源）— 783 个品种在从 18K 芯片中选出的 10,207 个 SNP 上分型；可作为亲缘和结构分析的参考，也是古籽捕获位点集的来源。 输入：public data。输出：n/a。版本：n/a（Crossref-verified in the literature review, 2026-11-14 CST）。 [doi:10.1371/journal.pone.0192540](https://doi.org/10.1371/journal.pone.0192540) · [link](https://doi.org/10.1371/journal.pone.0192540)  
  注：Crossref-verified in the literature review.
- **Freitas et al. 2021 wild hybridisation**（资源）— 西欧栽培品种和本地野生葡萄的重测序。 输入：public data。输出：n/a。版本：n/a（Crossref-verified in the literature review, 2026-11-14 CST）。 [doi:10.1126/sciadv.abi8584](https://doi.org/10.1126/sciadv.abi8584) · [link](https://doi.org/10.1126/sciadv.abi8584)  
  注：Accession identifier was not re-checked [待确认].
- **Xiao et al. 2023 introgression**（资源）— 基于 345 个样本的渗入研究（摘要）。 输入：public data。输出：n/a。版本：n/a（Crossref-verified in the literature review, 2026-11-14 CST）。 [doi:10.1073/pnas.2222041120](https://doi.org/10.1073/pnas.2222041120) · [link](https://doi.org/10.1073/pnas.2222041120)  
  注：Project IDs recorded in the literature review: PRJNA910315 and NGDC PRJCA016655.
- **Morales-Cruz et al. 2021 North American wild Vitis**（资源）— 6 个北美野生种的 130 个重测序个体。 输入：public data。输出：n/a。版本：n/a（Crossref-verified in the literature review, 2026-11-14 CST）。 [doi:10.1186/s13059-021-02467-z](https://doi.org/10.1186/s13059-021-02467-z) · [link](https://doi.org/10.1186/s13059-021-02467-z)  
  注：Project IDs recorded in the literature review include PRJNA731597.
- **Emanuelli et al. 2013 germplasm SSR/SNP**（资源）— 用 SSR 和 SNP 对 2,273 份种质分型（摘要）。 输入：public data。输出：n/a。版本：n/a（Crossref-verified in the literature review, 2026-11-14 CST）。 [doi:10.1186/1471-2229-13-39](https://doi.org/10.1186/1471-2229-13-39) · [link](https://doi.org/10.1186/1471-2229-13-39)
- **Nicolas et al. 2016 diversity panel**（资源）— 用于关联分析的 279 个品种多样性面板（摘要）。 输入：public data。输出：n/a。版本：n/a（Crossref-verified in the literature review, 2026-11-14 CST）。 [doi:10.1186/s12870-016-0754-z](https://doi.org/10.1186/s12870-016-0754-z) · [link](https://doi.org/10.1186/s12870-016-0754-z)
- **Liu et al. 2024 pangenome panel**（资源）— 29 个组装加上 466 个重测序品种（摘要）。 输入：public data。输出：n/a。版本：n/a（Crossref-verified in the literature review, 2026-11-14 CST）。 [doi:10.1038/s41588-024-01967-5](https://doi.org/10.1038/s41588-024-01967-5) · [link](https://doi.org/10.1038/s41588-024-01967-5)  
  注：The full accession list was not re-checked [待确认].
- **Guo et al. 2025 Vitis super-pangenome**（资源）— 72 个单倍型解析组装（25 个野生、47 个栽培）。 输入：public data。输出：n/a。版本：n/a（Crossref-verified in the literature review, 2026-11-14 CST）。 [doi:10.1038/s41588-025-02111-7](https://doi.org/10.1038/s41588-025-02111-7) · [link](https://doi.org/10.1038/s41588-025-02111-7)  
  注：Project ID recorded in the literature review: PRJNA1021789.
- **Kim et al. 2020 high-depth resequencing**（资源）— 对有籽、无籽和野生葡萄的高深度（高于 37 倍）重测序。 输入：public data。输出：n/a。版本：n/a（Crossref-verified in the literature review, 2026-11-14 CST）。 [doi:10.1534/g3.120.401521](https://doi.org/10.1534/g3.120.401521) · [link](https://doi.org/10.1534/g3.120.401521)  
  注：Project ID recorded in the literature review: PRJNA485199.

<a id="section-16"></a>
## 16. 在葡萄上仍少有充分测试的想法

<!-- PROSE:SECTION:P16 -->
本节列出的是预期分析方案而非已得结果，并不代表这些流程已在本仓库中针对葡萄数据实际运行过。
<!-- /PROSE:SECTION:P16 -->

**分组：**
- *Ideas still lightly tested on Vitis (complementary)*：ARG dating of grape domestication, Clone-aware ADMIXTURE and PCA recipes, Graph-aware introgression and inversion scans, Sex-determining region genotype as sample annotation (idea)。

- **ARG dating of grape domestication**（想法）— 在去克隆、已极化的面板上用 tsinfer/tsdate 或 Relate，并与古DNA末端日期比较。 输入：phased public VCF, maps。输出：dated tree sequence。版本：n/a（vitis-open-directions project 10）。 [link](https://github.com/Xuzhen-Li/vitis-open-directions)  
  注：See vitis-open-directions project 10. No results are claimed here. Use sexual-origin times as sample dates for clonal cultivars, and state the generation-time assumption when converting to years.
- **Clone-aware ADMIXTURE and PCA recipes**（想法）— 拟定做法：先检出克隆和重复（每个克隆组留一个样本），再按分析处理一级亲缘，而不是把他们当成同一基因型删掉。 输入：public VCF。输出：notes, plots。版本：n/a（stated in the current vitis-popgen README; not yet a script in the live repo）。 [link](https://github.com/Xuzhen-Li/vitis-popgen)  
  注：两步规则（克隆与一级亲缘）见 docs/WORKFLOW.zh.md。
- **Graph-aware introgression and inversion scans**（想法）— 把渗入和倒位分析从线性 VCF 转到泛基因组图上。 输入：graph, cohort genotypes。输出：tracts, local PCA。版本：n/a（vitis-open-directions projects 15 and 17; vitis-pangenome）。 [link](https://github.com/Xuzhen-Li/vitis-pangenome)  
  注：Details belong in vitis-pangenome; this repo only points to them.
- **Sex-determining region genotype as sample annotation (idea)**（想法）— 给样本注释葡萄性别决定区基因型（M、F、H），可用来推断野生样本的性别。葡萄没有异形性染色体，该位点是 2 号染色体上的一小段，栽培品种大多是两性花。见 vitis-open-directions 22 号。 输入：aligned reads or VCF around the SDR。输出：sample-level M/F/H annotation。版本：n/a（genetics review, 2026-11-14 CST）。 [link](https://github.com/Xuzhen-Li/vitis-open-directions)  
  注：Pointer only; this repository does not invent a new caller.

<a id="section-17"></a>
## 17. 亲本鉴定、系谱与名称核对

<!-- PROSE:SECTION:P17 -->
亲本鉴定、系谱重建和名称核对是葡萄群体遗传学的核心内容之一，因为少数亲本贡献了大量品种。分析前需先合并克隆样本。在此类分析中，亲属关系正是目标信号而非干扰项。同名异物与异名同物现象要同时对照基因型身份和 VIVC。
<!-- /PROSE:SECTION:P17 -->

**分组：**
- *Parentage and pedigree (complementary)*：sequoia, COLONY, Mendelian-error check on published trios (idea)。
- *Names and synonyms (complementary)*：VIVC name and genotype cross-check (idea)。

- **sequoia**（工具）— 用 SNP 推断亲本、半同胞和多代系谱。先合并克隆再运行。 输入：SNP genotype matrix, optional birth years。输出：pedigree, parent assignments。版本：3.2.0（CRAN sequoia 3.2.0 (package Date 2025-12-30), checked 2026-11-14 CST）。 [doi:10.1111/1755-0998.12665](https://doi.org/10.1111/1755-0998.12665) · [link](https://cran.r-project.org/package=sequoia)  
  注：Many grape cultivars have no reliable 'birth year'; how to set year priors remains [待确认]. Applicability to grape more generally remains [待确认].
- **COLONY**（工具）— 用全系谱似然推断亲本和同胞关系，支持雌雄同株和基因分型错误。 输入：multilocus genotypes。输出：parentage and sibship groups。版本：[待确认]（software site via the 2010 methods paper; current version not confirmed 2026-11-14 CST）。 [doi:10.1111/j.1755-0998.2009.02787.x](https://doi.org/10.1111/j.1755-0998.2009.02787.x) · [link](https://doi.org/10.1111/j.1755-0998.2009.02787.x)  
  注：Scalability to thousands of SNPs, and applicability to grape, remain [待确认]. Version [待确认].
- **Mendelian-error check on published trios (idea)**（想法）— 对文献中的亲本-子代三元组做孟德尔错误检验（例如 PLINK --mendel）。错误率高，说明系谱有误，或存在同名异物。 输入：BED + pedigree FAM。输出：Mendelian error counts。版本：n/a（uses PLINK already in this catalogue）。 [link](https://www.cog-genomics.org/plink/1.9/)  
  注：Uses the already-listed PLINK 1.9; not a second tool version.
- **VIVC name and genotype cross-check (idea)**（想法）— 同时根据基因型身份和 VIVC 的名称、同义名记录做交叉核对。同名异物和异名同物都要考虑，不能只按名称合并样本。 输入：sample names and clone groups。输出：name-to-genotype table。版本：n/a（uses the VIVC resource already listed in section 8）。 [link](https://www.vivc.de/)  
  注：The VIVC database itself is already catalogued in section 8; this row is the analysis idea.
