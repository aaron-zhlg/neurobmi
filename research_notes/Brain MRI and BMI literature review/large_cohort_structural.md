# Large-cohort and meta-analytic evidence on BMI/obesity and brain structure (adults, outside HCP-YA; ABCD as separate subsection)

Scope note: the notes come from about 15 search/fetch calls. Full text was read for Opel 2021 (PMC) and Ronan 2020 (PMC). Chen 2020 (an ALE meta-analysis) was also read, because the PMC link returned in the García-García search pointed to it. Other entries rest on abstracts, repository records, or press coverage, and each one says so. Any value marked "unverified" comes from memory and was not confirmed in a source. Check it before you cite it.

## Q1. Per-paper evidence: cohort, N, features/atlas, method, confounds, main results with effect sizes

### Takeaway
The best-powered FreeSurfer evidence is the ENIGMA-MDD mega-analysis (N=6,420, Desikan-Killiany). It uses the same pipeline as a typical HCP FreeSurfer study, so it makes the closest benchmark. Obesity (BMI>30) goes with widespread small cortical thinning (Cohen's d about −0.1 to −0.33). The largest effects are in the fusiform and temporal cortex, with the frontal cortex next. Surface-area effects are small and mixed in sign (|d| ≤ 0.17), and some subcortical volumes are *larger* (amygdala, thalamus, accumbens; d up to +0.21). UK Biobank (N≈10–12k, aged 45–76) shows lower total and subcortical gray-matter volume with higher adiposity, especially central adiposity (waist-hip ratio). VBM meta-analyses agree on lower medial prefrontal/orbitofrontal, cerebellar and temporal-pole GMV.

### Cited Findings

**ENIGMA MDD working group — Opel N, Thalamuthu A, Milaneschi Y, … Baune BT, Dannlowski U. Molecular Psychiatry 2021;26(9):4839–4852. DOI 10.1038/s41380-020-0774-9 (PMC8589644)**
- Sample: N=6,420 (3,519 controls, 2,901 MDD) from 28 sites. 1,223 obese (BMI>30) vs 2,917 normal-weight (BMI 18.5–25). Mean age 42.9 (SD 15.3); the paper gives no age range, and 520 participants were under 21. 56.95% female; mean BMI 25.97. Genetic subsample n=3,907. — [Opel 2021, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8589644/)
- Features: FreeSurfer with the Desikan-Killiany atlas. Thickness and surface area for 34 regions per hemisphere, 8 subcortical volumes per hemisphere, and global measures (157 measures in all). — [Opel 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8589644/)
- Method/confounds: a separate linear model for each measure. Model A is obese vs normal-weight; Model B is continuous BMI. Covariates were age, sex, MDD diagnosis and site, with ICV added for surface area and subcortical volume. Sensitivity analyses added antidepressant use and mean thickness. Results were Benjamini-Hochberg FDR-corrected (q<0.05), and d was derived from t. **Education, hypertension, diabetes and smoking were not covariates in the main models** (they are not listed in the methods). — [Opel 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8589644/)
- Cortical thickness (obese vs normal): left hemisphere mean d=−0.214, right d=−0.203. Largest regions: L fusiform −0.331, R fusiform −0.325, R superior temporal −0.251, L superior temporal −0.243, L inferior temporal −0.231, L middle temporal −0.227. About 50 regions were significant, mostly temporal and frontal. — [Opel 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8589644/)
- Surface area (small, mixed sign): L isthmus cingulate +0.167, R isthmus cingulate +0.147, L transverse temporal +0.138, R paracentral +0.104, L paracentral +0.087; R rostral middle frontal −0.111, L inferior temporal −0.096, R inferior temporal −0.089, L lingual −0.083. — [Opel 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8589644/)
- Subcortical volume (positive direction): R amygdala +0.211, L thalamus +0.147, R thalamus +0.129, L amygdala +0.123, L accumbens +0.118, R hippocampus +0.086. — [Opel 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8589644/)
- Multivariate SVM classifier (obese vs normal-weight): balanced accuracy 68.7%, AUC 0.687. It fell to 64.1% in an age-, sex- and diagnosis-matched sample and to 59.5% under leave-one-site-out. — [Opel 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8589644/)
- No BMI×MDD interaction survived FDR. — [Opel 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8589644/)

**UK Biobank — Dekkers IA, Jansen PR, Lamb HJ. Radiology 2019. "Obesity, Brain Volume, and White Matter Microstructure at MRI: A Cross-sectional UK Biobank Study"** (DOI 10.1148/radiol.2019181012, unverified)
- N=12,087, aged 45–76, imaged on 3T with T1 and DTI between 2014 and 2018. Total body fat % came from bioimpedance. — [UK Biobank publication record (via search)](https://www.ukbiobank.ac.uk/publications/obesity-brain-volume-and-white-matter-microstructure-at-mri-a-cross-sectional-uk-biobank-study/); [RSNA press release](https://www.rsna.org/news/2019/april/obesity-linked-structure-brain)
- In men, higher body fat was linked to lower total GMV and to lower subcortical GM volumes in every structure except the amygdala. In women it was linked only to globus pallidus volume. Press coverage gives the size of the effect in men: +5.5% total body fat ↔ −3,162 mm³ GMV. — [ScienceDaily](https://www.sciencedaily.com/releases/2019/04/190423133736.htm); [Sci.News](https://www.sci.news/medicine/excessive-body-fat-smaller-gray-matter-volume-07126.html)
- White matter: higher body fat went with *higher* fractional anisotropy in both sexes, which the authors read as altered microstructure. — [RSNA](https://www.rsna.org/en/news/2019/April/obesity-linked-structure-brain)
- The covariate list was not retrieved (gap).

**UK Biobank — Hamer M, Batty GD. Neurology 2019;92(6):e594–e600 (volume and pages unverified). PMID 30626649**
- N=9,652, mean age about 55. Exposures were BMI, waist-hip ratio (WHR) and fat mass. — [PubMed 30626649 (via search)](https://pubmed.ncbi.nlm.nih.gov/30626649/)
- After adjustment, higher WHR, BMI and fat mass were each linked to lower GMV. The WHR coefficient was −4,272 (95% CI −5,280 to −3,264), with units as in the original (mm³ per unit WHR, unverified). People with both high BMI and high WHR had the lowest GMV: about 785 cm³ vs about 798 cm³ in lean adults, per press coverage. — [PubMed](https://pubmed.ncbi.nlm.nih.gov/30626649/); [News-Medical](https://www.news-medical.net/news/20190111/Excess-belly-fat-may-lead-to-a-reduction-in-gray-matter.aspx)
- Obesity was also linked to lower caudate, putamen, pallidum and nucleus accumbens volumes. **No association with white matter volume.** — [PubMed](https://pubmed.ncbi.nlm.nih.gov/30626649/)
- Exact covariates were not retrieved. My recollection is age, sex, education, smoking, physical activity, hypertension, diabetes and others, but this is unverified (gap).

**Meta-analysis (VBM, SDM) — García-García I, Michaud A, Dadar M, … Dagher A. International Journal of Obesity 2019;43:943–951 (the e-pub is dated 2018). DOI 10.1038/s41366-018-0164-4**
- 21 VBM studies, N=5,882, pooled with seed-based d mapping (AES-SDM). — [Springer](https://link.springer.com/article/10.1038/s41366-018-0164-4); [CORE PDF](https://core.ac.uk/download/231719271.pdf)
- Obesity measures were linked to lower GMV in the medial prefrontal cortex, the bilateral cerebellum and the left temporal pole. — [Springer](https://link.springer.com/article/10.1038/s41366-018-0164-4)
- The clusters were validated in HCP (n=378). Most showed negative correlations with BMI; one cerebellar cluster was the exception. — [Springer](https://link.springer.com/article/10.1038/s41366-018-0164-4)

**Meta-analysis (VBM, ALE) — Chen EY, Eickhoff SB, Giovannetti T, Smith DV. NeuroImage: Clinical 2020;28:102420. DOI 10.1016/j.nicl.2020.102420**
- 25 articles and 28 experiments; the primary analysis used 26 experiments with N=7,612 (mean age 39.8, mean BMI 27.0). Method was random-effects ALE with cluster-level FWE at p<0.05. — [Chen 2020, PMC7509458](https://pmc.ncbi.nlm.nih.gov/articles/PMC7509458)
- The only convergent cluster was lower GMV in the **right orbitofrontal cortex**: frontal pole BA10 (peak 10,58,−22; Z=4.83) and frontal medial cortex BA11 (peak 6,52,−24; Z=5.10), with cluster volume 1,128 mm³. Only 6 experiments reported higher GMV with BMI, too few to analyze. — [Chen 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7509458)
- Confounds: not all included studies controlled for TIV or sex. Effects were weaker in samples with mean age ≥40. Publication bias and heterogeneity were not assessed. — [Chen 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7509458)

**Rotterdam Study — Frontiers in Neurology 2019 (10.3389/fneur.2019.00559; first author not retrieved)**
- About 4,100 adults with DXA body composition and MRI. Cross-sectionally, higher BMI and fat-mass index went with smaller **white matter** volume, while higher fat-free-mass index went with *larger* GMV. Longitudinally, body composition did not predict change in tissue volume, white matter integrity or small-vessel-disease markers, and the authors invoke shared etiology or cumulative risk. No cortical-thickness analysis was found. — [Frontiers in Neurology 2019](https://www.frontiersin.org/articles/10.3389/fneur.2019.00559)

**LIFE-Adult (Leipzig)**
- n=625, aged 20–59: higher BMI predicted lower (pre)frontal, temporal and occipital cortical thickness and a *larger* left nucleus accumbens volume. Food-addiction scores added little beyond BMI. The search result points to Beyer/Zhang et al. 2020, Int J Obes (DOI 10.1038/s41366-020-00702-4; attribution unverified). — [Springer](https://link.springer.com/10.1038/s41366-020-00702-4); [MPG PuRe PDF](https://pure.mpg.de/pubman/item/item_3264179_5/component/file_3264180/Beyer_Zhang_2020.pdf)
- n=748, aged 60–79: a metabolic profile of high body fat, visceral adiposity and inflammation was linked to lower GMV and possibly lower executive function. Body weight and fat mass contributed most. — [Frontiers in Aging Neuroscience 2019, 10.3389/fnagi.2019.00202](https://www.frontiersin.org/articles/10.3389/fnagi.2019.00202)
- An overview from the group (Witte lab): visceral fat is linked to lower GMV and more white-matter lesions, more strongly than BMI. — [MPI CBS](https://www.cbs.mpg.de/events/10324/2470)

**Other UK Biobank**
- A vertex-wise analysis of UK Biobank traits found 19 significant clusters with *small* associations with age, sex and BMI. — [Human Brain Mapping, PMC9122091](https://pmc.ncbi.nlm.nih.gov/articles/PMC9122091)

### Inferences
- Benchmark for a Desikan-Killiany FreeSurfer study: expect negative BMI–thickness associations, strongest in the fusiform, lateral/superior/inferior temporal and (orbito)frontal cortex, with d ≈ −0.2 to −0.33 for obese vs normal-weight. Continuous-BMI partial correlations should be small, probably |r| ≈ 0.05–0.15 (inferred from d; not reported directly). At HCP-YA sample sizes (~1,100), only the stronger regions will survive FDR.
- Thickness and surface area diverge. Thickness effects are consistently negative. Area effects are tiny and mixed in sign, with positive values in the isthmus cingulate and paracentral cortex. Volume results therefore partly depend on which component dominates.
- Subcortical direction depends on age and cohort. In younger and middle-aged FreeSurfer samples (ENIGMA, LIFE), amygdala, thalamus, accumbens and hippocampus can be *larger* with obesity. In older UK Biobank samples, striatal and pallidal volumes are *smaller*. Whether ICV is adjusted matters a lot (see Chiesa 2024 under Q2).
- Central adiposity (WHR, visceral fat) tends to show stronger effects than BMI. BMI also mixes fat with fat-free mass, and Rotterdam found fat-free mass positively related to GMV.

### Gaps
- Exact covariate lists for Dekkers 2019 and Hamer & Batty 2019 (the abstracts were blocked).
- % variance explained by BMI in the regional models is not reported in any source retrieved. Opel reports only d.
- No strong large-cohort study using the Destrieux atlas was found.
- Rotterdam first author and cortical-thickness data were not found.
- Effect sizes for Opel's overweight vs obese comparison are in the supplement only.

## Q2. Causal / Mendelian randomization / longitudinal and weight-loss evidence

### Takeaway
Causal evidence is mixed. One MR study using ENIGMA outcomes supports higher BMI → lower global cortical thickness. The largest life-course MR, in UK Biobank (Chiesa et al., Brain 2024), suggests that many adult obesity–brain associations reflect *childhood* adiposity and larger head size established in childhood, not effects of midlife obesity. Bariatric surgery studies (small n) show partial GM/WM density recovery after weight loss.

### Cited Findings
- **Chiesa ST et al., Brain 2024 (DOI 10.1093/brain/awae198).** A two-sample life-course MR in 37,501 UK Biobank imaging participants, plus 6,996 ABCD children. Instruments were 266 childhood-adiposity and 470 adult-adiposity variants from a GWAS of 407,741 participants. Genetically higher childhood adiposity predicted several smaller adult brain volumes *relative to ICV*. These effects held after adjusting for adult adiposity and birthweight, while most *observational* adult associations attenuated toward the null. A sensitivity analysis linked many effects to persistently larger head size in people who gained weight in childhood. ABCD children with high BMI at age 10 already showed a similar pattern. — [UK Biobank publication record](https://www.ukbiobank.ac.uk/publications/childhood-adiposity-underlies-numerous-adult-brain-traits-commonly-attributed-to-midlife-obesity/); [OxCIN record](https://www.oxcin.ox.ac.uk/publication/2009921)
- **MR in Brain Sciences 2023 (PMC10295948).** Univariable MR (GIANT/UKB BMI → ENIGMA cortical outcomes) found higher BMI → lower global cortical thickness (p=0.006). In multivariable MR, body fat % → thinner fusiform cortex. — [PMC10295948](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10295948/)
- A further MR report (up to 23,183 individuals) also found higher BMI linked to lower average global thickness. — [PsyPost summary](https://www.psypost.org/elevated-body-mass-index-might-lead-to-lower-cortical-thickness-study-finds/) (secondary source; the primary paper was not retrieved)
- **Opel 2021 PRS.** Obesity PRS was linked to lower left lateral occipital surface area (B=−45.92, FDR p=0.041, n=3,526). The PRS explained 1.2–1.8% of BMI variance. Left lateral orbitofrontal thickness mediated the PRS→BMI association (supplementary). — [Opel 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8589644/)
- **Bariatric surgery.** After sleeve gastrectomy, Michaud et al. (NeuroImage 2020) found widespread increases in GM and WM density, larger at 12 months and linked to weight loss and metabolic improvement. They describe this as "recovery". An earlier study (Tuulari) found global WM density increases and limited GM increases in occipital/temporal regions at 6 months. Rullmann (gastric bypass) found that only weight loss predicted GM density change, including in the striatum. A 5-patient study found cortical thickness increases with greater excess weight loss. — [Michaud 2020, PMC6994381](https://pmc.ncbi.nlm.nih.gov/articles/PMC6994381); [Frontiers Hum Neurosci 2019](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2019.00290/pdf)
- **Rotterdam (longitudinal).** Body composition did not predict *change* in brain volumes. — [Frontiers in Neurology 2019](https://www.frontiersin.org/articles/10.3389/fneur.2019.00559)

### Inferences
- For an HCP-YA (aged 22–35) FreeSurfer study, Chiesa's head-size result means it matters whether ICV is a covariate or regional measures are expressed relative to ICV. Present both raw and ICV-adjusted models.
- Weight-loss studies support some reversibility, but they are small, use VBM density rather than FreeSurfer thickness, and have no proper control arms.

### Gaps
- Chiesa per-SD β values and regional detail (the PMC fetch hit a CAPTCHA).
- No large longitudinal FreeSurfer weight-change cohort was retrieved.
- Sample sizes for the bariatric studies were not captured.

## Q3. Nonlinear / U-shaped associations, sex differences, age interactions

### Takeaway
Age amplifies the BMI–thickness association: ENIGMA found steeper age-related frontal and orbitofrontal thinning in obese participants. Sex differences are consistent, with stronger effects in men in both ENIGMA and UK Biobank. No large adult study clearly shows a U- or inverted-U-shaped BMI–thickness relationship. Nonlinear evidence comes only from smaller Korean cohorts, mostly involving WHR, underweight, or older age.

### Cited Findings
- **Age × obesity (ENIGMA).** Significant for thickness in the L rostral middle frontal, L lateral orbitofrontal, L pars orbitalis and pars triangularis, driven by faster age-related thinning in obese participants. Also significant for R hippocampal volume, L thalamic volume and R precuneus area. Effect sizes are not in the main text. — [Opel 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8589644/)
- **Sex × BMI (ENIGMA).** Significant for thickness, volume and area. The most consistent pattern was greater BMI-related thinning in **males**. — [Opel 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8589644/)
- **Sex (UK Biobank).** Body fat was linked to subcortical GM (all structures except the amygdala) in men, but only to the pallidum in women. — [RSNA](https://www.rsna.org/en/news/2019/April/obesity-linked-structure-brain)
- **Age (meta-analysis).** VBM effects were weaker in samples with mean age ≥40. — [Chen 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7509458)
- **Nonlinear.** Korean adults aged 45+ (n=1,777): WHR had an inverted-U relationship with total and frontal thickness in men and none in women. Body fat was positively and abdominal fat negatively related to thickness in men. — [PubMed 25626634](https://pubmed.ncbi.nlm.nih.gov/25626634); [SKKU record](https://pure.skku.edu/en/publications/association-of-body-fat-percentage-and-waist-hip-ratio-with-brain/)
- In older Korean men (GAM models), underweight participants showed thinning, while overweight and mildly obese participants had *greater* thickness in some regions. — [Yonsei repository](https://ir.ymlib.yonsei.ac.kr/handle/22282913/156923)
- Young adults (n=202, 2016): no global BMI–thickness association, only some regional effects. — [Int J Obes 2016 PDF](https://link.springer.com/content/pdf/10.1038/ijo.2016.42.pdf)

### Inferences
- For HCP-YA (young, narrow age range), expect weaker effects than ENIGMA's mixed-age sample, which is driven by older obese participants. Test BMI×sex, and expect stronger effects in males. A quadratic BMI term or spline is worth testing given the underweight thinning and nonlinear WHR findings, but no large adult study supplies a firm benchmark.

### Gaps
- No UK Biobank study testing quadratic or spline BMI terms on thickness or area was found.
- Interaction effect sizes are not reported in Opel's main text.

## Q4. ABCD children (separate subsection)

### Takeaway
In 9–11-year-olds, higher BMI goes with thinner cortex, especially in the prefrontal and orbitofrontal cortex. Thickness partly mediates the BMI–executive-function link. Generation R (Rotterdam children) reported the opposite direction (positive), so the pediatric findings are not uniform.

### Cited Findings
- **Laurent JA et al., JAMA Pediatrics 2020;174(2):170–177.** N=3,190 ABCD children (mean age 10.0; 51% male). A nested cross-validated GLM linked higher BMI to lower thickness, most strongly in the prefrontal cortex. Prefrontal thickness partly mediated the BMI association with 1 of 4 executive-function tasks (list-sorting working memory). Cross-sectional. — [JAMA Pediatrics abstract](https://jamanetwork.com/journals/jamapediatrics/article-abstract/2756127); [UVM news](https://www.uvm.edu/news/story/uvm-study-obesity-could-affect-brain-development-children)
- **Ronan L, Alexander-Bloch A, Fletcher PC. Cerebral Cortex 2020;30(4):2519–2528. DOI 10.1093/cercor/bhz257.** About 2,700 children aged 9–11 from ABCD release 1.0. FreeSurfer 5.3, Desikan-Killiany atlas. Covariates were age, sex, race, parental education, income, birth weight, motion, total brain volume, DHEA and physical activity, with FDR correction. BMI-z was negatively linked to thickness in the bilateral lateral OFC, pars orbitalis, pars triangularis, rostral middle frontal and superior frontal cortex, the L entorhinal cortex, and the R medial OFC and temporal pole. In the DHEA-adjusted subset only the rostral middle frontal survived (β=−0.13). BMI-z was not linked to total brain volume. Thickness in 11 regions partly mediated BMI→executive function (β=−0.05). — [Ronan 2020, PMC7175011](https://pmc.ncbi.nlm.nih.gov/articles/PMC7175011/)
- **Chiesa 2024 (ABCD arm, n=6,996).** High BMI at age 10 already shows the volume pattern seen in adults. — [UK Biobank record](https://www.ukbiobank.ac.uk/publications/childhood-adiposity-underlies-numerous-adult-brain-traits-commonly-attributed-to-midlife-obesity/)
- **Generation R (Rotterdam, aged 9–11).** BMI-SDS was *positively* and linearly linked to cortical thickness in several regions. — [Search summary of Generation R record](https://vufind-test.katalog.k.utb.cz/SummonRecord/FETCH-LOGICAL-c473t-e34f622ab55c26c4b938eb8acc42742a64c3cefc7f25be3c8ad467f0f7a536a83) (secondary; the primary paper was not retrieved)

### Inferences
- The prefrontal/OFC thickness pattern in ABCD matches the adult VBM OFC/mPFC convergence. This supports OFC and rostral middle frontal as a priori ROIs for the HCP study.

### Gaps
- Laurent's regional effect sizes were not retrieved, and Ronan's regional β values are in figures only.
- Generation R citation details are unverified.
