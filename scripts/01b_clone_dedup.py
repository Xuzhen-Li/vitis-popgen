#!/usr/bin/env python3
"""Toy identity / clone-group collapse from genotype dosages.

Inputs:  --vcf --out-vcf --related-tsv --keep-samples
         --toy-corr-threshold (default 0.99; toy only)
Outputs: a VCF with one sample kept per toy clone group, plus pair and keep tables.
Tested:  toy VCF (no planted clones; all samples are kept).
Production: run KING first (docs/WORKFLOW.md decisions 3 and 4). Keep one sample
per clone or duplicate group when KING kinship is above 0.354 (the duplicate or
MZ class in the KING manual; Manichaikul et al. 2010, 10.1093/bioinformatics/btq559).
Then handle first-degree relatives (0.177 to 0.354) according to the analysis.
This script is not KING. The --toy-corr-threshold default (0.99) is a toy
dosage-correlation cutoff for the simulator only; it is not a pre-registered
grape cutoff, and it is not convertible to KING kinship. KING kinship for
clones or duplicates is about 0.5 (the 0.354 cutoff already cited in the
WORKFLOW is the KING duplicate/MZ class boundary). The two scales cannot be
interchanged. In each connected toy group this script keeps the first sample
in VCF sample-column order and drops the rest. See also 01c_run_king.sh
(untested plink2 wrapper).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_vcf import dosage, read_vcf_gt, write_tsv, write_vcf_subset


def pairwise_corr(dos):
    n = dos.shape[1]
    out = np.full((n, n), np.nan)
    for i in range(n):
        out[i, i] = 1.0
        xi = dos[:, i]
        for j in range(i + 1, n):
            mask = (~np.isnan(xi)) & (~np.isnan(dos[:, j]))
            if mask.sum() < 20:
                continue
            a, b = xi[mask], dos[mask, j]
            if a.std() == 0 or b.std() == 0:
                continue
            r = float(np.corrcoef(a, b)[0, 1])
            out[i, j] = out[j, i] = r
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--vcf", required=True)
    ap.add_argument("--out-vcf", required=True)
    ap.add_argument("--related-tsv", required=True)
    ap.add_argument("--keep-samples", required=True)
    ap.add_argument("--toy-corr-threshold", type=float, default=0.99,
                    help="toy dosage-correlation cutoff only; not KING kinship 0.354")
    args = ap.parse_args()
    src = Path(args.vcf)
    v = read_vcf_gt(src)
    dos = dosage(v["alleles"])
    samples = list(v["samples"])
    corr = pairwise_corr(dos)
    # connected components of pairs at or above the toy cutoff
    parent = {s: s for s in samples}

    def find(s):
        while parent[s] != s:
            parent[s] = parent[parent[s]]
            s = parent[s]
        return s

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    pairs = []
    for i in range(len(samples)):
        for j in range(i + 1, len(samples)):
            r = corr[i, j]
            if r == r and r >= args.toy_corr_threshold:
                union(samples[i], samples[j])
                pairs.append([samples[i], samples[j], f"{r:.6f}", "toy_clone_or_duplicate"])
    groups = {}
    for s in samples:
        groups.setdefault(find(s), []).append(s)
    keep = []
    dropped = []
    # members were appended in VCF sample-column order, so members[0]
    # is the first sample in that group as it appears in the VCF.
    for members in groups.values():
        keep.append(members[0])
        for s in members[1:]:
            dropped.append([s, members[0]])
    write_vcf_subset(src, Path(args.out_vcf), keep_samples=keep)
    write_tsv(Path(args.related_tsv),
              ["sample_a", "sample_b", "dosage_corr", "note"],
              pairs)
    write_tsv(Path(args.keep_samples),
              ["sample", "status", "kept_as"],
              [[s, "kept", s] for s in keep] +
              [[d, "dropped_toy_clone", k] for d, k in dropped])
    print("samples", len(samples), "kept", len(keep), "dropped", len(dropped),
          "pairs_at_toy_cutoff", len(pairs))


if __name__ == "__main__":
    main()
