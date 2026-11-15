#!/usr/bin/env bash
# Run ADMIXTURE on a plink BED/BIM/FAM prefix, then point to qbar for Q-file alignment.
#
# Inputs:  PREFIX (plink files). Output directory as second argument.
# Production: after KING clone deduplication (docs/WORKFLOW.md decision 3),
# LD-prune and run on the largest unrelated subset (decision 4). After
# ADMIXTURE, align Q files with https://github.com/Xuzhen-Li/qbar and check
# residuals with evalAdmix (evalAdmix is a complement to ADMIXTURE, not a
# substitute). Repeat each K with several random seeds (-s) and report the
# CV error of each run. Choose K from the CV curve plateau together with
# evalAdmix residuals, not from the CV minimum alone. Align replicate Q
# files with qbar.
#
# The default K range 2..5 is a toy default only and is not a pre-registered
# grape K range. This wrapper is untested on the box (ADMIXTURE and qbar
# are not installed). --dry-run prints the documented commands and exits 2.

set -Ceu
if [ "${1:-}" = "--dry-run" ]; then
  printf '%s\n' "usage: 05_run_admixture.sh [--dry-run] PREFIX OUTDIR [KMIN KMAX THREADS]"
  printf '%s\n' "documented command (toy K range 2..5 unless you set KMIN/KMAX):"
  printf '%s\n' "  admixture --cv PREFIX.bed K -s SEED -j THREADS   # repeat seeds per K"
  printf '%s\n' "Then align Q files with qbar from https://github.com/Xuzhen-Li/qbar"
  printf '%s\n' "Run after KING clone deduplication and LD pruning (docs/WORKFLOW.md)."
  exit 2
fi
if [ "${1:-}" = "--help" ] || [ $# -lt 2 ]; then
  printf '%s\n' "usage: 05_run_admixture.sh [--dry-run] PREFIX OUTDIR [KMIN KMAX THREADS]"
  exit 0
fi
PREFIX=$1
OUTDIR=$2
KMIN=${3:-2}
KMAX=${4:-5}
THREADS=${5:-4}
printf 'Would run: mkdir -p %s and admixture --cv %s.bed K for K=%s..%s (-j%s), several seeds per K\n' "$OUTDIR" "$PREFIX" "$KMIN" "$KMAX" "$THREADS"
printf 'Then align Q files with qbar from https://github.com/Xuzhen-Li/qbar\n'
printf 'Example after install: qbar --qfiles %s/*.Q --out %s/qbar_aligned\n' "$OUTDIR" "$OUTDIR"
if ! command -v admixture >/dev/null; then
  printf '%s\n' "admixture is not on PATH; refusing to continue. Re-run with --dry-run or install the tool."
  exit 3
fi
printf '%s\n' "admixture found, but this script only documents the command in this version."
exit 3
