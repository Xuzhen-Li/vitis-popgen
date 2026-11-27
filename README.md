# vitis-popgen

English | [中文](README.zh.md)

<!-- PROSE:INTRO -->
This repository is a methods catalogue for *Vitis* population structure, gene flow, domestication, selection, demography, and related analyses on public or published data. It is organised by task, with jump links, one newest version per tool, and a workflow page in [`docs/WORKFLOW.md`](docs/WORKFLOW.md).
<!-- /PROSE:INTRO -->

It contains no unpublished genotypes, private coordinates, or sample-level matrices.

## Out of scope

- The 167K FASTQ-to-ancestry product: [grapeancestry](https://github.com/Xuzhen-Li/grapeancestry)
- Theory notes (one paper, one folder): [genomics-theory-book](https://github.com/Xuzhen-Li/genomics-theory-book)
- Chip design: [grapevine-chip](https://github.com/Xuzhen-Li/grapevine-chip)
- Pangenome graph construction and the long graph-tool list: [vitis-pangenome](https://github.com/Xuzhen-Li/vitis-pangenome)
- Ancient DNA wet lab through authentication: [grapevine-adna](https://github.com/Xuzhen-Li/grapevine-adna) (overlap with several sections here is expected)

<!-- PROSE:CATALOG_NOTE -->
**2026-11-14 catalogue, v3.2.** Each section opens with a **Clusters:** list that groups entries as alternatives (pick one), complementary (use together), or in order (run in sequence). Different versions of a single program are combined into one entry, named for the newest stable version checked on 2026-11-14, Asia/Shanghai (CST, UTC+8). Release candidates and pre-releases are excluded from catalogue versions. Unchecked versions or DOIs are marked [待确认]; any short qualifier follows the tag, such as [待确认] (numbering). A workflow with decision points is provided in [`docs/WORKFLOW.md`](docs/WORKFLOW.md).
<!-- /PROSE:CATALOG_NOTE -->

---

## Contents

1. [Variant calling and QC](#section-1) (32)
2. [Structure, admixture and PCA](#section-2) (16)
3. [Phylogeny and networks](#section-3) (12)
4. [Demography](#section-4) (17)
5. [Selection scans](#section-5) (14)
6. [Introgression and f-statistics](#section-6) (11)
7. [LD and recombination](#section-7) (5)
8. [ROH, inbreeding, kinship and clonality](#section-8) (12)
9. [GWAS, GEA and landscape genomics](#section-9) (15)
10. [Genetic load and deleterious mutations](#section-10) (6)
11. [Structural variants and pangenome-graph popgen](#section-11) (6)
12. [Simulation](#section-12) (8)
13. [Visualization](#section-13) (4)
14. [Workflows and pipelines](#section-14) (2)
15. [Vitis popgen studies and public resources](#section-15) (15)
16. [Ideas still lightly tested on Vitis](#section-16) (4)
17. [Parentage, pedigree and name identity](#section-17) (4)

This page lists 183 entries (147 tools; the rest are workflows, protocols, papers, resources or ideas). The table form is [`catalog/CATALOG.tsv`](catalog/CATALOG.tsv).

<a id="section-1"></a>
## 1. Variant calling and QC

<!-- PROSE:SECTION:P01 -->
Calling, QC, identity, phasing, and imputation for modern public resequencing data. Detect clones and duplicates before downstream analyses, and handle first-degree relatives separately (see the workflow).
<!-- /PROSE:SECTION:P01 -->

**Clusters:**
- *Joint genotyping (alternatives)*: GLnexus.
- *Mapping (alternatives)*: BWA (bwa mem / bwa aln), bwa-mem2.
- *BAM processing (complementary)*: samtools.
- *Phasing and imputation of modern data (in order)*: Beagle, GLIMPSE2, SHAPEIT5, WhatsHap.
- *Read QC (complementary)*: FastQC, MultiQC, fastp, seqkit.
- *Sample identity, before structure (complementary)*: KING, PLINK 1.9, peddy, plink2, somalier, verifybamid2, SNPRelate, Technical-replicate IBS or discordance cutoff (idea).
- *BAM hygiene / post-mapping (complementary)*: Picard.
- *VCF QC and manipulation (complementary)*: bcftools, htslib, mosdepth, vcftools, vt.
- *Variant calling (alternatives)*: DeepVariant, GATK HaplotypeCaller / GenotypeGVCFs, Octopus, freebayes.
- *Somatic variants among clones (complementary)*: GATK Mutect2, L1/L2 chimerism validation design (idea).

- **GLnexus** (tool) — Joint-genotypes DeepVariant gVCFs into a cohort VCF. Input: gVCF. Output: VCF. Version: 1.4.1 (GitHub dnanexus-rnd/GLnexus + Bioconda, 2026-11-14 CST). [link](https://github.com/dnanexus-rnd/GLnexus)  
  Note: AM03 alternative to GATK GenotypeGVCFs.
- **BWA (bwa mem / bwa aln)** (tool) — bwa mem for modern reads; bwa aln is the aDNA default (see grapevine-adna). Input: FASTQ, FASTA. Output: SAM/BAM. Version: 0.7.19 (GitHub lh3/bwa + Bioconda, 2026-11-14 CST). [doi:10.1093/bioinformatics/btp324](https://doi.org/10.1093/bioinformatics/btp324) · [link](https://github.com/lh3/bwa)
- **bwa-mem2** (tool) — Default short-read mapper for modern grape resequencing (AM03). Input: FASTQ, FASTA. Output: SAM/BAM. Version: 2.3 (GitHub bwa-mem2/bwa-mem2 + Bioconda, 2026-11-14 CST). [link](https://github.com/bwa-mem2/bwa-mem2)  
  Note: Use bwa aln for degraded aDNA; that route is in grapevine-adna.
- **samtools** (tool) — Sort, index, mark duplicates, filter and report alignment statistics. Input: SAM/BAM/CRAM. Output: BAM/CRAM, stats. Version: 1.25 (GitHub samtools/samtools + Bioconda, 2026-11-14 CST). [doi:10.1093/gigascience/giab008](https://doi.org/10.1093/gigascience/giab008) · [link](https://github.com/samtools/samtools)  
  Note: Same 1.25 line as bcftools and htslib. samtools is not a mapper; it belongs with BAM processing, not under Mapping.
- **Beagle** (tool) — Phasing and imputation alternative to SHAPEIT5 and GLIMPSE2. Input: VCF. Output: phased or imputed VCF. Version: 5.4_22Jul22.46e (Bioconda beagle, 2026-11-14 CST). [doi:10.1016/j.ajhg.2018.07.015](https://doi.org/10.1016/j.ajhg.2018.07.015) · [link](https://faculty.washington.edu/browning/beagle/beagle.html)  
  Note: Bioconda build date is 22 July 2022. Check the author site before pinning a newer unlisted build [待确认]. Beagle 5 paper DOI (Browning et al. 2018) verified by Crossref in the literature review.
- **GLIMPSE2** (tool) — Imputes low-coverage genomes from a haplotype reference panel. Input: low-coverage BAM or genotype likelihoods, reference panel. Output: imputed VCF. Version: 2.0.0 (GitHub odelaneau/GLIMPSE tag v2.0.0 (latest stable), 2026-11-14 CST; v2.0.1 is a GitHub pre-release and is not used as the catalogue version). [doi:10.1038/s41588-023-01438-3](https://doi.org/10.1038/s41588-023-01438-3) · [link](https://github.com/odelaneau/GLIMPSE)  
  Note: For aDNA, test accuracy on modern grapes downsampled to ancient depths first (AM17, project 20). GitHub v2.0.1 is marked pre-release (checked 2026-11-14 CST); Bioconda glimpse-bio may still list 2.0.1. This catalogue pins the latest stable tag, 2.0.0, consistent with not using RC or beta tags as the catalogue version.
- **SHAPEIT5** (tool) — Phases common then rare variants. Default in AM13 and AM26, with a published linkage map when one exists. Input: VCF, genetic map. Output: phased VCF. Version: 5.1.1 (GitHub odelaneau/shapeit5 + Bioconda, 2026-11-14 CST). [doi:10.1038/s41588-023-01415-w](https://doi.org/10.1038/s41588-023-01415-w) · [link](https://github.com/odelaneau/shapeit5)  
  Note: Do not use a pyrho map for phasing (AM26).
- **WhatsHap** (tool) — Read-backed phasing, useful where long reads or linked reads exist. Input: BAM, VCF. Output: phased VCF. Version: 2.8 (GitHub whatshap/whatshap + Bioconda/PyPI, 2026-11-14 CST). [link](https://github.com/whatshap/whatshap)
- **FastQC** (tool) — Per-file read quality, length and adapter content. Input: FASTQ. Output: HTML/zip QC. Version: 0.13.0 (GitHub s-andrews/FastQC + Bioconda, 2026-11-14 CST). [link](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
- **MultiQC** (tool) — Aggregates QC reports from many tools into one HTML summary. Input: tool QC files. Output: HTML report. Version: 1.35 (GitHub MultiQC/MultiQC + Bioconda, 2026-11-14 CST). [link](https://github.com/MultiQC/MultiQC)
- **fastp** (tool) — Trims adapters and low-quality bases and writes a QC report. Input: FASTQ. Output: trimmed FASTQ, HTML/JSON QC. Version: 1.4.0 (GitHub OpenGene/fastp + Bioconda, checked 2026-11-14 CST). [link](https://github.com/OpenGene/fastp)  
  Note: GitHub release 2026-10-07. Also in vitis-open-directions AM02.
- **seqkit** (tool) — FASTQ/FASTA statistics, filtering and conversion. Input: FASTQ/FASTA. Output: tables, filtered files. Version: 2.14.0 (GitHub shenwei356/seqkit + Bioconda, 2026-11-14 CST). [link](https://github.com/shenwei356/seqkit)
- **KING** (tool) — Robust kinship for clones or duplicates versus first-degree relatives. Clones and duplicates (kinship above 0.354) are reduced to one sample per group; first-degree relatives (0.177-0.354) are registered, not dropped as the same genotype. Input: hard-called diploid genotypes (BED). Output: kinship tables. Version: 2.3.2 (Bioconda king, 2026-11-14 CST). [doi:10.1093/bioinformatics/btq559](https://doi.org/10.1093/bioinformatics/btq559) · [link](https://www.kingrelatedness.com/)  
  Note: Thresholds follow the KING manual (https://www.kingrelatedness.com/manual.shtml): kinship above 0.354 is the duplicate/MZ class; 0.177-0.354 is first-degree. Paper: Manichaikul et al. 2010, 10.1093/bioinformatics/btq559. AM26 used 0.177 as the first-degree lower cutoff. Input should be hard-called diploid genotypes (BED). For low-coverage or ancient samples use ngsRelate, READv2, KIN or BREADR instead. Handling of first-degree relatives is analysis-specific; see docs/WORKFLOW.md.
- **PLINK 1.9** (tool) — Older PLINK still needed for some ROH runs and file conversions. Input: BED/PED. Output: IBD, ROH, association. Version: 1.90b6.21 (Bioconda plink, 2026-11-14 CST). [doi:10.1086/519795](https://doi.org/10.1086/519795) · [link](https://www.cog-genomics.org/plink/1.9/)  
  Note: DOI is Purcell et al. 2007. Chang et al. 2015 (doi:10.1186/s13742-015-0047-8) describes 1.9.
- **peddy** (tool) — Relatedness and ancestry-outlier QC. Mammal-style sex checks do not transfer to Vitis. Input: VCF, PED. Output: HTML QC. Version: 0.4.8 (GitHub brentp/peddy + Bioconda/PyPI, 2026-11-14 CST). [link](https://github.com/brentp/peddy)
- **plink2** (tool) — Converts VCF to analysis files and runs PCA, relatedness and basic association. Input: VCF, PGEN/BED. Output: PGEN, PCA, kinship, association. Version: 2.0.0-b.1.4 (GitHub chrchang/plink-ng 2026-11-07; Bioconda 2.00a5.10). [doi:10.1186/s13742-015-0047-8](https://doi.org/10.1186/s13742-015-0047-8) · [link](https://www.cog-genomics.org/plink/2.0/)  
  Note: Newest GitHub tag uses pre-release-style numbering. Bioconda still 2.00a5.10. The DOI is Chang et al. 2015 (PLINK 1.9); a separate paper for this exact 2.0 tag was not confirmed.
- **somalier** (tool) — Fast relatedness and sample-swap checks from BAM or VCF. Input: BAM/VCF. Output: relatedness, QC plots. Version: 0.3.7 (GitHub brentp/somalier + Bioconda, 2026-11-14 CST). [link](https://github.com/brentp/somalier)  
  Note: Like peddy and verifybamid2, this tool ships with human site lists. Build a grape site set before using it on Vitis; off-the-shelf human sites are not appropriate.
- **verifybamid2** (tool) — Estimates BAM-versus-VCF contamination and swaps. Written for humans; treat grape values as exploratory. Input: BAM, VCF. Output: contamination estimate. Version: 2.0.3 (GitHub Griffan/VerifyBamID + Bioconda, 2026-11-14 CST). [link](https://github.com/Griffan/VerifyBamID)  
  Note: See grapevine-adna for plant contamination.
- **SNPRelate** (tool) — IBS, IBD (MoM/MLE) and PCA in R; a cross-check for KING. Input: GDS (from VCF). Output: IBS matrix, IBD estimates, PCs. Version: 1.46.0 (Bioconductor release package SNPRelate 1.46.0, checked 2026-11-14 CST). [doi:10.1093/bioinformatics/bts606](https://doi.org/10.1093/bioinformatics/bts606) · [link](https://bioconductor.org/packages/SNPRelate/)  
  Note: Version is the Bioconductor release page value on 2026-11-14 CST.
- **Technical-replicate IBS or discordance cutoff (idea)** (idea) — Calibrate an 'same genotype' IBS or genotype-discordance cutoff from technical replicates and known clone pairs, so sequencing error and somatic differences are not treated as different cultivars. Input: VCF. Output: pairwise discordance distribution and a cutoff. Version: n/a (methods review, 2026-11-14 CST).  
  Note: Complements the KING 0.354 rule; it does not replace it.
- **Picard** (tool) — MarkDuplicates, read groups, CleanSam and related BAM hygiene. Input: BAM/SAM. Output: BAM, metrics. Version: 3.5.0 (GitHub broadinstitute/picard + Bioconda, 2026-11-14 CST). [link](https://github.com/broadinstitute/picard)  
  Note: Picard works on BAM (MarkDuplicates, read groups, CleanSam), not on VCF. GitHub release 2026-07-31 CST-relative: 2026-08-01 02:56 CST.
- **bcftools** (tool) — Filter, normalise, annotate, compute statistics, and call ROH (see section 8). Input: VCF/BCF or BAM. Output: VCF/BCF, tables. Version: 1.25 (GitHub samtools/bcftools + Bioconda, 2026-11-14 CST). [doi:10.1093/gigascience/giab008](https://doi.org/10.1093/gigascience/giab008) · [link](https://github.com/samtools/bcftools)
- **htslib** (tool) — Library behind samtools and bcftools; pin it to the same 1.25 line. Input: BAM/VCF streams. Output: same. Version: 1.25 (GitHub samtools/htslib + Bioconda, 2026-11-14 CST). [doi:10.1093/gigascience/giab008](https://doi.org/10.1093/gigascience/giab008) · [link](https://github.com/samtools/htslib)
- **mosdepth** (tool) — Fast per-base and window depth, used to build callable-site masks. Input: BAM/CRAM. Output: depth BED/txt. Version: 0.3.15 (GitHub brentp/mosdepth 2026-10-29; Bioconda still 0.3.14). [link](https://github.com/brentp/mosdepth)  
  Note: Newest is GitHub 0.3.15; Bioconda lagged at 0.3.14 on 2026-11-14.
- **vcftools** (tool) — Classic VCF filtering and window statistics. Prefer pixy for pi and dxy on all-sites VCFs. Input: VCF. Output: filtered VCF, window stats. Version: 0.1.17 (GitHub vcftools/vcftools + Bioconda, 2026-11-14 CST). [doi:10.1093/bioinformatics/btr330](https://doi.org/10.1093/bioinformatics/btr330) · [link](https://github.com/vcftools/vcftools)  
  Note: No newer tagged release than 0.1.17.
- **vt** (tool) — Normalises and decomposes complex variants before cohort QC. Input: VCF. Output: normalised VCF. Version: 0.57721 (GitHub atks/vt + Bioconda, 2026-11-14 CST). [link](https://github.com/atks/vt)
- **DeepVariant** (tool) — Default modern SNP/indel caller in the AM03 sketch (WGS model). Input: BAM/CRAM, FASTA. Output: VCF/gVCF. Version: 1.10.0 (GitHub google/deepvariant, 2026-11-14 CST). [doi:10.1038/nbt.4235](https://doi.org/10.1038/nbt.4235) · [link](https://github.com/google/deepvariant)  
  Note: Joint-genotype gVCFs with GLnexus. Record whether a plant-trained model is used.
- **GATK HaplotypeCaller / GenotypeGVCFs** (tool) — Alternative caller and joint-genotyping route for short-read SNPs and indels. Input: BAM, FASTA. Output: gVCF, joint VCF. Version: 4.7.0.0 (GitHub broadinstitute/gatk, 2026-11-14 CST). [doi:10.1101/gr.107524.110](https://doi.org/10.1101/gr.107524.110) · [link](https://github.com/broadinstitute/gatk)
- **Octopus** (tool) — Haplotype caller with strong indel and regional-haplotype modelling. Input: BAM, FASTA. Output: VCF. Version: 0.7.4 (GitHub luntergroup/octopus + Bioconda, 2026-11-14 CST). [link](https://github.com/luntergroup/octopus)
- **freebayes** (tool) — Haplotype-based Bayesian caller, useful in highly heterozygous grape regions. Input: BAM, FASTA. Output: VCF. Version: 1.3.10 (GitHub freebayes/freebayes + Bioconda, 2026-11-14 CST). [link](https://github.com/freebayes/freebayes)
- **GATK Mutect2** (tool) — Paired somatic-variant calling between clones of the same cultivar. Input: paired BAM. Output: somatic VCF. Version: 4.7.0.0 (same GATK 4.7.0.0 already listed for HaplotypeCaller in this catalogue). [link](https://github.com/broadinstitute/gatk)  
  Note: The tool exists. Power and false-positive rate under grape L1/L2 chimerism remain [待确认] and need independent validation. DOI of a Mutect2 methods paper [待确认].
- **L1/L2 chimerism validation design (idea)** (idea) — Low-frequency somatic variants should be validated with high depth, biological replicates, and preferably layer-specific tissue. Allele ratios from mixed L1/L2 tissue are not proof of a heritable variant. Input: high-depth BAM. Output: validated somatic variants. Version: n/a (methods and genetics reviews, 2026-11-14 CST).  
  Note: Biological interpretation of grape chimerism is outside the methods review; this is a design reminder.

<a id="section-2"></a>
## 2. Structure, admixture and PCA

<!-- PROSE:SECTION:P02 -->
Global ancestry, PCA, local ancestry, and spatial structure. Retain one sample per clone or duplicate group; handle first-degree relatives in an analysis-specific way (using an unrelated subset plus projection, or a sensitivity analysis) rather than dropping them as identical genotypes.
<!-- /PROSE:SECTION:P02 -->

**Clusters:**
- *Chromosome painting and local ancestry (in order)*: Loter, RFMix, fineSTRUCTURE / ChromoPainter.
- *Global ancestry (alternatives)*: ADMIXTURE, fastSTRUCTURE, sNMF (LEA).
- *Low-coverage genotype-likelihood methods (alternatives)*: ANGSD, PCAngsd.
- *ADMIXTURE fit check (complementary)*: evalAdmix.
- *PCA (alternatives)*: flashpca, smartpca (EIGENSOFT).
- *Q-matrix display (complementary)*: pophelper.
- *Spatial or inversion-aware structure (complementary)*: lostruct.
- *Spatial structure (alternatives)*: FEEMS, conStruct.
- *Key low-coverage references (complementary)*: Lou et al. 2021 lcWGS guide.

- **Loter** (tool) — Phasing-free local ancestry for two or more sources. Input: diploid genotypes. Output: local ancestry. Version: 1.0.1 (GitHub bcm-uga/Loter + Bioconda, 2026-11-14 CST). [link](https://github.com/bcm-uga/Loter)
- **RFMix** (tool) — Local ancestry after SHAPEIT5 phasing; default in AM13. Input: phased VCF, reference panels. Output: local-ancestry tracts. Version: 2.03.r0.9505bfa (Bioconda rfmix, 2026-11-14 CST (same string as AM13)). [link](https://github.com/slowkoni/rfmix)
- **fineSTRUCTURE / ChromoPainter** (tool) — Paints chromosomes as mosaics of donor haplotypes, finer than a single ADMIXTURE K. Input: phased haplotypes. Output: painting, coancestry. Version: [待确认] (Vendor site; version not checked in this build). [doi:10.1371/journal.pgen.1002453](https://doi.org/10.1371/journal.pgen.1002453) · [link](https://people.maths.bris.ac.uk/~madjl/finestructure/)  
  Note: Version [待确认].
- **ADMIXTURE** (tool) — Maximum-likelihood ancestry proportions; default in AM13. Input: BED, LD-pruned SNPs. Output: Q and P matrices. Version: 1.3.0 (Bioconda admixture, 2026-11-14 CST). [doi:10.1101/gr.094052.109](https://doi.org/10.1101/gr.094052.109) · [link](https://dalexander.github.io/admixture/)  
  Note: Clone-prune first (one sample per clone or duplicate group). First-degree relatives should not be dropped as if they were the same genotype; for ADMIXTURE use an unrelated subset or report a sensitivity analysis (see docs/WORKFLOW.md). Choose K with cross-validation and inspect fit with evalAdmix.
- **fastSTRUCTURE** (tool) — Variational STRUCTURE-like model for large SNP sets. Input: STRUCTURE or BED-like files. Output: Q matrix. Version: 1.0 (GitHub rajanil/fastStructure + Bioconda, 2026-11-14 CST). [doi:10.1534/genetics.114.164350](https://doi.org/10.1534/genetics.114.164350) · [link](https://github.com/rajanil/fastStructure)  
  Note: Last tagged release remains 1.0.
- **sNMF (LEA)** (tool) — Fast sparse NMF ancestry, often more tolerant of missing data than ADMIXTURE. Input: genotype matrix. Output: Q matrix. Version: sNMF 1.2; LEA package version [待确认] (Bioconda snmf 1.2; LEA is Bioconductor). [link](https://bcm-uga.github.io/LEA/)
- **ANGSD** (tool) — Genotype likelihoods, allele frequencies, SFS, association and haploid calls from BAM. Input: BAM, reference. Output: genotype likelihoods, SFS, MAF, haploid calls. Version: 0.940 (GitHub ANGSD/angsd + Bioconda, 2026-11-14 CST). [doi:10.1186/s12859-014-0356-4](https://doi.org/10.1186/s12859-014-0356-4) · [link](https://github.com/ANGSD/angsd)  
  Note: Central for aDNA and low-coverage modern data. Human X-chromosome contamination utilities do not transfer to grape.
- **PCAngsd** (tool) — PCA and admixture-style structure from genotype likelihoods, including low coverage. Input: ANGSD-style genotype likelihoods. Output: principal components, admixture. Version: 1.37.0 (GitHub Rosemeis/pcangsd 2026-10-23; Bioconda/PyPI 1.36.4). [doi:10.1534/genetics.118.301336](https://doi.org/10.1534/genetics.118.301336) · [link](https://github.com/Rosemeis/pcangsd)  
  Note: Newest GitHub tag is 1.37.0; Bioconda lagged at 1.36.4.
- **evalAdmix** (tool) — Checks whether an ADMIXTURE or NGSadmix Q matrix actually fits the data. Input: genotype likelihoods or genotypes, Q matrix. Output: residuals, plots. Version: 1.0 (GitHub GenisGE/evalAdmix + Bioconda, 2026-11-14 CST). [doi:10.1111/1755-0998.13171](https://doi.org/10.1111/1755-0998.13171) · [link](https://github.com/GenisGE/evalAdmix)  
  Note: DOI (Garcia-Erill and Albrechtsen 2020) verified by Crossref in the 2026-11-14 literature review.
- **flashpca** (tool) — Fast PCA on large SNP matrices. Input: BED. Output: principal components. Version: 2.0 (GitHub gabraham/flashpca + Bioconda, 2026-11-14 CST). [link](https://github.com/gabraham/flashpca)
- **smartpca (EIGENSOFT)** (tool) — PCA with shrinkage and lsqproject, the usual way to project aDNA onto a modern PCA. Input: EIGENSTRAT. Output: eigenvectors, projected PCs. Version: 9.0.0 (Bioconda); GitHub tag v8.0.0 [待确认] (numbering) (Bioconda eigensoft 9.0.0; DReichLab/EIG GitHub tag v8.0.0). [doi:10.1371/journal.pgen.0020190](https://doi.org/10.1371/journal.pgen.0020190) · [link](https://github.com/DReichLab/EIG)  
  Note: Pin the exact binary. Bioconda and GitHub numbers disagree.
- **pophelper** (tool) — Aligns and plots ADMIXTURE or STRUCTURE Q matrices across K. Input: Q files. Output: plots, aligned Q. Version: 2.3.1 (GitHub royfrancis/pophelper, 2026-11-14 CST). [link](https://github.com/royfrancis/pophelper)
- **lostruct** (tool) — Windowed local PCA to find inversions and local ancestry tracts. Input: genotypes. Output: local-PCA MDS, outlier windows. Version: [待确认] (GitHub petrelharp/local_pca; no release tag in this check). [link](https://github.com/petrelharp/local_pca)  
  Note: Useful on grape inversion candidates; see also vitis-pangenome and vitis-open-directions project 17.
- **FEEMS** (tool) — Estimates effective migration surfaces from sample geography. Input: genotypes, public coordinates. Output: migration surfaces. Version: 2.0.1 (GitHub NovembreLab/feems + PyPI, 2026-11-14 CST). [link](https://github.com/NovembreLab/feems)  
  Note: This repository does not accept private site coordinates.
- **conStruct** (tool) — Spatial structure that separates isolation by distance from admixture. Input: allele frequencies, coordinates. Output: layer contributions. Version: 1.0.3 (GitHub gbradburd/conStruct, 2026-11-14 CST). [link](https://github.com/gbradburd/conStruct)
- **Lou et al. 2021 lcWGS guide** (paper) — Practical guide to genotype-likelihood population genetics on low-coverage whole-genome data. Input: n/a. Output: n/a. Version: n/a (Crossref-verified in the literature review, 2026-11-14 CST). [doi:10.1111/mec.16077](https://doi.org/10.1111/mec.16077) · [link](https://doi.org/10.1111/mec.16077)

<a id="section-3"></a>
## 3. Phylogeny and networks

<!-- PROSE:SECTION:P03 -->
Trees and networks built from LD-pruned SNPs or gene trees. Conflicting evolutionary histories belong on a network, not only a single tree. Plastid haplotypes can provide a maternal line of evidence (see grapevine-plastid), though resolution within *Vitis* is low.
<!-- /PROSE:SECTION:P03 -->

**Clusters:**
- *Bayesian or dated trees (alternatives)*: BEAST 2.
- *Fast trees (alternatives)*: FastTree.
- *Maximum-likelihood trees (alternatives)*: IQ-TREE 2, IQ-TREE 3, RAxML-NG.
- *Networks and mixtures (alternatives)*: TreeMix.
- *Networks and mixtures (complementary)*: OptM, Twisst.
- *Species or multi-locus trees (alternatives)*: ASTRAL.
- *Splits and haplotype networks (alternatives)*: SplitsTree.
- *Tree display (complementary)*: ggtree.
- *Plastid maternal haplotypes (complementary)*: Chloroplast haplotype as a maternal lineage (idea).

- **BEAST 2** (tool) — Bayesian trees and tip-dating when time calibrations exist. Input: alignment, priors. Output: trees, dates. Version: 2.7.8 (GitHub CompEvol/beast2 + Bioconda, 2026-11-14 CST). [link](https://www.beast2.org/)  
  Note: For aDNA tip-dating use transversions or UDG-treated data.
- **FastTree** (tool) — Approximate ML tree for very large alignments, as a first look. Input: alignment. Output: tree. Version: 2.2.0 (Bioconda fasttree, 2026-11-14 CST). [link](http://www.microbesonline.org/fasttree/)
- **IQ-TREE 2** (tool) — Previous major line of IQ-TREE, still widely used. Input: SNP alignment. Output: tree. Version: 2.4.0 (GitHub iqtree/iqtree2 + Bioconda, 2026-11-14 CST). [doi:10.1093/molbev/msaa015](https://doi.org/10.1093/molbev/msaa015) · [link](https://github.com/iqtree/iqtree2)  
  Note: Listed because many published grape trees used v2; prefer v3 for new work unless a pipeline is pinned.
- **IQ-TREE 3** (tool) — Default ML tree builder in AM23. Input: SNP alignment, partitions. Output: tree, model fit. Version: 3.1.4 (GitHub iqtree/iqtree3 + Bioconda, 2026-11-14 CST). [link](https://github.com/iqtree/iqtree3)  
  Note: Do not put the IQ-TREE 2 DOI (10.1093/molbev/msaa015) in this row's DOI field. That DOI belongs to IQ-TREE 2 and is recorded only here as a cross-reference. An IQ-TREE 3 paper DOI was not confirmed [待确认].
- **RAxML-NG** (tool) — Alternative ML tree search, convenient on large SNP matrices. Input: alignment, partition. Output: tree. Version: 2.0.4 (GitHub amkozlov/raxml-ng + Bioconda, 2026-11-14 CST). [link](https://github.com/amkozlov/raxml-ng)
- **TreeMix** (tool) — Graph of population splits plus migration edges. Input: allele counts. Output: graph, residuals. Version: 1.12 (GitHub joepickrell/treemix + Bioconda, 2026-11-14 CST). [doi:10.1371/journal.pgen.1002967](https://doi.org/10.1371/journal.pgen.1002967) · [link](https://github.com/joepickrell/treemix)  
  Note: Choose the number of migration edges with OptM and residual plots; clone-prune first.
- **OptM** (tool) — Helps pick the number of TreeMix migration edges. Input: TreeMix outputs. Output: suggested edge number. Version: 0.1.9 (CRAN OptM, 2026-11-14 CST). [doi:10.1093/biomethods/bpab017](https://doi.org/10.1093/biomethods/bpab017) · [link](https://cran.r-project.org/package=OptM)  
  Note: DOI (Fitak 2021) verified by Crossref in the literature review.
- **Twisst** (tool) — Topology weighting along the genome, useful for introgression windows. Input: window trees. Output: weights along the genome. Version: 0.2 (GitHub simonhmartin/twisst, 2026-11-14 CST). [link](https://github.com/simonhmartin/twisst)
- **ASTRAL** (tool) — Species tree from unrooted gene trees under the multispecies coalescent. Input: gene trees. Output: species tree. Version: 5.7.1 (GitHub smirarab/ASTRAL + Bioconda, 2026-11-14 CST). [link](https://github.com/smirarab/ASTRAL)  
  Note: More relevant to Vitaceae family phylogeny than to cultivar SNPs.
- **SplitsTree** (tool) — NeighborNet and other split networks for conflicting histories. Input: alignment or distances. Output: network. Version: [待确认] (Official site; version not checked in this build). [link](https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/lehrstuehle/algorithms-in-bioinformatics/software/splitstree/)  
  Note: Version [待确认].
- **ggtree** (tool) — Grammar-of-graphics plotting of trees and associated data. Input: tree, annotations. Output: plots. Version: [待确认] (Bioconductor; GitHub path not resolved in this check). [link](https://bioconductor.org/packages/ggtree/)  
  Note: Version [待确认].
- **Chloroplast haplotype as a maternal lineage (idea)** (idea) — Plastid haplotypes record the maternal line and are a separate line of evidence from the nuclear genome. Assembly practice lives in grapevine-plastid. Within Vitis, plastid resolution is low and chloroplast capture can occur. Input: plastid reads or assemblies. Output: haplotype assignments. Version: n/a (genetics review, 2026-11-14 CST). [link](https://github.com/Xuzhen-Li/grapevine-plastid)  
  Note: Representative Vitis plastid-haplotype papers were not re-checked in this revision [待确认].

<a id="section-4"></a>
## 4. Demography

<!-- PROSE:SECTION:P04 -->
ARG, SMC, SFS, and recent-Ne methods. Reduce clones and duplicates to one sample per group. First-degree relatives distort recent Ne and LD estimates and should be removed or modelled for those analyses. Hybrid-origin cultivars can generate false old Ne peaks in PSMC and MSMC. Convert results to years only with an explicit generation-time assumption (the interval between sexual generations). For ARG and SMC methods, set a cultivar's sample time to its sexual origin rather than its extraction year. Because that origin date is usually unknown, treat it as a parameter or evaluate it via sensitivity analysis rather than as a fixed constant. Somatic mutations accumulated during clonal propagation have minimal impact on SMC, but can appear as a few overly long tip branches on an ARG.
<!-- /PROSE:SECTION:P04 -->

**Clusters:**
- *ARG methods alternative to the tsinfer/tsdate pair (alternatives)*: Relate, SINGER.
- *tsinfer then tsdate (in order)*: tsdate, tsinfer.
- *Model and observation format (complementary)*: tskit.
- *Recent Ne from LD or IBD (alternatives)*: GONE2, currentNe.
- *SFS and ABC demography (alternatives)*: GADMA, dadi, fastsimcoal2, moments.
- *SFS and ABC demography (complementary)*: demes / demesdraw.
- *SMC-style histories (alternatives)*: MSMC2, PSMC, SMC++.
- *Parameters shared by demographic and ARG methods (complementary)*: Generation time and mutation rate as explicit assumptions (idea), Sexual-origin time as the sample date (idea).

- **Relate** (tool) — Genome-wide genealogy estimation for thousands of samples; also feeds selection tests. Input: phased haplotypes, genetic map. Output: genealogies, coalescence rates. Version: [待确认] (No public tag resolved in this check (MyersGroup/relate returned 404)). [doi:10.1038/s41588-019-0484-x](https://doi.org/10.1038/s41588-019-0484-x) · [link](https://myersgroup.github.io/relate/)  
  Note: An alternative to the tsinfer-then-tsdate pair, not to tsinfer alone. Version and some setup details [待确认]. Sample time for a cultivar should be its sexual origin.
- **SINGER** (tool) — ARG inference with posterior sampling, an alternative to tsinfer plus tsdate. Input: phased haplotypes. Output: sampled ARGs. Version: 0.1.8-beta (GitHub popgenmethods/SINGER, 2026-11-14 CST (also AM14)). [link](https://github.com/popgenmethods/SINGER)  
  Note: An alternative to the tsinfer-then-tsdate pair. The listed version string includes beta and is used only because no later stable tag was confirmed [待确认] (whether a later stable tag exists). Sample time for a cultivar should be its sexual origin.
- **tsdate** (tool) — Dates a tsinfer tree sequence. Input: tree sequence. Output: dated tree sequence. Version: 0.2.7 (PyPI tsdate, 2026-11-14 CST (also AM14)). [link](https://github.com/tskit-dev/tsdate)  
  Note: Dates a tree sequence produced by tsinfer; it is the second step of that pair, not an alternative to tsinfer. Sample times should be sexual-origin dates for clonal cultivars.
- **tsinfer** (tool) — Infers a tree sequence (ARG approximation) from phased large samples. Input: phased genotypes. Output: tree sequence. Version: 0.5.1 (conda-forge tsinfer, 2026-11-14 CST (also AM14)). [doi:10.1038/s41588-019-0483-y](https://doi.org/10.1038/s41588-019-0483-y) · [link](https://github.com/tskit-dev/tsinfer)  
  Note: Run tsinfer first, then date the tree sequence with tsdate. Clone-prune and record close kinship first (AM14, project 10). For a cultivar, the sample time should be the sexual origin, not the extraction year.
- **tskit** (tool) — Library for tree sequences produced by tsinfer, msprime or SLiM. Input: tree sequence. Output: statistics, subsets. Version: 1.0.4 (conda-forge/PyPI tskit, 2026-11-14 CST). [link](https://github.com/tskit-dev/tskit)
- **GONE2** (tool) — Recent effective size from the linkage-disequilibrium spectrum; successor of GONE. Input: genotypes, map. Output: recent Ne. Version: v2.0.2 (GitHub esrud/GONE2 release v2.0.2, checked 2026-11-14 CST). [link](https://github.com/esrud/GONE2)  
  Note: Newest version of this lineage (GONE replaced by GONE2). The model assumes random mating and no strong structure; selfing, clones and population structure violate those assumptions, so clone-prune first and state the assumptions in the write-up. A related contemporary-Ne tool is currentNe.
- **currentNe** (tool) — Estimates contemporary effective size; a companion to GONE2. Input: genotypes. Output: contemporary Ne. Version: v1.0.0-1 (GitHub esrud/currentNe, only release tag v1.0.0-1, checked 2026-11-14 CST). [link](https://github.com/esrud/currentNe)  
  Note: The only GitHub tag is v1.0.0-1. Model assumptions (random mating, limited structure) should be stated; clone-prune first. Method DOI [待确认].
- **GADMA** (tool) — Automated search of demographic model structure on top of dadi or moments or fastsimcoal2. Input: SFS. Output: model, parameters. Version: 2.0.3 (GitHub ctlab/GADMA + Bioconda/PyPI, 2026-11-14 CST). [link](https://github.com/ctlab/GADMA)
- **dadi** (tool) — Fits demographic models to the site-frequency spectrum. Input: SFS. Output: model parameters, likelihood. Version: 2.0.5 (GitHub kern-lab/dadi + Bioconda/PyPI, 2026-11-14 CST). [doi:10.1371/journal.pgen.1000695](https://doi.org/10.1371/journal.pgen.1000695) · [link](https://github.com/kern-lab/dadi)
- **fastsimcoal2** (tool) — Composite-likelihood demographic inference under complex models, including site frequency spectra. Input: SFS, model. Output: parameter estimates. Version: [待确认] (Bioconda name not resolved) (Author site; no Bioconda hit in this check). [doi:10.1093/bioinformatics/btab468](https://doi.org/10.1093/bioinformatics/btab468) · [link](http://cmpg.unibe.ch/software/fastsimcoal2/)  
  Note: Software version [待确认]; the 2021 Bioinformatics paper DOI was verified.
- **moments** (tool) — SFS and LD-based demographic inference, including momentsLD. Input: SFS or LD statistics. Output: model parameters. Version: 1.7.0 (GitHub apragsdale/moments + Bioconda/PyPI, 2026-11-14 CST). [doi:10.1534/genetics.117.200493](https://doi.org/10.1534/genetics.117.200493) · [link](https://github.com/apragsdale/moments)
- **demes / demesdraw** (tool) — A common YAML format for demographic models, plus plotting. Input: demes YAML. Output: validated model, plots. Version: demes 0.2.3; demesdraw 0.4.1 (PyPI/conda-forge, 2026-11-14 CST). [link](https://github.com/popsim-consortium/demes-python)
- **MSMC2** (tool) — Cross-coalescence and Ne from a few phased haplotypes. Input: phased haplotypes, mask. Output: Ne and cross-coalescence. Version: 2.1.4 (GitHub stschiff/msmc2 + Bioconda, 2026-11-14 CST). [doi:10.1038/ng.3015](https://doi.org/10.1038/ng.3015) · [link](https://github.com/stschiff/msmc2)  
  Note: The catalogue DOI is Schiffels and Durbin 2014 (MSMC). MSMC2 is the later implementation, described in Schiffels and Wang 2020, 10.1007/978-1-0716-0199-0_7. Hybrid-origin cultivars can produce false old Ne peaks because the two haplotypes come from different source populations. For a clonal cultivar the sample time should be the sexual-origin date, treated as a parameter or a sensitivity analysis when that date is unknown.
- **PSMC** (tool) — Classic single-diploid Ne history; a useful baseline, but sensitive to heterozygosity and ROH in grape, and to hybrid origin. Input: consensus diploid FASTA. Output: Ne trajectory. Version: [待确认] (repo has unusual latest tag fixed-max-t) (GitHub lh3/psmc; Bioconda psmc; tag is not a clean version number). [doi:10.1038/nature10231](https://doi.org/10.1038/nature10231) · [link](https://github.com/lh3/psmc)  
  Note: Version tag is messy; pin a commit and record it. Highly homozygous lines such as PN40024 are a poor sole input. Hybrid-origin cultivars (for example crosses between eastern and western groups, or with sylvestris introgression) can show a false old Ne peak because the two haplotypes come from different sources. Convert to years only with an explicit generation-time assumption. Clonal propagation does not add meiotic generations; the sample time should be the sexual origin. Tag on GitHub is not a clean version number [待确认].
- **SMC++** (tool) — Effective-size history from many unphased genomes. Input: VCF, population labels. Output: Ne trajectory. Version: 1.15.2 (GitHub popgenmethods/smcpp + Bioconda, 2026-11-14 CST). [doi:10.1038/ng.3748](https://doi.org/10.1038/ng.3748) · [link](https://github.com/popgenmethods/smcpp)  
  Note: Reduce clones and duplicates to one sample per group. For recent Ne, also remove or model first-degree relatives (see docs/WORKFLOW.md). Clone-prune first. Convert to years only with an explicit generation-time assumption. For a clonal cultivar, the sample time should be the sexual origin, not the extraction year. Hybrid-origin diploids can distort the trajectory.
- **Generation time and mutation rate as explicit assumptions (idea)** (idea) — SMC, ARG and SFS models convert results to years only after stating generation time and mutation rate. In a clonal crop, a generation is the interval between sexual generations. Germline and somatic rates are different quantities (see vitis-open-directions item 13). Input: model output in generations. Output: year-scaled results. Version: n/a (genetics review, 2026-11-14 CST).  
  Note: Numerical values are not recommended here; they need a genetics and statistics review, and a sensitivity analysis [待确认].
- **Sexual-origin time as the sample date (idea)** (idea) — Clonal cultivars do not accumulate meiotic generations after their origin. For tsdate, Relate, SINGER and MSMC2, the sample time should be the cultivar's sexual origin, not the year of DNA extraction. Keep one record per clone. The origin date is usually unknown and should be a parameter or a sensitivity analysis, not a known constant. Somatic mutations during clonal propagation can appear as a few overly long ARG tip branches. Input: origin-date estimates. Output: sample-time table. Version: n/a (catalogue revision, 2026-11-14 CST).  
  Note: Do not invent a default origin date or mutation rate here. Numerical values remain [待确认].

<a id="section-5"></a>
## 5. Selection scans

<!-- PROSE:SECTION:P05 -->
Window diversity, haplotype and CLR scans, and structure-aware outliers. Grape domestication often involves selecting a single seedling and propagating it clonally—a single sampling event rather than a classic multi-generation hard sweep—so hard-sweep signals may be weak, whereas soft sweeps or gene flow from *sylvestris* may be more common. Domestication bottlenecks and hybrid origins can produce false positives; therefore, use simulations matched to grapevine history as the null, as already noted for diploS/HIC. XP-CLR and FST outliers describe differentiation between wild and cultivated groups and do not by themselves demonstrate selection. Contrast groups after removing clones, and handle first-degree relatives as outlined in the workflow.
<!-- /PROSE:SECTION:P05 -->

**Clusters:**
- *Diversity and differentiation windows (complementary)*: pixy, scikit-allel.
- *Environment and structure-aware outliers (alternatives)*: BayPass, BayeScan, LFMM 2, OutFLANK, pcadapt.
- *Sweep scans, haplotype (alternatives)*: hapFLK, rehh, selscan.
- *Sweep scans, machine learning (alternatives)*: diploS/HIC.
- *Sweep scans, site-frequency or CLR (alternatives)*: RAiSD, SweepFinder2, XP-CLR.

- **pixy** (tool) — Unbiased pi, dxy and Fst from all-sites VCFs, including invariant sites. Input: all-sites VCF, population file. Output: window statistics. Version: 2.2.5 (GitHub ksamuk/pixy 2026-09-18; conda-forge still 2.2.4). [doi:10.1111/1755-0998.13326](https://doi.org/10.1111/1755-0998.13326) · [link](https://github.com/ksamuk/pixy)  
  Note: Newest GitHub is 2.2.5; conda-forge lagged at 2.2.4. AM11 still recorded 2.2.4.
- **scikit-allel** (tool) — Python library for window diversity, Fst, Patterson f-statistics and plotting. Input: VCF or zarr. Output: statistics, plots. Version: 1.3.13 (GitHub cggh/scikit-allel + Bioconda/PyPI, 2026-11-14 CST). [link](https://github.com/cggh/scikit-allel)
- **BayPass** (tool) — Bayesian XtX differentiation and genotype-environment association. Input: allele counts, covariates. Output: XtX, association. Version: 3.1 (Bioconda baypass, 2026-11-14 CST). [doi:10.1534/genetics.115.181453](https://doi.org/10.1534/genetics.115.181453) · [link](https://forgemia.inra.fr/gguirao/baypass)  
  Note: Current official URL should be re-checked if the Forge moves [待确认].
- **BayeScan** (tool) — Older Fst-outlier Bayesian scan; keep only as a legacy comparison. Input: allele counts. Output: outlier q-values. Version: 2.1 (Bioconda bayescan, 2026-11-14 CST). [link](http://www.cmpg.unibe.ch/software/BayeScan/)  
  Note: Prefer pcadapt, OutFLANK or BayPass for new work.
- **LFMM 2** (tool) — Latent-factor mixed model for genotype-environment association. Input: genotypes, environmental variables. Output: association p-values. Version: 1.1 (GitHub bcm-uga/lfmm tag 1.1; Caye et al. 2019 paper verified). [doi:10.1093/molbev/msz008](https://doi.org/10.1093/molbev/msz008) · [link](https://github.com/bcm-uga/lfmm)  
  Note: Also listed under section 9. Version source: GitHub bcm-uga/lfmm 1.1; also packaged in Bioconductor LEA.
- **OutFLANK** (tool) — Fst outlier test with a trimmed-null among loci. Input: Fst per locus. Output: outliers. Version: [待确认] (GitHub whitlock/OutFLANK; no tag in this check). [link](https://github.com/whitlock/OutFLANK)  
  Note: Version [待确认].
- **pcadapt** (tool) — PCA-based outlier scan for selection, robust to some population structure. Input: genotypes. Output: outlier p-values. Version: 4.4.1 (CRAN pcadapt, 2026-11-14 CST). [doi:10.1111/1755-0998.12592](https://doi.org/10.1111/1755-0998.12592) · [link](https://github.com/bcm-uga/pcadapt)
- **hapFLK** (tool) — Haplotype Fst that accounts for population structure, useful for cultivar-group contrasts. Input: haplotypes, kinship or tree. Output: hapFLK scores. Version: 2.1 (PyPI hapflk 2.1 (2024-05-16), 2026-11-14 CST; official source INRAE Forge). [doi:10.1534/genetics.112.147231](https://doi.org/10.1534/genetics.112.147231) · [link](https://forgemia.inra.fr/bertrand.servin/hapflk)  
  Note: The previous GitHub URL bioinfo-lessmieux/hapflk returned 404 (checked 2026-11-14). Version source is PyPI 2.1; the Forge page may require a login. Bioconda version [待确认]. DOI is Fariello et al. 2013.
- **rehh** (tool) — R implementation of EHH-based scans and plots. Input: haplotypes. Output: iHS, XP-EHH, plots. Version: 3.2.3 (CRAN rehh, 2026-11-14 CST). [link](https://cran.r-project.org/package=rehh)
- **selscan** (tool) — iHS, nSL, XP-EHH and related haplotype scans, including unphased scans in 2.0+. Input: haplotypes or unphased genotypes, map. Output: scan scores. Version: 3.1.0 (GitHub szpiech/selscan + Bioconda, 2026-11-14 CST). [doi:10.1093/bioinformatics/btae006](https://doi.org/10.1093/bioinformatics/btae006) · [link](https://github.com/szpiech/selscan)  
  Note: DOI is Szpiech 2024 (selscan 2.0). Original 2014 paper is doi:10.1093/molbev/msu211. Newest tag is 3.1.0.
- **diploS/HIC** (tool) — Classifier for hard, soft and linked sweeps from window features, trained on simulations. Input: genotypes, trained model. Output: sweep classes. Version: 1.1.0 (GitHub kern-lab/diploSHIC + Bioconda, 2026-11-14 CST). [link](https://github.com/kern-lab/diploSHIC)  
  Note: Train on grape-like demography and clonality; off-the-shelf human models are not appropriate.
- **RAiSD** (tool) — Composite sweep statistic from mu, mu-var and mu-SFS; listed in AM11. Input: VCF or FASTA-like. Output: outlier windows. Version: [待确认] (no tagged release) (GitHub alachins/raisd exists (updated 2026-11-04) but no tag in this check). [doi:10.1038/s42003-018-0085-8](https://doi.org/10.1038/s42003-018-0085-8) · [link](https://github.com/alachins/raisd)  
  Note: Version remains [待确认], as in AM11.
- **SweepFinder2** (tool) — CLR sweep scan that can include a demographic background SFS. Input: allele frequencies, background SFS. Output: CLR scores. Version: 1.0 (Bioconda sweepfinder2, 2026-11-14 CST). [link](https://degiorgioroup.github.io/Website/computer.html)  
  Note: Official URL should be confirmed against the current lab page [待确认] (if the URL moves).
- **XP-CLR** (tool) — Cross-population composite likelihood ratio for sweeps, e.g. wild versus cultivated after clone removal. Input: allele frequencies, map. Output: XP-CLR scores. Version: 1.1.2 (GitHub hardingnj/xpclr + Bioconda, 2026-11-14 CST (also AM11)). [doi:10.1101/gr.100545.109](https://doi.org/10.1101/gr.100545.109) · [link](https://github.com/hardingnj/xpclr)

<a id="section-6"></a>
## 6. Introgression and f-statistics

<!-- PROSE:SECTION:P06 -->
f-statistics, admixture graphs, and hybrid tests, complementary to TreeMix and local ancestry. A non-zero D-statistic can arise from ancestral population structure rather than gene flow alone. A negative f3 indicates admixture, whereas a non-negative f3 does not rule it out, as genetic drift in the target can mask the signal. Define groups by geography or use type before testing for admixture; do not define groups based on the mixture signal under test. When a pseudo-haploid ancient sample serves as the f3 target, the heterozygosity term requires separate handling.
<!-- /PROSE:SECTION:P06 -->

**Clusters:**
- *Admixture date and painting (complementary)*: TreeMix.
- *Hybrid detection (alternatives)*: HyDe.
- *f-statistics and graphs (alternatives)*: ADMIXTOOLS (qpDstat, qp3Pop, qpAdm, qpGraph), ADMIXTOOLS 2, Dsuite.
- *Foundational f-statistic papers (complementary)*: Green et al. 2010 D statistic, Durand et al. 2011 D statistic, Reich et al. 2009 f-statistics, Peter 2016 f-statistics, Haak et al. 2015 qpAdm, Harney et al. 2021 qpAdm performance.

- **TreeMix** (tool) — Migration edges on a population tree; complementary to f-statistic graphs. Input: allele counts. Output: graph, residuals. Version: 1.12 (see section 3). [doi:10.1371/journal.pgen.1002967](https://doi.org/10.1371/journal.pgen.1002967) · [link](https://github.com/joepickrell/treemix)  
  Note: Same binary as section 3; listed here for the introgression workflow.
- **HyDe** (tool) — Site-pattern test for hybridisation in phylogenetic trios. Input: alignment, triples. Output: hybridisation p-values. Version: 1.0.2 (GitHub pblischak/HyDe + Bioconda, 2026-11-14 CST). [link](https://github.com/pblischak/HyDe)
- **ADMIXTOOLS (qpDstat, qp3Pop, qpAdm, qpGraph)** (tool) — Original C implementation of Patterson f-statistics and admixture-graph tools. Input: EIGENSTRAT or PACKEDANCESTRYMAP. Output: f-statistics, qpAdm, graphs. Version: 8.0.2 (GitHub DReichLab/AdmixTools + Bioconda, 2026-11-14 CST). [doi:10.1534/genetics.112.145037](https://doi.org/10.1534/genetics.112.145037) · [link](https://github.com/DReichLab/AdmixTools)  
  Note: DOI is Patterson et al. 2012. Prefer ADMIXTOOLS 2 for new analyses unless a pipeline is pinned to the C binary.
- **ADMIXTOOLS 2** (tool) — f2, f3, f4, qpAdm and qpGraph in R, with block jackknife. Input: genotype or f2 blocks. Output: f-statistics, admixture graphs. Version: 2.0.1 (GitHub uqrmaie1/admixtools v2.0.1, 2026-11-14 CST (also AM13)). [doi:10.7554/elife.85492](https://doi.org/10.7554/elife.85492) · [link](https://github.com/uqrmaie1/admixtools)  
  Note: Default alternative in AM13. Maier et al. 2023 eLife DOI verified.
- **Dsuite** (tool) — Fast D, f4-ratio and f-branch statistics with block jackknife. Input: VCF, tree or trio file. Output: D, f4, f-branch tables. Version: [待确认] (no tagged release) (GitHub millanek/Dsuite; no tag or Bioconda package in this check (same as AM13)). [doi:10.1111/1755-0998.13265](https://doi.org/10.1111/1755-0998.13265) · [link](https://github.com/millanek/Dsuite)  
  Note: Version remains [待确认], as in AM13. The 2021 paper DOI was verified.
- **Green et al. 2010 D statistic** (paper) — Neandertal-genome paper that introduced the D statistic used in ABBA-BABA tests. Input: n/a. Output: n/a. Version: n/a (Crossref-verified in the literature review, 2026-11-14 CST). [doi:10.1126/science.1188021](https://doi.org/10.1126/science.1188021) · [link](https://doi.org/10.1126/science.1188021)  
  Note: Literature addition; wording is deliberately general.
- **Durand et al. 2011 D statistic** (paper) — Formal properties of the D statistic. Input: n/a. Output: n/a. Version: n/a (Crossref-verified in the literature review, 2026-11-14 CST). [doi:10.1093/molbev/msr048](https://doi.org/10.1093/molbev/msr048) · [link](https://doi.org/10.1093/molbev/msr048)  
  Note: Literature addition; wording is deliberately general.
- **Reich et al. 2009 f-statistics** (paper) — Introduces f3 and f4 statistics. Input: n/a. Output: n/a. Version: n/a (Crossref-verified in the literature review, 2026-11-14 CST). [doi:10.1038/nature08365](https://doi.org/10.1038/nature08365) · [link](https://doi.org/10.1038/nature08365)  
  Note: Literature addition; wording is deliberately general.
- **Peter 2016 f-statistics** (paper) — Interpretation of f2, f3 and f4 under structure and admixture. Input: n/a. Output: n/a. Version: n/a (Crossref-verified in the literature review, 2026-11-14 CST). [doi:10.1534/genetics.115.183913](https://doi.org/10.1534/genetics.115.183913) · [link](https://doi.org/10.1534/genetics.115.183913)  
  Note: Literature addition; wording is deliberately general.
- **Haak et al. 2015 qpAdm** (paper) — Steppe-migration study usually cited as the origin of qpAdm (method in the supplement, not re-read here). Input: n/a. Output: n/a. Version: n/a (Crossref-verified in the literature review, 2026-11-14 CST). [doi:10.1038/nature14317](https://doi.org/10.1038/nature14317) · [link](https://doi.org/10.1038/nature14317)  
  Note: Literature addition; wording is deliberately general.
- **Harney et al. 2021 qpAdm performance** (paper) — Simulation study of qpAdm power and false positives. Input: n/a. Output: n/a. Version: n/a (Crossref-verified in the literature review, 2026-11-14 CST). [doi:10.1093/genetics/iyaa045](https://doi.org/10.1093/genetics/iyaa045) · [link](https://doi.org/10.1093/genetics/iyaa045)  
  Note: Literature addition; wording is deliberately general.

<a id="section-7"></a>
## 7. LD and recombination

<!-- PROSE:SECTION:P07 -->
Prefer a published grape linkage map interpolated onto the working reference. LD-based maps serve as ARG input only, not SHAPEIT5 input (AM26). Clonal propagation itself does not alter LD; instead, estimates are biased by duplicate samples, relatedness, inbreeding (where the effective recombination rate is approximately r(1 − F)), and population admixture. Polarisation with est-sfs is placed in section 10, as it is a prerequisite for genetic load, DFE, and ARG analyses rather than an LD method.
<!-- /PROSE:SECTION:P07 -->

**Clusters:**
- *LD decay and blocks (complementary)*: LDBlockShow, PopLDdecay.
- *LD-based recombination maps (alternatives, ARG input only)*: LDhelmet, ReLERNN, pyrho.

- **LDBlockShow** (tool) — LD heatmaps and haplotype blocks around candidate loci. Input: VCF, region. Output: plots, blocks. Version: 1.41 (GitHub BGI-shenzhen/LDBlockShow + Bioconda, 2026-11-14 CST). [link](https://github.com/BGI-shenzhen/LDBlockShow)
- **PopLDdecay** (tool) — LD decay curves by population, a standard first plot after clone removal. Input: VCF. Output: decay tables, plots. Version: 3.45 (GitHub BGI-shenzhen/PopLDdecay + Bioconda, 2026-11-14 CST). [link](https://github.com/BGI-shenzhen/PopLDdecay)
- **LDhelmet** (tool) — Alternative LD-based map, slower, used only if pyrho is unsuitable. Input: phased haplotypes. Output: recombination map. Version: 1.10 (Bioconda ldhelmet, 2026-11-14 CST (also AM26)). [link](https://sourceforge.net/projects/ldhelmet/)  
  Note: AM26 alternative to pyrho.
- **ReLERNN** (tool) — Recurrent-network estimator of recombination from simulations; treat as experimental on grape. Input: genotypes, simulations. Output: recombination map. Version: 2.0.0 (GitHub kr-colab/ReLERNN + Bioconda, 2026-11-14 CST). [link](https://github.com/kr-colab/ReLERNN)  
  Note: Train on grape-like demography; do not reuse a human model.
- **pyrho** (tool) — LD-based recombination rates. In AM26 it is used only as ARG input, never for SHAPEIT5 phasing. Input: phased haplotypes, Ne history. Output: recombination map. Version: 0.2.1 (Bioconda pyrho, 2026-11-14 CST (also AM26)). [doi:10.1126/sciadv.aaw9206](https://doi.org/10.1126/sciadv.aaw9206) · [link](https://github.com/popgenmethods/pyrho)  
  Note: Run per population after clone and first-degree pruning. See AM26 for why clonality and admixture LD bias rho.

<a id="section-8"></a>
## 8. ROH, inbreeding, kinship and clonality

<!-- PROSE:SECTION:P08 -->
Clonality is not merely a nuisance: a genotype remains frozen without segregation or recombination, somatic variants accumulate, and chimerism can be stratified across cell layers (L1/L2). ROH length retains its standard interpretation: long ROH reflect recent inbreeding or selfing (hermaphroditic cultivars can self, and PN40024 is an inbred line), whereas short ROH reflect older bottlenecks. Clonal propagation does not generate ROH. Identity checks inform every downstream section, and clones and first-degree relatives are not treated the same way.
<!-- /PROSE:SECTION:P08 -->

**Clusters:**
- *Kinship, IBD and clonality (complementary)*: GCTA, KING, VIVC, ngsRelate.
- *ROH callers (alternatives)*: GARLIC, RZooRoH, bcftools roh.
- *ROH callers, low coverage (alternatives)*: hapROH, ROHan.
- *Low-coverage kinship (complementary)*: READv2, KIN (KINgaroo), BREADR.

- **GCTA** (tool) — GRM-based relatedness and GBLUP; also used in GWAS (section 9). Input: BED. Output: GRM, heritability. Version: 1.94.1 (GitHub jianyangqt/gcta + Bioconda, 2026-11-14 CST). [link](https://yanglab.westlake.edu.cn/software/gcta/)
- **KING** (tool) — Robust kinship for clones or duplicates versus first-degree relatives. Clones and duplicates (kinship above 0.354) are reduced to one sample per group; first-degree relatives (0.177-0.354) are registered, not dropped as the same genotype. Input: hard-called diploid genotypes (BED). Output: kinship. Version: 2.3.2 (see section 1). [doi:10.1093/bioinformatics/btq559](https://doi.org/10.1093/bioinformatics/btq559) · [link](https://www.kingrelatedness.com/)  
  Note: Thresholds follow the KING manual (https://www.kingrelatedness.com/manual.shtml): kinship above 0.354 is the duplicate/MZ class; 0.177-0.354 is first-degree. Paper: Manichaikul et al. 2010, 10.1093/bioinformatics/btq559. AM26 used 0.177 as the first-degree lower cutoff. Input should be hard-called diploid genotypes (BED). For low-coverage or ancient samples use ngsRelate, READv2, KIN or BREADR instead. Handling of first-degree relatives is analysis-specific; see docs/WORKFLOW.md.
- **VIVC** (resource) — Public cultivar name registry, used with KING to attach living names to genotypes (AM04). Input: cultivar names. Output: accepted names, synonyms. Version: n/a (live database) (vivc.de, checked as the public cultivar name registry). [link](https://www.vivc.de/)  
  Note: Not software. Do not upload unpublished genotype matrices to this repository.
- **ngsRelate** (tool) — Relatedness from genotype likelihoods, including low-coverage data. Input: ANGSD genotype likelihoods. Output: relatedness. Version: 2.3.1 (GitHub ANGSD/NgsRelate + Bioconda, 2026-11-14 CST). [doi:10.1093/gigascience/giz034](https://doi.org/10.1093/gigascience/giz034) · [link](https://github.com/ANGSD/NgsRelate)
- **GARLIC** (tool) — ROH caller that models length classes explicitly. Input: BED or genotypes. Output: ROH classes. Version: 1.1.6 (GitHub szpiech/garlic + Bioconda, 2026-11-14 CST). [link](https://github.com/szpiech/garlic)
- **RZooRoH** (tool) — HMM caller that partitions the genome into multiple HBD (autozygous) classes. Input: genotypes. Output: ROH classes, inbreeding. Version: 0.4.3 (CRAN RZooRoH, 2026-11-14 CST). [link](https://cran.r-project.org/package=RZooRoH)
- **bcftools roh** (tool) — HMM runs of homozygosity. AM12 uses population allele frequencies after clone removal, not a default AF file. Input: VCF, population AF file. Output: ROH tables. Version: 1.25 (same bcftools 1.25 as section 1; also AM12). [doi:10.1093/bioinformatics/btw044](https://doi.org/10.1093/bioinformatics/btw044) · [link](https://github.com/samtools/bcftools)  
  Note: Default ROH tool in AM12. ROH method paper: Narasimhan et al. 2016, 10.1093/bioinformatics/btw044. The samtools/bcftools suite DOI 10.1093/gigascience/giab008 still applies to the package.
- **hapROH** (tool) — ROH from low-coverage data using a haplotype reference panel. Designed and tested on human data (1240k / 1000 Genomes panels). Not a clonal-history method: clonal propagation does not create ROH. Input: pseudo-haploid or low-coverage genotypes, reference panel. Output: ROH, inbreeding. Version: 0.70 (GitHub/PyPI hapROH 0.70; Bioconda 0.64). [doi:10.1038/s41467-021-25289-w](https://doi.org/10.1038/s41467-021-25289-w) · [link](https://github.com/hringbauer/hapROH)  
  Note: Human-specific as distributed. Use on Vitis only after building a Vitis phased haplotype panel and validating on modern grapes downsampled to the target depth; unvalidated results must not be reported. ROH reflects inbreeding at the sexual origin of the sampled genotype, not centuries of clonal propagation. Prefer species-general ROHan, or bcftools roh when depth is sufficient. Newest is 0.70 on GitHub/PyPI; Bioconda lagged at 0.64.
- **ROHan** (tool) — Joint estimate of heterozygosity and ROH from a single BAM, with optional damage correction, and without a human haplotype panel. A species-general alternative to hapROH. The paper reports usable depth as low as 5−6x on modern samples and 7−8x on ancient samples with moderate DNA damage. Input: BAM. Output: heterozygosity and ROH tracts. Version: v1.0.7 (GitHub grenaud/ROHan release v1.0.7, checked 2026-11-14 CST). [doi:10.1534/genetics.119.302057](https://doi.org/10.1534/genetics.119.302057) · [link](https://github.com/grenaud/ROHan)  
  Note: ROH still reflects inbreeding at sexual origin, not clonal history.
- **READv2** (tool) — Relatedness from pairwise mismatch rates on pseudo-haploid low-coverage data (up to third degree). Developed on human data; calibrate on modern grape clone and relative pairs downsampled to the same depth. Noraz et al. 2026 (doi:10.1038/s41467-026-70166-z) recalibrated it for grape clones against VIVC, as confirmed against that paper in the 2026-11-14 literature re-review. Input: pseudo-haploid PLINK or EIGENSTRAT. Output: relatedness class. Version: 2.1.1 (GitHub GuntherLab/READv2 release 2.1.1, checked 2026-11-14 CST). [doi:10.1186/s13059-024-03350-3](https://doi.org/10.1186/s13059-024-03350-3) · [link](https://github.com/GuntherLab/READv2)  
  Note: This is the current READ lineage; the original READ paper (10.1371/journal.pone.0195491) is not a second tool entry.
- **KIN (KINgaroo)** (tool) — HMM of IBD segments from low coverage (down to about 0.05x in the human tests), with optional contamination correction and an ROH model. Grape use needs calibration. Input: BAM via KINgaroo. Output: relatedness class and IBD segments. Version: v3.1.4 (GitHub DivyaratanPopli/Kinship_Inference release v3.1.4, checked 2026-11-14 CST). [doi:10.1186/s13059-023-02847-7](https://doi.org/10.1186/s13059-023-02847-7) · [link](https://github.com/DivyaratanPopli/Kinship_Inference)
- **BREADR** (tool) — Posterior probabilities of identical/twins, first-degree, second-degree or unrelated on ultra-low-coverage pseudo-haploid data. The identical class can be used for clone matching between ancient pips and living cultivars after calibration. Input: EIGENSTRAT. Output: relatedness-class posteriors. Version: 1.1.0 (CRAN BREADR 1.1.0, checked 2026-11-14 CST). [doi:10.32614/CRAN.package.BREADR](https://doi.org/10.32614/CRAN.package.BREADR) · [link](https://cran.r-project.org/package=BREADR)

<a id="section-9"></a>
## 9. GWAS, GEA and landscape genomics

<!-- PROSE:SECTION:P09 -->
Mixed-model GWAS, crop platforms, meta-analysis, genomic prediction, and genotype-environment association.
<!-- /PROSE:SECTION:P09 -->

**Clusters:**
- *GEA and landscape genomics (alternatives)*: BayPass, LFMM 2, dartR, wingen.
- *Meta-analysis and prediction (complementary)*: BGLR, LDSC, METAL, metafor, rrBLUP.
- *Mixed-model GWAS (alternatives)*: GEMMA, SAIGE, regenie.
- *Plant GWAS platforms (alternatives)*: GAPIT, TASSEL, rMVP.

- **BayPass** (tool) — Bayesian GEA and differentiation, reused from section 5. Input: allele counts, covariates. Output: XtX, association. Version: 3.1 (see section 5). [doi:10.1534/genetics.115.181453](https://doi.org/10.1534/genetics.115.181453) · [link](https://forgemia.inra.fr/gguirao/baypass)
- **LFMM 2** (tool) — Genotype-environment association with latent factors. Input: genotypes, environment. Output: association. Version: 1.1 (see section 5). [doi:10.1093/molbev/msz008](https://doi.org/10.1093/molbev/msz008) · [link](https://github.com/bcm-uga/lfmm)  
  Note: Same tool as section 5. Same 1.1 line as the LFMM 2 row in section 5.
- **dartR** (tool) — R toolkit for SNP population genetics and some landscape analyses, originally around DArT data. Input: genotypes. Output: diversity, structure, plots. Version: 2.7.2 (GitHub green-striped-gecko/dartR, 2026-11-14 CST). [link](https://github.com/green-striped-gecko/dartR)
- **wingen** (tool) — Mapped genomic diversity and adaptive variation from georeferenced samples. Input: genotypes, public coordinates. Output: maps. Version: 2.2.0 (CRAN wingen, 2026-11-14 CST). [link](https://cran.r-project.org/package=wingen)  
  Note: Public coordinates only.
- **BGLR** (tool) — Bayesian genomic prediction. Input: markers, phenotypes. Output: GEBV, accuracy. Version: 1.1.4 (CRAN BGLR, 2026-11-14 CST (also AM24)). [link](https://cran.r-project.org/package=BGLR)  
  Note: AM24: one sample per clone or duplicate group; keep clones, and first-degree relatives, in the same cross-validation fold.
- **LDSC** (tool) — LD-score intercepts for inflation and sample overlap in meta-analysis (AM24). Input: summary statistics, LD scores. Output: intercepts, heritability. Version: 1.0.1 (Bioconda ldsc 1.0.1; GitHub tag still v1.0.0). [link](https://github.com/bulik/ldsc)  
  Note: AM24: use only above a minimum number of SNPs and samples fixed in advance. Human-style LD scores are not a grape map.
- **METAL** (tool) — Fixed-effect GWAS meta-analysis; default in AM24. Input: summary statistics. Output: meta-analysis table. Version: 2020-05-05 (GitHub statgen/METAL, 2026-11-14 CST (also AM24)). [link](https://github.com/statgen/METAL)
- **metafor** (tool) — Random-effects meta-analysis (REML, Hartung–Knapp) when studies are few. Input: effect sizes. Output: pooled estimates. Version: 5.2-1 (CRAN metafor, 2026-11-14 CST (also AM24)). [link](https://cran.r-project.org/package=metafor)  
  Note: AM24 uses this when fewer than five studies.
- **rrBLUP** (tool) — Ridge-regression / GBLUP genomic prediction, AM24 alternative. Input: markers, phenotypes. Output: GEBV, accuracy. Version: 4.6.3 (CRAN rrBLUP, 2026-11-14 CST (also AM24)). [link](https://cran.r-project.org/package=rrBLUP)
- **GEMMA** (tool) — Linear mixed-model GWAS; default per-study tool in AM24. Input: BED, phenotypes, relatedness. Output: association, PVE. Version: 0.98.5 (GitHub genetics-statistics/GEMMA + Bioconda, 2026-11-14 CST (also AM24)). [doi:10.1038/ng.2310](https://doi.org/10.1038/ng.2310) · [link](https://github.com/genetics-statistics/GEMMA)  
  Note: Keep clones in the same cross-validation fold (AM24).
- **SAIGE** (tool) — Saddle-point mixed-model GWAS, mainly for binary traits. Input: genotypes, phenotypes. Output: association. Version: 0.29.5 (GitHub weizhouUMICH/SAIGE, 2026-11-14 CST). [link](https://github.com/weizhouUMICH/SAIGE)  
  Note: More common in human data; usable if a grape trait is binary and sample size is large.
- **regenie** (tool) — Fast whole-genome regression GWAS, AM24 alternative to GEMMA. Input: BED/PGEN, phenotypes. Output: association. Version: 4.1.3.1 (Bioconda regenie 4.1.3.1; GitHub tag v4.1.3 (2026-09-08)). [doi:10.1038/s41588-021-00870-7](https://doi.org/10.1038/s41588-021-00870-7) · [link](https://github.com/rgcgithub/regenie)  
  Note: Bioconda has a patch letter (4.1.3.1) on top of GitHub v4.1.3.
- **GAPIT** (tool) — R platform wrapping FarmCPU, BLINK, MLMM and related crop GWAS methods. Input: genotypes, phenotypes. Output: association, plots. Version: GAPIT4 (GitHub tag GAPIT4) (GitHub jiabowang/GAPIT3 tag GAPIT4, 2026-11-14 CST). [link](https://github.com/jiabowang/GAPIT3)  
  Note: Repository name still says GAPIT3; newest tag is GAPIT4. Record the exact tag you run.
- **TASSEL** (tool) — Long-standing crop GUI and command-line GWAS and diversity tool. Input: genotypes, phenotypes. Output: association, PCA, Kinship. Version: [待确认] (Official site; version not checked in this build). [link](https://www.maizegenetics.net/tassel)  
  Note: Version [待确认].
- **rMVP** (tool) — Memory-efficient crop GWAS and Manhattan plots. Input: genotypes, phenotypes. Output: association, plots. Version: 1.0.4 (CRAN rMVP, 2026-11-14 CST). [link](https://github.com/xiaolei-lab/rMVP)

<a id="section-10"></a>
## 10. Genetic load and deleterious mutations

<!-- PROSE:SECTION:P10 -->
Annotate variant effects, polarise to derived alleles, and report genetic load both with and without ROH as a covariate (AM12). Count derived alleles rather than simply non-reference alleles, because the reference allele is not the ancestral allele. A reference genome represents one individual's haplotype, so deleterious derived alleles carried by that individual would be missed if load were counted as non-reference. This logic does not depend on PN40024 being nearly homozygous; homozygosity simply means the reference approximates a single haplotype. Population data primarily measure germline load inherited at sexual origin, whereas somatic load accumulated during clonal propagation is a distinct quantity (see vitis-open-directions items 13 and 16). Report hemizygous and heterozygous (masked) recessive load separately.
<!-- /PROSE:SECTION:P10 -->

**Clusters:**
- *Polarisation (before DFE, load and ARG) (in order)*: est-sfs.
- *Distribution of fitness effects (alternatives)*: Grapes (DFE), polyDFE.
- *Variant-effect annotation (alternatives)*: Ensembl VEP, PlantCaduceus, SnpEff.

- **est-sfs** (tool) — Probabilistic ancestral-state estimation from multiple outgroups. Input: outgroup bases, site counts. Output: ancestral probabilities. Version: 2.04 (AM26 (2026-11-14); not re-checked against a public tag in this session). [link](https://sourceforge.net/projects/est-usfs/)  
  Note: Polarisation is a prerequisite for unfolded DFE, load and ARG work, not an LD tool. Use two or more outgroups, never Muscadinia alone (AM26).
- **Grapes (DFE)** (tool) — Gamma and related DFE models from SNP counts. Not the grape crop. Input: site counts. Output: DFE parameters. Version: v1.1.1 (GitHub BioPP/grapes release v1.1.1, checked 2026-11-14 CST). [doi:10.1371/journal.pgen.1005774](https://doi.org/10.1371/journal.pgen.1005774) · [link](https://github.com/BioPP/grapes)  
  Note: Official repository is BioPP/grapes (Galtier 2016). The previous GitHub URL bioinfo-lessmieux/grapes returned 404. Whether conda-forge package grapes 0.10.4 is the same software remains [待确认]; it is not used as the catalogue version.
- **polyDFE** (tool) — Estimates the distribution of fitness effects from SFS, folded or unfolded. Input: SFS, optionally polarised. Output: DFE parameters. Version: 2.0 (GitHub paula-tataru/polyDFE tag v2.0, 2026-11-14 CST). [link](https://github.com/paula-tataru/polyDFE)  
  Note: Polarise as in AM26 before unfolded analyses.
- **Ensembl VEP** (tool) — Alternative effect predictor; Ensembl Plants caches must match the chosen grape assembly. Input: VCF, cache. Output: annotated VCF or TSV. Version: 116.3 (GitHub Ensembl/ensembl-vep release/116.3, 2026-11-14 CST). [link](https://github.com/Ensembl/ensembl-vep)  
  Note: Confirm that a Vitis cache exists for the assembly you use [待确认] (cache).
- **PlantCaduceus** (tool) — Optional plant variant-effect scores, listed as experimental in AM12. Input: variants, model. Output: scores. Version: [待确认] (plantcad/plantcad-dev exists (updated 2026-04-23); no stable tag in this check (also AM12)). [link](https://github.com/plantcad/plantcad-dev)  
  Note: Version [待确认]. Do not treat unpublished model weights as a repo file.
- **SnpEff** (tool) — Annotates variants against a local database built from the chosen grape annotation (AM12: DS01). Input: VCF, SnpEff database. Output: annotated VCF. Version: 5.4.0c (Bioconda snpeff 5.4.0c; GitHub tag v5.4c (also AM12)). [doi:10.4161/fly.19695](https://doi.org/10.4161/fly.19695) · [link](https://pcingola.github.io/SnpEff/)  
  Note: Count load on derived alleles after polarisation (AM26), not on non-reference alleles, because the reference allele is not the ancestral allele.

<a id="section-11"></a>
## 11. Structural variants and pangenome-graph popgen

<!-- PROSE:SECTION:P11 -->
Pointers only: graph construction and the full tool list reside in vitis-pangenome. Long-read SV callers and the post-calling merge step are listed separately; this section is not a short-read SV catalogue.
<!-- /PROSE:SECTION:P11 -->

**Clusters:**
- *SV merging across samples (in order, after calling)*: Jasmine.
- *Long-read SV calling (alternatives)*: Sniffles2, cuteSV.
- *Graph genotyping (alternatives; details live in vitis-pangenome)*: PanGenie, vg (Giraffe + vg call).
- *Graph statistics (complementary)*: odgi.

- **Jasmine** (tool) — Merges structural-variant callsets across samples after per-sample calling. Input: per-sample SV VCF. Output: merged SV VCF. Version: 1.1.5 (GitHub mkirsche/Jasmine v1.1.5; Bioconda 1.1 (AM18 recorded 1.1)). [link](https://github.com/mkirsche/Jasmine)  
  Note: This is a downstream merge step, not an alternative caller. Use it after Sniffles2 or cuteSV, not as a substitute for them. Short-read SV callers are not listed here; see vitis-pangenome.
- **Sniffles2** (tool) — Default long-read structural-variant caller in this section. Input: long-read BAM. Output: SV VCF. Version: 2.8.1 (GitHub fritzsedlazeck/Sniffles + Bioconda, 2026-11-14 CST (also AM18)). [link](https://github.com/fritzsedlazeck/Sniffles)  
  Note: Long-read caller, not a short-read tool. Details and short-read SV methods live in vitis-pangenome.
- **cuteSV** (tool) — Alternative long-read structural-variant caller. Input: long-read BAM. Output: SV VCF. Version: 2.1.4 (GitHub tjiangHIT/cuteSV + Bioconda, 2026-11-14 CST (also AM18)). [link](https://github.com/tjiangHIT/cuteSV)  
  Note: Long-read caller, not a short-read tool. Details and short-read SV methods live in vitis-pangenome.
- **PanGenie** (tool) — k-mer genotyping of variants already in a pangenome graph. Input: short reads, graph or haplotypes. Output: VCF. Version: 4.2.2 (GitHub eblerjana/pangenie, 2026-11-14 CST (also AM07)). [link](https://github.com/eblerjana/pangenie)  
  Note: Pointer: vitis-pangenome section 5.
- **vg (Giraffe + vg call)** (tool) — Maps reads to a pangenome graph and genotypes graph variation. Input: reads, graph. Output: BAM-like GAM, VCF. Version: 1.78.0 (GitHub vgteam/vg, 2026-11-14 CST (also AM07, AM17)). [link](https://github.com/vgteam/vg)  
  Note: Do not duplicate the vitis-pangenome catalogue here. Use that repository for graph construction.
- **odgi** (tool) — Graph statistics and path similarity; a starting point for graph-aware popgen. Input: odgi/gfa graph. Output: stats, matrices. Version: 0.9.4 (GitHub pangenome/odgi + Bioconda, 2026-11-14 CST (also AM07)). [link](https://github.com/pangenome/odgi)  
  Note: Pointer: vitis-pangenome. Projects 15–17 in vitis-open-directions develop graph introgression, SV load and inversions.

<a id="section-12"></a>
## 12. Simulation

<!-- PROSE:SECTION:P12 -->
Coalescent and forward simulators, including clonal generations in SLiM. No official grape stdpopsim model was confirmed. The current Python forward simulator listed here is fwdpy11 (there is no fwdpy2).
<!-- /PROSE:SECTION:P12 -->

**Clusters:**
- *Coalescent simulators (alternatives to msprime)*: discoal, scrm.
- *Coalescent simulation (complementary)*: msprime, stdpopsim.
- *Forward or specialised simulation (alternatives)*: AlphaSimR, fwdpy11.
- *Forward simulation (alternatives)*: SLiM, pyslim.

- **discoal** (tool) — Coalescent simulations with selection, used to train sweep classifiers. Input: command-line model. Output: haplotypes. Version: 0.1.7 (GitHub kern-lab/discoal + Bioconda, 2026-11-14 CST). [link](https://github.com/kern-lab/discoal)
- **scrm** (tool) — Sequential coalescent with recombination, a fast ms-like simulator. Input: command-line model. Output: haplotypes. Version: 1.7.4 (GitHub scrm/scrm + Bioconda, 2026-11-14 CST). [link](https://github.com/scrm/scrm)
- **msprime** (tool) — Coalescent simulation and recapitation of tree sequences. Input: demes model or Python demography. Output: tree sequence, VCF. Version: 1.4.5 (conda-forge msprime, 2026-11-14 CST (also AM14)). [doi:10.1093/genetics/iyab229](https://doi.org/10.1093/genetics/iyab229) · [link](https://github.com/tskit-dev/msprime)  
  Note: Baumdicker et al. 2022 DOI verified (msprime 1.0).
- **stdpopsim** (tool) — Standardised simulation catalogue. AM14 records that no official grape model should be assumed. Input: species model id. Output: simulated genomes. Version: 0.3.0 (conda-forge stdpopsim, 2026-11-14 CST (also AM14)). [link](https://github.com/popsim-consortium/stdpopsim)  
  Note: No Vitis model was confirmed in the catalogue [待确认] (same caveat as AM14).
- **AlphaSimR** (tool) — Breeding-program simulation, useful for clonal selection and genomic prediction scenarios. Input: R founder haplotypes, crossing scheme. Output: simulated phenotypes and genotypes. Version: 2.1.0 (CRAN/GitHub AlphaSimR, 2026-11-14 CST). [link](https://github.com/gaynorr/AlphaSimR)
- **fwdpy11** (tool) — Python forward simulator built on fwdpp; can export tskit tree sequences. Input: Python model. Output: tree sequence. Version: 0.24.7 (PyPI fwdpy11 0.24.7 and GitHub molpopgen/fwdpy11 tag v0.24.7 (stable), 2026-11-14 CST; v0.24.8 releases are alpha/pre-release and are not used). [link](https://github.com/molpopgen/fwdpy11)  
  Note: There is no fwdpy2 repository under molpopgen; the current tool is fwdpy11. It is not described as built on tskit; tskit is an export format. DOI [待确认].
- **SLiM** (tool) — Forward simulation, including clonal generations relevant to grape. Input: SLiM script, tree-seq option. Output: tree sequence, VCF, individuals. Version: 5.2 (conda-forge slim, 2026-11-14 CST (also AM14)). [doi:10.1086/723601](https://doi.org/10.1086/723601) · [link](https://github.com/messerlab/SLiM)  
  Note: Verified DOI is Haller and Messer 2023 (SLiM 4). A paper specifically for SLiM 5 was not independently confirmed [待确认]. AM14 lists 5.2.
- **pyslim** (tool) — Links SLiM tree-sequence output to msprime recapitation and tskit. Input: SLiM tree sequence. Output: recapitated tree sequence. Version: 1.1.1 (PyPI and conda-forge 1.1.1; GitHub has 1.2.0b1 (beta, not used)). [link](https://github.com/tskit-dev/pyslim)  
  Note: Latest stable is 1.1.1. GitHub 1.2.0b1 is beta and is not used as the catalog version. Bioconda pyslim 0.401 is stale.

<a id="section-13"></a>
## 13. Visualization

<!-- PROSE:SECTION:P13 -->
Plotting tools used alongside the analyses above. Many method packages already generate their own figures.
<!-- /PROSE:SECTION:P13 -->

**Clusters:**
- *Association and ancestry plots (complementary)*: CMplot, ggtree, pophelper.
- *Maps and model drawings (complementary)*: demesdraw.

- **CMplot** (tool) — Circular and rectangular Manhattan and QQ plots for GWAS. Input: association tables. Output: plots. Version: 4.5.1 (CRAN CMplot, 2026-11-14 CST). [link](https://github.com/YinLiLin/CMplot)
- **ggtree** (tool) — Tree and annotation plots. Input: tree. Output: plots. Version: [待确认] (see section 3). [link](https://bioconductor.org/packages/ggtree/)
- **pophelper** (tool) — Standard ADMIXTURE/STRUCTURE bar plots. Input: Q files. Output: plots. Version: 2.3.1 (see section 2). [link](https://github.com/royfrancis/pophelper)  
  Note: Same tool as section 2.
- **demesdraw** (tool) — Draws demes demographic models. Input: demes YAML. Output: plots. Version: 0.4.1 (conda-forge demesdraw, 2026-11-14 CST). [link](https://github.com/popsim-consortium/demesdraw)

<a id="section-14"></a>
## 14. Workflows and pipelines

<!-- PROSE:SECTION:P14 -->
End-to-end workflows. The default analysis outline in this project remains the AM03-AM26 modules rather than a new pipeline in this repository.
<!-- /PROSE:SECTION:P14 -->

**Clusters:**
- *End-to-end workflows (alternatives)*: AM03–AM26 analysis modules, nf-core/sarek.

- **AM03–AM26 analysis modules** (workflow) — Project-level modules for calling, identity, diversity, ROH, ancestry, phasing, GWAS and aDNA. Input: public data listed in that repository. Output: analysis notes. Version: vitis-open-directions v3_2, 2026-11-14 (Local catalog in vitis-open-directions, not a GitHub release of this repo). [link](https://github.com/Xuzhen-Li/vitis-open-directions)  
  Note: The public repository may not be online yet. Content used here is the v3_2 snapshot dated 2026-11-14. grapeancestry remains the 167K product and is not replaced by this catalogue.
- **nf-core/sarek** (workflow) — Community Nextflow workflow for germline short-read variant calling. Not grape-specific. Input: FASTQ, reference. Output: VCF, QC. Version: [待确认] (Not version-checked in this build; listed as a well-known modern WGS workflow). [link](https://nf-co.re/sarek)  
  Note: Version [待确认]. The AM03 sketch (bwa-mem2 + DeepVariant or GATK) is the project default if you do not use sarek.

<a id="section-15"></a>
## 15. Vitis popgen studies and public resources

<!-- PROSE:SECTION:P15 -->
Public panels and sister repositories. This repository does not host unpublished genotypes.
<!-- /PROSE:SECTION:P15 -->

**Clusters:**
- *Identity and living collections (complementary)*: grapeancestry.
- *Public Vitis resequencing panels (complementary)*: Dong et al. 2023 resequencing panel (DS11), Magris et al. 2021 and related public panels (DS10, DS12).
- *Public Vitis resequencing or genotyping panels (complementary)*: Myles et al. 2011 SNP-array panel, Zhou et al. 2017 resequencing, Liang et al. 2019 472 accessions, Laucou et al. 2018 10K SNP panel, Freitas et al. 2021 wild hybridisation, Xiao et al. 2023 introgression, Morales-Cruz et al. 2021 North American wild Vitis, Emanuelli et al. 2013 germplasm SSR/SNP, Nicolas et al. 2016 diversity panel, Liu et al. 2024 pangenome panel, Guo et al. 2025 Vitis super-pangenome, Kim et al. 2020 high-depth resequencing.

- **grapeancestry** (resource) — 167K FASTQ-to-ancestry product. This catalogue does not replace it. Input: n/a. Output: n/a. Version: n/a (separate product) (https://github.com/Xuzhen-Li/grapeancestry). [link](https://github.com/Xuzhen-Li/grapeancestry)  
  Note: Out of scope for unpublished genotypes.
- **Dong et al. 2023 resequencing panel (DS11)** (resource) — Large published resequencing panel used for structure, domestication and load analyses. Input: public reads or VCF as published. Output: n/a. Version: n/a (vitis-open-directions DS11, recorded 2026-11-14). [doi:10.1126/science.add8655](https://doi.org/10.1126/science.add8655) · [link](https://doi.org/10.1126/science.add8655)  
  Note: DOI 10.1126/science.add8655 verified by Crossref. Accessions include NGDC PRJCA009314 (as recorded in the literature review). Cite the original paper when used; the DS11 module in vitis-open-directions has further pointers.
- **Magris et al. 2021 and related public panels (DS10, DS12)** (resource) — Additional published resequencing panels for population structure and diversity. Input: public data. Output: n/a. Version: n/a (vitis-open-directions DS10 and DS12, recorded 2026-11-14). [doi:10.1038/s41467-021-27487-y](https://doi.org/10.1038/s41467-021-27487-y) · [link](https://doi.org/10.1038/s41467-021-27487-y)  
  Note: Magris et al. 2021 DOI 10.1038/s41467-021-27487-y verified by Crossref. Related project IDs include PRJNA373967 (literature review). Pointers only; see the DS modules for accessions and sizes.
- **Myles et al. 2011 SNP-array panel** (resource) — SNP-array survey of more than 1,000 cultivated and wild accessions. Input: public data. Output: n/a. Version: n/a (Crossref-verified in the literature review, 2026-11-14 CST). [doi:10.1073/pnas.1009363108](https://doi.org/10.1073/pnas.1009363108) · [link](https://doi.org/10.1073/pnas.1009363108)  
  Note: Accession details were taken from the abstract in the literature review.
- **Zhou et al. 2017 resequencing** (resource) — Wild and cultivated resequencing for grape domestication genomics. Input: public data. Output: n/a. Version: n/a (Crossref-verified in the literature review, 2026-11-14 CST). [doi:10.1073/pnas.1709257114](https://doi.org/10.1073/pnas.1709257114) · [link](https://doi.org/10.1073/pnas.1709257114)  
  Note: DOI and title verified against Crossref (Evolutionary genomics of grape (Vitis vinifera ssp. vinifera) domestication). Resequencing reads: PRJNA388292 (SRP108271; 23 WGS runs). Zhou et al. also reused public RNA-seq SRP049306 (University of Verona, berry transcriptome) and SRP041212 (Instituto Superior de Agronomia, flower transcriptome) for expression analysis; those two projects are not Zhou et al. 2017 resequencing reads. PRJNA388292 was submitted by Zhou et al. 2017; Liang et al. 2019 later reused the 23 accessions.
- **Liang et al. 2019 472 accessions** (resource) — 472 accessions covering 48 of 60 extant Vitis species. Input: public data. Output: n/a. Version: n/a (Crossref-verified in the literature review, 2026-11-14 CST). [doi:10.1038/s41467-019-09135-8](https://doi.org/10.1038/s41467-019-09135-8) · [link](https://doi.org/10.1038/s41467-019-09135-8)  
  Note: Own data PRJNA393611; also reanalysed 23 accessions from PRJNA388292 (submitted by Zhou et al. 2017).
- **Laucou et al. 2018 10K SNP panel** (resource) — 783 cultivars typed at 10,207 SNPs from an 18K array; a parentage and structure reference, and the source of the pip-capture SNP set. Input: public data. Output: n/a. Version: n/a (Crossref-verified in the literature review, 2026-11-14 CST). [doi:10.1371/journal.pone.0192540](https://doi.org/10.1371/journal.pone.0192540) · [link](https://doi.org/10.1371/journal.pone.0192540)  
  Note: Crossref-verified in the literature review.
- **Freitas et al. 2021 wild hybridisation** (resource) — Resequencing of Western European cultivars and local wild vines. Input: public data. Output: n/a. Version: n/a (Crossref-verified in the literature review, 2026-11-14 CST). [doi:10.1126/sciadv.abi8584](https://doi.org/10.1126/sciadv.abi8584) · [link](https://doi.org/10.1126/sciadv.abi8584)  
  Note: Accession identifier was not re-checked [待确认].
- **Xiao et al. 2023 introgression** (resource) — Introgression study based on 345 samples (abstract). Input: public data. Output: n/a. Version: n/a (Crossref-verified in the literature review, 2026-11-14 CST). [doi:10.1073/pnas.2222041120](https://doi.org/10.1073/pnas.2222041120) · [link](https://doi.org/10.1073/pnas.2222041120)  
  Note: Project IDs recorded in the literature review: PRJNA910315 and NGDC PRJCA016655.
- **Morales-Cruz et al. 2021 North American wild Vitis** (resource) — 130 resequenced individuals of six North American wild species. Input: public data. Output: n/a. Version: n/a (Crossref-verified in the literature review, 2026-11-14 CST). [doi:10.1186/s13059-021-02467-z](https://doi.org/10.1186/s13059-021-02467-z) · [link](https://doi.org/10.1186/s13059-021-02467-z)  
  Note: Project IDs recorded in the literature review include PRJNA731597.
- **Emanuelli et al. 2013 germplasm SSR/SNP** (resource) — 2,273 accessions typed with SSRs and SNPs (abstract). Input: public data. Output: n/a. Version: n/a (Crossref-verified in the literature review, 2026-11-14 CST). [doi:10.1186/1471-2229-13-39](https://doi.org/10.1186/1471-2229-13-39) · [link](https://doi.org/10.1186/1471-2229-13-39)
- **Nicolas et al. 2016 diversity panel** (resource) — 279-cultivar diversity panel for association studies (abstract). Input: public data. Output: n/a. Version: n/a (Crossref-verified in the literature review, 2026-11-14 CST). [doi:10.1186/s12870-016-0754-z](https://doi.org/10.1186/s12870-016-0754-z) · [link](https://doi.org/10.1186/s12870-016-0754-z)
- **Liu et al. 2024 pangenome panel** (resource) — 29 assemblies plus 466 resequenced cultivars (abstract). Input: public data. Output: n/a. Version: n/a (Crossref-verified in the literature review, 2026-11-14 CST). [doi:10.1038/s41588-024-01967-5](https://doi.org/10.1038/s41588-024-01967-5) · [link](https://doi.org/10.1038/s41588-024-01967-5)  
  Note: The full accession list was not re-checked [待确认].
- **Guo et al. 2025 Vitis super-pangenome** (resource) — 72 haplotype-resolved assemblies (25 wild, 47 cultivated). Input: public data. Output: n/a. Version: n/a (Crossref-verified in the literature review, 2026-11-14 CST). [doi:10.1038/s41588-025-02111-7](https://doi.org/10.1038/s41588-025-02111-7) · [link](https://doi.org/10.1038/s41588-025-02111-7)  
  Note: Project ID recorded in the literature review: PRJNA1021789.
- **Kim et al. 2020 high-depth resequencing** (resource) — High-depth (above 37x) resequencing of seeded, seedless and wild Vitis. Input: public data. Output: n/a. Version: n/a (Crossref-verified in the literature review, 2026-11-14 CST). [doi:10.1534/g3.120.401521](https://doi.org/10.1534/g3.120.401521) · [link](https://doi.org/10.1534/g3.120.401521)  
  Note: Project ID recorded in the literature review: PRJNA485199.

<a id="section-16"></a>
## 16. Ideas still lightly tested on Vitis

<!-- PROSE:SECTION:P16 -->
Intended recipes, not results. No claim is made that these workflows have been run on grape in this repository.
<!-- /PROSE:SECTION:P16 -->

**Clusters:**
- *Ideas still lightly tested on Vitis (complementary)*: ARG dating of grape domestication, Clone-aware ADMIXTURE and PCA recipes, Graph-aware introgression and inversion scans, Sex-determining region genotype as sample annotation (idea).

- **ARG dating of grape domestication** (idea) — Use tsinfer/tsdate or Relate on a clone-pruned, polarised panel; compare with aDNA tip dates. Input: phased public VCF, maps. Output: dated tree sequence. Version: n/a (vitis-open-directions project 10). [link](https://github.com/Xuzhen-Li/vitis-open-directions)  
  Note: See vitis-open-directions project 10. No results are claimed here. Use sexual-origin times as sample dates for clonal cultivars, and state the generation-time assumption when converting to years.
- **Clone-aware ADMIXTURE and PCA recipes** (idea) — Documented intent: detect clones and duplicates first (one sample per clone group), then treat first-degree relatives in an analysis-specific way rather than dropping them as the same genotype. Input: public VCF. Output: notes, plots. Version: n/a (stated in the current vitis-popgen README; not yet a script in the live repo). [link](https://github.com/Xuzhen-Li/vitis-popgen)  
  Note: See docs/WORKFLOW.md for the two-step clone versus first-degree rule.
- **Graph-aware introgression and inversion scans** (idea) — Move introgression and inversion work from linear VCFs onto the pangenome graph. Input: graph, cohort genotypes. Output: tracts, local PCA. Version: n/a (vitis-open-directions projects 15 and 17; vitis-pangenome). [link](https://github.com/Xuzhen-Li/vitis-pangenome)  
  Note: Details belong in vitis-pangenome; this repo only points to them.
- **Sex-determining region genotype as sample annotation (idea)** (idea) — Annotate samples for the grape sex-determining region genotypes (M, F, H). This can infer sex in wild samples. Grape has no heteromorphic sex chromosomes; the locus is a small region on chromosome 2, and most cultivars are hermaphroditic. See vitis-open-directions item 22. Input: aligned reads or VCF around the SDR. Output: sample-level M/F/H annotation. Version: n/a (checked 2026-11-14 CST). [link](https://github.com/Xuzhen-Li/vitis-open-directions)  
  Note: Pointer only; this repository does not invent a new caller.

<a id="section-17"></a>
## 17. Parentage, pedigree and name identity

<!-- PROSE:SECTION:P17 -->
Parentage, pedigree reconstruction, and name identity are central to grape population genetics because a few parents have given rise to many cultivars. Merge clones first. Here, relatives represent the signal rather than a nuisance. Homonyms and synonyms must be verified against both genotype identity and VIVC.
<!-- /PROSE:SECTION:P17 -->

**Clusters:**
- *Parentage and pedigree (complementary)*: sequoia, COLONY, Mendelian-error check on published trios (idea).
- *Names and synonyms (complementary)*: VIVC name and genotype cross-check (idea).

- **sequoia** (tool) — SNP-based inference of parents, half-siblings and multi-generation pedigrees. Merge clones first. Input: SNP genotype matrix, optional birth years. Output: pedigree, parent assignments. Version: 3.2.0 (CRAN sequoia 3.2.0 (package Date 2025-12-30), checked 2026-11-14 CST). [doi:10.1111/1755-0998.12665](https://doi.org/10.1111/1755-0998.12665) · [link](https://cran.r-project.org/package=sequoia)  
  Note: Many grape cultivars have no reliable 'birth year'; how to set year priors remains [待确认]. Applicability to grape more generally remains [待确认].
- **COLONY** (tool) — Full-likelihood parentage and sibship inference; supports hermaphrodites and genotyping error. Input: multilocus genotypes. Output: parentage and sibship groups. Version: [待确认] (software site via the 2010 methods paper; current version not confirmed 2026-11-14 CST). [doi:10.1111/j.1755-0998.2009.02787.x](https://doi.org/10.1111/j.1755-0998.2009.02787.x) · [link](https://doi.org/10.1111/j.1755-0998.2009.02787.x)  
  Note: Scalability to thousands of SNPs, and applicability to grape, remain [待确认]. Version [待确认].
- **Mendelian-error check on published trios (idea)** (idea) — Run a Mendelian-error check (for example PLINK --mendel) on literature parent-offspring trios. A high error rate suggests a wrong pedigree or a homonym. Input: BED + pedigree FAM. Output: Mendelian error counts. Version: n/a (uses PLINK already in this catalogue). [link](https://www.cog-genomics.org/plink/1.9/)  
  Note: Uses the already-listed PLINK 1.9; not a second tool version.
- **VIVC name and genotype cross-check (idea)** (idea) — Cross-check cultivar names, synonyms and genotype identity against VIVC. Homonyms (same name, different genotypes) and synonyms (different names, same genotype) must both be considered; do not merge samples by name alone. Input: sample names and clone groups. Output: name-to-genotype table. Version: n/a (uses the VIVC resource already listed in section 8). [link](https://www.vivc.de/)  
  Note: The VIVC database itself is already catalogued in section 8; this row is the analysis idea.
