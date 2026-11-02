# CNN BMI prediction from head MRI: Cooper 2025 methods and extracranial-shortcut prior work

Verification legend: [FT] = read in full text (via WebFetch extraction of the full HTML page); [ABS] = abstract / index record / search snippet only; [INF] = my inference.

## Q1. Cooper, Elsayed, Owens, MacKillop 2025: exact pipeline

### Takeaway
Cooper 2025 did NOT feed raw or whole-head T1w images to the CNN. It used SPM12 VBM grey-matter maps (warped to MNI-152, modulated, 10 mm FWHM smoothed, 1.5 mm, 121x145x121), following Abrol et al. 2021, into a 5-conv-layer AlexNet-style 3D-CNN. N = 1,106 HCP young adults; ~80/20 family-grouped lockbox split; lockbox R2 = 0.442 for the CNN (the abstract's "0.325" is the CV mean) against R2 < 0.07 for atlas-feature RF/EN/TabNet. No MAE, no motion QC criteria, no extracranial-tissue check, and no mention of twins beyond the Family-ID grouping.

### Cited Findings
- Published version: "Deep learning using structural MRI dramatically improves cross-validated prediction accuracy of body mass index", *Brain Mechanisms* vol. 151, article 202524, DOI 10.1016/j.bramec.2025.202524, dated 1 Feb 2026. The title changed from "massively improves" in the preprint. [ABS] — [McMaster Experts record](https://experts.mcmaster.ca/display/publication3800984). The ScienceDirect page (pii S3050642525000405) returned 403, so the published full text was not checked. Numbers below come from the bioRxiv v1 full text.
- Preprint record: bioRxiv 10.1101/2025.04.11.648433, first posted 18 Apr 2025, CC BY-NC-ND. [ABS] — [Europe PMC PPR1006554](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1101/2025.04.11.648433&format=json&resultType=core)
- Data: HCP S1200 (1,206 subjects, aged 22–35). The CNN sample was 1,106 after removing subjects who "failed MRI quality control" or were missing sMRI or BMI. Comparator models used N = 1,099, after dropping 7 more for missing demographics. BMI came from self-reported height and weight. There were no underweight subjects; groups were healthy (18.5–25) vs overweight (≥25). [FT] — [bioRxiv full text](https://www.biorxiv.org/content/10.1101/2025.04.11.648433v1.full)
- Image QC: the paper reports no specific motion or image-QC criteria beyond "failed MRI quality control", presumably HCP's own QC flags [INF]. [FT] — [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.04.11.648433v1.full)
- CNN input: the pipeline follows Abrol et al. (2021). Images were segmented with SPM12 VBM, and only grey-matter maps were used, "warped, modulated, and smoothed using a Gaussian Kernel with a full width half max of 10mm". Maps were registered to MNI-152 at 1.5 mm isotropic, 121 x 145 x 121. The paper does not say which T1w file was the starting image (HCP minimally preprocessed vs. unprocessed), and it says nothing about explicit skull-stripping or cropping. [FT] — [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.04.11.648433v1.full)
- CNN covariates: the CNN used GM arrays only, with no age, sex or ICV entered. [FT] — [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.04.11.648433v1.full)
- Architecture and training: AlexNet-based 3D-CNN with 5 conv layers in PyTorch, adapted from Abrol et al. 2021. Training used MSE loss and Adam (momentum 0.9). The random search covered LR 1e-4 to 0.05, batch size 8/16/32, weight decay 1e-4 to 0.5 and dropout 0.3 to 0.8. Early stopping used patience 40 with a 200-epoch maximum, plus an LR scheduler. [FT] — [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.04.11.648433v1.full)
- Splits: a roughly 80/20 train/lockbox split "conducted on the Family ID variable", so relatives stay on one side. Inside training they ran 5-fold CV repeated 3 times (15 outer folds), with nested 3-fold random-search tuning selected by mean MSE. The best of the 15 fold models was applied once to the lockbox, and all model types shared the same splits. Exact train and lockbox N are not reported. Whether the inner CV folds were also family-grouped was not confirmed in text. [FT] — [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.04.11.648433v1.full)
- Comparator features: RF, elastic net and TabNet used demographics (sex, age, years of education, household income, intracranial volume) plus atlas-based cortical thickness, surface area and subcortical GM volumes (FreeSurfer-type ROI features). Each was also run with covariates only and with atlas features only. The ROI feature count is inconsistent within the paper: 255 in Methods 2.2.7, 153 in Results 3.2.2. [FT] — [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.04.11.648433v1.full)
- Results [FT] — [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.04.11.648433v1.full):
  - 3D-CNN: CV mean R2 = 0.325; lockbox R2 = 0.442.
  - RF with atlas + covariates: CV R2 = 0.063; lockbox R2 = 0.031.
  - Covariates only: RF R2 = 0.021, EN R2 = 0.011.
  - Adding ROI features: about 0.05 for both RF and EN (the text does not say whether CV or lockbox).
  - TabNet: R2 fell from 0.010 to −0.035 when ROI features were added.
  - Abstract: comparators "R2s < .07" in the lockbox.
  - Using CNN-extracted features (255): RF lockbox R2 = 0.485 (CV 0.383); EN lockbox R2 = 0.456 (CV 0.395).
  - No MAE and no model-level Pearson r are reported. Table 2 (lockbox metrics) did not appear in the extracted HTML text.
- Internal inconsistency: the abstract (preprint and published record) says lockbox R2 = .325, but Results attribute .325 to the CV mean and .442 to the lockbox. [FT] — [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.04.11.648433v1.full); [McMaster record](https://experts.mcmaster.ca/display/publication3800984)
- Explainability: they used "GRAD-RAM", a regression Grad-CAM. Gradients go into the final conv layer, ReLU is not applied, maps are z-normalised and thresholded at z > 2, then labelled with AAL on lockbox subjects. Regions highlighted in both BMI groups:
  - occipital (calcarine, lingual), fusiform, precuneus, posterior cingulum
  - cerebellum, hippocampus
  - caudate, putamen, pallidum, thalamus
  - mostly right-lateralised
  
  Insula appeared only in the healthy-weight group, and inferior temporal and parahippocampal gyri only in the overweight group. A t-SNE of CNN features was related to delay discounting, cognition, gait speed, dexterity and alcohol use. [FT] — [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.04.11.648433v1.full)
- Observed correlations of BMI with behaviour: delay discounting ρ = −0.252, total cognition r = −0.269, gait speed r = −0.143, dexterity r = −0.233, alcohol ρ = 0.097 (p = 0.167). [FT] — [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.04.11.648433v1.full)
- Limitations the authors list: small sample for deep learning, and cross-sectional design. They do not mention extracranial tissue, twins or motion. [FT] — [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.04.11.648433v1.full)
- Code: https://github.com/PBCAR/3DCNN_BMI (53 commits). Scripts are `Cleaning_data_bmi.py` (train/test split), `CNN_split.py` (nested folds), `Run_CNN_Fold.py`, `Run_Final_CNN_Fold.py`, `Run_Lockbox_CNN.py`, plus `models_tune.py` and `utils_tune.py` adapted from Abrol 2021. RF, EN and TabNet code sits under `ML_BMI/`. The README does not describe preprocessing or family handling; I did not open the scripts. [FT of README] — [GitHub](https://github.com/PBCAR/3DCNN_BMI)

### Inferences
- [INF] Because the CNN input is a modulated GM tissue-probability map, scalp fat, skull, neck and face are largely removed by segmentation. A direct extracranial shortcut is therefore much less plausible than with raw T1w input.
- [INF] Residual non-brain routes remain possible:
  - Misclassification of meninges, dura, venous sinuses or orbital fat as GM.
  - 10 mm smoothing that blurs boundary signal.
  - Modulation, which encodes head size / ICV and total GM volume. These track body size and sex and were not regressed out of the CNN.
  - T1 intensity or segmentation differences driven by adiposity, such as field inhomogeneity in larger heads.
- [INF] Grad-CAM from the final conv layer has very coarse resolution, upsampled from a small grid. AAL labelling of thresholded blobs cannot rule out edge or boundary signal.
- [INF] A study on whole-head vs brain-masked vs GM-only inputs, with saliency mass inside vs outside the brain, would not duplicate Cooper 2025. Cooper never tested raw or whole-head input.
- [INF] The large CNN-vs-atlas gap (R2 0.44 vs <0.07) itself suggests the CNN uses information that ROI morphometry does not capture. That fits either genuine fine-grained GM patterns or global, size- or boundary-related cues, which is a reason to run shortcut controls.

### Gaps
- I could not read the published *Brain Mechanisms* full text (HTTP 403). Numbers may have been revised; the abstract still says R2 = .325.
- Table 2 values (EN and TabNet lockbox R2) were not in the extracted text.
- Exact train/lockbox N, inner-fold family grouping, and the T1w source file (`T1w_acpc_dc_restore` vs raw) were not confirmed. The GitHub scripts were not inspected.
- The last ~12.7k characters of the bioRxiv page (likely references and supplement) were not read.

## Q2. Prior work on extracranial tissue (scalp, face, neck fat) as a BMI signal, or skull-stripped vs whole-head BMI CNNs

### Takeaway
I found no study that predicts BMI from extracranial tissue on head MRI, and none that compares skull-stripped vs whole-head (or brain-masked vs extracranial-only) inputs for a BMI CNN. Separately, head soft tissue clearly carries adiposity signal: DXA head fat % vs BMI r ≈ 0.43–0.67, and MRI facial soft-tissue thickness rises with BMI. The shortcut is therefore plausible, and to my search, untested for BMI.

### Cited Findings
- Vakli et al. 2020, *Front Neuroinform* 14:10, UK Biobank [FT] — [Frontiers full text](https://www.frontiersin.org/journals/neuroinformatics/articles/10.3389/fninf.2020.00010/full):
  - Sample: N = 17,938, split 13,938 / 2,000 / 2,000 at random.
  - Input: UKB FSL pipeline images (gradient-distortion corrected, FOV-cropped, skull-stripped, nonlinearly registered to MNI152), downsampled to 2 mm (91x109x91). The IXI transfer set was SPM12-normalised and skull-stripped.
  - Results: test R2 = 0.46 without age/sex (MAE 2.41, RMSE 3.20, r = 0.70); R2 = 0.44 with age/sex (MAE 2.48, r = 0.68).
  - Saliency (regression Grad-CAM without ReLU, averaged over the test set, |Z| > 2): left caudate, left medial temporal / amygdala region, right lateral temporal cortex including the middle temporal gyrus.
  - The paper does not discuss scalp, skull or extracranial signal, or shortcut learning.
- Finkelstein et al. 2024, *Human Brain Mapping*: ensemble DNN predicting BMI from structural brain MRI, applied to the DIRECT-PLUS 18-month lifestyle trial. Reductions in predicted BMI tracked weight loss, and XAI regions for BMI differed from those for age. [ABS] — [UK Biobank publication page](https://www.ukbiobank.ac.uk/publications/deep-learning-based-bmi-inference-from-structural-brain-mri-reflects-brain-alterations-following-lifestyle-intervention/); [BGU listing](https://www.bgu.ac.il/en/researcher/galia-avidan/publications/324431727/). The full-text PDF returned 403, so their preprocessing (skull-stripping?) was not verified.
- Cooper 2025 cites only two prior deep-learning studies of obesity phenotypes from MRI, one being Vakli 2020. [ABS] — [search snippet of bioRxiv](https://www.biorxiv.org/content/10.1101/2025.04.11.648433.full.pdf)
- Head fat vs BMI, DXA not MRI:
  - Gorniak, Meng, Yazdekhasti, Pollonini 2024, *Exp Biol Med*: NHANES 2005–06, N = 2,921 aged 8–19, DXA head-region fat % vs BMI r = 0.432. The authors frame this as a confound for functional neuroimaging (fNIRS). [FT] — [PMC10940915](https://pmc.ncbi.nlm.nih.gov/articles/PMC10940915/)
  - Gorniak, Meng, Pollonini 2022, *Human Movement Science*, adults 20–89: head subcutaneous fat % vs BMI r = 0.668. This attribution comes from the 2024 paper, and the r assignment is slightly ambiguous. [ABS] — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S016794572200077X); [PMC10940915](https://pmc.ncbi.nlm.nih.gov/articles/PMC10940915/)
- Facial soft-tissue thickness on MRI rises with BMI (forensic literature) [ABS] — [Arslan et al. 2026 Turkish children MRI](https://avesis.ankara.edu.tr/yayin/8c40176f-29ec-41a2-97d9-37f7e13ce84f/facial-soft-tissue-thickness-in-the-sub-adult-population-of-turkiye-mri-based-assessment-and-its-correlation-with-body-mass-index-bmi); [Taiwan adults, NTU](https://scholars.lib.ntu.edu.tw/handle/123456789/160965); [Iranian adults, Tabriz](https://dspace.tbzmed.ac.ir/xmlui/handle/123456789/46118):
  - Taiwan adults: BMI was the strongest determinant of FSTT, with increases at all landmarks.
  - Arslan 2026: children at the ≥85th/95th BMI percentile had higher FSTT (p < 0.001).
- Posterior cervical subcutaneous fat (neck) correlates with BMI only moderately, mainly at C7. [ABS] — [PMC9997731](https://pmc.ncbi.nlm.nih.gov/articles/PMC9997731/)
- A search for UK Biobank head/neck adiposity from brain-MRI deep learning found only body-composition models on neck-to-knee Dixon MRI (e.g., MIMIR). None used brain-protocol T1 scalp or neck tissue. [ABS] — [MIMIR, Radiology: AI](https://pubs.rsna.org/doi/full/10.1148/ryai.210178)

### Inferences
- [INF] Scalp, temporal and facial subcutaneous fat is visible and bright on T1w, and it correlates with BMI at roughly r 0.4–0.7, close to Vakli's r = 0.70. A whole-head CNN could plausibly reach similar or higher accuracy from extracranial tissue alone. This is the core motivation for a brain-vs-extracranial study.
- [INF] Even "skull-stripped" UKB images (Vakli) can keep residual extracranial voxels, and brain-mask boundaries may themselves differ with head adiposity.
- [INF] Novelty: as far as this search found, a systematic BMI study comparing (a) whole-head, (b) brain-masked, (c) extracranial-only and (d) GM-map inputs, with saliency-mass-outside-brain metrics, appears novel.

### Gaps
- I did not find any MRI study that directly measured scalp or temporal subcutaneous fat thickness and correlated it with BMI. The head-fat evidence is DXA (NHANES) or forensic facial MRI. A targeted PubMed search such as "scalp thickness MRI obesity" or "temporal fat pad MRI BMI" may still find one.
- ABCD-specific BMI CNN studies were not found in this search window.
- The Finkelstein 2024 preprocessing and the name of the second deep-learning obesity study cited by Cooper were not verified.

## Q3. Analogous shortcut learning in neuroimaging CNNs (non-brain tissue, preprocessing artefacts)

### Takeaway
Direct evidence exists for Alzheimer's classification: skull-stripping induces a contour/volume shortcut, and some unstripped models put relevance on the skull. For brain age, a large clinical study found raw (unstripped) T2 input performed slightly better than skull-stripped input, while claiming saliency ignored extracranial tissue. Head size is a documented confound in sex CNNs. I found no paper that explicitly quantifies extracranial reliance for brain age or sex in T1 CNNs.

### Cited Findings
- Tinauer, Sackl, Stollberger, Schmidt, Ropele, Langkammer 2025, "Skull-stripping induces shortcut learning in MRI-based Alzheimer's disease classification", arXiv 2501.15831; published in *Insights into Imaging* (10.1186/s13244-025-02158-4) [FT of arXiv v4] — [arXiv HTML](https://arxiv.org/html/2501.15831); [Springer](https://link.springer.com/article/10.1186/s13244-025-02158-4):
  - Data: ADNI-2, 990 AD and 990 CN scans; 3D CNN of about 0.3M parameters; LRP heatmaps.
  - Accuracy: aligned unstripped 71.1% vs skull-stripped 81.6%. Binarised skull-stripped images still reached 78–82%, so gray/white texture contributes little and contour/volume cues from skull-stripping drive the model.
  - External cohort (ASPS/ProDem): accuracy dropped about 9–13%, with binarised models near chance.
  - Some unstripped (D1) models' heatmaps highlighted skull regions (Supplementary 5).
- The same paper cites related shortcut work: Lapuschkin 2019 (Clever Hans); Wallis & Buvat 2022 (Clever Hans in a brain-tumour MRI dataset); Vásquez-Venegas 2024 (scoping review of Clever Hans in medical imaging); Dinsdale 2021 and Hofmann 2022/2025 (brain age heatmaps). I saw these by title only. [FT, citations only] — [arXiv HTML](https://arxiv.org/html/2501.15831)
- Wood et al. 2022, *NeuroImage*, "Accurate brain-age models for routine clinical MRI examinations": raw T2 scans MAE 3.05 y vs HD-BET skull-stripped 3.65 y. The authors state that training at scale let models "ignore irrelevant features such as extra-cranial tissue". [ABS, search snippet] — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1053811922000015)
- Adeli et al. 2020, *NeuroImage*, ABCD sex classification: head size accounts for much of the apparent sex difference. Matching on head size dropped accuracy from about 89.6% to 87.3%, and they derived confounder-free saliency. [ABS] — [PMC7780846](https://pmc.ncbi.nlm.nih.gov/articles/PMC7780846)
- 2024 multi-cohort age/sex 3D-CNN evaluation: saliency concentrated on brainstem, subcortical, limbic and insular regions. Whether off-brain saliency was tested is unknown. [ABS] — [PMC13342005](https://pmc.ncbi.nlm.nih.gov/articles/PMC13342005/)
- Yin et al. 2023, *PNAS*, interpretable brain-age CNN: used skull-stripped input with subject-level saliency. [ABS] — [PNAS](https://www.pnas.org/doi/10.1073/pnas.2214634120)

### Inferences
- [INF] The precedents show two things. Preprocessing choices (stripping or not, masking) change what CNNs learn. Unstripped models can exploit non-brain anatomy and stripped models can exploit mask contours. A BMI study should control for both, for example by comparing brain-only, extracranial-only and boundary-perturbed inputs.
- [INF] Wood 2022's raw > stripped result for brain age is consistent with extracranial tissue carrying predictive signal: scalp, muscle and fat change with age. Their "saliency ignores it" claim rests on qualitative maps.

### Gaps
- I did not find a brain-age or sex paper that quantitatively reports saliency mass outside the brain mask or trains on extracranial-only input. Dinsdale 2021 and Hofmann 2022 were not fetched, and there may be relevant MICCAI workshop papers.
- Wood 2022 numbers come from a snippet; the full text was not verified.

## Q4. Vakli 2020: skull-stripped? Saliency?

### Takeaway
Yes. Vakli 2020 used UK Biobank's FSL-processed, skull-stripped, MNI-registered T1s (2 mm). Saliency (regression Grad-CAM) highlighted the left caudate, left amygdala / medial temporal region and right lateral temporal cortex. The paper never discusses extracranial signal.

### Cited Findings
- Vakli's UKB images were gradient-distortion corrected, cropped, skull-stripped and nonlinearly registered to MNI152, then downsampled to 91x109x91 at 2 mm. The specific brain-extraction tool is not named beyond "FSL tools". [FT] — [Frontiers](https://www.frontiersin.org/journals/neuroinformatics/articles/10.3389/fninf.2020.00010/full)
- Architecture: separable-convolution 3D CNN with about 231k parameters; age and sex optionally concatenated at the fully connected layer.
- Test N = 2,000: R2 0.46 / r 0.70 / MAE 2.41 without age and sex; R2 0.44 with them.
- Saliency: left caudate, left medial temporal / amygdala region, right lateral temporal cortex including the middle temporal gyrus.
- FreeSurfer follow-up in a 200-person subset:
  - Left amygdala volume vs BMI r = 0.19 (p = 0.008).
  - Caudate n.s. (r = 0.028).
  - Right isthmus cingulate surface area survived FDR correction.
  
  [FT] — [Frontiers](https://www.frontiersin.org/journals/neuroinformatics/articles/10.3389/fninf.2020.00010/full)
- There is no discussion of skull, scalp or extracranial tissue, nor of head-size or registration confounds. [FT, first ~100k chars] — [Frontiers](https://www.frontiersin.org/journals/neuroinformatics/articles/10.3389/fninf.2020.00010/full)

### Inferences
- [INF] The right lateral temporal / middle temporal gyrus saliency lies near the temporalis muscle and temporal fat pad. At 2 mm with coarse Grad-CAM, residual non-brain tissue near the mask edge cannot be excluded. This is a concrete hypothesis a novelty study could test.

### Gaps
- The last ~24k characters of the Vakli page (probably references and supplement) were not read.
