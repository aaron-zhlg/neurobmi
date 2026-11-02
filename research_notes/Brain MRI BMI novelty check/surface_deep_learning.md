# Surface-based and vertex-wise (deep) models for BMI / obesity from cortical surface data

Search terms used (WebSearch, standard and extended): "vertex-wise cortical thickness BMI prediction deep learning"; "Couvy-Duchesne 2020 morphometricity BMI vertex-wise grey matter UK Biobank HCP"; "Surface Vision Transformer Dahan phenotype prediction dHCP HCP"; "SiT surface vision transformer fluid intelligence HCP MAE pretraining cortical phenotype regression"; "benchmarking geometric deep learning cortical segmentation neurodevelopmental phenotype prediction Fawaz"; "graph neural network cortical surface mesh obesity BMI prediction"; "spherical convolutional network cortical surface body mass index prediction 2024 OR 2025"; "Deep transfer learning of brain shape morphometry predicts Body Mass Index UK Biobank"; "surface-based vs volume-based vs ROI features prediction comparison ... BMI machine learning"; "cortical surface deep learning obesity adiposity vertex myelin thickness graph convolution UK Biobank ABCD"; plus a PMC search for Couvy-Duchesne vertex-wise papers. Full texts read: Couvy-Duchesne 2020 (PMC), Delzant 2025 (PMC), SiT TMI preprint (arXiv PDF), Cooper 2025 (bioRxiv), Im 2024 SPHARM-Net (PMC), Morys 2024 (PMC). Several sources were paywalled or bot-blocked (SPIE OMTNet paper, Wiley HBM page), so for those only abstracts and snippets were used.

## Q1. Has anyone predicted BMI / obesity from vertex-wise cortical maps (thickness, area, curvature, myelin) with ML or DL?

### Takeaway
Yes, but only in a few ways. (a) Linear mixed-model "morphometricity" plus BLUP prediction from about 650k vertex-wise thickness and area values (Couvy-Duchesne 2020; UKB, tested out-of-sample in HCP-YA). (b) One 2020 UKB study that turned vertex-wise shape maps into 2D images and used ImageNet CNNs to classify normal vs overweight/obese (Zeng et al., OMTNet). I found no study that trains a native surface deep model (spherical CNN, GNN, Surface Vision Transformer, MoNet, spherical U-Net) to regress BMI. I also found no study that uses T1w/T2w myelin maps or fsLR-32k surfaces to predict BMI, in HCP-YA or elsewhere.

### Cited Findings
**Couvy-Duchesne et al. 2020, Human Brain Mapping 41:4062–4076, "A unified framework for association and prediction from vertex-wise grey-matter structure"**
- Design: a linear mixed model (LMM) of each phenotype on 652,283 vertex-wise measures per person: 299,009 cortical thickness, 299,034 cortical surface area, 27,120 subcortical thickness and 27,120 subcortical log-Jacobian values (FreeSurfer fsaverage, unsmoothed). UKB discovery N = 9,497, UKB replication N = 4,323, HCP N = 1,110. Of 167 phenotypes, 58 showed significant morphometricity and 23 replicated. — [PMC7469763](https://pmc.ncbi.nlm.nih.gov/articles/PMC7469763/); [UKB publication page](https://www.ukbiobank.ac.uk/publications/a-unified-framework-for-association-and-prediction-from-vertex-wise-grey-matter-structure/)
- Weight, BMI, waist and hip circumference were "strongly associated (R2 > 0.40)" with grey-matter structure (morphometricity in UKB discovery). Exact per-trait values are only in Fig. 2 and Data S3, which I did not access. — [PMC7469763](https://pmc.ncbi.nlm.nih.gov/articles/PMC7469763/)
- BLUP prediction of BMI from vertex-wise data: UKB 10-fold CV r = 0.45 (R² = 0.20); UKB replication r = 0.45 (R² = 0.20); **HCP out-of-sample r = 0.21 (R² ≈ 0.042, p = 2.4e-12)**. Weight score in HCP: r = 0.19 (R² = 0.036). In-sample R² was about 0.085 for body fat %, 0.16 for waist and 0.15 for weight. — [PMC7469763](https://pmc.ncbi.nlm.nih.gov/articles/PMC7469763/)
- BLUP accuracy was similar to or better than LASSO. Smoothing (FWHM 5–25 mm) and coarser meshes (fsaverage6 down to fsaverage3) lowered morphometricity point estimates; unsmoothed full-resolution meshes gave the highest. — [PMC7469763](https://pmc.ncbi.nlm.nih.gov/articles/PMC7469763/)
- Body size explains much of the brain–phenotype association. Depression-score morphometricity fell from R² 0.050 to below 0.001 after conditioning on weight and BMI. In UKB, 14 of 58 associations lost significance after adjusting for weight and BMI (4 more after height). In HCP, 4 of 27 were lost after controlling for body size. — [PMC7469763](https://pmc.ncbi.nlm.nih.gov/articles/PMC7469763/)
- A pre-publication abstract (LINE 2019) reports slightly different numbers: 654,386 vertices and discovery N = 9,888. — [LINE 2019 abstract](https://line2019.sciencesconf.org/289498.html)

**Delzant, Colliot & Couvy-Duchesne 2025, Human Brain Mapping 46(16):e70372, "Choice of processing pipelines for T1-weighted brain MRI impacts association and prediction analyses"**
- BMI, waist and hip were treated as confounders here, not targets. Body-size morphometricity was R² 20–80% depending on the pipeline. Body-size association by pipeline: FSL-VBM 52%, FSL-ANAT 52%, CAT12 volume 43%, FreeSurfer (all modalities) 34%, CAT12 surface 15%. Volume-based pipelines generally gave better prediction than surface-based ones. — [PMC12572822](https://pmc.ncbi.nlm.nih.gov/articles/PMC12572822/)

**Zeng et al. 2020, SPIE Medical Imaging 11583 (and an MLCN 2020 Springer chapter), "Deep transfer learning of brain shape morphometry predicts Body Mass Index (BMI) in the UK Biobank"**
- About 26k UKB participants. An optimal-mass-transport, area-preserving mapping projected vertex-wise cortical and subcortical shape maps to 2D planes. ImageNet-pretrained VGG19, ResNet152 and DenseNet201 then classified normal vs overweight/obese BMI. — [SPIE](https://neurophotonics.spiedigitallibrary.org/conference-proceedings-of-spie/11583/1158309/Deep-transfer-learning-of-brain-shape-morphometry-predicts-Body-Mass/10.1117/12.2577074.full); [ADS abstract](https://ui.adsabs.harvard.edu/abs/2020SPIE11583E..09Z/abstract)
- Surface area and cortical thickness (especially the left hemisphere), together with subcortical shape, gave the highest accuracies. The SPIE abstract reports a network-ensemble accuracy of 65.6% with transfer learning vs 62.7% with direct learning. The MLCN chapter reports ensemble accuracies of 72.8% (ResNet152) and 73.9% (DenseNet201). These numbers conflict between the two versions; I could not read either full text. — [SPIE](https://neurophotonics.spiedigitallibrary.org/conference-proceedings-of-spie/11583/1158309/Deep-transfer-learning-of-brain-shape-morphometry-predicts-Body-Mass/10.1117/12.2577074.full); [Springer chapter](https://link.springer.com/chapter/10.1007/978-3-030-66843-3_17)

**Vertex-wise / parcel-wise association studies of BMI (not prediction)**
- Adults (N = 202, Int J Obesity 2016): surface-based morphometry found no global cortical association with BMI, but focal thinning with higher BMI in left lateral occipital and right ventromedial prefrontal cortex. Regional surface area showed no BMI association. — [IJO 2016](https://www.nature.com/articles/ijo201642)
- Children (N = 378, Frontiers in Neuroscience 2015): no significant vertex-wise association between cortical thickness and BMI. — [Frontiers 2015](https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2015.00024/pdf)
- Morys et al. 2024, Communications Biology 7:656: parcel-wise (DKT, 62 parcels) "obesity maps" of thickness vs BMI in ABCD (N = 9,521), **HCP-YA (N = 814)**, HCP-Aging (N = 228) and UKB (N = 36,333). Higher BMI went with thinner temporal and inferior frontal cortex in all four samples, with some positive associations in dorsal frontal and occipital cortex in adults. No ML prediction was done. — [PMC11133431](https://pmc.ncbi.nlm.nih.gov/articles/PMC11133431/)

**Volumetric deep learning for BMI (for context, not surface)**
- Vakli et al. 2020: a 3D CNN on structural MRI predicted BMI with MAE 2.36 kg/m² when age and sex were withheld. — [PMC7104804](https://pmc.ncbi.nlm.nih.gov/articles/PMC7104804)
- Cooper, Elsayed, Owens & MacKillop 2025 (bioRxiv), **HCP-YA S1200, N = 1,106**: a 3D CNN on VBM grey-matter maps (MNI, 10 mm FWHM) reached CV R² = 0.325 and lockbox R² = 0.442. Random forest on 255 Conte69 atlas ROI features (volume, thickness, area) reached CV R² = 0.063 and lockbox R² = 0.031; elastic net and TabNet on ROIs were below R² 0.07. RF or elastic net on CNN-extracted features reached lockbox R² of 0.485 and 0.456. No surface or vertex model was tested. The preprint is internally inconsistent: the abstract gives 0.325 as the lockbox R² while the Results give it as the CV mean, and the ROI count is stated as 255 in one place and 153 in another. — [bioRxiv 2025.04.11.648433](https://www.biorxiv.org/content/10.1101/2025.04.11.648433v1.full)
- Finkelstein et al. 2024, Human Brain Mapping: ensemble deep learning inferred BMI from structural MRI, and predicted BMI tracked weight loss in the DIRECT-PLUS trial. The snippets do not say the input was vertex-wise. — [record](https://searchworks.jioinstitute.edu.in/articles/cmedm__38375968); [AMiner](https://aminer.org/pub/65d5140c939a5f40826269b5/deep-learning-based-bmi-inference-from-structural-brain-mri-reflects-brain-alterations)

### Inferences
- The only out-of-sample vertex-wise BMI benchmark in HCP-YA I found is Couvy-Duchesne's UKB-trained BLUP, which reached **r = 0.21** when transferred to HCP. A within-HCP-YA surface deep model has no direct published comparator. The relevant HCP-YA comparators are volumetric: Cooper 2025's 3D CNN (R² of about 0.33–0.44) and its weak ROI baselines (R² < 0.07).
- None of the BMI work uses T1w/T2w myelin, fsLR-32k (HCP MSMAll) surfaces, or native surface operators. Each of these is a plausible novelty claim, as long as it is framed against the Couvy-Duchesne LMM/BLUP and Zeng OMTNet precedents.
- Because body size accounts for a large share of grey-matter morphometricity, surface models of BMI need careful deconfounding (head size/ICV, age, sex, family structure in HCP). Reviewers will likely ask whether surface signal adds beyond total brain or ICV.

### Gaps
- I could not access exact BMI morphometricity values (Couvy-Duchesne Fig. 2 / Data S3) or the HCP-only morphometricity for BMI.
- I could not resolve the conflicting OMTNet accuracies (65.6% vs 72.8–73.9%) or confirm the exact cortical inputs, because the full texts are paywalled.
- I could not check whether Finkelstein 2024 used surface features.
- My searches may have missed 2025–2026 MICCAI/MIDL workshop papers; MICCAI 2025 and MIDL 2025/2026 proceedings were not browsed directly.

## Q2. Surface deep learning frameworks on other phenotypes (HCP / dHCP / UKB): targets and accuracy. Has BMI or body size been a target?

### Takeaway
Surface DL frameworks have been benchmarked mainly on neonatal age (dHCP PMA/GA), HCP fluid intelligence, UKB age and sex, and disease classification. None of the frameworks I found (SiT, MS-SiT, sMAE/vsMAE, the Fawaz gDL benchmark with S2CNN, ChebNet, GConvNet, Spherical U-Net and MoNet, SPHARM-Net, SurfGNN) used BMI or body size as a target. The one GNN-for-body-fat paper works on whole-body surface meshes, not cortex.

### Cited Findings
- **Surface Vision Transformer (SiT; Dahan et al., IEEE TMI 2022 / arXiv 2204.03408)**, tested on three tasks:
  - dHCP: inputs were sulcal depth, curvature, cortical thickness and T1w/T2w myelin; N = 530 for PMA and 514 for GA.
  - HCP fluid intelligence: N = 446; inputs were the 115 HCP-MMP feature maps (thickness, T1w/T2w myelin, curvature, task and rest fMRI maps).
  - SCOT-HEART coronary calcium score.
  
  Best average dHCP MAE was 0.89 weeks for SiT-small vs 1.05 for MoNet, the best gDL model. Baseline averages were S2CNN 1.06, ChebNet 1.16, GConvNet 1.39 and Spherical U-Net 1.11. On deconfounded GA in native space, Spherical U-Net degraded from 0.85 to 2.16 MAE. HCP fluid intelligence: SiT-tiny r = 0.35 ± 0.03 vs MS-G3D r = 0.26. No body-size target was used. — [arXiv 2204.03408](https://arxiv.org/abs/2204.03408) (numbers from the PDF text)
- **Multiscale SiT (MIDL 2024)**: hierarchical windowed attention that outperformed earlier surface DL on dHCP neonatal phenotyping, plus parcellation on UKB and MindBoggle. — [PMLR v250](https://proceedings.mlr.press/v250/dahan24a.html); [arXiv 2303.11909](https://arxiv.org/abs/2303.11909v2)
- **Surface masked autoencoders (sMAE/vsMAE; Dahan et al., MIDL 2024)**: pretraining improved dHCP phenotype prediction by at least 26%, with 80% faster convergence; vsMAE added a further 13%. On HCP fluid intelligence from 3T contrast maps it reached r = 0.39 vs at most 0.3 from scratch (from the appendix, via snippet). Pretraining on UKB transferred. — [arXiv 2308.05474](https://arxiv.org/abs/2308.05474v2); [MLAnthology](https://mlanthology.org/midl/2024/dahan2024midl-spatiotemporal)
- **Fawaz et al. 2021 benchmark (bioRxiv 2021.12.01.470730)**: compared geometric vs traditional DL on dHCP for PMA, GA and M-CRIB-S parcellation, and found the advantage of gDL is task-dependent and sensitive to registration. A G-Node data record lists a retraction date (03 Dec 2021), but the reason is unclear; it may concern the dataset record rather than the paper. Code is in the Abdulah-Fawaz/Benchmarking-Surface-DL GitHub repository. — [bioRxiv](https://www.biorxiv.org/content/10.1101/2021.12.01.470730.full.pdf); [G-Node](https://doi.gin.g-node.org/10.12751/g-node.7p3tww/)
- **Spherical U-Net (Zhao et al. 2019)**: applied to infant cortical parcellation and prediction of cortical attribute development (vertex-wise thickness maps), not to phenotype regression of body size. — [arXiv 1904.00906](https://arxiv.org/pdf/1904.00906)
- **SPHARM-Net (Im et al., bioRxiv 2024)**:
  - UKB N ≈ 32,979: age MAE 2.97 y (R² 0.77, r 0.90), using thickness and area; sex AUC 0.97, using curvature and convexity.
  - ADNI N = 1,213: AD vs control AUC 0.90.
  
  Inputs were FreeSurfer vertex-wise maps at 163,842 vertices. No BMI target and no ROI or voxel baselines. — [PMC11565793](https://pmc.ncbi.nlm.nih.gov/articles/PMC11565793/)
- **SurfGNN (arXiv 2411.05825)**: treats the cortical mesh as a sparse graph; applied to neonatal brain age. — [arXiv 2411.05825](https://www.arxiv.org/abs/2411.05825)
- **Graph convolutions on spectral embeddings of cortical surfaces (2018)**: an early GCN on cortical data, used for parcellation. — [arXiv 1803.10336](https://arxiv.org/pdf/1803.10336)
- **Vertex-wise DL for a psychiatric phenotype**: an MDD classification study using vertex-wise sulcal depth, curvature and thickness with deep and shallow models (I saw only the title in a PMC listing). — [PMC12916314](https://pmc.ncbi.nlm.nih.gov/articles/PMC12916314/)
- **Body-fat GNN (not brain)**: GNNs on whole-body triangulated surface meshes (UKB body MRI) predicted visceral and subcutaneous adipose volumes. The paper calls BMI a coarse proxy. — [arXiv 2308.02493](https://arxiv.org/pdf/2308.02493)

### Inferences
- In HCP-YA, the established surface-DL benchmark target is fluid intelligence (SiT r of about 0.35–0.39 using 115 MMP maps). A BMI target on fsLR-32k thickness, myelin and curvature with SiT, MS-SiT, a spherical CNN or a GNN would appear to be the first of its kind in that literature.
- The metrics-lab SiT code already supports HCP fsLR/ico-resampled inputs, so it is a natural baseline.
- dHCP results show gDL ranking is unstable across tasks and spaces (template vs native). A BMI study should report several surface architectures and both registered (MSMAll) and native settings.

### Gaps
- I did not verify every MICCAI 2023–2025 surface-DL paper, for example Gemini, Spherical Transformer or deformable spherical U-Net follow-ups, for body-size targets.
- I did not check GitHub issues or repositories for unpublished BMI experiments.

## Q3. Comparisons of surface/vertex-level vs ROI-level vs voxel-level models for BMI or other non-brain phenotypes

### Takeaway
Direct three-way comparisons for BMI are scarce. Couvy-Duchesne 2020 found vertex-wise data always explained more variance than ROI summaries (34 Desikan regions plus subcortical volumes), across phenotypes including body size. Delzant 2025 found volume-based (VBM) representations generally beat surface-based ones for association and prediction, with body-size morphometricity of 43–52% for volume pipelines vs 15–34% for surface pipelines. Cooper 2025 in HCP-YA found a voxel 3D CNN far outperformed ROI-based ML for BMI (R² about 0.33–0.44 vs below 0.07). No study I found puts a native surface deep model against voxel and ROI models for BMI.

### Cited Findings
- Vertex-wise LMM always gave greater R² than ROI-based reduction (34 cortical thickness and area regions plus subcortical volumes). — [Couvy-Duchesne 2020, PMC7469763](https://pmc.ncbi.nlm.nih.gov/articles/PMC7469763/)
- Body-size morphometricity by pipeline: FSL-VBM 52%, FSL-ANAT 52%, CAT12 volume 43%, FreeSurfer 34%, CAT12 surface 15%. Volume pipelines also gave better prediction for the 29 traits tested. This compares representation types, not vertex vs ROI. — [Delzant 2025, PMC12572822](https://pmc.ncbi.nlm.nih.gov/articles/PMC12572822/)
- In HCP-YA BMI: 3D CNN on VBM (lockbox R² 0.442) vs random forest on atlas ROIs (lockbox R² 0.031), with elastic net and TabNet below 0.07. — [Cooper 2025, bioRxiv](https://www.biorxiv.org/content/10.1101/2025.04.11.648433v1.full)
- An ROI-level elastic net on BMI (Developmental Cognitive Neuroscience 2021) found 64% of selected structural ROIs negatively related to BMI. — [PMC8066422 figure](https://pmc.ncbi.nlm.nih.gov/articles/PMC8066422/figure/fig0010)
- dHCP: geometric surface DL vs traditional (image-projected) DL advantage is task-dependent. — [Fawaz 2021 bioRxiv](https://www.biorxiv.org/content/10.1101/2021.12.01.470730.full.pdf)

### Inferences
- The literature points two ways. Finer resolution helps (vertex beats ROI), but surface pipelines capture less body-size variance than volume pipelines, probably because VBM includes white matter, CSF and head size, and skull or adiposity-related intensity effects. A surface model in HCP-YA may therefore fall short of Cooper's 3D CNN. A fair novelty framing is "surface-specific (thickness, myelin, curvature) signal for BMI, deconfounded from head size", rather than "best BMI predictor".
- A head-to-head design on the same HCP-YA subjects and family-aware folds would itself be a contribution, since no such comparison was found. It would run surface DL against vertex-wise BLUP/ridge, ROI ridge or elastic net, and a voxel 3D CNN.

### Gaps
- I found no published comparison of native surface DL vs voxel CNN vs ROI models for BMI.
- I did not find Couvy-Duchesne's ROI-vs-vertex R² specifically for BMI (it is in the supplement).
- I did not verify whether Cooper 2025 has been peer-reviewed since April 2025.
