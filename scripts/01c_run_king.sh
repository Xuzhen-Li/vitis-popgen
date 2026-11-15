#!/usr/bin/env bash
# Document plink2 KING for clone and duplicate detection.
# Production (docs/WORKFLOW.md decisions 3 and 4): after variant QC, run KING;
# keep one sample per clone or duplicate group when kinship is above 0.354
# (Manichaikul et al. 2010, doi:10.1093/bioinformatics/btq559).
# First-degree relatives (0.177 to 0.354) are recorded, not treated as clones.
# Untested on this box (plink2 is not installed).

set -Ceu
if [ "${1:-}" = "--help" ] || [ "${1:-}" = "--dry-run" ]; then
  printf '%s\n' "usage: 01c_run_king.sh PREFIX OUTDIR"
  printf '%s\n' "documented production commands (install plink2 first):"
  printf '%s\n' "  plink2 --bfile PREFIX --make-king square --out OUTDIR/king"
  printf '%s\n' "  plink2 --bfile PREFIX --king-cutoff 0.354 --out OUTDIR/king_dedup"
  printf '%s\n' "0.354 is the KING manual duplicate or MZ class, already cited in docs/WORKFLOW.md."
  printf '%s\n' "This wrapper does not invent a grape-specific cutoff."
  printf '%s\n' "--king-cutoff writes ID lists whose names follow the --out prefix:"
  printf '%s\n' "  OUTDIR/king_dedup.king.cutoff.in.id and OUTDIR/king_dedup.king.cutoff.out.id"
  printf '%s\n' "  when --out is OUTDIR/king_dedup. Those lists must then be passed to"
  printf '%s\n' "  plink2 --keep or --remove; --king-cutoff alone does not write a filtered"
  printf '%s\n' "  genotype file."
  printf '%s\n' "The plink2 retention rule (keep as many samples as possible) differs from"
  printf '%s\n' "  the 01b toy script, which keeps the first sample in VCF order in each group."
  if [ "${1:-}" = "--dry-run" ]; then exit 2; fi
  exit 0
fi
printf '%s\n' "plink2 is not invoked automatically in this wrapper; see --help."
exit 3
