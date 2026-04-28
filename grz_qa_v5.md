# GraphRAG Zero V2 — Questions & Answers

**Corpus:** Leukemia Drug Discovery — 3,071 Papers  
**Questions:** 100 (50 Global + 50 Local)  
**Avg Latency:** 21.1s | **Total:** 35.2 min  
**Success Rate:** 100/100 (100%)

---

# Global Questions (Cross-Document Synthesis)

---

## G1. [GLOBAL] How do different in vitro assays link treatments to cell-cycle, apoptosis, and adhesion changes?

*ID: 7c50c22e-4b3... | Latency: 40.2s*

**Answer:**

In vitro studies typically link a *treatment* to downstream *cell-cycle, apoptosis, and adhesion* phenotypes by combining (1) **gross growth/viability readouts** with (2) **mechanism-facing phenotypic assays** (flow cytometry, imaging, invasion/adhesion formats) and (3) **molecular confirmation** (e.g., western blot/protein arrays). A common workflow is: first establish dose–response effects on growth/viability, then test whether growth inhibition reflects **cell-cycle arrest** and/or **apoptotic death**, and finally test whether the same treatments also perturb **cell adhesion/migration/invasion** phenotypes (and their molecular correlates) [Data: Sources (184909, 185103, 109, 249483, 176698, +more)].

### Linking treatments to cell-cycle changes
**DNA-content flow cytometry (PI incorporation)** is used to quantify the fraction of cells in **G0/G1, S, and G2/M** and infer arrest/accumulation in specific phases after treatment [Data: Sources (176698, 43930, 241634, 265535, 333175, +more)]. In colorectal cancer cells, compounds “3a” and “3b” caused strong **G0/G1 accumulation** in cancer lines (Caco2, HCT-116) with little effect on a non-transformed line (841 CoN), supporting a treatment-linked cell-cycle arrest that is selective for tumour cells in that context [Data: Sources (176698, 176696)]. Cell-cycle interpretation can break down when apoptosis is high: in one combination-treatment setting, cell-cycle phase distributions were described as **unreliable due to increased apoptosis**, highlighting a known limitation where extensive sub-G1/fragmentation complicates phase calling [Data: Sources (333177)].

Cell-cycle assignment is frequently strengthened by measuring **cell-cycle regulatory proteins** (cyclins, p27, pHH3) alongside PI profiles, so that a treatment-associated phase shift (e.g., G0/G1 increase) is supported by corresponding marker changes [Data: Sources (176698)]. This “phenotype (PI) + mechanism (protein markers)” pairing is also used in other systems, e.g., to confirm drug-induced cell-cycle perturbations and checkpoint/progression effects [Data: Sources (254465, 310081)].

### Linking treatments to apoptosis
Apoptosis is commonly connected to treatments using **Annexin V-based flow cytometry**, exploiting phosphatidylserine exposure: viable cells are Annexin V−/PI−, early apoptotic are Annexin V+/PI−, and late apoptotic/necrotic are Annexin V+/PI+ [Data: Sources (185051, 185053, 185197, 265535, 241634, +more)]. This approach is used both as a primary apoptotic endpoint and as a validation that reduced viability reflects apoptotic death rather than only metabolic suppression or membrane rupture [Data: Sources (185197, 241634)].

Apoptosis can also be linked with **caspase assays** (e.g., NucView caspase-3 by flow cytometry; kinetic caspase 3/7 live imaging), which provide a functional “executioner caspase” readout that can be used to pick doses that significantly induce apoptosis and then carry those doses into downstream cell-cycle and morphology assays [Data: Sources (50398, 50345, 32520, 109)]. Molecular confirmation is commonly done by western blotting for markers such as **cleaved PARP and cleaved caspase-3**, and pro-/anti-apoptotic proteins; in the 3a/3b example, cleaved PARP/RIP/caspase-3 increased in cancer lines but not in normal cells, aligning apoptosis markers with selective treatment response [Data: Sources (176696, 176697)]. Mitochondrial involvement may be probed by **JC-1 mitochondrial membrane potential** loss, linking a treatment to intrinsic-apoptosis initiation upstream of caspase activation [Data: Sources (33242, 156396)].

Importantly, datasets also highlight practical interpretation issues: shifts in Annexin V populations may be visually apparent yet not statistically significant due to variability between repeats, and treatment effects may differ strongly across cell lines (e.g., smaller apoptotic shifts in one line vs another) [Data: Sources (185198, 185197)].

### Linking treatments to adhesion/migration/invasion changes
Adhesion and motility phenotypes are commonly connected to treatments using **matrix-coated adhesion assays** (e.g., collagen-, fibronectin-coated plates), **Boyden chamber migration/invasion assays** (±Matrigel), and **scratch/wound-healing** assays [Data: Sources (249483, 314095, 241305, 33362, 31947, +more)]. In one adhesion assay format, cells were pretreated with drugs (e.g., cisplatin or eribulin) before plating onto BSA or collagen, then adherent cells were stained with crystal violet and quantified by absorbance—directly mapping treatment history to subsequent adhesion capacity [Data: Sources (249483)]. Migration/invasion assays similarly connect treatment to the number of cells traversing a porous membrane toward a chemoattractant (e.g., HGF), with Matrigel introducing an invasion barrier [Data: Sources (314095)].

These phenotypes are often paired with molecular “adhesion/invasion machinery” measurements. For example, a kinase inhibitor (CX-4945) showed dose-dependent and even biphasic invasion effects, which were linked to altered levels of MMPs (e.g., MMP-7, MMP-9, MMP-2), supporting a mechanistic bridge from drug → invasion phenotype → matrix-remodelling enzymes [Data: Sources (31905, 31906)]. More broadly, adhesion-dependent control of proliferation is also noted: integrin engagement and cell spreading regulate G1 progression through pathways such as FAK phosphorylation, providing a conceptual link between adhesion assays and cell-cycle readouts when treatments perturb adhesion signalling [Data: Sources (144852, 144854)].

### How the assays work together to make a “linked” claim
A robust linkage usually comes from *concordant readouts* across layers: (i) viability/cytotoxicity screens (ATP, MTT/resazurin, LDH) establish potency and exposure windows [Data: Sources (333994, 264149, 114341, 242698)]; (ii) PI cell-cycle profiling and Annexin V/caspase assays attribute growth inhibition to arrest vs apoptosis [Data: Sources (43930, 185053, 50398, 265535)]; and (iii) western blot/protein profiling connects these phenotypes to pathway markers (cell-cycle regulators, cleaved PARP/caspases, junction/adhesion proteins) [Data: Sources (176698, 176696, 326236)]. Finally, adhesion/migration/invasion assays test whether treatments also reprogram cell–ECM behaviours that matter for metastasis and tissue interaction, sometimes revealing non-intuitive dose effects that viability assays alone would miss [Data: Sources (31905, 249483, 314095)].

---

## G2. [GLOBAL] What types of quantitative endpoints are reported to support scientific claims?

*ID: ed054793-0a1... | Latency: 40.2s*

**Answer:**

Quantitative endpoints reported to support scientific claims span **measured properties/effects** (what was observed) and **statistical/derived metrics** (how strongly and reliably the observation supports the claim), across in vitro, in vivo, clinical, and real‑world contexts.

### 1) Experimentally measured (biological/toxicological) endpoints
Studies report numeric outputs from specific assays and biological models, including:
- **Cytotoxicity and cell-death related measures**, ideally defined at the level of a specific measurement such as **percent apoptotic cells** or **percent dead cells**, and sometimes grouped under broader terms like “cytotoxicity” [Data: Sources (53001, 52999)].  
- **Dose/concentration–response summary statistics** such as **LC50**, **EC25**, and **LOAEL/LOEL** (lowest observed (adverse/effect) level) [Data: Sources (53006, 53007, 213154, 242743, +more)]. Some nano-toxicity work reports endpoints like **EC25 expressed in surface-area concentration units** (e.g., mm²/mL) [Data: Sources (53098, 43548)].  
- **Organism-level lethal and sub-lethal endpoints** such as embryonic zebrafish **mortality/excess lethality at specific times (e.g., 24 vs 120 hpf)**, with binary labels often derived from LOEL thresholds [Data: Sources (213064, 213161)].  
- **Genotoxicity/mutagenicity endpoints**, e.g., **log(TA100)** where TA100 is mean mutant counts in the Salmonella microsome test at a specified dose [Data: Sources (53095, 53096)].  
- **Physiological/cardiovascular endpoints** such as **QT/QTc**, **QRS**, **T-wave morphology**, **heart rate**, **blood pressure**, and **contractility**, often linked to exposure–response analyses [Data: Sources (90006, 90010)].  
- **Biomarker and omics/metabolite endpoints**, including quantitative changes in endogenous metabolites (metabolites, lipids, proteins/peptides) used to evidence drug effects or target engagement [Data: Sources (12372, 12329, 12089)].  

### 2) Clinical and trial endpoints (patient outcome measures)
To support clinical claims, studies report endpoints such as:
- **Time-to-event outcomes** including **overall survival (OS)**, **progression-free survival (PFS)**, **event-free survival (EFS)**, and **duration of response** [Data: Sources (63199, 138916)].  
- **Binary or categorical response endpoints** (e.g., responder proportions, complete/partial/overall response) and disease relapse [Data: Sources (63199, 274893)].  
- **Adverse-event endpoints**, including counts/proportions of patients with **AEs/SAEs**, and **graded laboratory abnormalities** (e.g., worsening to grade 3–4) [Data: Sources (63199, 215205)].  
- **Patient-reported outcomes (PROs)/quality-of-life instruments**, where endpoints are changes in validated scale scores (e.g., EORTC QLQ-C30) [Data: Sources (63199, 274893, 41175)].  

### 3) Real‑world / observational quantitative endpoints
Some claims are supported using post‑marketing data with:
- **Adverse-event signal metrics** such as **empirical Bayes geometric mean (EBGM)** with thresholds like **EB05 > 2** [Data: Sources (209803)].  
- **Incidence rates** of outcomes (e.g., cardiac dysrhythmia) normalized by exposure (e.g., patient‑years) when claims data allow denominators [Data: Sources (209828)].  

### 4) Statistical endpoints used to justify and quantify claims
Across domains, scientific claims are quantitatively supported by reporting:
- **Effect sizes and uncertainty**: confidence intervals (CIs), prediction intervals, standard deviation (SD), standard error (SEM), and explicit effect size measures (e.g., Cohen’s d, Pearson’s r) [Data: Sources (102030, 213698, 206430)].  
- **Significance testing outputs**: exact **p-values**, test statistics (t, F, r), degrees of freedom, and multiple‑testing corrections (e.g., FDR q-values, Bonferroni) [Data: Sources (201599, 213698)].  
- **Model/assay performance metrics**, including:
  - For regression models: **R²** and **standard error of estimate** [Data: Sources (53071, 53073)].  
  - For classification models: confusion‑matrix derived statistics (e.g., Cooper statistics) [Data: Sources (53075)].  
  - **Predictive checks** and uncertainty for model validation (e.g., **visual predictive checks**, percentiles with CIs) [Data: Sources (15459, 260983)].  
  - **Assay QC/hit thresholds** such as **Z′** and **SSMD** (e.g., SSMD |β| > 2 as a strong threshold) [Data: Sources (25895)].  

### 5) Quantitative endpoint specification details that are often reported
To make endpoints usable for scientific and regulatory inference, reports emphasize that endpoints should be clearly defined with:
- **Assay identity and experimental protocol details**, key experimental variables, and units (especially for numerical endpoints) [Data: Sources (52996, 53014)].  
- **Dose metric choice** (mass vs particle number vs surface area), including conversion when appropriate for nanomaterials [Data: Sources (53007, 53008, 53014)].

---

## G3. [GLOBAL] How do studies in the dataset connect molecular mechanisms to measurable phenotypes?

*ID: 2e0d51d5-c9c... | Latency: 30.1s*

**Answer:**

Studies in the dataset connect molecular mechanisms to measurable phenotypes by (1) translating gene- or variant-level signals into pathway/network hypotheses, and then (2) validating those hypotheses against quantitative or structured phenotype measurements (patient phenotypes, model-organism phenotypes, drug response markers, or cellular readouts).

A common strategy is **pathway/functional enrichment from affected genes** (e.g., from CNVs or differential expression), using resources like GO/KEGG, mouse knockout phenotypes (MGI), or co-expression networks (BrainSpan/GTEx), under the assumption that genes contributing to a phenotype act in shared biological pathways [Data: Sources (88501, 88390, 88468, 88828)]. Several studies then explicitly test whether inferred pathways “explain” phenotypes by checking whether individuals whose variants hit the same pathway are **more phenotypically similar** to each other than to non-contributing individuals (“phenotypic convergence”), turning pathway membership into a testable phenotype-level prediction [Data: Sources (88829, 88518, 88817, 88469)]. Protein–protein interaction data (e.g., DAPPLE) are used as an additional mechanistic layer to confirm that phenotype-associated gene sets form plausible molecular networks, rather than disconnected gene lists [Data: Sources (88505, 88488)].

Another recurrent bridge is **integrated functional networks that score gene–gene functional similarity**, specifically the Phenotypic Linkage Network (PLN). Here, heterogeneous molecular evidence (co-expression, PPIs, GO annotations, co-citation, and mouse phenotypes transferred by orthology) is combined into a single weighted similarity between genes; the network is trained/weighted using semantic similarity of phenotype ontologies (mouse phenotypes; then calibrated to human phenotypes via HPO), yielding edges intended to reflect shared phenotypic effects in humans [Data: Sources (88445, 88448, 88449)]. These gene–gene similarity scores are then used to identify **functional clusters** in CNVs (or genome-wide), and cluster “hits” are tested for associations with pathogenicity and for similarity of patient phenotypes across different CNVs that affect the same cluster (linking molecular connectivity to observed clinical outcomes) [Data: Sources (88811, 88737, 88663)].

Several chunks also show studies connecting mechanism to phenotype via **directional causal knowledgebases**. For example, Ingenuity Pathway Analysis (IPA) uses literature-curated causal gene→function relationships and observed fold-changes to compute predicted activation states of functional terms (e.g., migration/invasion, proliferation, viability), effectively mapping transcriptional change to higher-level phenotypic programs and disease-relevant functions [Data: Sources (15341, 15369)].

The dataset also contains examples where the phenotype is **directly quantitative and proximal to biochemistry**, especially in pharmacogenomics: plasma concentrations of drug metabolites are treated as precise quantitative phenotypes that sit close to underlying biochemical pathways (ADME), enabling clearer links between genetic variation in metabolic enzymes and measurable response markers (and then, separately, evaluation of downstream clinical response/ADRs) [Data: Sources (192435, 192438, 192454)].

Finally, some studies connect mechanisms to phenotypes through **high-dimensional cellular or single-cell readouts** plus modeling. Examples include pseudotime/trajectory models that compress gene expression into a latent “progression” axis and explicitly model covariate-by-trajectory interactions (linking context-dependent regulatory programs to disease progression phenotypes) [Data: Sources (94377, 94379, 94413)], and machine-learning approaches that extract hundreds of image-derived cellular features and identify small feature sets predictive of functional delivery outcomes (linking perturbations to multivariate phenotypic signatures) [Data: Sources (266314, 266315)].

---

## G4. [GLOBAL] Which therapeutic areas and pathogens are targeted by interventions described in the dataset?

*ID: 14c42a49-cb4... | Latency: 40.1s*

**Answer:**

## Therapeutic areas represented

The interventions in the dataset primarily fall into **anti-infectives**, spanning bacterial, viral, fungal, and parasitic diseases, with some emphasis on **antimicrobial resistance (AMR)** and **host-directed/anti-virulence strategies** as alternatives or adjuncts to conventional antimicrobials [Data: Sources (81014, 81015, 81024, 310525, 218954, +more)]. Additional clinical contexts include **infections in high-risk/immunocompromised populations** (e.g., neutropenic patients; neonatal sepsis) where prophylaxis, empiric therapy, diagnostics, and stewardship are key intervention areas [Data: Sources (112545, 60263, 201238, 201241, 112566, +more)].

## Bacterial pathogens and syndromes targeted

A major focus is **bacterial infection under AMR pressure**, including interventions aimed at the **ESKAPE pathogens**—*Enterococcus faecium, Staphylococcus aureus, Klebsiella pneumoniae, Acinetobacter baumannii, Pseudomonas aeruginosa,* and *Enterobacter* spp.—via alternative approaches such as bacteriophages, nanoparticles, photodynamic therapy, antimicrobial peptides, and host-based therapies that enhance macrophage/neutrophil killing [Data: Sources (81024, 81015, 310525, 222412, 192712, +more)].

Specific pathogen/disease foci include:
- **Clostridioides difficile infection (CDI)**, including pathogen-directed targets (toxins, adhesins, biofilms, spores, p-cresol pathway, fatty acid synthesis FabK) and host-directed targets (VEGF-A receptor, innate immunity, intestinal ion channels, microRNA therapeutics) [Data: Sources (203035, 203046, 203106, 153932)].
- **Pseudomonas aeruginosa infections**, including “Trojan horse” siderophore–antibiotic strategies (e.g., cefiderocol conceptually) and antivirulence/quorum-sensing interference (e.g., QSS/PqsR antagonism) [Data: Sources (29562, 280126, 310520, 310525)].
- **Shigellosis and invasive enteric bacterial disease**, especially **MDR/XDR *Shigella* spp.** (including *S. flexneri* and *S. sonnei*), with repurposing/assessment of oral carbapenems such as **tebipenem** as an alternative therapy; broader enteric panels include non-typhoidal *Salmonella*, *Campylobacter*, and pathogenic *E. coli* [Data: Sources (215423, 215448, 215489, 215542)].
- **Tuberculosis**, including **Mycobacterium tuberculosis** (with work on profiling drug responses, PK/PD modeling, and intensified regimens for tuberculous meningitis) [Data: Sources (66217, 227780, 230338, 291115)].
- **Neonatal sepsis pathogens**, with analyses explicitly involving **E. coli, K. pneumoniae, and S. aureus** isolates (and antibiotic options such as meropenem, fosfomycin, colistin in simulations) [Data: Sources (201241, 201238, 201256)].

## Viral pathogens targeted

The dataset includes **dengue virus**, with therapeutic/chemoprophylaxis efforts focused on **small-molecule inhibitors of viral replication** [Data: Sources (152229)]. It also references **SARS-CoV-2/COVID-19** as a therapeutic area where host and viral targets and drug repurposing (including discussion of remdesivir) are considered [Data: Sources (81645, 176523)].

## Fungal pathogens targeted

Interventions include both pathogen- and host-directed approaches for **invasive fungal infections**, notably:
- **Candida albicans / candidiasis**, including antifungal anti-virulence strategies (e.g., targeting secreted hydrolytic enzymes like secreted aspartyl proteases) and interest in **Candida vaccines** [Data: Sources (218957, 218954, 772)].
- **Aspergillosis**, discussed in the context of immunomodulatory adjuncts in invasive fungal disease [Data: Sources (772)].
- **Cryptococcal meningitis**, including discussion of **exogenous interferon-gamma** as potentially beneficial in HIV-associated disease contexts [Data: Sources (769, 772)].

## Parasitic pathogens targeted

The dataset covers multiple parasitic therapeutic areas, including:
- **Malaria (Plasmodium spp., especially *Plasmodium falciparum*)**, including drugs/compounds targeting multiple lifecycle stages (liver, blood, gametocytes, transmission stages) and host-directed strategies (e.g., blocking host receptors CD68/CD81 for liver invasion; targeting host pathways such as MEK; host peroxiredoxin 6) [Data: Sources (68823, 265068, 265164, 100174)].
- **Kinetoplastid diseases**, including:
  - **Visceral leishmaniasis** caused by *Leishmania donovani* and *L. infantum* (drug discovery and intracellular macrophage-resident parasite challenges) [Data: Sources (153017, 3780)].
  - **Chagas disease** caused by *Trypanosoma cruzi* (compound screening concepts and proteasome-inhibitor work referenced) [Data: Sources (256971, 245866)].
  - **Human African trypanosomiasis** involving *Trypanosoma brucei* (bloodstream-form screening and BBB penetration as part of target product profiles) [Data: Sources (189135, 47788)].
- **Helminth infections**, including **schistosomiasis** and **soil-transmitted helminths** (*Ascaris lumbricoides, Trichuris trichiura, Necator americanus, Ancylostoma duodenale*) as areas with limited treatment options and ongoing need for new drugs [Data: Sources (189121, 189123)]. The dataset also describes **filarial disease** via anti-Wolbachia strategies (e.g., corallopyronins targeting Wolbachia endosymbionts) [Data: Sources (189133, 110237)].

---

## G5. [GLOBAL] What experimental methods are used to validate results across the dataset?

*ID: b774cf1f-f8b... | Latency: 40.2s*

**Answer:**

Across the dataset, results are validated using a mix of **resampling-based internal validation**, **explicit train/test splits (external validation)**, and **experimental/empirical cross-checks against independent observations**, often paired with **statistical significance and uncertainty quantification**.

### Resampling-based internal validation (cross-validation, LOOCV, bootstrap)
Many studies use **K-fold cross-validation** (commonly 5-fold, sometimes 10-fold or 3-fold) with performance aggregated across folds and often across multiple random seeds/partitions to stabilize estimates [Data: Sources (13848, 213081, 13847, 13860, 13836,+more)]. Several variants appear:
- **Stratified repeated K-fold CV** (e.g., 5 repetitions of 5-fold) with averaged metrics and averaged feature/descriptor importance across seeds [Data: Sources (13847, 13848, 13860)].
- **Nested (“external”) cross-validation**, where scaling, feature selection, and hyperparameter tuning are performed *within* each training fold to reduce optimistic bias [Data: Sources (213081, 213128, 43550, 302666)].
- **Leave-one-out CV (LOOCV)**, including “external LOOCV” where all model selection/tuning is performed only on the LOO training subset; some works repeat LOOCV multiple times due to algorithm randomness and report mean/SD/SE across repetitions [Data: Sources (43549, 43550, 43552)].
- **Bootstrap resampling** used either as an alternative validation estimate or to build **confidence intervals/standard errors** around out-of-sample loss or performance metrics [Data: Sources (53066, 120702, 120716, 234155, 234912)].

### Specialized partitioning to avoid leakage / optimistic bias
Several chunks emphasize that **random partitioning can be optimistic**, especially when related measurements can leak across train/test splits (e.g., same entity measured under multiple conditions) [Data: Sources (120687, 13849, 13863)].
- A concrete example is a **“remove temperature” pseudo-cross-validation** protocol that prevents solubility measurements of the *same material at different temperatures* from appearing in both train and test, addressing inflated performance seen with “vanilla” CV [Data: Sources (13848, 13849, 13863, 13921)].
- In structure-based virtual screening, validation includes **per-target CV** and more stringent split strategies (e.g., **cross-target/clustered splits** to avoid training/testing on highly similar targets) plus evaluation on **independent test sets** [Data: Sources (138530, 141067, 141068)].

### Hold-out test sets and “true” external validation / prospective validation designs
Beyond resampling, some studies explicitly split data into **training and dedicated validation/test sets**, emphasizing that a **hidden validation set** (data not used—or even collected—during training) provides higher confidence than cross-validation alone [Data: Sources (55979, 55978, 55981, 118501, 118502)].
- In nano-QSAR contexts, the text distinguishes **internal validation** (goodness-of-fit/robustness) from **external validation** (predictivity on unseen data) and notes that true external validation is often limited by data scarcity [Data: Sources (53059, 53080, 53081)].
- Some modeling workflows augment validation with **additional labeled external test molecules** drawn from later literature, alongside random hold-outs and/or 10-fold CV [Data: Sources (302667, 302669)].

### Permutation / randomization tests for chance correlation
To test robustness and rule out chance correlations, the dataset includes **Y-scrambling / response permutation** approaches, where the response labels are permuted many times and model quality under permutation is compared to the true model; importantly, the entire modeling protocol should be repeated during permutations for validity [Data: Sources (53069, 53070, 9869, 9868)].

### Statistical testing, multiple comparisons, and uncertainty reporting
Validation commonly includes not just point estimates but also **statistical inference**:
- Model comparisons based on **paired fold-wise RMSE** (or \(R^2\) in some scenarios), with **approximate p-values** and **multiple-comparison adjustments** (adjusted p<0.05), while acknowledging the approximate nature and potential overstatement of significance [Data: Sources (13850, 13851, 13861)].
- Broader reporting practices include specifying replication, sample sizes, normality checks, and multiple-testing corrections, plus reporting effect sizes and confidence intervals where appropriate [Data: Sources (201599, 102030, 213698)].

### Experimental/empirical validation against independent observations and protocols
In mechanistic and simulation-heavy parts of the dataset, “validation” is framed as comparing simulations to **experimental observations not used for parameter estimation**, ideally via **new experiments designed based on model predictions** (though this is described as uncommon at publication time) [Data: Sources (64383, 64384, 64388)].
- Practical guidance includes **overlaying simulation outputs with experimental data**, including variability (standard errors, confidence intervals, ensemble “shadows”) and using disagreements to drive model revision and new assay design [Data: Sources (64386, 64387, 64402)].
- Some infrastructures (e.g., electrophysiology “Web Lab” concepts) validate by running **different experimental protocols** than those used for fitting and systematically comparing protocol-matched predictions vs observed data [Data: Sources (29009, 28998, 29007)].

If you want, I can summarize these methods into a short checklist of “validation patterns” (internal, leakage-aware splitting, external, permutation-based, and experimental protocol-based) that recur across the dataset.

---

## G6. [GLOBAL] Which model systems are used to study disease, treatment, and biological function?

*ID: 69cea3e5-829... | Latency: 40.1s*

**Answer:**

A wide range of **experimental and computational model systems** are used to study disease mechanisms, treatment response, and core biological function, spanning **in vivo**, **in vitro/ex vivo**, and **in silico** approaches.

**In vivo animal and organism models** remain common for studying integrated physiology and treatment effects, particularly when whole-organism interactions matter. Rodents (especially mice) are widely used (including genetically engineered and transplantation tumour models for cancer) but may not fully translate due to species differences in physiology and gene regulation [Data: Sources (185073, 115844, 30878, +more)]. Alternative in vivo models include **zebrafish** (used for cardiovascular development/disease mechanisms and in vivo compound screening) and invertebrates such as **Drosophila melanogaster** and **Caenorhabditis elegans** (used in neurodegenerative disease research and high-throughput screening, albeit with limitations in recapitulating human pathophysiology) [Data: Sources (196053, 137436, 137437, 137438, +more)]. In cancer, mouse systems include **xenografts** (e.g., nude/SCID hosts), **genetically engineered/autochthonous tumour models**, and increasingly **humanized mice** to study immunotherapy where a human immune–tumour interaction is needed [Data: Sources (80532, 80554, 185072, 185073, +more)].

**Human cell–based models** are increasingly used to address translation limits of animals. **Human induced pluripotent stem cell (hiPSC) models** can be derived from patients or engineered (e.g., with CRISPR-Cas9) and differentiated into disease-relevant cell types (neurons, cardiomyocytes, hepatocytes, etc.) for mechanistic studies and drug testing [Data: Sources (97428, 137439, 137440, 39076, +more)]. In the cardiovascular space, **hiPSC-derived cardiomyocytes** and **engineered heart tissue (EHT) / 3D cardiac models** are used for disease modelling (arrhythmia, cardiomyopathy, heart failure), probing cell–cell interactions (e.g., fibroblast–cardiomyocyte interplay), and potential cardiotoxicity screening; these systems are positioned as more human-physiology–relevant and may reduce reliance on animal models (3Rs) [Data: Sources (307013, 307012, 307019, 55993, +more)].

Beyond 2D monolayers, **3D in vitro models** are used to better reproduce tissue-like gradients and microenvironments. Examples include **tumour spheroids** for solid tumour modelling and drug/nanoparticle penetration studies, as well as **organoids**, **hydrogel/ECM scaffold systems**, and **microfluidic organ-on-a-chip (microphysiological systems)** that enable controlled delivery of biochemical/mechanical cues and may support disease modelling and drug screening (including multiorgan interaction concepts) [Data: Sources (39202, 242700, 137441, 46857, +more)]. **Ex vivo models** such as **precision-cut tissue slices** preserve native cytoarchitecture and multiple cell types, aiming to better mimic in vivo-like metabolism and responses than simpler in vitro systems [Data: Sources (242702, 242703)].

**In silico/computational models** are used to study biological function and to predict treatment response, often complementing experiments. Mechanistic models include **ordinary differential equation (ODE)** systems (and sometimes **PDEs** for space-dependent phenomena), **agent-based models (ABMs)** for heterogeneous, spatially structured systems (e.g., tumours), and hybrid/multiscale approaches that combine multiple formalisms [Data: Sources (193598, 193664, 193665, 188496, +more)]. For example, a modular multiscale immune model of **CD4+ T cells** integrates logical models (signaling/gene regulation), constraint-based metabolic models, ABM population dynamics, and ODE cytokine dynamics to study immune responses and infection contexts [Data: Sources (188492, 188497, 188499)]. In drug development, **PK/PD** and **PBPK** models support dose–concentration–effect understanding, translation across species/populations, and trial optimization; **quantitative systems pharmacology (QSP)** combines systems biology with translational PK/PD to connect drug action to pathophysiology [Data: Sources (101188, 89986, 89987, 210085, +more)]. In cardiac research specifically, mechanistic electrophysiology models (from ion channels to whole-heart/ECG scales) are used to understand arrhythmias and predict drug effects, with emphasis on calibration/validation and translation across cell types/species [Data: Sources (28974, 89990, 89996, 123867, +more)].

---

## G7. [GLOBAL] How are chemical compounds characterized and linked to biological activity in the dataset?

*ID: 6676d2bc-0f5... | Latency: 40.2s*

**Answer:**

Chemical compounds in the dataset are characterized primarily by **standardized structural identifiers/encodings** and **computed molecular representations (descriptors/fingerprints)**, and they are linked to biological activity via **assay endpoints and derived labels** that can be used for QSAR/ML, similarity search, clustering, or pharmacophore-based ranking.

## How compounds are characterized

**1) Structure encodings and identifiers**
- Molecules are stored as **SMILES** strings (and in some workflows also InChI/InChIKey) to provide a machine-readable representation suitable for descriptor calculation, deduplication, and cross-database linkage [Data: Sources (52375, 302663, 302664, 120718, 265170)].
- Compounds may also be referenced by external database identifiers (e.g., **PubChem CIDs**, **ChEMBL IDs**, and other database-specific IDs such as those used for phytochemicals) to connect structures to metadata and names across resources [Data: Sources (99393, 177220, 177225, 265170)].

**2) Fingerprints and descriptor vectors**
- A central approach is transforming chemical structures into **numerical descriptors** (sometimes thousands per compound) that cover physicochemical and structural features and serve as model inputs [Data: Sources (146489, 146498)].
- Widely used molecular representations include **circular fingerprints** such as **Morgan/ECFP**, typically encoded as fixed-length bit vectors (e.g., 128, 512, 1024 bits; radii such as 2 or 3 are used depending on the study) [Data: Sources (302664, 120718, 77137, 273347, 256972)].
- Other fingerprint types also appear (e.g., **MDL fingerprints**, **MACCS fingerprints**) depending on the modeling or similarity task [Data: Sources (329252, 177264)].
- Standard computed physicochemical properties (e.g., **MW, LogP, TPSA**) are calculated from SMILES and used either directly as features or for filtering/analysis [Data: Sources (52375, 241105, 241438)].

**3) Similarity matrices and chemical space visualization**
- Structural similarity is computed using **Tanimoto coefficients** on fingerprints; these similarities are used for dendrograms, networks, clustering, and selection of representative compounds [Data: Sources (47058, 289139)].
- The dataset uses dimensionality reduction methods (e.g., **PCA** on descriptor sets and **t-SNE** on ECFP representations) to visualize chemical space and to examine separation/clustering of actives vs inactives [Data: Sources (146498, 302676, 272938)].

## How compounds are linked to biological activity

**1) Quantitative bioactivity endpoints (regression-ready)**
- Biological activity is linked to compound–target pairs through curated potency/affinity endpoints such as **IC50, EC50, Ki, Kd** (and related measures), typically restricted to **protein targets** in some subsets [Data: Sources (52375, 120717, 302663)].
- Activities may be transformed to standardized logarithmic scales such as **pIC50** or **pChEMBL** to normalize units and support modeling [Data: Sources (120717, 302663)].
- Where multiple measurements exist for a compound–target pair, consensus values are computed (e.g., mean/median under specified rules) and duplicates can be removed using structure identity (e.g., via SMILES-based redundancy checks) [Data: Sources (52375, 302663)].

**2) Binary activity labels (classification-ready)**
- In some datasets, molecules are labeled **active/inactive** using explicit thresholds (e.g., pIC50 ≥ 5.0 with high confidence) and non-matching molecules are assumed inactive for that class [Data: Sources (329252)].
- Other workflows define “active” using thresholds on transformed potency (e.g., setting an activity threshold and reporting the resulting active fraction) [Data: Sources (302675, 302676)].

**3) Pharmacophore model “fit” and estimated activity**
- For certain target-focused nutraceutical/phytochemical datasets, compounds are linked to activity through **pharmacophore models** that output an **estimated activity** and a **fit value** describing how well a compound matches pharmacophore features (with 10 indicating ideal mapping) [Data: Sources (177220, 177225)].

## How the dataset operationalizes the structure–activity link

**1) QSAR/ML modeling**
- The general workflow is: compute descriptors/fingerprints → train classifiers/regressors on known activities (active/inactive or IC50-like endpoints) → apply models to score new compounds [Data: Sources (146489, 138742)].
- Multiple ML approaches are referenced, including neural networks and other standard learners; model training relies on known activity labels/values derived from curated screening/assay data [Data: Sources (146489, 302664)].

**2) Network/clustering approaches that relate structure to activity**
- Compounds can be clustered by fingerprint similarity (Tanimoto-based networks/modules) and then modeled within clusters to yield interpretable relationships between descriptors and activity (e.g., piecewise linear models per structural module) [Data: Sources (289132, 289139)].
- Conversely, compounds can also be clustered by **activity profiles across targets**, enabling “drug-activity profiles” that support target/compound similarity analyses based on predicted or observed responses [Data: Sources (204270, 204293)].

**3) Screening integration and evidence strength**
- For multi-assay screening collections, activity calls gain credibility when a compound is active in **multiple assays** or when a screening hit is confirmed by **dose–response follow-up**, helping mitigate inter-laboratory/assay variability [Data: Sources (23558, 100236, 179180)].

---

## G8. [GLOBAL] What polymer design variables control nano-object morphology in RAFT dispersion polymerization?

*ID: 24cbdf28-14b... | Latency: 30.2s*

**Answer:**

In RAFT dispersion polymerization (PISA), nano-object morphology (spheres/worms/vesicles and related phases) is primarily governed by **(i) stabilizer-block design**, **(ii) core-forming block design**, and **(iii) formulation variables that change solvation/plasticization and packing during in situ self-assembly**.

**1) Stabilizer block (corona) design variables**  
- **Steric stabilizer degree of polymerization (DP)**: Longer stabilizer blocks generally favor **spheres** and can suppress access to higher-order morphologies; shorter stabilizer blocks can enable **worms and vesicles** within the appropriate composition window [Data: Sources (86127, 254219, 86161, 254228, 274535)].  
- **Stabilizer chemistry and ionization** (where relevant): Using **ionic/anionic stabilizers** can make morphology sensitive to **pH and ionic strength**, which can shift (or frustrate) self-assembly and sometimes enables higher-order morphologies in otherwise sphere-biased formulations [Data: Sources (86130, 324704, 324708, 254275)].

**2) Core-forming block (insoluble block) design variables**  
- **Target DP of the core-forming block**: Increasing the core-block DP typically drives the sequence **spheres → worms → vesicles** (with mixed phases possible), and morphology maps/pseudo-phase diagrams are commonly built using this axis [Data: Sources (86127, 324728, 254210, 254223, 86119)].  
- **Core-block hydrophobicity and chain mobility (e.g., Tg)**: More weakly hydrophobic and/or more mobile core-forming chains can facilitate **particle fusion and morphology evolution**, expanding access to worms/vesicles and enabling unusual anisotropic forms under certain conditions [Data: Sources (254185, 254247, 86131, 324746)].  
- **Critical DP for micellar nucleation** depends on the core-block chemistry/solvation (e.g., PHBA vs PHPMA), which alters when self-assembly begins and how morphology evolves thereafter [Data: Sources (254206, 254207)].

**3) Monomer/solvent compatibility (solubility) and plasticization variables**  
- **Monomer aqueous solubility (and resulting core plasticization)**: Higher (or intermediate) monomer solubility can increase monomer/water ingress into the growing core, enhancing chain mobility and enabling transitions to worms/vesicles (or even “monkey nut” morphologies) rather than kinetically trapped spheres [Data: Sources (324704, 324712, 86131, 324746, 86167)].  
- This is often invoked to rationalize why **aqueous dispersion polymerizations (water-miscible monomers)** more readily access worms/vesicles than many **aqueous emulsion polymerizations (water-immiscible monomers)**, which frequently yield kinetically trapped spheres [Data: Sources (254194, 324710, 86128, 254305)].

**4) Concentration (solids content) / copolymer concentration**  
- **Copolymer concentration (solids)** shifts morphology: lower concentrations and/or longer stabilizers tend to favor **spheres**, whereas higher concentrations (with appropriate block ratios) favor **vesicles**; worms often occupy a narrow intermediate region [Data: Sources (86127, 86134, 86119)].

**5) Environmental variables coupled to polymer design (especially for ionic stabilizers)**  
- **Solution pH and ionic strength** (when using pH-responsive/ionic blocks or end groups) can change colloidal stability and effective packing, thereby influencing accessible morphologies [Data: Sources (86130, 324704, 254274, 254275)].

---

## G9. [GLOBAL] What experimental protocol choices shape Western blot and qRT-PCR measurement comparability?

*ID: 401d46ff-f0e... | Latency: 40.1s*

**Answer:**

Experimental protocol choices that most strongly shape how comparable Western blot (protein abundance) and qRT-PCR (mRNA abundance) measurements are fall into a few recurring categories: how samples are prepared and normalized, how each assay’s dynamic range and detection limits are managed, and how analysis/quality control is performed.

### Sample preparation and input normalization (both assays)
For **qRT-PCR**, comparability depends on controlling RNA integrity/contamination and equalizing input across samples. Common protocol choices include DNase treatment plus RT-negative controls to rule out genomic DNA signal, defined RNA mass into reverse transcription (e.g., 500 ng–3 µg), and defined cDNA mass/volume per PCR well (e.g., 10–30 ng per reaction) [Data: Sources (8713, 302487, 245506, 53141, 53142)]. Primer design to **span exon–exon junctions** (or different exons) is a specific experimental choice used to reduce genomic DNA contributions and improve comparability across experiments [Data: Sources (18919, 162598, 162230, 43813)].

For **Western blots**, comparability depends on consistent extraction chemistry and quantifying/normalizing loaded protein. Protocols vary in lysis buffers (e.g., RIPA vs high-SDS/Laemmli-style buffers; inclusion of protease/phosphatase inhibitors), denaturation conditions (e.g., 95–100 °C for 5 min), and whether protein concentration is measured (BCA/Bradford/detergent-compatible assays) prior to loading defined masses (often 10–50 µg) [Data: Sources (8713, 214629, 261219, 289011, 171671, +more)]. When treatments can change cell number/viability over longer windows, explicitly measuring protein concentration (rather than assuming equal protein per condition) becomes important for comparability [Data: Sources (47893)].

### Choice of normalization controls (housekeeping genes vs loading controls)
A major protocol choice is **what each assay is normalized to**, and whether those normalizers are stable under the experimental conditions.

* **qRT-PCR reference gene strategy.** Many protocols normalize to a single housekeeping gene such as GAPDH or 18S, while others use multiple reference genes and algorithms (e.g., GeNorm) to select stable controls [Data: Sources (161264, 52634, 152111, 190897, 28354)]. Some workflows explicitly verify that the housekeeping gene Ct does not vary by more than ~1 cycle across treatments, which increases comparability of fold-change estimates [Data: Sources (188626)].
* **Western blot loading controls.** Blots are commonly normalized to proteins such as GAPDH, β-actin, or tubulin, and phospho-proteins may be normalized to total protein (e.g., phospho/total ratios) [Data: Sources (117435, 276272, 228577)]. Importantly, subcellular fractionation introduces a comparability issue: normalized values from nuclear vs cytoplasmic fractions cannot be directly compared if different fraction-specific loading controls are used [Data: Sources (47874, 47888)].

Because the assays normalize to different kinds of internal standards (mRNA housekeeping transcripts vs protein loading controls), protocol decisions about **which normalizers** to use and whether they are validated for stability directly affect how meaningfully qRT-PCR trends can be compared to Western blot trends.

### Quantification approach, dynamic range, and saturation/threshold rules
Protocol choices that manage **assay linearity** and **limits of detection** strongly affect cross-assay comparability.

* **qRT-PCR quantification method and efficiency assumptions.** Many studies use comparative Ct (2^-ΔΔCt), which assumes similar (near-100%) amplification efficiency between target and reference; others use approaches that estimate efficiency (e.g., LinRegPCR) or use standard curves for absolute quantification (transcripts per µg RNA) [Data: Sources (162596, 103792, 188626, 294953)]. Running dilution curves to confirm linearity/primer performance (e.g., R² > 0.9) and melt curves for single products are explicit design choices that improve comparability across targets and runs [Data: Sources (43813)].
* **Ct/Cq inclusion cutoffs.** Some protocols exclude or treat with caution high-Ct results (e.g., Ct>30 excluded; Cq>33 not reported) to avoid low-efficiency/low-template false positives, which changes what is considered “detectable” compared with protein detection by Western blot [Data: Sources (171671, 53928, 162598)].
* **Western blot detection and saturation.** Quantitative comparability depends on staying within the linear detection range (chemiluminescent film vs digital systems), standardized exposure/acquisition parameters, and consistent densitometry workflows (ImageJ/Image Studio/Quantity One, etc.) [Data: Sources (161266, 276272, 31033, 294400)]. Image bit-depth and avoiding detector saturation are explicit analysis choices that affect densitometry comparability across experiments and instruments [Data: Sources (47870)].

### Replication structure and run-level consistency
Protocol decisions on **technical replicates** (often duplicates/triplicates) and **biological replicates**, and whether thresholds/settings are held constant across all samples in a comparison set, influence comparability and interpretability.

* qRT-PCR frequently uses technical duplicates/triplicates per gene/sample and stresses consistent threshold setting across samples plus stable reference genes for reliability [Data: Sources (8713, 161264, 333438)].
* Western blots are often repeated across independent experiments and quantified by densitometry; comparability improves when blots are acquired/processed in parallel with similar parameters [Data: Sources (294400, 275134)].

### Broader comparability caveat: biology and site effects
Even with careful protocols, cross-laboratory work shows that **site (laboratory) and hidden confounders** can mask true biological effects in both transcript and protein readouts; cellular heterogeneity and other unmeasured factors can inflate variance, reducing apparent agreement between mRNA and protein measures unless nuisance variation is modeled/removed [Data: Sources (105606, 105657, 105619, 105630)].

---

## G10. [GLOBAL] How do acidity and salinity jointly influence feldspar dissolution indicators like pH and dissolved silica?

*ID: c88a1c65-af2... | Latency: 30.1s*

**Answer:**

Acidity and salinity interact in two main ways that matter for feldspar-dissolution indicators (like solution pH evolution and dissolved silica): (i) pH directly controls feldspar dissolution kinetics, and (ii) salinity (ionic strength/NaCl) can both shift pH for a given CO₂ loading and also alter dissolution (slightly) via ion–surface interactions—making it hard to attribute changes in dissolved silica to “salinity alone” unless pH is tightly controlled.

Feldspar dissolution shows a strong pH dependence, with faster dissolution at both low and high pH and the slowest rates near neutral pH (a U-shaped dependence) [Data: Sources (231196)]. Under acidic conditions relevant to CO₂-charged injection waters, feldspar dissolution consumes protons (H⁺), so fluids tend to neutralize (pH rises) as dissolution proceeds [Data: Sources (231432, 231433, 231434, 231435)]. Because dissolved silica (Si) is released during feldspar dissolution, rising Si in solution is a direct indicator that dissolution is occurring and continuing; in PHREEQC calculations, Si can rise continuously even while pH increases and secondary Al-phases begin to precipitate [Data: Sources (231417)].

Salinity complicates this picture because increasing NaCl changes carbonate-system speciation and ion activities, which may shift measured/achieved pH for the same intended acidity. The dataset notes competing effects: electrolytes may reduce CO₂ stability/solubility (tending to *raise* pH), but they may also stabilize carbonic-acid dissociation products and increase effective dissociation (tending to *lower* pH) [Data: Sources (231626, 231628)]. In the NaCl–feldspar experiments, this “salinity-driven acidity shift” made it difficult to separate the direct impact of NaCl from the indirect impact of pH changes [Data: Sources (231635, 231641, 231642)].

When acidity and salinity are varied together (NaCl from 0 to 2.1 M under acidic conditions), dissolved silica release still indicates substantial feldspar dissolution. After 7 days at ~100 °C with pH close to ~3 and NaCl between 0 and 2.1 M, measured Si increased to roughly 40–100 mg/L, and Si and Al releases were of similar magnitude across NaCl concentrations—suggesting that using saline fluids (seawater-like) will not completely inhibit feldspar dissolution [Data: Sources (231640, 231761, 231105)]. However, there were qualitative indications that higher Na⁺ may *slightly* inhibit dissolution (e.g., Al trends with NaCl and literature results for anorthite inhibition attributed to competition of Na⁺ with H⁺ at mineral surfaces), but this effect was minor and difficult to isolate from pH changes without better pH control [Data: Sources (231596, 231635, 231637, 231641, 231233)].

Mineralogy mediates the joint effect: more calcic (anorthite-rich) plagioclase can buffer acidic saline fluids more effectively, raising pH (toward ~5 in post-experiment fluids in some cases), which then can slow further feldspar dissolution as conditions approach the “near-neutral minimum” in the U-shaped pH–rate curve [Data: Sources (231641, 231632, 231196, 231113)]. This creates an important coupled feedback: higher acidity accelerates dissolution and boosts dissolved silica, but dissolution-driven pH neutralization (especially in anorthite-rich feldspars) can reduce acidity and thereby dampen ongoing dissolution and silica release over time [Data: Sources (231632, 231641, 231196)].

---

## G11. [GLOBAL] What computational approaches are used to predict binding, structure, or pharmacokinetics?

*ID: 6fcd7755-75a... | Latency: 30.1s*

**Answer:**

Computational prediction of **binding (pose, affinity, and selectivity)** is commonly approached with a hierarchy of methods that trade throughput for physical realism. At the high-throughput end, **molecular docking** proposes ligand poses in a binding pocket and ranks them with **scoring functions**; these scoring functions are often categorized as **force-field/physics-based**, **empirical**, **knowledge-based**, or **machine-learning-based** [Data: Sources (140834, 151370, 190393, 250414, 114939, +more)]. Docking searches may be driven by algorithms such as **genetic algorithms, Monte Carlo, systematic searches, fragment-based methods, distance geometry, and related heuristics** [Data: Sources (326495, 272766, 275961)]. To prioritize compounds before docking (or to complement it), **pharmacophore modeling and pharmacophore-based virtual screening** identify molecules matching spatial arrangements of features (e.g., H-bond donors/acceptors, hydrophobes, aromatics, charges), using either ligand-derived or structure-derived feature hypotheses [Data: Sources (177113, 326488, 326490, 182404, 151371, +more)].

For more quantitative binding energetics, **molecular dynamics (MD)** is used to model protein/ligand flexibility, solvent effects, and entropic contributions that are difficult for static scoring functions to capture [Data: Sources (99600, 94783, 94784, 273274, 260097, +more)]. Within MD-based free-energy estimation, commonly cited approaches include **alchemical free energy calculations** (e.g., free energy perturbation/thermodynamic integration; both **RBFE** and **ABFE**), **steered/pulling methods** (including **Jarzynski non-equilibrium work** and **potential of mean force** calculations), and **endpoint post-processing** methods such as **MM/PBSA** and **MM/GBSA** (often using implicit solvent) [Data: Sources (260081, 94790, 94791, 88292, 94997, +more)]. Enhanced sampling approaches like **metadynamics** (including funnel restraints or path collective variables) are also discussed for sampling binding/unbinding events [Data: Sources (94791, 94792, 88292)]. These more rigorous methods can be accurate but are computationally expensive and are therefore typically applied to smaller sets of compounds later in lead optimization rather than ultra-large virtual screens [Data: Sources (140838, 273274, 95386, 88341)].

For **structure prediction and structural modeling** when experimental complexes are missing, workflows may use **homology modeling** to generate target structures for subsequent docking and simulation [Data: Sources (241071, 140816, 94782)]. For protein binding-site identification (where you must first determine *where* ligands might bind), commonly used non-ML methods include **FPocket** (Voronoi tessellations/alpha spheres with partial least squares ranking), **FTSite** (probe placement with empirical free-energy clustering), and **DoGSite3** (difference-of-Gaussians pocket detection) [Data: Sources (299845)]. For protein–protein or peptide–protein structural prediction/docking, ML-based structure predictors such as **AlphaFold2-Multimer** have been used for peptide:protein docking, sometimes alongside specialized peptide docking tools (e.g., methods that fold flexible peptides during docking) [Data: Sources (283645)].

**Machine learning (ML) and deep learning (DL)** approaches are used across binding prediction tasks: (i) **pose prediction** (classifying near-native poses), (ii) **virtual screening** (binder vs non-binder classification), and (iii) **binding affinity prediction** (regression) [Data: Sources (260084, 140841, 190393)]. Structure-based ML scoring functions commonly include **3D convolutional neural networks (CNNs)**, **graph neural networks (GNNs)**, and other **3D fingerprint/descriptor** models, often aiming to outperform classical docking scoring functions [Data: Sources (273298, 190393, 273326, 140834)]. Ligand-based ML/QSAR models use molecular descriptors and fingerprints (e.g., ECFP, RDKit descriptors) with algorithms such as **random forests, support vector machines, neural networks, decision trees, and Bayesian classifiers** [Data: Sources (71550, 177105, 273326, 64287)]. ML is also described for broader drug–target interaction prediction using **sequence-based** and **structure-based** predictors, including DL architectures that learn representations of proteins and ligands jointly [Data: Sources (281677, 281589)].

For **pharmacokinetics/ADMET prediction**, in silico methods include classical **QSAR/QSPR** models for properties (e.g., solubility and other physicochemical endpoints), ML models trained on experimental ADMET data, and mechanistic **physiologically based pharmacokinetic (PBPK) modeling/simulation** to predict absorption, distribution, metabolism, and excretion (and sometimes CNS disposition) using scaled in vitro inputs and physiological compartments [Data: Sources (71529, 273277, 230406, 323923, 87111, +more)]. Practical ADME property calculators (e.g., tools that estimate logP/logS, permeability, plasma protein binding, hERG risk, BBB penetration, CYP inhibition) are also used to triage compounds alongside binding predictions in selection workflows [Data: Sources (326582, 326918, 64300)].

---

## G12. [GLOBAL] How do different immune stimuli shape cytokine production across immune cell subsets?

*ID: 134d9de3-6eb... | Latency: 40.2s*

**Answer:**

Different immune stimuli shape cytokine production by (i) providing distinct upstream “instructive” cytokines, (ii) engaging different innate receptors or co-stimulatory pathways, and (iii) acting on cell subsets that differ in cytokine-receptor expression and signaling state—so the same trigger can yield different cytokine outputs depending on the responding subset and the surrounding cytokine milieu.

Across **CD4+ T cell subsets**, cytokine combinations during priming are central in determining effector differentiation and the cytokines subsequently produced. IL-12 (often with IFN-γ) promotes Th1 differentiation, characterized by IFN-γ production, whereas IL-4 drives Th2 differentiation, associated with IL-4/IL-5/IL-13 secretion; TGFβ plus IL-6 promotes Th17 (IL-17A production), while TGFβ alone (or with IL-2 and absence of IL-6) promotes induced Treg differentiation (FOXP3 expression and regulatory cytokine programs) [Data: Sources (87263, 109358, 188511, 188512)]. Model-based and experimental summaries further emphasize that more than one cytokine is typically required to induce a given Th fate and that different cytokine pairings have different strengths (e.g., IL-2+IL-4 strongly converting naïve cells to Th2, while IL-2+TGFβ yielding a weaker Treg response under some conditions) [Data: Sources (188511, 188512, 87263)]. In addition to the cytokine milieu, **TCR signal strength/quality** shapes which cytokines dominate: lower activation signals (tuned by peptide affinity/density) can bias toward Th17 responses in a pro-Th17 cytokine environment, while stronger signals can favor other outcomes and alter IFN-γ/IL-4 patterns [Data: Sources (51580, 51588, 51592, 51619)].

For **NK cells**, cytokine production is highly stimulus- and subset-dependent. Innate accessory-cell cytokines (notably IL-12, IL-15, and IL-18) are recurring amplifiers of NK IFN-γ production and can act synergistically with each other and with additional cues like IL-2 or antibody-dependent activation via CD16 [Data: Sources (50965, 48793, 48796, 44617, 286271)]. NK subsets differ in cytokine receptor expression and therefore in responsiveness: less differentiated NK cells (e.g., CD56^bright or CD56^dimCD57^−) are generally more cytokine-responsive and produce more IFN-γ to cytokine stimulation, whereas more differentiated CD56^dimCD57^+ cells are less cytokine-responsive but can be highly responsive to antibody-dependent activation through higher CD16 expression [Data: Sources (49052, 48776, 38679, 49356, 51310)]. This means the same inflammatory cytokines may elicit strong IFN-γ in one NK subset but little in another, while antibody-antigen complexes may invert that pattern [Data: Sources (49356, 51311)].

Among **monocytes/macrophages**, the stimulus and context can switch cytokine programs and even induce regulatory features. Whole-bacteria exposure can drive monocytes toward IL-23 secretion and simultaneously induce an acquired IL-10 resistance phenotype; mechanistically, IL-1α/IL-1β signaling through IL-1R1 is essential for monocyte IL-23 production in that setting, while many other tested cytokines had little impact on IL-23 induction [Data: Sources (132082, 132083, 132085)]. In macrophages, classical inflammatory stimuli (e.g., LPS+IFN-γ) support M1-like outputs (IL-1, IL-6, TNF-α, and IL-12 that can promote Th1 polarization), while alternative activation supports higher IL-10/TGFβ and tissue-repair-associated programs [Data: Sources (273879, 120817, 70733, 39)]. Even closely related differentiation signals can yield different secretomes: IL-34 versus CSF-1 (shared CSF-1R) can produce macrophages with different chemokine/cytokine profiles after polarization, altering their capacity to shape downstream Th1 polarization [Data: Sources (101592, 101600)].

For **dendritic cells (DCs)**, innate receptor engagement and environmental “conditioning” change whether DCs deliver pro-inflammatory vs tolerogenic cytokines to T cells. For example, certain immobilized monosaccharides suppress LPS-induced DC activation—reducing CD40 and IL-12 while increasing IL-10—consistent with a regulatory DC phenotype that promotes naïve T cell polarization toward regulatory programs in DC–T cell co-cultures [Data: Sources (87436, 87499, 87504)]. Likewise, some DC types exhibit high baseline IL-10 and require stronger combined stimuli (inflammatory cytokines plus TLR agonists plus CD40 ligation) to elicit substantial IL-12p70 production, which is otherwise limited—thereby biasing away from Th1 priming unless the activating inputs are sufficiently strong [Data: Sources (100342, 100343)]. Myeloid DCs can also differ in signaling constraints on cytokine production (e.g., p38 MAPK inhibition having opposite effects on IL-12 in distinct DC types), which will alter how the same TLR stimuli translate into IL-12-driven Th1 polarization [Data: Sources (19472, 19481)].

Finally, multiple examples show that **combined stimuli often produce non-additive (synergistic) cytokine outputs** across compartments. IL-15 can boost influenza-driven myeloid cytokines (e.g., IL-12, type I IFN, GM-CSF), which in turn correlates with enhanced NK IFN-γ responses [Data: Sources (49057, 49573, 49133, 49569)]. Similarly, in CD4 T cells, IL-33 alone may not induce IFN-γ, but it can synergize with IL-12 to enhance IFN-γ production in an ST2-dependent manner without inducing other cytokines in that context [Data: Sources (146754, 146755)]. Together these findings illustrate a general principle: immune stimuli shape cytokine production by layering innate-receptor triggers, cytokine-cytokine synergy, and subset-specific receptor/signaling capacity, thereby producing distinct cytokine “signatures” across immune cell subsets [Data: Sources (48796, 44617, 132083, 87436, 87263, +more)].

---

## G13. [GLOBAL] How do different neural differentiation protocols shape progenitor and neuron marker expression?

*ID: 2f6e5eb6-c0c... | Latency: 40.2s*

**Answer:**

Different neural differentiation protocols tune **when** cells exit pluripotency, **which progenitor identity** they adopt (e.g., rosette NPC, neural crest, ventral midbrain floorplate, ventral telencephalon, spinal motor neuron progenitor), and **which neuronal subtype markers** rise during maturation. Across protocols, a common early signature is **downregulation of pluripotency markers** (e.g., OCT4/POU5F1, NANOG) accompanied by **upregulation of progenitor markers** (e.g., SOX2, NESTIN, PAX6), but the *regional patterning cues* then drive diverging marker trajectories [Data: Sources (72031, 163858, 334979, 193548, 171634)].

## Dual-SMAD neural induction: rosette NPC markers rise, pluripotency falls
Protocols that start with **dual SMAD inhibition** (TGFβ/Activin inhibition plus BMP inhibition) robustly push hPSCs into neuroectoderm/NPC states, typically visible as rosettes with increased **NESTIN** and **PAX6**, while pluripotency genes **OCT4** and **SOX2** decline as differentiation proceeds toward neurons [Data: Sources (72031, 93788, 162483, 15947, 121900)]. In some ESC→dopaminergic time courses, **Nanog/Oct4 drop within days (day 1–3)**, an early differentiation marker **Fgf5** is transient, and neural/progenitor-associated genes such as **Blbp, Hes5, Mash1/Ascl1** rise from ~day 2 onward, while **Sox2** can persist as it is shared by ESCs and many CNS progenitors [Data: Sources (163858)].

## Ventral midbrain dopaminergic (mDA): SHH/FGF8 biases subtype markers without strongly changing “pan-neuronal” markers
When dual-SMAD neural induction is followed by **SHH + FGF8a** patterning, progenitors are steered toward **ventral midbrain dopaminergic fate**, driving strong upregulation of mDA lineage markers such as **TH, NURR1, PITX3, FOXA2, LMX1A, EN1** (and related transcripts like Dmrt5 in one dataset) [Data: Sources (165012, 165013, 72032, 93789, 72037)]. In contrast, **general neuronal markers** (e.g., **TUBB3, MAP2, ASCL1, NGN2**) can show *similar expression profiles* between SHH/FGF8-treated and control neuronal cultures, indicating that patterning cues can selectively alter subtype identity markers more than pan-neuronal maturation markers [Data: Sources (165013, 165018)]. Protein-level assays corroborate this, with abundant **TH+** neurons and subsets co-expressing **FOXA2** (floorplate/ventral midbrain feature) and nuclear **PITX3/NURR1** [Data: Sources (72032, 93789)].

Related maturation dynamics also appear in longer dopaminergic maturation series: the proneural gene **Ngn2** may peak at an immature stage (e.g., ~day 16) then drop by later time points, while **Nurr1** remains expressed at later stages consistent with a maintenance role [Data: Sources (163863)].

## Predictive-marker vs “common marker” issue in DA progenitors: marker choice depends on what outcome you care about
For dopamine progenitors intended for transplantation, some widely used mesDA progenitor markers (**FOXA2, LMX1A, CORIN**) are reported as **not sufficient to predict in vivo dopaminergic yield/function**, whereas a more **caudal midbrain/MHB-adjacent marker set** (e.g., **EN1, ETV5, CNPY1, PAX8, SPRY…**) correlates better with dopaminergic yield after grafting and was used to guide a GMP protocol [Data: Sources (162176, 162116, 162121, 162170)]. This highlights that protocols can produce progenitors that “look correct” by common markers, yet differ in later neuron marker outcomes depending on how completely regional identity has been specified.

## Ventral telencephalon / striatal programs: WNT/BMP inhibition, SHH, and Activin shift progenitor and MSN markers in different directions
In forebrain/striatal differentiation frameworks, early dual-SMAD (often with **WNT inhibition**) yields telencephalic neuroectoderm, and subsequent ventralization signals determine whether cultures favor dorsal cortical-like vs subpallial/striatal identities [Data: Sources (171634, 162482, 162255, 162950)]. Reported examples include:

- **DKK1 + SHH** patterning generating more ventral/LGE-like progenitors (e.g., higher **ISL1+** fractions) that later mature into **striatal GABAergic** neurons expressing **CTIP2/BCL11B**, **GAD65/67**, **GABA**, and sometimes **DARPP32**; whereas “default dorsal” progenitors tend toward **CTIP2+ vGLUT1+ glutamatergic** cortical-like outcomes [Data: Sources (162510)].
- In a systematic comparison, **concurrent BMP and WNT inhibition** enhanced **FOXG1+ telencephalic** and LGE-like specification by ~day 16, and during terminal differentiation produced neurons with **CTIP2** and **DARPP32** (with **Activin** increasing DARPP32 yield), while **SHH pathway activation (e.g., purmorphamine/SAG)** in the same window tended to **downregulate DARPP32/CTIP2** and bias toward **MGE interneuron markers** instead of LGE/MSN markers [Data: Sources (162255, 162950, 162951, 163002)].
- Activin treatment is also described as promoting progenitor differentiation (e.g., apparent upregulation of neuronal markers such as **TUBB3, MAP2, DCX**) while not necessarily changing early neuroectodermal markers (**SOX2, SOX1, NES**) [Data: Sources (162950, 162875)].

## Neural crest induction: BMP “set point” flips SOX2/PAX6 vs SOX10 programs
Neural crest protocols illustrate an especially sharp tradeoff in marker expression depending on BMP handling. A fully defined neural crest system reported that **an optimum level of BMP activity is required for neural crest induction**, whereas **higher or lower BMP** drives expression toward **non-neural** or **neural (SOX2/PAX6)** identities, respectively; poor efficiency correlated with increased **SOX2/PAX6** (neural) or **GATA2/GATA3** (non-neural) at the expense of the neural crest marker **SOX10** [Data: Sources (334972, 334978, 334973)]. In that protocol, neural crest identity at ~day 7 included induction of **p75**, and increased **TFAP2a, PAX3, SOX10**, with **OCT4** repressed [Data: Sources (334979)].

## Posterior ventral spinal cord / motor neuron progenitors: NMP markers first, then HOX/posterior and ventral progenitor markers
Protocols that route through **neuromesodermal progenitors (NMPs)** show a different progenitor-marker sequence. NMP induction uses **WNT + FGF stimulation with BMP inhibition** to limit neural crest and is marked by **TBXT (T) + SOX2 co-expression** [Data: Sources (193540)]. Subsequent patterning with **BMP and TGF-β inhibition plus RA and SHH agonism** yields posterior neurectoderm and then ventral spinal cord progenitors expressing **HOXC9/SOX1/PAX6** plus posterior **HOX PG(6–9)**, and later ventral/MN progenitor markers **NKX6.1, NKX6.2, OLIG2, LHX3** by ~day 14 [Data: Sources (193548, 193561, 193562)].

## Neuronal maturation cocktails and timing: pan-neuronal markers rise while subtype markers depend on earlier patterning
Across multiple systems, terminal maturation steps (e.g., **BDNF/GDNF/cAMP/ascorbic acid** in midbrain protocols) support neuronal maturation after patterning, with increases in pan-neuronal markers like **TUBB3** and **MAP2**, while earlier morphogen history largely determines subtype markers such as **TH/PITX3/NURR1** (mDA) or **DARPP32/CTIP2** (striatal MSN-like) [Data: Sources (72031, 165013, 162510, 162255, 72003)]. In SH-SY5Y neuron-like differentiation, sequential **RA then BDNF** is explicitly associated with greater apparent maturity (neurite outgrowth/network formation) and dependency on neurotrophic support, again emphasizing that different protocols can change both the magnitude and stability of neuronal marker expression [Data: Sources (230999, 244670)].

---

## G14. [GLOBAL] How are institutional affiliations formatted across the dataset, including full postal addresses?

*ID: 634098bd-622... | Latency: 30.1s*

**Answer:**

Institutional affiliations in the dataset are generally presented as **free-text, comma-separated strings**, often tied to an **affiliation index number** (e.g., `1`, `2`, `3`) that maps authors to institutions [Data: Sources (215295, 164084, 307102, 49026, 137581, +more)]. The ordering within each affiliation typically moves from **smallest organizational unit to largest geographic unit**: *Department/Unit → Center/Institute/Lab → University/Health system → City → Postal/ZIP code (when provided) → Region/State (when applicable) → Country* [Data: Sources (49026, 307102, 112982, 189076, 45867, +more)].

Full postal addresses are **inconsistently included**. Many affiliations include only **institution + city + country** (sometimes with a postal code), while others provide **street address lines, building names, PO Boxes, or campus identifiers** [Data: Sources (303337, 203568, 190483, 189076, 45865, +more)]. When present, postal information appears in several common patterns:
- **UK-style**: city followed by postcode and “UK/United Kingdom” (e.g., `Oxford OX3 7DQ, UK`; `London WC1E 7HT, United Kingdom`) [Data: Sources (307102, 49026, 122774, 103826, 173332)].
- **US-style**: city + state abbreviation + ZIP code + “USA/United States” (e.g., `Seattle, WA 98109-4766, United States`; `Stanford, CA 94305-4145`) [Data: Sources (189076, 164084, 6725, 115531, 112982)].
- **Continental Europe**: postal code precedes or follows city; country name included; sometimes “Cedex” (France) or regional qualifiers (Italy) [Data: Sources (214722, 45863, 150572, 215295, 279981)].

Across publishers/journals in the dataset, affiliations appear in a few recurring **layout conventions**:
1. **Numbered list blocks** (common in MDPI and many multi-author articles), where each line begins with an index and then the affiliation; emails may be appended after semicolons [Data: Sources (215295, 192200, 249171, 279981, 150573)].
2. **“Author details” sections** that bundle numbered affiliations into a paragraph-style block and often include city/postal code/country (e.g., South Africa examples include `Durban 4041, South Africa`) [Data: Sources (137581)].
3. **Highly granular, full-address entries** including building names, mail codes, street addresses, and room identifiers (e.g., Stanford affiliations with mail codes and street addresses) [Data: Sources (164084, 189076, 11147, 41991, 91783)].

Where full postal addresses are provided, they may include **street name and number**, sometimes **PO Box**, and occasionally **campus/building names**:
- Example with **street + postal code**: `6 Avenue Victor Le Gorgeu, 29238 Brest, France` [Data: Sources (215295)].
- Example with **PO Box**: `PO Box 1826, 20 Route de Pré-Bois, 1215 Geneva 15, Switzerland` [Data: Sources (189076)].
- Example with **street + mail stop/room**: `443 Via Ortega Drive, Stanford, CA 94305-4145` and `1265 Welch Road, Stanford CA 94305-5479` [Data: Sources (164084)].
- Example with **named building + hospital**: `Welcome Trust Brenner Building, St. James's University Hospital, Leeds LS9 7TF, England` [Data: Sources (198045)].

Finally, the dataset also contains many publisher boilerplate statements about neutrality “with regard to jurisdictional claims in published maps and institutional affiliations,” but these do not standardize affiliation formatting; they simply recur alongside the affiliation sections across multiple publishers (e.g., Springer Nature, MDPI) [Data: Sources (65215, 83043, 249171, 111776, 302643)].

---

## G15. [GLOBAL] How do ventricular myocyte models link adrenergic stimulation to ionic-current changes and repolarization?

*ID: b9e3cff2-675... | Latency: 30.1s*

**Answer:**

Ventricular myocyte models link adrenergic stimulation to ionic-current changes by explicitly coupling a β‑adrenergic signalling module (often driven by an agonist such as isoproterenol, ISO) to phosphorylation-dependent modulation of ion-channel, pump, and Ca-handling flux formulations. Many β‑ARS frameworks represent agonist binding to β1/β2 receptors, downstream G‑protein activation, cAMP production, and kinase activity (PKA and sometimes CaMKII), then map kinase-dependent phosphorylation onto specific targets (e.g., \(I_{\mathrm{CaL}}\), \(I_{\mathrm{Ks}}\), phospholamban/PLB, troponin I/TnI, and sometimes phospholemman/PLM influencing \(I_{\mathrm{NaK}}\)) to alter channel kinetics and/or maximal conductances and thereby reshape the action potential (AP) and Ca transient [Data: Sources (182290, 182302, 182313, 182314, 182316, +more)].

At the AP level, these coupled models explain repolarization changes as a shifting balance between inward (mainly Ca\(^{2+}\)) and outward (mainly K\(^+\)) currents during stress. In a rat ventricular myocyte modelling study that emulated exercise by combining faster pacing (1–10 Hz) with adrenergic stimulation (ISO), adrenergic stimulation increased peak currents broadly (reported increases ~23%–67%) except \(I_{\mathrm{K1}}\), and the resulting APD changes were interpreted as a frequency- and state-dependent change in the Ca\(^{2+}\):K\(^+\) current balance, with repolarizing K\(^+\) currents increasingly dominating APD control at higher rates [Data: Sources (272498, 272500, 272598)]. Sensitivity analyses in the same work linked *early/plateau* repolarization primarily to \(I_{\mathrm{to}}\) and \(I_{\mathrm{Ca}}\), while *late* repolarization depended strongly on \(I_{\mathrm{K1}}\), \(I_{\mathrm{Ca}}\), and \(I_{\mathrm{Ks}}\); notably, modulating \(I_{\mathrm{Ks}}\) had the largest leverage on late repolarization during adrenergic simulations [Data: Sources (272500, 272614)].

Human ventricular models used in drug-safety and mechanistic studies (e.g., ORd and derivatives) implement similar principles but with human-specific “repolarization reserve”: humans rely heavily on \(I_{\mathrm{Kr}}\) for repolarization compared with many animals, and differences in \(I_{\mathrm{Ks}}\)/\(I_{\mathrm{Kr}}\)/\(I_{\mathrm{K1}}\) expression help explain why the same adrenergic or pharmacological perturbation can yield different APD effects across species and cell types [Data: Sources (126416, 126417, 126402)]. When β‑ARS modules are embedded into such human ventricular electrophysiology models and ISO is applied, simulations can reproduce characteristic time courses: phosphorylation of \(I_{\mathrm{Ks}}\) tends to be slower than phosphorylation of \(I_{\mathrm{CaL}}\), PLB, or TnI, and APD may show a transient rise followed by shortening as outward current enhancement (especially via \(I_{\mathrm{Ks}}\)) catches up and outweighs increased inward Ca current [Data: Sources (182314, 182316)].

These modelling links are also used to connect adrenergic stimulation with *repolarization instability* and triggers such as EADs/DADs. Early β‑ARS modelling work identified a mechanistic route to EADs via reactivation of \(I_{\mathrm{CaL}}\) during plateau/repolarization when conditions favor it (e.g., reduced repolarization reserve) [Data: Sources (182319)]. More generally, ventricular and Purkinje modelling highlights how adrenergic-driven increases in Ca entry and SR loading can promote spontaneous SR Ca release and then recruit inward \(I_{\mathrm{NCX}}\) to generate depolarizing afterpotentials (DADs) [Data: Sources (121495, 121518, 126523)]. In sum, ventricular myocyte models “close the loop” from adrenergic receptor activation → phosphorylation-mediated current/Ca-handling changes → altered plateau and terminal repolarization (APD\(_{50}\)/APD\(_{90}\)) and, under vulnerable conditions, afterdepolarizations and arrhythmia propensity [Data: Sources (272614, 182290, 182319, 121495)].

---

## G16. [GLOBAL] Which coordination numbers are assumed when modeling glass network structure from diffraction?

*ID: 08ec56aa-6fa... | Latency: 20.1s*

**Answer:**

When modelling glass network structure from diffraction (in particular neutron diffraction real‑space fitting), the following coordination numbers are assumed/used as starting constraints in the provided reports:

- **Network former silicon:** **Si(4)** (tetrahedral SiO\(_4\)) [Data: Sources (16290, 17274, 17437)]  
- **Modifier alkalis/alkaline earths (assumed in the model):** **Na(6)**, **Li(4)**, **Ca(6)**, **Ba(8)** [Data: Sources (16290, 16292, 16511)]  
- **Oxygen (average oxygen coordination used in modelling/empirical constraints):** **O(4)** [Data: Sources (16291, 16512, 16474)]

Additional coordination assumptions explicitly stated for mixed-network glasses:

- **Boron:** both **B(3)** and **B(4)** are present; one model assumes **2/3** of B is 3‑fold and **1/3** is 4‑fold, giving an **average B–O CN = 3.33** [Data: Sources (16512)]  
- **Phosphorus in orthophosphate units:** **P(3)** for the O–P–O coordination used when estimating the total O…O coordination contribution (orthophosphate tetrahedra treated as isolated units in that context) [Data: Sources (17638, 17688)]  
- **Zinc (when present):** predominantly **Zn(4)** (tetrahedral ZnO\(_4\)) supported by diffraction/EXAFS fitting [Data: Sources (17500, 17670, 17516)]  
- **Magnesium (when present):** reported as mixed coordination with **predominantly Mg(4)** and a fraction of **Mg(5)** (and in some discussion also 6-fold as possible) [Data: Sources (17648, 17835, 17606)]

Finally, when using network-connectivity/\(Q^n\)-based simplifications to model overlapping correlations, the reports use derived **O–(Si)–O (i.e., O…O in Si tetrahedral network) coordination numbers** such as:
- **~4.0** for a metasilicate \(Q^2\) network (average O…O CN) [Data: Sources (17382, 17272)]  
- **4.8** for \(Q^3\) contribution (used in weighted averages) [Data: Sources (17272, 17688)]

---

## G17. [GLOBAL] How do reaction workup and quenching steps vary across the dataset’s syntheses?

*ID: 935e1fba-de0... | Latency: 30.1s*

**Answer:**

Reaction workup and quenching vary substantially across the syntheses represented in the provided chunks, ranging from **minimal/no formal workup** (direct analysis of crude mixtures) to **multi-stage aqueous quench → extraction → wash → drying → purification** workflows.

## 1) “No-workup” / crude-mixture workflows (quench effectively omitted)
Some syntheses (notably high-throughput/miniaturized contexts) deliberately bypass classical quenching and workup, instead **diluting and directly analyzing** crude reaction mixtures. For example, one workflow diluted each well with ethylene glycol and injected the reaction mixture directly into mass spectrometry after 24 h, with no described aqueous quench/extraction sequence [Data: Sources (300126)]. In the crystallography-coupled high-throughput synthesis workflow, **crude reaction mixtures were soaked onto protein crystals**, explicitly “bypassing small molecule purification,” which implies reduced or altered downstream workup compared to conventional isolation pipelines [Data: Sources (272899, 273072)].

## 2) Aqueous quench choices vary with reagent class and reaction risk
Across conventional bench syntheses, the **quench reagent** depends strongly on the reactive species present:

- **Salt solutions as “soft” quench + phase split:** reactions quenched with **sat. aq. NaCl (brine)** followed by extraction are described (a common approach for reactive bases like NaH in THF once major reactivity has ceased) [Data: Sources (227231)].  
- **Ammonium chloride quenches** (classic for organometallics/hydrides): reactions are quenched with **sat. aq. NH4Cl** and then extracted into organic solvent [Data: Sources (236216, 236094)].  
- **Bicarbonate/carbonate neutralizations:** acidic or acylation-derived mixtures are quenched/neutralized using **aq. NaHCO3** (including “30% sol’n”) before extraction [Data: Sources (258966)]. Separately, strongly acidic iodination conditions (HI present) were cooled and quenched with **sat. aq. K2CO3** [Data: Sources (181744)].  
- **Acid quench to a target pH:** one synthesis reports diluting with EtOAc and then **quenching to pH 7 with 1 M HCl(aq)** prior to extraction and extensive aqueous washing [Data: Sources (181739)].  
- **Chelation quench (special case):** at least one example uses **sat. aq. tetrasodium EDTA** as the quench, consistent with metal-mediated transformations where sequestering metals is beneficial [Data: Sources (227308)].

## 3) Typical downstream workups: extraction, washes, drying, and concentration
After quench, many procedures converge on a standard but variably elaborate sequence:
- **Liquid–liquid extraction** (often EtOAc or DCM; multiple pulls common) [Data: Sources (227231, 258966, 181744, 149278)].  
- **Brine washes** are frequently included before drying [Data: Sources (123087, 227231, 222208)].  
- **Drying agents** such as **Na2SO4** or **MgSO4** are used, then filtration and solvent removal in vacuo [Data: Sources (123087, 181739, 77587)].  
- Some workflows add **filtration through Celite** (to remove catalysts/solids) before phase partitioning [Data: Sources (123087, 132824)].

## 4) Workup can include aggressive impurity-removal washes (beyond “standard”)
A subset of syntheses uses unusually intensive washing steps. One example includes washing organic extracts with **0.5 M aqueous LiCl (5×)** before brine, drying, and chromatography—an approach often used to strip polar/amine-containing residues (e.g., DMF) [Data: Sources (181739)]. Another workup explicitly includes repeated washes with **1 M aqueous KF (3×)** (at least 1 min per wash), consistent with removing silicon-derived residues or fluoride-sensitive byproducts [Data: Sources (236094)].

## 5) “Quench” as a deliberate follow-on reagent addition (reaction-stopping by trapping)
Not all “quenching” is neutralization; sometimes it is **chemical trapping** to terminate an intermediate and drive to product. For example, after base-promoted transformation, the mixture was “quenched with the appropriate bromide electrophile (5.0 eq.)” (i.e., electrophile capture as the stop/finish step), then worked up by DCM/H2O partition and extraction [Data: Sources (235759)].

## 6) Dataset-level caveat: many reactions may not encode workup at all
Separate from laboratory procedures, the dataset’s patent/ELN reaction records often require cleaning because **solvents/catalysts may or may not be included and some components may be missing**, and preprocessing may remove unmapped components like solvents/catalysts from the reaction representation [Data: Sources (53328, 53329)]. This implies that **workup and quench steps are frequently not captured or are inconsistently represented** in the underlying reaction data, even when they occurred experimentally.

---

## G18. [GLOBAL] How do datasets describe workflows linking sample prep, instruments, and readouts?

*ID: 0d50e369-771... | Latency: 30.1s*

**Answer:**

Datasets that *explicitly link sample prep → instrument → readout* tend to describe workflows as a structured chain of stages, where each stage contributes (a) files, (b) parameters/conditions, and (c) software/code needed to reproduce transformations. Across the provided materials, a few recurring patterns show up.

## 1) “Protocol-linked” workflows: conditions + procedure + post-processing as one machine-readable object
One approach is to treat the *protocol* as the glue that links the biological sample and prep conditions to both the measurement procedure and the readout extraction logic. For example, the Cardiac Electrophysiology Web Lab concept describes a stepwise roadmap in which datasets progress from “adding annotated data” to “linking data to protocols” and then to systematic comparison and provenance tracking [Data: Sources (28992, 109457)]. In that framing, a “protocol” includes experimental conditions and stimulus/measurement procedure (e.g., voltage-step sequences), and it may also include explicit post-processing steps needed to compute a reported summary readout (e.g., APD restitution curves) [Data: Sources (28996, 109460)]. The protocol is described as machine-readable and composed of foundational operations on n-dimensional arrays (time series such as voltage/current), enabling reproducible extraction of derived readouts like “peak current detection” or “APD measurement” [Data: Sources (28996)].

## 2) Raw vs pre-processed vs “code to reproduce pre-processing”
A common dataset pattern for linking measurements to downstream readouts is to store data artifacts in tiers:
- raw, unprocessed instrument output
- pre-processed data produced by experiment-specific handling
- the code (or scripts) that reproduce that pre-processing

This is explicitly recommended for electrophysiology datasets, where measurement artefacts (leak, drift, noise, capacitance artefacts) depend on the *measurement method* and therefore should not be “silently” normalized away. Instead, datasets “should” store raw + pre-processed + reproducible pre-processing code so the transformation is inspectable and reusable [Data: Sources (28995, 28994, 109459)].

## 3) File-level linkages: instrument outputs, intermediate formats, and exported analysis tables
Workflows are also described by naming the concrete file types that represent each stage of the chain. Examples include:
- **Microarray**: scanned image files (.DAT) → probe intensities (.CEL) → gene-level summaries [Data: Sources (77069)]. Other descriptions show scanning on an instrument (e.g., iScan/BeadArray reader) and processing in vendor software (GenomeStudio/BeadStudio) before export to text/CSV and downstream normalization/statistics in R/Bioconductor packages such as `lumi`/`limma` [Data: Sources (306556, 113654, 103167)].
- **Flow or mass cytometry**: acquisition produces raw FCS files, then normalization (e.g., bead normalization), gating/cleanup (exclude debris/doublets/dead cells), then export of channel summaries (mean ion counts) and/or gated-cell FCS for downstream statistics/visualization in R/FlowCore [Data: Sources (304403, 304404)].
- **Sequencing**: instrument output (BCL) → demultiplexing to FASTQ → alignment/count matrices → downstream analysis (e.g., Cell Ranger → Seurat workflows) [Data: Sources (289967)].

These file-type narratives are often how datasets concretely “link” the bench/instrument step to the analytical readout, because they define the handoff artifacts between tools.

## 4) Resource-table style metadata: naming instruments + acquisition software + analysis software
Many datasets describe the linkage by listing, side-by-side, (a) instruments used for data collection and (b) software used for collection and analysis. For example, reporting templates and methods sections often specify that flow cytometry data were acquired on a named cytometer with FACSDiva, microscopy images captured on specific microscopes, and qPCR acquired on a particular real-time PCR system [Data: Sources (279482, 292630)]. Similar “software and algorithms” tables enumerate analysis environments (FlowJo, ImageJ/Fiji, Prism, vendor MS tools, etc.), making the workflow traceable from sample handling to instrument readout to analysis package [Data: Sources (204, 283461, 299210)].

## 5) Provenance, annotation, and structured queries as workflow enablers
Finally, datasets often emphasize that workflow linkage depends on robust metadata: origin/species/cell type and experimental conditions, with a mix of free-form description and structured annotations for queryability (e.g., standards like MICEE) [Data: Sources (109458, 109457)]. Some systems additionally aim to document data provenance and (later) model provenance and continuous testing—treating the workflow as not only “lab → instrument → readout” but “lab → instrument → processed data → model comparison/fitting,” all traceable [Data: Sources (28992, 109457)].

---

## G19. [GLOBAL] How do biomedical papers attribute computational work and disclose commercial interests?

*ID: f2fbc257-16e... | Latency: 40.2s*

**Answer:**

## Attributing computational work (who did what)

Biomedical papers commonly make computational contributions explicit in **author contribution statements**. These statements may name who “undertook the bioinformatics” or “performed computational studies,” alongside who wrote the manuscript and supervised the project [Data: Sources (278855, 307533, 189519, 249567, 256058, +more)]. Many journals also support or require **CRediT-style roles** (e.g., *Software*, *Formal analysis*, *Visualization*, *Methodology*, *Validation*), which helps distinguish computational implementation from experimental work and writing [Data: Sources (174864, 256275, 256058, 284806, 249567, +more)].

Papers also often attribute computation by describing **software environments and versions** (e.g., R/Seurat, GraphPad Prism, FlowJo, ImageJ/CellProfiler) and, where applicable, pointing to **custom pipelines** [Data: Sources (299211, 283461, 297035, 213701, 102031, +more)].

## Sharing code/models and documenting computational methods

Across computational biology/modeling, a recurring issue is that papers may provide a model description but **omit the actual model file or code**, or provide code that is **insufficiently documented**, impeding reproduction and reuse [Data: Sources (64340, 64341)]. To address this, guidance recommends (i) clearly stating model assumptions and algorithms, potentially with pseudo-code for complex models, and (ii) depositing **code/model files** in repositories and/or as supplementary materials [Data: Sources (64339, 64365)].

Where standards exist, papers are encouraged to encode models in **interoperable formats** (e.g., SBML, CellML, PharmML, MDL) and deposit them in model repositories (e.g., BioModels, CellML) or public code platforms such as **GitHub** [Data: Sources (64340, 64365)]. Some publishers’ policies add that if **custom software is central** and not yet described in the literature, it **must be made available to editors and reviewers**, and code deposition (e.g., GitHub) is strongly encouraged [Data: Sources (278902, 283462, 102031, 283461, 297035, +more)].

In many papers, code availability is handled via explicit links (often GitHub) and “data/code availability statements” describing what is public, what is available on request, and what is restricted (e.g., patient data) [Data: Sources (292636, 299211, 291063, 278902, 211462, +more)].

## Disclosing commercial interests and industry involvement

Biomedical papers typically disclose commercial interests in a dedicated **Competing interests / Conflict of interest / Declaration of interests** section. Disclosures often include:
- **Employment and shareholding** in pharmaceutical/biotech companies (sometimes explicitly labelled “employees and shareholders”) [Data: Sources (173466, 149636, 64413, 105676, 251972, +more)].
- **Consulting, honoraria, advisory boards, research funding, travel support**, and other financial relationships with companies [Data: Sources (121634, 256275, 271869, 229784, 221248, +more)].
- **Equity ownership/founder roles** in startups and commercial entities [Data: Sources (251305, 201556, 255354, 105676, 120740, +more)].
- **Patents/patent applications** and institutional commercialization schemes (e.g., “reward for discoverers”) [Data: Sources (39349, 38042, 38311, 175106)].

Papers may also explicitly state the **role of funders**, commonly noting that funders/employers “had no role” in study design, data collection/analysis, interpretation, or publication decisions—even when authors are company employees or salaries are paid by commercial entities [Data: Sources (119245, 102789, 102791, 255699, 163834, +more)].

## Medical writing support and sponsor-funded publication assistance

Some biomedical papers disclose **medical writing support** (naming the writer and organization) and specify that this support was **funded by the sponsor**, while also describing authors’ involvement in drafting and approval [Data: Sources (119245)].

## Commercial-use restrictions vs open licensing (how “commercial interests” intersect with reuse)

In addition to conflict-of-interest disclosure, some papers/software releases describe **license terms that restrict commercial use**, e.g., releasing a tool under a CC BY-NC license and stating that non-academic/commercial users must contact the authors for commercial use [Data: Sources (289115)]. Conversely, many open-access articles specify permissive reuse under **CC BY**, while others use more restrictive variants (e.g., CC BY-NC-ND), which can affect downstream commercial reuse even when the paper is openly accessible [Data: Sources (188487, 8600)].

---

## G20. [GLOBAL] How do genomic repeat elements change across in vitro human germline cell states?

*ID: 7eb86183-e10... | Latency: 20.1s*

**Answer:**

Genomic repeat-element expression changes markedly as human cells transition from a pluripotent state (4i ES cells) into in vitro primordial germ cell-like states, with distinct classes of repeats moving in opposite directions rather than a uniform “repeat activation” program. In particular, **LTR7 and HERVH-int are downregulated** in **DM\*PGCLCs and DZ\*PGCLCs** relative to **4i ES cells** [Data: Sources (296916)]. Conversely, **LTR5_Hs and HERVK-int are upregulated** in **DM\*PGCLCs**, resembling the pattern reported for **week 5 PGCs** [Data: Sources (296916)]. Additional repeat families show state-dependent behavior in this in vitro germline context, including **SVA_D**, **LTR12C**, **ALR/Alpha (centromeric satellite)**, and **SST1** [Data: Sources (296916)].

These repeat-expression dynamics are linked to germline epigenetic remodeling and transcription-factor activity. The dataset describes repeat regulation in the context of **5hmC enrichment and 5mC depletion** at associated regulatory regions during germline progression [Data: Sources (296899, 296925)]. It further highlights that **DMRT1 binding to hominoid-specific LTR12C** coincides with **5hmC/5mC epigenetic changes**, and that this is accompanied by **upregulation of some neighboring genes, including mitotic arrest genes**, suggesting a potential regulatory role for these repeat-linked loci in human PGC programs [Data: Sources (296925)]. In contrast, **SVA_D activation** is reported to occur **without detectable upregulation of neighboring genes**, implying that different young transposable element families may engage distinct regulatory coupling to nearby genes across germline-like states [Data: Sources (296925)].

---

## G21. [GLOBAL] Which drugs, antibodies, and lead compounds are highlighted for further development?

*ID: a1a92826-5c3... | Latency: 30.1s*

**Answer:**

Several **small-molecule leads/compounds** are explicitly highlighted as being taken forward (or proposed) for further development. In a tetrahydroquinolone (THQ) antiprotozoal/antimalarial series, **JAG50 and JAG21** were identified as lead compounds, with **JAG21** described as a “mature lead compound” with sufficient drug-like properties to move to advanced formulations and with marked in vivo efficacy in models (including oral nano preparation efficacy) [Data: Sources (83719, 123241)]. In antimalarial lead series progression, **E209** and **N205** were front-runners in a *P. berghei* model and initial DMPK assessments, with **E209** selected for further profiling and advanced through candidate-selection checkpoints [Data: Sources (11246)]. For acute myeloid leukemia (AML) differentiation therapy, hit-to-lead optimization around **OXS007417** produced next-generation compounds **OXS008255** and **OXS008474**, highlighted as improved (PK and in vivo efficacy) leads relative to OXS007417 [Data: Sources (335811, 335884, 200775)]. For fibrodysplasia ossificans progressiva (ALK2/ACVR1), structural modification yielded advanced preclinical candidates **M4K2009**, **M4K2163**, and **M4K2117** (derived from compounds **6a**, **11b**, and **14k**) selected for further preclinical development [Data: Sources (124454)]. In kinetoplastid/NTD programs for leishmaniasis/Chagas and related indications, highlighted candidates and leads include **DNDI-0690** (promising oral candidate for cutaneous leishmaniasis), bicyclic nitroimidazoles **DNDI-8219** and **DNDI-0690**, oxaborole/benzoxaborole series members including **DNDI-5421**, **DNDI-5610** (lead optimization for leishmaniasis), and **DNDI-6148** (entered clinical phases), and the pyrazolopyrimidine lead **DDD853651 / GSK3186899** [Data: Sources (35868, 35349, 130675)]. For HAT, late-stage highlighted compounds include **fexinidazole** and the benzoxaborole **acoziborole** [Data: Sources (203253)]. For schistosomiasis, two hit series were specifically noted as improvable/optimizable in terms of potency vs cytotoxicity: **LSHTM-1507** and **LSHTM-1945** [Data: Sources (189862, 189830)].

A smaller set of **repurposed/approved drugs** is also pointed out as worth advancing or re-evaluating in development programs. In the context of accelerating approaches via repurposing, **auranofin**, **diidohydroxyquinoline**, and **ronidazole** are specifically named as existing approved/investigational drugs that may open “orthogonal approaches” due to known safety profiles [Data: Sources (203118)]. In a TB meningitis (TBM) future-therapy prioritization discussion, **high-dose rifampicin** is supported for further study, and **linezolid**, **delamanid**, and **pretomanid** are noted as meriting further evaluation [Data: Sources (230402)]. For CXCR4 modulation, the approved small molecule **AMD3100** is highlighted (approved and repurposed for stem cell mobilization), with **TG-0054 (burixafor)** and **AMD11070** in clinical trials/development [Data: Sources (65002)]. For antimalarial development guided by MMV target product profiles, **ACT-451840** is described as a new chemical class selected for early development [Data: Sources (96306)].

On the **antibody/biologic** side, the dataset highlights classes and specific antibody directions rather than many named development candidates. In AML, the “most attractive antibodies” under investigation are **anti-CD33** and **anti-CD123** monoclonal antibodies (CD33-directed agents are discussed as a major focus, including earlier clinical experience) [Data: Sources (146201)]. In Notch-pathway targeting, a safer approach is described for tumor-selective blockade: a combined **Jagged1/2 neutralizing antibody** made tumor-microenvironment–restricted via **Probody technology** [Data: Sources (113742)]. In cutaneous leishmaniasis immunotherapy, **CPG-D35 oligonucleotides** are described as a novel candidate immunotherapy approach aimed at activating immune cells in skin lesions [Data: Sources (35347)].

---

## G22. [GLOBAL] How do genetic perturbations of mTORC1 signaling alter hematopoietic progenitor and B-cell development?

*ID: d213ea4d-164... | Latency: 30.1s*

**Answer:**

Genetic perturbations that *reduce mTORC1 signaling* (most directly by deleting **Raptor**, the defining mTORC1 component) impair hematopoietic progenitor function and skew lineage output. In adult mice, inducible **mTOR** deletion in hematopoietic cells causes pancytopenia, increased apoptosis (with decreased Mcl-1), altered progenitor composition (skewing toward CMPs with fewer CLPs), and impaired colony-forming potential despite expansion of phenotypic LSK cells [Data: Sources (10010)]. More specifically implicating mTORC1, **Raptor** loss in HSC/progenitors disrupts HSC regenerative capacity and engraftment (cells home but show abnormal niche localization and fail to reconstitute) [Data: Sources (10012)]. In contrast, genetic or pharmacologic *dampening of signaling downstream of mTOR* can preserve or enhance long-term HSC function: **S6K1-deficient** mice and **rapamycin** treatment are associated with increased LT-HSC repopulating capacity [Data: Sources (10009)]. Conversely, *constitutive mTORC1 activation* (e.g., deletion of upstream brakes **PTEN** or **TSC1** in HSCs) drives loss of LT-HSC quiescence/self-renewal through increased cycling and ROS/mitochondrial biogenesis, leading to functional exhaustion; TSC1−/− HSCs show elevated ROS and reduced self-renewal [Data: Sources (10006)].

For **B-cell development**, mTORC1 is repeatedly implicated at early commitment and later maturation checkpoints. **Raptor cKO** causes a major loss of B-cell generation due to an *early block in lineage commitment* [Data: Sources (10028)]. When Raptor is deleted specifically within the B lineage, there is a *profound developmental arrest*: Mb1-Cre–driven Raptor deletion blocks cells at the **pre-B stage**, abrogating maturation, proliferation, germinal center responses, and antibody production; inducible hCD20-Cre deletion reduces germinal center B cells and nascent plasma cells, eliminating germinal centers and lowering serum antibody levels [Data: Sources (10028)]. In fetal/ontogenic settings, deletion of Raptor at the HSC stage (Vav-Cre) produces a *block in B-cell lineage commitment* alongside perinatal lethality from erythroid defects, and adult inducible Raptor deletion similarly confirms defective B-lineage commitment with dysregulation of key lineage regulators including **PAX5** [Data: Sources (57840, 57844)]. In a CLL-like model, Raptor deficiency in HSPCs prevents generation of CD19+ cells and blocks disease initiation, consistent with an HSPC-level inability to commit to the B lineage when mTORC1 is absent [Data: Sources (284495, 284515)].

Perturbations that *increase mTORC1 signaling* can also be detrimental to B-cell maturation. For example, B-cell-specific deletion of **TSC1** (a negative regulator upstream of mTORC1) renders mTOR constitutively active and is associated with a partial block in maturation (increased T1/T2 transitional B cells) and depletion of marginal zone B cells [Data: Sources (10027)]. Together, these genetic studies support a model in which B lymphopoiesis requires a “Goldilocks” level of mTORC1 activity: too little (Raptor loss) blocks commitment and key developmental transitions, while chronic hyperactivation (loss of upstream brakes) perturbs maturation programs.

Finally, although the question focuses on mTORC1, several genetic datasets distinguish **mTORC2** effects from mTORC1 during B-cell development. Rictor (mTORC2) loss has been reported to reduce mature splenic B cells while accumulating earlier bone marrow B-cell subsets (pro-B/pre-B/immature), linked to elevated FOXO1 and RAG1 expression [Data: Sources (10029)]. SIN1−/− hematopoietic cells can still reconstitute lineages, but show features consistent with mTORC2 acting *after* B-lineage commitment (e.g., altered IL-7 and RAG expression and fewer IgM+ immature B cells) [Data: Sources (10030)]. This supports the view that mTORC1 is more critical for *early hematopoietic and B-lineage commitment decisions*, whereas mTORC2 more subtly shapes later maturation and survival programs.

---

## G23. [GLOBAL] What study designs and matching strategies are used for selecting control cohorts?

*ID: b5ca74dd-524... | Latency: 40.1s*

**Answer:**

Control cohorts are selected using a mix of **randomized concurrent controls**, **historical controls**, and **matched observational control cohorts**, with matching implemented either by direct covariate matching (e.g., age/sex) or by **propensity score methods** (matching/weighting). The design choice is often driven by feasibility and bias considerations.

In **randomized controlled trials**, controls are created by random treatment allocation, commonly at **1:1**, but sometimes **2:1** (more participants on the new treatment) to increase information on the experimental arm while retaining a concurrent control group [Data: Sources (37776, 37778, 37784)]. Randomization may be “balanced” to maintain approximate allocation ratios at trial end and may use **stratification/minimisation** so that prognostic factors (e.g., disease stage, age group, gender) remain balanced between arms; minimisation may include a random element and may be reset when new arms are added in multi-stage trials to preserve within-stage balance [Data: Sources (37792, 37793, 133236, 133235)]. A key caution is that using **historical controls** alone can be misleading due to systematic changes over time (referral patterns, supportive care, clinician skill, selective inclusion), so some guidance recommends that at least **one-third** of patients should be randomized concurrent controls if historical comparisons are also used [Data: Sources (37778, 37779, 37784)].

In **observational case-control and cohort-based designs**, controls are frequently chosen via **individual matching** on core demographics. A population-based example transformed from a case-control study into a matched cohort used **age- and sex-matched controls from the general population**, assigned a “pseudo-diagnosis” date aligned to the case’s diagnosis age to ensure comparable follow-up timing, and retained registered controls regardless of interview participation to limit selection bias [Data: Sources (286900, 286910, 286923, 286910)]. Another nested case-control design selected controls using **incidence density (risk-set) sampling**, where each case was matched to a control randomly sampled from those still at risk at the case’s event time; controls could later become cases and could be sampled more than once. Matching included recruitment centre, sex, age at recruitment, recruitment date, follow-up time, and blood draw timing/fasting status [Data: Sources (96857, 96858)]. Some retrospective cohort studies also sample controls from electronic health databases in fixed ratios (e.g., ~5:1) and hard-match on age/sex and enrollment/index dates [Data: Sources (190163)].

Beyond simple matching, several studies use **propensity score (PS) matching** to construct control cohorts that are comparable across a broader confounder set. One example estimated the PS of “having cancer” and then selected the closest control satisfying hard-match constraints (same sex; age within ±2 years) plus a PS **caliper** (within 0.05 SD), incorporating covariates such as neighbourhood income, rurality, comorbidity indices, and long-term care residence at index date [Data: Sources (59760, 59774)]. Another example used PS matching with a **1:3 ratio** and a **0.25 SD caliper** after checking overlap to balance chemotherapy vs no chemotherapy groups while retaining sample size [Data: Sources (156696)]. Related weighting strategies are also used to address participation/nonresponse differences: inverse probability (propensity) weights can reweight respondents to the target population distribution of key characteristics (e.g., age, gender, language region, nationality, cancer type, relapse) [Data: Sources (330337, 330338)].

---

## G24. [GLOBAL] Which therapeutic and delivery strategies are discussed for targeting cells and peptides?

*ID: 867937d0-9f2... | Latency: 30.1s*

**Answer:**

A range of **peptide/protein therapeutic strategies** are discussed, including use of **protein-based vaccines** and **immunoregulatory peptides/proteins** as therapeutics (but limited by short half-life and poor uptake) [Data: Sources (13611)]. Peptides are also described as **targeted intracellular inhibitors** in cancer—used to target intracellular proteins essential for tumour proliferation/invasion, either as monotherapies or combined with conventional chemotherapeutics, and positioned alongside other “gene product interference” modalities (siRNA/shRNA, intracellular antibodies, dominant-negative proteins, aptamers) [Data: Sources (63535, 63536)]. For peptide therapeutics more broadly, strategies to improve in vivo performance include **engineering peptide analogs (e.g., with unnatural amino acids)** and **conjugation to polymers, fatty acids, or large proteins** to improve residence time and reduce clearance, especially for subcutaneous dosing [Data: Sources (57519, 57530)]. Specific chemical strategies highlighted include **PEGylation** (to raise effective molecular weight, reduce proteolysis via steric hindrance, and extend half-life) and **lipidation** [Data: Sources (314454, 314461)].

Several **carrier/delivery strategies for peptides and targeting cells** are described. A recurring approach is **encapsulation/embedding** of proteins and peptides in **polymer microcapsules, nanoparticles, or microgels**, with the caveat that a **release mechanism is required** because the polymer barrier can prevent activity at the target site until release occurs [Data: Sources (13611)]. For peptide drugs specifically, **polymeric nanoparticles** are discussed as a means to protect peptides from degradation, improve cellular uptake, enable targeted cellular/intracellular delivery, and sustain release; PLGA (including PEG‑PLGA) is highlighted as a biocompatible/biodegradable encapsulant used for peptide delivery [Data: Sources (63536, 63537, 63527)]. More generally, **polymer-based depot/controlled-release formulations** are cited as a way to optimize pharmacokinetics for long-term controlled release (examples of marketed products are mentioned) [Data: Sources (57530)].

Multiple **peptide-enabled cell-targeting and gene/nucleic-acid delivery approaches** are also discussed. **Cell-penetrating peptides (CPPs)** are presented as a major strategy to improve intracellular delivery of nucleic acids/oligonucleotides, via two main “vectorization” modes: **covalent conjugation** to cargo or **noncovalent nanoparticle complex formation** [Data: Sources (92282, 105338)]. CPP systems are further modified to improve endosomal escape and uptake, including **lipid (fatty acid/cholesterol) addition**, **fusogenic viral-derived sequences (e.g., influenza HA2)**, incorporation of **protonatable buffering domains (e.g., histidines/chloroquine analogs)**, and other strategies—balanced against increased toxicity risk [Data: Sources (92291)]. A related engineered format, **GET (GAG-binding enhanced transduction) peptides**, combines **heparan-sulfate binding**, **CPP elements**, and **endosomal escape elements** to enhance uptake/escape and has been used to deliver proteins and nucleic acids [Data: Sources (81978)].

For **cell-specific targeting**, several ligand-display strategies are described on nanoparticle surfaces. In **lipopolyplex gene delivery vectors**, cell-type targeting may be achieved by displaying **targeting peptides on the nanoparticle surface**, either through **bimodal peptides** (containing both receptor-binding and DNA-condensing sequences) or by **direct conjugation of the targeting ligand to a lipid** in the liposomal component; EGFR-targeting peptide sequences (e.g., GE11, D4, AE) are given as examples, and performance is noted to depend strongly on peptide sequence and architecture [Data: Sources (32762, 32767, 32797, 32768)]. In nanomedicine more broadly, **active targeting** is described as coupling **peptides/antibodies/ligands** to nanocarriers to bind disease-associated cell-surface biomarkers, with examples including **RGD-modified liposomes** for angiogenic endothelium and other peptide- or antibody-targeted liposomes [Data: Sources (292385, 292384)]. **Passive targeting** via the EPR effect is also discussed as a tumor accumulation mechanism for nanoscale carriers [Data: Sources (292376, 143179)].

Finally, several **triggered/spatiotemporal release strategies** are discussed that help concentrate action at target sites and/or enhance cellular uptake. These include **stimuli-responsive prodrug/linker approaches** (release in response to tumour/disease cues such as low pH, enzymes, redox, hypoxia, ROS) and **externally triggered release** mechanisms (e.g., **light, ultrasound, temperature, magnetic fields**) [Data: Sources (29137, 29210, 43644)]. **Ultrasound-mediated cavitation** with microbubbles is described as a way to increase membrane permeability and/or disrupt liposomes to trigger local release, including an example of **ultrasound-triggered release of a liposome-loaded radiopeptide** for cytotoxicity in EGFR-overexpressing cells [Data: Sources (118392, 118381)].

---

## G25. [GLOBAL] What parameters are reported to ensure reproducibility across biotechnology protocols?

*ID: 4a963d70-788... | Latency: 30.1s*

**Answer:**

Across the provided biotechnology-related sources, reproducibility is supported by reporting **both wet-lab experimental variables** (especially those known to inflate cross-site variation) and **analysis/statistical metadata** (sample sizes, replicate structure, tests, code/data availability). Key reported parameters include:

## Wet-lab protocol parameters to report (especially for iPSC differentiation and other multi-step cell workflows)

Multi-site iPSC differentiation work identified several *variation-inflating confounders* that are often not disclosed but were strongly suggested to become standard reporting items in published differentiation protocols, including: **iPSC passage number before differentiation; number of passages before “FP”; media volume changes; feeding at weekends; and whether frozen neural progenitor cells were used** [Data: Sources (105665, 173392, 105664, 173391, 170444)]. Reporting should also capture **passaging effects and progenitor storage** because they were highlighted as major contributors to site-driven variability [Data: Sources (105597, 105602, 173333, 173334, 173328, +more)].

Beyond these specific variables, the same study emphasizes the need to **recognize, record, and report experimental variables** in multi-site studies, because “laboratory/site” effects can dominate variance and mask biological signals [Data: Sources (105657, 105664, 173348, 173391, 170444)].

## Reagents, materials, and traceability information

To ensure experimental comparability over time, one reporting summary states that **reagent suppliers and catalog numbers were maintained as long as possible; when new reagents were introduced, validation/optimization experiments were performed to ensure comparable results** [Data: Sources (213706)].

## Replicate structure and what counts as an independent replicate

Multiple sources highlight reporting:
- The **exact number of biological and technical replicates**, and where replicate counts are provided (e.g., in figure legends) [Data: Sources (36194, 211197, 297568, 130881, 201779)].
- A clear definition of what constitutes a **biological replicate** (e.g., independent plates/cultures processed independently) [Data: Sources (201598)].
- Whether experiments were repeated on **separate days** and/or with **different passages** of cells (used explicitly as a replicate definition in one source) [Data: Sources (130881, 201779)].

## Statistics and analysis reporting required for reproducibility

Nature-style reporting summaries repeatedly require authors to report: **exact sample size (n); whether measurements are from distinct samples or repeated measures; how many times experiments were replicated; which statistical tests were used (including one- vs two-sided); covariates tested; assumptions/corrections (normality testing, multiple comparisons correction); and clear definitions of error bars/summary statistics** [Data: Sources (213697, 229800, 279480, 102030, 102031)].

## Data, code, and model parameter reporting (computational/quantitative protocols)

For computational model development and parameterization, reproducibility-focused guidance calls for detailed parameter documentation, including **parameter symbol/name, definition, value (or range), units, source/citation, and how the value was determined (measured, fitted, assumed), including limitations/outliers/excluded points** [Data: Sources (64398, 64367)]. Complementary guidance stresses the importance of **sharing raw data and code**, and (for broader reproducibility beyond rerunning the same code) using standardized, machine-readable model/protocol formats (e.g., **CellML/SBML for models; SED-ML for protocols**) [Data: Sources (28971, 28976, 28978, 109446, 109445)].

---

## G26. [GLOBAL] How do the studies connect specific mutations or signaling markers to cancer progression?

*ID: 759e35d7-8da... | Latency: 30.1s*

**Answer:**

Studies typically connect **specific mutations** or **signaling markers** to cancer progression by showing (i) that the alteration confers a selective growth/survival advantage (“driver” events), (ii) that it maps onto core hallmark-regulating pathways (cell fate, survival, genome maintenance), and/or (iii) that its activity level correlates with stage, metastasis, prognosis, or therapy response in patients and models [Data: Sources (241277, 241278, 215662, 221469, 219274, +more)].

A common connection is made through **canonical oncogenic pathway activation**. In lung cancer, activating events in RTKs or downstream nodes (e.g., **EGFR, KRAS, BRAF mutations; ALK fusions**) are described as promoting tumorigenesis via hyper-activation of the **PI3K/AKT/mTOR** and **RAS–RAF–MEK–ERK (MAPK)** cascades—pathways linked to malignant progression and used as targets for inhibitors in practice [Data: Sources (205061, 96820)]. Similarly, in NSCLC, **MET** dysregulation is tied to progression by showing that MET mutation/amplification or c-Met overexpression activates PI3K/AKT/mTOR and MAPK signaling and correlates with advanced stage and poor prognosis (and can mediate resistance to EGFR-TKIs) [Data: Sources (205064, 205178)].

Other studies connect progression by linking **marker abundance or phosphorylation status** to lesion grade or outcome. For example, **STAT3 pathway activation** is inferred from increased STAT3 protein and phosphorylation (including nuclear localization) in high-grade HPV lesions compared to low-grade/control tissue, supporting a relationship between this signaling marker and more advanced disease states [Data: Sources (6436)]. Hypoxia-associated markers provide another route: hypoxic tumors upregulate **HIF-1α**, which induces angiogenic programs (e.g., VEGF and additional targets), connecting a measurable transcriptional response to microenvironment-driven progression and vascularization [Data: Sources (241687)].

Several reports emphasize that progression is often tied to **late-arising mutations that enable invasion/metastasis or therapy resistance** rather than initiation alone. In pancreatic ductal adenocarcinoma, models describe early **KRAS** activation followed by intermediate events (e.g., CDKN2A loss) and later **TP53** mutation; acquisition of TP53 mutations in advanced disease is linked to genomic instability and an invasive/metastatic phenotype [Data: Sources (65821)]. In this context, mutant p53 is further connected mechanistically to aggressive behavior through altered transcriptional programs and interactions with chromatin-modifying complexes, affecting invasion, migration, and proliferation [Data: Sources (65822, 65825)].

Beyond DNA sequence changes, studies also connect progression through **epigenetic alterations and their pathway consequences**. Epigenetic changes (chromatin modification, DNA methylation, imprinting) are described as both contributing to tumor formation and potentially catalyzing genetic mutations, framing epigenetic state as an upstream driver of progressive transformation [Data: Sources (215662)]. Clinically relevant examples include epigenetic silencing of tumor suppressors such as **RASSF1A**, where promoter methylation/silencing correlates with advanced disease, metastatic potential, adverse prognosis, and (in analyses) reduced survival in lung adenocarcinoma [Data: Sources (111097)].

Finally, some studies connect progression using **stage- or subtype-enriched alterations** identified by comparative genomics/transcriptomics. In cutaneous SCC, amplification/upregulation of candidate driver genes during progression (including epigenetic modifiers such as **PRMT3**) and enrichment of alterations in pathways like **TGF-β signaling** in more aggressive (moderate/poorly differentiated) tumors are used to argue that these molecular changes track with—and may contribute to—progression [Data: Sources (36043, 36034)].

---

## G27. [GLOBAL] How do E-cadherin-targeting peptides alter AFM single-molecule adhesion measurements across experiments?

*ID: 16e13658-b01... | Latency: 30.1s*

**Answer:**

E-cadherin-targeting peptides primarily alter **AFM single-molecule force spectroscopy (SMFS)** readouts by **reducing the frequency of specific E-cadherin adhesion events**, while leaving the **rupture-force distributions of the remaining specific events largely unchanged** across experiments. This is consistent with a blocking/competitive effect that lowers the probability of bond formation during tip–sample contact rather than changing the underlying unbinding mechanics of bonds that still form [Data: Sources (277438, 277449, 277458, 277464, 277495)].

Across sequential buffer experiments on **Ecad-Fc functionalised surfaces**, both **Epep** and **EpepW2R** show reversible inhibition: after peptide exposure, switching back to **Ca²⁺ buffer** restores adhesion frequency toward baseline, and **DECMA-1** can still inhibit afterward—supporting that peptide effects are not due to irreversible probe/sample degradation [Data: Sources (277436, 277441, 277442, 277464, 277495)]. In titration-style experiments (1, 10, 100 µM), **Epep** shows a concentration-dependent drop in specific-event frequency with a plateau above the reported equilibrium concentration (~3.4 µM), and at higher concentrations its inhibition approaches that of **DECMA-1** [Data: Sources (277445, 277454, 277455, 277486, 277495)].

Force histograms for peptide-treated conditions repeatedly retain a **modal rupture force around ~30–40 pN** (often interpreted as strand-swap/S-dimer unbinding), indicating the **modal force regime is stable across Ca²⁺, EGTA/DECMA-1, and peptide buffers** even when event frequency changes [Data: Sources (277390, 277456, 277471, 277483, 277495)]. For **EpepW2R**, AFM detects inhibition of specific adhesion frequency despite prior cell-based assays reporting no loss of cell–cell contact; in AFM the inhibition can appear strong (at 100 µM comparable to EGTA/DECMA-1) and is also reversible with Ca²⁺ wash [Data: Sources (277463, 277464, 277487, 277488, 277583)]. Some force distributions for EpepW2R include an additional higher-force population (~60–70 pN) in certain conditions (notably reported at 100 µM), which is discussed as potentially consistent with alternate cadherin bond states (e.g., X-dimers) or other peptide-mediated interaction modes, though this interpretation was presented as tentative [Data: Sources (277472, 277580)].

When extending SMFS to **cell monolayers (E14 mESCs)**, peptide effects are qualitatively similar: **DECMA-1 reduces specific events**, and **Epep in culture medium reduces E-cadherin-specific adhesion frequency** relative to baseline, while the **modal rupture force remains near ~30 pN** across conditions—again suggesting peptides mainly modulate how often bonds form rather than the force of those that do [Data: Sources (277480, 277481, 277483, 277484, 277495)]. Experimental constraints differ on cells (e.g., EGTA not used because it detaches cells; medium contains Ca²⁺), and analysis thresholds were adapted (allowing longer rupture distances) due to the more compliant/ambiguous cell surface, which can affect event classification across experiments [Data: Sources (277430, 277433)].

---

## G28. [GLOBAL] What LC conditions and flow rates are used for peptide or protein pull-down MS analyses?

*ID: f534333f-aad... | Latency: 30.1s*

**Answer:**

Peptide/protein pull-down workflows that proceed to MS typically use **nano–reversed-phase (RP) LC** with **acidified water/acidified acetonitrile** mobile phases and low nL/min flow rates. Across the provided protocols, commonly reported **mobile phases** are **solvent A = 0.1% formic acid (FA) in water** and **solvent B = acetonitrile (ACN) with 0.1% FA** (often ~80% ACN in B) [Data: Sources (74942, 74943, 180322, 101726, 197746)]. In several setups, **5% DMSO** is included in both A and B (e.g., A: 0.1% FA + 5% DMSO in water; B: 0.1% FA + 5% DMSO in ACN), which is then used with standard 2–35% B peptide gradients [Data: Sources (181445, 211175, 102619, 138597)].

## Typical nanoLC gradients and flow rates (peptide-level LC-MS/MS after pull-down)
Many pull-down MS methods use a **75 µm ID C18 analytical column (often 50 cm)** at **~250–300 nL/min**, with gradients in the **~60–130 min** range:

- **250 nL/min**, C18 EASY-Spray **75 µm × 500 mm**, linear **2–35% B over 60 min** (A: 5% DMSO, 0.1% FA; B: ACN + 5% DMSO + 0.1% FA) [Data: Sources (181445)].  
- **250 nL/min**, trap + analytical PepMap setup; **2 h (120 min) gradient**: **3–6% B (3 min), 6–35% B (117 min), 35–47% (5 min), 47–100% (5 min), hold 100% (8 min)** [Data: Sources (74943)].  
- **300 nL/min**, EASY-Spray C18 50 cm; **3.8–50% B over 97 min** [Data: Sources (180322)].  
- **300 nL/min**, PepMap RSLC C18 75 µm × 50 cm; **2–35% B in 125 min, then to 98% B** (after loading on a trap at high flow) [Data: Sources (281125)].  
- **300 nL/min**, PepMap RSLC C18 75 µm × 50 cm; **5→35% B in 130 min then to 98% B**, followed by wash and re-equilibration [Data: Sources (245945)].  
- **300 nL/min**, in-house packed 25 cm C18; **5–30% B over 90 min, 30–55% over 20 min, then 98% B** [Data: Sources (101726)].  
- **200 nL/min**, in-house packed RP column; **5–28% B over 42 min, then 28–45% B over 13 min** [Data: Sources (297332)].  

Some pull-down-related methods use slightly higher nano flows (still sub-µL/min), e.g. **400 nL/min loading** with **200 nL/min elution** during a **90 min 2→35% B** gradient [Data: Sources (103147)].

## Long gradients for complex/enriched pull-down-type samples (e.g., glycopeptides)
For highly complex or enriched species (e.g., glycopeptides), much longer gradients may be used at typical nano flows:
- **300 nL/min**, EasySpray PepMap RSLC C18 **75 µm × 75 cm**; **0–32% ACN in 0.1% FA over 240 min**, then **80% ACN/0.1% FA for 35 min** (total ~275 min) [Data: Sources (284446)].

## Intact protein LC-MS (non-digest; less common in pull-down “proteomics”)
One intact-protein LC-MS method uses analytical-flow LC (not nanoLC), with FA in water/ACN and short gradients on a wider-bore column:
- Dionex Ultimate 3000 RSLC with **Aeris Widepore XB-C8 (150 × 2.1 mm)**; gradient from aqueous **0.1% FA** to ACN **0.1% FA** (intact mass measurement) [Data: Sources (285602)].

## Notes tied to pull-down handling but affecting LC injection solvents
Several protocols resuspend peptides for LC-MS in low-organic/acid (common for pull-down digests), such as **2% ACN + 0.1% FA** [Data: Sources (211175, 180322)] or **0.1% FA** alone [Data: Sources (284445)], before nanoLC separation.

If you want, I can extract a “most common default method” (column, buffers, gradient, and flow) as a single recommended starting LC method for pull-down proteomics based strictly on these sources.

---

## G29. [GLOBAL] Which scaffold design features are linked to improved cell growth and mineralization?

*ID: 92b9afa8-b4e... | Latency: 30.1s*

**Answer:**

Several scaffold **geometry and architecture** features are linked to better cell growth and/or mineralization. Across TPMS scaffolds, geometry (including curvature) has been described as a key driver of hMSC/pre‑osteoblast proliferation and differentiation, and TPMS are highlighted for their high surface-area-to-volume ratio that can increase available attachment area [Data: Sources (270799, 270749, 270607)]. Curvature in particular is repeatedly linked to osteogenic outcomes: pre‑osteoblast growth/bone tissue growth increased with **increasing concave curvature**, while little growth occurred on planar/convex regions [Data: Sources (270749)]. Related reports also note mineralization can preferentially occur in **curved cavities** rather than planar surfaces, and that **smaller curvature radius** cavities can yield higher mineralization [Data: Sources (270957)]. In one optimisation study, an “optimal” **Lidinoid TPMS** design was reported to achieve a substantially higher predicted average cell growth rate than comparator 2D scaffolds [Data: Sources (270943)].

**Pore size, porosity, interconnectivity and permeability** are consistently identified as enabling features for cell colonization and downstream tissue formation because they govern transport and cell movement. High porosity and rough surfaces are described as core scaffold requirements for attachment, differentiation and matrix formation, while maintaining adequate mechanical strength [Data: Sources (52300)]. Interconnected, permeable pore networks support nutrient/oxygen delivery and cell migration/penetration; insufficient transport in static culture is linked to peripheral-only growth, and pores can become occluded as cells/ECM accumulate—especially in smaller-pore / lower-porosity scaffolds—further hindering central tissue development [Data: Sources (233251, 233252)]. Empirically, smaller pores (e.g., ~215 µm) have been associated with significantly improved proliferation and ECM production in one study, while other work found larger pores could yield higher cell numbers by day 7 because improved migration outweighed initial attachment benefits from higher surface area [Data: Sources (233179)]. Pore **size gradients** (e.g., 100–750 µm) have been reported to improve **cell seeding efficiency** and promote more homogeneous cell distribution compared with homogeneous pores, even when homogeneous scaffolds had better mechanical properties [Data: Sources (233189)].

**Surface/topography and fiber architecture** also show links to osteogenic maturation and mineral deposition. Roughened struts and surface roughness are cited to enhance stem cell proliferation/differentiation and osteoblastic differentiation, potentially by altering cell shape and protein adsorption [Data: Sources (198476, 198455)]. On electrospun fibrous scaffolds, **fiber alignment** can modulate osteogenic readouts and mineral deposition, but effects can be cell-type dependent: aligned fibers increased ALP activity and calcium deposition for mature osteoblasts (MLO‑A5), whereas osteogenic progenitors (hES‑MPs) showed higher ALP/collagen/calcium on random fibers [Data: Sources (198394, 198428)]. Beyond fibers, nanoscale disorder/ordering is described as influential: disordered “near-square” nanopit patterns increased osteogenic response relative to ordered patterns in one report [Data: Sources (9914)].

Finally, **bioactive mineral phases and osteoinductive factor integration** are repeatedly associated with stronger osteogenic differentiation and mineralization on/within scaffolds. Hydroxyapatite addition to polymer scaffolds increased MSC ALP activity versus non-HA controls [Data: Sources (5652)]. Bioactive glass–nanocellulose composite cryogels formed hydroxyapatite layers, had rough mineralized surfaces favorable for cell functions, and supported mineralization (Alizarin Red positive) in the bioactive composite but not in the cellulose-only control [Data: Sources (52315, 52321)]. Delivery of osteoinductive factors is also highlighted: combining scaffold geometry with osteogenic media and **BMP‑2** is described as enhancing proliferation/differentiation/mineralization more than single parameters alone, and BMP‑2 supplementation on gyroid scaffolds increased ALP secretion and showed more calcium deposition by Alizarin Red [Data: Sources (270799, 270862)].

---

## G30. [GLOBAL] How do diffusion coefficients and porosity values shape drug-release model predictions?

*ID: 4b2e3832-1eb... | Latency: 30.1s*

**Answer:**

Diffusion coefficients and porosity primarily shape drug-release model predictions by setting the **timescales and rate-limiting resistances** for mass transport, and by shifting which physics must be included (pure diffusion vs advection–diffusion) in order to match observed release curves.

In mechanistic implant models, the **free diffusion coefficient** in the release medium (often taken as \(D_f\sim10^{-9}\,\mathrm{m^2/s}\) as a baseline) directly controls how quickly dissolved drug can be transported away from the device; reducing \(D_f\) slows release (longer diffusion timescale) in both orifice and porous-wall designs, although the sensitivity depends on whether advection is dominating transport in parts of the geometry [Data: Sources (193102, 193126, 193129, 193133)]. In stirred **orifice-pin** systems, computed transport can be **advection-dominated** within the orifices/core, so changes in \(D_f\) may have negligible impact during periods when the medium is saturated and advection is the fastest process, but will matter once concentrations fall below saturation and diffusion becomes more important [Data: Sources (193113, 193129)]. This is why a **3D dissolution–advection–diffusion** model is required for orifice pins, and why adding flow accelerates release relative to diffusion-only predictions [Data: Sources (193055, 193108, 193138)].

Porosity shapes predictions mainly by changing the **effective diffusivity through the porous barrier**, and thereby the device’s overall transport resistance. In porous-wall systems, the porous-wall diffusion coefficient is commonly related to the fluid diffusion coefficient via porosity and tortuosity (e.g., \(D_p/D_f=\phi_e/\lambda\), with \(\phi_e\) taken as ~90% of bulk porosity and tortuosity often assumed ~3) [Data: Sources (266419, 193102, 193103)]. Sensitivity analyses show that, for a porous pin, **increasing wall porosity yields faster release**, and varying porosity over a plausible range (0.1–0.75) can shift the predicted time to 95% release from ~81 days down to ~23 days—indicating strong porosity sensitivity when diffusion through the wall is rate-controlling [Data: Sources (193132)]. In contrast, because the porous pin release profile is largely **insensitive to external flow**, models can often be reduced to a **radial 1D dissolution–diffusion** description without losing accuracy (1D/2D/3D diffusion predictions are nearly indistinguishable) [Data: Sources (193114, 193117, 193138)].

A key implication for model predictions is that diffusion/porosity parameters don’t act in isolation: they interact with dissolution and boundary conditions via nondimensional balances (e.g., reaction–advection–diffusion competition). For example, when solubility limits apply (medium saturation), changing dissolution rate may have little effect because release becomes transport-limited (diffusion/advection) until the system desaturates; conversely, changing porosity or diffusivity directly changes the transport bottleneck [Data: Sources (193130, 193131, 193134, 193138)]. Additionally, simplifying the release medium to an **infinite sink** boundary can overestimate release, so diffusion/porosity sensitivities may be misrepresented if the external concentration field is modeled too aggressively [Data: Sources (193135)].

---

## G31. [GLOBAL] How does age at diagnosis relate to reported effect estimates across studies?

*ID: 7f65d678-7cf... | Latency: 20.1s*

**Answer:**

Across studies, *older age at diagnosis* is generally associated with *larger adverse effect estimates* (higher relative risk/hazard/odds), while *younger age at diagnosis* often appears “protective” (lower relative measures). The strength of this age–effect relationship varies by outcome and whether effects are reported on a *relative* (e.g., HR/OR/SMR) versus *absolute excess* scale (e.g., AER).

Several studies quantify a monotonic increase in relative effect with increasing age at diagnosis. For example, one analysis reports a **1.50-fold increase per 10-year increase in age at diagnosis** (95% CI 1.47–1.53), and categorical estimates rise from the 45–54 group (reference) to older age bands (e.g., HR 1.32 for 55–64 vs 45–54) [Data: Sources (205904, 207999)]. In other disease settings, a systematic review of surveillance outcomes reports that increasing age is consistently associated with higher risks (e.g., for advanced neoplasia/cancer at surveillance), with continuous-age ORs/HRs above 1 (e.g., OR 1.04 per yearly increment; HR 1.02 per year) and older-age groups having higher incidence than younger reference groups [Data: Sources (212603, 212604, 212606, 212610)].

In contrast, some survivor studies show **decreasing relative excess risk with increasing age at cancer diagnosis**, because the comparator is the *general population* where baseline risk rises with age. In a large study of teenage/young-adult cancer survivors, **SMRs for cardiac mortality decreased with older age at cancer diagnosis**, dropping from **~4.2 at diagnosis age 15–19** to **~1.2 at age 35–39**, with similar declines in AER (3.6 to 1.4) [Data: Sources (97922)]. This illustrates that, depending on the metric, older age at diagnosis can be linked to *lower relative excess* (SMR) even when absolute risks may not fall.

Studies that explicitly test age interactions also suggest that malignancy-associated relative effects may be *stronger at younger ages*. For example, the association between malignancy and herpes zoster was more pronounced in younger participants (solid malignancy OR 1.70 for <50 vs 1.11 for >80; haematological OR 3.08 vs 1.77) [Data: Sources (332082)]. This pattern is consistent with a diminishing *relative* contrast at older ages as baseline risk increases.

Finally, some multi-parameter survival modeling indicates that the age effect may be **non-linear and time-varying** rather than constant over follow-up. Excess mortality hazard ratios were higher for older patients, but differences between ages could be largest soon after diagnosis and again later, with periods where age effects converge (e.g., around ~18 months after diagnosis in some models) [Data: Sources (205809, 205810)].

---

## G32. [GLOBAL] Which immune cell types and markers are used to track hematopoiesis changes in mice?

*ID: cc1f6c7f-513... | Latency: 30.1s*

**Answer:**

Mouse studies typically track hematopoiesis changes by flow-cytometric quantification of **HSPC (stem/progenitor) compartments** plus **committed progenitors and mature lineages**, using a combination of lineage-exclusion (“Lin−”) and defining surface markers.

## Hematopoietic stem and multipotent progenitor compartments (HSPCs)
Commonly used populations include:
- **LSK cells (Lin− Sca-1+ c-Kit/CD117+)** as a broad HSPC gate [Data: Sources (125541, 12601, 134657, 203881, 330864, +more)].
- **Phenotypic HSCs (often “SLAM-HSCs”)**: **LSK CD150+ CD48−** (sometimes with **CD34− and/or Flt3−** to enrich LT-HSCs) [Data: Sources (283346, 44065, 99929, 125540, 134657, +more)].
- **MPPs**: typically **LSK CD150− CD48+** [Data: Sources (122622, 99955, 191186, 330864, 44065, +more)].
- **Flt3/CD135 and CD34** are frequently used to resolve early progenitor subsets (e.g., LT-HSC vs ST-HSC vs LMPP) within LSK [Data: Sources (330803, 191186, 327782, 330864, 99929, +more)].

**Lineage-depletion (“Lin”) marker cocktails** used to exclude mature cells commonly include combinations of **CD3/CD4/CD8 (T cells), B220 (B cells), Ter119 (erythroid), Ly6G/Gr-1 (granulocytes), CD11b/Mac-1 (myeloid)** [Data: Sources (44127, 134657, 229662, 294432, 330864, +more)].

## Myeloid and erythroid committed progenitors
Once past LSK, many studies quantify myeloid/erythroid progenitors in the **LK gate (Lin− Sca-1− c-Kit+)**, then subdivide using markers such as **CD34** and **CD16/32 (FcγR)**:
- **CMP**: LK **CD34+ CD16/32−**
- **GMP**: LK **CD34+ CD16/32+**
- **MEP**: LK **CD34− CD16/32−**  
[Data: Sources (146872, 191186, 194661, 330864, 125546, +more)]

Other erythro-megakaryocytic branch readouts used include **MkP** and staged erythroblast populations (EryA/B/C, ProEry) in some panels [Data: Sources (283429, 89920)].

## Mature lineage outputs (peripheral/BM composition)
To detect lineage skewing downstream of progenitors, common mature markers include:
- **Erythroid**: **Ter119** (often with **CD71** for erythroid maturation staging) [Data: Sources (122508, 287125, 294432, 69240, 69246, +more)].
- **Neutrophils/granulocytes**: **CD11b+ Ly6G+** (or **Mac-1+ Gr-1+**) [Data: Sources (122508, 69240, 173504, 24242, 68296, +more)].
- **Monocytes/myeloid**: **CD11b** with additional markers depending on context (e.g., Gr-1/Ly6C/Ly6G; F4/80 for macrophage-lineage) [Data: Sources (44127, 68296, 72975, 155604, 196242, +more)].
- **Lymphocytes**: **B220/CD19** (B cells) and **CD3/CD4/CD8** (T cells) [Data: Sources (44127, 146867, 173504, 294432, 69240, +more)].

## Cell-cycle/proliferation readouts used alongside immunophenotyping
To interpret “hematopoiesis change” as altered HSC/progenitor turnover, studies also track:
- **Ki-67** (often with **DAPI/7-AAD** for cell-cycle staging) and/or **BrdU incorporation** in defined HSC gates [Data: Sources (191188, 330816, 327788)].

These marker sets are repeatedly used to quantify shifts in HSC abundance (e.g., LSK CD150+CD48−), progenitor balance (CMP/GMP/MEP/CLP), and mature output (Ter119+ erythroid vs CD11b+Ly6G+ neutrophils, etc.) as readouts of hematopoiesis changes in mice [Data: Sources (122508, 146872, 191186, 327788, 44065, +more)].

---

## G33. [GLOBAL] Which thresholds and criteria define statistical significance in the dataset’s analyses?

*ID: 8d2d1f6a-0d0... | Latency: 30.1s*

**Answer:**

## Core statistical-significance thresholds (p / α)

Across the dataset’s analyses, statistical significance is most commonly defined using a **p-value threshold of 0.05** (often explicitly described as “alpha set to 0.05” or “p<0.05 considered significant”) [Data: Sources (97171, 228188, 255956, 53959, 206430, +more)]. Many results also use the standard “star” annotation scheme tied to increasingly stringent p-value cutoffs (e.g., * for p<0.05; ** for p<0.01; *** for p<0.001; **** for p<0.0001) [Data: Sources (228188, 135017, 278239, 206430, 28360, +more)].

Some analyses apply **more stringent p-value thresholds in specific contexts**, including:
- **Bonferroni-adjusted thresholds** for certain comparisons (e.g., p≤0.003 when comparing continents; other group-specific thresholds such as 0.016 or 0.025 depending on the subgrouping) [Data: Sources (216539)].
- A stated **threshold for statistical significance between treatments of p≤0.008** in at least one analysis [Data: Sources (216771)].
- **Genome-wide association** thresholds such as **p < 5×10⁻⁸**, and gene-wide/pathway/tissue Bonferroni thresholds such as **p < 2.8×10⁻⁶** (gene-wide), **p < 1.15×10⁻⁶** (pathways), and **p < 8×10⁻⁵** (tissue enrichment), often alongside **FDR < 0.05** [Data: Sources (97070, 106348, 97072)].
- **Interim-analysis stopping boundaries** with a much smaller two-sided efficacy boundary (e.g., **0.00312**) and a futility boundary based on an O’Brien–Fleming approach (e.g., **0.39 one-sided**) [Data: Sources (38526)].

## Criteria involving multiple-testing adjustment (FDR / q-values)

Several parts of the dataset explicitly require significance to be based on **multiple-hypothesis adjusted p-values**:
- As a general rule in some methods sections, results are considered significant if an **adjusted p-value** (e.g., **FDR q-value** or **Bonferroni-corrected p**) is **<0.05**, with exceptions when stricter criteria are used [Data: Sources (201599)].
- Some workflows specify different thresholds by analysis type:
  - Differential abundance: **raw p<0.05 AND BH-adjusted p<0.25** [Data: Sources (289927)].
  - Differential fate probability / metabolic flux / differential expression: **BH-adjusted p<0.05** [Data: Sources (289927)].
  - Other analyses: **raw p<0.05** [Data: Sources (289927)].
- Other examples include DESeq2-style differential-expression thresholds requiring **FDR < 0.05** combined with effect-size filters (see below) [Data: Sources (104686)] and methylation or other analyses using **FDR below 0.05** [Data: Sources (68671)].
- Some exploratory analyses highlight **raw p<0.05**, then apply **Benjamini–Hochberg FDR adjustment** to reduce Type I error under multiple comparisons [Data: Sources (139042)].

## Effect-size and combined “biological + statistical” criteria

In multiple places, “significance” is not defined by p-values alone, but by **p-values/FDR plus effect-size thresholds**:
- Differential expression: DESeq2 thresholds such as **average baseMean > 20**, **abs(log2 fold change) ≥ 1**, and **FDR < 0.05** to call genes differentially expressed; and definitions for “unregulated” genes such as **abs(log2FC) ≤ 0.2 AND FDR > 0.8** [Data: Sources (104686)].
- Microarray-type filters sometimes combine a **p-value cutoff (0.05)** with a **fold-change cutoff (e.g., 1.5)** [Data: Sources (65780)], and in another case genes are retained only if **−log10(adjusted p) > 2** and **log2(fold change) > 0.5** [Data: Sources (24018)].
- Proteomics quantitation includes a software-defined identification filter (e.g., “significance of 13” corresponding to **FDR-adjusted p≤1%**) plus other quality filters, then uses **p<0.05** and a **fold change of 1.5** for downstream selection [Data: Sources (39532)].

## Assumption checks that gate which significance criterion applies

Several analyses specify **decision rules for choosing parametric vs nonparametric tests**, which indirectly define how statistical significance is assessed:
- **Normality testing** (e.g., Shapiro–Wilk or D’Agostino–Pearson) is performed; if normality holds, **t-tests/ANOVA** are used; otherwise **Mann–Whitney/Kruskal–Wallis/Friedman** approaches are used, typically still using **p<0.05** as the significance threshold [Data: Sources (214638, 194052, 281843, 216742, 201599)].
- **Variance heterogeneity** sometimes triggers **Welch’s correction**, reflecting a criterion that equal variances are not assumed; significance is still typically evaluated at **p<0.05** [Data: Sources (97171, 194052)].

## Notes on reporting and exceptions

Not all analyses adjust for multiple comparisons; at least one text chunk explicitly states that **adjustments were not made for multiple comparisons** while still using p-value thresholds (e.g., p<0.01, p<0.001) [Data: Sources (214638)]. Another modeling-focused analysis notes that results labeled “statistically significant” refer to **adjusted p<0.05**, but cautions that these are **approximate** and may overstate significance [Data: Sources (13851)].

---

## G34. [GLOBAL] Which small-molecule inhibitors are used to modulate inflammatory and osteoclast differentiation programs?

*ID: 44db0c2b-703... | Latency: 40.2s*

**Answer:**

Small-molecule inhibitors used to modulate **inflammatory programs** and/or **osteoclast differentiation programs** in the provided text include:

## NF-κB / IKK pathway inhibitors (anti-inflammatory; anti-osteoclastogenic)
These agents inhibit NF-κB signaling, a core inflammatory pathway that is also essential for RANKL-driven osteoclastogenesis. Small-molecule IKK inhibitors can inhibit osteoclast formation in vitro and prevent inflammatory bone loss/destruction in vivo.  
- **BMS-345541** (highly selective IKK inhibitor) blocks joint inflammation and destruction in collagen-induced arthritis in mice [Data: Sources (7804)]  
- **Small-molecule IκB kinase (IKK) signaling inhibitors** (class) inhibit osteoclast formation in vitro and prevent ovariectomy-induced bone loss in vivo [Data: Sources (7803)]  
- **Parthenolide (PTN)** (verified NFκB inhibitor) reduces cancer-related osteoclastogenesis/osteolysis (reported in metastatic breast cancer models and studied in prostate cancer–related osteolysis contexts) [Data: Sources (42658, 7790)]  
- **Amlexanox** suppresses osteoclastogenesis and prevents ovariectomy-induced bone loss [Data: Sources (7805)]  

## Prostaglandin/COX axis inhibitor (inflammation-linked osteoclastogenesis)
- **Indomethacin** (NSAID; COX inhibitor) suppressed LTA-induced osteoclast differentiation and completely blocked LTA-induced bone resorption in organ culture; it also blocked LTA-induced PGE2 and RANKL expression in osteoblast-lineage cells [Data: Sources (214357, 214358)]

## Epigenetic bromodomain inhibitors (osteoclast differentiation program; inflammatory-linked outputs)
Inhibition of BRPF bromodomains suppressed RANKL-driven osteoclast differentiation and reduced osteoclast functional markers (e.g., actin rings, pit formation, MMP9 secretion).  
- **OF-1** (BRPF bromodomain inhibitor) suppresses osteoclast fusion/differentiation (mouse and human) and can completely suppress multinucleated osteoclast-like cell formation under tested conditions [Data: Sources (99737, 99744, 99745)]  
- **NI-57** (BRPF bromodomain inhibitor) suppresses osteoclast differentiation and resorption activity [Data: Sources (99737, 99745)]  
- **PFI-4** (BRPF-family bromodomain probe; less complete suppression than OF-1 in the cited comparison) reduces osteoclast differentiation and MMP9 secretion [Data: Sources (99744, 99747)]

## Histone deacetylase inhibitors (HDACi; osteoclast differentiation program)
Several HDAC inhibitors are described as blocking osteoclast differentiation/osteoclastogenesis.  
- **Romidepsin** (preferential HDAC1/2 inhibitor) inhibits osteoclastogenesis [Data: Sources (47221)]  
- **Trichostatin A (TSA)** inhibits osteoclast differentiation and has been reported to cause osteoclast death (noting some contradictory findings regarding RANKL induction) [Data: Sources (47224)]  
- **Sodium butyrate (NaB)** inhibits osteoclast differentiation [Data: Sources (47224)]  
- **MS-275** (HDAC2-specific inhibitor) reported to reduce bone absorption [Data: Sources (47224)]

## BMP type I receptor inhibitors (SMAD/BMP program intersecting bone cell differentiation and osteoclast burden)
These are primarily framed as BMP pathway inhibitors, but are also shown to reduce osteoclast formation in vitro and osteoclast number/burden in vivo in a myeloma bone disease setting.  
- **LDN-193189** (pan-BMP type I receptor inhibitor) reduced osteoclast formation in vitro and reduced osteoclast number in vivo (myeloma model) [Data: Sources (117128, 117129)]  
- **Dorsomorphin** (BMP signaling inhibitor) is cited as a BMP small-molecule inhibitor (used broadly to block BMP-SMAD1/5/8 phosphorylation) [Data: Sources (124329, 162534)]  

## Hypoxia/HIF-modulating small molecules used in osteoclast differentiation studies
These are used to modulate hypoxia/HIF signaling, which affects osteoclast differentiation and resorption activity.  
- **Dimethyloxalylglycine (DMOG)** inhibited formation of murine osteoclasts in the cited experiments [Data: Sources (90067)]  
- **Desferrioxamine** inhibited murine osteoclast formation and (per the review text) inhibits human monocyte–osteoclast differentiation [Data: Sources (90067)]  
- **CoCl₂** inhibited differentiation of human PBMC to osteoclasts in the cited experiments [Data: Sources (90067)]

## Receptor tyrosine kinase inhibitors affecting osteoclastogenesis (cFMS/CSF-1R axis and related RTKs)
These kinase inhibitors are described as decreasing osteoclastogenesis and/or increasing osteoclast apoptosis, often through **cFMS (CSF-1R)** signaling inhibition.  
- **Imatinib mesylate** decreases osteoclastogenesis and increases mature osteoclast apoptosis via inhibition of cFMS signaling [Data: Sources (150186)]  
- **Dasatinib** abolishes osteoclast formation in vitro by inhibiting cFMS activation [Data: Sources (150186)]  
- **Sorafenib** (RET/VEGFR inhibitor) is described as targeting osteoclasts similarly [Data: Sources (150186)]

## Osteoclast effector-enzyme inhibitors (bone resorption program)
- **Zoledronic acid (zoledronate; nitrogen-containing bisphosphonate)** induces osteoclast apoptosis via mevalonate-pathway inhibition and inhibits osteoclast differentiation in described settings [Data: Sources (327761, 68338)]  
- **Cathepsin K chemical inhibitors** (class) were developed to treat malignant and nonmalignant bone loss by targeting a key osteolytic cysteine protease [Data: Sources (151435)]  
- **MMP9 targeting by antisense oligodeoxyribonucleotide** (not a small molecule, but an osteoclast migration/resorption target noted in the dataset) affects osteoclast migration and resorption [Data: Sources (151435)]

## “Drug-like” small-molecule analogues (SMAs) with anti-inflammatory and anti-osteoclast differentiation effects
Synthetic phosphorylcholine-based SMAs that mimic the helminth product ES-62 can inhibit osteoclast differentiation and functional maturation, linked to induction of antioxidant response and suppression of ROS needed for heightened osteoclastogenesis in inflammatory disease contexts.  
- **SMA 11a** inhibits functional osteoclast differentiation in vitro [Data: Sources (12583, 12635)]  
- **SMA 12b** inhibits osteoclast differentiation and decreases expression of key osteoclast genes (including NFATc1, MMP9, cathepsin K, DC-STAMP, β3) [Data: Sources (12642, 12656)]

---

## G35. [GLOBAL] Which phosphorylation and gene-expression readouts are used to measure pathway activation?

*ID: 0a767917-4e8... | Latency: 30.2s*

**Answer:**

Pathway activation is measured using both **phosphorylation-based** (protein/post-translational) readouts and **gene-expression–based** (transcriptional) readouts, with the chosen readout often reflecting how proximal or distal the assay is to the initiating receptor/transducer event (e.g., binding vs downstream amplification) [Data: Sources (286655, 286656, 286660, 286661)].

## Phosphorylation readouts (protein-level activation)
Common phosphorylation readouts include direct quantification of specific phospho-proteins by **immunoblotting (Western blot)** or **phospho-specific antibody assays/arrays**, and broader discovery via **mass-spectrometry phosphoproteomics** [Data: Sources (286661, 7765, 146012, 145967, 210236)]. Examples of phospho-readouts used as activation markers include:
- **pERK1/2 (p44/p42)** as a MAPK pathway activation readout (often measured by Western blot; sometimes quantified as phospho/total ratio) [Data: Sources (102432, 102437, 230084, 326065, 330315)].
- **pAKT** as a PI3K/AKT pathway activation readout [Data: Sources (102432, 122547, 334440, 82509, 326065)].
- **p38 and pJNK phosphorylation** as MAPK branch activation readouts [Data: Sources (102432, 230084, 31053, 6836)].
- **pSTAT family members** (e.g., **pSTAT3**, also STAT1/STAT5 in some contexts) as JAK/STAT pathway activation readouts (measured by phospho-specific antibodies via flow cytometry or immunoblot/IF/IHC) [Data: Sources (226261, 38733, 309437, 40703, 8553)].
- **mTORC1 downstream phosphorylation targets**, especially **phospho-ribosomal protein S6 (pS6; Ser235/236)**, used as a well-established marker for mTORC1 activity (including by flow cytometry) [Data: Sources (167334, 8553, 8566, 226261, 82509)].
- **ATM and Chk2 phosphorylation** as DNA damage pathway activation readouts (reported as increased phosphorylation of ATM and its downstream target Chk2) [Data: Sources (290449)].
- **Receptor phosphorylation** itself (e.g., phosphorylation of a receptor measured by Western blot) [Data: Sources (325705)].
- Larger phospho-panels: **RPPA** and other antibody-based multiplex formats using multiple phospho-markers (e.g., phospho-p70S6R, phospho-AKT, phospho-ERK, phospho-4EBP1, phospho-EIF4G, phospho-Chk1) as pathway engagement/activation readouts [Data: Sources (82509)].
- Broad phosphoproteomic inference of kinase pathway activation using **kinase-substrate enrichment analysis (KSEA)** from MS phosphoproteomics (e.g., inferring activation of kinases such as MAP2K1 and JAK2 from regulated phosphosites) [Data: Sources (197642, 197735, 197736)].

## Gene-expression readouts (transcriptional activation)
Pathway activation is also inferred from transcriptional outputs measured by **RNA-seq**, **microarrays**, **targeted gene panels/arrays**, and **RT-qPCR**, then summarized with enrichment or causal inference tools [Data: Sources (290672, 83209, 53151, 100010, 330315)]. Common gene-expression readouts include:
- **RT-qPCR of pathway target genes** or marker genes (used to validate pathway-associated DEGs) [Data: Sources (290672, 81345, 108693, 116506, 325705)].
- **Expression of immediate-early / MAPK-responsive transcription factors**, e.g. **EGR1** and **IER2** reported as downstream of MAPK with increased expression under certain perturbations [Data: Sources (38019)].
- **Expression of pathway target gene sets**, such as **Notch target genes** (e.g., NRARP, HES1, HEY1) used to indicate activation at the transcriptional level [Data: Sources (53151)].
- **Gene set enrichment / pathway enrichment** based on differential expression (DESeq2/edgeR/limma voom) using tools such as **GSEA/clusterProfiler**, **DAVID**, **Reactome classifiers**, **Metascape**, **MetaCore**, and **pathfindR** to infer which pathways are up/down [Data: Sources (43350, 197032, 290672, 77093, 100010)].
- **Ingenuity Pathway Analysis (IPA)** to infer pathway activation states and **upstream regulator activation** using z-scores (e.g., TFs or signaling regulators predicted as “activated” when target-gene changes match known activation patterns) [Data: Sources (40703, 83209, 290672, 81346)].
- Examples where pathway activation is concluded from gene programs: transcriptional signatures consistent with **PI3K signaling** contributing to a disease transcriptional program (based on genes altered upon PI3K inhibition vs disease DEGs) [Data: Sources (334430, 334431)].

## Reporter-gene readouts that reflect pathway-driven transcription
Some pathway activation measurements use **luciferase reporters** controlled by pathway-responsive transcriptional elements, e.g.:
- **NF-κB SEAP reporter** for NF-κB activity [Data: Sources (197069)].
- **WNT/β-catenin (TopFlash) luciferase** and **NOTCH (4xCSL) luciferase** reporters [Data: Sources (306443)].
- **MEF2-dependent reporter assays** (MEF2–GAL4 luciferase) described as a more direct transcriptional readout of **ERK5** activity when ERK5/MEK5 are co-expressed to stimulate the pathway [Data: Sources (84990, 84993)].
- More generally, pathway-specific luciferase constructs used with stimuli such as WNT3A, TNFα, or TGFβ1 [Data: Sources (108693)].

---

## G36. [GLOBAL] What sampling strategies are used to characterize drug exposure in infectious disease studies?

*ID: b8cbf787-b91... | Latency: 30.2s*

**Answer:**

Sampling strategies used to characterise drug exposure in infectious disease studies generally range from **rich/intensive sampling** (many samples per participant to define a full concentration–time curve) to **sparse sampling** (few samples per participant, enabling larger sample sizes and population PK/PD modelling) [Data: Sources (230257, 68500, 93018)].

A common strategy is **intensive PK sampling in a subset**, sometimes early in development or in key populations, followed by **population PK using sparse designs** to reduce participant burden (especially in ill children) while still estimating exposure parameters and variability [Data: Sources (68500, 93018, 90126)]. Sparse designs may be **randomised across predefined post-dose time “windows”** so that, collectively, participants cover the dosing interval; for example, three samples per person randomised within several post-treatment time blocks, with protocols adjusted when later concentrations prove unmeasurable [Data: Sources (70175)]. Another sparse approach assigns participants to combinations of **early/middle/late time points** (e.g., minutes–hours for absorption plus 24–72 h for clearance), explicitly to minimise invasiveness while maximising information and avoiding the pitfalls of purely opportunistic/scavenged sampling [Data: Sources (110289, 110304)].

Many studies incorporate **targeted time points** chosen for clinically predictive exposure metrics, such as **day 7 concentrations** for medium/long half-life antimalarials (often aligned with routine follow-up visits), with earlier/more frequent sampling for short half-life drugs [Data: Sources (93018, 68499)]. For reinfection/recrudescence analyses, guidance emphasises having at least enough sampling to estimate elimination (e.g., day 7 and at recurrence if drug remains detectable) and sufficiently long follow-up to capture most recurrences [Data: Sources (97379)]. In TB and MDR-TB regimens, protocols may mix structured profiles (e.g., several samples on day 1 and again at week 8), **trough sampling** at later visits, and **opportunistic samples** at more distant time points to capture longer-term exposure [Data: Sources (191605)].

For difficult-to-sample infection sites, studies may use **paired matrices** and staggered timing. For CNS infections (e.g., TB meningitis), PK sampling is often performed **early after treatment initiation (within ~2–5 days)** to capture the critical illness period and limit missingness from early mortality, with additional sampling around **day 10–14**; CSF is often limited to a single sample per participant, with **between-participant variation in CSF sampling times** used to reconstruct the CSF profile via population PK modelling [Data: Sources (230237, 230408)]. Where possible, **CSF and blood may be sampled simultaneously** to support penetration ratio estimates and site-of-action interpretation [Data: Sources (230257)].

To reduce logistical and ethical burdens, infectious disease studies also use **alternative or minimally invasive matrices** and techniques. Examples include **capillary blood dried on filter paper/dried blood spots** (field-feasible but requiring careful SOPs to manage volume accuracy and contamination, and potentially higher variability), as well as interest in **saliva and hair** for longer-term monitoring and improved feasibility in TB/HIV populations [Data: Sources (68496, 128459, 267361, 45502)]. For measuring **unbound concentrations at the site of infection**, **microdialysis** is highlighted as a minimally invasive approach that can provide real-time unbound drug levels in tissues (useful when plasma is a poor surrogate), though it requires specialised expertise and infrastructure [Data: Sources (35378, 60297)]. In pulmonary infections, lung exposure has been characterised using **BAL, sputum, microdialysis, and lung tissue homogenates**, each reflecting different compartments (extracellular vs site-specific vs total lung) and therefore selected based on the scientific question [Data: Sources (32390, 32439)].

---

## G37. [GLOBAL] What datasets, accession identifiers, and simulation settings support reproducible statistical workflows?

*ID: 46e4a516-a0a... | Latency: 30.1s*

**Answer:**

Reproducible statistical workflows in the provided sources are supported by a mix of **publicly deposited datasets (with accession identifiers)**, **archived code/data snapshots (with DOIs)**, and (for simulation studies) **explicitly reported simulation and inference settings**.

## Public datasets and accession identifiers (examples)
Several sources explicitly deposit high-throughput datasets in community archives, enabling independent re-analysis:

- **NCBI GEO (Gene Expression Omnibus)** accessions, including:
  - RNA-seq: **GSE105159** [Data: Sources (44145)]
  - scRNA-seq: **GSE157244** [Data: Sources (279486)]
  - microarray and single-cell RNA-seq: **GSE90588** and **GSE121568** [Data: Sources (42434)]
  - RNA-seq: **GSE86654** [Data: Sources (162192)]
  - GEO deposition for multiple sequencing modalities: **GSE223036** [Data: Sources (297036, 296981)]
  - mouse scRNA-seq: **GSE215118** [Data: Sources (299212)]
  - dataset availability statement: **GSE153191** [Data: Sources (134038)]

- **SRA / BioProject** accession:
  - **PRJNA562324** (raw data uploaded to SRA) [Data: Sources (233974)]

- **EGA (European Genome-Phenome Archive)** study accession:
  - **EGAS00001007143** (RNA-seq data) [Data: Sources (278902)]

- **ArrayExpress** accession:
  - **A-GEOD-11339** (Affymetrix microarray datasets) [Data: Sources (42400)]

- Some studies also enumerate **reused public datasets** with multiple GEO accessions and an ENA project accession (e.g., **PRJEB23605**) to support exact reuse/replication of upstream inputs [Data: Sources (278483)].

## Archived code/data and workflow packaging (DOIs and repositories)
Reproducible workflows are also supported by versioned code+data releases and public repositories:

- **Zenodo DOIs for archived source code and datasets**
  - PyHillFit archived snapshot: **10.5281/zenodo.163113** (with experimental input data in CSV) [Data: Sources (104869)]
  - Another archived “source code and datasets” record: **10.5281/zenodo.237643** [Data: Sources (24960)]

- **GitHub repositories for analysis pipelines**
  - KoalaGenome scripts: `https://github.com/DrRebeccaJ/KoalaGenome` [Data: Sources (102031)]
  - LBC_ARCHER analysis code: `https://github.com/neilrobertson/LBC_ARCHER` [Data: Sources (229802)]
  - Astuti et al. 2023 analysis code: `https://github.com/CBFLivUni/Astuti_et_al_2023` [Data: Sources (299211)]

- **Open Science Framework (OSF)** hosting many datasets and ML models:
  - “thousands of datasets … links to the code … and ~50,000 ML RF models”: `https://osf.io/vbn5u/` [Data: Sources (204300)]

- Some workflows include **step-by-step reproduction guides** and **pinned environments** (e.g., conda environment files specifying exact dependency versions and OS details) to reproduce all results and figures [Data: Sources (213147, 213148)].

## Simulation and statistical inference settings reported for reproducibility
Where simulation is central, multiple sources indicate that reproducibility is improved by reporting *machine-readable protocols* and explicit *algorithm settings*:

- **Machine-readable model & protocol standards**
  - Models in **CellML/SBML**, protocols in **SED-ML** (or Web Lab protocol descriptions) are presented as a route to reproducible simulation execution across tools [Data: Sources (28978, 28979, 109442)].

- **Web Lab (WL2) fitting specifications and explicit MCMC configuration**
  - WL2 fitting specifications include named algorithm controls such as the number of MCMC iterations (**`numIters`**) and burn-in (**`burn`**), plus a CMA-ES-based multi-start procedure (e.g., **5 random restarts** of CMA-ES) to select an MCMC starting point [Data: Sources (29024)].
  - WL2 also records how experimental and simulated data are aligned by mapping named inputs/outputs (e.g., matching experimental time vector **`t`** to protocol input **`exp_times`**, and comparing simulated output **`IKr`** to data field **`exp_IKr`**) to avoid ad hoc protocol edits when data naming differs [Data: Sources (29025, 109490)].

- **Explicit convergence and replication settings for stochastic simulations**
  - A convergence study is used to choose the number of realizations; one model reports deciding that **50 simulations/realizations** are required for average outputs to converge, and treats a “simulation” as a set of those realizations thereafter [Data: Sources (188581, 188582)].

- **Reported MCMC settings in statistical workflows**
  - Example MCMC reporting includes: software (**JAGS** via **R2jags**), number of chains (**3**), burn-in (**10,000**), thinning (**500**), and post–burn-in iterations (**1,000,000**) producing **2,000 samples per chain** [Data: Sources (179441)].

## Data + protocol linkage and preprocessing provenance (for end-to-end workflows)
Beyond depositing “final” datasets, reproducible workflows are supported by storing:

- **raw + preprocessed data + preprocessing code**, so preprocessing can be inspected and re-run, and raw data remains available for alternative processing choices [Data: Sources (28995, 109460)].
- **links between datasets and the exact experimental/simulation protocol** (e.g., solution composition, temperature, voltage-step protocol; post-processing definitions) to ensure the analysis matches the conditions under which data were generated [Data: Sources (109460, 28995)].

---

## G38. [GLOBAL] Which instruments and platforms are referenced for mass spectrometry and microplate measurements?

*ID: 61149a68-46f... | Latency: 30.1s*

**Answer:**

## Mass spectrometry: instruments/platforms referenced

- **Thermo Scientific Q Exactive (Orbitrap) / Orbitrap (QE)** is referenced as a mass spectrometer with an Orbitrap mass analyser (schematics and table of mass analyser types) [Data: Sources (11971, 11970, 11991)].  
- **FT-ICR / FTICR mass spectrometry (Fourier transform ion cyclotron resonance)** is referenced as a high-resolution mass spectrometry option for MSI (including schematics and discussion of FTICR mass analysers) [Data: Sources (11971, 11991, 12004, 49826)].  
- **Time-of-Flight (ToF) mass analysers** are referenced (including axial/reflectron/orthogonal reflectron ToF schematics) [Data: Sources (11970, 11991, 11993)].  
- **Triple quadrupole (QqQ) mass spectrometers** and **quadrupole mass analysers** are referenced, including use in selected reaction monitoring (SRM) and as part of MSI-capable setups [Data: Sources (11984, 11991, 12000, 12218)].  
- **Ion trap mass analysers** (including linear/3D quadrupole ion traps and their relation to Orbitrap/FTICR) are referenced [Data: Sources (11984, 12001)].  
- **Waters MALDI HDMS Synapt G2** is referenced for MALDI-MSI/MALDI-MSP imaging work (Nd:YAG laser, imaging parameters) [Data: Sources (66669, 66830, 66865)].  
- **Bruker Autoflex III** and **Bruker Autoflex Speed** MALDI instruments are referenced for MALDI profiling/imaging (Smartbeam™ lasers) [Data: Sources (66801, 66599, 66801)].  
- **Bruker microTOF / MicroTOF II** (ESI-TOF HRMS) is referenced for high-resolution electrospray MS measurements [Data: Sources (65077, 88066, 222712)].  
- **Thermo LTQ Orbitrap XL / Orbitrap XL LCMS** is referenced (ESI infusion / LCMS) [Data: Sources (77762, 202192)].  
- **Thermo Exactive MS** (coupled to an Accela LC system) is referenced for LC-MS full scan acquisition [Data: Sources (22894)].  
- **Orbitrap Fusion Tribrid / Orbitrap Fusion Lumos Tribrid** is referenced in the context of proteomics MS acquisition [Data: Sources (79219, 12397)].  
- **Waters Xevo G2-XS QTof** is referenced for LC-MS/MS measurements [Data: Sources (66745, 66830)].  
- **Waters Acquity UPLC + Waters Xevo Q-TOF** is referenced as a narrow-window LC/MS platform [Data: Sources (124536)].  
- **Applied Biosystems/MDS Sciex Q-Star Pulsar-i (Q-TOF) with an orthogonal MALDI source** is referenced (hybrid quadrupole time-of-flight with MALDI) [Data: Sources (314208)].  
- **OrbiSIMS** is referenced as a SIMS platform combining ToF-SIMS with an Orbitrap analyser (“OrbiTrap™M”, high resolving power) [Data: Sources (221607, 249977)].  

Ionisation/MSI “platforms” (interfaces) explicitly referenced include **MALDI**, **DESI**, **LESA**, **SIMS**, **LAESI**, and **LDI** as MSI-relevant approaches [Data: Sources (11984, 12107, 12216, 30834)].

## Microplate measurements: instruments/platforms referenced

- **SpectraMax Multi-mode Microplate Reader (Molecular Devices), model “M3”** is referenced for microplate-based measurements [Data: Sources (107680, 265899)].  
- **Perkin Elmer plate reader** is referenced for absorbance measurements in cell viability assays [Data: Sources (271460)].

---

## G39. [GLOBAL] How do vincristine and RO5461111 treatments affect blood–brain barrier permeability in mice?

*ID: 60171270-e4e... | Latency: 20.1s*

**Answer:**

Vincristine (VCR) treatment increases CNS barrier permeability in mice. In vitro, VCR activates murine CNS endothelial cells (bEND.3), increasing adhesion molecule expression (ICAM-1/VCAM-1), decreasing trans-endothelial electrical resistance, and increasing paracellular permeability—consistent with weakened barrier properties [Data: Sources (55401, 55402)]. In vivo, after a 5-day VCR cycle (0.5 mg/kg/day, i.p.), Evans Blue (EB) extravasation is significantly increased in both brain and spinal cord tissue versus controls (with spinal cord EB reported as ~4× higher), indicating increased permeability of the BBB/BSCB during treatment [Data: Sources (55376, 55409, 55413, 55428, +more)]. VCR dosing is also associated with increased monocyte adhesion/trafficking at the spinal cord endothelium, which is consistent with barrier dysfunction enabling leukocyte entry [Data: Sources (55408, 55362, 55428)].

RO5461111, a peripherally restricted cathepsin S inhibitor, does not appear to reduce VCR-associated CNS barrier permeability in the provided mouse data. When administered orally (200 µmol/kg twice daily during the 5-day VCR cycle), RO5461111 showed peripheral target engagement (e.g., spleen P10 accumulation) but no evidence is provided that it restored BBB/BSCB integrity or reduced EB leakage; rather, its effect in the study is discussed in terms of lacking efficacy on VCR-induced mechanical hypersensitivity when peripherally restricted [Data: Sources (55377, 55411, 55422)].

---

## G40. [GLOBAL] How are LC-MS and TOF MS results combined to confirm compound identity?

*ID: 133b1de7-5d8... | Latency: 20.1s*

**Answer:**

LC–MS and TOF MS are typically combined by using **LC retention time** (chromatographic behaviour) plus **high-accuracy TOF mass measurements** (exact mass, isotope pattern and often MS/MS fragments) as orthogonal evidence that the detected signal is the intended compound, rather than an isobaric interferent.

From the **LC–MS side**, the compound is first separated from matrix components and (where relevant) from isomers; this is important because compounds can share the same nominal or even exact mass, and LC can resolve them into different peaks for individual identification [Data: Sources (102589, 129652)]. Identity assignment is then strengthened by matching multiple measured characteristics to an authentic standard: **accurate mass (e.g., <5 ppm), retention time (e.g., ±15 s), fragmentation pattern, and isotope pattern matching (e.g., >90%)** [Data: Sources (102302)].

From the **TOF MS side**, identity is confirmed using **accurate mass full-scan data** (often <5 ppm) together with **isotope spacing/abundance matching** and, where needed, **product-ion (MS/MS) spectra** to check that fragments are consistent with the proposed structure [Data: Sources (5833, 102302)]. In practice, workflows may first acquire full-scan TOF spectra, then select key precursor ions for QTOF MS/MS to verify diagnostic fragments and refine elemental formulae based on accurate-mass fragments [Data: Sources (5833)].

When both datasets are available, confirmation is achieved by requiring that the **same LC peak** corresponds to a **TOF feature with the expected exact m/z (within ppm tolerance), correct isotope pattern, and appropriate MS/MS fragmentation**—and, ideally, that this combined evidence matches what is observed for an authentic reference standard run under the same LC–MS conditions [Data: Sources (102302, 5833)].

---

## G41. [GLOBAL] Which NMR solvents and nuclei are used for structural characterization across the dataset?

*ID: 6b55a920-17a... | Latency: 20.1s*

**Answer:**

Across the dataset, **solution-state NMR structural characterization** is primarily performed using deuterated organic solvents—most often **CDCl₃**, **DMSO‑d₆**, and **CD₃OD / MeOD (methanol‑d₄)** [Data: Sources (44271, 75644, 274061, 294591, 124458)]. Additional solution solvents used include **D₂O** (especially where aqueous conditions are needed) [Data: Sources (124125, 291366, 267617, 318397)], **CD₃CN (acetonitrile‑d₃)** [Data: Sources (202191, 135348)], **CD₂Cl₂ (dichloromethane‑d₂)** [Data: Sources (14538, 279550, 279550)], and (in some protocols) non-deuterated residual-solvent referencing also mentions **DMF** and **MeOH** as reference solvents [Data: Sources (200554)]. Protein/biophysical NMR samples commonly use **aqueous buffer supplemented with D₂O (e.g., 5–10%)**, and sometimes an internal reference such as **DSS** [Data: Sources (111267, 125293, 149957)].

The **most frequently observed nuclei** for small-molecule characterization are **¹H and ¹³C**, with routine inclusion of **¹⁹F** where fluorinated compounds are present [Data: Sources (44271, 167460, 170518, 34829, 116594)]. The dataset also includes **³¹P NMR** for phosphorus-containing compounds [Data: Sources (201834, 119694, 235744, 170517, 279550)]. In biomolecular NMR, the key heteronuclear experiment reported is **¹H–¹⁵N HSQC/HMQC** (so **¹H and ¹⁵N** are used), and resonance assignment/binding studies also employ **¹³C/¹⁵N-labelled proteins** enabling **¹H–¹³C** and **¹H–¹⁵N** correlation spectra [Data: Sources (5960, 91025, 125293, 326540, 326694)]. 

The dataset also contains **solid-state NMR** applications, notably **solid-state ¹³C MAS/CPMAS** [Data: Sources (56412)], and general discussion of multinuclear solid-state NMR capability for spin-active nuclei such as **²⁹Si, ²³Na, ⁶/⁷Li, and ¹¹B** [Data: Sources (16243, +more)].

---

## G42. [GLOBAL] How do experimental and computational studies link physiological interventions to measurable tissue and cellular responses?

*ID: 50cc17fc-4a5... | Latency: 40.2s*

**Answer:**

Experimental and computational studies connect physiological interventions to measurable tissue/cellular responses by creating **chains of evidence across scales**—from a controlled perturbation (drug, temperature, mechanical load, electrical pacing, perfusion flow) to quantifiable cellular phenotypes and, where possible, to tissue/organ biomarkers and clinical readouts.

In **cardiac electrophysiology and safety pharmacology**, experiments provide measurable cell- and tissue-level endpoints (e.g., action potential morphology, Ca²⁺ handling, contraction force), while simulations integrate these mechanisms to predict organ-level risk. Multiscale efforts explicitly aim to link single-cell simulation outputs (e.g., APD90, early afterdepolarization propensity, upstroke velocity) to clinically used biomarkers such as QT/QTc, T-wave morphology, and beat-to-beat variability, helping translate cellular drug effects to clinical observations [Data: Sources (90008, 209798, 90007, 228810, 126874, +more)]. This linkage typically requires *calibration and validation*: models are calibrated to reproduce experimental observations and then tested against independent validation datasets; their usefulness depends strongly on calibration quality and the experimental protocol used [Data: Sources (123765, 210085, 123763, 28998, 29006)]. Studies also emphasize that experimental conditions (e.g., electrotonic coupling, compensatory currents, protocol details) can bias inferred parameters, so accounting for these conditions is part of turning an intervention into a reliable mechanistic inference [Data: Sources (123855, 78138, 123929)]. On the experimental side, refined in vitro intervention protocols in hiPSC-cardiomyocytes and engineered heart tissues (EHTs)—including controlling spontaneous beat rate and extending exposure from acute (≤30 min) to chronic (≥24 h)—improved accuracy for detecting clinically relevant inotropic effects, demonstrating how changing the *physiological context of the intervention* changes measurable functional outputs (force-frequency relationships, contractility, Ca²⁺ handling) [Data: Sources (81781, 81939, 81944)]. In parallel, **model-driven optimal experimental design** uses computational objectives to propose patch-clamp protocols that better identify model parameters (e.g., maximum conductances), improving predictive power while reducing experiment duration—an explicit computational-to-experimental loop linking “what to perturb” with “what response will be most informative” [Data: Sources (274437, 274442, 274436)].

Across other physiological domains, studies similarly combine controlled perturbations with quantitative readouts. For **adipose tissue thermophysiology**, low temperature (cold exposure) is treated as an intervention; cell culture and stem-cell models show a *cell-autonomous* response even without neural input, enabling measurement of adipogenic differentiation and “browning” features in vitro. A translational loop is illustrated where caffeine induced browning features in stem-cell cultures and was then linked to activation of brown adipose tissue metabolism in healthy volunteers after coffee consumption [Data: Sources (86073, 86115)]. In **neurovascular physiology**, pharmacological agents are used to “calibrate” neuroimaging variables: caffeine (vasoconstrictive) and CO₂ (vasodilatory) modulate vascular components of the BOLD/CBF signals to study neurovascular coupling and improve models relating imaging biomarkers to underlying physiology, while acknowledging confounds from systemic cardio-pulmonary effects [Data: Sources (101123, 101124, 101135, 101131)]. In **tissue engineering and mechanobiology**, interventions often take the form of mechanical loading, scaffold microarchitecture, or perfusion flow; responses are quantified as changes in proliferation, morphology, differentiation, and tissue formation. Computational models (e.g., finite element / fluid-structure interaction, CFD) are used to estimate local mechanical stimuli experienced by cells and to predict where and how tissue will differentiate (e.g., fracture healing, scaffold conditioning), while experiments provide the tissue-level outcomes for validation and refinement [Data: Sources (180129, 180139, 233210, 233059)]. High-throughput material screening plus machine learning can map how combinations of material chemistry and microtopography instruct phenotypes (including osteoinduction and immunomodulation), creating measurable structure–activity relationships between designed physical interventions and cell fate outputs [Data: Sources (138348, 139013)].

A recurring theme is that **translation and uncertainty** must be addressed explicitly. Cardiac whole-heart simulations show that predicted arrhythmia inducibility can depend strongly on uncertain tissue-scale assumptions (e.g., spatial distribution of “M cells”, cell-to-cell coupling), so sensitivity analysis and uncertainty quantification are needed before interpreting an intervention→response link as robust [Data: Sources (89640, 114573)]. Likewise, models may be poorly constrained when data are scarce or protocols differ, limiting quantitative prediction even if qualitative mechanistic insight is still useful [Data: Sources (210085, 221284)]. To reduce these gaps, many reports describe iterative “model–simulation–experiment” workflows and standardized/reproducible infrastructures for comparing protocols and models against shared datasets, so that intervention effects can be traced consistently from experimental measurement to computational prediction and back again [Data: Sources (128336, 28970, 109453, 123944)].

---

## G43. [GLOBAL] How are bioanalytical quantification limits linked to dosing studies and sample matrices?

*ID: 5c4ec425-f98... | Latency: 30.1s*

**Answer:**

Bioanalytical quantification limits (especially the lower limit of quantification, LLOQ/LOQ) are linked to dosing studies because they determine **which post‑dose concentrations can be measured reliably** in the chosen biological matrix, and therefore what parts of the exposure–time profile (e.g., troughs, terminal elimination phase, predose carryover) can be characterized for PK/PD and dose selection. Bioanalytical methods typically define LLOQ as the lowest spiked concentration in the relevant matrix that meets predefined accuracy and precision criteria (often ±20% at LLOQ vs ±15% at higher QC levels) [Data: Sources (24231, 24232, 24243)]. If expected concentrations after a given dose fall near/below the LLOQ, then the study may not be able to support its objectives (e.g., estimating AUC to late timepoints, comparing regimens, or confirming target exposure).

**Matrix choice directly affects quantification limits and interpretability.** LLOQ may differ substantially between matrices (e.g., plasma vs urine), reflecting different extraction recovery, ion suppression, and achievable assay sensitivity; one example reports LLOQ 10 pg/mL in urine vs 50 pg/mL in plasma for the same analyte with separate validated methods [Data: Sources (32461, 32462)]. Across studies, using different matrices can complicate comparisons because “there are not always straightforward concentration relationships between different matrices,” which can undermine pooling/meta-analysis unless methods and calibration approaches are standardized [Data: Sources (68480, 68482, 68484)]. Even within broadly similar matrices, differences such as capillary dried blood spots vs venous plasma can introduce decreased sensitivity and increased variability, and the relationship between capillary whole-blood and venous plasma can be unclear [Data: Sources (98060)].

**Dosing study design and sample volume constraints feed back into LLOQ feasibility.** Achieving a low LLOQ may require larger sample volumes; published high-sensitivity methods (e.g., ng/mL LLOQs) have required hundreds of microliters to ~1 mL of plasma, which can be problematic for pediatric TDM and for PK studies in small animals where blood volume is limited [Data: Sources (82074, 24221)]. This creates a trade-off: dose level and sampling schedule may need to be adapted to what can be quantified from feasible sample volumes, or more sensitive instrumentation/sample prep may be required.

**Calibration/QC are matrix-matched and bracket dosing-related concentrations.** Dosing studies rely on calibration curves prepared by spiking analyte into *blank matrix* and including QC samples at multiple levels; acceptance criteria (e.g., proportions of standards/QCs within set % of nominal) define which concentration range is reportable for study samples [Data: Sources (189848, 143994)]. Because dosing vehicles and dilutions can affect quantification, some workflows explicitly assay study samples pre/post dilution to check for vehicle effects and validate dilution integrity when concentrations exceed the assay range [Data: Sources (189848)].

**How BLQ (below LLOQ/LOQ) values are handled in PK analyses links quantification limits to dosing conclusions.** Sparse sampling, low doses, or late timepoints often generate BLQ observations; different modeling strategies (ignore, impute LLOQ/2, likelihood/censoring methods) can change parameter estimation and interpretation [Data: Sources (105483, 325121, 109874)]. Some population PK analyses even include BLQ and above-range concentrations with additional error/covariate structures to preserve information when many such values exist [Data: Sources (70186)].

Finally, when the “matrix” is **tissue** rather than biofluid, quantification limits and matrix effects become even more central: heterogeneous tissue environments can cause variable ion suppression and extraction recovery, so quantitative tissue methods often require tissue-specific calibration approaches and/or isotopically labeled standards, and comparisons across tissues may only be valid where ion suppression is similar [Data: Sources (12106, 219347, 219358)]. This is why plasma concentrations—while convenient—may be a poor proxy for site-of-action exposure in some contexts, motivating additional assays (e.g., tissue, CSF, BAL) whose achievable quantification limits must match expected concentrations under the dosing regimen [Data: Sources (11977, 230259, 32391)].

---

## G44. [GLOBAL] What clinical endpoints and patient-reported outcomes are used to assess therapy effectiveness?

*ID: f165a181-ac9... | Latency: 40.1s*

**Answer:**

Clinical effectiveness is assessed using a mix of **clinical endpoints** (e.g., survival, progression/relapse, response, biomarkers, imaging, service use) and **patient-reported outcomes (PROs)** (e.g., symptoms, functioning, health-related quality of life). The specific endpoints used vary by disease area and trial purpose.  

## Common clinical endpoints used to assess effectiveness

**Survival and time-to-event endpoints**
- **Progression-free survival (PFS)** and **overall survival (OS)** are widely used as main endpoints in oncology trials and other clinical studies [Data: Sources (112210, 14074, 279751, 179471, 302609, +more)].  
- Related time-to-event endpoints include **event-free survival (EFS)**, **disease-free survival (DFS)**, **time to progression (TTP)**, **duration of response**, and relapse-related endpoints (e.g., time to relapse) [Data: Sources (254387, 204996, 79046, 63199, 246231, +more)].

**Response/Remission endpoints (clinical or composite)**
- **Overall response rate (ORR)** and proportions achieving **complete response (CR)**/**partial response (PR)** are common, often defined via disease-specific response criteria (e.g., IWCLL criteria for CLL; IPCG criteria for primary CNS lymphoma; RECIST for solid tumours) [Data: Sources (14074, 254387, 262552, 203523, 82975, +more)].
- Some trials use **molecular endpoints**, such as **measurable/minimal residual disease (MRD)** (e.g., undetectable MRD at a specific time point, MRD response over time, molecular relapse) [Data: Sources (262552, 274893, 227427, 246190, 243488, +more)].

**Imaging-based endpoints**
- Imaging can define response or progression, such as **PET-CT metabolic response** (e.g., complete metabolic response using Deauville scale/Lugano criteria) and CT/MRI-based criteria (e.g., modified RECIST for mesothelioma; gadolinium-enhanced MRI response for PCNSL) [Data: Sources (302560, 302609, 79046, 252848, 254387, +more)].

**Symptoms/functional status assessed clinically**
- Some areas (e.g., TB meningitis) use endpoints such as **resolution of coma**, **new neurological or radiological events**, **mortality at defined timepoints**, and **functional status/disability composites**, including **Glasgow Coma Scale (GCS) improvement** and later **cognitive impairment** [Data: Sources (230298, 230297, 230299, 215127)].  
- Performance/functional measures such as **ECOG performance status** may be tracked as outcomes [Data: Sources (128236, 63191, 205280)].

**Safety/tolerability and real-world effectiveness proxies**
- Trials frequently include **adverse events (AEs)** graded by **CTCAE**, and discontinuation outcomes (e.g., **all-cause treatment discontinuation**) may be used as pragmatic measures capturing both efficacy and tolerability [Data: Sources (114779, 192461, 252848, 38521)].  
- **Healthcare utilization** (e.g., hospital admissions, length of stay, antibiotics use) is sometimes included as an endpoint or secondary outcome [Data: Sources (192457, 155440, 246231, 41176)].
- In psychiatry, response is often operationalised as **pre–post change on symptom rating scales**, sometimes combined with **functioning** or service-use outcomes (e.g., hospital admission), but standardisation is a known challenge [Data: Sources (192457, 192458, 192459)].

## Patient-reported outcomes (PROs) used to assess effectiveness

**Health-related quality of life (HRQoL) / QoL instruments**
- **EORTC QLQ-C30** is repeatedly used across oncology settings, sometimes alongside disease modules (e.g., **EORTC QLQ-CLL16**, **EORTC QLQ-CML24**, **EORTC LC13** for lung-cancer symptoms, **EORTC BN20** for brain tumours) [Data: Sources (262552, 78981, 252848, 282232, 78994, +more)].
- Generic health utility measures used for QoL and cost-utility include **EQ-5D** variants (e.g., EQ-5D-3L, EQ-5D-5L) [Data: Sources (78981, 246190, 310801, 310840, 310845, +more)].
- Other commonly used QoL/HRQoL tools include **FACT-G** (Functional Assessment of Cancer Therapy—General) and disease-targeted FACT measures such as **FACT-Lym** [Data: Sources (189274, 302560)].

**Symptom burden and symptom-specific PROs**
- Patient-reported symptom burden during chemotherapy may be assessed using tools such as the **Memorial Symptom Assessment Scale (MSAS)** in remote symptom monitoring interventions [Data: Sources (189274)].  
- Disease-related symptom PROs include **FACIT-Fatigue (FACIT-F)** and symptom improvement/impact captured through EORTC domains (e.g., fatigue subscales) [Data: Sources (14074, 41175, 41182)].  
- Pain can be tracked via daily diaries or validated pain tools (e.g., **BPI-SF**; daily pain severity diaries) [Data: Sources (65660, 62355)].

**Functioning and participation**
- HRQoL instruments frequently capture **physical, psychosocial, and social functioning** (e.g., PedsQL physical/psychosocial scores; EORTC functioning scales) [Data: Sources (93938, 327712, 114779, 128241)].
- In Duchenne muscular dystrophy, effectiveness monitoring includes functional capacity endpoints such as **6-minute walk test (6MWT)** and timed function tests, with interest in augmenting these with technology-based monitoring of real-world activity [Data: Sources (160693)].

**Mental health and other patient-centered constructs**
- Trials may include PROs for **anxiety**, **self-efficacy**, and **supportive care needs** (e.g., **STAI-R**, **CASE-Cancer**, **SCNS-SF34**) [Data: Sources (189274)].  
- Disease-specific PROs can include measures like **CushingQoL** and **Beck Depression Inventory (BDI)** in Cushing’s disease trials [Data: Sources (83884)].
- Some fields require PROs that demonstrate improvement in everyday functioning/quality of life (e.g., tinnitus trials using the **Tinnitus Functional Index (TFI)** global score and responder thresholds) [Data: Sources (38508, 38584)].

## Notes on measurement strategy
- Multiple sources emphasise that effectiveness measurement often benefits from **longitudinal, multifaceted assessment** rather than relying on a single symptom scale, especially where biomarkers are limited (e.g., psychiatry) [Data: Sources (192458, 192459)].  
- PRO collection may be scheduled repeatedly during therapy and follow-up (examples include baseline and multiple post-baseline timepoints for PedsQL in paediatric oncology; HRQoL repeated across chemotherapy cycles and follow-up in oncology trials) [Data: Sources (93938, 78991)].

---

## G45. [GLOBAL] Which infectious diseases and standard treatments are discussed across the dataset?

*ID: 1fd95657-2f9... | Latency: 40.2s*

**Answer:**

Across the dataset, the following infectious diseases are explicitly discussed, along with the standard (or commonly used) treatments that are named.

## Tuberculosis (TB), including drug-resistant TB and tuberculous meningitis (TBM)
- **TB (including MDR/XDR/RR-TB)** is discussed, including TB–HIV coinfection and drug resistance [Data: Sources (52199, 189092, 189142, 234289, 234343, +more)].  
- **Standard TB drugs/regimens referenced** include **rifampicin** as an essential component of drug-sensitive TB treatment [Data: Sources (234343, 36832, 127, 230411, 15830)] and multiple second-line/DR-TB agents such as **linezolid, clofazimine, pyrazinamide, carbapenems, and moxifloxacin** [Data: Sources (234301, 234288, 234289, 66222, 291894)].  
- For **TBM**, the dataset discusses intensified antimicrobial therapy and specifically mentions trials evaluating **higher-dose rifampicin and linezolid** [Data: Sources (230411, 230401, 15830, 230222, 36832)].

## HIV/AIDS (including interactions with TB and malaria therapies)
- **HIV-1 infection** and its long-term management are discussed; **combination antiretroviral therapy (cART)** is named as a major standard treatment approach [Data: Sources (142741, 312166, 189083, 234343, 189142)].  
- The dataset also highlights clinical complexity from **drug–drug interactions between antiretrovirals and anti-TB/antimalarial drugs** in endemic settings [Data: Sources (36832, 234343, 6314, 127, 189142)].

## Malaria
- **Malaria** is discussed extensively, including resistance and treatment policy [Data: Sources (189083, 72668, 68504, 328828, 97361)].  
- **Standard antimalarial treatments referenced** include **artemisinin-based combination therapies (ACTs)**, specifically **artemether–lumefantrine (AL)** and **dihydroartemisinin–piperaquine (DHA-PQP)** [Data: Sources (72668, 105, 72694, 127, 189083)].  
- The **artemether–lumefantrine** product **Riamet** is explicitly mentioned as prescribed treatment in a controlled human infection context [Data: Sources (139791)].

## Bacterial sepsis / neonatal sepsis and empiric antibacterial therapy
- **Neonatal sepsis** and antimicrobial resistance to commonly recommended regimens are discussed [Data: Sources (211560, 201242, 211797, 288040, 288078)].  
- **Standard/empiric antibiotics named** include **ampicillin, gentamicin, and ceftriaxone**, with reported non-susceptibility concerns in some settings [Data: Sources (211560, 36832, 288040, 201242, 288078)].

## Injection-related bacterial infections (and one fungal example)
- Qualitative studies cover injecting-related **skin and soft-tissue infections, endocarditis, bacteraemia, and osteomyelitis**; one study includes **candidal ophthalmitis** [Data: Sources (269548, 269540)].  
- While these sections focus more on risk pathways than named regimens, they explicitly situate these as infections for which people may or may not access treatment [Data: Sources (269540, 269542)].

## Specific bacterial pathogens and “typical” drug classes used
A table in the dataset links several bacterial pathogens to commonly used therapies (presented as typical choices rather than individualized guidance):  
- **Staphylococcus aureus** → **vancomycin** (for methicillin-resistant strains) [Data: Sources (223117)].  
- **Helicobacter pylori** → **clarithromycin** [Data: Sources (223117)].  
- **Campylobacter, Salmonella spp., Shigella spp.** → **fluoroquinolones** [Data: Sources (223117)].  
- **Neisseria gonorrhoeae** → **3rd-generation cephalosporin** (also fluoroquinolone listed) [Data: Sources (223117)].  
- **Streptococcus pneumoniae** → **penicillin**; **Haemophilus influenzae** → **ampicillin** [Data: Sources (223117)].

## Clostridioides (Clostridium) difficile infection
- **C. difficile-associated disease/colitis** is discussed with **metronidazole** explicitly named as a treatment used in referenced work [Data: Sources (46051, 155449, 155439)].

## Invasive fungal infections, including cryptococcal meningitis and candidiasis
- **Cryptococcal meningitis** (noted in the context of HIV-associated mycoses) is discussed; **interferon-gamma** is mentioned as a potential adjunctive immune therapy, and timing of ART is highlighted as affecting outcomes [Data: Sources (769, 772)].  
- **Invasive candidiasis** is discussed in the context of immune therapies and vaccination strategies (e.g., Candida vaccine trials) [Data: Sources (769, 772)].  
- **Candidemia** appears in pharmacodynamic context with **fluconazole** exposure–response discussed [Data: Sources (11933)].

## Cutaneous/visceral leishmaniasis
- **Cutaneous leishmaniasis (CL)** is discussed with a “current treatment” section listing standard systemic options including **pentavalent antimonials, miltefosine, and amphotericin B** [Data: Sources (35272, 332138, 189083, 130674, 35893)].  
- **Visceral leishmaniasis (VL)** is also discussed (including limitations of pentavalent antimony and the need for better options) [Data: Sources (332138, 153017, 189083)].

## Chagas disease (Trypanosoma cruzi infection)
- **Chagas disease** is discussed, explicitly naming the two available treatments: **benznidazole** and **nifurtimox** (noting long treatment courses and toxicity) [Data: Sources (242343, 332138, 153017)].

## Pneumocystis jirovecii pneumonia (PJP)
- **PJP** appears as an opportunistic infection, and **PJP prophylaxis** is explicitly mentioned in the context of infection risk mitigation guidance [Data: Sources (286858, 113968, 215280)].

## Cryptosporidiosis
- **Cryptosporidiosis** is discussed, with **nitazoxanide** explicitly identified as the only FDA-approved drug [Data: Sources (189106, 112566)].

## Viral respiratory infections and COVID-19
- **SARS-CoV-2/COVID-19** is discussed, including clinical management elements; the dataset lists commonly used (non-specific) antivirals such as **remdesivir** and **lopinavir/ritonavir**, plus immunomodulators such as **tocilizumab** and **sarilumab**, alongside steroids and supportive care [Data: Sources (155734, 228957, 218642, 102, 210325)].  
- **Influenza** is referenced in immunocompromised populations and revaccination contexts, rather than as a detailed treatment pathway [Data: Sources (257789, 113952, 48949)].

## Ebola virus disease and dengue
- **Ebola virus disease** is referenced (largely as background/citation) without specific standard therapeutic regimens detailed in the provided chunks [Data: Sources (48949, 48950)].  
- **Dengue** therapeutics are discussed; trials of **chloroquine** and **prednisolone** are mentioned as investigated but without clear benefit in those cited trials [Data: Sources (152231, 152244)].

---

## G46. [GLOBAL] How are DOIs presented and formatted across journal articles in the dataset?

*ID: afc13629-c78... | Latency: 20.1s*

**Answer:**

DOIs in the dataset are presented in several distinct *surface formats* (URL-form, “doi:” label form, and occasionally mixed/legacy link forms), and they appear in different *article locations* (e.g., as the article’s identifier, in supplementary-information notices, in data-availability statements, and in reference lists).

A common pattern is the **canonical DOI URL** form, `https://doi.org/<doi>`, used both for the main article and for associated content like supplementary material. Examples include explicit “Supplementary information accompanies this paper at …” lines pointing to `https://doi.org/10.1038/...` [Data: Sources (7650, 169537, 194605, 65215, 2221, +more)], as well as repository records that place the DOI on its own line under a “DOI” heading (e.g., `https://doi.org/10.15252/embj.201489072`) [Data: Sources (76092)]. The same URL form is also used for dataset identifiers in data availability statements (e.g., “uploaded … on the following DOI: https://doi.org/10.5518/398”) [Data: Sources (13603)].

Another frequent style is the **prefixed label form** `doi:<doi>` (sometimes without a space after the colon). This appears in some “Additional information”/supplementary notices (e.g., `Supplementary Information ... at doi:10.1038/...`) [Data: Sources (104659, 227830, 329926, 334668)]. It also appears in citation-like contexts where the DOI is embedded in a bibliographic string (e.g., `Sci. Rep. 7, 41160; doi: 10.1038/srep41160 (2017)`) [Data: Sources (24438)], and in reference lists where the field is explicitly written as `doi: 10....` alongside a separate “URL https://doi.org/...” [Data: Sources (205451, 205452)].

The dataset also contains **legacy/alternative resolver URLs**, especially `http://dx.doi.org/<doi>`, commonly used in “Supplementary data … can be found online at …” appendices and in repository “To link to this article DOI:” lines [Data: Sources (8759, 241937, 266085)]. In Elsevier-style appendices, DOI links may be rendered with inserted spacing or line breaks (e.g., `https://doi. org/10.1016/...`) [Data: Sources (286112, 298662, 221949)].

Finally, DOIs can appear with **formatting irregularities introduced by extraction or templating**, such as spaces after `https://doi.org/` (e.g., `https://doi.org/ 10.1016/...`) [Data: Sources (13306, 65215)], or accidental duplication (`https://doi.org/https://doi.org/...`) in a link to a figshare DOI [Data: Sources (309787)]. Some publisher templates also instruct citation via DOI in all-caps text (e.g., “PLEASE CITE THIS ARTICLE AS DOI: 10.1063/5.0012309”) [Data: Sources (81557)].

---

## G47. [GLOBAL] How do the dataset’s chemistry studies connect synthesis conditions, characterization data, and structural models?

*ID: f96536a2-3a0... | Latency: 30.1s*

**Answer:**

The dataset’s chemistry studies connect **synthesis conditions → characterization data → structural models** by treating each stage as mutually constraining evidence, then using curated identifiers to make the links explicit.

In the **solid‑state solubility/enthalpy studies**, the synthesis/handling context is captured indirectly via *which solid state is actually dissolving* and (when available) *which polymorph* was present. During curation, entries were filtered out if there was no evidence the measurements reflected dissolution from the solid state (rather than another state) [Data: Sources (13828)]. Molecular structures were integrated by retrieving SMILES from external resolvers/databases, and inconsistent structures were manually resolved using additional references [Data: Sources (13828)]. Those molecular identifiers were then cross‑referenced to crystal structures by mapping each “molecule + polymorph description” to Cambridge Structural Database (CSD) refcodes; because polymorph labels were usually missing, matches were often provisional and were cleaned by deleting conflicts and then selecting a putative lowest‑energy structure (via calculated lattice energy) when multiple candidate crystal structures remained [Data: Sources (13829, 13830)]. This creates an explicit bridge from endpoint measurements to a specific (or best‑guess) crystal structural model, while also documenting limitations: descriptors may be calculated for the “wrong” polymorph, and polymorph solubilities can differ materially even if polymorph energies are often close [Data: Sources (13891)].

In the **high‑throughput medicinal chemistry / structure‑based campaigns**, the connection is made through a cycle: synthesize many compounds (often robotically), characterize reaction outcomes (LCMS; and critically X‑ray), and use the resulting structural models to guide the next round of synthesis. One workflow synthesised thousands of crude reaction mixtures on an OpenTrons platform, generated hundreds of usable protein–ligand X‑ray datasets, and used those crystallographic models to identify binding products and pose changes (including a pose switch caused by a single methyl addition at a chiral center) [Data: Sources (272883)]. Data products explicitly bundle chemistry execution outputs with characterization (X‑ray and LCMS) in a deposited directory, supporting traceability from synthesis conditions to structural interpretation [Data: Sources (272930)]. Downstream modeling then uses experimentally determined protein–ligand crystal structures to featurize complexes (e.g., with interaction/score descriptor sets) and train predictive models; comparisons show models using experimental structural biology data outperform ligand‑only (fingerprint) and docking‑approximation models, reinforcing the role of crystallographic characterization in connecting chemical changes to learned structural rules [Data: Sources (300049, 300042, 300048, 300051, +more)]. Where experimental structures are not available prospectively, docked structures are used as approximations, and predictive performance is shown to degrade as docked poses diverge from crystal poses—making “structure agreement” itself part of the synthesis‑to‑model linkage [Data: Sources (300051)].

Finally, in **crystallographic structure determination and validation**, datasets connect experimental conditions and raw diffraction processing to final structural models using standardized pipelines and deposition. Examples include use of DIALS/XDS/xia2/autoPROC for processing, PanDDA/DIMPLE maps for event detection, Coot for ligand fitting, and refinement with Buster/REFMAC/PHENIX, followed by model validation (e.g., MolProbity) and deposition of models/structure factors to public repositories (PDB/CCDC) [Data: Sources (292804, 289288, 42097, 82861)]. This provides a reproducible chain from experimental crystallization/diffraction conditions through characterization outputs to the structural model objects that feed later analysis and machine learning.

---

## G48. [GLOBAL] Which reagents and conditions are used for hydroxylamine-based transformations across the dataset?

*ID: 8b963020-4eb... | Latency: 30.1s*

**Answer:**

Across the dataset, hydroxylamine-based transformations mainly fall into three recurring patterns: (1) **hydroxylamine generation by hydrazinolysis of phthalimide-protected O‑arylmethyl hydroxylamines**, (2) **formation of oximes or hydroxamic acids using hydroxylamine salts/solutions plus base**, and (3) **use of O‑alkyl hydroxylamines as nucleophiles in acylation/coupling contexts**.

## 1) Hydrazinolysis to unmask O‑substituted hydroxylamines
Multiple entries prepare *O‑substituted hydroxylamines* by cleaving **N‑phthalimido‑O‑(substituted)hydroxylamines** with **hydrazine monohydrate (65% aq)** at **room temperature** in **DCM** (sometimes with **MeOH**), followed by filtration and concentration [Data: Sources (181730, 181979, 181757, +more)].  
Examples include:
- Hydrazine monohydrate (4.0 eq) in **MeOH/DCM** at **rt** for ~**4 h** to give **O‑(4‑nitrobenzyl)hydroxylamine** [Data: Sources (181730)].  
- Hydrazine monohydrate (4.0 eq) in **DCM** at **rt** for ~**3 h** (done “in the dark” for a nitrobenzyl system) to give **O‑(4,5‑dimethoxy‑2‑nitrobenzyl)hydroxylamine** [Data: Sources (181979)].  
- Hydrazine monohydrate (8.0 eq) in **DCM/MeOH** at **rt** for ~**5 h** to give **O‑(6‑nitroquinolin‑5‑yl)hydroxylamine** [Data: Sources (181757)].

## 2) Oxime formation (carbonyl derivatisation) using hydroxylamine
Several procedures form **oximes** from carbonyl compounds using **hydroxylamine hydrochloride** (or **hydroxylamine 50% in water**) typically in **ethanol** and sometimes with **extended heating/reflux**:
- **Hydroxylamine hydrochloride in EtOH** at **rt (~45 min)** to form an oxime intermediate, followed by **HCl addition and Zn** (a reductive step after oxime formation) [Data: Sources (52034)].  
- A sterically hindered ketone required **reflux in ethanol with hydroxylamine hydrochloride for 48 h** to obtain the oxime in good yield [Data: Sources (323560)].  
- Dataset context also notes oxime formation as a common derivatisation reaction of carbonyl compounds “by reaction with hydroxylamines” [Data: Sources (66792)].

## 3) Hydroxamic acid / hydroxamate formation from acids or activated derivatives
Hydroxylamine is frequently used to form **hydroxamic acids (R‑C(O)NHOH)** or **O‑benzyl hydroxamates** via activated carboxylic acid derivatives and base.

### 3A) Via CDI activation then hydroxylamine hydrochloride
A representative sequence uses **carbonyldiimidazole (CDI)** to activate an acid (or related precursor) in **dry THF**, then adds **hydroxylamine hydrochloride** at **rt** with long stirring (~**19 h**) [Data: Sources (181831)].

### 3B) Coupling (EDCI/HOBt or similar) to form O‑benzyl hydroxamates, then hydrogenation
The dataset describes formation of **O‑benzyl hydroxamates** using coupling reagents such as **EDCI·HCl + HOBt** (or **CDI**) with a **tertiary amine base**, and then **Pd/C hydrogenation** to give the corresponding **acetohydroxamic acids** essentially quantitatively [Data: Sources (274005, 274375, +more)].  

A detailed example shows **O‑benzylhydroxylamine hydrochloride** used as the nucleophile under **argon**, with a tertiary amine base (**TEA**) and coupling reagents, stirred **40–45 h at 30–35 °C** [Data: Sources (274263)].

### 3C) Direct use of hydroxylamine hydrochloride + base to make hydroxamate-type products
One scheme specifies **NH2OH·HCl + NaOH** in **H2O/EtOH (1:1)** at **80 °C for 2 h** as a discrete hydroxylamine step [Data: Sources (175676)].

## 4) Use of hydroxylamine hydrochloride with added base (TEA) in ethanol
A repeated operational motif is adding **hydroxylamine hydrochloride** together with **triethylamine (TEA)** in **EtOH** at **room temperature**, often after a preliminary stirring period, to achieve hydroxylamine incorporation (e.g., oxime/hydroxamate-type formation depending on substrate) [Data: Sources (85839)].

## 5) Use of O‑alkyl hydroxylamines as nucleophiles (e.g., O‑(benzyl)hydroxylamine·HCl)
Beyond NH2OH itself, the dataset uses **O‑benzylhydroxylamine hydrochloride** as a nucleophile in longer **rt** reactions (e.g., **18 h**) with aqueous **HCl quench** and extraction workups [Data: Sources (181784)]. This is consistent with broader hydroxamate synthesis contexts described elsewhere in the dataset [Data: Sources (274005, 274263)].

---

## G49. [GLOBAL] Which small-molecule inhibitors and electrophysiology metrics are used to validate hPSC-derived cells?

*ID: cc3c8778-7ea... | Latency: 40.1s*

**Answer:**

## Small-molecule inhibitors (and related modulators) used to validate hPSC-derived cells

### Cardiac differentiation / subtype specification (pathway modulators)
Cardiogenic monolayer differentiation protocols routinely use the **GSK3β inhibitor CHIR99021** early, followed by **WNT inhibitors** such as **IWR1, IWR4, C59, or XAV939** to drive cardiac specification [Data: Sources (23349)]. Other differentiation approaches also mention WNT modulation using **KY02111** and **XAV393** during cardiomyocyte formation [Data: Sources (21011)].

### Ion-channel pharmacology used as functional validation in hPSC-cardiomyocytes
hPSC-CMs are validated by showing expected responses to canonical ion-channel modulators/blockers, including:
- **Tetrodotoxin (TTX)** (Na\(^+\) channel blocker; inhibits \(I_\mathrm{Na}\)) [Data: Sources (22739, 22825, 31009)]  
- **Nifedipine** (L-type Ca\(^{2+}\) channel blocker; inhibits \(I_\mathrm{CaL}\)) [Data: Sources (22739, 31009)]  
- **E-4031** (hERG/\(I_\mathrm{Kr}\) blocker) [Data: Sources (22739, 31009, 48325)]  
- **Terfenadine** (used as a K\(^+\) current blocker in APC workflows; dose-dependent inhibition of \(I_K\) reported) [Data: Sources (22825)]  
- **Dofetilide** (hERG/\(I_\mathrm{Kr}\) inhibitor) and **quinidine** (multi-channel blocker; including hERG with additional Nav1.5/Cav1.2 activity at higher concentrations) are used in hiPSC-CM action potential/APD validation studies [Data: Sources (27215, 48324)]  
- **Verapamil** (dual blocker: \(I_\mathrm{Kr}\) and \(I_\mathrm{CaL}\)) and **ranolazine** (multi-channel including \(I_\mathrm{Kr}\) and \(I_\mathrm{Na}\)) are cited as examples where multi-channel pharmacology can yield QT-neutral behavior at clinically relevant doses in hPSC-CMs [Data: Sources (30932, 30933)]  
- **FPL 64176** (L-type Ca\(^{2+}\) channel activator) used to probe Ca-channel kinetics/current changes [Data: Sources (30956)]  
- **Heptanol** (gap junction blocker) used to uncouple cardiomyocytes in MEA-based assays [Data: Sources (30956)]  
- **Lidocaine** (Na\(^+\) channel inhibitor) used in MEA/patch studies (e.g., conduction slowing or beating cessation at higher doses) [Data: Sources (30965)]  
- **ZD7288** (If blocker) used to reduce beating frequency [Data: Sources (30988)]  
- **Isoprenaline (isoproterenol)** is used as a β-adrenergic stressor to provoke LQTS-related phenotypes in patient hiPSC-CMs, and **nadolol** (β-blocker) can reverse the induced arrhythmias in vitro [Data: Sources (30888)]. In isogenic GRK5 variant hPSC-CMs, isoprenaline effects on beat rate can be reversed by **propranolol** [Data: Sources (28041)].

### Other small-molecule/probe examples used for “cell stress/toxicity” validation in hPSC-CMs
- **Chelerythrine** (cell-permeable protein kinase C inhibitor) used to trigger stress; imaging readouts include mitochondrial function (e.g., with **TMRM**), apoptosis (caspase-3), and cell death (BOBO-1) [Data: Sources (23451)]  
- **Valinomycin, etoposide, rotenone** used in high-content imaging cardiotoxicity panels [Data: Sources (30997, 23452)]  
- **Doxorubicin** is used as a cardiotoxic reference compound; electrophysiology changes may be detectable acutely, while contractility effects may require longer exposure [Data: Sources (23180, 81934, 81949)].

## Electrophysiology metrics used to validate hPSC-derived (especially cardiac) cells

### Patch-clamp action potential (AP) metrics
Whole-cell patch clamp validation commonly reports:
- **APD** (action potential duration), including **APD\(_{50}\)** and **APD\(_{90}\)** [Data: Sources (22778)]  
- **AP amplitude (APA)**, **resting membrane potential (RMP)**, and **upstroke velocity** [Data: Sources (22778)]  
Some studies also explicitly use **APD\(_{20}\)**, **APD\(_{90}\)**, and **APD\(_{90}\) − APD\(_{20}\)** (a repolarization-shape/triangulation-related metric) [Data: Sources (27079)].

### Ion-current measurements (voltage clamp)
Functional maturity/identity is assessed via current density/kinetics for major currents, including **\(I_\mathrm{Na}\)**, **\(I_\mathrm{Ca}\)/\(I_\mathrm{CaL}\)**, and **K\(^+\)** currents such as **\(I_\mathrm{Kr}\)** [Data: Sources (22736, 22739, 22813, 31009)].

### MEA/field potential metrics (syncytial preparations)
Multi-electrode array readouts used for validation include:
- **Field potential duration (FPD)** and beating frequency/rate changes [Data: Sources (30952, 30988)]  
MEA/patch studies in LQTS models report **EADs (early afterdepolarizations)** and increased FPD/APD relative to controls [Data: Sources (30951)].

### Optical electrophysiology metrics (voltage dyes/optical AP)
Optical platforms (often in CiPA-style evaluations) resolve:
- **Beat rate**
- **Action potential durations** (e.g., **APD\(_{30}\)** and **APD\(_{90}\)**)
- **Action potential shape features spanning depolarization and repolarization** [Data: Sources (48272, 48320)]  
Optical platforms are also described as enabling metrics such as **APD**, **triangulation of repolarization**, and **conduction velocity** [Data: Sources (48270)].

### Impedance-/multimodal platforms that incorporate electrophysiology
Some systems combine mechanical and electrical readouts; for example, **CardioExcyte96** measures **extracellular field potentials** alongside impedance, enabling assessment of **beat rates, amplitudes, and electrophysiology** [Data: Sources (23474)].

---

## G50. [GLOBAL] How do CO2-acidified injection fluids change pH during water–rock reactions?

*ID: 6973ed69-781... | Latency: 20.1s*

**Answer:**

CO2‑acidified injection fluids initially lower pH because dissolved CO2 forms carbonic acid and releases protons as it dissociates ( \(CO_2+H_2O\rightleftharpoons H_2CO_3\rightleftharpoons H^+ +HCO_3^-\rightleftharpoons 2H^+ +CO_3^{2-}\) ) [Data: Sources (231186, 231187, 166040)]. In basaltic aquifers, this can drive a local pH drop from typical formation-water values around pH 8–9.5 down to ~pH 3.5 near the injection zone under pressurised CO2 [Data: Sources (231196, 231197)].

During subsequent water–rock reactions, pH commonly rebounds (is buffered upward) as minerals dissolve and consume acidity. Experiments with volcanic rocks show that when starting from pH ~3, fluid pH can rise toward near‑neutral values over days to weeks (e.g., from pH 3 up to ~5.5–7 depending on sample mineralogy) [Data: Sources (231414, 231358)]. Feldspar dissolution is highlighted as a key neutralisation mechanism: systems with higher feldspar content (and higher anorthite content in plagioclase) tend to be more effective at consuming \(H^+\) and raising pH, which is important because carbonate mineral formation generally requires near‑neutral conditions [Data: Sources (231434, 231113, 231419)]. In modelling/interpretation of these experiments, secondary Al‑hydroxide formation (gibbsite) is predicted to begin after initial feldspar dissolution once pH rises to ~5, and then plateau as pH approaches neutral [Data: Sources (231416, 231417)].

As pH increases and divalent cations are released from dissolving minerals, carbonate precipitation can begin, but this introduces a feedback on pH. Carbonate minerals dissolve rapidly at low pH and thus do not persist under strongly acidic conditions [Data: Sources (231189)]. Once pH is buffered upward, dissolved carbonate species can combine with Ca/Mg/Fe to precipitate carbonates; however, carbonate precipitation itself produces \(H^+\) (e.g., \((Ca,Mg,Fe)^{2+}+CO_2+H_2O\leftrightarrow (Ca,Mg,Fe)CO_3+2H^+\)), so continued mineral dissolution (or mixing with more alkaline formation waters) is needed to consume the generated protons and sustain precipitation [Data: Sources (231380, 231537, 231213)]. This coupling helps explain why mineralisation is favoured where rock dissolution and/or mixing neutralises the injected acidity, and why pH may fluctuate under non‑continuous injection conditions [Data: Sources (231214, 231213)].

Fluid composition (especially salinity) can modify the pH trajectory by influencing CO2 solubility and carbonic acid dissociation. Reported experimental observations show measured starting pH decreasing with increasing NaCl concentration (for solutions equilibrated with atmospheric CO2), with an interpretation that salinity can both reduce CO2 solubility and increase carbonic acid dissociation; the net effect observed was lower pH at higher NaCl [Data: Sources (231625, 231627, 231628)]. In CO2‑charged reservoir contexts, this implies that pH near the injection point may differ between freshwater and seawater/brine injection, and the buffering response will depend strongly on host‑rock mineralogy and its acid neutralisation capacity [Data: Sources (231113, 231223)].

---

# Local Questions (Document-Specific Facts)

---

## L1. [LOCAL] In the CML study’s BCL-2 family inhibitor toolkit, which inhibitor was identified as selective for BCL-XL?

*ID: 78082215-747... | Latency: 10.1s*

**Answer:**

In the CML study’s BCL-2 family inhibitor toolkit, **A-1331852** was identified as the **BCL-XL-selective** inhibitor [Data: Sources (152097, 152101, 152128, 245450)].

---

## L2. [LOCAL] In the colony-forming cell assay using Methocult H4034 (Stem Cell Technologies), how many cells were mixed into 3 mL of methylcellulose before plating into two 35 mm plates?

*ID: 6db3030c-b96... | Latency: 10.1s*

**Answer:**

In the colony-forming cell (CFC) assay using Methocult® H4034 (Stem Cell Technologies), **3000 cells** were mixed into **3 mL** of methylcellulose, and this mixture was then **split evenly between two 35 mm plates** for plating [Data: Sources (243997)].

---

## L3. [LOCAL] In the MD-based MMGBSA and Interaction Entropy ranking of fragment follow-up compounds, how many compounds were predicted to bind more favourably than crystallographic fragment F558?

*ID: 168af94c-c52... | Latency: 10.1s*

**Answer:**

In the MD-based MMGBSA + Interaction Entropy free-energy ranking of the fragment follow-up compounds, **30 compounds** were predicted to bind more favourably (i.e., have significantly better predicted binding free energies) than the most favourable crystallographic fragment **F558** [Data: Sources (273035, 273052, 273053)].

---

## L4. [LOCAL] In the in vitro human germline model, which genomic repeat elements were downregulated in DM*PGCLCs and DZ*PGCLCs compared with 4i embryonic stem cells?

*ID: 8e5f09e5-a06... | Latency: 10.1s*

**Answer:**

In the in vitro human germline model, the repeat subfamilies that were **downregulated in both DM\*PGCLCs and DZ\*PGCLCs compared with 4i embryonic stem (ES) cells** were:

- **LTR7**
- **HERVH-int** (HERVH internal region) [Data: Sources (296916, 297029)]

---

## L5. [LOCAL] In the UK Haematological Malignancy Research Network (HMRN) cohort, how many patients were diagnosed with haematological malignancies between 2009 and 2015?

*ID: f329906f-278... | Latency: 10.1s*

**Answer:**

In the UK Haematological Malignancy Research Network (HMRN) cohort, **18,127 patients** were diagnosed with haematological malignancies **between 2009 and 2015** [Data: Sources (210494, 210499, 210507)].

This figure is reported in the HMRN cohort profile update describing the subset of HMRN patients diagnosed in 2009–2015 who were subsequently matched to population controls for comparative analyses [Data: Sources (210494, 210507, 210508)].

---

## L6. [LOCAL] In the 2021 review “The immune landscape in BCR-ABL negative myeloproliferative neoplasms” (DOI: 10.1111/bjh.17850), which three MPN disorders are listed?

*ID: ceaa53c8-da5... | Latency: 10.1s*

**Answer:**

In the 2021 British Journal of Haematology review **“The immune landscape in BCR-ABL negative myeloproliferative neoplasms” (DOI: 10.1111/bjh.17850)**, the MPN spectrum is stated to include **polycythaemia vera (PV)**, **essential thrombocythaemia (ET)**, and **myelofibrosis** [Data: Sources (245627, 245628, 245630)].

---

## L7. [LOCAL] In Howlett et al.’s 2023 mLR rat ventricular myocyte model, altering which ionic current most strongly affected late repolarization, measured by APD90 prolongation?

*ID: cd2f61a7-582... | Latency: 10.1s*

**Answer:**

In Howlett et al.’s 2023 modified Leeds rat (mLR) ventricular myocyte model, late repolarization (quantified by **APD90 prolongation**) was most strongly affected by altering the **slow delayed rectifier potassium current, \(I_{\mathrm{Ks}}\)**. In their sensitivity analysis, **\(I_{\mathrm{Ks}}\)** alterations produced the **largest magnitude influence on late repolarization**, with reported effects of **~35%–846% APD90 prolongation** under the tested conditions [Data: Sources (272500, 272504)].

---

## L8. [LOCAL] In the Western blot protocol in Input Text 330159, what temperature and incubation duration were used for the primary antibodies on the membranes?

*ID: 670e8528-6ed... | Latency: 10.1s*

**Answer:**

In Input Text 330159’s Western blot protocol, the membranes were incubated with the primary antibodies **at room temperature for 1 hour** [Data: Sources (54712)].

---

## L9. [LOCAL] In the South African linezolid popPK study of adults with drug-resistant pulmonary TB, how many plasma samples were collected from the 124 participants?

*ID: 0491edc2-c45... | Latency: 10.1s*

**Answer:**

In the South African linezolid population pharmacokinetic (popPK) study in adults with drug-resistant pulmonary TB, the **124 participants provided 444 plasma samples** [Data: Sources (206305, 206310, 206316)].

---

## L10. [LOCAL] In the RAFT aqueous dispersion polymerization study of PGMAx–PHBAy nano-objects, between what PGMA stabilizer DPs was the upper limit for obtaining pure worms and vesicles reported?

*ID: 7fda0f19-c5f... | Latency: 10.1s*

**Answer:**

In this RAFT aqueous dispersion polymerization study of **PGMA\_x–PHBA\_y** nano-objects, the authors report that **the upper-limit PGMA stabilizer DP for still obtaining pure worms and pure vesicles lies between PGMA DP = 130 and 140** [Data: Sources (254230)].

---

## L11. [LOCAL] In Input Text 216864’s table for case 1A, on the row where the value is 380, what is the third numeric entry in that row?

*ID: 48c11cb4-1de... | Latency: 10.1s*

**Answer:**

In Input Text **216864**, table for **case 1A**, the row where the value is **380** reads (in part):

`1A | 19 | 6.38 | 380 | 3.230 | 2232.32 | 1.821E-04 | 0.000 | 165.130` [Data: Sources (131717)]

Counting the numeric entries across that row, the **third numeric entry** is **6.38**. [Data: Sources (131717)]

---

## L12. [LOCAL] In the Plasmodium falciparum asexual growth inhibition assay that screened compounds at 10 µM, what IC50 value was reported for the top hit compound A22?

*ID: 9c8885dd-575... | Latency: 10.1s*

**Answer:**

In the *Plasmodium falciparum* asexual growth inhibition assay where compounds were initially screened at a fixed concentration of **10 µM**, the top hit compound **A22** was subsequently dose-tested and reported to have an **IC₅₀ of 8.29 µM** [Data: Sources (289183, 289192)].

---

## L13. [LOCAL] In the TOF ES+ mass spectrometry characterization, what found [M+H]+ m/z value is reported for compound 18: 1-(2-hydroxycyclohexyl)-4-(2-((4-bromo-2-fluorobenzyl)oxy)phenyl)pyridin-2(1H)-one?

*ID: d2dc869c-7c1... | Latency: 10.1s*

**Answer:**

In the TOF ES+ mass spectrometry characterization for compound **18** (1-(2-hydroxycyclohexyl)-4-(2-((4-bromo-2-fluorobenzyl)oxy)phenyl)pyridin-2(1H)-one), the reported **found** \([M+H]^+\) value is **m/z 457.3** [Data: Sources (21745)].

---

## L14. [LOCAL] In the RapidFire high-throughput MS workflow, which mass spectrometer was the Agilent RapidFire RF 365 sampling robot attached to?

*ID: 1672b0b7-60c... | Latency: 10.1s*

**Answer:**

In the RapidFire high-throughput MS workflow, the Agilent RapidFire **RF 365** sampling robot was attached to an **iFunnel Agilent 6550 accurate mass quadrupole time-of-flight (Q-TOF) mass spectrometer** [Data: Sources (124731, 153446, 124208, 182172, 201453, +more)].

---

## L15. [LOCAL] In the 2002 Int J Radiat Oncol Biol Phys pancreatic cancer xenograft study, what anti-EGFR monoclonal antibody name and code were combined with gemcitabine and radiation?

*ID: 6e603058-6b2... | Latency: 10.1s*

**Answer:**

In the **2002 *Int J Radiat Oncol Biol Phys*** pancreatic cancer xenograft study, the anti‑EGFR monoclonal antibody combined with **gemcitabine and radiation** was **Erbitux**, with the code **IMC‑C225** [Data: Sources (326305)].

---

## L16. [LOCAL] In the reported bromination step converting compound 2i into the 3-bromo-5-tert-butyl derivative 12, what brominating reagent was used?

*ID: 9394938f-396... | Latency: 10.1s*

**Answer:**

In the bromination step converting compound **2i** into the **3-bromo-5-tert-butyl derivative 12**, the brominating reagent used was **copper(II) bromide (CuBr₂)** [Data: Sources (85635)].

---

## L17. [LOCAL] In the intravenous pharmacokinetic study analyzed by non-compartmental methods, what clearance rate (mL/min/kg) was reported for Compound 1?

*ID: d4a6d4fd-43c... | Latency: 10.1s*

**Answer:**

In the intravenous pharmacokinetic study analyzed by non-compartmental methods, **Compound 1** was reported to have a **clearance rate of ~28 mL/min/kg** (reported as 28 mL/min/kg; also reported as **27.6 ± 8 mL/min/kg** in the associated PK table) [Data: Sources (37547, 37551, 37516, 37557)].

---

## L18. [LOCAL] In Input Text 99048, what 13C-NMR chemical shift is listed for the spectrum in CDCl3 at 192.8 ppm?

*ID: 3c018ee3-94d... | Latency: 10.1s*

**Answer:**

In Input Text **99048**, the **¹³C-NMR** spectrum recorded in **CDCl₃** lists the carbon resonance at **δ 192.8 ppm** (assigned as **C-1**) [Data: Sources (55753)].

---

## L19. [LOCAL] In Input Text 47880, after diluting the DMF reaction with ethyl acetate, which aqueous solution was used to quench the reaction mixture?

*ID: 1f613388-963... | Latency: 10.1s*

**Answer:**

In Input Text 47880, after diluting the DMF reaction with ethyl acetate, the reaction mixture was quenched/washed using **saturated aqueous sodium bicarbonate (sat. aq. NaHCO₃)** [Data: Sources (139406)].

---

## L20. [LOCAL] In a mouse MVA-Ag85A vaccination study, which cytokine-producing CD8+ T-cell subset was most predominant in Figure 4B?

*ID: 81972b6b-deb... | Latency: 10.1s*

**Answer:**

In **Figure 4B**, the most predominant cytokine-producing **CD8+ T-cell** subset was the population that **simultaneously produced IFN-γ and TNF-α (IFN-γ+ TNF-α+ double-positive cells)** (with IFN-γ–only cells also prominent) [Data: Sources (69341, 69342)].

---

## L21. [LOCAL] In the table labeled Input Text 150292, what adjusted effect estimate (95% CI) is reported for diagnosis age 5–9.9 years versus <5 years?

*ID: 30147569-4a3... | Latency: 10.1s*

**Answer:**

In **Input Text 150292**, the **adjusted effect estimate (95% CI)** reported for **diagnosis age 5–9.9 years versus <5 years** is **1.41 (95% CI 1.02–1.96)** [Data: Sources (328030)].

---

## L22. [LOCAL] In LPS-stimulated bone marrow–derived macrophages, which small molecule analogue (SMA 11a or SMA 12b) suppressed LPS-induced upregulation of IL-1 and NLRP3 mRNA?

*ID: 3d234769-396... | Latency: 10.1s*

**Answer:**

In LPS-stimulated bone marrow–derived macrophages, **SMA 12b** (but not SMA 11a) suppressed the LPS-induced upregulation of **IL-1** and **NLRP3** mRNA [Data: Sources (40737)].

---

## L23. [LOCAL] In poly(I:C)-induced Mx1-cre+Raptorfl/fl mice assessed 5 weeks later, which B-cell marker changed in bone marrow and spleen: Ebf1, Pax5, or both?

*ID: ba7f10a3-6c3... | Latency: 10.1s*

**Answer:**

In poly(I:C)-induced **Mx1-cre+Raptor^fl/fl** mice assessed **5 weeks** later, **Ebf1** was decreased in both **bone marrow and spleen**, while **Pax5 did not change** [Data: Sources (284513, 284518)].

---

## L24. [LOCAL] In the mantle cell lymphoma study, what was the median progression-free survival reported after second-line treatment among patients who received second-line therapy?

*ID: 7173621e-8af... | Latency: 10.1s*

**Answer:**

Among mantle cell lymphoma patients who **received second-line therapy**, the study reported a **median progression-free survival (PFS) after second-line treatment of 1.2 years** (reported alongside an OS of 2.5 years) [Data: Sources (284615)].

---

## L25. [LOCAL] In the in vitro comparison of G-CH1 versus G-CH2 hydrogels seeded with BM-hMSCs/AT-hMSCs, which scaffold was reported as more advantageous for cell growth and mineralization?

*ID: 22a7d989-651... | Latency: 10.1s*

**Answer:**

In the reported in vitro comparison, **G‑CH1** (the gelatin–chitosan hydrogel with lower chitosan content, 8.1 wt%) was described as **more advantageous** than G‑CH2 for **cell growth and scaffold mineralization** when seeded with **BM‑hMSCs and AT‑hMSCs** [Data: Sources (39593, 39503, 39591, 39559, 39504, +more)]. 

Specifically, the authors state that **G‑CH1 supported significantly higher cell proliferation (particularly for BM‑hMSCs)** and showed **better mineralization**, supported by **Von Kossa staining** and related mineralization analyses [Data: Sources (39593, 39559, 39567, 39504, 39503)].

---

## L26. [LOCAL] In Input Text 293245, what GEO Series accession number is listed for the gene expression dataset deposited in NCBI’s Gene Expression Omnibus?

*ID: 66c500fa-271... | Latency: 20.1s*

**Answer:**

In **Input Text 293245**, the gene expression dataset deposited in NCBI’s Gene Expression Omnibus is listed under the GEO Series accession number **GSE90588** [Data: Sources (42398)].

---

## L27. [LOCAL] Which two drugs are identified as the standard therapeutic options for treating Chagas disease in the input texts?

*ID: 94a68006-073... | Latency: 10.1s*

**Answer:**

The two drugs identified as the standard (and only approved/proven effective) therapeutic options for treating Chagas disease in the provided texts are **benznidazole** and **nifurtimox** [Data: Sources (9719, 33741, 54501, 245858, 332286, +more)].

---

## L28. [LOCAL] What DOI is listed for the 2017 ChemMedChem article authored by N. Trapp, W. Haap, T. Schirmeister, and F. Diederich?

*ID: 1e40a840-6e3... | Latency: 10.1s*

**Answer:**

The 2017 *ChemMedChem* article authored by N. Trapp, W. Haap, T. Schirmeister, and F. Diederich lists the DOI **10.1002/cmdc.201600563**. [Data: Sources (305688)]

---

## L29. [LOCAL] In Table 1 of the drug-release model, what baseline value is listed for Df, the diffusion coefficient in the fluid-infused core?

*ID: f3449d70-e35... | Latency: 10.1s*

**Answer:**

In **Table 1** of the drug-release model, the listed baseline value for **\(D_f\)** (the diffusion coefficient in the fluid-infused core) is:

\[
D_f = 10^{-9}\ \left(m^{2}s^{-1}\right)
\]
[Data: Sources (266455, 266456)]

---

## L30. [LOCAL] At the end of 7-day, 100°C batch reactor experiments simulating CO2-acidified injection fluids, what pH values were typically measured in post-experiment fluids reacted with the PF feldspar sample?

*ID: 8526e90a-b60... | Latency: 20.1s*

**Answer:**

In the 7-day batch reactor experiments at 100 °C intended to simulate CO₂-acidified injection fluids (target starting pH ≈3 via HCl addition), the **post-experiment fluids that reacted with the PF feldspar sample typically had final pH values “roughly around 5.”** [Data: Sources (231622)]

The study further summarizes this as **pH values close to 5 measured in most post-experiment PF fluids** (contrasting with the AF feldspar series, where pH remained close to 3). [Data: Sources (231641)]

---

## L31. [LOCAL] In the neutron-diffraction-based structural modelling of the studied silicate glasses, what coordination number (CN) is assumed for oxygen?

*ID: 18177fad-d4e... | Latency: 10.1s*

**Answer:**

In the neutron-diffraction-based structural modelling of the studied silicate glasses, oxygen is **assumed to be 4-coordinated (CN = 4)** [Data: Sources (16291, 16512, 16474)].

---

## L32. [LOCAL] In chapter 4 AFM SMFS tests on Ecad-Fc functionalised surfaces, what effect did adding the E-cadherin-targeting peptide EpepW2R have on adhesion frequency?

*ID: 4a72e13e-5ca... | Latency: 10.1s*

**Answer:**

In Chapter 4 SMFS experiments on **Ecad‑Fc functionalised surfaces**, adding the E‑cadherin‑targeting peptide **EpepW2R** caused a **decrease in the frequency of specific adhesion events** (i.e., reduced adhesion frequency relative to the Ca²⁺ control condition) [Data: Sources (277463, 277464, 277487, 277495)].

In the **EpepW2R titration** (1 µM, 10 µM, 100 µM), the peptide-induced reduction in specific adhesion frequency was observed across concentrations, and at **100 µM** the loss of adhesion events was reported as **comparable to** the inhibition seen with **EGTA** and **DECMA‑1** buffers [Data: Sources (277463, 277464)]. The inhibition was also reported to be **reversible**: after replacing the peptide solution with **Ca²⁺ buffer**, the adhesion frequency returned to the original Ca²⁺ baseline [Data: Sources (277464, 277495)].

---

## L33. [LOCAL] In Arber et al. (2015) hPSC differentiation experiments, which two mRNAs increased with SHH treatment (alone or with Activin) compared with Activin treatment?

*ID: bf095f3d-63e... | Latency: 10.1s*

**Answer:**

In the Arber et al. (2015) hPSC differentiation experiments, **SHH treatment** (either **alone** or **combined with Activin**) increased **NKX2.1** and **LHX8** mRNA compared with **Activin treatment** [Data: Sources (162501)].

---

## L34. [LOCAL] In the Burkina Faso population pharmacokinetic study of oral artesunate–mefloquine (ClinicalTrials.gov NCT00701961), by what percentage was dihydroartemisinin clearance higher in pregnant women than controls?

*ID: e21242a7-8c9... | Latency: 10.1s*

**Answer:**

In the Burkina Faso population pharmacokinetic study of oral artesunate–mefloquine (ClinicalTrials.gov NCT00701961), **dihydroartemisinin (DHA) clearance was 21% higher in pregnant women than in non-pregnant controls** [Data: Sources (51486, 51494, 51526, 51567, 193298)].

---

## L35. [LOCAL] In Input Text 298340’s TaqMan qRT-PCR analysis on QuantStudio 7 using a ΔΔCt approach, which endogenous control genes were used for normalization?

*ID: 3c5b628e-e4a... | Latency: 10.1s*

**Answer:**

In Input Text 298340, the TaqMan qRT-PCR data on the QuantStudio 7 were normalized using **Actb**, **B2m**, and **Gapdh** as the endogenous control genes for the ΔΔCt calculations [Data: Sources (175638, 283817)].

---

## L36. [LOCAL] In mouse brain tissue, how many times higher was measurable Evans Blue per mg after vincristine treatment (days 0–4) than after saline treatment?

*ID: f8392853-24e... | Latency: 10.1s*

**Answer:**

In mouse **brain** tissue, vincristine (days 0–4) resulted in **more than three times higher** measurable Evans Blue (per mg) than saline treatment [Data: Sources (55412)].

---

## L37. [LOCAL] In the orthotopic mouse TNBC model with 750,000 MDA-MB-231 Luc+ cells implanted in the mammary fat pad, what tumor volume threshold was used to sacrifice mice?

*ID: b1e9bc27-a63... | Latency: 10.1s*

**Answer:**

In this orthotopic TNBC model (750,000 MDA-MB-231 Luc+ cells implanted into the mammary fat pad), mice were sacrificed when the tumor volume reached **1,500 mm³** [Data: Sources (261097)].

---

## L38. [LOCAL] In the NCS1 competition experiments using the native D2R peptide, what binding affinity is reported for the D2R peptide–NCS1 interaction?

*ID: d8db8121-f55... | Latency: 10.1s*

**Answer:**

In the NCS1 competition experiments using the native D2R peptide, the D2R peptide–NCS1 interaction is described as having a **binding affinity of 30 µM** (with a reported **2:1 ligand:peptide ratio**) [Data: Sources (327008, 327009)].

---

## L39. [LOCAL] In the 72-hour resazurin viability assay for K562 and KCL22 cells, what excitation and emission wavelengths were used to read the plate on a microplate reader?

*ID: d93131a3-c73... | Latency: 10.1s*

**Answer:**

In the 72-hour resazurin viability assay for K562 and KCL22 cells, plates were read using **535 nm excitation** and **590 nm emission** on a microplate reader [Data: Sources (241616)].

---

## L40. [LOCAL] In acute myeloid leukemia (AML), which FLT3 mutation is described as causing ligand-independent activation of the FLT3 receptor?

*ID: 03213d92-4cc... | Latency: 10.1s*

**Answer:**

In AML, **FLT3 internal tandem duplication (FLT3‑ITD)** mutations are described as causing **ligand-independent activation of the FLT3 receptor** [Data: Sources (192961, 85153, 85158, 297408, 251319, +more)].

---

## L41. [LOCAL] In Mahmood et al. (2016), which two endocytosis pathways mainly internalized HIV-1 Tat 49–57 peptide–decorated SEDDS anchored with oleic acid?

*ID: b7679fda-a4e... | Latency: 10.1s*

**Answer:**

In Mahmood et al. (2016), HIV-1 Tat 49–57 peptide–decorated SEDDS anchored with oleic acid were mainly internalized via **clathrin-mediated endocytosis** and **caveolae-mediated endocytosis** [Data: Sources (44954, 44955)].

---

## L42. [LOCAL] In Input Text 113813, what full postal address is listed for the Leeds Institute of Medical Research at St James's University Hospital in Leeds, United Kingdom?

*ID: 2a815acc-0eb... | Latency: 10.1s*

**Answer:**

In Input Text **113813**, the **Leeds Institute of Medical Research at St James's University Hospital** is listed at the following full postal address:

**Leeds Institute of Medical Research, Faculty of Medicine and Health, University of Leeds, St. James's Hospital, Beckett Street, Leeds LS9 7TF, United Kingdom**. [Data: Sources (228554)]

---

## L43. [LOCAL] In Input Text 142270, what institution is listed as affiliation 1 for author Axel Behrens?

*ID: db277799-535... | Latency: 10.1s*

**Answer:**

In Input Text 142270, **affiliation 1** for author **Axel Behrens** is listed as **the Cancer Research UK Manchester Centre (FC001039)** [Data: Sources (194962)].

---

## L44. [LOCAL] In the chemotherapy HRQoL study of malignant pleural mesothelioma patients, how many weeks after baseline was time point 3 scheduled?

*ID: 41a802b0-923... | Latency: 10.1s*

**Answer:**

In the chemotherapy HRQoL sub-study of the SWAMP trial in malignant pleural mesothelioma, **time point 3 (visit 3) was scheduled at 16 weeks after baseline** [Data: Sources (78991, 79029, 79012, 78981, 79030)].

This aligns with the paper’s description of HRQoL assessments at five time points—**baseline, 6 weeks, 16 weeks, 12 months, and 18 months**—and with multiple analyses explicitly framing outcomes as “from baseline to 16 weeks” and “at 16 weeks” for visit/time point 3 [Data: Sources (78991, 79012, 79029, 78981, 79000)].

---

## L45. [LOCAL] In the DESeq2 differential expression workflow described in Input Text 200604, what adjusted p-value cutoff and minimum fold-change were used to define differentially expressed genes?

*ID: f32d3625-9c8... | Latency: 10.1s*

**Answer:**

In the DESeq2 differential expression workflow described in Input Text 200604, genes were defined as differentially expressed using an adjusted p-value (Benjamini–Hochberg) cutoff of **< 0.05** and a minimum fold-change of **≥ 1.5 (absolute fold change)** [Data: Sources (96070)].

---

## L46. [LOCAL] In immunocytochemistry of day-16 progenitors from the 34D6 human iPSC line, what percentages of cells were GSX2+ and CTIP2+?

*ID: c24b46c8-17f... | Latency: 10.1s*

**Answer:**

In day-16 progenitors from the **34D6 human iPSC line**, immunocytochemistry showed approximately **32% GSX2+** cells and approximately **54% CTIP2+** cells (each reported as a percentage of total DAPI+ nuclei) [Data: Sources (162947, 162948)].

---

## L47. [LOCAL] In NONMEM pharmacokinetic modeling, what ΔOFV threshold indicates a significant likelihood-ratio-test improvement at P=0.05 when adding one parameter to a nested model?

*ID: 62d4dee0-ad7... | Latency: 10.1s*

**Answer:**

In NONMEM pharmacokinetic modeling, when comparing **nested** models that differ by **one additional parameter** (i.e., **1 degree of freedom**), a **decrease in objective function value (ΔOFV) of 3.84 or more** is commonly used as the likelihood-ratio-test criterion for a statistically significant improvement at **P = 0.05** (based on the χ² distribution) [Data: Sources (32417, 51512, 90121, 105481, 191634, +more)].

---

## L48. [LOCAL] In Figure 1A flow-cytometry analysis of 8–10-week-old mouse bone marrow, how many Flt3+/+ mice and how many Flt3-ITD/ITD mice were included?

*ID: fd02d2bb-c42... | Latency: 10.1s*

**Answer:**

In Figure 1A (flow-cytometry analysis of 8–10-week-old mouse bone marrow), the study included **31 Flt3+/+ mice** and **23 Flt3-ITD/ITD mice** [Data: Sources (99929)].

---

## L49. [LOCAL] In the mouse competitive HSC transplantation schematic using CD45.2 donor HSCs, how many donor HSCs were mixed with how many competitor bone marrow cells?

*ID: d041fc93-54a... | Latency: 10.1s*

**Answer:**

In the competitive HSC transplantation schematic with **CD45.2 donor HSCs**, the donor and competitor cells were mixed as **150 donor HSCs** with **2 × 10^5 competitor bone marrow (BM) cells (CD45.1)** before transplantation into lethally irradiated CD45.1 recipients [Data: Sources (173503, 173504)].

---

## L50. [LOCAL] What were the dates of the 14th post-American Society of Hematology (ASH) International Workshop on Chronic Myeloproliferative Malignancies in Orlando, Florida?

*ID: ea4c772f-617... | Latency: 10.1s*

**Answer:**

The 14th post-American Society of Hematology (ASH) International Workshop on Chronic Myeloproliferative Malignancies in Orlando, Florida took place on **December 10 and 11, 2019** [Data: Sources (245721, 245724, 245725, 245729)].

---
