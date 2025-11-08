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

- 🧾 **MongoDB Seed Data Added** → Introduced detailed JSON seed files for all major collections (`users`, `patients`, `doctors`, `medical_files`, `ai_summaries`, `vectors`, and `audit_logs`).  
  This provides structured initial data for testing, validation, and integration with the backend.
- 🧠 **Functional Requirements Wiki (Iteration 2)** → Updated wiki with new mandatory and recommended system requirements, following RFC 2119 standards (SHALL, SHOULD, MAY).  
  A direct link to this page has been added to the main project wiki.
- ⚙️ **Environment Setup Enhancements** → Updated `.env.sample` with new variables for AI APIs, logging, DICOM handling, caching, and email notifications.
- 🩺 **Data Audit Logger Integrated** → `medical_data_collector.py` now automatically logs new patient data actions using `data_audit_logger.py`.  
  This improves traceability and supports HIPAA compliance tracking.
- 💾 **Data Validation Improvements** → Introduced safety checks for filenames, data types, and duplicate record prevention.
- 📁 **Repository Structure Cleanup** → Organized files for better maintainability and updated documentation links.
- 🧩 **Medical Data Collector Upgrade** → Enhanced to save structured patient data to JSON files and support integration with MongoDB collections.

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
- Database seeding verified using `mongoimport` with seed JSON files.  
- Test results stored under `/tests/reports/` for consistency.  

---

## 📚 Documentation

- **Non-Functional Requirements** → Describes performance, security, reliability, and compliance standards.  
- **Data Management Plan** → Explains what data is stored, how it’s structured, and how it’s secured.  
- **Functional Requirements (Iteration 2)** → Updated and maintained in the project **Wiki**, with links from the main page.  

---

## 🧩 Environment Setup

The environment configuration file (`.env.sample`) now includes settings for:
- MongoDB and PostgreSQL databases  
- AWS / S3 file storage  
- Hugging Face and OpenAI API keys  
- DICOM file paths for medical imaging  
- Redis caching and background task flags  
- Logging, anonymization, and file upload controls  
- SMTP and notification settings  

Refer to the **Environment Setup Guide** in `/docs/` for installation and configuration steps.

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

*Last updated: 11/07/2025*
