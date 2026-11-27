# ARG-based population genetics

The current vitis-popgen catalogue already lists tsinfer, tsdate, Relate, SINGER and tskit under demography (section 4), and an “ARG dating of grape domestication” idea in section 16. This chapter supplies the method papers and GitHub READMEs opened on 15 November 2026 (CST). No grape ARG was inferred in this addition.

## What an ARG / tree sequence is for

A 2024 review (Brandt et al., GBE, full text, doi:10.1093/gbe/evae005) is titled “The Promise of Inferring the Past Using the Ancestral Recombination Graph.” The abstract defines the ARG as “a structure that represents the history of coalescent and recombination events connecting a set of sequences,” and says “The full ARG can be represented as a set of genealogical trees at every locus in the genome, annotated with recombination events that change the topology of the trees between adjacent loci and the mutations that occurred along the branches of those trees.” Use that review for the general case. We do not copy unreplicated numerical benchmarks from it here.

The tskit README (https://github.com/tskit-dev/tskit, opened 2026-11-15 CST) says: “The succinct tree sequence (`tskit`) format is an efficient way of representing the genetic history - sometimes known as an Ancestral Recombination Graph or ARG - of a set of related DNA sequences.” The shorter “Population-scale Ancestral Recombination Graph (ARG) library” wording is the GitHub repository description, not that README sentence.

## Scalable inference: tsinfer and Relate

Kelleher et al. (2019, full text, doi:10.1038/s41588-019-0483-y), the tsinfer paper, wrote:

> “Here we introduce an algorithm that is able to not only infer whole-genome histories with comparable accuracy to the state-of-the-art but also process four orders of magnitude more sequences. … We apply the method to human data from the 1000 Genomes Project, Simons Genome Diversity Project and UK Biobank.”

The tsinfer README (https://github.com/tskit-dev/tsinfer) states: “Infer whole-genome tree sequences from genetic variation data.” It also says tsinfer “does not attempt to infer node times,” so dating needs a separate tool such as tsdate, and it warns that the GitHub main branch is a 1.0 development branch: “DO NOT USE THIS CODE for your research.” Improvements from 0.2.0 onward are recorded in Wohns et al. 2022.

Speidel et al. (2019, full text, doi:10.1038/s41588-019-0484-x) described Relate:

> “We have developed a method, Relate, scaling to >10,000 sequences while simultaneously estimating branch lengths, mutational ages and variable historical population sizes, as well as allowing for data errors.”

Applications in that paper are to 1000 Genomes Project haplotypes (26 human populations). That is not a grape analysis.

## Dating: tsdate, as used in Wohns et al. 2022

Wohns et al. (2022, full text, doi:10.1126/science.abi8264; EuropePMC author order Wohns AW, Wong Y, Jeffery B, Akbari A, Mallick S, Pinhasi R, Patterson N, Reich D, Kelleher J, McVean G) inferred “a unified genealogy of modern and ancient humans.” The tsdate GitHub README (https://github.com/tskit-dev/tsdate) says “``tsdate`` is a scalable method for estimating the age of ancestral nodes in a tree sequence.” It cites Wohns et al. 2022 for the original `inside_outside` and `maximization` algorithms, and says: “If using the `variational_gamma` algorithm (the default from version 0.2 onwards), please cite the [preprint](https://www.biorxiv.org/content/10.64898/2026.01.07.698223v1): Nathaniel S. Pope, Sam Tallman, Ben Jeffery, Duncan Robertson, Yan Wong, Savita Karthikeyan, Peter L. Ralph, and Jerome Kelleher (2026) Tracing the evolutionary histories of ultra-rare variants using variational dating of large ancestral recombination graphs. bioRxiv: 2026.01.07.698223; doi: https://doi.org/10.64898/2026.01.07.698223” (README opened 2026-11-15 CST, 3,093 bytes; abstract of the preprint opened 2026-11-15 CST; full text of the preprint not downloaded). Using the default algorithm while citing only Wohns 2022 would be the wrong paper. The Wohns abstract says the representation “uses ancient samples to constrain and date relationships.” The existing vitis-popgen note that tsdate can be paired with aDNA tip dates is consistent with that paper’s human ancient-sample design; it is not evidence that a grape ARG with aDNA tips has been built here.

## Posterior sampling: SINGER

Deng, Nielsen and Song (2025, full text, doi:10.1038/s41588-025-02317-9) introduced SINGER (sampling and inferring of genealogies with recombination). The abstract says it “accelerates ARG sampling from the posterior distribution by two orders of magnitude, enabling accurate inference and uncertainty quantification for hundreds of whole-genome sequences,” and that competing scalable methods “reconstruct only a single ARG topology and cannot quantify the considerable uncertainty associated with ARG inferences.” The application in the paper is to British and African individuals in the 1000 Genomes Project. The README (https://github.com/popgenmethods/SINGER) spells out the acronym and describes MCMC under the Sequentially Markovian Coalescent.

## Using these tools on Vitis (worked route, not a result)

A method-level route, matching the existing section 16 idea, is: start from a public Vitis panel that has been clone-pruned and polarised; infer a tree sequence with tsinfer (or use Relate / SINGER if the sample size and error model fit the paper you cite); date nodes with tsdate if you need ages, citing Pope et al. 2026 (doi:10.64898/2026.01.07.698223; abstract only, full text not downloaded) when the default `variational_gamma` algorithm is used; and state the generation-time and mutation-rate assumptions, which this repository still marks [待确认] for grape.

Additional required inputs, taken from the official documentation:

- Clone pruning follows this repository’s rule on the live Xuzhen-Li/vitis-popgen main branch (commit `eb29b98ccb3b6bb74370cd1752cf2b8232dd4460`, 2026-11-15 17:29 CST). `docs/WORKFLOW.md` step 3, `scripts/01b_clone_dedup.py`, and the README treat KING kinship above 0.354 as the same clone or duplicate, and do not drop first-degree relatives (0.177–0.354) as clones. The KING manual (https://www.kingrelatedness.com/manual.shtml, opened 2026-11-15 CST) says: “an estimated kinship coefficient range >0.354, [0.177, 0.354], [0.0884, 0.177] and [0.0442, 0.0884] corresponds to duplicate/MZ twin, 1st-degree, 2nd-degree, and 3rd-degree relationships respectively.” Manichaikul et al. 2010 (doi:10.1093/bioinformatics/btq559; abstract opened) is the paper for the method; the 0.354 cutoff is not in that abstract, and the paper body was not opened ([待确认]). A later change to the rule would also be [待确认].
- Relate’s getting-started page (https://myersgroup.github.io/relate/getting_started.html, opened 2026-11-15 CST) requires phased data (“The data needs to be phased”), the ancestral allele denoted by 0 (“the ancestral allele is denoted by 0 and the derived allele is denoted by 1”), a genetic map (`--map`), a mutation rate (`-m`), and a haploid effective size (`-N`, “population size of haplotypes”). The documented example (`-m 1.25e-8 -N 30000`) is a human example and must not be copied to grape.
- SINGER’s README currently supports “phased, high-quality genomes”; `-m` or `-mut_map` is required; `-polar` defaults to 0.5 (unpolarised) and 0.99 is suggested for polarised data. Branch lengths are in generations (the README’s human conversion uses a 28-year generation time). The documented `-m 1.25e-8` is likewise a human example.
- A grape genetic map, and grape values of μ and g, remain [待确认]. How to phase highly heterozygous, clonally propagated material is also [待确认].
- Treating a living clone as if it were sampled at its sexual-origin date is a model assumption, not a tool-documented sample-age field (those fields are for ancient DNA). Living clones may still carry somatic mutations accumulated since that origin (this repository’s reasoning, not sourced here; [待确认]). Sensitivity to that assumption should be stated; it is not a result.

Selfing is expected to inflate HBD, somatic mutations are expected to affect dated mutation counts, and wild–cultivated introgression is expected to affect how population labels are read on an ARG (this repository’s reasoning, not sourced here; [待确认]). None of the papers above analysed Vitis. Treating their human-scale accuracy claims as automatically true for a highly clonal, vegetatively propagated perennial would be an extrapolation and is [待确认].

## Claim–source table

| Claim | Source | Quoted sentence or figure/table | What was read |
|---|---|---|---|
| tsinfer infers whole-genome histories at much larger sample sizes than previous accurate methods; applied to 1000G, SGDP, UK Biobank | doi:10.1038/s41588-019-0483-y | Abstract sentences quoted above | Full text (PMC6726478) + README https://github.com/tskit-dev/tsinfer |
| Relate scales to >10,000 sequences and estimates branch lengths, mutational ages and historical Ne; applied to 26 human populations | doi:10.1038/s41588-019-0484-x | Abstract sentence quoted above | Full text (PMC7610517) |
| Wohns et al. 2022: unified genealogy of modern and ancient humans; ancient samples constrain and date relationships; this is the paper cited for tsdate | doi:10.1126/science.abi8264 ; https://github.com/tskit-dev/tsdate | Abstract; README citation line | Full text (PMC10027547) + README |
| SINGER samples ARGs from the posterior, with uncertainty, for hundreds of whole genomes; 1000G application | doi:10.1038/s41588-025-02317-9 ; https://github.com/popgenmethods/SINGER | Abstract sentences quoted above | Full text (PMC12425808) + README |
| 2024 review on the promise of ARGs for inferring the past | doi:10.1093/gbe/evae005 | Paper title | Full text (PMC10834162) |
| tskit represents genetic history / an ARG as a succinct tree sequence | https://github.com/tskit-dev/tskit | README sentence quoted above; the shorter tagline is the repo description | README |
| tsdate default from v0.2 is variational_gamma and should be cited as Pope et al. 2026 (doi:10.64898/2026.01.07.698223; abstract opened 2026-11-15 CST, full text not downloaded); Wohns 2022 is the citation for the earlier algorithms | https://github.com/tskit-dev/tsdate ; doi:10.1126/science.abi8264 | README citation paragraph quoted above | README + Wohns full text |
| ARG definition used here | doi:10.1093/gbe/evae005 | Abstract sentences quoted above | Full text (PMC10834162) |
| A published grape ARG with dated domestication nodes | — | — | Not found in the sources opened for these chapters; idea only; [待确认] |
