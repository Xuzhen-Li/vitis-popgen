# Identity-by-descent at cohort scale

The existing catalogue already has KING, GCTA, ngsRelate, hapROH and low-coverage kinship tools. This chapter adds cohort-scale IBD segment callers whose papers or READMEs were opened for these chapters. We did not run them on grape.

## hap-IBD

Zhou, Browning and Browning (2020, abstract; the AJHG PMC XML does not include the full article body, doi:10.1016/j.ajhg.2020.02.010) wrote:

> “Our method, called hap-IBD, combines a compressed representation of haplotype data, the positional Burrows-Wheeler transform, and multi-threaded execution to produce very fast analysis times. … We evaluate hap-IBD and four state-of-the-art IBD segment detection methods (GERMLINE, iLASH, RaPID, and TRUFFLE) using UK Biobank chromosome 20 data and simulated sequence data. We show that hap-IBD detects IBD segments faster and more accurately than competing methods, and that hap-IBD is the only method that can rapidly and accurately detect short 2–4 centiMorgan (cM) IBD segments in the full UK Biobank data. Analysis of 485,346 UK Biobank samples … detects 231.5 billion autosomal IBD segments with length ≥2 cM in 24.4 h.”

The method requires **phased** genotype data and a cM genetic map. The GitHub README (https://github.com/browning-lab/hap-ibd) says the program “detects identity-by-descent (IBD) segments and homozygosity-by-descent (HBD) segments in phased genotype data” and “can analyze data sets with hundreds of thousands of samples.” Required parameters include `gt=` (phased genotypes, no missing alleles) and `map=` (PLINK format, cM). The README’s example maps are human HapMap GRCh36/37/38. Those speed and accuracy comparisons, and the 2–4 cM claim, are on UK Biobank and simulations, not on Vitis.

## Other IBD software opened here

RaPID2 (Tang et al. 2026, full text, doi:10.1093/bioadv/vbag078) is titled “RaPID2: a parallel scalable framework for identity-by-descent segment detection via parallel PBWT.”

The 2026 update of RZooRoH (Forneris et al. 2026, full text, doi:10.1111/1755-0998.70186) is titled “Updating the RZooRoH Package for the Analysis of Inbreeding, Identity-By-Descent and Relatedness From Genomic Data.” Use that paper for the package’s current IBD/inbreeding functions; do not treat it as a grape analysis.


## Assumptions before applying to Vitis

These are prerequisites, not results we obtained on grape. This chapter does not cover using IBD segment lengths to infer historical Ne.

1. Merge clones first. Pairs from the same clone, under this repository’s rule (live main `docs/WORKFLOW.md` step 3, commit `eb29b98c…`; KING kinship greater than 0.354, the duplicate/MZ class in the opened KING manual; first-degree relatives are not dropped as clones), can show IBD over nearly the entire genome and will inflate relatedness and the IBD-segment length distribution (this last clause is this repository’s reasoning, not sourced here; [待确认]). Selfing is expected to inflate HBD (this repository’s reasoning, not sourced here; [待确认]) and should be stated as a separate assumption.
2. A *Vitis* genetic map in cM is required. hap-IBD’s README lists `map=` as a required PLINK-format genetic map with cM units, and the default `min-seed` / `min-output` thresholds are 2.0 cM (plus `min-markers=100`, `min-mac=2`). Those 2–4 cM figures in the hap-IBD abstract come from UK Biobank analyses under a human map. Without a grape map, a 2 cM cutoff has no grape meaning. Which grape map to use is [待确认]. Genotypes must be phased, with no missing alleles, as the README requires. Switch errors in small or structured cohorts can break long segments (this repository’s reasoning, not sourced here; [待确认]).
3. Converting segment length to time assumes sexual generations. Vegetative propagation is expected to distort that conversion (this repository’s reasoning, not sourced here; [待确认]).

## Claim–source table

| Claim | Source | Quoted sentence or figure/table | What was read |
|---|---|---|---|
| hap-IBD detects IBD in phased data with PBWT; compared with GERMLINE, iLASH, RaPID, TRUFFLE; UK Biobank timing and 2–4 cM claim | doi:10.1016/j.ajhg.2020.02.010 | Abstract sentences quoted above | Abstract (PMC XML has no article body) + README https://github.com/browning-lab/hap-ibd |
| RaPID2 is a parallel PBWT framework for IBD segments | doi:10.1093/bioadv/vbag078 | Paper title | Full text (PMC13049448) |
| RZooRoH 2026 update covers inbreeding, IBD and relatedness | doi:10.1111/1755-0998.70186 | Paper title | Full text (PMC13509087) |
| These callers have been benchmarked on a published Vitis cohort in the sources opened for these chapters | — | — | Not found; [待确认] |
