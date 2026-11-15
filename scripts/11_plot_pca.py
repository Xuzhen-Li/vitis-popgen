#!/usr/bin/env python3
"""Write a simple SVG scatter plot of PC1 vs PC2 from 04_pca.py scores.

Inputs:  --scores-tsv
Outputs: --svg
Tested:  toy PCA scores. Does not require matplotlib.
"""
from __future__ import annotations

import argparse
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--scores-tsv", required=True)
    ap.add_argument("--svg", required=True)
    args = ap.parse_args()
    rows = []
    with Path(args.scores_tsv).open(encoding="utf-8") as f:
        header = f.readline().rstrip("\n").split("\t")
        for line in f:
            rec = dict(zip(header, line.rstrip("\n").split("\t")))
            rows.append(rec)
    xs = [float(r["PC1"]) for r in rows]
    ys = [float(r["PC2"]) for r in rows]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    def sx(x):
        return 60 + (x - xmin) / (xmax - xmin + 1e-12) * 520
    def sy(y):
        return 360 - (y - ymin) / (ymax - ymin + 1e-12) * 300
    colours = {"POP1": "#1f72ae", "POP2": "#119b76", "POP3": "#f77e12", "NA": "#444444"}
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="420" viewBox="0 0 640 420">',
        '<rect width="640" height="420" fill="#ffffff"/>',
        '<text x="320" y="28" text-anchor="middle" font-size="16" font-family="sans-serif">PCA (toy VCF)</text>',
        '<line x1="60" y1="360" x2="580" y2="360" stroke="#222" />',
        '<line x1="60" y1="360" x2="60" y2="60" stroke="#222" />',
        '<text x="320" y="400" text-anchor="middle" font-size="12" font-family="sans-serif">PC1</text>',
        '<text x="18" y="210" font-size="12" font-family="sans-serif" transform="rotate(-90 18 210)">PC2</text>',
    ]
    for r, x, y in zip(rows, xs, ys):
        c = colours.get(r.get("population", "NA"), "#444444")
        parts.append(f'<circle cx="{sx(x):.2f}" cy="{sy(y):.2f}" r="5" fill="{c}" stroke="#111" stroke-width="0.5"/>')
    parts.append("</svg>\n")
    with Path(args.svg).open("x", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print("points", len(rows))


if __name__ == "__main__":
    main()
