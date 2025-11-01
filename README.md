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

- 🧾 **Data Audit Logger Added** → Introduced `data_audit_logger.py` to track key system events such as file uploads, deletions, and record updates.  
  Each log entry now includes a timestamp, event type, user, and a short description for **traceability and compliance**.  
- 🩺 **Integration Pipeline Enhancement** → `medical_data_collector.py` now integrates with the audit logger to automatically record new patient data activities.  
- 💾 **Data Management Plan** → Added new planning document outlining **data storage structure, security, and access control**.  
- 🧠 **Improved Data Validation** → Added `safe_filename_generator.py` for generating safe filenames with timestamps to avoid naming conflicts or overwrites.  
- 🧰 **Maintenance Utilities** → Introduced helper scripts for **merging, validating, and cleaning patient data**.  
- 🔍 **Logging & Error Handling Improvements** → Added detailed exception handling and structured logging for file parsing and record validation errors.  
- 📁 **Repository Organization** → Cleaned up project structure for easier navigation and updated `.env.sample` configuration file.

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

- Unit and integration testing using **PyTest**.  
- API testing using **Postman**.  
- Validation tests added for **redaction, filename generation, and data merging scripts**.  
- Test results stored under `/tests/reports/` for consistency.  

---

## 📚 Documentation

- **Non-Functional Requirements** → Describes performance, security, reliability, and compliance standards.  
- **Data Management Plan** → Explains what data is stored, how it’s structured, and how it’s secured.  

---

## 📌 Future Enhancements

- Background processing with **Celery + Redis** for heavy AI tasks.  
- Role-based access control for doctors, administrators, and testers.  
- Export summaries as **PDF/CSV** directly from the dashboard.  
- Real-time notifications via **WebSockets**.  
- Integration with **hospital EHR systems**.  
- Confidence scores for AI-generated summaries.  
- Automatic backup of patient data and audit logs to secure cloud storage.  

---

*Last updated: 10/31/2025*
