# Twin and family designs linking brain MRI and BMI/obesity (novelty check: within-MZ-pair test of ML brain-BMI scores)

Search scope: Europe PMC REST API (abstracts), web search, bioRxiv/medRxiv; 2010–2026. PMC full-text pages were blocked by a reCAPTCHA wall, so many details below come from abstracts. Where only an abstract was read, this is noted.

## Q1. Co-twin control / BMI-discordant MZ twin MRI studies

### Takeaway
The BMI-discordant MZ co-twin MRI literature is small. It comes from three groups: the Netherlands Twin Register (Doornweerd/IJzerman; 16 female pairs), the Finnish/Turku PET Centre CROSSYS project (Hentilä/Pietiläinen group; 12 pairs), and the Washington State Twin Registry (Schur lab; tens of pairs). All of them use fMRI, rs-fMRI, PET or hypothalamic T2 measures, with small samples and region-of-interest or network hypotheses. I found no BMI-discordant MZ study that analysed whole-brain structural morphometry (VBM or cortical thickness), and none that used a multivariate or ML-derived brain score.

### Cited Findings
- **Netherlands Twin Register, resting-state fMRI (Doornweerd et al., 2017, Hum Brain Mapp 38:5069–5081)**
  - Sample: 16 female MZ pairs, age 48.8 ± 9.8 y, mean within-pair BMI discordance 3.96 ± 2.1 kg/m² (range 0.7–8.2).
  - Methods: ICA of the salience, basal ganglia, default mode and ACC-OFC networks.
  - Findings: heavier co-twins had lower functional connectivity in bilateral putamen within the basal ganglia network (P < 0.05 FWE). No other network differed. Lower left-putamen connectivity correlated with higher fat intake (P < 0.01). — [Europe PMC abstract, PMC6867098](https://pmc.ncbi.nlm.nih.gov/articles/PMC6867098)
- **Netherlands Twin Register, food-cue fMRI (Doornweerd et al., 2018, Brain Imaging Behav 12:718–727, "Brain reward responses to food stimuli among female MZ twins discordant for BMI")**
  - Sample: the same 16 female pairs, ~4 kg/m² discordance.
  - Findings: no significant ROI activation differences between leaner and heavier co-twins after correction. Heavier co-twins reported more hunger and sweet-food craving.
  - The authors concluded that inherited factors largely drive obesity-related food-cue brain responsivity.
  - The intro describes a larger pool of 54 selected pairs.
  - A 2015 EASD conference report had described decreased activation in heavier twins, which conflicts with the published null result. — [VU research portal](https://research.vu.nl/en/publications/brain-reward-responses-to-food-stimuli-among-female-monozygotic-t/); [Springer PDF](https://link.springer.com/content/pdf/10.1007/s11682-017-9711-1.pdf); [Healio 2015](https://cm.healio.com/news/endocrinology/20150917/twins-with-higher-bmi-show-decreased-brain-activity-while-viewing-highcalorie-food)
- **Finland, CROSSYS exercise trial in BMI-discordant MZ twins (Hentilä et al., 2025, Diabetes Obes Metab, doi 10.1111/dom.70109)**
  - Sample: 12 MZ pairs, mean age 40.4 y. Leaner co-twin BMI 29.1 ± 6.3, heavier 36.7 ± 7.0 kg/m², so about 7.6 kg/m² apart.
  - Methods: [18F]FDG-PET during a hyperinsulinaemic clamp, [11C]PK11195 TSPO-PET and rs-fMRI, with a 6-month exercise intervention.
  - Findings: at baseline, heavier co-twins had higher insulin-stimulated brain glucose uptake in parietal cortex and caudate, and higher resting brain activity. Exercise decreased resting activity in the heavier co-twins. Leaner co-twins had higher TSPO in white matter and hippocampus. — [Europe PMC, PMC12587225](https://pmc.ncbi.nlm.nih.gov/articles/PMC12587225)
  - CROSSYS protocol: MZ twins discordant for body weight, exercise intervention, brain–gut–peripheral glucose cross-talk. — [Heiskanen et al., 2021, BMC Sports Sci Med Rehabil](https://doi.org/10.1186/s13102-021-00241-z)
  - Same cohort, non-brain organs: [Lietzén et al., 2024, Biomolecules](https://doi.org/10.3390/biom14091070); [Lietzén et al., 2024, Nutrients](https://doi.org/10.3390/nu16203554)
- **Washington State Twin Registry (Schur lab)**
  - **Sewaybricker et al., 2021, Physiol Behav**
    - Sample: 54 MZ and 30 DZ adult twins (individuals) from pairs with at least one member obese; 75% had obesity.
    - Measures: DXA, a standardized meal plus buffet, and pre/post-meal food-cue fMRI.
    - Findings: body fat mass was not associated with food-cue brain response in appetite regions (pre-meal β = −0.12 [−0.32, 0.09], P = 0.26). Lower fat mass was associated with being weight-reduced and with greater pre-meal dorsolateral PFC activation (Z = 3.63, P = 0.017). The models accounted for genetic factors by using within-pair comparisons. — [Europe PMC, PMC8440478](https://pmc.ncbi.nlm.nih.gov/articles/PMC8440478)
  - **Salience network study**
    - Sample: 40 MZ and 15 DZ pairs.
    - Measure: hypothalamic gliosis by multi-echo T2 MRI.
    - Findings: baseline salience-network connectivity strength was inherited. Adiposity and gliosis modulated the meal-induced change in connectivity. — [escholarship](https://escholarship.org/uc/item/9n93525r); [WSTR fMRI tag](https://wstwinregistry.org/tag/fmri/)
  - **Berkseth et al., Obesity**
    - Sample: 41 men from 23 twin pairs.
    - Finding: mediobasal hypothalamic T2 (a gliosis index) and visceral fat correlated negatively with testosterone. — [PMC6251490](https://pmc.ncbi.nlm.nih.gov/articles/PMC6251490); [doi 10.1002/oby.22324](https://zendy.io/title/10.1002/oby.22324)
  - **Ongoing trial NCT07430852 ("Inherited and Environmental Risks Acting on Body Weight")**
    - Design: co-twins discordant for habitual diet.
    - Primary outcome: hypothalamic gliosis (T2 relaxation time).
    - No results posted. — [ClinicalTrials.gov](https://clinicaltrials.gov/study/NCT07430852)
- **Related discordant-MZ design for a different exposure (Schur et al., 2012, Physiol Behav)**
  - Sample: 10 MZ pairs discordant for restrained eating.
  - Finding: restrained twins showed greater amygdala and thalamus food-cue activation. — [PMC4151510](https://pmc.ncbi.nlm.nih.gov/articles/PMC4151510)
- **Discordant-MZ grey matter study for physical activity (not BMI)**
  - Sample: 10 male MZ pairs discordant for leisure-time physical activity (Finnish).
  - Finding: active co-twins had larger striatal and PFC grey matter volumes. — [UCL Discovery entry](https://discovery-pp.ucl.ac.uk/id/eprint/1564459)

### Inferences
- The co-twin control results are mixed:
  - Two NTR food-cue analyses and the WSTR analysis largely support genetic confounding of obesity–brain-response associations: the effects vanish within pairs.
  - Within-pair differences do persist for putamen connectivity, brain glucose uptake and hypothalamic gliosis-related measures.
- No BMI-discordant MZ study used structural T1 morphometry at whole-brain level, or the HCP/UK Biobank-style features an ML BMI predictor would use.
- Pair counts are 12–40, which is underpowered for anything except large within-pair effects.

### Gaps
- I could not verify the brief's "Raji/others", "TwinFat" brain-imaging or "Ollikainen" studies. Ollikainen's TwinFat work appears to be adipose-tissue and epigenetic, not brain MRI. My searches found no Finnish structural MRI study of BMI-discordant MZ twins; only the PET/fMRI CROSSYS papers turned up.
- I found no co-twin control BMI MRI study in QTIM, VETSA, TwinsUK or ABCD.

## Q2. Genetic correlation / bivariate heritability of brain measures and BMI

### Takeaway
Across HCP-YA, an adolescent US twin sample, VETSA and the San Antonio extended pedigrees, the brain–BMI association is mostly genetic. Twin and pedigree estimates put 77–95% of the phenotypic correlation on shared additive genetics, with rG of about 0.25–0.45.

### Cited Findings
- **Vainik et al., 2018, PNAS 115(37), "Neurobehavioral correlates of obesity are largely heritable"**
  - Sample: HCP S900, n = 895 siblings, including 111 MZ pairs and 188 DZ-twin/sibling pairs.
  - Method: effects for each neurobehavioural factor (cortical thickness, volume, cognition, personality) were aggregated into composite scores, then fitted in bivariate twin models.
  - Findings:
    - Higher BMI was associated with thinner right and thicker left frontal cortex, notably lateral PFC (the "right brain hypothesis"), and with lower entorhinal–parahippocampal thickness and volume.
    - Cognitive and brain morphometry composites had rG = 0.25–0.45 with BMI.
    - Genetics explained 77–89% of the phenotypic correlations. — [Europe PMC abstract, PMC6140494](https://pmc.ncbi.nlm.nih.gov/articles/PMC6140494); [bioRxiv preprint](https://www.biorxiv.org/content/10.1101/204917.full.pdf)
  - Methodological relevance: this "aggregate the brain correlates of BMI into a score, then do twin modelling" step is the nearest precedent to an ML brain-BMI score in twins. It was a correlational composite in a variance-decomposition model, not a cross-validated predictor tested within MZ pairs.
- **Weise et al., 2017, Int J Obes 41:603–611, "The obese brain as a heritable phenotype"**
  - Sample: HCP, n = 875 (age 28.8 ± 3.7; BMI 26.6 ± 5.3), including 86 MZ and 82 DZ pairs.
  - Findings: VBM showed BMI–GMV associations, positive in vmPFC and right cerebellum and widespread negative elsewhere. Heritability of BMI-associated regions varied and was highest in cerebellum and subcortical structures.
  - Univariate ACE only; no bivariate rG. — [PMC5402354](https://pmc.ncbi.nlm.nih.gov/articles/PMC5402354)
- **Kennedy et al., 2019, NeuroImage**
  - Sample: adolescent twins, n = 258 (54 MZ, 75 DZ pairs; age 13.6), with BMIz.
  - Findings: VBM regional heritability was 15–97%. In bivariate models, BMIz and brain structure share "~1/3 of their genes", and "~95% of the phenotypic correlation" was due to shared additive genetics. — [PMC6688918](https://pmc.ncbi.nlm.nih.gov/articles/PMC6688918)
- **Curran et al., 2013, Hum Hered**
  - Sample: 839 Mexican Americans in extended pedigrees (San Antonio Family Heart Study), analysed with SOLAR.
  - Findings: genetic factors raising BMI were associated with reduced cortical surface area and subcortical volume. There were two pleiotropic QTLs: BMI with ventral diencephalon volume, and BMI with supramarginal surface area. — [UTHSCSA record](https://scholars.uthscsa.edu/en/publications/identification-of-pleiotropic-genetic-effects-on-obesity-and-brai/); [PMC3889074](https://pmc.ncbi.nlm.nih.gov/articles/PMC3889074)
- **Spieker et al., 2015, Front Genet**
  - Sample: 761 family members (San Antonio).
  - Heritabilities: BMI h² = 0.58, waist circumference h² = 0.57, FA h² = 0.49.
  - Genetic correlations of BMI with FA: corpus callosum genu ρG = −0.25, body −0.30, splenium −0.26; internal capsule −0.29; thalamic radiation −0.31; superior fronto-occipital fasciculus −0.39. — [PMC4327744](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4327744/)
- **HCP white-matter twin preprint (medRxiv)**
  - Sample: 1,065 participants aged 22–36.
  - Findings: FA heritability was >50%, BMI heritability ~60%. Greater BMI was associated with lower white matter integrity, plausibly through common genetic effects. A secondary summary reports that "1/2 to 2/3" of the brain-structure–BMI correlation was attributable to heritability.
  - Not peer-reviewed. — [medRxiv](https://medrxiv.org/node/97539)
- **VETSA, Franz et al., 2019, Neurobiol Aging**
  - Sample: 373 men with BMI measured at ~20, 40, 56 and 62 years. The obese-trajectory group (n = 171) was compared with the lean-trajectory group (n = 202).
  - Findings: the obese trajectory was associated with thinner frontal and temporal cortex at age 62. There was no white-matter difference.
  - This is an association analysis in twins; I did not see a reported co-twin analysis in the abstract. — [PMC6591047](https://pmc.ncbi.nlm.nih.gov/articles/PMC6591047); [escholarship](https://escholarship.org/uc/item/08d220rj)
- **ABCD**
  - No twin-based BMI–brain rG found.
  - Morys et al. used a BMI polygenic score in 4,157 ABCD children and linked it to lower frontal and temporal cortical thickness and volume. — [medRxiv 2022](https://medrxiv.org/content/10.1101/2022.06.07.22275937v1.full.pdf)
  - A 2026 DCN review covers a decade of ABCD weight-gain and brain-development work. — [Adise et al., 2026](https://doi.org/10.1016/j.dcn.2026.101776)
- **Molecular-genetic confirmation (no twins): Fusco et al., 2025, PLoS Genet**
  - Data: UK Biobank GWAS.
  - Finding: most significant BMI–brain-morphology genetic correlations were negative. — [PMC12048161](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12048161/)

### Inferences
- Twin and pedigree evidence converges: about 77–95% of the brain–BMI covariance is genetic.
- So any ML brain-BMI score is expected to carry mostly between-family/genetic signal. A within-MZ-pair test would directly measure how much of the score's validity survives once genes and shared environment are held constant.
- The NTR and WSTR co-twin results already hint that much of the signal may not survive.

### Gaps
- I could not verify "Medic 2019 HCP with family random effects". The only Medic paper I found was Medic et al., 2016, Int J Obes, a non-twin VBM study, and I did not confirm its details. Treat this citation as unverified.
- No QTIM (Queensland) or TwinsUK BMI–brain bivariate twin paper surfaced in my searches.
- Specific environmental correlations (rE) from Vainik 2018 were not retrievable: the full text was blocked by PMC captcha and bioRxiv returned HTTP 429.

## Q3. Has anyone applied an ML brain-predicted BMI (or "brain-BMI gap") within twin pairs, or used family structure to separate within- vs between-family prediction?

### Takeaway
I found no study that tests an ML-derived brain-BMI score with within-MZ-pair differences, or that decomposes brain-based BMI prediction into within- and between-family components. ML brain-BMI papers use family structure only to prevent leakage, by grouping train/test splits by family. Within-family decomposition is standard for polygenic scores, but I found no imaging analogue for BMI. On current evidence the idea appears novel.

### Cited Findings
- **Cooper, Elsayed, Owens & MacKillop, 2025, bioRxiv 10.1101/2025.04.11.648433**
  - Data: 3D-CNN on HCP S1200 T1, final n = 1,106.
  - Accuracy: mean CV R² = 0.325 and lockbox R² = 0.442. A random forest on atlas features reached lockbox R² = 0.031. Random forest and elastic net on CNN features reached R² = 0.485 and 0.456.
  - "The train/test split was conducted on the Family ID variable", given sibling oversampling in HCP.
  - No twin-specific or within-pair analysis was reported (first 100k characters of the full text read). — [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.04.11.648433v1.full)
- **Deep-learning "brain-BMI gap" in the DIRECT-PLUS lifestyle trial (2024, Hum Brain Mapp 10.1002/hbm.26595)**
  - Reductions in predicted BMI tracked actual weight loss and were larger in active-diet arms.
  - Not a twin design. — [PMC10878010](https://pmc.ncbi.nlm.nih.gov/articles/PMC10878010/); [Wiley](https://onlinelibrary.wiley.com/doi/full/10.1002/hbm.26595)
- **CNN BMI prediction from a single T1 plus age and sex (2020, Front Neuroinform)**
  - Saliency pointed to caudate and amygdala.
  - Not twins. — [PMC7104804](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7104804/)
- **Cerebellocerebral CPM predicting BMI in HCP-YA (2025, GigaScience giaf010)**
  - Uses permutation testing.
  - The abstract does not describe a within-family analysis. — [PMC11899596](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11899596/)
- **Earlier HCP rs-fMRI + DTI PLS regression BMI prediction (2015, PLOS ONE)**
  - Percent error 15.0%. — [PMC4633033](https://pmc.ncbi.nlm.nih.gov/articles/PMC4633033)
- **Closest analogue, ML brain-age scores in twins: heritability studies, not co-twin control**
  - Brouwer et al., 2021, Cereb Cortex: n = 673 adolescent twins/siblings; heritability of the brain-age gap up to 79%. — [escholarship PDF](https://escholarship.org/content/qt9p75z8vm/qt9p75z8vm.pdf?t=piy9h2)
  - Gillespie et al., 2022, Front Aging Neurosci: VETSA, n = 734 men aged 51–72; predicted brain age h² = 59–75%; a single latent factor with h² = 73%. — [Frontiers](https://www.frontiersin.org/articles/10.3389/fnagi.2022.831002)
  - Cole et al., 2017: 62 female twins, deep-learning brain age heritable. — [arXiv 1612.02572](https://arxiv.org/pdf/1612.02572)
  - A VETSA review notes that co-twin control has mainly been used for psychiatric disorders. — [escholarship](https://escholarship.org/content/qt0x5669wv/qt0x5669wv.pdf?t=rffkx5)
- **Within-family logic for genetic and brain predictors**
  - Within- vs between-family polygenic score prediction is well established; most predictive power usually persists within families, with attenuation (~55%) for educational attainment. — [Selzam et al., PMC6698881](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6698881/); [Lello et al., sibling validation, PMC7411027](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7411027/)
  - Within-family estimates can still carry residual biases. — [PLOS Biol 2023](https://journals.plos.org/plosbiology/article?id=10.1371%2Fjournal.pbio.3002511)
  - Imaging precedent: brain size does not predict IQ within sibling pairs (Schoenemann et al., 2000, PNAS; outside the 2010 window but conceptually relevant). — [PNAS](https://www.pnas.org/doi/10.1073/pnas.97.9.4932)
  - A later within-family brain-size/IQ analysis exists. — [Lee et al., Intelligence 2019](https://www.sciencedirect.com/science/article/abs/pii/S0160289618301703)

### Inferences
- The proposed analysis has several parts:
  - Train an ML brain-BMI model on unrelated people or other families.
  - Test whether within-MZ-pair differences in predicted BMI track within-pair differences in measured BMI.
  - Compare within-family and between-family slopes, mirroring PGS within-family validation.
- I found no direct precedent for this combination. The closest precedents are Vainik 2018 (composite brain score plus twin rG), brain-age heritability in twins, and family-grouped CV in HCP brain-BMI models.
- Prior co-twin evidence (NTR and WSTR null food-cue results) and the ~77–95% genetic share of the brain–BMI covariance predict strong attenuation within MZ pairs. That would be an informative result either way: it would show whether the score indexes BMI-caused or environmentally driven brain change, or only genetic predisposition.

### Gaps
- Coverage of conference abstracts (OHBM, ObesityWeek) and of non-English literature was not exhaustive. A 2025–2026 preprint could exist that my searches missed.
- I did not check whether UK Biobank sibling pairs have been used for within-sibling brain-BMI prediction.

## Q4. How many MZ pairs are in HCP-YA, and how BMI-discordant are they?

### Takeaway
HCP-YA S1200 has 149 genotype-confirmed MZ pairs. Analysed subsets typically contain 86–151 MZ pairs, depending on release and QC. I found no published figure for within-MZ-pair BMI discordance in HCP-YA, so it would need to be computed from the restricted data.

### Cited Findings
- dbGaP phs001364: genotype data for 1,142 of 1,206 S1200 participants, including 149 genetically confirmed MZ pairs (298 participants) and 94 DZ pairs (188 participants). — [HCP announcement](https://humanconnectome.org/study/hcp-young-adult/article/hcp-releases-snp-genotypes-collected-hcp-young-adult-subjects-dbgap); [OmicsDI phs001364](https://omicsdi.org/dataset/dbgap/phs001364)
- Analysis subsets:
  - Vainik 2018 (S900): 111 MZ pairs — [PMC6140494](https://pmc.ncbi.nlm.nih.gov/articles/PMC6140494)
  - Weise 2017: 86 MZ and 82 DZ pairs — [PMC5402354](https://pmc.ncbi.nlm.nih.gov/articles/PMC5402354)
  - A 2018 S1200 sibling study: 138 MZ, 79 DZ and 108 non-twin sibling pairs
  - An ACE cortical-thickness study: 151 MZ and 78 DZ pairs
  - The last two are from search summaries of [arXiv 1802.03397](https://arxiv.org/pdf/1802.03397) and [arXiv 1905.07502](https://arxiv.org/pdf/1905.07502); attribution between these two was not checked in full text.
- Self-reported zygosity in HCP is sometimes wrong (some self-reported DZ pairs are genetically MZ), so the ZygosityGT field should be used. — [HCP-Users mail archive](https://mail-archive.com/hcp-users@humanconnectome.org/msg04199.html)
- BMI-discordance benchmarks from dedicated discordant-twin samples, for comparison:
  - NTR: 3.96 ± 2.1 kg/m² (range 0.7–8.2) — [PMC6867098](https://pmc.ncbi.nlm.nih.gov/articles/PMC6867098)
  - CROSSYS: ~7.6 kg/m² (29.1 vs 36.7) — [PMC12587225](https://pmc.ncbi.nlm.nih.gov/articles/PMC12587225)
- HCP-YA BMI distribution (Weise 2017 sample): mean 26.6 ± 5.3 kg/m². — [PMC5402354](https://pmc.ncbi.nlm.nih.gov/articles/PMC5402354)

### Inferences
- HCP-YA is an unselected sample: twins were not recruited for discordance, and BMI heritability is ~60%. Most MZ pairs will therefore have small within-pair BMI differences, likely far fewer pairs differing by ≥4 kg/m² than in the dedicated discordant cohorts.
- This variance restriction plus measurement noise in predicted BMI makes power the key design risk. Using continuous within-pair differences across all ~140–149 pairs, rather than dichotomized "discordant" pairs, is advisable.
- ABCD (~800+ twin pairs at baseline) could add power, but I did not verify that number here.

### Gaps
- No source reported the distribution of within-MZ-pair BMI differences in HCP-YA. It must be computed from the restricted HCP data (ZygosityGT, Family_ID, BMI).
- The MZ pair count with usable T1 plus BMI after QC in S1200 was not found as a single authoritative number. The values above vary from 86 to 151.
