#!/usr/bin/env python3
"""Allele-frequency f2, f3 and f4 on a toy VCF.

Inputs:  --vcf --pops --out-prefix
Outputs: prefix_f2.tsv, prefix_f3.tsv, prefix_f4.tsv
Tested:  toy VCF (three populations, so f4 is empty).
Production: ADMIXTOOLS2 with block jackknife.
This script uses raw sample frequencies with no finite-sample bias
correction (no heterozygosity term is subtracted). f2 and f3 are therefore
biased upward, and a negative f3 is harder to observe, so admixture would
be under-called. These are biased toy estimates; do not decide whether f3
is negative from this output. Whether and how to correct the bias is left
to statistics review.
"""
from __future__ import annotations

import argparse
import itertools
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_vcf import dosage, read_pops, read_vcf_gt, write_tsv


def pop_freq(dos, mask):
    d = dos[:, mask]
    an = 2 * np.sum(~np.isnan(d), axis=1)
    ac = np.nansum(d, axis=1)
    p = np.divide(ac, an, out=np.full(len(ac), np.nan), where=an > 0)
    return p, an


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--vcf", required=True)
    ap.add_argument("--pops", required=True)
    ap.add_argument("--f2-tsv", required=True)
    ap.add_argument("--f3-tsv", required=True)
    ap.add_argument("--f4-tsv", required=True)
    args = ap.parse_args()
    v = read_vcf_gt(Path(args.vcf))
    dos = dosage(v["alleles"])
    pops = read_pops(Path(args.pops))
    pop_of = np.array([pops[s] for s in v["samples"]])
    names = sorted(set(pop_of))
    freq = {}
    for name in names:
        freq[name] = pop_freq(dos, pop_of == name)[0]
    f2, f3, f4 = [], [], []
    for a, b in itertools.combinations(names, 2):
        d = (freq[a] - freq[b]) ** 2
        f2.append([a, b, f"{np.nanmean(d):.8f}", int(np.isfinite(d).sum())])
    if len(names) >= 3:
        for c in names:
            others = [x for x in names if x != c]
            for a, b in itertools.combinations(others, 2):
                d = (freq[c] - freq[a]) * (freq[c] - freq[b])
                f3.append([c, a, b, f"{np.nanmean(d):.8f}", int(np.isfinite(d).sum())])
    if len(names) >= 4:
        for a, b, c, dpop in itertools.permutations(names, 4):
            # report each unordered quartet once: a,b;c,d with a<b, c<d, a<c
            if not (a < b and c < d and a < c):
                continue
            val = (freq[a] - freq[b]) * (freq[c] - freq[dpop])
            f4.append([a, b, c, dpop, f"{np.nanmean(val):.8f}", int(np.isfinite(val).sum())])
    write_tsv(Path(args.f2_tsv), ["pop1", "pop2", "f2", "n_sites"], f2)
    write_tsv(Path(args.f3_tsv), ["popC", "popA", "popB", "f3_CAB", "n_sites"], f3)
    write_tsv(Path(args.f4_tsv), ["popA", "popB", "popC", "popD", "f4", "n_sites"], f4)
    print("f2", len(f2), "f3", len(f3), "f4", len(f4))


if __name__ == "__main__":
    main()
