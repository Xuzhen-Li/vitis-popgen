#!/usr/bin/env python3
"""Filter sites by missing rate and allele-frequency bounds.

Inputs:  --vcf --max-missing (default 0.1) --min-af (default 0.05) --max-af (default 0.95)
Outputs: --out-vcf
Tested:  toy VCF.
Production: bcftools view / filter, or plink2 --geno --maf.
The defaults here are for the toy dataset only, not a pre-registered grape threshold.
Sites are selected by chrom:pos:ref:alt, not by the VCF ID column (often ".").
Run this after clone deduplication (01b_clone_dedup.py / KING).
This pipeline does not apply an HWE filter; that is intentional for clonal and
inbred crops.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_vcf import dosage, read_vcf_gt, write_vcf_subset


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--vcf", required=True)
    ap.add_argument("--out-vcf", required=True)
    ap.add_argument("--max-missing", type=float, default=0.1)
    ap.add_argument("--min-af", type=float, default=0.05)
    ap.add_argument("--max-af", type=float, default=0.95)
    args = ap.parse_args()
    src = Path(args.vcf)
    v = read_vcf_gt(src)
    dos = dosage(v["alleles"])
    miss = np.isnan(dos).mean(axis=1)
    an = 2 * np.sum(~np.isnan(dos), axis=1)
    ac = np.nansum(dos, axis=1)
    af = np.divide(ac, an, out=np.zeros(len(ac)), where=an > 0)
    keep = (miss <= args.max_missing) & (af >= args.min_af) & (af <= args.max_af)
    write_vcf_subset(src, Path(args.out_vcf), keep_keys=list(v["key"][keep]))
    print("kept", int(keep.sum()), "of", len(keep),
          "skipped_multiallelic", v["n_multiallelic_skipped"])


if __name__ == "__main__":
    main()
