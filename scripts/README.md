# scripts

Toy implementations of the main analysis steps in `docs/WORKFLOW.md`, starting from a working VCF. They do not replace bcftools, plink, ADMIXTURE, pixy or ADMIXTOOLS2, which remain the production tools listed in the catalogue. Citations for those tools are in the README catalogue rows.

The chain follows the published order: QC, clone or duplicate collapse, missingness and allele-frequency filters, LD pruning, and then population structure and the downstream demonstrations. Production inputs must be clone-deduplicated with KING (docs/WORKFLOW.md decision 3) before MAF, LD, PCA or ADMIXTURE. Because the toy VCF contains no planted clones, `01b_clone_dedup.py` keeps every sample. When a toy group does occur, `01b` retains the first sample in VCF sample-column order. The 0.99 dosage-correlation cutoff is a toy criterion and is not convertible to KING kinship (about 0.5 for clones; 0.354 is the already-cited KING duplicate/MZ boundary). `01c_run_king.sh` documents that `plink2 --king-cutoff` writes ID lists whose names follow the `--out` prefix and must then be passed to `--keep` or `--remove`. This pipeline does not apply an HWE filter; that is intentional for clonal and inbred crops.

Generate a small simulated VCF and run the tested Python chain:

```bash
bash scripts/run_toy_pipeline.sh OUTDIR
```

The simulator writes 40 samples across three populations and 1,200 SNPs (seed 7). It is not real *Vitis* data. Toy filters (maximum missingness 0.1, minimum allele frequency 0.05, LD r-squared 0.2, Fst z-score 2, ROH min-snps 50, windows 50 kb / 25 kb, ADMIXTURE K 2..5, clone-dedup dosage correlation 0.99) are for this demonstration only and are not pre-registered grape thresholds.

| File | Purpose | Tested? |
|------|---------|---------|
| `lib_vcf.py` | Minimal VCF genotype reader; sites keyed by chrom:pos:ref:alt | Yes, used by the chain |
| `00_simulate_toy_vcf.py` | Write the toy VCF and population table | Yes |
| `01_vcf_qc.py` | Per-sample and per-site missingness and allele frequency | Yes |
| `01b_clone_dedup.py` | Toy clone/duplicate collapse from dosage correlation; not KING | Yes |
| `01c_run_king.sh` | Document plink2 KING (0.354 as already cited in the WORKFLOW) | No, `--dry-run` exits 2 |
| `02_filter_variants.py` | Missingness and allele-frequency filter | Yes |
| `03_ld_prune.py` | Greedy windowed r-squared prune | Yes |
| `04_pca.py` | sklearn PCA on mean-imputed dosages (does not drop relatives) | Yes |
| `05_run_admixture.sh` | Document ADMIXTURE; then use [qbar](https://github.com/Xuzhen-Li/qbar) and evalAdmix | No. `--dry-run` exits 2, with or without PREFIX OUTDIR. |
| `05b_qbar_align.sh` | Document Q-file alignment with qbar | No, `--dry-run` exits 2 |
| `06_roh.py` | Consecutive homozygous runs; not plink `--homozyg` | Yes (on the filtered VCF) |
| `07_diversity_windows.py` | Windowed diversity; per-base pi only with `--accessible-bed`; numerator is variants inside the bed; coordinates are 0-based half-open; `--min-variant-sites` (default 5) is an explicit toy gate that can bias pi upward (statistics review [待确认]) | Yes. The toy driver uses the post-dedup, pre-MAF VCF. Per-base pi must not use a MAF-filtered VCF. Production still uses pixy on an all-sites VCF. |
| `08_selection_scan.py` | Fst z-score outliers as candidates, not evidence of selection | Yes |
| `09_fstats.py` | Allele-frequency f2, f3 and f4; biased, no jackknife; not ADMIXTOOLS2 | Yes (f4 is empty with only three populations) |
| `10_demography_prep.py` | Writes a demo table; not valid MSMC input | Yes |
| `11_plot_pca.py` | PCA SVG without matplotlib | Yes |
| `run_toy_pipeline.sh` | Driver for the tested Python scripts only | Yes |

ADMIXTURE should be run on an LD-pruned, largely unrelated subset after clone deduplication (see `docs/WORKFLOW.md`). evalAdmix complements ADMIXTURE rather than replacing it.
