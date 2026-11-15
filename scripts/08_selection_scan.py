#!/usr/bin/env python3
"""Flag windowed Fst z-score outliers as selection-scan candidates.

Inputs:  --fst-tsv from 07_diversity_windows.py --out-tsv --z (default 2, toy only)
Outputs: --out-tsv
Tested:  toy Fst table.
Production: formal scans (iHS, XP-CLR, or pre-registered window statistics)
on the unrelated, clone-deduplicated set. The default z=2 is a toy cutoff
only, not a pre-registered grape threshold. High-Fst windows are candidates,
not evidence of selection: population history, low recombination and
background selection can also produce outliers.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

# do not use sed/awk; parse here
def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fst-tsv", required=True)
    ap.add_argument("--outliers-tsv", required=True)
    ap.add_argument("--z-threshold", type=float, default=2.0)
    args = ap.parse_args()
    rows = []
    with Path(args.fst_tsv).open(encoding="utf-8") as f:
        header = f.readline().rstrip("\n").split("\t")
        for line in f:
            p = line.rstrip("\n").split("\t")
            rec = dict(zip(header, p))
            if rec["fst_hudson"] == "NA":
                continue
            rec["_fst"] = float(rec["fst_hudson"])
            rows.append(rec)
    if not rows:
        raise SystemExit("no finite Fst rows")
    vals = np.array([r["_fst"] for r in rows])
    mu, sd = float(vals.mean()), float(vals.std(ddof=1) if len(vals) > 1 else 0.0)
    out = Path(args.outliers_tsv)
    with out.open("x", encoding="utf-8") as f:
        f.write("chrom\tstart\tend\tpop1\tpop2\tfst_hudson\tz\n")
        n = 0
        for r in rows:
            z = 0.0 if sd == 0 else (r["_fst"] - mu) / sd
            if z >= args.z_threshold:
                f.write(f"{r['chrom']}\t{r['start']}\t{r['end']}\t{r['pop1']}\t{r['pop2']}\t{r['fst_hudson']}\t{z:.4f}\n")
                n += 1
    print("outliers", n, "mu", f"{mu:.4f}", "sd", f"{sd:.4f}")


if __name__ == "__main__":
    main()
