# HCP-YA (S500/S900/S1200, ages 22–35) studies relating BMI / obesity to brain MRI

Search method: PubMed query `"Human Connectome Project" AND (BMI OR obesity OR "body mass")` returned 79 records (all 8 pages read on 2026-11-01). Each relevant record was pulled through NCBI E-utilities, and the key papers were also read in full on PMC. Each entry says how deeply it was checked. **[FT]** means the full text was read on PMC. **[ABS]** means only the abstract was read, so atlas, covariate and CV fields marked "not stated" may still appear in the full paper. Numbers are copied from the source. Where a value is absent, the entry says so.

---

## Q1. Paper-by-paper catalogue: citation, N, BMI distribution, features/atlas, method, confounds, results

### Takeaway
I found about 35 HCP-YA papers that use BMI or obesity as a variable of interest with sMRI, rs/task-fMRI or dMRI. Most are mass-univariate. Analysed samples range from 100 to 1,206. Typical HCP-YA BMI is about 26.5 ± 5.2 kg/m², and about 22% of participants have BMI ≥ 30. Structural effects are small: |r| ≈ 0.1–0.2 per region, and cortical thickness results are inconsistent in direction. The strongest prediction results come from multivariate models: CPM on task fMRI gives r = 0.70, elastic net on morphometry gives a held-out R² of 8.9%, and SVM obese-vs-lean classification gives AUC 0.65.

### Cited Findings

#### A. Structural MRI (FreeSurfer / VBM / myelin / subcortical)

**A1. Medic N, Kochunov P, Ziauddeen H, …, Fletcher PC (2019). "BMI-related cortical morphometry changes are associated with altered white matter structure." *Int J Obes* 43(3):523–532. doi:10.1038/s41366-018-0269-9. PMC6462878. [FT]**
- HCP is "Dataset C": n = 897 (503 F), age 28.8 ± 3.7, 381 families. BMI 26.65 ± 5.29 (range 16.48–47.76). Two non-HCP datasets were also analysed (n = 52 and 202) — [PMC6462878](https://pmc.ncbi.nlm.nih.gov/articles/PMC6462878/)
- Features: FreeSurfer cortical thickness, pial and white surface area, mean and Gaussian curvature, WM volume, WM signal intensity 1 mm below the surface, and whole-brain FA (ENIGMA-DTI). Regional analysis used lobes. Linear mixed models with family as a random effect, FDR across 3 tests in HCP, and mediation with 1,000 simulations. Covariates were age and sex, plus surface area for curvature and ICV for WM volume. Motion and education are not mentioned — [PMC6462878](https://pmc.ncbi.nlm.nih.gov/articles/PMC6462878/)
- Results in HCP: BMI showed **no significant association with cortical thickness or surface area**. White-surface Gaussian curvature was positive (β = 0.014, p = 0.028, pFDR < 0.05). FA was negative (β = −0.0206, p = 0.004). WM signal intensity was a trend (β = −0.0119, p = 0.054). FA mediated BMI→curvature (ACME = 0.00014, p = 0.01) — [PMC6462878](https://pmc.ncbi.nlm.nih.gov/articles/PMC6462878/)

**A2. Vainik U, Baker TE, Dadar M, et al. (2018). "Neurobehavioral correlates of obesity are largely heritable." *PNAS* 115(37):9312–9317. doi:10.1073/pnas.1718206115. PMID 30154161. [ABS; the PNAS full text returned HTTP 403]**
- n = 895 HCP siblings, including twins. BMI was analysed continuously — [PubMed 30154161](https://pubmed.ncbi.nlm.nih.gov/30154161/)
- Higher BMI was associated with decreased right frontal and increased left lateral prefrontal cortical thickness, lower entorhinal-parahippocampal thickness and volume, and increased parietal-occipital thickness. It was also associated with poorer visuospatial function, verbal episodic memory, impulsivity and cognitive flexibility — [PubMed 30154161](https://pubmed.ncbi.nlm.nih.gov/30154161/)
- BMI heritability A = 71% (95% CI 61–78%). Genetic correlations of the cognitive and morphometric correlates with BMI were 0.25–0.45, and 77–89% of the phenotypic correlations were explained by genetic factors — [PNAS (search snippet)](https://www.pnas.org/doi/10.1073/pnas.1718206115); [PubMed 30154161](https://pubmed.ncbi.nlm.nih.gov/30154161/)

**A3. Weise CM, Piaggi P, Reinhardt M, et al. (2017). "The obese brain as a heritable phenotype: a combined morphometry and twin study." *Int J Obes* 41(3):458–466. doi:10.1038/ijo.2016.222. PMID 27916985. [ABS]**
- n = 875 (386 M / 489 F), age 28.8 ± 3.7, BMI 26.6 ± 5.3, with 86 MZ and 82 DZ pairs. Whole-brain VBM GMV regressed on BMI, plus ACE twin models — [PubMed 27916985](https://pubmed.ncbi.nlm.nih.gov/27916985/)
- BMI was **positively** associated with GMV in vmPFC and right cerebellum and **negatively** associated with GMV across widespread PFC, cerebellum, temporal lobes and subcortical structures. Heritability was highest for cerebellar and subcortical GMV. No numeric h² is given in the abstract — [PubMed 27916985](https://pubmed.ncbi.nlm.nih.gov/27916985/)

**A4. Weise CM, Bachmann T, Pleger B (2019). "Brain structural differences in monozygotic twins discordant for body mass index." *NeuroImage* 201:116006. doi:10.1016/j.neuroimage.2019.07.019. PMID 31299367. [ABS]**
- 68 BMI-discordant MZ pairs (ΔBMI > 2.5) and 153 MZ pairs for regression. VBM with paired t-tests, TFCE and FWE p < 0.05 — [PubMed 31299367](https://pubmed.ncbi.nlm.nih.gov/31299367/)
- The heavier co-twin had less GMV in occipital and cerebellar cortex, PFC and bilateral striatum including nucleus accumbens. Larger ΔBMI predicted less GMV in the heavier twin. This within-MZ-pair design controls for genetics and shared environment — [PubMed 31299367](https://pubmed.ncbi.nlm.nih.gov/31299367/)

**A5. García-García I, Michaud A, Dadar M, et al. (2019). "Neuroanatomical differences in obesity: meta-analytic findings and their validation in an independent dataset." *Int J Obes* 43(5):943–951. doi:10.1038/s41366-018-0164-4. PMID 30022057. [ABS]**
- A VBM meta-analysis (21 studies, n = 5,882, AES-SDM) found lower GMV in obesity in mPFC, bilateral cerebellum and left temporal pole. These clusters were validated in **HCP (n = 378)**: GMV was negatively associated with BMI in every cluster except one cerebellar cluster — [PubMed 30022057](https://pubmed.ncbi.nlm.nih.gov/30022057/)

**A6. Syan SK, Owens MM, Goodman B, et al. (2019). "Deficits in executive function and suppression of default mode network in obesity." *NeuroImage Clin* 24:102015. doi:10.1016/j.nicl.2019.102015. PMID 31795049. [ABS]**
- Obese (BMI ≥ 30) n = 243 vs lean (18–24.9) n = 469. Measures were N-back task fMRI and FreeSurfer volume, thickness and surface area. FDR correction and an integrative classifier — [PubMed 31795049](https://pubmed.ncbi.nlm.nih.gov/31795049/)
- The obese group performed worse on 7 cognitive tasks (d = 0.231–0.405). It showed greater activation in task-negative regions (vmPFC, PCC, right precentral), i.e. reduced DMN suppression. Morphometry differed in medial OFC, rostral ACC, inferior and superior parietal cortex and temporal pole (FDR p < 0.001). The classifier reached 73.8% accuracy. The abstract does not state the CV scheme or covariates — [PubMed 31795049](https://pubmed.ncbi.nlm.nih.gov/31795049/)

**A7. Xu H, Owens MM, MacKillop J (2023). "Neuroanatomical profile of BMI implicates impulsive delay discounting and general cognitive ability." *Obesity* 31(11):2799–2808. doi:10.1002/oby.23880. PMID 37853988. [ABS]**
- n = 1,100 HCP-YA, of whom 242 (22%) had BMI > 30. Regional morphometry was modelled with **elastic net**, 5-fold CV and a held-out test set — [PubMed 37853988](https://pubmed.ncbi.nlm.nih.gov/37853988/)
- **CV R² = 10.05%; held-out R² = 8.87%.** Predictive regions were enriched in DMN, executive control and salience networks. The association was partly mediated by delay discounting and general cognitive ability. The abstract does not say whether CV was grouped by family — [PubMed 37853988](https://pubmed.ncbi.nlm.nih.gov/37853988/)

**A8. Xu H, Xu C, Xu J (2025). "Altered gray matter structural covariance networks in young adults with obesity." *Int J Obes* 49(5):801–808. doi:10.1038/s41366-024-01703-3. PMID 39695278. [ABS]**
- HCP S1200: 243 obese vs 243 matched lean. Structural covariance of CT and CSA analysed as graphs (BCT) with permutation tests — [PubMed 39695278](https://pubmed.ncbi.nlm.nih.gov/39695278/)
- In obesity, CSA was lower in left entorhinal cortex. CT was higher in left rostral ACC and right superior parietal cortex and lower in left temporal pole. Global network measures did not differ. Nodal differences appeared in PCC, bilateral SFG, entorhinal cortex and insula — [PubMed 39695278](https://pubmed.ncbi.nlm.nih.gov/39695278/)

**A9. Xu G, He J, Zhao J, Wang Y, Xu H (2026). "Identification of critical brain regions for young adults with obesity…" *Int J Obes* 50(10):2222–2230. doi:10.1038/s41366-026-02184-2. PMID 42581075. [ABS]**
- HCP S1200: 243 obese vs 475 healthy-weight. Features were CSA, CT and subcortical GMV, classified with **SVM + SHAP**, plus normative modelling — [PubMed 42581075](https://pubmed.ncbi.nlm.nih.gov/42581075/)
- **ROC-AUC 0.648** with neuroanatomy alone and **0.740** with demographic and cognitive covariates added. Ten of the top 15 features were associated with delay discounting (AUC-DD). The abstract does not state the CV scheme — [PubMed 42581075](https://pubmed.ncbi.nlm.nih.gov/42581075/)

**A10. He J, Xu G, Zhao J, et al. (2026). "Sex-related difference of subcortical gray matter volume associated with crystallized intelligence…" *Biol Sex Differ* 17(1):62. doi:10.1186/s13293-026-00850-8. PMID 41656321. [ABS]**
- HCP S1200: 243 obese vs 243 lean, likely the same sample as A8. Males with obesity had significantly higher right amygdala GMV than lean males. The abstract gives no statistics — [PubMed 41656321](https://pubmed.ncbi.nlm.nih.gov/41656321/)

**A11. Morys F, Tremblay C, Rahayel S, …, Dagher A (2024). "Neural correlates of obesity across the lifespan." *Commun Biol* 7:656. doi:10.1038/s42003-024-06361-9. PMC11133431. [FT, partial]**
- HCP-YA n = 814 (one twin per pair dropped), age 29 ± 4, BMI 26.60 ± 5.28, 421 F. The study also includes ABCD (9,521), HCP-Aging (228) and UK Biobank (36,333) — [PMC11133431](https://pmc.ncbi.nlm.nih.gov/articles/PMC11133431/)
- FreeSurfer 6.0.1 with the **DKT atlas (62 parcels)**. Covariates were age, sex and income. Motion and family are not listed as covariates; relatedness was handled by exclusion — [PMC11133431](https://pmc.ncbi.nlm.nih.gov/articles/PMC11133431/)
- Across the lifespan, BMI was associated with negative thickness in temporal and inferior frontal cortex. **Adult samples showed positive associations in dorsal frontal and occipital regions.** The main text gives no HCP-specific effect sizes (they are in Fig. 1b and the supplement). HCP-YA maps showed no significant neurotransmitter, gene or cognitive correspondence — [PMC11133431](https://pmc.ncbi.nlm.nih.gov/articles/PMC11133431/)

**A12. Dong D, Wang Y, Long Z, et al. (2021). "The Association between Body Mass Index and Intra-Cortical Myelin: Findings from the Human Connectome Project." *Nutrients* 13(9):3221. doi:10.3390/nu13093221. PMID 34579106. [ABS]**
- n = 1,066, using the T1w/T2w myelin ratio. Linear regression with "covariates of no interest". A replication added TIV, substance use and fluid intelligence as covariates — [PubMed 34579106](https://pubmed.ncbi.nlm.nih.gov/34579106/)
- Higher BMI was associated with **lower** myelin in mOFC, rostral ACC, visual cortex, inferior and middle temporal cortex, insula and supramarginal gyrus. It was associated with **higher** myelin in somatosensory cortex, lateral IFG and frontal pole — [PubMed 34579106](https://pubmed.ncbi.nlm.nih.gov/34579106/)

**A13. Brown SSG, Westwater ML, Seidlitz J, Ziauddeen H, Fletcher PC (2023). "Hypothalamic volume is associated with body mass index." *NeuroImage Clin* 39:103478. doi:10.1016/j.nicl.2023.103478. PMC10509524. [FT]**
- HCP-YA n = 1,111. BMI groups were underweight < 18.49, normal 18.5–24.9, overweight 25–29.9 and obese ≥ 30, with counts 14 / 474 / 375 / 242. These sum to 1,105, which is inconsistent with the stated total. Two Cambridge cohorts (n = 240) were also analysed — [PMC10509524](https://pmc.ncbi.nlm.nih.gov/articles/PMC10509524/)
- FreeSurfer 7 with the CNN hypothalamic segmentation of Billot et al. 2020 (5 subunits per hemisphere). Volumes were corrected proportionally by ICV. Tests were Mann-Whitney U with FDR plus linear regression. Motion and family structure are not mentioned, and sex was not analysed — [PMC10509524](https://pmc.ncbi.nlm.nih.gov/articles/PMC10509524/)
- Whole-hypothalamus volume was **positively** associated with BMI (p < 0.05; r² = 0.009 right, 0.012 left). Obese participants had larger bilateral hypothalamus than normal-weight participants (FDR p < 0.01). In the overweight-vs-normal comparison, only the left tubular inferior subunit survived correction — [PMC10509524](https://pmc.ncbi.nlm.nih.gov/articles/PMC10509524/)

**A14. Couvy-Duchesne B, Strike LT, Zhang F, et al. (2020). "A unified framework for association and prediction from vertex-wise grey-matter structure." *Hum Brain Mapp* 41(14):4062–4076. doi:10.1002/hbm.25109. PMID 32687259. [ABS]**
- Analysed 652,283 vertex-wise cortical and subcortical measures in UK Biobank (9,497 + 4,323) and **HCP (n = 1,110)** using linear-mixed-model "morphometricity". Body size traits (height, weight, BMI, waist and hip circumference, body fat %) accounted for a substantial share of morphometricity across phenotypes. The abstract gives no BMI-specific numbers — [PubMed 32687259](https://pubmed.ncbi.nlm.nih.gov/32687259/)

**A15. Chin Fatt CR, Jha MK, Minhajuddin A, et al. (2021). Sex differences in the BMI–brain aging link in young adults (HCP). *Psychoneuroendocrinology* 124:105059. doi:10.1016/j.psyneuen.2020.105059. PMID 33254060. [ABS]**
- n = 1,112 (507 M / 605 F), age 28.80 ± 3.70, BMI 26.53 ± 5.20. Brain age was predicted from T1 with Gaussian process regression. Covariates were sex, race, ethnicity, income and education — [PubMed 33254060](https://pubmed.ncbi.nlm.nih.gov/33254060/)
- BMI × sex on brain-age gap: p = 0.041. Males β = 0.215 (SE 0.050, p < 0.0001); females β = 0.122 (SE 0.035, p = 0.0005) — [PubMed 33254060](https://pubmed.ncbi.nlm.nih.gov/33254060/)

**A16. Soleymani Y, Khalagi K, Negarandeh S, et al. (2026). Metabolic, demographic and behavioral risk factors predict brain structural variability. *Neurol Sci* 47(6):490. doi:10.1007/s10072-026-09095-0. PMID 42120719. [ABS]**
- HCP-YA n = 1,082. BMI is one predictor among many in this "reverse" design, which predicts brain volumes with XGBoost + SHAP. R² > 0.80 for total brain and GM volumes, but BMI is not named among the top SHAP predictors — [PubMed 42120719](https://pubmed.ncbi.nlm.nih.gov/42120719/)

#### B. Resting-state / task fMRI

**B1. Park B-y, Park H, Morys F, …, Dagher A, Bernhardt BC (2021). "Inter-individual body mass variations relate to fractionated functional brain hierarchies." *Commun Biol* 4:735. doi:10.1038/s42003-021-02268-x. PMC8203627. A bioRxiv preprint (10.1101/2020.08.07.241794) was published as this paper. [FT]**
- n = 325 unrelated participants from HCP S900 (twins excluded), age 28.56 ± 3.74, 55% F. BMI 26.30 ± 5.16 (16.65–47.76): underweight 6, healthy 143, overweight 113, obese 63 — [PMC8203627](https://pmc.ncbi.nlm.nih.gov/articles/PMC8203627/)
- **Schaefer 200 (7-network)** atlas, checked at 100/300/400 parcels. rs-FC at 10% density was embedded with BrainSpace diffusion maps; 3 gradients were Procrustes-aligned and summarised as "manifold eccentricity". SurfStat models covaried age and sex. FD was used only in a sensitivity analysis — [PMC8203627](https://pmc.ncbi.nlm.nih.gov/articles/PMC8203627/)
- Higher BMI was associated with greater eccentricity, i.e. **more differentiation between unimodal and heteromodal networks** (permutation p < 0.001). Cortical thickness vs BMI: **r = −0.21 in the temporal pole** (FDR < 0.05). Curvature showed no effect. The T1w/T2w myelin proxy gave r = −0.35 (occipital, central, ventrolateral PFC) — [PMC8203627](https://pmc.ncbi.nlm.nih.gov/articles/PMC8203627/)
- Replication: HCP S1200 (n = 74), 1,000 bootstraps of 300 participants tested on 99, and an independent St Vincent's dataset (n = 36). **Controlling for head motion increased effects by about 42% in most networks but decreased the frontoparietal effect by about 14%** — [PMC8203627](https://pmc.ncbi.nlm.nih.gov/articles/PMC8203627/)

**B2. Bachmann T, Mueller K, Kusnezow SNA, Schroeter ML, Piaggi P, Weise CM (2025). "Cerebellocerebral connectivity predicts body mass index: a new open-source Python-based framework for connectome-based predictive modeling." *GigaScience* 14:giaf010. doi:10.1093/gigascience/giaf010. PMC11899596. [FT]**
- HCP S1200, with n = 999 for both rs-fMRI and all-task analyses (range 999–1,077 across modalities). Median age 29, about 53–54% F, about 75% White. BMI median 25.4 (IQR 22.8–29.1): 43% normal, 33% overweight, 23% obese, 1.4% underweight — [PMC11899596](https://pmc.ncbi.nlm.nih.gov/articles/PMC11899596/)
- 513 nodes: **Glasser HCP-MMP1.0 360** + Tian subcortex 54 + 100 data-driven cerebellar parcels. Task FC used tangent-space connectivity with Ledoit-Wolf shrinkage. **CPM** kept edges at p < 0.05 and combined positive and negative networks in a GLM. Validation was **128-fold CV, with siblings of test participants removed from each training fold**. Gender, age and ethnicity were regressed out. **Head motion was not regressed as a confound** beyond preprocessing — [PMC11899596](https://pmc.ncbi.nlm.nih.gov/articles/PMC11899596/)
- Results: rs-fMRI cerebellocerebral CPM **r = 0.44**. The whole-brain value is reported inconsistently in the paper (0.44 vs 0.40). Single-task models gave r ≈ 0.59–0.62, and the **task-general (average of all tasks) model gave r = 0.70**. Contrast maps predicted poorly. R² is not reported. Positive networks involved temporopolar, perirhinal and entorhinal regions plus FPN (task) and salience/dmFPN (rest). Negative networks involved auditory and sensorimotor regions and right crus (task) and DMN (rest) — [PMC11899596](https://pmc.ncbi.nlm.nih.gov/articles/PMC11899596/)

**B3. Park B, Seo J, Yi J, Park H (2015). "Structural and Functional Brain Connectivity of People with Obesity and Prediction of Body Mass Index Using Connectivity." *PLoS One* 10(11):e0141376. doi:10.1371/journal.pone.0141376. PMC4633033. [FT]**
- n = 120 HCP participants: 60 with BMI < 25 (22.53 ± 1.37) and 60 with BMI ≥ 25 (32.55 ± 3.60). **AAL 116** atlas, with DTI fibre density and rs-FC. Group SC differences were tested by permutation, then BMI was predicted with **PLS regression under leave-one-out CV** — [PMC4633033](https://pmc.ncbi.nlm.nih.gov/articles/PMC4633033/)
- Six motion parameters plus WM and CSF signals were regressed from the fMRI. Age and sex were not used as covariates, and family structure was not handled — [PMC4633033](https://pmc.ncbi.nlm.nih.gov/articles/PMC4633033/)
- Predicted vs actual BMI **r = 0.4414**, RMSE 5.26. The top FC predictor was the right thalamus (R² = 0.205), followed by right superior OFC (R² = 0.067). The top SC predictor was right thalamus–caudate (R² = 0.06). Note that features were pre-selected using group differences, and the paper does not say whether that selection was done inside the CV loop — [PMC4633033](https://pmc.ncbi.nlm.nih.gov/articles/PMC4633033/)

**B4. Sadler JR, Shearrer GE, Burger KS (2018). "Body mass variability is represented by distinct functional connectivity patterns." *NeuroImage* 181:55–63. doi:10.1016/j.neuroimage.2018.06.082. PMID 29966718. [ABS]**
- Three samples of 47 pairs each: BMI-discordant twins (ΔBMI 6.7 ± 3.1), BMI-discordant unrelated pairs, and BMI-similar twins. Between-network rs-FC — [PubMed 29966718](https://pubmed.ncbi.nlm.nih.gov/29966718/)
- Gustatory, visual and DMN networks were weight-sensitive. The leaner twin had stronger striatal/thalamic–PFC FC (pFWE = 0.04), and the heavier twin had stronger cerebellar–insular FC (pFWE = 0.04). Neither effect appeared in BMI-similar twins — [PubMed 29966718](https://pubmed.ncbi.nlm.nih.gov/29966718/)

**B5. Doucet GE, Rasgon N, McEwen BS, et al. (2018). "Elevated Body Mass Index is Associated with Increased Integration and Reduced Cohesion of Sensory-Driven and Internally Guided Resting-State Functional Brain Networks." *Cereb Cortex* 28(3):988–997. doi:10.1093/cercor/bhx008. PMID 28119342. [ABS]**
- n = 496, plus a subsample of obesity-discordant siblings. BMI was associated with FC changes in DMN, central executive, sensorimotor and visual networks. Within discordant siblings, obesity was associated with reduced cohesion of the sensorimotor and visual networks. The abstract gives no numbers — [PubMed 28119342](https://pubmed.ncbi.nlm.nih.gov/28119342/)

**B6. Guo Y, Xia Y, Chen K (2023). "The body mass index is associated with increased temporal variability of functional connectivity in brain reward system." *Front Nutr* 10:1210726. doi:10.3389/fnut.2023.1210726. PMC10300418. [FT]**
- HCP S1200: 954 participants from 428 families, reduced to **one per family, n = 428** (52% F, age 28.61 ± 3.75, BMI 25.86 ± 4.41, non-normal). 300 ROIs (Seitzman) grouped into 9 networks. Sliding-window dynamic FC with 20–40 s windows — [PMC10300418](https://pmc.ncbi.nlm.nih.gov/articles/PMC10300418/)
- Covariates were **age, sex, education, handedness, race and mean FD**. BMI correlated with education (r = −0.165). Inference used permutation with FDR — [PMC10300418](https://pmc.ncbi.nlm.nih.gov/articles/PMC10300418/)
- Higher BMI was associated with greater FC variability in ventral OFC and visual cortex (r ≈ 0.15–0.18), within the limbic network (partial r = 0.18) and DMN (0.12), and between limbic and SMN (0.14), VAN (0.141), DMN (0.16) and FPN (0.15). No replication was reported. The authors describe BMI as "self-reported" — [PMC10300418](https://pmc.ncbi.nlm.nih.gov/articles/PMC10300418/)

**B7. Han J, Zhuang K, Dong D, et al. (2024). "Elevated BMI impacts brain-state dynamics within the sensorimotor-to-transmodal hierarchy." *Obesity* 32(2):291–303. doi:10.1002/oby.23933. PMID 38269472. [ABS]**
- HCP n = 998, plus a Chinese cohort (n = 1,923) and a longitudinal subsample (n = 34). Hidden Markov model brain states — [PubMed 38269472](https://pubmed.ncbi.nlm.nih.gov/38269472/)
- Higher BMI shifted dynamics toward a sensorimotor metastate and reduced transitions to the transmodal metastate. The effect replicated longitudinally and mediated BMI→cognition/mental-health links. The abstract gives no numbers — [PubMed 38269472](https://pubmed.ncbi.nlm.nih.gov/38269472/)

**B8. Zhao J, Manza P, Gu J, et al. (2021). "Contrasting dorsal caudate functional connectivity patterns between frontal and temporal cortex with BMI increase: link to cognitive flexibility." *Int J Obes* 45(12):2608–2616. doi:10.1038/s41366-021-00929-9. PMID 34433905. [ABS]**
- n = 417, using VMHC and seed-based FC. BMI vs DCCS: r = −0.14. Higher BMI was associated with greater caudate–hippocampus FC and lower caudate–IFG/ACC/MFG FC. Right caudate–left hippocampus FC vs DCCS: r = −0.15 — [PubMed 34433905](https://pubmed.ncbi.nlm.nih.gov/34433905/)

**B9. Wang T, Jackson T, Lock M, et al. (2025). "Obesity-related alterations of intrinsic functional architecture: a resting-state fMRI…" *Front Nutr* 12:1559325. doi:10.3389/fnut.2025.1559325. PMID 40510501. [ABS]**
- 198 obese vs 291 healthy-weight, using ICC, fALFF and seed FC plus neurotransmitter maps. Abnormalities were found in right DLPFC and left insula. DLPFC FC was increased with precuneus, insula and IPL and decreased with pre/postcentral and paracentral cortex. Insula and DLPFC measures partially mediated the BMI–executive function link — [PubMed 40510501](https://pubmed.ncbi.nlm.nih.gov/40510501/)

**B10. Del Mauro G, Wang Z (2024). "Associations of Brain Entropy Estimated by Resting State fMRI With Physiological Indices, Body Mass Index, and Cognition." *J Magn Reson Imaging* 59(5):1697–1707. doi:10.1002/jmri.28948. PMID 37578314. [ABS]**
- n = 1,206, voxelwise rs-fMRI brain entropy. BMI was **positively** associated with entropy in DMN-overlapping regions (T 4.75–4.8, |r| ≥ 0.15, FWE) — [PubMed 37578314](https://pubmed.ncbi.nlm.nih.gov/37578314/)

**B11. Rolls ET, Feng R, Cheng W, et al. (2023). "Orbitofrontal cortex connectivity is associated with food reward and body weight in humans." *SCAN* 18(1):nsab083. doi:10.1093/scan/nsab083. PMID 34189586. [ABS]**
- Discovery in UK Biobank (rs-FC n = 37,286); **HCP n = 545 used for cross-validation**. BMI groups: high ≥ 30, mid 22–25, low ≤ 20.5. In HCP, OFC FC differed between high and mid BMI (P = 6 × 10⁻⁵), and low OFC FC was associated with low BMI (P < 0.024) — [PubMed 34189586](https://pubmed.ncbi.nlm.nih.gov/34189586/)

**B12. Shearrer GE, Sadler JR, Papantoni A, et al. (2020). "Earlier onset of menstruation is related to increased body mass index in adulthood…" *J Neuroendocrinol* 32(12):e12891. doi:10.1111/jne.12891. PMID 32939874. [ABS]**
- n = 510 women, BMI 25.9 ± 5.6, using **HCP 1200 PTN netmats** (FSLNets) with race and age as covariates. Menarche × BMI was associated with stronger somatosensory–visual FC (t = 3.45, pFWE = 0.026) and visual–cingulo-opercular FC (t = 4.74, pFWE = 0.0002) — [PubMed 32939874](https://pubmed.ncbi.nlm.nih.gov/32939874/)

**B13. Shearrer GE (2023).** "The Interaction of Glycemia with Anxiety and Depression…". *Brain Sci* 13(7):1086. doi:10.3390/brainsci13071086. PMID 37509016. [ABS]
- n = 325, BMI reported as "26.11 ± 0.29" (SD as printed; it may be an SE). The analysis used 15-IC PTN netmats (FSLNets) with motion, age and race as covariates. The original BMI-related hypotheses were not supported; significant effects involved HbA1c × anxiety/depression — [PubMed 37509016](https://pubmed.ncbi.nlm.nih.gov/37509016/)

**B14. Soleymani Y, Batouli SA, Khalagi K, Pourabbasi A (2026). "Large-Scale Brain Network Connectivity Mediates…" *Int J Endocrinol Metab* 24(4):e168867. doi:10.5812/ijem-168867. PMID 42763643. [ABS]**
- n = 676 with 14 group-ICA networks and age, sex, race and education as covariates. Network connectivity mediated BMI-related reductions in vocabulary (example indirect effect −0.0238, 95% CI −0.0421 to −0.0085) — [PubMed 42763643](https://pubmed.ncbi.nlm.nih.gov/42763643/)

**B15. Task fMRI, BMI as a group or continuous variable [all ABS]:**
- Lancaster TM et al. (2018), *Transl Psychiatry* 8:19, doi:10.1038/s41398-017-0068-4. n = 1,055, mean BMI 26.4. Ventral striatal BOLD to monetary reward vs BMI: β = 0.44, P = 0.013. Heritability: BMI 0.57, VS BOLD 0.12. **Genetic correlation ρg = 0.47 (P = 0.011)**; environmental correlation ρE = −0.07 (ns) — [PubMed 29317597](https://pubmed.ncbi.nlm.nih.gov/29317597/)
- Park BY, Hong J, Park H (2017), *Sci Rep* 7:7664. n = 196 (bootstrap-like resampling), emotion task, **AAL**. Hippocampus, amygdala and ITG activity correlated with BMI — [PubMed 28794427](https://pubmed.ncbi.nlm.nih.gov/28794427/)
- Agarwal K et al. (2021), *Int J Obes* 45:2455. n = 418, gambling task, obesity × alcohol-risk groups. Interactions appeared in DMN and salience regions. No numbers in the abstract — [PubMed 34363001](https://pubmed.ncbi.nlm.nih.gov/34363001/)
- Slomp M et al. (2023), *Brain Connect* 13(9):541. n = 300. **Null**: BMI was not associated with habenula rs-FC or gambling-task activation — [PubMed 37578129](https://pubmed.ncbi.nlm.nih.gov/37578129/)
- Syan et al. 2019 (N-back), see A6.

**B16. Lee WH, Moser DA, Ing A, et al. (2019).** *Brain Topogr* 32(1):80–86. n = 818. **Sparse CCA** of rs-network metastability against non-imaging traits, which included physical well-being indicators such as BMI. The abstract reports only a "modest but significant" association — [PubMed 30136050](https://pubmed.ncbi.nlm.nih.gov/30136050/)

**B17. Sjuls GS, Specht K (2022).** *Brain Connect* 12(10):870–882. Dynamic causal modelling of rs-fMRI in HCP. Body mass and blood pressure can introduce between-participant variability in BOLD hemodynamic parameters. The abstract gives no numbers — [PubMed 35473334](https://pubmed.ncbi.nlm.nih.gov/35473334/)

#### C. Diffusion MRI
- Medic et al. 2019 (A1): HCP FA vs BMI β = −0.0206, p = 0.004 — [PMC6462878](https://pmc.ncbi.nlm.nih.gov/articles/PMC6462878/)
- Park et al. 2015 (B3): DTI fibre-density connectivity used in BMI prediction (DTI-only explained variance 0.359) — [PMC4633033](https://pmc.ncbi.nlm.nih.gov/articles/PMC4633033/)
- Spindler M, Özyurt J, Thiel CM (2020). "Automated diffusion-based parcellation of the hypothalamus reveals subunit-specific associations with obesity." *Sci Rep* 10:22238. doi:10.1038/s41598-020-79289-9. n = 100 HCP. Hypothalamus clustered into 4 subunits per hemisphere from DWI; **MD of the anterior-superior cluster predicted obesity**. The abstract gives no numbers — [PubMed 33335266](https://pubmed.ncbi.nlm.nih.gov/33335266/)
- Luo Q et al. (2020), *BMC Med* 18:278. Primarily IMAGEN; **HCP 7T DTI (n = 156)** was used only to map frontopolar–hypothalamus tractography — [PubMed 33054810](https://pubmed.ncbi.nlm.nih.gov/33054810/)
- Opel N et al. (2019), *Sci Rep* 9:12885. n = 1,206 FA, with BMI only as a nuisance covariate. Not a BMI study — [PubMed 31501448](https://pubmed.ncbi.nlm.nih.gov/31501448/)

#### D. Incidental / adjacent (HCP-YA uses BMI but brain–BMI is not the focus, or the study is not HCP-YA)
- Jha MK et al. (2021), *Psychoneuroendocrinology* 131:105321. Habenular volume, n = 693, with BMI as a covariate only — [PubMed 34157587](https://pubmed.ncbi.nlm.nih.gov/34157587/)
- Lv K et al. (2025), *Front Public Health* 13:1559582. n = 1,205, BMI→cognition. **No imaging** — [PubMed 40182524](https://pubmed.ncbi.nlm.nih.gov/40182524/)
- Rosenblatt M et al. (2024), *Nat Hum Behav* 8:2018. Power for external validation of brain-phenotype prediction. BMI is one of 7 phenotypes, and HCP-YA and HCP-Development are among the datasets. The abstract gives no BMI-specific numbers — [PubMed 39085406](https://pubmed.ncbi.nlm.nih.gov/39085406/)
- **Preprints:** Orlichenko A et al. (2025), medRxiv: a VAE modelling weight effects on FC (HCP-YA, UK Biobank, ADNI) — [PubMed 41001445](https://pubmed.ncbi.nlm.nih.gov/41001445/). Sadil P et al. (2026), bioRxiv: motion-based exclusion — [PubMed 42619703](https://pubmed.ncbi.nlm.nih.gov/42619703/)
- **HCP Lifespan, not HCP-YA:** Farahani A et al. (2026), *PLoS Biol* 24(6):e3003856, uses HCP-Aging and UK Biobank and finds a metabolic axis (BMI, HbA1c, BP) linked to reduced perfusion — [PubMed 42296166](https://pubmed.ncbi.nlm.nih.gov/42296166/). Morys et al. 2024 (A11) also includes HCP-Aging (n = 228) — [PMC11133431](https://pmc.ncbi.nlm.nih.gov/articles/PMC11133431/)

### Inferences
- The BMI distribution in HCP-YA is stable across papers: mean about 26.3–26.65, SD about 5.2–5.3, range about 16.5–47.8. About 22% have BMI ≥ 30 (242–243 obese out of about 1,100). Matched obese-vs-lean designs (243 vs 243/469/475) are a common template.
- Cortical thickness findings conflict. Medic 2019 found no global CT or SA effect (n = 897). Park 2021 found temporal-pole thinning (r = −0.21). Vainik 2018 found a mixed pattern (frontal thinner and thicker in different subregions, entorhinal thinner, parieto-occipital thicker). Morys 2024 found positive dorsal frontal and occipital effects in adults. Xu 2025 found mixed CT changes in obesity. Temporal pole and entorhinal/parahippocampal thinning recur most often; GMV decreases (VBM) are more consistent than CT.
- The best prediction numbers come from task-fMRI CPM (r = 0.70) and rs-CPM (r = 0.44), against structural elastic net (R² ≈ 9–10%, roughly r ≈ 0.3) and structural SVM (AUC 0.65). None of the FC-prediction studies covaried head motion at the prediction stage. This matters because motion is phenotypically and genetically correlated with BMI (see Q4).

### Gaps
- Several abstract-only entries lack atlas, covariate and CV details: Vainik 2018, Xu 2023, Xu 2026, Syan 2019, Doucet 2018, Han 2024, Weise 2017/2019 and Dong 2021. Full texts were not retrieved; PNAS returned 403.
- The PubMed query used the phrase "Human Connectome Project". Papers that only say "HCP" or appear in non-indexed venues may be missed. Examples include conference papers, theses, and possible Kharabian-Masouleh-type HCP analyses, which I did not find.
- I found no HCP-YA study using waist circumference or adiposity measures other than BMI as the primary variable. Couvy-Duchesne 2020 includes waist and hip circumference only within a morphometricity panel.

---

## Q2. Methods landscape: mass-univariate vs multivariate, CV, atlases

### Takeaway
About 75% of the studies are mass-univariate: VBM, FreeSurfer ROI regression, SurfStat, FSLNets with FWE, or seed FC. The few multivariate or ML studies are CPM, PLSR, elastic net, SVM, sparse CCA and morphometricity LMM. Only Bachmann 2025 explicitly reports family-aware CV.

### Cited Findings
- CPM with 128-fold CV that removes siblings of test participants from training; Glasser 360 + Tian 54 + 100 cerebellar parcels — [Bachmann 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11899596/)
- PLSR with LOOCV on AAL-116 rs-FC + DTI (n = 120) — [Park 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4633033/)
- Elastic net with 5-fold CV + held-out test set on morphometry — [Xu 2023](https://pubmed.ncbi.nlm.nih.gov/37853988/)
- SVM + SHAP classification of obese vs healthy-weight from CSA/CT/subcortical volume — [Xu 2026](https://pubmed.ncbi.nlm.nih.gov/42581075/)
- Integrative classifier, 73.8% accuracy — [Syan 2019](https://pubmed.ncbi.nlm.nih.gov/31795049/)
- Sparse CCA (metastability × non-imaging traits) — [Lee 2019](https://pubmed.ncbi.nlm.nih.gov/30136050/)
- Vertex-wise LMM "morphometricity" — [Couvy-Duchesne 2020](https://pubmed.ncbi.nlm.nih.gov/32687259/)
- Atlases in use: Schaefer-200 ([Park 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8203627/)), DKT-62 ([Morys 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11133431/)), FreeSurfer lobes ([Medic 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6462878/)), Seitzman-300 ([Guo 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10300418/)), HCP PTN ICA netmats ([Shearrer 2020](https://pubmed.ncbi.nlm.nih.gov/32939874/); [Shearrer 2023](https://pubmed.ncbi.nlm.nih.gov/37509016/)), AAL-116 ([Park 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4633033/); [Park 2017](https://pubmed.ncbi.nlm.nih.gov/28794427/)), Glasser-360 ([Bachmann 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11899596/)), and CNN hypothalamic subunits ([Brown 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10509524/))

### Inferences
- No HCP-YA BMI study I found uses PALM with HCP exchangeability blocks, even though that is the HCP-recommended approach for permutation inference with family structure. This is a clear methodological gap that a new study could fill.
- Only one ML study (Bachmann 2025) is explicitly family-aware in CV. For Xu 2023 and Xu 2026 it is unknown from the abstracts whether CV folds were grouped by family. If they were not, twin leakage could inflate the estimates.
- Park 2015 selected features by group difference before LOOCV. If that selection was done outside the CV loop, r = 0.44 would be optimistic, though the paper does not explicitly say which.

### Gaps
- I found no HCP-YA BMI study using ridge regression/KRR, SVR or deep learning on FC, or reporting nested CV. Xu 2023 and 2026 may report this in their full texts.

---

## Q3. Confound handling (age, sex, ICV, motion, family, SES, race)

### Takeaway
Age and sex are nearly always covaried. ICV is handled inconsistently. Head motion (FD) is covaried in only a minority of FC studies (Guo 2023, Shearrer 2023) and is absent from CPM prediction (Bachmann 2025). Family structure is handled in one of three ways: random effects (Medic), one participant per family or exclusion of twins (Guo, Park 2021, Morys), or sibling-aware CV (Bachmann).

### Cited Findings
- Family as a random effect in an LMM; age, sex, ICV (for WM volume); motion not mentioned — [Medic 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6462878/)
- One participant per family (n = 428); age, sex, education, handedness, race and mean FD — [Guo 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10300418/)
- Unrelated participants only (twins excluded); age and sex; FD only in sensitivity analysis, where it changed effects by +42% / −14% — [Park 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8203627/)
- One twin per pair excluded; age, sex and income — [Morys 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11133431/)
- Siblings excluded from training folds; gender, age and ethnicity regressed; motion not regressed — [Bachmann 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11899596/)
- Proportional ICV normalisation; family structure not addressed even though there are 457 families — [Brown 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10509524/)
- Covariates were sex, race, ethnicity, income and education — [Chin Fatt 2021](https://pubmed.ncbi.nlm.nih.gov/33254060/)
- Six motion parameters regressed in preprocessing only; age, sex and family not covaried — [Park 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4633033/)
- Motion, age and race as covariates — [Shearrer 2023](https://pubmed.ncbi.nlm.nih.gov/37509016/)
- Dong 2021 added TIV, substance use and fluid intelligence in a replication analysis — [PubMed 34579106](https://pubmed.ncbi.nlm.nih.gov/34579106/)
- BMI correlates with education (r = −0.165) in HCP-YA — [Guo 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10300418/). BMI also correlates with systolic BP (r = 0.45), diastolic BP (r = 0.30) and fluid intelligence (r = −0.17) — [Park 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8203627/)

### Inferences
- Education, blood pressure and fluid intelligence are non-trivially correlated with BMI in HCP-YA. Regressing them out removes shared variance that may be on the causal path. That choice should be explicit, with results reported with and without these covariates.

### Gaps
- Guo 2023 calls HCP BMI "self-reported". I could not verify this from the HCP data dictionary within this search, so whether BMI is measured or self-reported is unresolved here.

---

## Q4. Twin / heritability analyses of BMI–brain associations

### Takeaway
HCP twins have been used in four ways: ACE heritability of BMI-related GMV, genetic correlations of BMI with morphometry and cognition, BMI-discordant MZ co-twin designs for GMV and FC, and genetic overlap between BMI and head motion or striatal reward BOLD. Brain–BMI correlations appear to be mostly genetically mediated, although within-MZ-pair differences still show GMV and FC effects.

### Cited Findings
- BMI heritability 71% (CI 61–78%). Genetic correlations of morphometry and cognition with BMI were 0.25–0.45, and 77–89% of the phenotypic correlation was genetic — [Vainik 2018, PNAS](https://www.pnas.org/doi/10.1073/pnas.1718206115); [PubMed](https://pubmed.ncbi.nlm.nih.gov/30154161/)
- ACE models on 86 MZ + 82 DZ pairs: heritability of BMI-related GMV was highest in cerebellum and subcortical structures — [Weise 2017](https://pubmed.ncbi.nlm.nih.gov/27916985/)
- MZ discordant pairs (68): the heavier twin had less GMV in PFC, striatum/NAcc, occipital cortex and cerebellum — [Weise 2019](https://pubmed.ncbi.nlm.nih.gov/31299367/)
- BMI-discordant twins: cerebellar–insular FC was higher in the heavier twin, and striatal/thalamic–PFC FC was higher in the leaner twin (pFWE = 0.04 each) — [Sadler 2018](https://pubmed.ncbi.nlm.nih.gov/29966718/)
- Obesity-discordant siblings: reduced cohesion of sensorimotor and visual networks — [Doucet 2018](https://pubmed.ncbi.nlm.nih.gov/28119342/)
- BMI–ventral striatum reward BOLD ρg = 0.47 (P = 0.011), ρE = −0.07 (ns); BMI H² = 0.57 — [Lancaster 2018](https://pubmed.ncbi.nlm.nih.gov/29317597/)
- Adult BMI and visual–somatosensory FC were "highly heritable"; the abstract gives no values — [Shearrer 2020](https://pubmed.ncbi.nlm.nih.gov/32939874/)
- Head motion h² = 0.427 in HCP (n = 864). Head motion–BMI was the most strongly replicated phenotypic relationship and showed shared genetic influences — [Hodgson 2017](https://pubmed.ncbi.nlm.nih.gov/27744290/)

### Inferences
- BMI heritability varies by method across HCP papers: 0.57 (Lancaster, SOLAR-type H²r) versus 0.71 (Vainik). This likely reflects different samples and models rather than a conflict.
- Because brain–BMI and motion–BMI associations are both largely genetic, a genetic correlation between BMI and an FC feature could partly reflect motion. Hodgson 2017 shows that this pathway exists.

### Gaps
- I found no HCP-YA study estimating genetic correlations between BMI and DTI metrics, or between BMI and FreeSurfer regional CT using a full bivariate ACE model with published per-region numbers (Vainik's per-region values were not retrieved).

---

## Q5. Methodological criticisms (motion, family leakage, etc.)

### Takeaway
Head motion is the main threat to BMI–FC findings in HCP-YA. Motion correlates with weight (Siegel 2017) and shares genetics with BMI (Hodgson 2017), and motion-based exclusion disproportionately removes higher-BMI participants (Sadil 2026 preprint). Most BMI–FC studies do not fully address this.

### Cited Findings
- Siegel JS, Mitra A, Laumann TO, et al. (2017). "Data Quality Influences Observed Links Between Functional Connectivity and Behavior." *Cereb Cortex* 27(9):4492–4502. doi:10.1093/cercor/bhw253. In HCP, 23 of 122 behavioural, demographic and physiological measures correlated with head motion, **including weight**. Additional cleaning substantially changed previously reported FC–behaviour relationships, and the authors suggest motion-mediated spurious effects may be widespread — [PubMed 27550863](https://pubmed.ncbi.nlm.nih.gov/27550863/); [PMC6410500](https://pmc.ncbi.nlm.nih.gov/articles/PMC6410500)
- Hodgson K, Poldrack RA, Curran JE, et al. (2017). "Shared Genetic Factors Influence Head Motion During MRI and Body Mass Index." *Cereb Cortex* 27(12):5539–5546. doi:10.1093/cercor/bhw321. HCP n = 864 (replication of a Mexican-American pedigree, n = 689). Head motion h² = 0.427 in HCP. Motion–BMI was the strongest replicated association, with shared genetics — [PubMed 27744290](https://pubmed.ncbi.nlm.nih.gov/27744290/)
- **Preprint:** Sadil P et al. (2026, bioRxiv). Across 6 datasets including HCP-YA, higher-BMI participants were disproportionately excluded by motion thresholds; the abstract gives no coefficient — [PubMed 42619703](https://pubmed.ncbi.nlm.nih.gov/42619703/)
- Park 2021 reported that adding motion control changed BMI–gradient effects by +42% in most networks and −14% in FPN — [PMC8203627](https://pmc.ncbi.nlm.nih.gov/articles/PMC8203627/)
- Bachmann 2025 (rs r = 0.44, task r = 0.70) does not list head motion as a regressed confound — [PMC11899596](https://pmc.ncbi.nlm.nih.gov/articles/PMC11899596/)
- Physiological confounds: BMI and blood pressure contribute between-participant BOLD variability at the hemodynamic level — [Sjuls & Specht 2022](https://pubmed.ncbi.nlm.nih.gov/35473334/). Brain-entropy work controlled for respiratory rate, heart rate and systolic BP — [Del Mauro 2024](https://pubmed.ncbi.nlm.nih.gov/37578314/)
- Reporting inconsistencies to watch for: Brown 2023 group counts sum to 1,105 vs a stated 1,111 ([PMC10509524](https://pmc.ncbi.nlm.nih.gov/articles/PMC10509524/)). Bachmann 2025 gives rs whole-brain r as both 0.44 and 0.40 ([PMC11899596](https://pmc.ncbi.nlm.nih.gov/articles/PMC11899596/)). Medic 2019 reports an ACME outside its CI in a non-HCP dataset ([PMC6462878](https://pmc.ncbi.nlm.nih.gov/articles/PMC6462878/))

### Inferences
- High BMI–FC prediction accuracies (r = 0.44–0.70) should be treated as upper bounds until they are re-estimated with FD covaried or partialled from both features and target, family-grouped CV, and ideally external validation. Rosenblatt et al. 2024 show that internal and external performance often differ ([PubMed 39085406](https://pubmed.ncbi.nlm.nih.gov/39085406/)).
- Structural (FreeSurfer) BMI associations are less vulnerable to fMRI motion, but T1 motion can still bias cortical thickness. None of the structural HCP-YA BMI papers I read report a T1 motion or quality covariate.
- For the neurobmi project, which uses FreeSurfer regions against BMI, the most comparable benchmarks are:
  - Medic 2019: null for CT and SA with family-LMM, n = 897.
  - Park 2021: temporal pole r = −0.21.
  - Morys 2024: DKT regression, n = 814.
  - Xu 2023: elastic net, held-out R² = 8.87%.
  - Xu 2026: SVM, AUC 0.648.

### Gaps
- I found no published HCP-YA BMI study that directly reruns a BMI–FC analysis with versus without motion censoring and reports the attenuation (beyond Park 2021's sensitivity numbers). I also found no peer-reviewed paper explicitly critiquing a specific HCP-YA BMI result for motion.
