#!/usr/bin/env python3
"""PCA on mean-imputed genotype dosages.

Inputs:  --vcf --pops --out-prefix --n-pcs (default 5)
Outputs: prefix_scores.tsv, prefix_loadings.tsv, prefix_variance.tsv
Tested:  toy VCF, sklearn.
Production: plink2 --pca on an LD-pruned, unrelated subset; project relatives.
Before that, merge clones and duplicates with KING (docs/WORKFLOW.md decision 3:
kinship above 0.354, one sample per clone group). This script does not drop
relatives or clones. Use 01b_clone_dedup.py or 01c_run_king.sh first.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from sklearn.decomposition import PCA

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_vcf import dosage, read_pops, read_vcf_gt, write_tsv


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--vcf", required=True)
    ap.add_argument("--pops", default=None)
    ap.add_argument("--scores-tsv", required=True)
    ap.add_argument("--loadings-tsv", required=True)
    ap.add_argument("--variance-tsv", required=True)
    ap.add_argument("--n-pcs", type=int, default=5)
    args = ap.parse_args()
    v = read_vcf_gt(Path(args.vcf))
    dos = dosage(v["alleles"])
    colmean = np.nanmean(dos, axis=1)
    for i in range(dos.shape[0]):
        nan = np.isnan(dos[i])
        dos[i, nan] = colmean[i]
    x = dos.T  # samples x sites
    x = x - x.mean(axis=0, keepdims=True)
    k = min(args.n_pcs, x.shape[0] - 1, x.shape[1])
    pca = PCA(n_components=k, svd_solver="full")
    scores = pca.fit_transform(x)
    pops = read_pops(Path(args.pops)) if args.pops else {}
    write_tsv(Path(args.scores_tsv),
              ["sample_id", "population"] + [f"PC{i+1}" for i in range(k)],
              [[v["samples"][j], pops.get(v["samples"][j], "NA"),
                *[f"{scores[j, i]:.8f}" for i in range(k)]]
               for j in range(len(v["samples"]))])
    write_tsv(Path(args.loadings_tsv),
              ["id", "chrom", "pos"] + [f"PC{i+1}" for i in range(k)],
              [[v["id"][i], v["chrom"][i], v["pos"][i],
                *[f"{pca.components_[c, i]:.8f}" for c in range(k)]]
               for i in range(len(v["id"]))])
    write_tsv(Path(args.variance_tsv),
              ["PC", "explained_variance_ratio"],
              [[f"PC{i+1}", f"{pca.explained_variance_ratio_[i]:.8f}"] for i in range(k)])
    print("PCs", k, "var1", f"{pca.explained_variance_ratio_[0]:.4f}")


if __name__ == "__main__":
    main()
