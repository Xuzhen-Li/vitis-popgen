#!/usr/bin/env python3
"""Windowed pi, Tajima's D (per population) and pairwise Fst (Hudson).

Version v1_10 (2026-11-15, R1–R2). This file is a new
script. It does not overwrite 07_diversity_windows.py,
07_diversity_windows_v1_7.py, 07_diversity_windows_v1_8.py, or
07_diversity_windows_v1_9.py (sha256
584b0ad8571ee9d4164e1f2bf3b5089376c94c2f3d0cec64f7338960fec0d4d1).
The earlier edit of v1_9.py (prior sha256 ecefe85fbeb29cee… →
584b0ad8571ee9d4…) was docstring-only; that in-place sha change is
recorded in CHANGELOG and the build-side log. Further docstring wording
belongs in this new filename.

Inputs:  --vcf --pops --window-bp (default 50000, toy) --step-bp (default 25000, toy)
         optional --accessible-bed (chrom, 0-based start, end; half-open)
         optional --chrom-sizes (chrom, length) so the window grid can cover
         the full chromosome. Without it, the grid runs from 0 to
         max(last variant 0-based end, last bed end on that chrom).
Outputs: --diversity-tsv --fst-tsv
         start and end columns are 0-based, half-open (BED-style).
         The end column is the clipped end (clip_end = min(win_start +
         window, chrom length)), not the unclipped win_start + window_bp.
Tested:  toy VCF; a zero-variant window with callable bases emits pi=0;
         a window with variants but fewer than two called individuals in
         a population emits NA for that population, not 0.
Production: pixy on an all-sites VCF with an accessible-site mask
(docs/WORKFLOW.md decision 6). This toy VCF is variants-only, so
mean_pi_per_variant_site is not a per-base rate.

When --accessible-bed is given:
  * the default --min-variant-sites is 0, so a window with 0 variants and
    enough callable bases is emitted with pi_per_callable_site = 0.
  * if the window has one or more variants, but a population has fewer
    than two called individuals at all of those sites, pi_per_callable_site
    and mean_pi_per_variant_site are NA for that population (not 0).
    Only a window with zero variants in the selected set (len(sel)==0)
    is written as pi_per_callable_site = 0.
  * the diversity gate is --min-callable-sites (default 1, i.e. the window
    must have a non-empty denominator). The current production ruling,
    still [待确认] until run on real grape data, is a fraction of the
    clipped window length: --min-callable-frac 0.5 (for the default
    50 kb window that is 25,000 bases), with sensitivity analyses at
    0.25 and 0.75. When --min-callable-frac is set, it replaces the
    integer cutoff for that run. The script prints the fraction of
    grid windows dropped by the callable gate, and, if --te-bed is
    given, the mean overlap of dropped versus kept windows with the
    TE annotation. The gate only controls precision; it does not
    correct the denominator bias below. Terminal short windows should
    be reported separately because a fixed integer cutoff would drop
    them more often.
  * the denominator n_callable_sites is the number of accessible bases in
    the window from the bed. It is NOT reduced by per-population missing
    genotypes. That can bias pi_per_callable_site downward, in the
    direction described by Korunes and Samuk 2021 (pixy,
    doi:10.1111/1755-0998.13326; full text opened in v5,
    PMC8044049, NCBI efetch XML 92,442 bytes, 2026-11-15 CST): treating
    missing genotypes as invariant
    biases pi downward). A per-population, per-site callable count (as
    in pixy) is the production alternative. v1_9 output is for
    description or toy checks, not a formal grape result.
  * Cross-window summaries of pi_per_callable_site must be weighted by
    callable bases: (sum of pi_per_callable_site * n_callable_sites)
    / (sum of n_callable_sites), over windows where
    pi_per_callable_site is not NA. Do not take an unweighted mean of
    per-window pi. Zero-variant windows (pi=0) belong in that weighted
    sum; NA windows do not.
  * Fst is gated only by --min-variant-sites-fst (default 5), not by
    --min-variant-sites or --min-callable-sites. A zero-variant window
    has an undefined Hudson Fst and is omitted under the default Fst
    gate. A single-window Hudson Fst may be negative; do not clip
    negatives to 0. For a genome-wide or multi-window summary, do not
    average per-window Fst; use the sum of per-window numerators over
    the sum of per-window denominators (the practice attributed to
    Bhatia et al. 2013, doi:10.1101/gr.154831.113). The opened full
    text (PMC3759727, NCBI efetch XML 90,871 bytes, 2026-11-15 CST)
    recommends a ratio of averages. Verbatim: “In the first approach,
    variance components—the numerator and denominator—are averaged
    separately and the genome-wide estimate of FST is a ‘ratio of
    averages’ … This is the basis of our recommendation that FST be
    estimated as a ratio of averages.” Columns fst_hudson_num and
    fst_hudson_den are written so those sums can be formed.

Without a bed, mean_pi_per_variant_site remains a descriptive statistic,
the default --min-variant-sites is 5, and pi_per_callable_site is NA.

The window grid starts at 0 and steps across the chromosome (or the
fallback end described above). It does not start at the first variant.
A MAF-filtered VCF removes low-frequency variants from the numerator
without shrinking the callable denominator, so per-base pi would be too
low. Give this script a VCF that has not been MAF-filtered.
Hudson Fst uses the same site set for the within and between terms
(sites with at least two called individuals in both populations) and a
ratio of means on that shared set. Citations for the method names:
Hudson, Slatkin and Maddison 1992 (doi:10.1093/genetics/132.2.583;
abstract opened in v4; body [待确认]); Bhatia et al. 2013
(doi:10.1101/gr.154831.113; full text opened in v5,
PMC3759727); Tajima 1989
(doi:10.1093/genetics/123.3.585; abstract opened in v4;
body [待确认]). The opened Hudson abstract compares
FST and a cladistic migration estimator and does not restate the
window formula used here; that formula match remains [待确认]
against the paper body.

TEST_SUMMARY addition for v1_9: a no-bed run must leave
n_callable_sites and pi_per_callable_site as NA and still write
mean_pi_per_variant_site. Toy inputs and the numeric result of that
counterexample are recorded in the build-side log after the script is run
on local tests.
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


def load_chrom_sizes(path: Path):
    sizes = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            sizes[parts[0]] = int(parts[1])
    return sizes


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
    n_ok = int(ok.sum())
    if n_ok == 0:
        return np.nan, 0, np.nan, np.nan
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
        return np.nan, n_ok, np.nan, np.nan
    # Site-weighted numerator and denominator so multi-window
    # summaries can use sum(num)/sum(den) instead of mean(Fst).
    num = (pib - piw) * n_ok
    den = pib * n_ok
    return float(1.0 - piw / pib), n_ok, float(num), float(den)


def fmt(x):
    return f"{x:.8f}" if x == x else "NA"


def chrom_end_fallback(chrom, v, acc):
    idx = np.where(v["chrom"] == chrom)[0]
    ends = []
    if len(idx):
        ends.append(int(v["pos"][idx].max()))  # 1-based POS, equal to 0-based exclusive end of that base
    if acc is not None and chrom in acc:
        ends.append(max(b for _, b in acc[chrom]))
    return max(ends) if ends else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--vcf", required=True)
    ap.add_argument("--pops", required=True)
    ap.add_argument("--diversity-tsv", required=True)
    ap.add_argument("--fst-tsv", required=True)
    ap.add_argument("--window-bp", type=int, default=50000)
    ap.add_argument("--step-bp", type=int, default=25000)
    ap.add_argument("--accessible-bed")
    ap.add_argument("--chrom-sizes", help="tab-delimited chrom, length; recommended so the grid covers the full chromosome")
    ap.add_argument("--min-variant-sites", type=int, default=None,
                    help="minimum variants after the callable filter for a diversity row. Default 0 when a bed is given (zero-variant windows emit pi=0), else 5. Without a bed this is not a per-base rate. This gate does not apply to Fst rows.")
    ap.add_argument("--min-callable-sites", type=int, default=1,
                    help="minimum accessible bases in the window when a bed is given, for diversity rows only. Default 1 only requires a non-empty denominator. Ignored when --min-callable-frac is set. This gate does not apply to Fst rows.")
    ap.add_argument("--min-callable-frac", type=float, default=None,
                    help="if set, diversity rows require n_callable >= frac times the clipped window length. The current production ruling is 0.5, with sensitivity runs at 0.25 and 0.75, still [待确认]. This gate does not apply to Fst rows.")
    ap.add_argument("--te-bed",
                    help="optional BED of TE intervals used only to report overlap of dropped versus kept windows; not a filter")
    ap.add_argument("--min-variant-sites-fst", type=int, default=5,
                    help="minimum variants for an Fst row, independent of --min-variant-sites and --min-callable-sites; kept separate because Fst is undefined at 0 variants")
    args = ap.parse_args()
    if args.min_callable_sites < 0:
        raise SystemExit("--min-callable-sites must be >= 0")
    if args.min_callable_frac is not None and not (0.0 <= args.min_callable_frac <= 1.0):
        raise SystemExit("--min-callable-frac must be between 0 and 1 inclusive")
    if args.min_variant_sites_fst < 0:
        raise SystemExit("--min-variant-sites-fst must be >= 0")
    v = read_vcf_gt(Path(args.vcf))
    dos = dosage(v["alleles"])
    pops = read_pops(Path(args.pops))
    pop_of = np.array([pops[s] for s in v["samples"]])
    pop_names = sorted(set(pop_of))
    acc = load_accessible(Path(args.accessible_bed)) if args.accessible_bed else None
    te = load_accessible(Path(args.te_bed)) if args.te_bed else None
    sizes = load_chrom_sizes(Path(args.chrom_sizes)) if args.chrom_sizes else {}
    if args.min_variant_sites is None:
        args.min_variant_sites = 0 if acc is not None else 5
    if args.min_variant_sites < 0:
        raise SystemExit("--min-variant-sites must be >= 0")
    div_rows, fst_rows = [], []
    n_grid = 0
    n_dropped_callable = 0
    te_dropped = []
    te_kept = []
    chroms = list(np.unique(v["chrom"]))
    if acc is not None:
        for c in acc:
            if c not in chroms:
                chroms.append(c)
    if sizes:
        for c in sizes:
            if c not in chroms:
                chroms.append(c)
    for chrom in chroms:
        idx = np.where(v["chrom"] == chrom)[0]
        pos0 = v["pos"][idx].astype(int) - 1 if len(idx) else np.array([], dtype=int)
        end = sizes.get(chrom, chrom_end_fallback(chrom, v, acc))
        if end <= 0:
            continue
        win_start = 0
        while win_start < end:
            win_end = win_start + args.window_bp
            clip_end = min(win_end, end)
            in_win = (pos0 >= win_start) & (pos0 < clip_end)
            sel = idx[in_win] if len(idx) else np.array([], dtype=int)
            pos0_sel = pos0[in_win] if len(idx) else np.array([], dtype=int)
            if acc is not None:
                if len(pos0_sel):
                    in_acc = np.array([site_in_bed(acc, chrom, int(p)) for p in pos0_sel], dtype=bool)
                    sel = sel[in_acc]
                n_callable = callable_in_window(acc, chrom, win_start, clip_end)
            else:
                n_callable = None
            clipped_len = clip_end - win_start
            if n_callable is None:
                pass_callable = True
            elif args.min_callable_frac is not None:
                pass_callable = n_callable >= (args.min_callable_frac * clipped_len)
            else:
                pass_callable = n_callable >= args.min_callable_sites
            n_grid += 1
            if n_callable is not None and not pass_callable:
                n_dropped_callable += 1
            if te is not None:
                te_bp = callable_in_window(te, chrom, win_start, clip_end)
                te_frac = (te_bp / clipped_len) if clipped_len else 0.0
                if n_callable is not None and not pass_callable:
                    te_dropped.append(te_frac)
                else:
                    te_kept.append(te_frac)
            if pass_callable and len(sel) >= args.min_variant_sites:
                for pop in pop_names:
                    if len(sel) == 0:
                        mean_pi, td, n_ok, pi_sum = np.nan, np.nan, 0, 0.0
                        if n_callable is not None and n_callable > 0:
                            pi_call = 0.0
                        else:
                            pi_call = np.nan
                    else:
                        d = dos[np.ix_(sel, pop_of == pop)]
                        mean_pi, td, n_ok, pi_sum = pi_tajima(d)
                        # N1: do not coerce a NaN pi_sum to 0. Zero is reserved
                        # for windows with no selected variants (len(sel)==0).
                        if n_callable is not None and n_callable > 0 and pi_sum == pi_sum:
                            pi_call = pi_sum / n_callable
                        else:
                            pi_call = np.nan
                    div_rows.append([
                        chrom, win_start, clip_end, pop, len(sel), n_ok,
                        n_callable if n_callable is not None else "NA",
                        fmt(mean_pi), fmt(pi_call), fmt(td),
                    ])
            # Fst uses only --min-variant-sites-fst, not the diversity gates.
            if len(sel) >= args.min_variant_sites_fst:
                for a, b in itertools.combinations(pop_names, 2):
                    fst, n_shared, num, den = hudson_fst(
                        dos[np.ix_(sel, pop_of == a)],
                        dos[np.ix_(sel, pop_of == b)],
                    )
                    fst_rows.append([chrom, win_start, clip_end, a, b, len(sel), n_shared, fmt(fst), fmt(num), fmt(den)])
            win_start += args.step_bp
    write_tsv(Path(args.diversity_tsv),
              ["chrom", "start", "end", "population", "n_variant_sites", "n_ok",
               "n_callable_sites", "mean_pi_per_variant_site",
               "pi_per_callable_site", "tajima_d"],
              div_rows)
    write_tsv(Path(args.fst_tsv),
              ["chrom", "start", "end", "pop1", "pop2", "n_variant_sites",
               "n_shared_called_sites", "fst_hudson", "fst_hudson_num",
               "fst_hudson_den"],
              fst_rows)
    dropped_frac = (n_dropped_callable / n_grid) if n_grid else "NA"
    print("div_windows", len(div_rows), "fst_windows", len(fst_rows),
          "n_windows_grid", n_grid,
          "n_windows_dropped_by_callable", n_dropped_callable,
          "dropped_frac_callable", dropped_frac)
    if te is not None:
        def _mean(xs):
            return (sum(xs) / len(xs)) if xs else "NA"
        print("te_overlap_mean_dropped", _mean(te_dropped),
              "te_overlap_mean_kept", _mean(te_kept))


if __name__ == "__main__":
    main()
