# Pretrained / Foundation Brain MRI Models Applied to BMI and Adiposity Prediction

Scope: whether pretrained 3D brain MRI models (SFCN, BrainIAC, BrainLM, AnatCL, SimCLR-type, MedicalNet, BrainSegFounder, etc.) have been fine-tuned or linearly probed for BMI or adiposity; brain-age deltas and BMI; whether pretraining helps vs from-scratch or linear models at N~1000 (HCP-YA scale).
Search date: 2026-11-01. Caveat: bioRxiv full text was rate-limited (HTTP 429) during this session, so numbers for the BrainFMBench paper come from the project's GitHub README and search snippets, not the PDF.

## Q1. Which brain MRI foundation / pretrained models report BMI (or waist, body fat) as a downstream task?

### Takeaway
I found only one foundation-model benchmark that uses BMI as a downstream target: BrainFMBench / "A Comparative Evaluation of Structural MRI Foundation Models for Age, Sex, and Body-Mass Index Predictions" (bioRxiv 2026, accepted to MedAGI 2026). It used frozen features and a RandomForest probe on NKI (N=958) and HBN (N=997), cohorts close in size to HCP-YA. BMI was the hardest task. Frozen foundation-model features beat FreeSurfer features on BMI by only modest margins, and an "un-CNN" model beat every pretrained model. The flagship foundation-model papers (BrainIAC, BrainLM, Brain2Vec, BrainFedFM) report no BMI task. The DL BMI predictors that do exist were trained from scratch on UK Biobank.

### Cited Findings
**Foundation-model benchmark that includes BMI**
- The paper is titled "A Comparative Evaluation of Structural MRI Foundation Models for Age, Sex, and Body-Mass Index Predictions" (bioRxiv 10.64898/2026.05.15.725427, v4). It benchmarks four public structural MRI foundation models (AnatCL, BrainIAC, 3D-Neuro-SimCLR, SwinBrain) on T1w MRI from PPMI, HBN and NKI, using a frozen-feature probing protocol with FreeSurfer morphometrics as the baseline. According to a co-author post, it was accepted to MedAGI 2026. Authors per the search snippet: Encin, Gilmore, Rokem, Dickie, Glatard. — [bioRxiv](https://www.biorxiv.org/content/10.64898/2026.05.15.725427v4.full); [ScienceCast summary of earlier version](https://bio.sciencecast.org/casts/o4l3dfez6gp0)
- The search snippet of the paper says AnatCL significantly outperformed FreeSurfer baselines on age, but was "less consistent" on sex and BMI regression. It calls BMI the most challenging task. The probe is a Random Forest on frozen features. — [bioRxiv](https://www.biorxiv.org/content/10.64898/2026.05.15.725427v4.full)
- The BrainFMBench protocol, per the README, is a RandomForest probe (200 trees, depth 6) on standardized frozen features, with 5-fold CV × 5 seeds plus a held-out test set. Metrics are MAE for age and BMI and balanced accuracy for sex. — [GitHub epics-lab/BrainFMBench](https://github.com/epics-lab/BrainFMBench)
- BMI MAE (kg/m²) on **NKI, N=958**, from the README: un-CNN 3.13±0.11; 3D-Neuro-SimCLR 3.52±0.17; Dinov3D-neuro 3.69±0.12; AnatCL Local 3.92±0.25; AnatCL Global 3.92±0.22; SwinBrain 3.97±0.20; FS aparc 3.99±0.36; FS Schaefer 3.99±0.35; BrainIAC 4.16±0.25. — [GitHub epics-lab/BrainFMBench](https://github.com/epics-lab/BrainFMBench)
- BMI MAE on **HBN, N=997** (a paediatric/adolescent cohort): un-CNN 2.70±0.33; 3D-Neuro-SimCLR 3.02±0.29; Dinov3D-neuro 3.23±0.27; AnatCL Local 3.34±0.40; AnatCL Global 3.39±0.33; SwinBrain 3.41±0.36; FS Schaefer 3.44±0.31; FS aparc 3.51±0.31; BrainIAC 3.59±0.49. — [GitHub epics-lab/BrainFMBench](https://github.com/epics-lab/BrainFMBench)
- The README also says "Ranking varies by task and dataset; there is no single overall winner". It reports no naive (predict-the-mean) BMI baseline and no r/R². — [GitHub epics-lab/BrainFMBench](https://github.com/epics-lab/BrainFMBench)
- A fork (rlbachen/BrainFMBench) shows a different leaderboard snapshot: NKI BMI MAE 3.83 (SimCLR) and 4.18 (SwinBrain); HBN 3.11 (SimCLR) and 3.49 (SwinBrain). These numbers conflict with the epics-lab README, so the leaderboard has changed over time. — [GitHub rlbachen/BrainFMBench](https://github.com/rlbachen/BrainFMBench) vs [GitHub epics-lab/BrainFMBench](https://github.com/epics-lab/BrainFMBench)
- A CAMH-linked write-up (search snippet) says "its unCNN model obtained the best BMI prediction performance on the datasets where BMI was available". — [search result, LinkedIn E. Tio](https://www.linkedin.com/in/earvin-tio/)

**Foundation models with no BMI downstream task found**
- BrainIAC (Nature Neuroscience 2026) is a contrastive SSL model validated on seven downstream applications, including brain age. BMI is not among them. — [Nature Neuroscience](https://www.nature.com/articles/s41593-026-02202-6); [GitHub AIM-KannLab/BrainIAC](https://github.com/AIM-KannLab/BrainIAC)
- BrainLM (fMRI foundation model, ICLR 2024) is fine-tuned with an MLP head on UKB to predict age, neuroticism, PTSD (PCL-5) and anxiety (GAD-7). BMI is not listed. Pretraining used 76,296 UKB recordings (~6,450 h). — [BrainLM bioRxiv](https://www.biorxiv.org/content/10.1101/2023.09.12.557460v1.full); [HuggingFace model card](https://huggingface.co/vandijklab/brainlm)
- Brain2Vec (arXiv 2610.28411) is pretrained on 74,425 T1w scans. Its frozen embeddings beat volumetric features on 4 of 5 classification tasks, and the snippet mentions no BMI. — [arXiv](https://arxiv.org/abs/2610.28411)
- BrainFedFM (arXiv 2609.27611) has 17 tasks across 20 datasets. Its regression tasks are brain age (SALD, NKI-RS), with no BMI. — [arXiv](https://arxiv.org/pdf/2609.27611)

**DL BMI predictors trained from scratch (not foundation models)**
- Vakli et al. 2020 (Front. Neuroinform.) trained a 3D CNN with spatially separable convolutions on UKB T1, using age and sex as inputs. The UKB test set was N=2000, with external IXI test N=36. Attribution pointed to the caudate and amygdala. As cited by Finkelstein 2024, the reported performance is MAE 2.41 kg/m² and r≈0.7 on the UKB test set. The abstract does not mention transfer learning. — [PubMed 32265681](https://pubmed.ncbi.nlm.nih.gov/32265681/); [PMC7104804](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7104804/); numbers via [Finkelstein 2024, PMC10878010](https://pmc.ncbi.nlm.nih.gov/articles/PMC10878010/)
- Finkelstein et al. 2024 (Hum Brain Mapp) used an ensemble of 10 randomly initialised 3D CNNs, combined by linear regression, trained on ~19k scans (13,471 train / 1,957 val / 3,847 test; the text elsewhere says 19,491, which is inconsistent). Held-out results were MAE 2.06 kg/m², r=0.80. External DIRECT-PLUS: MAE 5.29, r=0.46 (T0) and MAE 5.23, r=0.50 (T18). The paper explicitly says the CNNs were "randomly initialized", with no brain-age transfer. Predicted BMI decreased with real weight loss after a lifestyle intervention. — [PMC10878010](https://pmc.ncbi.nlm.nih.gov/articles/PMC10878010/)
- OMTNet (SPIE 2020) used ImageNet-pretrained 2D networks on cortical-shape maps (optimal mass transport) from UKB to classify normal weight vs overweight/obese. Accuracy was ~65.6% with transfer learning. This is one of the few explicit transfer-learning BMI papers, but the transfer is from ImageNet, not a brain model. — [ADS / SPIE 11583](https://ui.adsabs.harvard.edu/abs/2020SPIE11583E..09Z/abstract)

### Inferences
- At N≈1000 (NKI/HBN), frozen foundation-model features give BMI MAE about 0.0–0.5 kg/m² better than FreeSurfer parcellation features. BrainIAC is at or below the FreeSurfer level. An "un-CNN" (my reading: possibly an untrained/randomly initialised CNN feature extractor; the README does not define it here, so verify) beats all pretrained models on BMI. If that reading is right, current SSL pretraining adds little BMI-relevant signal beyond generic image statistics.
- Without a predict-the-mean baseline, the absolute BMI MAEs (~3–4 kg/m²) are hard to interpret. For typical BMI SD of ~4–6 kg/m², they may correspond to modest r. This needs checking against the paper.
- No study fine-tunes (rather than freezes) a brain foundation model end-to-end for BMI at HCP-YA scale. No study evaluates BMI on HCP-YA with any pretrained model. Both look like open niches.

### Gaps
- Exact r/R², the naive baseline, and PPMI results from the BrainFMBench paper: I could not read the full text (bioRxiv 429).
- No reports found of SFCN (Peng), MedicalNet, BrainSegFounder, or Prima features probed for BMI, waist, or body fat. "Not found" is not proof of absence. I did not exhaustively search MICCAI proceedings.
- No foundation-model paper found that uses waist circumference, body-fat %, or visceral fat as a downstream target.

## Q2. Do brain-age deltas (brain-PAD) relate to BMI, and has brain-age-pretrained feature transfer been used to predict BMI?

### Takeaway
Brain-PAD links more consistently to visceral fat and metabolic markers than to BMI itself, and the associations are small and sex-dependent. I found no study that transfers brain-age-pretrained network features (e.g., SFCN weights) to predict BMI. Finkelstein 2024 trained parallel age and BMI CNNs separately from random init and only compared their saliency maps.

### Cited Findings
- In a UKB diffusion-MRI brain-age study (~21,000 participants), a higher brain-age gap was associated with greater BMI, waist-to-hip ratio and body-fat % in males. In females it was associated only with WHR, not BMI or BF%. — [Subramaniapillai et al., PMC9294301](https://pmc.ncbi.nlm.nih.gov/articles/PMC9294301)
- In 551 sedentary adults aged ≥65, BMI was not correlated with age-adjusted brain-PAD (r=0.048, p=0.257). Visceral adipose tissue was (r=0.152, p<0.001). — [PMC9894084 Table 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC9894084/table/T2)
- In two weight-loss trials, reduced brain-PAD tracked weight loss. HOMA insulin resistance and leptin were consistently associated with higher brain-PAD. — [MDC Berlin edoc](https://edoc.mdc-berlin.de/25960/)
- Adults with Prader-Willi syndrome (n=20 vs 40 controls) had higher brain-PAD, and this persisted in a BMI-matched subgroup. The authors list obesity and type 2 diabetes among conditions associated with older-appearing brains. — [PMC6412082](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6412082/)
- Finkelstein 2024 trained both age and BMI CNNs, each "randomly initialized, and separately trained to predict age or BMI". There was no fine-tuning from the brain-age model; the age model was used only to compare explanation maps. — [PMC10878010](https://pmc.ncbi.nlm.nih.gov/articles/PMC10878010/)

### Inferences
- Since brain-PAD explains little BMI variance (r≈0.05–0.15 where reported), brain-age-pretrained features may not carry much BMI-specific information. Holderrieth et al. (Q3) found that transfer works best when the pretraining label matches the target label, which points the same way.

### Gaps
- No study found that linearly probes SFCN (or other brain-age network) penultimate features for BMI. This appears to be untested.
- I did not retrieve exact BMI–brain-PAD effect sizes from the large UKB T1 brain-age studies (e.g., Cole, Kolbeinsson, Dinsdale 2021).

## Q3. Does pretraining help small-sample phenotype prediction vs training from scratch, and what do DL-vs-linear comparisons say at N~1000?

### Takeaway
At N≈1000, the large-scale comparisons consistently find deep learning about equal to linear/kernel models for brain-derived phenotypes (Schulz 2020, He 2020). Abrol 2021 finds DL advantages only at larger N, beyond ~1,157 training subjects. Pretraining or transfer helps small-N prediction of *age and sex*: Peng 2021, Gong 2021, Holderrieth 2022. Holderrieth reports that transfer works best when the pretraining task matches the target. None of these papers tested BMI or any non-brain body phenotype, so for BMI at N~1000 the expectation from the literature is that DL will be no better than linear unless pretraining adds the right inductive bias.

### Cited Findings
**Schulz et al. 2020, Nat Commun 11:4238**
- Targets were a 10-class age×sex label, sex, age, fluid intelligence, household size, and income. **BMI and weight were not included.** UKB N=9,300, with training sizes up to 8,000 and 20 random splits. — [PMC7447816](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7447816/)
- At ~1,000 training subjects (UKB sMRI, 10-class age/sex), logistic regression scored 31.80% and RBF-SVM 32.14%, statistically indistinguishable. On MNIST the same comparison was 86.31% vs 88.23%. On brain data, linear, kernel and deep models were about the same across all sample sizes, and linear models "keep improving as the sample size approaches ~10,000 subjects". — [PMC7447816](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7447816/)

**He et al. 2020, NeuroImage 206 (FC-based)**
- HCP: 58 behavioral measures (cognition, emotion, personality). UKB: age, sex, fluid intelligence, pairs matching. **BMI/weight are not among the UKB measures.** The HCP list is in Table S1, which I could not read. The main text names fluid intelligence, grip strength, picture vocabulary. Whether a body measure is among the 58 is unverified, but the categories make it unlikely. — [PMC6984975](https://pmc.ncbi.nlm.nih.gov/articles/PMC6984975)
- HCP mean r across 58 measures: FNN 0.121, kernel regression 0.115 (p=0.60), BrainNetCNN 0.114, GCNN 0.072 (kernel significantly better than GCNN). UKB age r: 0.599 for both kernel and FNN. UKB fluid intelligence r: 0.239 for both. No UKB differences survived correction. — [PMC6984975](https://pmc.ncbi.nlm.nih.gov/articles/PMC6984975)
- In UKB, fluid-intelligence accuracy rose sharply from N=100 to 1,000 and more modestly from 1,000 to 5,000. Kernel regression stayed competitive at all sizes. — [PubMed 31610298](https://pubmed.ncbi.nlm.nih.gov/31610298/)

**Abrol et al. 2021, Nat Commun 12:353**
- Tasks were 10-way age×sex, sex, and age (UKB n=12,314), plus MMSE (ADNI n=828). **No BMI or non-brain phenotypes.** Training sizes ran from 100 to 10,000. — [PMC7806588](https://pmc.ncbi.nlm.nih.gov/articles/PMC7806588)
- DL significantly beat standard ML only at training sizes beyond the 1,157-subject test size. At small N, "DL analysis at small sample sizes (n = 50 and n = 100) did not perform worse than SML". — [PMC7806588](https://pmc.ncbi.nlm.nih.gov/articles/PMC7806588)
- At n=10,000: age MAE 2.94 (DL) vs 3.25 (SML), PCC 0.87 vs 0.84. MMSE (n=428 train): MAE 1.74 vs 1.81, PCC 0.56 vs 0.51. The paper has no transfer-learning experiments of its own. SML trained on DL embeddings improved SML. — [PMC7806588](https://pmc.ncbi.nlm.nih.gov/articles/PMC7806588)

**Pretraining / transfer for small cohorts**
- Peng et al. 2021 (Med Image Anal 68:101871) introduced SFCN, a lightweight network suited to small 3D datasets. Even with ~50 training subjects it beat widely used regression models for brain age. Pretrained weights (14,503 UKB scans) are released. — [summary via Gong et al. 2021, Front Psychiatry](https://www.frontiersin.org/articles/10.3389/fpsyt.2021.627996/full)
- Gong et al. 2021 (PAC 2019): UKB-pretrained SFCN gave better single-model brain-age performance than random initialisation on the PAC 2019 dataset. — [Front Psychiatry](https://www.frontiersin.org/articles/10.3389/fpsyt.2021.627996/full)
- Holderrieth, Smith & Peng (medRxiv 2022) pretrained SFCN on UKB for age and sex and transferred to three small MRI datasets. The transfer beat classical regression and training from scratch, and features transferred well **when the pretraining task matched the target label**. Targets were age and sex only. Code: GitHub PeterHolderrieth/TransferLearning_Neuroimaging. — [medRxiv 10.1101/2022.12.11.22283324](https://www.medrxiv.org/content/10.1101/2022.12.11.22283324)
- A scoping review reports that transfer learning improved performance in almost all neuroimaging studies it reviewed. Publication bias is a plausible caveat. — [PMC8899512](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8899512/)

### Inferences
- For a non-brain phenotype like BMI at HCP-YA scale (~1,100), the evidence suggests: (a) regularized linear/kernel models on IDPs or FC are a strong and possibly unbeatable baseline (Schulz, He, Abrol); (b) generic SSL foundation-model features give at most small gains over FreeSurfer features (BrainFMBench, NKI/HBN N≈1000); (c) brain-age-pretrained transfer may not help BMI, because the pretraining label does not match (Holderrieth).
- A large-N BMI-supervised pretrained model, e.g., a UKB-trained BMI CNN in the style of Vakli or Finkelstein, then fine-tuned or probed on HCP-YA, would be the label-matched transfer that Holderrieth suggests works. I found no published instance of it. Domain shift is a risk: Finkelstein's external MAE rose from 2.06 to ~5.3.

### Gaps
- None of Schulz 2020, He 2020 (UKB part), or Abrol 2021 includes BMI, weight, waist, or body fat as a target. Direct DL-vs-linear BMI comparisons at matched N are missing from this literature.
- I did not check Dinsdale et al. 2021 (NeuroImage, brain-age CNN in UKB) for transfer or BMI associations within the tool budget.
- He 2020 HCP Table S1 was not verified for a BMI or weight measure.
