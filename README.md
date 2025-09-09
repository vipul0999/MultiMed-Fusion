# MultiMed-Fusion
A tool that collects medical files like lab reports, medical images, audio notes and then uses AI to create easy to read summaries for doctors .


Problem Statement:

Doctors often have to review information scattered across lab reports, medical scans, and dictated notes before making decisions. Going through each file one by one takes a lot of time, and important details can be missed under the pressure of heavy workloads. At the same time, patients worry about how safely their personal health details are handled when this data is stored or shared.

Right now, there isn’t a simple way to bring all these different types of medical data together in one place, summarize them clearly, and still keep patient privacy protected. MultiMed Fusion – Multi-Modal Medical Data & AI Summary is designed to close that gap. The tool gathers data from different sources, removes sensitive identifiers, and produces an AI-generated summary with links back to the original files. This helps doctors save time, reduces their workload, and gives patients confidence that their information is handled responsibly.

Technicalities and Softwares used:

The MultiMed Fusion project uses a Python (Flask/FastAPI) backend with AI models built on PyTorch/TensorFlow and Hugging Face to generate summaries from medical reports, images, and audio notes. A Bootstrap-based dashboard presents these summaries with links to original files, while spaCy, regex, and pydicom ensure anonymization of sensitive data. Results are stored in MongoDB/PostgreSQL, tested with PyTest and Postman, versioned in GitHub, and deployed on Render or Dockerized cloud environments for accessibility.
(09/03/2025)

---

## ✨ New Features & Functions (Extension)

### 1. Critical Findings Highlight  
Summaries now highlight **abnormal lab values, urgent notes, or red-flag findings** in a color-coded format so doctors can prioritize urgent cases faster.  

### 2. Multi-Language Support  
The dashboard supports **multiple languages**, allowing international doctors and patients to interact with the system more easily.  

### 3. Audit & Traceability  
Every summary includes **links back to the original files** and a change log of anonymization steps, ensuring full traceability for compliance and audits.  

### 4. Role-Based Access Control  
User accounts can be set up for **doctors, administrators, and researchers** with different access levels, keeping patient data secure and restricting who can view what.  

### 5. Export & Reporting  
Doctors can export AI-generated summaries as **PDF or CSV reports**, making it easier to attach findings to patient records or share with colleagues.  

### 6. API Endpoints for Integration  
MultiMed Fusion now exposes **REST API endpoints** so hospitals can integrate summaries into their existing Electronic Health Record (EHR) systems.  

---

📌 *These functions are part of ongoing improvements to make MultiMed Fusion more practical, accessible, and secure for real-world healthcare workflows.*
(09/09/25)


