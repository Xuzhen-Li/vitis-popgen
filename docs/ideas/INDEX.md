# 2026-11-15 idea chapters

Add-only teaching chapters for vitis-popgen. Existing README, catalogue and scripts are not replaced.

| Chapter | English | Chinese |
|---|---|---|
| 1. ARG methods | [01_arg_methods.md](01_arg_methods.md) | [01_arg_methods.zh.md](01_arg_methods.zh.md) |
| 2. IBD at cohort scale | [02_ibd_cohort.md](02_ibd_cohort.md) | [02_ibd_cohort.zh.md](02_ibd_cohort.zh.md) |
| 3. Local ancestry and spatial structure | [03_local_ancestry_spatial.md](03_local_ancestry_spatial.md) | [03_local_ancestry_spatial.zh.md](03_local_ancestry_spatial.zh.md) |
| 4. Graph-aware SV popgen | [04_graph_sv_popgen.md](04_graph_sv_popgen.md) | [04_graph_sv_popgen.zh.md](04_graph_sv_popgen.zh.md) |
| 5. Polygenic scores and mutation load | [05_pgs_and_load.md](05_pgs_and_load.md) | [05_pgs_and_load.zh.md](05_pgs_and_load.zh.md) |
| 6. Recent Vitis popgen studies | [06_vitis_popgen_recent.md](06_vitis_popgen_recent.md) | [06_vitis_popgen_recent.zh.md](06_vitis_popgen_recent.zh.md) |

Each English chapter ends with a claim–source table. Figures: [F1](../../figures/F1_popgen_method_map.svg), [F2](../../figures/F2_vitis_panels_quoted.svg).

## Assumptions that apply across these chapters (not results)

- Clone merging: this repository’s rule on live Xuzhen-Li/vitis-popgen main (commit `eb29b98c…`, `docs/WORKFLOW.md` step 3) treats KING kinship greater than 0.354 as the same clone or duplicate (KING manual duplicate/MZ class, opened; Manichaikul et al. 2010 abstract opened, body [待确认]) and does not drop first-degree relatives as clones. A later change to the rule is [待确认].
- Selfing is expected to inflate HBD / IBD; somatic mutations are expected to affect ARG mutation counts and tip dates; wild–cultivated introgression is expected to affect FLARE reference panels and ARG population labels (this repository’s reasoning, not sourced here; [待确认]).
- Calendar dates from demographic models depend on μ and g and are not directly comparable across studies (chapter 6).
- A *Vitis* genetic map, and grape values of μ and g, remain [待确认].
