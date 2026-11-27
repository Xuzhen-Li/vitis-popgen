# Changelog

This is the public summary of changes to the teaching files in `vitis-popgen`. Detailed logs are not part of this repository.

## 2026-11-15

- The tsdate README quotation now uses only the README’s own wording, including the DOI written as `doi: https://doi.org/10.64898/2026.01.07.698223`. The reading note sits outside the quotation marks.
- The Xiao et al. 2023 correction (PMC10756202, 11,216 bytes) and the pixy paper (PMC8044049, 92,442 bytes) were opened; teaching text cites these primary sources directly.
- Bhatia et al. 2013 was opened in full (PMC3759727, 90,871 bytes). The multi-window FST summary as a ratio of averages is quoted from the paper, and the earlier body caveat is lifted.
- The Chinese local-ancestry chapter now includes the three vinifera abstract sentences already quoted in the English chapter.
- The PanGenie GitHub repository description remains [待确认].

Claims without an opened source remain cut or marked [待确认].

## 2026-11-15 (follow-up)

A 2026-11-15 reading (sha256 319cea8a…) accepted the previous teaching files with three non-blocking points. All three are applied. No new blocking points were raised.

- R1. `scripts/07_diversity_windows_v1_9.py` changed from sha256 `ecefe85fbeb29cee…` to sha256 `584b0ad8571ee9d4164e1f2bf3b5089376c94c2f3d0cec64f7338960fec0d4d1`. That edit was docstring-only (Bhatia “ratio of averages” quote and related wording); the code was unchanged. The previous CHANGELOG did not record the new sha. `07_diversity_windows_v1_9.py` retains the same code (only docstring wording is updated here), and further docstring updates also ship in `scripts/07_diversity_windows_v1_10.py` (sha256 `8510b8b842548bd6360d940355db523c3536f057fe637c9a4271efe4b423df66`).
- R2. The phrases at `v1_9.py:92` and `:95` (Hudson 1992, Tajima 1989) referred to abstracts opened earlier rather than on 2026-11-15. Those two `v1_9.py` lines, and the pixy and Bhatia full-text lines in the same file, now use the date 2026-11-15 CST. Pope 2026 in `docs/ideas/01_arg_methods.md:35` still notes that only the abstract was read. In `v1_10`, the pixy and Bhatia full-text opens record the fetch date directly.
- R3. The PanGenie GitHub repository description “Pangenome-based genome inference” was re-fetched from the GitHub repository API (5,185 bytes, sha256 `411a57ee8a50b3d6efb1c8ee252b250116b613574e5f3b69e77ab9e071d1a4f4`) and matches the existing chapter wording. The [待确认] on that description is lifted in `docs/ideas/04_graph_sv_popgen.md` and `SOURCES_READ.tsv`. The README (455 bytes, sha256 `c4cd33b8…`) was also re-fetched.

Claims without an opened source remain cut or marked [待确认].
