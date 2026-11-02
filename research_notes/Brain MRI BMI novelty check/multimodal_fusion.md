# Multimodal brain MRI fusion for predicting BMI / obesity / adiposity

Scope: studies from 2015 to 2026, preprints included, that predict BMI, waist, body fat or obesity status from brain MRI, with a focus on combining two or more modalities. Single-modality BMI predictors are listed as baselines. Searched on 2026-11-01 with web search, Europe PMC REST abstracts and full text (PMC7643372, PMC8203627), and the GigaScience PDF of Bachmann 2025, which I parsed locally. Coverage limit: about 17 tool calls. Treat absence of evidence here as "not found in this pass", not as proof that no study exists.

## Q1. Which multimodal BMI prediction studies exist, and what are their designs and performance?

### Takeaway
Only a handful of studies truly fuse two or more MRI modalities to predict BMI or obesity: Park 2015 (DTI + rs-fMRI, small sample), Adise 2021 (ABCD children; sMRI + DTI + rs-fMRI + task fMRI, each modelled separately) and Bhatt 2023 (sMRI + rs-fMRI + DTI, obesity classification, n=183). None of them is in HCP-YA or HCP-Aging, none uses T1w/T2w myelin maps or perfusion as fused predictors, and none runs a formal stacking or deep-fusion test of whether modalities add to each other. This looks like an open niche.

### Cited Findings
- **Park, Seo, Yi & Park 2015, PLoS ONE.** Combined DTI connectivity with rs-fMRI connectivity. Features were selected from group differences between healthy-weight and non-healthy-weight subjects: "Six DTI-driven connections and 10 rs-fMRI-driven connectivities". These were fed into partial least-squares regression to predict BMI, with "percent error 15.0%". DTI features "better reflected group-wise differences" than rs-fMRI features. Fusion method: feature concatenation into PLSR. No correlation or R² is reported in the abstract. — [Europe PMC / PLoS ONE](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0141376); [PMC4633033](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4633033/)
- **Adise et al. 2021, Developmental Cognitive Neuroscience (ABCD, 9–10 years old; children, so reported separately).** Inputs were sMRI (thickness, area, subcortical volume), DTI, rs-fMRI, and task fMRI (reward, inhibitory control, working memory). The method was cross-validated elastic net with a train/test split. Each modality was modelled separately; no joint fusion model is reported in the abstract.
  - Structural + DTI: "explained 35% of the variance in the training set and generalized well to the test set (R² = 0.27)".
  - rs-fMRI: R²train = 0.21, R²test = 0.14.
  - Working-memory activation: R²train = 0.20, R²test = 0.16.
  - Reward and inhibitory-control tasks were unrelated to BMI.
  - Pathological weight gain one year later: predicted only by structure (AUCtrain = 0.83, AUCtest = 0.83), "but not by fMRI nor rsfMRI".
  - — [Adise 2021, DCN](https://www.sciencedirect.com/science/article/pii/S1878929321000396); [DOAJ record](https://doaj.org/article/31d59fb084ad466fa51bf2c316493b42)
- **Bhatt, Todorov, Sood, …, Jahanshad & Gupta 2023, Brain Communications ("Integrated multimodal brain signatures predict sex-specific obesity status").** Combined structural, resting-state functional and diffusion MRI with clinical and questionnaire data. Classified high BMI against normal BMI separately by sex. N=183 (78 high-BMI, 105 non-obese). The search results did not give classification accuracy or AUC. — [ResearchGate](https://www.researchgate.net/publication/356175686_Integrated_Multimodal_Brain_Signatures_Predict_Sex-Specific_Obesity_Status); [UCLA Health release](https://www.uclahealth.org/news/men-and-women-have-different-obesity-drivers-pointing-need); [UCLA CNS](https://uclacns.org/?p=11875)
- **Park BY et al. 2021, Communications Biology (HCP-YA, n=325).** Not a predictive fusion model, but a multimodal control analysis. BMI associations with functional connectome gradients were tested while controlling for MRI-derived morphology and microstructure. Separate univariate findings:
  - Cortical thickness: r = −0.21 in the temporal pole.
  - Myelin proxy (T1w/T2w): r = −0.35 in occipital, central and ventrolateral PFC regions, both FDR < 0.05.
  - Module degree: r = 0.20. Participation coefficient: r = −0.12.
  - — [Comm Biol 2021](https://www.nature.com/articles/s42003-021-02268-x); [PMC8203627 full text via Europe PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8203627)

**Single-modality BMI predictors (baselines a fusion model would need to beat):**
- **Park BY, Byeon K, …, Dagher A, Park H 2020, Human Brain Mapping (rs-FC degree centrality; n≈2,400 across four cohorts).** Elastic net with "five-fold cross-validation using strictly separated training and test data". The pattern was developed in UK Biobank and tested on independent cohorts. Correlations between the FC pattern score and the phenotype (Table 2):
  - UKB (n=1,497, development): BMI r = 0.265, waist circumference r = 0.308, waist-to-hip ratio r = 0.236.
  - **HCP (n=587, validation): BMI r = 0.146.**
  - eNKI-RS (n=276): BMI r = 0.150, waist r = 0.169.
  - SVH (n=30): BMI r = 0.463.
  - A pattern trained on eNKI generalized poorly; for example, HCP BMI r = 0.003.
  - Motion handling: volumes with FD > 0.5 mm were removed, plus ICA-FIX.
  - — [PMC7643372 full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC7643372); [HBM DOI 10.1002/hbm.25167](https://zendy.io/title/10.1002/hbm.25167)
- **Wang J, Dong D, …, Qiu J, Chen H 2023, Cerebral Cortex 33(13):8368–8381 (rs-FC only).** Predicted four phenotypes (body fat %, BMI, waist circumference, waist–height ratio) in three datasets (n = 2,992). Reports "good generalizability to longitudinal and independent datasets". The predictive pattern centered on visual cortex, visual–IPL, visual–orbital and amygdala–orbital connections. The abstract does not give the exact r or AUC, and I did not retrieve the full text, so the HCP status of the cohorts is unverified. — [Cerebral Cortex](https://academic.oup.com/cercor/article/33/13/8368/7109831); [BVS record](https://pesquisa.bvsalud.org/portal/resource/en/mdl-37032621)
- **Bachmann et al. 2025, GigaScience (HCP-YA, task and rest FC).** Details in Q2. — [GigaScience PMC11899596](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11899596/)
- **Vakli et al. 2020, Frontiers in Neuroinformatics (T1w 3D CNN with age and sex as inputs).** Reports that BMI "can be accurately predicted". The abstract gives no numeric metric. Localization maps highlighted the caudate and amygdala. — [Frontiers](https://www.frontiersin.org/articles/10.3389/fninf.2020.00010)
- **Cooper, Elsayed, Owens & MacKillop 2025, bioRxiv preprint (T1w 3D-CNN, n=1,106 adults).** Lockbox (held-out) R² = 0.325 for the 3D-CNN, against R² < 0.07 for random forest, elastic net and TabNet. — [bioRxiv 2025.04.11.648433](https://www.biorxiv.org/content/10.1101/2025.04.11.648433v1)
- **Finkelstein et al. 2024, Human Brain Mapping (DIRECT-PLUS trial; ensemble deep learning on T1w).** Brain-predicted BMI fell with actual weight loss over an 18-month lifestyle intervention. The search results gave no numeric accuracy. — [HBM 10.1002/hbm.26595](https://aminer.org/pub/65d5140c939a5f40826269b5/deep-learning-based-bmi-inference-from-structural-brain-mri-reflects-brain-alterations)
- **UK Biobank transfer learning on vertex-wise cortical shape (SPIE 2020).** Normal vs overweight/obese classification accuracy was 65.6 ± 0.7% (transfer) and 62.7 ± 0.7% (direct). — [ADS](https://ui.adsabs.harvard.edu/abs/2020SPIE11583E..09Z/abstract)

### Inferences
- True multimodal BMI prediction in adults is limited to small samples: Park 2015 has a small n with group-difference feature selection, which is likely leaky, and Bhatt 2023 has n=183. The largest multimodal BMI study (Adise 2021) is in children and models each modality separately.
- Out-of-sample performance from rs-FC alone in independent cohorts is modest (r ≈ 0.15 in HCP when trained on UKB). sMRI in ABCD reaches a test R² of 0.27 (r ≈ 0.52).

### Gaps
- I could not retrieve Wang 2023 full-text metrics, Bhatt 2023 accuracy, or Vakli 2020 MAE/r. Those need a full-text pull.
- I found no BMI study in HCP-Aging, multimodal or otherwise, in this pass.
- I found no study that fuses perfusion (ASL) or T1w/T2w myelin maps as predictors of BMI. Park 2021 used myelin only univariately.

## Q2. What is the best reported BMI prediction performance in HCP-YA, and how much does head motion explain?

### Takeaway
The highest reported HCP-YA figure is Bachmann 2025: task-general (averaged across all tasks) cerebellocerebral FC CPM, r = 0.70. Its confound handling is incomplete: it regressed gender, age and ethnicity at the edge-selection stage, but did not regress head motion (FD), even though motion is known to correlate with BMI. The motion-explained share of this r is therefore unknown and may be substantial. More conservative HCP figures are rs-FC r = 0.44 (Bachmann) and r = 0.146 for an externally trained pattern (Park 2020).

### Cited Findings
- **Bachmann et al. 2025, GigaScience 14:giaf010 (from the PDF text):**
  - Data: HCP-YA S1200 MSMAll; N ranges from 999 (rs-fMRI) to 1,077 (gambling); 999 subjects had all tasks; median BMI 25.4 (IQR 22.8–29.1).
  - CV: CPM with k = 128 folds and an edge threshold of p < 0.05. Gender, age and ethnicity were regressed out during edge selection. "We took care to remove siblings from each fold before model building, thus ensuring that closely related subjects did not predict each other's BMI." The wording is ambiguous about whether this is a full family-grouped split.
  - Significance: permutation tests (10,000 for task, 2,000 for rest).
  - Head motion: only FLIRT motion correction in preprocessing. No FD covariate or motion regression in CPM was found in the text.
  - FC estimation: tangent-space FC with Ledoit-Wolf shrinkage.
  - Results:
    - rs-fMRI cerebellocerebral: r = 0.44.
    - Whole-brain rs-FC vs restricted: "r = 0.44 vs. 0.40" in the Results section. The Discussion phrases it as whole-brain "not much better (Pearson's r = 0.40 vs. 0.44)". These two passages contradict each other on which value belongs to which model.
    - Task contrasts (e.g. 2-back minus 0-back): "generally low and not significant".
    - Per-task averaged-condition FC: r = 0.59 (emotion), 0.61 (relational), 0.62 (language, social, WM).
    - Task-general (all tasks averaged): **r = 0.70, P ≤ 0.001**.
  - No held-out test set: the pooled r is computed across CV predictions.
  - — [GigaScience PMC11899596](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11899596/); [PDF](https://rcastoragev2.blob.core.windows.net/7ea2b8add9422c6aa31744481a12acd6/giaf010.pdf)
- **Park 2020 HBM:** a UKB-trained rs-FC pattern applied to HCP (n=587) gave BMI r = 0.146. — [PMC7643372](https://pmc.ncbi.nlm.nih.gov/articles/PMC7643372)
- **Park 2021 Comm Biol (HCP, n=325):** "head motion was found to be related to BMI, in a rather complex way"; "additionally controlling for head motion parameters … increased the effect sizes in several networks but reduced effect sizes in the frontoparietal network". The paper cites "Weight loss reduces head motion: Revisiting a major confound in neuroimaging". — [PMC8203627](https://pmc.ncbi.nlm.nih.gov/articles/PMC8203627)
- **Siegel et al. 2017, Cerebral Cortex (HCP):** head motion is "a likely source of systematic bias in measured connectivity–behavior relationships", and data cleaning "can substantially change previously reported relationships". I did not confirm the exact BMI–FD correlation from the snippets. — [PMC6410500](https://pmc.ncbi.nlm.nih.gov/articles/PMC6410500); [WUSTL profile](https://profiles.wustl.edu/en/publications/data-quality-influences-observed-links-between-functional-connect/)
- A separate study found high-frequency motion is "more prominent in older individuals and those with a higher body mass index" in slower-TR datasets. — [PMC7308220](https://pmc.ncbi.nlm.nih.gov/articles/PMC7308220) (attribution from the search snippet; not verified in full text)

### Inferences
- Bachmann's r = 0.70 is unusually high for any HCP behavioral or physical phenotype prediction. Rest is r = 0.44 and an externally trained FC pattern gives r ≈ 0.15. Plausible inflators:
  - FD was not regressed, and BMI–motion coupling is documented.
  - Averaging task FC may amplify motion-related or physiological (respiration, cardiac) signal shared across tasks.
  - There is no locked holdout.
  - Sibling handling is ambiguous.
- Any new HCP-YA BMI result should report performance with FD partialled from the target, or FD-matched, and use family-grouped CV. Without that it is not comparable to Bachmann's figure.

### Gaps
- I did not find the exact BMI–mean-FD correlation in HCP-YA from Siegel 2017. It needs a full-text check.
- I found no paper that re-analyzes Bachmann's r = 0.70 with motion control.
- I could not find a separate "Park 2020" HCP BMI prediction paper beyond the HBM 2020 FC paper. If the user meant another paper, its title is needed.

## Q3. Has anyone shown that combining structure and function adds over either alone for BMI? Is there multimodal deep learning for BMI?

### Takeaway
No study found here formally shows incremental value of fusing structure and function for BMI prediction. The closest evidence is mixed:
- Adise 2021 (children): structure beat function, and only structure predicted weight gain.
- Park 2021: BMI–FC gradient associations were "virtually unchanged" after controlling for morphology and microstructure, which implies partly non-overlapping signal.
- Ooi 2022 (general behavior, BMI not included): fusion helped only cognition.

I found no multimodal deep learning model for BMI. Deep learning work on BMI is T1w-only.

### Cited Findings
- Adise 2021 (ABCD): structural + DTI test R² = 0.27, against rs-fMRI 0.14 and WM-task 0.16. Structure alone predicted weight gain (AUC 0.83). — [DCN 2021](https://www.sciencedirect.com/science/article/pii/S1878929321000396)
- Park 2021: BMI–connectome-manifold associations held when controlling for MRI-derived morphology and microstructure indices. — [Comm Biol 2021](https://www.nature.com/articles/s42003-021-02268-x)
- Ooi et al. 2022, NeuroImage 263:119636 (HCP n=753 + ABCD):
  - Compared anatomical T1, diffusion, rest FC and task FC using KRR, LRR and elastic net.
  - "Functional connectivity models performed best" in both datasets.
  - Combining modalities helped cognition but not other behavioral domains.
  - The extracted text did not list BMI among the targets.
  - — [bioRxiv 2022.03.08.483564](https://www.biorxiv.org/content/10.1101/2022.03.08.483564.full.pdf); [DOAJ](https://doaj.org/article/c23f5da921b94686ac7743315e8517f3)
- Deep learning for BMI is T1w-only:
  - Cooper 2025 preprint: 3D-CNN, lockbox R² = 0.325, n = 1,106. — [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.04.11.648433v1)
  - Vakli 2020: CNN. — [Frontiers](https://www.frontiersin.org/articles/10.3389/fninf.2020.00010)
  - Finkelstein 2024: ensemble deep learning. — [aminer](https://aminer.org/pub/65d5140c939a5f40826269b5/deep-learning-based-bmi-inference-from-structural-brain-mri-reflects-brain-alterations)
  - A targeted search found no study fusing DTI and fMRI with deep learning for BMI in 2024–2025. — [search result summary; bioRxiv Cooper 2025](https://www.biorxiv.org/content/10.1101/2025.04.11.648433v1)

### Inferences
- A rigorous HCP-YA or HCP-A study has not been done. It would need:
  - stacked or concatenated T1w morphometry, T1w/T2w myelin, rest FC and task FC;
  - family-grouped CV plus a locked holdout;
  - age, sex and FD handling;
  - a formal paired test of fusion against the best single modality.
- That study appears novel. A positive "fusion adds" result would be a genuine contribution, and a null result would still be informative given Ooi 2022.
- Given Cooper's T1w 3D-CNN R² = 0.325 and Adise's sMRI R² = 0.27, structure may be a stronger BMI channel than rest FC. The structure-vs-function ranking in HCP-YA, where Bachmann reports task FC r = 0.70, is unresolved and probably sensitive to motion.

### Gaps
- I did not verify whether Ooi 2022 supplementary material includes BMI or another anthropometric target.
- I found no multimodal DL (e.g. graph fusion, cross-attention) for BMI or adiposity in any cohort.

## Q4. Large-scale multi-phenotype imaging prediction papers that include BMI: what accuracy do they report?

### Takeaway
I could not confirm BMI-specific accuracy figures from the large "predict many phenotypes" papers (Dadi 2021, Cole 2020, Tian & Zalesky, Schulz 2020, Ooi 2022) in this pass. The searches show these papers target mental health, age or cognition. Where BMI appears (Tian 2023), it is an input to body-age models rather than a target predicted from the brain.

### Cited Findings
- Dadi et al. 2021, GigaScience ("Population modeling with machine learning can enhance measures of mental health"; UKB multimodal MRI + sociodemographics): targets were age-delta, fluid intelligence and neuroticism proxies. BMI was not found as a target in the search summary. — [typeset PDF](https://typeset.io/pdf/population-modeling-with-machine-learning-can-enhance-3yqc6kojr7.pdf); [PMC8559220](https://pmc.ncbi.nlm.nih.gov/articles/PMC8559220)
- Tian, Zalesky et al. 2023, Nature Medicine: built organ age-gap models for 7 body systems and 3 brain systems in UKB (body n = 143,423; brain n = 36,901). BMI is an input musculoskeletal or body phenotype, not predicted from the brain. — [Nature Medicine PDF](https://www.nature.com/articles/s41591-023-02296-6.pdf); [medRxiv](https://medrxiv.org/content/10.1101/2022.09.03.22279337v2.full.txt)
- Schulz et al. 2020, Nature Communications (UKB scaling of linear vs deep models): found "neither saturation of accuracy … with increasing sample size nor performance gains from kernel models". The BMI-specific number was not retrieved. — [Nat Commun](https://www.nature.com/articles/s41467-020-18037-z)
- Vertex-wise grey-matter morphometricity in UKB: body size, including BMI, accounts for a "substantial proportion" of morphometricity, a potential confound for case-control MRI findings. — [UKB publication page](https://www.ukbiobank.ac.uk/publications/a-unified-framework-for-association-and-prediction-from-vertex-wise-grey-matter-structure/)
- Ooi 2022 (HCP/ABCD): BMI not identified among targets (see Q3). — [bioRxiv](https://www.biorxiv.org/content/10.1101/2022.03.08.483564.full.pdf)

### Inferences
- The large multi-phenotype benchmark papers have mostly not reported BMI as a brain-predicted target, or I could not find their BMI numbers. That supports the novelty of a dedicated multimodal BMI benchmark.
- The UKB morphometricity finding suggests T1w-derived features carry strong BMI signal. Any multimodal model should report the T1w-only baseline.

### Gaps
- I did not find Cole 2020 (UKB multimodality brain age) BMI prediction accuracy; it is likely an association with brain-age gap rather than a prediction.
- I did not check whether the Miller 2016 / Smith UKB IDP-by-non-IDP association papers report a BMI prediction r.
- I found no ABCD multi-phenotype paper (beyond Adise 2021) that reports a BMI prediction figure.
- These gaps need targeted full-text checks of supplementary tables, which I did not do within the tool budget.
