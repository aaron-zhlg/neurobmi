# Shortcut audits and twin tests remain unclaimed

Of the five candidate ideas, two are clearly open and three are only partly open. **Nobody has tested whether a BMI CNN reads extracranial tissue**: no published study compares whole-head, brain-masked, extracranial-only and grey-matter-map inputs for BMI. **Nobody has tested an ML brain-BMI score within MZ twin pairs**, or split its validity into within-family and between-family parts. Each has close neighbours, but no direct precedent. The other three ideas have been partly claimed, which narrows the novelty that is left:

- **Multimodal fusion:** done in small adult samples and in ABCD children, but never in HCP-YA with a formal test of whether added modalities help.
- **Surface-based models:** vertex-wise BMI prediction exists as a linear mixed model, and a 2D-projection CNN exists; no native surface deep model has been used.
- **Foundation models:** one 2026 benchmark probed frozen foundation-model features for BMI and found they barely beat FreeSurfer.

The bar in HCP-YA is Cooper et al. 2025. Their 3D-CNN reached **cross-validated R² 0.325 and lockbox R² 0.442**, against R² below 0.07 for atlas-ROI models on the same subjects. Their input was not the raw head but **modulated, 10 mm-smoothed SPM12 grey-matter maps**. Cooper never ran an extracranial control, a head-size control or a twin analysis, and never explained why voxels beat ROIs six- to fourteen-fold. Our FreeSurfer-ROI models (R² ≈ 0.08 family-grouped CV, ≈ 0.07 locked holdout) already match or exceed every published ROI baseline in this cohort. So the gap to Cooper is about representation, not about tuning. The strongest paper fuses ideas 1 and 5. It decomposes what a voxel-level BMI CNN actually learns, using input ablations, and then uses HCP's MZ twins to tell signal that reads body fat apart from signal that reflects shared genetic predisposition.

## Cooper 2025 sets the bar with grey-matter maps, not whole heads

The full bioRxiv text pins down Cooper's pipeline exactly ([bioRxiv full text](https://www.biorxiv.org/content/10.1101/2025.04.11.648433v1.full)).

- **Sample:** **1,106 HCP S1200 subjects** with structural MRI and BMI. BMI came from **self-reported height and weight**, which resolves a question the earlier literature review left open.
- **Input:** SPM12 VBM segmentation, using grey matter only, "warped, modulated, and smoothed" at 10 mm FWHM. Maps were in MNI-152 space at 1.5 mm (121×145×121).
- **Model:** a five-layer AlexNet-style 3D-CNN adapted from Abrol et al. 2021. Age, sex and ICV were not entered.
- **Splits:** a roughly 80/20 train/lockbox split "conducted on the Family ID variable". Within training they ran 5-fold CV repeated three times, with nested random-search tuning. The best of the 15 fold models was applied once to the lockbox.
- **Comparators:** random forest on atlas features plus covariates reached **CV R² 0.063 and lockbox R² 0.031**. Covariates alone reached R² 0.021 (RF) and 0.011 (elastic net), and TabNet fell to −0.035 when ROIs were added.
- **Feature transfer:** CNN-extracted features fed into RF or elastic net reached lockbox R² of **0.485 and 0.456**.

The paper was published as "Deep learning using structural MRI dramatically improves cross-validated prediction accuracy of body mass index" in *Brain Mechanisms* 151:202524 ([McMaster record](https://experts.mcmaster.ca/display/publication3800984)). The published full text was paywalled, so revised numbers cannot be ruled out.

Four features of this result matter for anyone trying to beat or explain it:

1. **The abstract is internally inconsistent.** It calls 0.325 the lockbox R², while the Results assign 0.325 to the CV mean and 0.442 to the lockbox ([bioRxiv](https://www.biorxiv.org/content/10.1101/2025.04.11.648433v1.full)). The defensible headline is the CV figure. The lockbox holds only about 220 subjects, so a single R² from it carries a standard error of roughly ±0.1 (my estimate). A lockbox score that beats the CV mean by 0.12 is more consistent with split luck than with real superiority.
2. **Family grouping is confirmed only for the outer split.** The text does not say whether the inner CV folds were family-grouped. Exact train and lockbox Ns, MAE and model-level r are not reported.
3. **Modulation keeps a body-size channel open.** Modulated GM maps encode local and total grey-matter volume, which scales with head size and sex, and the CNN received no ICV adjustment. In UK Biobank, life-course Mendelian randomization ties many adult obesity–brain associations to childhood adiposity and the larger head size that persists from it ([Chiesa 2024, UK Biobank](https://www.ukbiobank.ac.uk/publications/childhood-adiposity-underlies-numerous-adult-brain-traits-commonly-attributed-to-midlife-obesity/)). A CNN on modulated maps can exploit that route without anything one would call neuroanatomy.
4. **The explanation is coarse.** Regression Grad-CAM from the last conv layer, thresholded at z > 2 and labelled with AAL, highlighted occipital, fusiform, precuneus, cerebellar, hippocampal and basal-ganglia regions ([bioRxiv](https://www.biorxiv.org/content/10.1101/2025.04.11.648433v1.full)). At that resolution, signal from tissue boundaries or meninges cannot be told apart from cortical signal.

Code is public at [PBCAR/3DCNN_BMI](https://github.com/PBCAR/3DCNN_BMI), so an exact replication is feasible.

| HCP-YA BMI result | Input / model | Validation | Reported accuracy |
|---|---|---|---|
| Cooper 2025 | Modulated GM maps, 3D-CNN | Family-grouped lockbox; nested CV | CV R² 0.325; lockbox R² 0.442 |
| Cooper 2025 | Atlas ROIs + covariates, RF | Same splits | CV R² 0.063; lockbox 0.031 |
| Xu 2023 | Regional CT/SA/volume, elastic net | Held-out test; family grouping not reported | Brain-only R² 0.0635 |
| Couvy-Duchesne 2020 | ~650k vertex-wise values, BLUP | Trained on UKB, tested in HCP | r = 0.21 (R² ≈ 0.042) |
| Bachmann 2025 | Cerebellocerebral FC, CPM | 128-fold CV, siblings removed; no holdout; FD not regressed | rest r = 0.44; task-general r = 0.70 |
| Park 2020 | UKB-trained rs-FC pattern | External | r = 0.146 |
| neurobmi (ours) | FreeSurfer ROIs | Family-grouped CV; locked holdout | R² ≈ 0.08 / ≈ 0.07 |

Sources: [Cooper 2025](https://www.biorxiv.org/content/10.1101/2025.04.11.648433v1.full), [Xu 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC12614112/), [Couvy-Duchesne 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7469763/), [Bachmann 2025](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11899596/), [Park 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7643372).

Read this way, the realistic state of the art for structural HCP-YA prediction is a **family-grouped CV R² of about 0.3 from voxel-level grey-matter CNNs**. The ceiling for ROI and vertex-wise linear models is **about 0.03–0.08**. Our ROI result sits at the top of that range. Bachmann's FC figures are not a comparable bar: there is no locked holdout, no motion regression, and BMI–motion coupling in HCP is documented ([Park 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8203627)).

## No one has asked whether BMI CNNs read the scalp (idea 1: open)

The search found **no study that predicts BMI from extracranial tissue on head MRI**, and none that compares skull-stripped with whole-head inputs for a BMI CNN. The closest work comes from three directions, and none of them settles the question.

The two large BMI CNNs both used skull-stripped, registered inputs and never discussed non-brain signal:

- **Vakli et al. 2020.** UK Biobank, N = 17,938, FSL-processed skull-stripped T1s at 2 mm. Test R² 0.46, r = 0.70, MAE 2.41. Saliency fell on left caudate, left amygdala and right lateral temporal cortex ([Frontiers full text](https://www.frontiersin.org/journals/neuroinformatics/articles/10.3389/fninf.2020.00010/full)).
- **Finkelstein et al. 2024.** An ensemble of ten randomly initialised CNNs reached MAE 2.06 and r = 0.80 in UK Biobank, falling to r ≈ 0.46–0.50 in the external DIRECT-PLUS trial ([PMC10878010](https://pmc.ncbi.nlm.nih.gov/articles/PMC10878010/)).

Vakli's right lateral temporal hotspot sits next to the temporalis muscle and temporal fat pad. With coarse Grad-CAM at 2 mm, leakage across the mask edge there is a concrete, testable hypothesis rather than idle speculation.

Head soft tissue carries strong adiposity signal. DXA head-region fat percentage correlates with BMI at **r = 0.43 in NHANES youths** ([Gorniak 2024, PMC10940915](https://pmc.ncbi.nlm.nih.gov/articles/PMC10940915/)) and about **r = 0.67 in adults** ([Gorniak 2022](https://www.sciencedirect.com/science/article/abs/pii/S016794572200077X)). Facial soft-tissue thickness on MRI rises with BMI at every landmark ([NTU Taiwan study](https://scholars.lib.ntu.edu.tw/handle/123456789/160965)). Subcutaneous fat is bright on T1w. A whole-head CNN could therefore plausibly match Vakli's r ≈ 0.7 from scalp alone. That possibility alone justifies the experiment.

Analogous shortcuts are proven in neighbouring tasks. In ADNI Alzheimer's classification, **binarised skull-stripped masks alone reached 78–82% accuracy**, against 81.6% for full skull-stripped images. The models were learning mask contour and volume rather than tissue texture, and some unstripped models put relevance on the skull ([Tinauer 2025, arXiv](https://arxiv.org/html/2501.15831); [Insights into Imaging](https://link.springer.com/article/10.1186/s13244-025-02158-4)). For brain age, raw unstripped T2 beat skull-stripped input (MAE 3.05 vs 3.65 years). The authors' claim that the models "ignore" extracranial tissue rests on qualitative maps ([Wood 2022](https://www.sciencedirect.com/science/article/pii/S1053811922000015)). In ABCD sex classification, head size accounted for much of the apparent signal ([Adeli 2020, PMC7780846](https://pmc.ncbi.nlm.nih.gov/articles/PMC7780846)).

The gap is therefore specific. A study would need to train the same architecture on the same family-grouped HCP-YA splits with the following inputs:

- the whole head;
- the brain-masked T1w;
- an extracranial-only image (brain zeroed);
- modulated and unmodulated GM maps;
- binarised brain masks, testing the Tinauer contour shortcut.

It would then report the fraction of saliency mass outside the brain mask. Such a study would be the first of its kind for BMI. It would not duplicate Cooper, who never tested raw input. It would directly ask whether Cooper's ROI-to-voxel gap is neuroanatomy or a body-size and boundary readout. Either answer is publishable. Before committing, check what the released HCP-YA T1w volumes still contain. The notes did not establish whether the unprocessed images are defaced, which would remove facial fat but probably leave scalp and temporal fat.

## Twin co-twin tests exist for VBM, not for ML predictions (idea 5: open)

The twin literature is richer than the twin-specific search alone suggested, and HCP-YA has already been used for co-twin designs.

| Study | Sample | Design | Finding |
|---|---|---|---|
| Weise, Bachmann & Pleger 2019 | HCP-YA: 68 BMI-discordant MZ pairs (ΔBMI > 2.5); 153 MZ pairs for regression | Paired VBM with TFCE; within-pair regression | The heavier co-twin had less grey matter in prefrontal, striatal/accumbens, occipital and cerebellar cortex; larger ΔBMI predicted less GMV |
| Sadler 2018 | 47 BMI-discordant twin pairs (ΔBMI 6.7) | Between-network FC | Discordant twins differed in striatal/thalamic–PFC and cerebellar–insular FC (pFWE = 0.04); no difference in BMI-similar twins |
| Vainik 2018 | HCP S900, 895 siblings incl. 111 MZ pairs | BMI correlates aggregated into composite scores, then bivariate twin models | Composites had genetic correlation 0.25–0.45 with BMI; 77–89% of the phenotypic correlation was genetic |
| Small dedicated discordant-MZ cohorts (NTR 16 pairs; CROSSYS 12 pairs; WSTR) | Adults | Food-cue fMRI, rs-fMRI, PET, hypothalamic T2 | Food-cue effects largely vanished within pairs; putamen connectivity, brain glucose uptake and gliosis-related differences persisted |

Sources: [Weise 2019](https://pubmed.ncbi.nlm.nih.gov/31299367/); [Sadler 2018](https://pubmed.ncbi.nlm.nih.gov/29966718/); [Vainik 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6140494); NTR [rs-fMRI](https://pmc.ncbi.nlm.nih.gov/articles/PMC6867098) and [food-cue](https://link.springer.com/content/pdf/10.1007/s11682-017-9711-1.pdf); [CROSSYS](https://pmc.ncbi.nlm.nih.gov/articles/PMC12587225); [WSTR](https://pmc.ncbi.nlm.nih.gov/articles/PMC8440478).

None of these used a cross-validated ML predictor. Weise 2019 is mass-univariate VBM. Vainik built correlational composites inside variance-decomposition models. ML brain-BMI papers use family structure only to block leakage: Cooper grouped its split by Family ID and reported nothing per pair ([bioRxiv](https://www.biorxiv.org/content/10.1101/2025.04.11.648433v1.full)).

The within- versus between-family decomposition is routine for polygenic scores. There, most predictive power typically survives within families, with notable attenuation for educational attainment ([Selzam 2019, PMC6698881](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6698881/)). The search found **no imaging analogue for BMI**. The closest imaging-ML-in-twins work is brain-age heritability ([Brouwer 2021](https://escholarship.org/content/qt9p75z8vm/qt9p75z8vm.pdf?t=piy9h2); [Gillespie 2022](https://www.frontiersin.org/articles/10.3389/fnagi.2022.831002)), not co-twin control.

The idea has three parts:

- Train on other families.
- Test whether within-MZ-pair differences in predicted BMI track within-pair differences in measured BMI.
- Compare the within-family slope with the between-family slope, as in PGS validation.

This is open. Weise's positive VBM result makes a non-zero within-pair signal plausible, so the test is not foredoomed. Vainik's 77–89% genetic share predicts strong attenuation.

Power is the main risk, and it decides how the analysis must be built. HCP-YA has **149 genotype-confirmed MZ pairs** ([HCP dbGaP announcement](https://humanconnectome.org/study/hcp-young-adult/article/hcp-releases-snp-genotypes-collected-hcp-young-adult-subjects-dbgap)), and published analysis subsets hold 86–153. Zygosity must come from the genotype field, because some self-reported DZ pairs are genetically MZ ([HCP-Users archive](https://mail-archive.com/hcp-users@humanconnectome.org/msg04199.html)). With about 140 pairs, a within-pair correlation needs to reach roughly **r ≈ 0.24 for 80% power** (my calculation, two-sided α = 0.05). Restricted within-pair BMI variance and self-reported BMI both push the true value down. The analysis should therefore use continuous within-pair differences rather than a discordance cut-off. It should pool DZ and non-twin sibling pairs in a mixed within/between-family model. Predictions must come strictly from models trained without the pair's family.

## Fusion, surfaces and foundation models are crowded or weak (ideas 2–4: partly open)

**Multimodal fusion (idea 2)** has been attempted, but never rigorously in HCP-YA. Three precedents exist:

- **Park 2015** concatenated six DTI and ten rs-fMRI connections into PLS regression, with 15% percent error. Its features were selected from group differences, which is likely leaky ([PLoS ONE](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0141376)).
- **Adise 2021**, in ABCD children, modelled each modality separately. Structure plus DTI reached test R² 0.27, rs-FC 0.14 and working-memory activation 0.16, and only structure predicted later weight gain ([DCN](https://www.sciencedirect.com/science/article/pii/S1878929321000396)).
- **Bhatt 2023** fused sMRI, rs-fMRI and DTI to classify sex-specific obesity in 183 adults ([ResearchGate](https://www.researchgate.net/publication/356175686_Integrated_Multimodal_Brain_Signatures_Predict_Sex-Specific_Obesity_Status)).

In HCP, Park 2021 tested T1w/T2w myelin only univariately (r = −0.35) ([Comm Biol](https://www.nature.com/articles/s42003-021-02268-x)). The general HCP benchmark on behaviour found that fusion helped cognition but not other domains ([Ooi 2022](https://www.biorxiv.org/content/10.1101/2022.03.08.483564.full.pdf)).

What remains open is a family-grouped, locked-holdout HCP-YA study that stacks T1 morphometry, myelin, rest and task FC and DTI. It would need a paired test of fusion against the best single modality, with framewise displacement treated as a first-class confound. That is new, but incremental. FC adds a motion confound that could swallow the paper. A probable null result (structure dominates) is informative but not headline-grade.

**Surface deep learning (idea 3)** is open only in its narrowest form. Vertex-wise BMI prediction exists:

- **Couvy-Duchesne 2020** applied BLUP to about 650k vertex measures. It reached r = 0.45 within UK Biobank and **r = 0.21 when transferred to HCP**. Vertex-wise features always beat ROIs ([PMC7469763](https://pmc.ncbi.nlm.nih.gov/articles/PMC7469763/)).
- **Zeng 2020** projected cortical shape maps to 2D and classified overweight status with ImageNet CNNs at 65.6% accuracy ([ADS](https://ui.adsabs.harvard.edu/abs/2020SPIE11583E..09Z/abstract)).

No native surface model has targeted BMI or any body-size phenotype: not SiT, MS-SiT, the spherical CNNs, the GNNs or SPHARM-Net ([SiT, arXiv 2204.03408](https://arxiv.org/abs/2204.03408); [SPHARM-Net, PMC11565793](https://pmc.ncbi.nlm.nih.gov/articles/PMC11565793/)). The HCP-YA surface benchmark target is fluid intelligence, at r ≈ 0.35–0.39 ([sMAE, arXiv 2308.05474](https://arxiv.org/abs/2308.05474v2)).

The decisive warning comes from **Delzant 2025**. Body-size morphometricity was **43–52% for volume pipelines but only 15–34% for surface pipelines**, and volume-based representations generally predicted better ([PMC12572822](https://pmc.ncbi.nlm.nih.gov/articles/PMC12572822/)). A surface model will very likely land below Cooper. Its value lies in the contrast: surface models see cortical geometry and myelin but not head size or tissue outside the cortex. That makes the surface arm a useful control in a shortcut study rather than a standalone paper.

**Foundation models (idea 4)** are the least open of the five. **BrainFMBench** (bioRxiv 2026, accepted to MedAGI 2026) has already probed AnatCL, BrainIAC, 3D-Neuro-SimCLR and SwinBrain for BMI at HCP-YA-scale N, using NKI (N = 958) and HBN (N = 997). On NKI, frozen features gave BMI MAE of 3.52–4.16 against 3.99 for FreeSurfer. BrainIAC was worse than FreeSurfer, and an "un-CNN" baseline beat every pretrained model at 3.13 ([GitHub](https://github.com/epics-lab/BrainFMBench); [bioRxiv](https://www.biorxiv.org/content/10.64898/2026.05.15.725427v4.full)). The leaderboard has shifted between versions, and no R² or naive baseline is reported, so it is not a precise bar.

The literature on deep versus linear models at N ≈ 1,000 also finds little advantage for deep models ([Schulz 2020](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7447816/); [Abrol 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7806588)). Transfer helps most when the pretraining label matches the target ([Holderrieth 2022](https://www.medrxiv.org/content/10.1101/2022.12.11.22283324)). Brain-age gaps relate only weakly to BMI (r = 0.048 in older adults) ([PMC9894084](https://pmc.ncbi.nlm.nih.gov/articles/PMC9894084/table/T2)). Two things remain unpublished:

- **end-to-end fine-tuning** of a foundation model on HCP-YA BMI;
- **label-matched transfer**: pretrain a BMI CNN on UK Biobank, then fine-tune on HCP-YA.

The second is the most promising route to beating Cooper's R² outright. Domain shift is the catch: Finkelstein's external accuracy fell from r = 0.80 to about 0.5 ([PMC10878010](https://pmc.ncbi.nlm.nih.gov/articles/PMC10878010/)).

| Idea | Closest prior work | Their result | Verdict |
|---|---|---|---|
| 1. Extracranial shortcut | Tinauer 2025 (AD); Wood 2022 (brain age); Vakli 2020 and Cooper 2025 (BMI, no control) | Mask-only AD models reach 78–82% accuracy; no BMI test | **Open** |
| 2. Multimodal fusion | Adise 2021 (children); Park 2015; Bhatt 2023 (n = 183) | sMRI+DTI test R² 0.27; no fusion test | Partly open (HCP-YA, formal fusion test) |
| 3. Surface DL | Couvy-Duchesne 2020 BLUP; Zeng 2020 OMTNet | HCP r = 0.21; 65.6% accuracy | Partly open (native surface DL only) |
| 4. Foundation models | BrainFMBench 2026 | Frozen features ≈ FreeSurfer; un-CNN best | Mostly claimed; fine-tuning and BMI-label transfer open |
| 5. Twin validation of ML scores | Weise 2019 VBM co-twin; Vainik 2018 | Within-MZ GMV differences; 77–89% genetic | **Open** for ML predictions |

## Ablations plus co-twin validation make the strongest paper

Ideas 1 and 5 share one question: *what does a high-scoring brain-BMI model actually measure?* Combining them makes the twin test sharper than either study alone. An extracranial or head-size channel reads current adiposity directly. Subcutaneous fat differs between MZ co-twins exactly as much as their BMI does, so an extracranial-only model should keep most of its accuracy within pairs. A brain-tissue model whose signal is mostly genetic predisposition, as Vainik's 77–89% genetic share implies, should attenuate sharply within MZ pairs. A brain model whose signal reflects BMI-driven tissue change should survive in between, as Weise's within-pair VBM result hints.

Running the input-ablation ladder through the within-pair test therefore yields a **two-dimensional decomposition**:

- **Where** the signal lives: brain versus non-brain, contour versus texture, modulated versus unmodulated.
- **What** it reflects: shared family factors versus individual adiposity.

No prior paper can produce that.

A concrete design has four parts:

1. **Replicate Cooper exactly** from its public code under fully nested, family-grouped CV with a locked holdout. Report CV R² as the headline, with bootstrap intervals on the holdout.
2. **Train the input ladder** on identical folds: whole head, brain-masked, extracranial-only, modulated and unmodulated GM, binarised mask. Use our FreeSurfer-ROI ridge (R² ≈ 0.08/0.07) as the anatomical floor, and optionally add a surface model as a head-size-blind arm.
3. **Add controls:** BMI residualised on ICV and sex, and saliency mass outside the brain.
4. **Score every out-of-family prediction** within MZ pairs, DZ pairs and siblings, reporting within- and between-family slopes.

A UK Biobank-pretrained BMI CNN fine-tuned on HCP-YA is the best optional arm if beating Cooper outright matters. Fusion is best left to a follow-up.

The realistic expectations are as follows. An honest grey-matter CNN under stricter nesting should land at **CV R² of about 0.2–0.33**. A lockbox figure like 0.442 is unlikely to reproduce. If whole-head input beats brain-masked input, or extracranial-only input approaches it, the paper reframes the field's best numbers. If brain-masked and unmodulated inputs hold near 0.3 while the extracranial-only model falls short, Cooper's result gains the validation it currently lacks. In both cases the within-pair analysis says how much of the surviving signal is individual rather than familial.

## Conclusion

The novelty in this space lies less in new architectures than in **auditing the numbers the field already celebrates**. Cooper's six- to fourteen-fold voxel-over-ROI gain is the most striking unexplained result in HCP-YA BMI prediction. Its input keeps a head-size channel open through modulation, and it has never faced a shortcut or within-family test. Our ROI result already sits at the published ROI ceiling, so stacking more tabular features will not close the gap. Testing what the gap consists of will.

Four things remain uncertain. The published *Brain Mechanisms* version may have revised Cooper's numbers. The released HCP T1w images may be defaced. The within-MZ BMI variance in HCP-YA has never been reported and could make the twin arm underpowered, so the first practical step is to compute it from the restricted data before building the pipeline. Finally, a 2025–2026 conference paper on BMI shortcuts or twin-validated brain predictors could have escaped these searches, so a quick check of the OHBM, MICCAI and MIDL proceedings is worth doing before submission.
