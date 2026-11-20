# Local ancestry and spatial structure

The catalogue already lists RFMix, fineSTRUCTURE/ChromoPainter, and FEEMS. This chapter records the papers actually opened for FLARE, MOSAIC, fineSTRUCTURE and FEEMS.

## Local ancestry

Browning, Waples and Browning (2023, abstract only; AJHG PMC XML has no article body, doi:10.1016/j.ajhg.2022.12.010) titled their paper “Fast, accurate local ancestry inference with FLARE.” The abstract describes local ancestry as “the source ancestry at each point in the genome of an admixed individual” under an “extended Li and Stephens model.” The GitHub README (https://github.com/browning-lab/flare) says “The flare program performs local ancestry inference.” Required parameters include phased genotypes with no missing alleles and a genetic map (`map=`). The README states: “A reference panel should contain individuals from the same source population. A reference panel should not normally contain admixed samples.” Default `gen` is 10 generations since admixture (`em=true` estimates it); default `min-mac` is 50. We quote these requirements rather than unreplicated accuracy numbers, because the full article body was not in the XML.

Those reference-panel assumptions are hard to meet in Vitis: Eurasian wild *sylvestris* and cultivated groups both carry introgression in the vinifera papers already opened (Magris et al. 2021 abstract: “followed by numerous and pervasive introgressions from European wild populations”; Xiao et al. 2023 abstract: “continuous gene flow between European wild grapes (EU) and cultivated grapes over the past ~2,000 y”; Freitas et al. 2021 abstract: “postdomestication hybridization with local wild genotypes”). The “~14% of the average Vitis genome” figure in chapter 6 is from a North American *Vitis* species paper (Wang et al. 2026, doi:10.1073/pnas.2607754123) and must not be read as a sylvestris–vinifera result. Admixture time in generations is also expected to be distorted by vegetative propagation (this repository’s reasoning, not sourced here; [待确认]). The README cites FLARE2 (Browning, Temple and Browning 2025, doi:10.1101/2025.10.13.681993; abstract opened 2026-11-15 CST, full text not downloaded) as a later approach for poorly matched reference panels; application to *Vitis* remains [待确认].

Salter-Townshend and Myers (2019, full text, doi:10.1534/genetics.119.302139) is titled “Fine-Scale Inference of Ancestry Segments Without Prior Knowledge of Admixing Groups.” This is the MOSAIC method: it infers ancestry segments without requiring the admixing groups to be specified in advance.

Lawson, Hellenthal, Myers and Falush (2012, full text, doi:10.1371/journal.pgen.1002453) is titled “Inference of population structure using dense haplotype data” (fineSTRUCTURE / ChromoPainter). It is already in the catalogue; the full text was re-opened for these chapters.

A method that does local ancestry **on a pangenome graph**, as opposed to a linear reference, was not among the papers opened here and remains [待确认] as a grape recipe. RFMix stays in the existing catalogue; we did not re-fetch its original paper in the sources opened for these chapters.

## Spatial structure: FEEMS (and EEMS as described there)

Marcus, Ha, Barber and Novembre (2021, full text, doi:10.7554/eLife.61927) described FEEMS. The abstract says:

> “Petkova et al., 2016 developed a statistical method called Estimating Effective Migration Surfaces (EEMS) for visualizing spatially heterogeneous isolation-by-distance on a geographic map. While EEMS is a powerful tool for depicting spatial population structure, it can suffer from slow runtimes. Here, we develop a related method called Fast Estimation of Effective Migration Surfaces (FEEMS).”

They apply FEEMS to North American gray wolves and report solutions “orders of magnitude faster” than EEMS. The FEEMS paper is our source for what EEMS is; the original EEMS article is Petkova, Novembre and Stephens 2016, Nat Genet 48:94–100, doi:10.1038/ng.3464 (title and abstract opened 2026-11-15 CST; not used to teach new numerical results). The README opened at https://github.com/Novembrelab/feems is the accompanying package. The FEEMS paper also states that “FEEMS is not a Bayesian method … FEEMS returns a particular point estimate: a local minimum point of the optimization landscape,” so it does not return posterior uncertainty, and that the penalty λ is “selected … using leave-one-out cross-validation.” Incorporating “knowledge of uncertainty in position” is described there as future work. Whether isolation-by-distance surfaces are appropriate for a crop that has been moved along trade routes, then clonally propagated, is [待确认]. Cultivar sampling coordinates are usually a collection site or vineyard, not a centre of origin, which is expected to break the isolation-by-distance premise (this repository’s reasoning, not sourced here; [待确认]); a cautious use would be restricted to wild samples with reliable provenance, after clone merging.

## Claim–source table

| Claim | Source | Quoted sentence or figure/table | What was read |
|---|---|---|---|
| FLARE is a method for fast, accurate local ancestry inference | doi:10.1016/j.ajhg.2022.12.010 ; https://github.com/browning-lab/flare | Paper title; README tagline | Abstract only (no XML body) + README |
| MOSAIC infers ancestry segments without prior knowledge of admixing groups | doi:10.1534/genetics.119.302139 | Paper title | Full text (PMC6614886) |
| fineSTRUCTURE / ChromoPainter: structure from dense haplotype data | doi:10.1371/journal.pgen.1002453 | Paper title | Full text (PMC3266881) |
| FEEMS is a faster relative of EEMS for effective migration surfaces; wolf application | doi:10.7554/eLife.61927 ; https://github.com/Novembrelab/feems | Abstract sentences quoted above | Full text (PMC8324296) + README |
| Original EEMS 2016 paper | doi:10.1038/ng.3464 (Petkova, Novembre and Stephens 2016, Nat Genet 48:94–100) | Title and abstract opened 2026-11-15 CST; not used to teach new numerical results | Abstract (EuropePMC); full text not downloaded |
| Local ancestry called on a Vitis pangenome graph | — | — | Not opened for these chapters; [待确认] |
