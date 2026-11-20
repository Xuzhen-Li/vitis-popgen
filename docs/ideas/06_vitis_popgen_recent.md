# Recent Vitis population-genomic studies

This chapter records Vitis resequencing and pangenome papers opened for these chapters. Several of them are already in the catalogue (Dong 2023, Magris 2021, Xiao 2023, Freitas 2021, Liang 2019, Zhou 2017, Liu 2024, Guo 2025). Two 2026 papers were not previously listed. The main point is not to pick a single domestication story, but to keep the published claims next to each other.

## How many domestication events?

Dong et al. (2023, abstract only, doi:10.1126/science.add8655) analysed “3,525 cultivated and wild accessions worldwide” and wrote:

> “Then, domestication occurred concurrently about 11,000 years ago in Western Asia and the Caucasus to yield table and wine grapevines. The Western Asia domesticates dispersed into Europe with early farmers, introgressed with ancient wild western ecotypes, and subsequently diversified along human migration trails into muscat and unique western wine grape ancestries by the late Neolithic.”

Magris et al. (2021, full text, doi:10.1038/s41467-021-27487-y) analysed 204 genomes of *Vitis vinifera* and wrote that “all analyses support a single domestication event that occurred in Western Asia and was followed by numerous and pervasive introgressions from European wild populations.”

Xiao et al. (2023, full text, doi:10.1073/pnas.2222041120) analysed “resequencing data from 345 samples.” The abstract argues for a single domestication and says gene flow into cultivated grapes over the past ~2,000 y was “especially from EU to wine grapes.” The wording “introgression from the wild relative to wine, but not to table, grapes” is from the Significance statement, not the abstract, and is qualified here: the abstract does not deny introgression into table grapes, and the full text also reports fd outlier windows in table grapes. Those introgressed regions, the Significance statement says, “are enriched for genes related to aromatic compound synthesis.” The opened Xiao full text does not use the phrase “Western Asia” (search count 0). A correction is recorded: doi:10.1073/pnas.2317674120 (PNAS 120(52): e2317674120, issue 2023-12-26), which updates 10.1073/pnas.2222041120. The correction full text (PMC10756202, NCBI efetch XML 11,216 bytes, 2026-11-15 CST) states that 17 of the 345 accessions (5%) were removed as misidentified, leaving a curated set of 328 accessions for Dsuite, fd, SMC++, Fastsimcoal, PBS, Shic and Filet; it also replaces Fig. 4 and corrects SI “table, n = 148” to “n = 154.” The abstract still reports 345 samples. Population-genetic analyses in that paper should be read as using the curated 328 accessions.

Freitas et al. (2021, full text, doi:10.1126/sciadv.abi8584) support “a central domestication event in grapevine … followed by postdomestication hybridization with local wild genotypes,” with “the strongest signal … associated with a subset of Iberian grapevine varieties showing large introgression tracts,” which they present as adaptive introgression.

These abstracts disagree on one versus two domestication events. This repository does not adjudicate that disagreement.

## Dates, load, and earlier panels

Zhou et al. (2017, full text, doi:10.1073/pnas.1709257114) “estimated that our wild and cultivated grape samples diverged ∼22,000 years ago and that the cultivated lineage experienced a steady decline in population size (Ne) thereafter.” That ∼22 kya figure is from MSMC cross-coalescence between sylvestris and wine or table grapes (Fig. 2B), converted with g = 3 y and μ = 2.5 × 10⁻⁹ mutations per nucleotide per year. The n = 4 runs in the same paper are the vinifera Ne analyses (Fig. 2A: “two separate runs of four individuals”). The sample set for the cross-coalescence is [待确认] (SI Appendix Table S1 was not opened). The same paper’s SMC++ analyses gave “an estimated divergence time (∼30 kya) that greatly predates domestication,” and an “∼2.6-kya divergence of wine and table grapes.” The Significance statement also writes of a “22,000-y population decline prior to domestication.” The authors note that “demographic calculations assume a mutation rate and a generation time that may be incorrect.” Their load result is quoted in docs/ideas/05_pgs_and_load.md.

These calendar dates, Dong’s “about 11,000 years ago,” and the Armenia 2026 “~18.5k years ago” sit on different models and, unless shown otherwise, different μ and g. They cannot be compared as if they were the same kind of number. μ and g for Dong (abstract only) and for the Armenia paper were not extracted here and are [待确认].

Liang et al. (2019, full text, doi:10.1038/s41467-019-09135-8) reported whole-genome variation of 472 *Vitis* accessions covering “48 out of 60 extant Vitis species” and “a recent dramatic expansion and contraction of effective population size in the domesticated grapevines,” with “cultivars from the pan-Black Sea region” having “a unique demographic history.”

## Pangenomes and 2026 panels

Liu 2024 and Guo 2025 are summarised, with quotes, in docs/ideas/04_graph_sv_popgen.md.

Wang et al. (2026, PNAS, full text, doi:10.1073/pnas.2607754123) “analyzed whole-genome resequencing data from 639 accessions representing 48 Vitis species,” performed population-genetic analyses for 19 species, and “uncovered widespread evidence of introgression, comprising ~14% of the average Vitis genome.” Introgression “was associated with the geographic distribution between species, and highly admixed individuals were more frequently found near ecological niche margins.”

Nikoghosyan et al. (2026, full text, doi:10.1186/s12870-026-08287-2) re-analysed whole-genome data of 164 Armenian cultivated and wild accessions from a previous worldwide collection. “Population structure analysis revealed a clear genetic separation between wild and cultivated groups and three distinct ancestral components within the cultivated gene pool, reflecting a west-to-east geographical gradient in Armenia.” The same abstract says “wild and cultivated lineages began to separate ~18.5k years ago, with divergence intensifying ~4k years ago under human cultivation.” Those dates are this study’s estimates, not a replacement for Dong or Zhou.

## Claim–source table

| Claim | Source | Quoted sentence or figure/table | What was read |
|---|---|---|---|
| 3,525 accessions; two concurrent domestications about 11,000 years ago in Western Asia and the Caucasus, “to yield table and wine grapevines.” The abstract does not say “respectively,” and the next sentence has the Western Asia branch later contributing to western wine-grape ancestry, so this is not a one-to-one table/wine map. μ and g [待确认] | doi:10.1126/science.add8655 | Abstract sentences quoted above | Abstract only |
| 204 V. vinifera genomes: one Western Asian domestication, then pervasive introgression from European wild populations | doi:10.1038/s41467-021-27487-y | Abstract sentence quoted above | Full text (PMC8692429) |
| 345 samples in the abstract; correction e2317674120 removes 17 misidentified accessions, leaving 328 for the population-genetic analyses, and replaces Fig. 4 / SI table n; single domestication; introgression especially from EU into wine grapes (abstract). “Not to table” is Significance-only and is qualified here. The paper does not claim a Western Asian location in the opened text | doi:10.1073/pnas.2222041120 ; doi:10.1073/pnas.2317674120 | Abstract and Significance wording distinguished above; correction facts from PMC10756202, opened 2026-11-15 CST (NCBI efetch XML 11,216 bytes, 2026-11-15 CST) | Full text (PMC10268302); correction full text (PMC10756202), opened 2026-11-15 CST |
| Central domestication then hybridization with local wild genotypes; strongest signal in some Iberian wine varieties; adaptive introgression | doi:10.1126/sciadv.abi8584 | Abstract sentences quoted above | Full text (PMC8604406) |
| Zhou et al.: wild vs cultivated divergence ∼22 kya is MSMC cross-coalescence between sylvestris and wine or table grapes (Fig. 2B), converted with g = 3 y, μ = 2.5×10⁻⁹ /bp/yr; the n = 4 runs are the vinifera Ne analyses (Fig. 2A); cross-coalescence sample set [待确认] (SI Table S1 not opened); SMC++ in the same paper gave ∼30 kya; wine vs table ∼2.6 kya; dates are not directly comparable across studies | doi:10.1073/pnas.1709257114 | Abstract, Results, Fig. 2 caption and Significance sentences quoted above | Full text (PMC5676911) |
| Liang et al.: 472 accessions, 48 of 60 extant Vitis species; recent Ne expansion and contraction in domesticated grapevines | doi:10.1038/s41467-019-09135-8 | Abstract sentences quoted above | Full text (PMC6416300) |
| 639 accessions, 48 Vitis species; introgression ~14% of the average Vitis genome; more admixture near niche margins | doi:10.1073/pnas.2607754123 | Abstract sentences quoted above | Full text (PMC13462565) |
| 164 Armenian accessions; wild vs cultivated separation; three cultivated components on a west–east gradient; split ~18.5k years ago, intensifying ~4k years ago. μ and g used for those dates [待确认] | doi:10.1186/s12870-026-08287-2 | Abstract sentences quoted above | Full text (PMC12998295) |
| Liu 2024 and Guo 2025 pangenome / SV claims | see 04_graph_sv_popgen.md | — | Full text / abstract as in ch. 4 |
