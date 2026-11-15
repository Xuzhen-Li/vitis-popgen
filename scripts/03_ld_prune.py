#!/usr/bin/env python3
"""Greedy LD pruning within a window of neighbouring SNPs on the same chromosome.

Inputs:  --vcf --r2-threshold (default 0.2) --window (default 50 SNPs)
Outputs: --out-vcf of kept sites, --dropped-tsv
Tested:  toy VCF.
Production: plink2 --indep-pairwise, then LD-prune before PCA and ADMIXTURE
(see docs/WORKFLOW.md decision 4), after clone deduplication (decision 3).
The numeric defaults here (r-squared 0.2, window 50 SNPs) are for the toy set
only and are not pre-registered grape thresholds.
Sites are selected by chrom:pos:ref:alt, not by the VCF ID column (often ".").
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_vcf import dosage, read_vcf_gt, write_tsv, write_vcf_subset


def corr_r2(a, b):
    mask = (~np.isnan(a)) & (~np.isnan(b))
    if mask.sum() < 5:
        return np.nan
    x, y = a[mask], b[mask]
    if x.std() == 0 or y.std() == 0:
        return np.nan
    r = np.corrcoef(x, y)[0, 1]
    return float(r * r)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--vcf", required=True)
    ap.add_argument("--out-vcf", required=True)
    ap.add_argument("--dropped-tsv", required=True)
    ap.add_argument("--r2-threshold", type=float, default=0.2)
    ap.add_argument("--window", type=int, default=50)
    args = ap.parse_args()
    src = Path(args.vcf)
    v = read_vcf_gt(src)
    dos = dosage(v["alleles"])
    m = dos.shape[0]
    keep = np.ones(m, dtype=bool)
    dropped = []
    for i in range(m):
        if not keep[i]:
            continue
        for j in range(i + 1, min(m, i + 1 + args.window)):
            if not keep[j]:
                continue
            if v["chrom"][j] != v["chrom"][i]:
                break
            r2 = corr_r2(dos[i], dos[j])
            if r2 == r2 and r2 > args.r2_threshold:
                keep[j] = False
                dropped.append([v["key"][j], v["key"][i], f"{r2:.4f}"])
    write_vcf_subset(src, Path(args.out_vcf), keep_keys=list(v["key"][keep]))
    write_tsv(Path(args.dropped_tsv), ["dropped_key", "tag_key", "r2"], dropped)
    print("kept", int(keep.sum()), "dropped", len(dropped))


if __name__ == "__main__":
    main()
