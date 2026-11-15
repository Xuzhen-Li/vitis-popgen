#!/usr/bin/env bash
# Tested Python popgen toy chain. Does not call ADMIXTURE, qbar, plink2 or pixy.
# Order follows docs/WORKFLOW.md: QC, then clone dedup, then filter, then LD prune,
# then structure and downstream demonstrations.
set -Ceu
if [ "${1:-}" = "--help" ] || [ $# -lt 1 ]; then
  printf '%s\n' "usage: run_toy_pipeline.sh OUTDIR"
  exit 0
fi
OUT=$1
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$OUT"
python3 "$HERE/00_simulate_toy_vcf.py" --vcf "$OUT/toy.vcf" --pops "$OUT/toy.pops" --seed 7
python3 "$HERE/01_vcf_qc.py" --vcf "$OUT/toy.vcf" --site-tsv "$OUT/qc_sites.tsv" --sample-tsv "$OUT/qc_samples.tsv"
python3 "$HERE/01b_clone_dedup.py" --vcf "$OUT/toy.vcf" --out-vcf "$OUT/toy.dedup.vcf" \
  --related-tsv "$OUT/clone_pairs.tsv" --keep-samples "$OUT/clone_keep.tsv"
python3 "$HERE/02_filter_variants.py" --vcf "$OUT/toy.dedup.vcf" --out-vcf "$OUT/toy.filtered.vcf"
python3 "$HERE/03_ld_prune.py" --vcf "$OUT/toy.filtered.vcf" --out-vcf "$OUT/toy.pruned.vcf" \
  --dropped-tsv "$OUT/ld_dropped.tsv"
python3 "$HERE/04_pca.py" --vcf "$OUT/toy.pruned.vcf" --pops "$OUT/toy.pops" \
  --scores-tsv "$OUT/pca_scores.tsv" --loadings-tsv "$OUT/pca_loadings.tsv" --variance-tsv "$OUT/pca_variance.tsv"
python3 "$HERE/06_roh.py" --vcf "$OUT/toy.filtered.vcf" --roh-tsv "$OUT/roh.tsv" --min-snps 50
python3 "$HERE/07_diversity_windows.py" --vcf "$OUT/toy.dedup.vcf" --pops "$OUT/toy.pops" \
  --diversity-tsv "$OUT/diversity.tsv" --fst-tsv "$OUT/fst.tsv"
python3 "$HERE/08_selection_scan.py" --fst-tsv "$OUT/fst.tsv" --outliers-tsv "$OUT/fst_outliers.tsv"
python3 "$HERE/09_fstats.py" --vcf "$OUT/toy.filtered.vcf" --pops "$OUT/toy.pops" \
  --f2-tsv "$OUT/f2.tsv" --f3-tsv "$OUT/f3.tsv" --f4-tsv "$OUT/f4.tsv"
python3 "$HERE/10_demography_prep.py" --vcf "$OUT/toy.filtered.vcf" --out-tsv "$OUT/demography_demo.tsv"
python3 "$HERE/11_plot_pca.py" --scores-tsv "$OUT/pca_scores.tsv" --svg "$OUT/pca.svg"
printf '%s\n' "toy pipeline finished in $OUT"
