#!/usr/bin/env python3
"""Per-site and per-sample QC tables for a VCF.

Inputs:  --vcf
Outputs: --site-tsv, --sample-tsv
Tested:  toy VCF from 00_simulate_toy_vcf.py (numpy).
Production: bcftools stats / vcftools --missing / plink2 --missing, then filter.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_vcf import dosage, read_vcf_gt, write_tsv


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--vcf", required=True)
    ap.add_argument("--site-tsv", required=True)
    ap.add_argument("--sample-tsv", required=True)
    args = ap.parse_args()
    v = read_vcf_gt(Path(args.vcf))
    dos = dosage(v["alleles"])
    n = dos.shape[1]
    # site missing and AF
    site_miss = np.isnan(dos).mean(axis=1)
    ac = np.nansum(dos, axis=1)
    an = 2 * np.sum(~np.isnan(dos), axis=1)
    af = np.divide(ac, an, out=np.full(len(ac), np.nan), where=an > 0)
    het = np.nanmean((dos == 1), axis=1)
    write_tsv(Path(args.site_tsv),
              ["chrom", "pos", "id", "n_called", "missing_rate", "ac", "an", "af", "het"],
              [[v["chrom"][i], v["pos"][i], v["id"][i], int(an[i] // 2),
                f"{site_miss[i]:.6f}", int(ac[i]), int(an[i]), f"{af[i]:.6f}", f"{het[i]:.6f}"]
               for i in range(len(af))])
    # samples
    samp_miss = np.isnan(dos).mean(axis=0)
    samp_het = np.nanmean(dos == 1, axis=0)
    write_tsv(Path(args.sample_tsv),
              ["sample_id", "n_sites", "missing_rate", "het"],
              [[v["samples"][j], dos.shape[0], f"{samp_miss[j]:.6f}", f"{samp_het[j]:.6f}"]
               for j in range(n)])
    print("sites", len(af), "samples", n)


if __name__ == "__main__":
    main()
