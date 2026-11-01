# Machine-learning prediction of BMI / obesity from brain MRI, and methods for brain-phenotype prediction

Scope note: these notes come from web search plus full-text fetches of the PMC versions of Vakli 2020, Bachmann 2025 and Xu 2023. Several full texts were blocked: Wiley returned 403, ScienceDirect returned 403, bioRxiv returned 429 (rate limit), and the Springer and Nature pages redirected to a login. Numbers for those papers come from abstracts or search snippets and are marked that way. Items marked "[prior knowledge, not re-verified]" are bibliographic facts I know but could not check against the source this session. The report writer should treat those as leads to check, not as confirmed.

## Benchmark table: reported BMI prediction performance from brain features

### Takeaway
Held-out performance depends heavily on feature type and N. The most comparable result for a new baseline is HCP-YA (N=1,100) with FreeSurfer-style regional CT, CSA and GMV fed to elastic net. That reached only about 6% held-out R² from sMRI alone, and about 9% when demographics were added. Much larger numbers come from different setups: voxel-level 3D-CNNs (UK Biobank, N≈18k: r=0.70, R²=0.46), connectome CPM on HCP task FC (r up to 0.70, without motion control), and multimodal ABCD children (test R²=0.27).

### Cited Findings

**Summary table (only numbers reported by the sources; "NR" = not reported / not retrieved)**

| Study | Dataset, N | Features | Model | Validation | Confounds | BMI performance |
|---|---|---|---|---|---|---|
| Xu, Owens & MacKillop 2023, *Obesity* 31(11):2799–2808, DOI 10.1002/oby.23880, PMID 37853988 | HCP-YA S1200, N=1,100, age 22–35 (242 with BMI>30) | Regional cortical thickness and surface area, subcortical and brainstem GMV, plus TIV | Elastic net (scikit-learn / Brain Predictability toolbox) | 5-fold CV plus held-out test set, repeated over 10 splits. Nested tuning and family-grouped folds are **not reported** | Demographics (age, sex, income, education) entered as predictors only in Models 2/3. Fold-wise confound regression not described | sMRI only: CV R²=5.57%, held-out R²=6.35%. Demographics only: 4.16% / 2.60%. sMRI + demographics: 10.05% / 8.87%. No r/MAE reported. No permutation test |
| Cooper, Elsayed, Owens & MacKillop 2025 (bioRxiv 10.1101/2025.04.11.648433, **preprint**; later published on ScienceDirect with the title "…dramatically improves cross-validated prediction accuracy of BMI") | HCP-YA, N=1,106 adults | Whole T1 volume (3D-CNN) vs atlas ROI tabular features (volume, thickness, area) | 3D-CNN vs TabNet, elastic net, random forest | Cross-validated (details not retrieved) | NR | 3D-CNN R²=0.325 (from search snippet). Comparator R² values were not retrievable (bioRxiv rate-limited) |
| Vakli, Deák-Meszlényi, Auer & Vidnyánszky 2020, *Front Neuroinform* 14:10, DOI 10.3389/fninf.2020.00010, PMID 32265681 | UK Biobank, N=17,938 (train 13,938 / val 2,000 / test 2,000), age 44–80; transfer to IXI (N=269) | Minimally processed T1 volume | 3D CNN (≈232k params), with/without age+sex inputs | Single random train/val/test split, no k-fold | Age/sex as inputs (ablation) | UKB with age+sex: MAE 2.48, RMSE 3.24, r=0.68, R²=0.44. Without age+sex: MAE 2.41, RMSE 3.20, r=0.70, R²=0.46. IXI fine-tuned: MAE 3.00, r=0.49, R²=0.21. No age/sex-only baseline |
| Finkelstein, Levakov et al. 2024, *Hum Brain Mapp*, DOI 10.1002/hbm.26595 | Trained on large MRI data; applied to a lifestyle-intervention cohort | Structural MRI | Deep-learning ensemble ("brain-BMI") | NR | NR | Performance numbers **not retrieved** (full text blocked) |
| Bachmann, Mueller, Kusnezow, Schroeter, Piaggi & Weise 2025, *GigaScience* 14:giaf010, DOI 10.1093/gigascience/giaf010 | HCP-YA S1200; rsfMRI N=999; tfMRI N≈1,007–1,077 per task | Cerebellocerebral FC, 513 parcels (HCP-MMP 360 + Tian 54 subcortical + 100 cerebellar). Pearson FC (rest), tangent-space FC (task) | CPM (edge threshold p<0.05, positive/negative networks, GLM) | 128 folds. **Siblings removed from each training fold** | Age, gender, ethnicity regressed. **Head motion not mentioned** | rsfMRI cerebellocerebral r=0.44; whole-brain rsfMRI ≈0.40 (Results and Discussion disagree on which is 0.40 and which 0.44); task groups r=0.59–0.62; task-general FC r=0.70 (p≤0.001, 2,000–10,000 permutations). No R²/MAE |
| Brain Imaging and Behavior 2025, DOI 10.1007/s11682-025-01056-z ("Functional connectome fingerprinting related to BMI and its association with impulsivity") | HCP1200; external validation in NKI | Resting-state FC | Connectome-based model (details NR) | NR (full text paywalled) | NR | HCP r=0.52, MAE=3.30. NKI validation r=0.35 (from search snippet) |
| Adise et al. 2021, *Dev Cogn Neurosci* 49:100948 (PMC8066422) | ABCD baseline, age 9–10, N≈6,851 (as cited by Xu 2023) | sMRI (CT, SA, subcortical volume) + DTI; separately rsFC and task activations | Elastic net | Cross-validated, train/test split | NR here | sMRI+DTI: train R²=0.35, test R²=0.27. rsFC test R²=0.14. WM-task activation test R²=0.16. Reward/inhibition tasks: no relationship. Pathological weight gain from structure: AUC_test=0.83; fMRI did not predict it |
| Park et al. 2015, *PLoS ONE* (journal.pone.0141376) | HCP | DTI structural connectivity + rsFC | Prediction of BMI from connectivity | NR | NR | Numbers not retrieved |
| Zhao et al. (SPIE 2020, 11583) | UK Biobank | Vertex-wise cortical thickness/area shape maps | Transfer learning, classification normal vs overweight/obese | NR | NR | Accuracy 65.6±0.7% (transfer) vs 62.7±0.7% (direct). Classification, not regression |

Sources for the rows above:
- Xu et al. 2023 full text: [PMC12614112](https://pmc.ncbi.nlm.nih.gov/articles/PMC12614112/)
- Cooper et al. 2025 preprint: [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.04.11.648433v1.full); published version: [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S3050642525000405)
- Vakli et al. 2020: [PMC7104804](https://pmc.ncbi.nlm.nih.gov/articles/PMC7104804)
- Finkelstein et al. 2024: [Wiley](https://onlinelibrary.wiley.com/doi/full/10.1002/hbm.26595); [MPG PDF](https://pure.mpg.de/pubman/item/item_3571962_3/component/file_3571963/Finkelstein_2024.pdf)
- Bachmann et al. 2025: [PMC11899596](https://pmc.ncbi.nlm.nih.gov/articles/PMC11899596/)
- Brain Imaging and Behavior 2025: [Springer](https://link.springer.com/article/10.1007/s11682-025-01056-z)
- Adise et al. 2021: [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1878929321000396); [DOAJ record](https://doaj.org/article/31d59fb084ad466fa51bf2c316493b42)
- Park et al. 2015: [PLoS ONE](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0141376)
- Zhao et al. 2020: [ADS](https://ui.adsabs.harvard.edu/abs/2020SPIE11583E..09Z/abstract)

**Notes on individual studies**
- Xu 2023 abstract versus model: the abstract headlines 10.05% and 8.87%, which belong to the sMRI + demographics model. The brain-only figures are lower (5.57% CV, 6.35% held-out). — [PMC12614112](https://pmc.ncbi.nlm.nih.gov/articles/PMC12614112/)
- Xu 2023 possible inflation: the "neuroanatomical profile" score used for mediation came from a model trained on the full training set. Training participants therefore got in-sample scores, which could inflate downstream associations. — [PMC12614112](https://pmc.ncbi.nlm.nih.gov/articles/PMC12614112/)
- Xu 2023 family structure: univariate LME models used family ID as a random intercept, but the paper does not say whether the ML folds were family-grouped. — [PMC12614112](https://pmc.ncbi.nlm.nih.gov/articles/PMC12614112/)
- Cooper 2025 claims the 3D-CNN "massively outperformed" ML and DL models built on tabular atlas ROI features, attributing the gain to features learned directly from the image. — [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.04.11.648433v1.full)
- Vakli 2020 age/sex inputs: removing age and sex did not hurt performance (r 0.70 vs 0.68). The CNN therefore extracts BMI-related signal beyond demographics, though the paper reports no demographic-only baseline. — [PMC7104804](https://pmc.ncbi.nlm.nih.gov/articles/PMC7104804)
- Vakli 2020 mass-univariate analysis: after multiple-comparison correction there was no significant BMI association with cortical thickness or curvature. The only significant cortical finding was a surface-area cluster in the isthmus cingulate. — [Vakli 2020 via search summary of PMC7104804](https://pmc.ncbi.nlm.nih.gov/articles/PMC7104804)
- Bachmann 2025 also released an open-source Python CPM framework. — [PMC11899596](https://pmc.ncbi.nlm.nih.gov/articles/PMC11899596/)

### Inferences
- In this table, regional FreeSurfer features with linear models give the lowest numbers (R²≈0.06 brain-only at N≈1,100 in HCP-YA). Voxel-level CNNs and FC-based CPM report much higher numbers, but none of the high-number studies clearly controls head motion (FC) or uses repeated nested family-grouped CV.
- The FC-based r values (0.44–0.70) are probably partly driven by motion, because BMI correlates with in-scanner head motion. Bachmann 2025 does not mention motion as a covariate, so those values may be inflated relative to a motion-controlled analysis. This is my inference and is not stated in the paper.
- Performance in ABCD children (test R²=0.27) is much higher than in HCP adults (≈0.06). The difference may reflect larger N, multimodal features (DTI) and developmental/site variance, so these numbers should not be pooled.

### Gaps
- Exact comparator numbers (elastic net, RF, TabNet on ROI features) in Cooper 2025 could not be retrieved because bioRxiv was rate-limited and ScienceDirect blocked access. These are the most directly relevant HCP-YA baselines, so fetch them manually.
- Finkelstein 2024 MAE/r values and the training dataset were not retrieved.
- Authors and CV details of the Brain Imaging and Behavior 2025 paper were not retrieved.
- I found no UK Biobank study reporting BMI prediction from multimodal IDPs with ridge regression.

## Large multi-phenotype benchmarking studies: do they report BMI separately?

### Takeaway
I could not confirm that any of the named large benchmarking papers (Ooi 2022, Dadi 2021, Schulz 2020, Cole 2020, Marek 2022) reports a separate BMI prediction accuracy. Their search snippets and abstracts discuss behavior, cognition, age or mental-health targets. Treat them as methodological references, not as BMI benchmarks, unless the report writer verifies otherwise.

### Cited Findings
- Ooi et al. 2022, *NeuroImage* 263:119636: kernel ridge, linear ridge and elastic net applied to HCP and ABCD, comparing anatomical (CT/area/volume), diffusion (DTI/NODDI on TBSS) and FC features. FC gave the best predictions across datasets, models and behaviors. Cognition was predicted better than other domains. Combining resting and task FC improved prediction about as much as combining all modalities. — [bioRxiv preprint PDF](https://www.biorxiv.org/content/10.1101/2022.03.08.483564.full.pdf); [DOAJ](https://doaj.org/article/c23f5da921b94686ac7743315e8517f3); [author PDF](https://shaoshiz.github.io/assets/pdf/2022_Ooi_Comparison%20of%20individualized%20behavioral%20predictions%20across%20anatomical,%20diffusion%20and%20functional%20connectivity%20MRI.pdf)
- Ooi 2022 behavioral target list: whether BMI is among the targets could not be confirmed from retrieved text. — [DOAJ](https://doaj.org/article/c23f5da921b94686ac7743315e8517f3)
- "Individual characteristics outperform resting-state fMRI for the prediction of behavioral phenotypes" (*Communications Biology* 2024) compares individual characteristics (which may include BMI as a predictor) with rsFC. The full text was not retrieved, so the role BMI plays is unconfirmed. — [Nature Comms Bio](https://www.nature.com/articles/s42003-024-06438-5)
- Marek et al. 2022, *Nature* 603:654–660, "Reproducible brain-wide association studies require thousands of individuals." Secondary sources report that small samples produce inflated, non-replicating effects. Cecchetti 2022 (PsyArXiv) disputes the "thousands" claim. — [secondary citation, PMC11092871](https://pmc.ncbi.nlm.nih.gov/articles/PMC11092871/); [Molecular Psychiatry perspective](https://www.nature.com/articles/s41380-022-01635-2)
- Xu 2023 cites Marek 2022 and Owens 2021 to argue that brain-wide BMI effects are typically small. — [PMC12614112](https://pmc.ncbi.nlm.nih.gov/articles/PMC12614112/)
- Other benchmarking papers, listed as [prior knowledge, not re-verified]:
  - Schulz et al. 2020, *Nature Communications* 11:4238, "Different scaling of linear models and deep learning in UK Biobank brain images versus machine-learning datasets", DOI 10.1038/s41467-020-18037-z. Targets were age, sex and several behavioral phenotypes. I do not recall a separately reported BMI result.
  - Dadi et al. 2021, *GigaScience*, "Population modeling with machine learning can enhance measures of mental health", DOI 10.1093/gigascience/giab071. Targets were age, fluid intelligence and neuroticism, not BMI.
  - Cole 2020, *Neurobiology of Aging*, "Multimodality neuroimaging brain-age in UK Biobank". BMI and other variables appear as correlates of the brain-age gap, not as a prediction target.
  - Bibliographic link for Marek 2022: [doi.org/10.1038/s41586-022-04492-9](https://doi.org/10.1038/s41586-022-04492-9)

### Inferences
- The best BMI-specific benchmarks are single-target studies: Xu 2023, Cooper 2025, Vakli 2020, Adise 2021, Bachmann 2025. Multi-phenotype benchmarks are mainly useful for the general finding that FC beats anatomy for behavior, and that accuracy grows slowly with N for linear models on IDPs.

### Gaps
- I did not verify, for any of Ooi 2022, Schulz 2020, Dadi 2021, Cole 2020 or Marek 2022, that BMI was or was not a separately reported prediction target. Check their supplementary target lists. Ooi 2022 HCP's 58 behavioral measures may not include BMI. Marek 2022 used cognition and psychopathology.
- Engemann et al. (UK Biobank, *eLife* 2020/2022) was not searched because of the tool-call budget.

## Methodological best practices a new BMI baseline must follow

### Takeaway
A defensible HCP-YA BMI baseline needs five things: (1) family-grouped outer and inner CV, with family-aware permutation (exchangeability blocks); (2) nested hyperparameter tuning; (3) confound regression, for example of age, sex, TIV and for FC also motion, fitted on training folds only and applied to test folds; (4) a demographics-only baseline and a permutation null; (5) reporting of R² (out-of-sample, sum-of-squares based), r and MAE, averaged over repeated splits.

### Cited Findings
- Family structure is real leakage in HCP-YA. Bachmann 2025 removed siblings from training folds "to prevent closely related subjects from predicting each other." — [PMC11899596](https://pmc.ncbi.nlm.nih.gov/articles/PMC11899596/)
- Xu 2023 modeled family ID as a random intercept in univariate LMEs but did not report family-grouped ML folds. This is a reporting gap a new baseline should close. — [PMC12614112](https://pmc.ncbi.nlm.nih.gov/articles/PMC12614112/)
- Permutation testing precedent: Bachmann 2025 permuted BMI within the test set (2,000 permutations for rsfMRI, 10,000 for tfMRI). — [PMC11899596](https://pmc.ncbi.nlm.nih.gov/articles/PMC11899596/)
- Demographic baseline matters. In Xu 2023, demographics alone gave held-out R²=2.6%, and demographics plus sMRI gave 8.87%, so brain-only R² (6.35%) should be reported next to the combined model. — [PMC12614112](https://pmc.ncbi.nlm.nih.gov/articles/PMC12614112/)
- Out-of-sample scoring: an in-sample "profile" score inflates downstream associations (the Xu 2023 caveat). All derived scores should be out-of-fold predictions. — [PMC12614112](https://pmc.ncbi.nlm.nih.gov/articles/PMC12614112/)
- More et al. compared whole-data confound regression with cross-validated (fold-wise) confound regression in a sex-prediction case study (brain size and age as confounds). Normalizing before or after confound removal made no difference. Under dataset/confound shift, the four confound-removal procedures gave mixed results. The paper is a sex-prediction study, not BMI. — [catalog record](https://vufind-test.katalog.k.utb.cz/SummonRecord/FETCH-LOGICAL-p339t-25287049a1267908d5014e6360c8ac998a7746c1657062007f4c944908da973/Details)
- Snoek, Miletić & Scholte 2019, *NeuroImage* 184:741–760, "How to control for confounds in decoding analyses of neuroimaging data" (citation verified via secondary references). From [prior knowledge, not re-verified]: the main recommendation is to regress confounds out within each CV fold, fitting on train and applying to test, because whole-dataset regression can bias results. — [secondary citation list](https://www.researchgate.net/publication/362533734_Leveraging_machine_learning_for_gaining_neurobiological_and_nosological_insights_in_psychiatric_research)
- Poldrack, Huckins & Varoquaux 2020, *JAMA Psychiatry* 77:534–540, "Establishment of best practices for evidence for prediction: a review" (citation verified via secondary reference). From [prior knowledge, not re-verified]: it recommends out-of-sample (CV or held-out) evaluation, using R² computed as 1 − SS_res/SS_tot rather than squared correlation, and reporting MAE. It cautions against leave-one-out CV and small samples, and asks that all feature selection and tuning be done inside CV. — [Poldrack publications](http://poldrack.github.io/publications); [secondary citation](https://www.researchgate.net/publication/362533734_Leveraging_machine_learning_for_gaining_neurobiological_and_nosological_insights_in_psychiatric_research)
- A meta-research paper reports that data leakage in ML studies propagates into meta-analytic estimates of predictive performance. — [PMC12602356](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12602356/)
- A 2024 PMC paper on the reliability and predictability of phenotype information from FC in large datasets is relevant to FC-based BMI targets. — [PMC11092871](https://pmc.ncbi.nlm.nih.gov/articles/PMC11092871/)
- HCP exchangeability blocks [prior knowledge, not re-verified]: Winkler et al. 2015, *NeuroImage*, "Multi-level block permutation", gives the framework (PALM, exchangeability blocks from family structure) for valid permutation tests in HCP.

### Inferences
Recommended protocol for neurobmi/linear_baseline.py, synthesized from the above:
1. **Folds:** use repeated (e.g. 10×) outer K-fold split by Family_ID (GroupKFold / StratifiedGroupKFold on binned BMI), with family-grouped inner CV for the alpha / l1_ratio search.
2. **Confounds:** regress age, sex and TIV out of the features with the regression fitted on the training fold only. Alternatively, report both "raw" and "confound-adjusted" models. Do not residualize BMI on the whole dataset. For any FC model, also include mean FD.
3. **Scaling:** fit standardization inside the fold.
4. **Baselines:** report a mean predictor (R²≈0), a demographics-only model and a brain-only model, plus brain + demographics.
5. **Metrics:** report out-of-sample R² (sklearn `r2_score` on pooled or per-fold predictions), Pearson r and MAE, as mean ± SD over repeats.
6. **Null:** run permutation tests, permuting BMI within or between whole families (exchangeability blocks), with at least 1,000 permutations.
7. **Realistic expectation:** for BMI from FreeSurfer regional features with linear models at N≈1,000 in HCP-YA, expect brain-only held-out R² of about 0.03–0.10 (r≈0.2–0.3), anchored on Xu 2023's 6.35%. A result above about 0.15 should trigger a leakage check: family leakage, confounds fitted on all data, or TIV/sex shortcuts. Voxel-level 3D-CNNs reach around 0.3 in the same cohort (Cooper 2025, preprint). The r≈0.2–0.3 range is my conversion (√0.06 ≈ 0.25), not a reported number.

### Gaps
- I could not directly verify the full text of Snoek 2019, Poldrack 2020, More 2021 or Winkler 2015 this session. Their specific recommendations above come from prior knowledge.
- I found no source that quantifies, specifically for HCP BMI models, how much family leakage or motion leakage inflates performance.
- Kong / Yeo lab and Tian & Zalesky papers were not searched because of the tool-call budget.
