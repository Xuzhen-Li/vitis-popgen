#!/usr/bin/env python3
"""Draw two original SVGs for vitis-popgen. No bitmaps, no journal reprints."""
from pathlib import Path

def escape(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))

def box(x, y, w, h, title, lines, fill="#f7f4ee", stroke="#3d4f5f"):
    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>',
        f'<text x="{x+10}" y="{y+22}" font-family="Source Sans 3, DejaVu Sans, sans-serif" font-size="14" font-weight="700" fill="#1f2a33">{escape(title)}</text>',
    ]
    yy = y + 42
    for line in lines:
        parts.append(
            f'<text x="{x+10}" y="{yy}" font-family="Source Sans 3, DejaVu Sans, sans-serif" font-size="11.5" fill="#2b3a45">{escape(line)}</text>'
        )
        yy += 16
    return "\n".join(parts)

def svg_doc(w, h, title, body, foot):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <rect width="{w}" height="{h}" fill="#ffffff"/>
  <text x="28" y="32" font-family="Source Sans 3, DejaVu Sans, sans-serif" font-size="18" font-weight="700" fill="#1f2a33">{escape(title)}</text>
  {body}
  <text x="28" y="{h-16}" font-family="Source Sans 3, DejaVu Sans, sans-serif" font-size="10" fill="#5a6570">{escape(foot)}</text>
</svg>
"""

def write(path, text):
    path = Path(path)
    if path.exists():
        raise SystemExit("exists " + str(path))
    if not path.parent.exists():
        path.parent.mkdir()
    with path.open("x", encoding="utf-8") as f:
        f.write(text if text.endswith("\n") else text + "\n")

def draw_f1(outdir):
    boxes = [
        (28, 52, 280, 118, "ARG methods",
         ["tsinfer, Relate, tsdate (Wohns 2022;", "Pope 2026 if default algorithm),", "SINGER, tskit. No grape ARG here.", "Map, μ and g [待确认]."]),
        (328, 52, 280, 118, "IBD at cohort scale",
         ["hap-IBD (phased data + cM map),", "RaPID2, RZooRoH 2026 update.", "Clone-merge first; not IBD-Ne.", "Not run on Vitis here."]),
        (628, 52, 280, 118, "Local ancestry",
         ["FLARE (abstract + README only),", "MOSAIC, fineSTRUCTURE.", "Local ancestry on a Vitis graph", "was not opened; [待确认]."]),
        (28, 190, 280, 118, "Spatial surfaces",
         ["FEEMS paper (wolves); EEMS only", "as described there.", "Trade-route / clonal cultivars:", "appropriateness [待确认]."]),
        (328, 190, 280, 118, "Graph / SV popgen",
         ["PanGenie and Giraffe papers.", "Liu 2024 Grapepan v.1.0:", "9,105,787 short; 236,449 SVs.", "Guo 2025: 72 haplotype-resolved genomes."]),
        (628, 190, 280, 118, "PGS and load",
         ["Human PGS portability cautions.", "Grape load: Zhou 2017, +5.2%", "(9 wild vs 18 cultivated ind.).", "Arabidopsis/Ulmus are not grape."]),
        (178, 328, 580, 100, "Vitis studies (claims kept side by side)",
         ["Dong 2023: two domestications ~11,000 ya (abstract; no 1-to-1 table/wine map).",
          "Magris 2021: one Western Asian domestication + later introgression.",
          "Xiao 2023: single domestication (not claimed as Western Asia here)."]),
    ]
    body = "\n".join(box(*b) for b in boxes)
    foot = "Original schematic for Xuzhen-Li/vitis-popgen. Boxes cite papers opened 2026-11-15 CST; not a pipeline we ran."
    write(outdir / "F1_popgen_method_map.svg", svg_doc(936, 460, "vitis-popgen: method map for 2026-11-15 additions", body, foot))

def draw_f2(outdir):
    # Quoted panel sizes only. Accession counts taken from abstracts or full texts opened 2026-11-15 CST.
    rows = [
        ("Zhou et al. 2017", "9 wild vs 18 cultivated (14 cultivars)", "~22 kya MSMC cross-coalescence (Fig. 2B); n=4 is vinifera Ne (Fig. 2A); SMC++ ~30 kya"),
        ("Liang et al. 2019", "472 accessions; 48 of 60 species", "recent Ne expansion and contraction in domesticated vines"),
        ("Magris et al. 2021", "204 V. vinifera genomes", "one Western Asian domestication, then European wild introgression"),
        ("Freitas et al. 2021", "n not extracted from opened full text", "local wild hybridization (strongest in Iberian varieties)"),
        ("Dong et al. 2023", "3,525 cultivated and wild", "two domestications ~11,000 ya in W. Asia and Caucasus (not 1-to-1)"),
        ("Xiao et al. 2023", "345 samples (abstract); 328 after curation (correction)", "single domestication; introgression especially into wine grapes"),
        ("Liu et al. 2024", "18 new T2T + 11 published; 466 resequenced cultivars", "Grapepan v.1.0; 236,449 SVs; 88.6% of SVs overlapped TEs"),
        ("Guo et al. 2025", "72 haplotype-resolved genomes (25 wild, 47 cult.)", "over 63 SVs associated with downy mildew resistance"),
        ("Wang et al. 2026 (NA Vitis)", "639 accessions; 48 species", "introgression ~14% of the average Vitis genome"),
        ("Nikoghosyan et al. 2026", "164 accessions (re-analysis)", "wild vs cultivated split; three cultivated components"),
    ]
    header_y = 60
    body_parts = [
        f'<rect x="28" y="48" width="880" height="28" fill="#e8eef2"/>',
        '<text x="40" y="67" font-family="Source Sans 3, DejaVu Sans, sans-serif" font-size="12" font-weight="700" fill="#1f2a33">Paper</text>',
        '<text x="230" y="67" font-family="Source Sans 3, DejaVu Sans, sans-serif" font-size="12" font-weight="700" fill="#1f2a33">Quoted sample size</text>',
        '<text x="470" y="67" font-family="Source Sans 3, DejaVu Sans, sans-serif" font-size="12" font-weight="700" fill="#1f2a33">Quoted claim (see chapter tables for sources)</text>',
    ]
    y = 76
    for i, (paper, n, claim) in enumerate(rows):
        fill = "#ffffff" if i % 2 == 0 else "#f7f4ee"
        body_parts.append(f'<rect x="28" y="{y}" width="880" height="36" fill="{fill}" stroke="#d5dde3" stroke-width="0.8"/>')
        body_parts.append(f'<text x="40" y="{y+23}" font-family="Source Sans 3, DejaVu Sans, sans-serif" font-size="12" fill="#1f2a33">{escape(paper)}</text>')
        body_parts.append(f'<text x="230" y="{y+23}" font-family="Source Sans 3, DejaVu Sans, sans-serif" font-size="12" fill="#2b3a45">{escape(n)}</text>')
        body_parts.append(f'<text x="470" y="{y+23}" font-family="Source Sans 3, DejaVu Sans, sans-serif" font-size="11.5" fill="#2b3a45">{escape(claim)}</text>')
        y += 36
    foot = "Original table-style schematic. Numbers and claims are copied from abstracts or full texts opened 2026-11-15 CST. This is not a reanalysis."
    write(outdir / "F2_vitis_panels_quoted.svg", svg_doc(936, y + 36, "Quoted Vitis panel sizes and claims (opened sources only)", "\n".join(body_parts), foot))

if __name__ == "__main__":
    import sys
    out = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    if not out.exists():
        out.mkdir()
    targets = [out / "F1_popgen_method_map.svg", out / "F2_vitis_panels_quoted.svg"]
    missing = [p for p in targets if p.exists()]
    if missing:
        raise SystemExit("refusing to write; already present: " + ", ".join(str(p) for p in missing))
    draw_f1(out)
    draw_f2(out)
    print("drew F1 and F2 into", out)
