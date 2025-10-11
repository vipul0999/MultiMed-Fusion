# 🏥 MultiMed-Fusion

MultiMed-Fusion is a tool that collects medical files like **lab reports, medical images, and audio notes**, then uses **AI** to create easy-to-read summaries for doctors.  
The project is designed to save doctors time, reduce information overload, and protect patient privacy.

---

## 📌 Problem Statement

Doctors often have to review information scattered across **lab reports, medical scans, and dictated notes** before making decisions.  
Going through each file one by one takes a lot of time, and important details can be missed under the pressure of heavy workloads.  

At the same time, **patients worry about how safely their personal health details are handled** when data is stored or shared.

Currently, there is no simple way to:  
- Bring together different types of medical data in one place.  
- Summarize them clearly for fast decision-making.  
- Ensure patient privacy is preserved.  

**MultiMed Fusion – Multi-Modal Medical Data & AI Summary** closes this gap.  
The system gathers data from multiple sources, removes sensitive identifiers, and produces an **AI-generated summary** with links back to the original files.  

This helps:  
- ✅ Doctors save time and reduce their workload.  
- ✅ Patients feel confident that their information is handled responsibly.  

---

## 🛠️ Technicalities and Software Used

- **Backend**: Python (**Flask/FastAPI**)  
- **AI Models**: PyTorch / TensorFlow + Hugging Face Transformers  
- **Frontend**: Bootstrap-based dashboard for summaries and file links  
- **Data Privacy**: spaCy, regex, and pydicom for anonymization  
- **Database**: MongoDB / PostgreSQL for summaries, metadata, and anonymized references  
- **Cloud & Deployment**: Render / Dockerized environments  
- **Testing**: PyTest + Postman collections  
- **Version Control**: GitHub (with GitHub Actions for CI/CD)  

---

## ✨ New Features (This Week’s Updates)

- 🧩 **Anonymization & Validation Modules** → Added regex and validation functions to automatically mask names, emails, and phone numbers in patient data.  
- 🧠 **Enhanced AI Summarization Pipeline** → Optimized text extraction, transcription, and embedding generation for improved accuracy.  
- 🧾 **Developer Guide Added** → A complete setup and contribution guide (`DEVELOPER_GUIDE.md`) for onboarding new contributors.  
- 🧪 **Testing Guide Created** → Detailed testing steps with **unit tests, integration tests, and Postman collection** added to `TESTING_GUIDE.md`.  
- 📄 **Non-Functional Requirements (Iteration 2)** → Added documentation on performance, security, reliability, and compliance requirements.  
- 🗂️ **Research Notes** → Added summarized findings on privacy, interoperability, and clinical summarization techniques.  
- 🧰 **Environment Configuration Update** → Simplified `.env.sample` with clearer variable grouping and toggles for anonymization and async tasks.  
- ⚙️ **Patient Record Merger Script** → Introduced `merge_patient_records.py` for combining multiple patient records with validation and logging.  

---

## 📊 UML Diagrams

To better understand the system, we created diagrams:

- **Use Case Diagram**  
  ![Use Case Diagram](https://github.com/vipul0999/MultiMed-Fusion/blob/main/Images/updated_use_case_diagram_clear.png)

- **System Architecture**  
  ![System Architecture](https://github.com/vipul0999/MultiMed-Fusion/blob/main/Images/system_architecture.png)

- **Sequence Diagram**  
  ![Sequence Diagram](https://github.com/vipul0999/MultiMed-Fusion/blob/main/Images/sequence_diagram.png)

---

## 🧪 Testing Overview

- Unit and Integration testing via **PyTest**.  
- API validation with **Postman**.  
- Code coverage tracking in GitHub Actions.  
- Redaction and validation modules now include test cases for PII detection.  
- Test results are automatically logged in `/tests/reports/`.  

---

## 📚 Developer Documentation

- **Developer Guide** → [DEVELOPER_GUIDE.md](https://github.com/vipul0999/MultiMed-Fusion/wiki/Developer-Guide)  
- **Testing Guide** → [TESTING_GUIDE.md](https://github.com/vipul0999/MultiMed-Fusion/wiki/Testing-Guide)  
- **Research Notes** → [RESEARCH_NOTES.md](https://github.com/vipul0999/MultiMed-Fusion/wiki/Research-Notes)  
- **Non-Functional Requirements** → [NON_FUNCTIONAL_REQUIREMENTS.md](https://github.com/vipul0999/MultiMed-Fusion/wiki/Non-Functional-Requirements)  

---

## 📌 Future Enhancements

- Background processing with **Celery + Redis** for heavy AI tasks.  
- Role-based access control for doctors, administrators, and testers.  
- Export summaries as **PDF/CSV** directly from the dashboard.  
- Real-time notifications via **WebSockets**.  
- Integration with **hospital EHR systems**.  
- Integration of **confidence scores** in AI-generated summaries.  

---

*Last updated: 10/10/2025*
