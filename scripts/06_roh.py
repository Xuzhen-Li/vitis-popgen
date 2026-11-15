#!/usr/bin/env python3
"""Consecutive homozygous runs as a toy ROH demonstration.

Inputs:  --vcf --out-tsv --min-snps (default 50, toy only)
Outputs: --out-tsv
Tested:  toy VCF with planted ROH on two samples.
Production: plink --homozyg or bcftools roh can be run on unphased genotypes.
ROH does not require phasing. hap-IBD finds IBD between different individuals
and is not an ROH tool. A published map is useful for length in genetic units
but is not required to call ROH.
In a clonal crop, a cultivar's ROH reflects inbreeding at its sexual origin
(relatedness of the parents). Clonal propagation itself does not create ROH.
The default --min-snps 50 is a toy value only, not a pre-registered grape
parameter. Production settings (minimum length in kb, SNP density, allowed
heterozygotes and missing sites, or the bcftools roh model) remain [待确认]
and should be pre-registered, including whether sites are first filtered by
MAF or LD. This toy counter allows no heterozygotes and does not use physical
length, so a single genotyping error can split a run.
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
    ap.add_argument("--roh-tsv", required=True)
    ap.add_argument("--min-snps", type=int, default=50)
    args = ap.parse_args()
    v = read_vcf_gt(Path(args.vcf))
    dos = dosage(v["alleles"])
    rows = []
    for j, sid in enumerate(v["samples"]):
        for chrom in np.unique(v["chrom"]):
            idx = np.where(v["chrom"] == chrom)[0]
            hom = (dos[idx, j] == 0) | (dos[idx, j] == 2)
            miss = np.isnan(dos[idx, j])
            run_start = None
            run_len = 0
            for k, (is_hom, is_miss) in enumerate(zip(hom, miss)):
                if is_miss:
                    continue
                if is_hom:
                    if run_start is None:
                        run_start = k
                        run_len = 1
                    else:
                        run_len += 1
                else:
                    if run_start is not None and run_len >= args.min_snps:
                        a, b = idx[run_start], idx[run_start + run_len - 1]
                        rows.append([sid, chrom, int(v["pos"][a]), int(v["pos"][b]),
                                     run_len, v["id"][a], v["id"][b]])
                    run_start, run_len = None, 0
            if run_start is not None and run_len >= args.min_snps:
                a, b = idx[run_start], idx[run_start + run_len - 1]
                rows.append([sid, chrom, int(v["pos"][a]), int(v["pos"][b]),
                             run_len, v["id"][a], v["id"][b]])
    write_tsv(Path(args.roh_tsv),
              ["sample_id", "chrom", "start", "end", "n_snps", "start_id", "end_id"],
              rows)
    print("roh_rows", len(rows))


if __name__ == "__main__":
    main()
