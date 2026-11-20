# Polygenic scores and mutation load

The current catalogue has genomic-prediction and DFE tools (rrBLUP, GCTA, Grapes). This chapter records papers opened for these chapters on polygenic-score portability and on mutation load, including one grape paper already in the catalogue. We did not find a published grape polygenic-score transfer study in the sources opened for these chapters.

## Polygenic score portability (human papers; method cautions only)

Martin et al. (2019, full text, doi:10.1038/s41588-019-0379-x) is titled “Clinical use of current polygenic risk scores may exacerbate health disparities.” The abstract says current PRS “are several times more accurate in individuals of European ancestry than other ancestries” and that “this disparity is an inescapable consequence of Eurocentric biases in genome-wide association studies.”

Wang et al. (2026, full text, doi:10.1038/s41467-026-68565-3) is titled “Three open questions in polygenic score portability.” The abstract measures “PGS prediction accuracy as a continuous function of individuals’ genome-wide genetic dissimilarity to the GWAS sample (genetic distance)” and reports three gaps: individual-level accuracy is only weakly predicted by genetic distance (and comparably by socioeconomic measures); trends vary by trait; and even qualitative trends can depend on the performance metric.

Both papers are about human clinical or human trait scores. They are included as cautions if someone transfers a score across grape gene pools. They are not evidence that a grape PGS has been built or transferred here. A grape-specific PGS-transfer result is [待确认].

Two further statistical cautions from the 2026 paper (full text, PMC12835231) are kept as method warnings, not as grape results: “R 2 can be arbitrarily low even when the model fitted to the data is correct. It also cannot be compared across transformations of the data.” And “Lower heterozygosity in PGS markers impacts the genetic variance a polygenic score can capture.” A grape-specific training/validation split should be by cultivar or clone, not by plant or ramet, otherwise accuracy can leak and be overestimated; that split rule is statistical reasoning and is [待确认] (no grape PGS paper was opened for it).

## Mutation load in grape, and two non-grape plant papers

Zhou, Massonnet, Sanjak, Cantu and Gaut (2017, full text, doi:10.1073/pnas.1709257114), already listed in the catalogue, wrote in the abstract:

> “The domestication of perennial crops differs from that of annuals in several ways, including the intensity of bottlenecks, and it is not yet clear if they accumulate deleterious variants. We found that grape accessions contained 5.2% more deleterious variants than wild individuals, and these were more often in a heterozygous state. Using forward simulations, we confirm that clonal propagation leads to the accumulation of recessive deleterious mutations but without decreasing fitness.”

The same paper’s Results (“Plant Samples and Population Structure”) compared nine putatively wild *sylvestris* individuals with 18 *vinifera* individuals representing 14 cultivars, plus one *Vitis rotundifolia* outgroup. Derived deleterious variants were those predicted by a SIFT score of ≤0.05, with the outgroup allele submitted to prediction programs “to avoid reference bias,” and were counted per individual as “2 × the number of homozygous variants + heterozygous.” The result sentence is: “The number of derived deleterious variants was 5.2% higher, on average, for vinifera individuals than for sylvestris individuals (Fig. 4).” That 5.2% is an average per individual. The 18 cultivated individuals represent only 14 cultivars. Treating those individuals as independent, and calling them pseudo-replicates with effective n ≤ 14, is this repository’s reasoning, not a sentence in Zhou et al. ([待确认]). In the opened full text (PMC5676911), the P values in that section are for the homozygous/heterozygous distribution, the heterozygous proportion, and the deleterious-to-synonymous ratio. No test name or P value was found for the 5.2% contrast itself (Wilcoxon / Mann / permutation / bootstrap / Student were not hit in the XML). Do not present 5.2% as a tested significant difference. Do not generalise the figure beyond this comparison.

Xiao et al. (2023, full text, doi:10.1073/pnas.2222041120), already in the catalogue, provide a second grape load observation. The abstract says “the introgressed fragments introduced a higher deleterious burden, with most deleterious SNPs and structural variants hidden in a heterozygous state.”

Jiang et al. (2025, full text, doi:10.1038/s41467-025-58021-z; first author Jiang J, not Zhang; EuropePMC authors: Jiang J, Chen JF, Li XT, Wang L, Mao JF, Wang BS, Guo YL) analysed 1,115 globally distributed *Arabidopsis thaliana* accessions and “find that effective population size (Ne) is the major contributor of genetic load variation … and can explain 74–94% genetic load variation in natural populations.” That 74–94% is a correlational (explained-variance) figure in Arabidopsis, not grape. Jiang et al. used SMC++ for population histories; for allele-age estimation they cite Ne ≈ 300,000 and μ ≈ 7e-9 per site per generation from previous studies. The generation time used for calendar dates was not found in the opened full text ([待确认]).

Lin et al. (2025, *Plant Journal*, abstract only, doi:10.1111/tpj.70425) is a population-genomic study of the endangered relict tree *Ulmus elongata*, including demographic history, genetic load and local adaptation. It is not a grape paper.

Bertorelle et al. 2022 (Nat Rev Genet 23:492–503, doi:10.1038/s41576-022-00448-x; title and abstract opened 2026-11-15 CST) is a review of genetic-load estimates in animals. It is not a grape paper and is not used here to teach a grape load number. Full text was not downloaded.

## Claim–source table

| Claim | Source | Quoted sentence or figure/table | What was read |
|---|---|---|---|
| Current human PRS are several times more accurate in European-ancestry individuals; disparity follows Eurocentric GWAS | doi:10.1038/s41588-019-0379-x | Abstract sentences quoted above | Full text (PMC6563838, via NCBI efetch, 100,953 bytes, matching SOURCES_READ) |
| Three open questions in PGS portability; accuracy as a function of genetic distance; human traits | doi:10.1038/s41467-026-68565-3 | Abstract and title quoted above | Full text (PMC12835231) |
| A published grape PGS-transfer study | — | — | Not opened for these chapters; [待确认] |
| Cultivated grapes had 5.2% more derived deleterious variants than wild, on average per individual (9 wild vs 18 cultivated individuals / 14 cultivars; SIFT ≤ 0.05; polarised with V. rotundifolia). The 5.2% contrast itself has no test name or P value in the opened text | doi:10.1073/pnas.1709257114 | Results sentences and Fig. 4 quoted or cited above; abstract also has the 5.2% figure | Full text (PMC5676911) |
| Xiao 2023: introgressed fragments introduced a higher deleterious burden, mostly heterozygous | doi:10.1073/pnas.2222041120 | Abstract sentence quoted above | Full text (PMC10268302) |
| In Arabidopsis, Ne is a major correlational contributor (74–94% of genetic-load variation) among 1,115 accessions; first author Jiang J, not Zhang | doi:10.1038/s41467-025-58021-z | Abstract sentences quoted above | Full text (PMC11926394) |
| Ulmus elongata study includes load, demography and local adaptation | doi:10.1111/tpj.70425 | Title and abstract opening | Abstract only; not grape |
