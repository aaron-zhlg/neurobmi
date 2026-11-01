# Resting-state functional connectivity (rs-FC) and obesity / BMI

Scope: mostly adults; ABCD (children) has its own subsection. Numbers come only from the sources fetched. Anything I could not verify is marked UNKNOWN or listed under Gaps. Search date: 2026-11-01.

## Q1. What do reviews and meta-analyses conclude about which networks and connections relate to BMI?

### Takeaway
The three reviews broadly agree. Obesity and overweight go with weaker default mode network (DMN) and executive control network (ECN) connectivity, stronger salience network (SN) connectivity, stronger hypothalamus connectivity to reward, limbic and salience regions (and weaker to cognitive regions), stronger orbitofrontal (OFC) and weaker insula connectivity, and lower graph efficiency. The reviews also flag that methods vary widely across the primary studies.

### Cited Findings
- **Syan SK et al., 2021**, *Neurosci Biobehav Rev* 131:270–292, DOI 10.1016/j.neubiorev.2021.08.019, PMID 34425125. Systematic review of **29 studies** comparing overweight/obese adults with healthy-BMI controls. Findings:
  - obesity/overweight is consistently linked to DMN hypoconnectivity and SN hyperconnectivity;
  - hypothalamus shows increased connectivity with reward, limbic and salience regions and decreased connectivity with cognitive regions;
  - signal power is higher in regions tied to inhibition and emotion;
  - nodal efficiency, degree centrality and global efficiency are lower.
  - [PubMed 34425125](https://www.pubmed.gov/34425125/); [McMaster record](https://experts.mcmaster.ca/display/publication2104988)
- **Parsons N et al.**, *Rev Endocr Metab Disord* 2022;23(4):861–879 (online June 2021; databases disagree on whether it is 2021 or 2022), DOI 10.1007/s11154-021-09665-x. Findings:
  - consistently **increased OFC** and **decreased insula** rs-FC in obesity versus healthy weight;
  - increased BOLD amplitude, mainly in subcortical regions (hippocampus, amygdala, putamen);
  - results framed around a triadic model of reward, inhibitory and homeostatic systems.
  - [DOI](https://doi.org/10.1007/s11154-021-09665-x); [ACU record](https://acuresearchbank.acu.edu.au/item/8z34y/a-systematic-review-of-resting-state-functional-connectivity-in-obesity-refining-current-neurobiological-frameworks-and-methodological-considerations-moving-forward)
- **Donofry SD et al., 2020**, *Social Cognitive and Affective Neuroscience*. A review, not a meta-analysis as far as the snippet shows. The rs-FC alterations reported most often are in the ECN, SN and DMN, with obesity linked to weaker ECN connectivity. Exact title, DOI and the number of studies covered could not be verified from the snippet. [core.ac.uk PDF](https://core.ac.uk/download/363492922.pdf)
- **Kullmann S et al., 2014**, *Hum Brain Mapp*. Seed-based analysis of medial (MH) and lateral hypothalamus connectivity: n = 49 normal-weight adults, plus a separate normal-weight versus overweight/obese comparison. Overweight/obese participants showed higher FC with the OFC and nucleus accumbens within the MH network. [PMC6869436](https://pmc.ncbi.nlm.nih.gov/articles/PMC6869436)
- **Hypothalamus seed study, *Int J Obes* 2019/2020** (authors UNKNOWN from the snippet), n = 105 healthy adults. BMI correlated positively with hypothalamic rs-FC to the insula, thalamus, globus pallidus and cerebellum, and negatively with hypothalamic rs-FC to the superior parietal lobule. [Nature IJO s41366-019-0496-8](https://www.nature.com/articles/s41366-019-0496-8)
- **Contreras-Rodríguez O et al., 2017**, *Sci Rep*. Excess weight was linked to increased MH–striatum and MH–subgenual ACC connectivity, and decreased MH connectivity with the middle frontal gyrus and the bed nucleus of the stria terminalis (BNST). [UB repository](https://diposit.ub.edu/dspace/handle/2445/124385)

### Inferences
- The recurring "triad" is reward/OFC/striatum hyper-connectivity, executive control/DMN hypo-connectivity, and hypothalamic coupling shifted toward reward and away from cognitive regions. This is the prior to test against in HCP-YA.
- Most primary studies in these reviews are small seed-based case-control designs. The reviews did not systematically grade how motion was controlled, so the shared conclusions may carry motion-related bias (see Q2).

### Gaps
- I found no formal coordinate-based meta-analysis (ALE/SDM) of rs-FC in obesity. Donofry 2020 appears to be a narrative or systematic review. The full texts of Syan and Parsons were not retrieved, so I could not extract how many of the included studies used FD-based censoring or controlled for motion.

## Q2. How confounded is the BMI–FC link by in-scanner head motion? (Siegel 2017, Beyer 2017, Hodgson 2017)

### Takeaway
Of all non-imaging traits tested, BMI is the one most strongly tied to head motion. In HCP, Siegel et al. report r = 0.66 between BMI and FD, the largest of 23 motion-correlated measures. The link is partly genetic. Within-subject motion effects look like between-subject "trait" effects, so BMI–FC results are vulnerable unless motion is strictly controlled. Some findings survive, for example Beyer's posterior DMN result after motion-matching.

### Cited Findings
- **Siegel JS, Mitra A, Laumann TO, Seitzman BA, Raichle M, Corbetta M, Snyder AZ.** "Data quality influences observed links between functional connectivity and behavior." *Cereb Cortex* 2017;27(9) (online Aug 2016), PMID 27550863, PMC6410500.
  - Data: HCP Q3; 457 subjects analysed, main results on 284.
  - **BMI–motion correlation r = 0.66** (Table 1), the highest of 23 measures that correlated with motion. Weight r = 0.52, systolic BP r = 0.23. The authors suggest the BMI–FD link may be partly mediated by respiratory effort.
  - "Type B" cleaning:
    - FD computed with a 50 mm head radius, 0.3 Hz low-pass filtered, and thresholded at 0.025 mm;
    - DVARS threshold at 105% of the run median;
    - censored frames interpolated before bandpass filtering at 0.009–0.08 Hz;
    - runs with fewer than 400 of 1200 frames left were dropped;
    - an average grey-matter regressor was included (effectively GSR), plus white-matter and ventricle regressors.
  - Effect of cleaning: Type B removed nearly all FC:behaviour relations seen with minimal "Type A" cleaning. The motion influence on FC:behaviour fell from r = 0.50 to about 0. The correlation between cross-subject and within-subject motion effects fell from 0.643 to 0.03. For IQ, the motion influence went from r = −0.31 (P = 0.008) to −0.14 (P = 0.129). The authors note that some confounding remains even after Type B cleaning.
  - [PMC6410500](https://pmc.ncbi.nlm.nih.gov/articles/PMC6410500)
  - Caveat: r = 0.66 was extracted by the fetch tool from Table 1. Check it against the PDF before quoting, because it is high compared with the BMI–FD correlations usually reported.
- **Beyer F et al., 2017.** "Higher body mass index is associated with reduced posterior default mode connectivity in older adults." *Hum Brain Mapp* 38(7):3502–3515, DOI 10.1002/hbm.23605, PMID 28397392, PMC6867016.
  - Sample: LIFE-Adult (Leipzig), N = 712 healthy adults aged 60–80 (main n = 521, replication n = 191). Mean BMI 27.6 ± 4.2; BMI range UNKNOWN.
  - Methods: group ICA (18 RSN components) followed by dual regression, a multivariate model-selection step, then univariate models with FDR p < 0.05.
  - Results: higher BMI was linked to lower DMN connectivity in the PCC/precuneus (components 29 and 42) and higher connectivity in a visual network (component 25).
  - Motion: BMI correlated positively with mean FD. In a **motion-matched subsample** that correlation was much smaller, and the DMN effect held. The effect also held after adjusting for age, sex, head motion, registration quality, cardiovascular and genetic factors, and it replicated in the independent subsample.
  - Lower connectivity in the BMI-related regions was weakly associated with worse executive function. Numeric FD values and the BMI–FD r were not available in the material retrieved.
  - [PubMed](https://pubmed.ncbi.nlm.nih.gov/28397392/); [NeuroVault collection 2143](https://neurovault.org/collections/2143/)
- **Hodgson K et al., 2017**, *Cereb Cortex*, "Shared genetic factors influence head motion during MRI and body mass index," PMID 27744290. Data: Mexican-American extended pedigrees (n = 689) plus HCP. Head motion is heritable, and of all traits it is most strongly correlated with BMI, with evidence of shared genetic influence in both datasets. [PubMed 27744290](https://pubmed.ncbi.nlm.nih.gov/27744290/); [PDF](https://www.Gwern.net/doc/genetics/heritable/correlation/2016-hodgson.pdf)
- A preregistered bariatric-surgery rs-FC study (medRxiv 2021) cites a consistent link between higher BMI and more rs-fMRI motion. It concludes that weight-loss effects on FC may be confounded by motion and that rigorous motion correction is needed in overweight samples. [medRxiv 2021.04.01.21254543](https://medrxiv.org/content/10.1101/2021.04.01.21254543v1.full-text)

### Inferences
- For HCP-YA, BMI and FD will be substantially correlated. Plain FD-as-covariate regression may both under- and over-correct, because FD is partly a downstream marker of BMI (respiration, shared genetics). Report results under several strategies: ICA-FIX ± GSR, scrubbing, FD covariate, and a motion-matched or low-motion subsample. Also report the edge-level QC-FC correlation (FC vs FD) next to the BMI-FC correlation.
- Respiration is a plausible mediator. That argues for respiratory-artifact-aware denoising (GSR or physiological regressors) in addition to rigid-body motion regressors.

### Gaps
- No paper found quantifies how much each review-level network finding shrinks under strict motion control.
- I did not find a systematic multiverse study across denoising pipelines specifically for BMI–FC.

## Q3. Large-cohort and whole-brain connectome / ML evidence in adults (UK Biobank, HCP, others)

### Takeaway
Whole-brain connectome models do predict adiposity, but the effects are modest: about r = 0.1–0.3 out-of-sample across cohorts, and about 0.4–0.5 in better-controlled within-cohort CV. Reward and prefrontal regions (vmPFC/OFC, pallidum, insula, NAcc) load positively. Sensory and visual regions load negatively or form part of the predictive set.

### Cited Findings
- **Park B, Byeon K, Lee MJ, …, Morys F, Bernhardt B, Dagher A, Park H, 2020.** *Hum Brain Mapp* 41(17):4912–4924, DOI 10.1002/hbm.25167, PMID 32804441.
  - Data: discovery in UK Biobank (n = 1,497; age about 40–70; mean BMI 29.61 ± 3.97). Validation in HCP (n = 587), eNKI-RS (n = 276) and SVH (n = 30); about 2,400 participants in total.
  - Methods: Brainnetome 246 parcellation; ridge-regularised partial correlation (FSLNets, rho = 0.5); soft threshold β = 6; degree centrality; elastic net predicting waist circumference.
  - Denoising: ICA-FIX in all cohorts. GSR not mentioned. Volumes with FD > 0.5 mm removed in eNKI/SVH only. UKB and HCP relied on their standard pipelines, with no subject-level FD exclusion described and FD not reported as a covariate.
  - Performance: training CV r = 0.275; held-out r = 0.102. The FC score correlated with BMI at r = 0.265 in UKB, 0.146 in HCP, 0.150 in eNKI and 0.463 in SVH (n = 30).
  - Direction: positive in vmPFC/vlPFC, cingulate, globus pallidus, and in insula and NAcc (Caucasian-only analysis). Negative in precentral, fusiform, ITG, parahippocampal cortex and thalamus.
  - [PMC7643372](https://pmc.ncbi.nlm.nih.gov/articles/PMC7643372)
- **Wang J, Dong D, Liu Y, …, Chen H, 2023.** "Multivariate resting-state functional connectomes predict and characterize obesity phenotypes." *Cereb Cortex* 33(13):8368–8381, DOI 10.1093/cercor/bhad122.
  - Data: discovery in a Chinese cohort (BBP, n = 1,646), internal longitudinal validation (n = 488), external validation in HCP (n = 1,033) and GBB (n = 313).
  - Methods: Brainnetome 246; Pearson correlation with Fisher z.
  - Motion:
    - subjects excluded if mean FD-Power ≥ 0.2 mm (BBP/GBB) or ≥ 0.3 mm (HCP; the 0.2 mm cut would have dropped more than 20% of HCP);
    - spike regression of frames with FD > 0.5 mm plus 1 frame before and 2 after;
    - Friston-24 motion regressors and 5 aCompCor components;
    - **mean FD as a covariate** in feature selection and in a control analysis.
  - Model: relevance vector regression (elastic net and SVR as checks), 10-fold CV repeated 100 times, permutation testing.
  - Performance (r): body-fat % 0.46, **BMI 0.39**, waist circumference 0.40, waist-to-height ratio 0.29; range 0.23–0.50 across schemes, all FDR p < 0.001.
  - Key edges: IPL–visual cortex, orbital gyrus–visual cortex, orbital gyrus–amygdala; also insula, precuneus, basal ganglia and hippocampus.
  - [Cereb Cortex](https://academic.oup.com/cercor/article/33/13/8368/7109831)
- **UK Biobank OFC studies (Rolls ET et al., *SCAN* 2021/2023):** OFC rs-FC, especially with the anterior cingulate, correlated positively with liking for sweet foods and with BMI. N is inconsistent across sources (37,286 in the abstract versus 22,331 imaging participants in the methods), and effect sizes and motion handling were not verified. [PMC10498940](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10498940/)
- **UK Biobank, *Sci Rep* 2020 (n = 13,718):** OFC connectivity varied with the interaction between periventricular white-matter-hyperintensity burden and degree of obesity. [Sci Rep s41598-020-60054-x](https://www.nature.com/articles/s41598-020-60054-x)
- **HCP-YA connectome-based predictive modelling (CPM) of BMI:** cerebellocerebral connectivity predicted BMI, with predictive edges overlapping frontoparietal, somatomotor, salience and default mode networks. Task-general connectivity predicted better than rest alone. Authors, year and r were NOT verified. [arXiv/OUP search result via frontiersin 10.3389/fnins.2023.1096232](https://www.frontiersin.org/articles/10.3389/fnins.2023.1096232/pdf)
- **Park B et al.**, connectome manifold (gradient) learning in 325 healthy young adults: whole-brain functional organisation is associated with BMI and linked to post-mortem gene expression. This is an association study, not a predictive one. [Commun Biol s42003-021-02268-x](https://www.nature.com/articles/s42003-021-02268-x)

### Inferences
- Across UKB and HCP, generalisable out-of-sample r is roughly 0.1–0.4. A realistic HCP-YA target for BMI from rs-FC is r ≈ 0.15–0.4, and the high end needs strict checks that motion is not driving it.
- Brainnetome-246 with ICA-FIX is the most common pipeline in this literature, which makes it a sensible comparable baseline.

### Gaps
- **GNN / deep learning:** I found no peer-reviewed graph neural network or deep-learning connectome study that specifically predicts BMI or obesity. Existing ML work uses elastic net, RVR, SVR and CPM. A search on "graph convolutional network rs-fMRI obesity" was not run within the budget.
- UK Biobank effect sizes and motion handling for the Rolls OFC studies were not retrieved.
- Tangent-space FC estimators have not been used in the obesity papers found so far.

## Q4. ABCD (children, 9–11 y) subsection

### Takeaway
ABCD studies report weaker network topology and connectivity in DMN, salience, control and reward networks with excess BMI, with small effects (Cohen's d 0.07–0.39). Seed results such as putamen–SN and NAcc–frontoparietal are mixed and moderated by sex or race. Motion handling ranges from rigorous (Brooks 2023) to not reported (Assari 2020).

### Cited Findings
- **Brooks SJ, Smith C, Stamoulis C, 2023.** "Excess BMI in early adolescence adversely impacts maturating functional circuits supporting high-level cognition and their structural correlates." *Int J Obes*, DOI 10.1038/s41366-023-01303-7.
  - Sample: N = 4,922 (median age 120 months); 15.0% overweight, 13.7% obese.
  - Methods: 1,088 parcels; graph topology; cross-validated linear regression.
  - Motion: frames with FD > 0.3 mm censored; runs with more than 10% of frames censored excluded; number of censored frames used as a covariate; results reproduced across several run-selection datasets.
  - Results: lower efficiency, resilience, connectivity and clustering in DMN, dorsal attention, salience, control, limbic and reward networks (p ≤ 0.04, d 0.07–0.39). Lower cortico-thalamic efficiency only in the obese group (d 0.09–0.19). Effects were partly mediated by cortical thickness and volume, and partly correlated with fluid reasoning.
  - Sources: PDF text, [NSF PAR](https://par.nsf.gov/servlets/purl/10405260); [IJO](https://springerlink.bibliotecabuap.elogim.com/10.1038/s41366-023-01303-7)
- **Assari S, Boyce S, Bazargan M, 2020.** *Brain Sci* 10:703, DOI 10.3390/brainsci10100703. ABCD release 2.0.1, N = 3,784 (9–10 y), 1-year longitudinal design. Baseline NAcc–frontoparietal rs-FC (ABCD tabulated ROI–network correlation) was inversely correlated with follow-up BMI, adjusting for baseline BMI and SES, and the effect was significant only in girls. **Motion was not mentioned** anywhere in the extracted text. [PDF](https://rcastoragev2.blob.core.windows.net/43435c919ab1d678841409e35584fc6d/PMC7600639.pdf)
- **Putamen–salience network study** (authors and year UNKNOWN), N = 6,473 ABCD children. Higher right putamen–SN connectivity was associated with higher BMI in non-Hispanic White children but not in non-Hispanic Black children. [UTB catalogue record](https://vufind.katalog.k.utb.cz/SummonRecord/FETCH-LOGICAL-c493t-17a2a59b31fd6a8d9d7dc6a5b9203778dc1f08f7ea5dbb10b2a3b26ad222ff403)
- **ABCD news release (RSNA 2022):** higher BMI z-scores were associated with decreased connectivity in cognitive-control and reward networks. [EurekAlert](https://www.eurekalert.org/news-releases/971991)
- **ABCD 2025:** a whole-brain rs-FC factor partly mediates socioeconomic disparities in children's BMI and blood pressure. [PMC11829797](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11829797/)

### Inferences
- Paediatric effects are small (d below 0.4) even at N of about 5,000, which is consistent with the modest adult prediction accuracies. Studies that use ABCD's tabulated FC without their own FD censoring (for example Assari 2020) should be treated as low-confidence given the BMI–motion confound.

### Gaps
- For the putamen–SN and RSNA studies, motion-handling details and effect sizes were not retrieved.
- I found no ABCD study that explicitly reports a BMI–FD correlation.
