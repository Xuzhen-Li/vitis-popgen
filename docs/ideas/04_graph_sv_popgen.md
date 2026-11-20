# Graph-aware SV population genetics

Section 11 of the current README is a pointer to vitis-pangenome, listing PanGenie, vg (Giraffe + vg call), odgi, Sniffles2, cuteSV and Jasmine. This chapter adds the method papers and one grape pangenome variation map that were opened here. It does not replace vitis-pangenome.

## Genotyping known variants from a pangenome

Ebler et al. (2022, full text, doi:10.1038/s41588-022-01043-w) is the PanGenie paper, titled “Pangenome-based genome inference allows efficient and accurate genotyping across a wide spectrum of variant classes.” The GitHub README (https://github.com/eblerjana/pangenie) says it is “A short-read genotyper for various types of genetic variants … represented in a pangenome graph,” and that “Genotypes are computed based on read k-mer counts and a panel of known, fully assembled haplotypes.” Inputs are therefore short reads plus a haplotype-resolved assembly panel, not an unspecified “reads, pangenome.” The shorter “Pangenome-based genome inference” wording is the GitHub repository description, not that README sentence. That description was re-fetched on 2026-11-15 CST from the GitHub repository API (https://api.github.com/repos/eblerjana/pangenie, 2026-11-15 CST, 5,185 bytes, sha256 411a57ee8a50b3d6efb1c8ee252b250116b613574e5f3b69e77ab9e071d1a4f4) and is, verbatim, “Pangenome-based genome inference”. The catalogue’s note that PanGenie genotypes variants already in a pangenome graph matches this paper’s scope. Graph construction (minigraph-cactus, pggb), vg call, and SV-load workflows are outside these chapters and remain in vitis-pangenome.

Sirén et al. (2021, full text, doi:10.1126/science.abg8871) is titled “Pangenomics enables genotyping of known structural variants in 5202 diverse genomes.” This is the Giraffe mapper / vg-team paper used to genotype known SVs in thousands of genomes. The vg README (https://github.com/vgteam/vg) was also opened.

These two papers are human/pangenome-method studies. They justify using graph genotyping in a cohort; they are not Vitis results.

## A grape graph and SV map: Liu et al. 2024 and Guo et al. 2025

Liu et al. (2024, full text, doi:10.1038/s41588-024-01967-5) “constructs a graph-based pangenome reference (Grapepan v.1.0) from 18 newly generated phased telomere-to-telomere assemblies and 11 published assemblies. Using Grapepan v.1.0, we build a variation map with 9,105,787 short variations and 236,449 structural variations (SVs).” In the results they wrote: “On average, 88.6% of the SVs overlapped TEs, whereas 30.9% intersected gene structures (Supplementary Fig. 7c,d).” They also wrote: “The estimated heritability improves by 22.78% on average when including SVs.” Those two numbers are results of this study, not general laws.

Guo et al. (2025, abstract only, doi:10.1038/s41588-025-02111-7) “assembled and annotated haplotype-resolved genomes of 72 global Vitis accessions including 25 wild and 47 cultivated grapevines, among which genomes for 60 grapevines are newly released.” The abstract further says European cultivars “have a smaller repertoire of resistance genes in the NLR family” and that the authors “identified over 63 SVs and their relevant genes significantly associated with DM resistance.” That is a super-pangenome and resistance result, not a cohort SV frequency pipeline.

## Claim–source table

| Claim | Source | Quoted sentence or figure/table | What was read |
|---|---|---|---|
| PanGenie: short-read genotyping of variants already represented in a pangenome graph, using k-mer counts and a haplotype-resolved assembly panel | doi:10.1038/s41588-022-01043-w ; https://github.com/eblerjana/pangenie | Paper title; README sentences quoted above | Full text (PMC9005351) + README |
| Giraffe / pangenomics genotypes known SVs in 5,202 diverse genomes | doi:10.1126/science.abg8871 ; https://github.com/vgteam/vg | Paper title | Full text (PMC9365333) + README |
| Grapepan v.1.0 from 18 new T2T + 11 published assemblies; 9,105,787 short variants and 236,449 SVs | doi:10.1038/s41588-024-01967-5 | Abstract / opening results, as quoted above | Full text (PMC11631756) |
| On average, 88.6% of the SVs overlapped TEs, whereas 30.9% intersected gene structures | doi:10.1038/s41588-024-01967-5 | Results sentence; Supplementary Fig. 7c,d cited by the paper | Full text (PMC11631756) |
| Heritability improved by 22.78% on average when including SVs (this study) | doi:10.1038/s41588-024-01967-5 | Sentence quoted above | Full text |
| Guo et al.: 72 haplotype-resolved Vitis genomes (25 wild, 47 cultivated, 60 newly released); >63 SVs associated with downy mildew resistance | doi:10.1038/s41588-025-02111-7 | Abstract sentences quoted above | Abstract only |
