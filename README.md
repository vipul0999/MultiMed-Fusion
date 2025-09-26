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

## ✨ New Features (Latest Updates)

- 📂 **File Versioning** → Keeps old versions of uploaded files for safety and compliance.  
- 🔎 **Search Functionality** → Doctors can search summaries by **keywords or dates**.  
- 📧 **Basic Notifications** → Email alerts when summaries are ready.  
- ❤️ **Health Check Endpoint** → `/health` endpoint to verify if the backend is running.  
- 🔐 **Access Control** → Only authorized users can view patient data.  
- 🧪 **Testing Improvements** → Added automated test coverage reports with CI.  
- 📊 **System Monitoring** → Added `/metrics` endpoint to track system performance.  

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

## 📌 Future Enhancements

- Background processing with **Celery + Redis** for heavy AI tasks.  
- Role-based access control for doctors, administrators, and testers.  
- Export summaries as **PDF/CSV** directly from the dashboard.  
- Real-time notifications via **WebSockets**.  
- Integration with **hospital EHR systems**.  

---

*Last updated: 09/26/2025*
