#!/usr/bin/env python3
"""Windowed pi, Tajima's D (per population) and pairwise Fst (Hudson).

Inputs:  --vcf --pops --window-bp (default 50000, toy) --step-bp (default 25000, toy)
         optional --accessible-bed (chrom, 0-based start, end; half-open)
Outputs: --diversity-tsv --fst-tsv
         start and end columns are 0-based, half-open (BED-style).
Tested:  toy VCF, numpy.
Production: pixy on an all-sites VCF with an accessible-site mask
(docs/WORKFLOW.md decision 6). This toy VCF is variants-only, so the
mean per-variant-site pi is not a per-base rate. Per-base pi
(pi_per_callable_site) is written only when --accessible-bed is given.
The numerator is the sum of per-site pi over variant sites whose 1-based
VCF POS, converted to a 0-based coordinate, falls inside the accessible
intervals (and inside the window). The denominator is the number of
accessible bases in the window, using the same 0-based half-open intervals.
Without a bed, that column is NA.
A MAF-filtered VCF removes low-frequency variants from the numerator
without shrinking the callable denominator, so per-base pi would be too
low. Give this script a VCF that has not been MAF-filtered (the toy
driver uses the post-dedup, pre-MAF VCF). Production still uses pixy
on an all-sites VCF. Window and step defaults are toy values only. A window is emitted only when
it contains at least --min-variant-sites variants after the callable-bed
filter (default 5). That gate drops low-diversity windows and can bias
per-window pi upward; whether to keep it, and at what value, is left to
statistics review [待确认].
Hudson Fst uses the same site set for the within and between terms
(sites with at least two called individuals in both populations).
Whether to average ratios or take a ratio of averages is left to
statistics review; this script uses a ratio of means on that shared set.
"""
from __future__ import annotations

import argparse
import itertools
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_vcf import dosage, read_pops, read_vcf_gt, write_tsv


def load_accessible(path: Path):
    iv = defaultdict(list)
    with path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#"):
                continue
            chrom, start, end = line.rstrip("\n").split("\t")[:3]
            iv[chrom].append((int(start), int(end)))
    for chrom in iv:
        iv[chrom].sort()
    return iv


def site_in_bed(iv, chrom, pos0):
    for a, b in iv.get(chrom, []):
        if a <= pos0 < b:
            return True
    return False


def callable_in_window(iv, chrom, start, end):
    # start and end are 0-based half-open
    n = 0
    for a, b in iv.get(chrom, []):
        lo, hi = max(a, start), min(b, end)
        if hi > lo:
            n += hi - lo
    return n


def pi_tajima(dos):
    called = np.sum(~np.isnan(dos), axis=1)
    ac = np.nansum(dos, axis=1)
    ok = called >= 2
    if ok.sum() == 0:
        return np.nan, np.nan, 0, np.nan
    n_al = called.astype(float) * 2
    p = np.divide(ac, n_al, out=np.zeros_like(ac, dtype=float), where=n_al > 0)
    with np.errstate(invalid="ignore", divide="ignore"):
        pi_s = 2 * p * (1 - p) * n_al / (n_al - 1)
    pi_s = np.where(n_al > 1, pi_s, np.nan)
    mean_pi_per_variant = float(np.nanmean(pi_s[ok]))
    S = int(np.sum((ac > 0) & (ac < n_al) & ok))
    if S < 2:
        return mean_pi_per_variant, np.nan, int(ok.sum()), float(np.nansum(pi_s[ok]))
    n_mean = float(np.mean(n_al[ok]))
    a1 = np.sum(1.0 / np.arange(1, n_mean))
    a2 = np.sum(1.0 / np.arange(1, n_mean) ** 2)
    b1 = (n_mean + 1) / (3 * (n_mean - 1))
    b2 = 2 * (n_mean ** 2 + n_mean + 3) / (9 * n_mean * (n_mean - 1))
    c1 = b1 - 1 / a1
    c2 = b2 - (n_mean + 2) / (a1 * n_mean) + a2 / a1 ** 2
    e1 = c1 / a1
    e2 = c2 / (a1 ** 2 + a2)
    theta_w = S / a1
    pi_sum = float(np.nansum(pi_s[ok]))
    var = e1 * S + e2 * S * (S - 1)
    d = (pi_sum - theta_w) / np.sqrt(var) if var > 0 else np.nan
    return mean_pi_per_variant, float(d), int(ok.sum()), pi_sum


def hudson_fst(d1, d2):
    c1 = np.sum(~np.isnan(d1), axis=1)
    c2 = np.sum(~np.isnan(d2), axis=1)
    ok = (c1 >= 2) & (c2 >= 2)
    if ok.sum() == 0:
        return np.nan, 0
    d1s, d2s = d1[ok], d2[ok]
    pi1, _, _, _ = pi_tajima(d1s)
    pi2, _, _, _ = pi_tajima(d2s)
    ac1 = np.nansum(d1s, axis=1)
    ac2 = np.nansum(d2s, axis=1)
    n1 = np.sum(~np.isnan(d1s), axis=1) * 2
    n2 = np.sum(~np.isnan(d2s), axis=1) * 2
    p1 = np.divide(ac1, n1, out=np.zeros_like(ac1, dtype=float), where=n1 > 0)
    p2 = np.divide(ac2, n2, out=np.zeros_like(ac2, dtype=float), where=n2 > 0)
    pib = float(np.mean(p1 * (1 - p2) + p2 * (1 - p1)))
    piw = np.nanmean([pi1, pi2])
    if pib == 0 or np.isnan(pib) or np.isnan(piw):
        return np.nan, int(ok.sum())
    return float(1.0 - piw / pib), int(ok.sum())


def fmt(x):
    return f"{x:.8f}" if x == x else "NA"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--vcf", required=True)
    ap.add_argument("--pops", required=True)
    ap.add_argument("--diversity-tsv", required=True)
    ap.add_argument("--fst-tsv", required=True)
    ap.add_argument("--window-bp", type=int, default=50000)
    ap.add_argument("--step-bp", type=int, default=25000)
    ap.add_argument("--accessible-bed")
    ap.add_argument("--min-variant-sites", type=int, default=5,
                    help="minimum variants in a window after the callable filter; default 5 is a toy gate that can bias pi upward, statistics review [待确认]")
    args = ap.parse_args()
    if args.min_variant_sites < 1:
        raise SystemExit("--min-variant-sites must be at least 1")
    v = read_vcf_gt(Path(args.vcf))
    dos = dosage(v["alleles"])
    pops = read_pops(Path(args.pops))
    pop_of = np.array([pops[s] for s in v["samples"]])
    pop_names = sorted(set(pop_of))
    acc = load_accessible(Path(args.accessible_bed)) if args.accessible_bed else None
    div_rows, fst_rows = [], []
    for chrom in np.unique(v["chrom"]):
        idx = np.where(v["chrom"] == chrom)[0]
        pos0 = v["pos"][idx].astype(int) - 1  # VCF POS is 1-based
        pmin0, pmax0 = int(pos0.min()), int(pos0.max())
        win_start = pmin0
        while win_start <= pmax0:
            win_end = win_start + args.window_bp
            in_win = (pos0 >= win_start) & (pos0 < win_end)
            sel = idx[in_win]
            pos0_sel = pos0[in_win]
            if acc is not None:
                in_acc = np.array([site_in_bed(acc, chrom, int(p)) for p in pos0_sel], dtype=bool)
                sel = sel[in_acc]
                n_callable = callable_in_window(acc, chrom, win_start, win_end)
            else:
                n_callable = None
            if len(sel) >= args.min_variant_sites:
                for pop in pop_names:
                    d = dos[np.ix_(sel, pop_of == pop)]
                    mean_pi, td, n_ok, pi_sum = pi_tajima(d)
                    if n_callable is not None and n_callable > 0:
                        pi_call = pi_sum / n_callable if pi_sum == pi_sum else np.nan
                    else:
                        pi_call = np.nan
                    div_rows.append([
                        chrom, win_start, win_end, pop, len(sel), n_ok,
                        n_callable if n_callable is not None else "NA",
                        fmt(mean_pi), fmt(pi_call), fmt(td),
                    ])
                for a, b in itertools.combinations(pop_names, 2):
                    fst, n_shared = hudson_fst(
                        dos[np.ix_(sel, pop_of == a)],
                        dos[np.ix_(sel, pop_of == b)],
                    )
                    fst_rows.append([chrom, win_start, win_end, a, b, len(sel), n_shared, fmt(fst)])
            win_start += args.step_bp
    write_tsv(Path(args.diversity_tsv),
              ["chrom", "start", "end", "population", "n_variant_sites", "n_ok",
               "n_callable_sites", "mean_pi_per_variant_site",
               "pi_per_callable_site", "tajima_d"],
              div_rows)
    write_tsv(Path(args.fst_tsv),
              ["chrom", "start", "end", "pop1", "pop2", "n_variant_sites",
               "n_shared_called_sites", "fst_hudson"],
              fst_rows)
    print("div_windows", len(div_rows), "fst_windows", len(fst_rows))


if __name__ == "__main__":
    main()
