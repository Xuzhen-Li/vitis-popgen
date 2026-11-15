#!/usr/bin/env python3
"""Simulate a small diploid VCF with three populations, LD blocks, and a few ROH samples.

Inputs:  --seed (default 7). No external genotypes.
Outputs: --vcf and --pops TSV (sample_id, population).
Tested:  Python 3.13 + numpy on the box (see evidence log for sha and command).
This is toy data for script tests. It is not a grape dataset and must not be
published as real Vitis genotypes.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--vcf", required=True)
    ap.add_argument("--pops", required=True)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--n-snps", type=int, default=1200)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)

    pops = (["POP1"] * 16) + (["POP2"] * 16) + (["POP3"] * 8)
    samples = [f"S{i+1:02d}" for i in range(len(pops))]
    n = len(samples)
    m = args.n_snps
    # Three chromosomes, even SNP layout
    chroms = np.array(["chr1"] * 400 + ["chr2"] * 400 + ["chr3"] * 400)
    pos = np.concatenate([np.linspace(1000, 399000, 400, dtype=int) for _ in range(3)])

    # Population allele frequencies
    base = rng.beta(0.8, 0.8, size=m)
    p = np.vstack([
        np.clip(base + 0.15, 0.02, 0.98),
        np.clip(base - 0.05, 0.02, 0.98),
        np.clip(base - 0.20, 0.02, 0.98),
    ])
    alleles = np.zeros((m, n, 2), dtype=int)
    for j, pop in enumerate(pops):
        k = {"POP1": 0, "POP2": 1, "POP3": 2}[pop]
        alleles[:, j, 0] = rng.binomial(1, p[k])
        alleles[:, j, 1] = rng.binomial(1, p[k])

    # LD blocks: copy a tag SNP onto the next 8 sites in 20 regions
    for start in range(0, m, 60):
        tag = alleles[start]
        for w in range(1, 8):
            if start + w < m:
                flip = rng.random(n) < 0.1
                alleles[start + w, :, 0] = np.where(flip, 1 - tag[:, 0], tag[:, 0])
                alleles[start + w, :, 1] = np.where(flip, 1 - tag[:, 1], tag[:, 1])

    # ROH: make S01 and S17 homozygous across a 80-SNP window on chr1
    for sid, a, b in (("S01", 40, 120), ("S17", 200, 280)):
        j = samples.index(sid)
        alleles[a:b, j, 1] = alleles[a:b, j, 0]

    vcf = Path(args.vcf)
    pops_path = Path(args.pops)
    with vcf.open("x", encoding="utf-8") as f:
        f.write("##fileformat=VCFv4.2\n")
        f.write("##source=00_simulate_toy_vcf.py seed=%d\n" % args.seed)
        f.write('##INFO=<ID=PR,Number=0,Type=Flag,Description="toy">\n')
        f.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
        f.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t" + "\t".join(samples) + "\n")
        bases = np.array(list("ACGT"))
        for i in range(m):
            ref = "A"
            alt = "G"
            gts = []
            for j in range(n):
                a, b = int(alleles[i, j, 0]), int(alleles[i, j, 1])
                gts.append(f"{a}/{b}")
            vid = f"rs{i+1}"
            f.write(f"{chroms[i]}\t{pos[i]}\t{vid}\t{ref}\t{alt}\t.\tPASS\t.\tGT\t" + "\t".join(gts) + "\n")
    with pops_path.open("x", encoding="utf-8") as f:
        f.write("sample_id\tpopulation\n")
        for s, p in zip(samples, pops):
            f.write(f"{s}\t{p}\n")
    print("wrote", vcf, "sites", m, "samples", n)


if __name__ == "__main__":
    main()
