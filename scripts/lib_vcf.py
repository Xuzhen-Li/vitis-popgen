#!/usr/bin/env python3
"""Minimal VCF helpers for the vitis-popgen toy scripts. Not a replacement for bcftools.

Site keys are chrom:pos:ref:alt, not the VCF ID column (which is often ".").
Multi-allelic sites (ALT contains a comma) are skipped. Haploid genotypes
(no / or |) are treated as missing and counted.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np


def site_key(chrom, pos, ref, alt):
    return f"{chrom}:{pos}:{ref}:{alt}"


def read_vcf_gt(path: Path):
    samples = None
    recs = []
    n_multiallelic = 0
    n_haploid = 0
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.startswith("##"):
                continue
            if line.startswith("#CHROM"):
                samples = line.rstrip("\n").split("\t")[9:]
                continue
            if not line.strip() or samples is None:
                continue
            p = line.rstrip("\n").split("\t")
            chrom, pos, vid, ref, alt = p[0], int(p[1]), p[2], p[3], p[4]
            if "," in alt or "," in ref:
                n_multiallelic += 1
                continue
            gts = []
            for g in p[9:]:
                tok = g.split(":")[0]
                if tok in (".", "./.", ".|."):
                    gts.append((np.nan, np.nan))
                    continue
                if "/" not in tok and "|" not in tok:
                    n_haploid += 1
                    gts.append((np.nan, np.nan))
                    continue
                sep = "|" if "|" in tok else "/"
                a, b = tok.split(sep)[:2]
                gts.append((np.nan if a == "." else int(a), np.nan if b == "." else int(b)))
            recs.append((chrom, pos, vid, ref, alt, gts))
    if samples is None:
        raise ValueError(f"no VCF header in {path}")
    n = len(samples)
    m = len(recs)
    alleles = np.full((m, n, 2), np.nan, dtype=float)
    chroms, positions, ids, refs, alts, keys = [], [], [], [], [], []
    for i, (chrom, pos, vid, ref, alt, gts) in enumerate(recs):
        chroms.append(chrom)
        positions.append(pos)
        ids.append(vid)
        refs.append(ref)
        alts.append(alt)
        keys.append(site_key(chrom, pos, ref, alt))
        for j, (a, b) in enumerate(gts):
            alleles[i, j, 0] = a
            alleles[i, j, 1] = b
    return {
        "samples": samples,
        "chrom": np.array(chroms),
        "pos": np.array(positions, dtype=int),
        "id": np.array(ids),
        "ref": np.array(refs),
        "alt": np.array(alts),
        "key": np.array(keys),
        "alleles": alleles,
        "n_multiallelic_skipped": n_multiallelic,
        "n_haploid_as_missing": n_haploid,
    }


def dosage(alleles):
    return alleles[:, :, 0] + alleles[:, :, 1]


def write_tsv(path: Path, header, rows):
    with path.open("x", encoding="utf-8") as f:
        f.write("\t".join(header) + "\n")
        for row in rows:
            f.write("\t".join(str(x) for x in row) + "\n")


def read_pops(path: Path):
    pops = {}
    with path.open(encoding="utf-8") as f:
        header = f.readline()
        for line in f:
            if not line.strip():
                continue
            sid, pop = line.rstrip("\n").split("\t")[:2]
            pops[sid] = pop
    return pops


def write_vcf_subset(src: Path, dest: Path, keep_keys=None, keep_samples=None):
    """Rewrite a VCF keeping selected sites (by chrom:pos:ref:alt) and/or samples."""
    keep_keys = None if keep_keys is None else set(keep_keys)
    keep_samples = None if keep_samples is None else list(keep_samples)
    with src.open(encoding="utf-8") as fin, dest.open("x", encoding="utf-8") as fout:
        sample_idx = None
        for line in fin:
            if line.startswith("##"):
                fout.write(line)
                continue
            if line.startswith("#CHROM"):
                cols = line.rstrip("\n").split("\t")
                names = cols[9:]
                if keep_samples is None:
                    sample_idx = list(range(len(names)))
                    fout.write(line)
                else:
                    name_to_i = {n: i for i, n in enumerate(names)}
                    sample_idx = [name_to_i[s] for s in keep_samples]
                    fout.write("\t".join(cols[:9] + [names[i] for i in sample_idx]) + "\n")
                continue
            if not line.strip():
                continue
            cols = line.rstrip("\n").split("\t")
            key = site_key(cols[0], cols[1], cols[3], cols[4])
            if keep_keys is not None and key not in keep_keys:
                continue
            if sample_idx is None:
                fout.write(line)
            elif keep_samples is None:
                fout.write(line)
            else:
                gts = cols[9:]
                fout.write("\t".join(cols[:9] + [gts[i] for i in sample_idx]) + "\n")
