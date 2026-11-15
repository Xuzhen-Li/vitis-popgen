#!/usr/bin/env python3
"""Write a multi-haplotype multi-site text table as a demography-prep demonstration.

Inputs:  --vcf --pops
Outputs: --msmc-like TSV with chrom, pos, called_haplotypes, genotypes_as_0_1_string
Tested:  toy VCF format only.
Production: use published MSMC2 / SMC++ / stairway / ARG input converters from
the catalogue, with generation time and sample times treated as in
docs/WORKFLOW.md decision 7. This file is not a valid MSMC input and must not be
fed to those tools.
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
    ap.add_argument("--out-tsv", required=True)
    args = ap.parse_args()
    v = read_vcf_gt(Path(args.vcf))
    alle = v["alleles"]
    rows = []
    for i in range(len(v["pos"])):
        bits = []
        called = 0
        for j in range(alle.shape[1]):
            a, b = alle[i, j]
            if np.isnan(a) or np.isnan(b):
                bits.append(".")
            else:
                bits.append(str(int(a)) + str(int(b)))
                called += 2
        rows.append([v["chrom"][i], int(v["pos"][i]), called, "".join(bits)])
    write_tsv(Path(args.out_tsv),
              ["chrom", "pos", "called_haplotypes", "diploid_calls"],
              rows)
    print("rows", len(rows))


if __name__ == "__main__":
    main()
