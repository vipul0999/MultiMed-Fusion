# 📑 Research Notes – Multi-Modal Medical Data & AI Summary

---

## 1. Project Brief
MultiMed Fusion is a tool that collects medical files such as **lab reports, medical images, and audio notes**, then uses AI to create **easy-to-read summaries** for doctors.  
The goal is to save doctors time, reduce cognitive load, and ensure patient privacy through anonymization.  

### User Stories
- **Doctor:** Wants a single summary from different sources to save time.  
  - *Acceptance:* AI generates a structured summary with links back to original files.  
- **Patient:** Wants private details removed to keep their data safe.  
  - *Acceptance:* Uploaded files are anonymized before saving or processing.  

---

## 2. Key Research Areas

### a) Clinical & Radiology Summarization
- Large Language Models (LLMs) like **BioBART, ClinicalBERT, GPT-4, and MedPaLM** can summarize discharge notes, radiology reports, and doctor-patient conversations.  
- Datasets used for evaluation include:  
  - **MIMIC-CXR** (radiology reports)  
  - **RadSum23** (radiology summarization)  
  - **MEDIQA** (clinical summarization benchmarks)  
- Evaluation Metrics: **ROUGE**, **BERTScore**, and **clinician factuality checks** to ensure accuracy.  

### b) Privacy & De-identification
- **HIPAA** requires removal of 18 PHI (Protected Health Information) identifiers.  
- Two main de-identification approaches:  
  - **Safe Harbor** → rule-based removal of identifiers.  
  - **Expert Determination** → expert validates anonymization process.  
- Tools & Methods:  
  - **Text de-ID:** i2b2/n2c2 datasets, Microsoft **Presidio**, NER-based pipelines.  
  - **Image de-ID:** **pydicom** tools + DICOM PS3.15 Annex E for metadata cleanup.  
  - Hybrid approach (rules + ML) offers better balance between safety and accuracy.  

### c) Traceability & Interoperability
- **FHIR (Fast Healthcare Interoperability Resources)** provides standards to keep links back to original files.  
  - **DocumentReference** and **Media** resources ensure traceability.  
- Doctors must be able to cross-check every summary with its source for clinical trust.  

---

## 3. References (Current Sources)
- [HIPAA De-identification Guidance – HHS](https://www.hhs.gov/hipaa/for-professionals/special-topics/de-identification/index.html)  
- [DICOM PS3.15 (De-identification Profiles)](https://dicom.nema.org/medical/dicom/current/output/html/part15.html)  
- [i2b2 De-identification Challenge (PHI benchmark)](https://portal.dbmi.hms.harvard.edu/projects/n2c2-nlp/)  
- [Microsoft Presidio (open-source de-ID tool)](https://github.com/microsoft/presidio)  
- [HL7 FHIR Overview](https://www.hl7.org/fhir/overview.html)  
- [MIMIC-CXR Radiology Dataset](https://physionet.org/content/mimic-cxr/)  
- [Clinical Summarization Surveys – JMIR, Nature Digital Medicine]  

---

## 4. Open Research Questions
- Which summarization model works best for **multi-source input** (BioBART vs ClinicalBERT vs GPT-4/MedPaLM)?  
- How to design **factual correctness checks** so summaries remain clinically valid?  
- Which pipeline is most effective for de-identification: **rule-based only** or **hybrid ML + rules**?  
- How should the **UI/UX** highlight traceability (e.g., clickable references for every summary line)?  

---

## 5. Next Steps
- Collect latest (2023–2025) research papers on **clinical summarization benchmarks**.  
- Test **open-source de-identification tools** like Presidio on dummy medical notes.  
- Experiment with **FHIR DocumentReference** for linking original files.  
- Keep a **daily/weekly research log** and commit updates to GitHub Wiki.  

---

*Last updated: 09/27/2025*  
