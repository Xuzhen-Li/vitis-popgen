# 2026-11-15 additions (do not replace the existing README)

These files are add-only material for vitis-popgen. Existing README.md, README.zh.md, catalog/CATALOG.tsv, scripts and testdata from the 2026-11-15 merge of PR #4 are not modified here.

New teaching chapters live in docs/ideas/. Each chapter ends with a claim–source table. `SOURCES_READ.tsv` lists every paper and GitHub README opened for these chapters. `catalog/CATALOG_additions_2026-11-15.tsv` lists only newly cited sources or old catalogue tools that now have a verified method paper DOI from a text we actually opened.

Section 16 of the current README listed four ideas that were still lightly tested on Vitis. After this addition:

- ARG dating of grape domestication still has no grape ARG result in this repository. The method chapter (docs/ideas/01_arg_methods.md) now cites tsinfer, Relate, tsdate (Wohns et al. 2022), SINGER, and a 2024 ARG review, and restates the existing caveats (clone-pruned, polarised panel; sexual-origin times; generation time [待确认]).
- Graph-aware introgression and inversion scans still belong primarily in vitis-pangenome. docs/ideas/04_graph_sv_popgen.md adds the PanGenie and Giraffe/vg papers and the Liu 2024 Grapepan v.1.0 variation map.
- Clone-aware ADMIXTURE/PCA and sex-determining-region annotation are not expanded with a new primary paper in the sources opened for these chapters; they remain ideas (see WORKFLOW.md and vitis-open-directions).

A live disagreement in the Vitis literature is recorded, not resolved, in docs/ideas/06_vitis_popgen_recent.md: Dong et al. 2023 argue for two domestication events, whereas Magris et al. 2021 argue for one Western Asian domestication plus later introgression. Xiao et al. 2023 argue for a single domestication; the opened Xiao text does not say Western Asia (a full-text search for “Western Asia” is 0). SV-load and pangenome-graph construction (minigraph-cactus, pggb, vg call) are outside these chapters and remain in vitis-pangenome.
