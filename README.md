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

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|---|---|
| Python | Core language |
| Django + Django REST Framework | REST API framework, routing, middleware |
| Celery | Async background task processing (OCR, embedding, transcription) |
| Redis | Task queue broker for Celery + response caching |
| JWT (djangorestframework-simplejwt) | Authentication and secure token management |

### Frontend
| Technology | Purpose |
|---|---|
| React.js | Single-page application UI |
| JavaScript (ES6+) | Frontend logic and API integration |
| CSS | Styling and layout |

### AI / ML
| Technology | Purpose |
|---|---|
| OpenAI API | LLM-based AI summary generation from retrieved context |
| Hugging Face Transformers | Pre-trained models for NLP tasks and embedding support |
| Sentence Transformers | Vector embedding generation for semantic search (RAG pipeline) |
| Tesseract OCR | Text extraction from medical images and scanned documents |
| Audio Transcription API | Speech-to-text conversion for doctor audio notes |
| RAG (Retrieval-Augmented Generation) | Grounded AI summarization pipeline from document embeddings |

### Data & Storage
| Technology | Purpose |
|---|---|
| MongoDB | Primary database for patient records, vector embeddings, AI summaries, and audit logs |
| PostgreSQL | Structured relational storage for user and access management |
| AWS S3 | Secure medical file storage (PDFs, images, audio) with versioning |
| Redis | Task queue broker for Celery + caching layer for repeated queries |
| DICOM Storage | Local path-based storage for medical imaging files |

### Data Privacy & Security
| Technology | Purpose |
|---|---|
| spaCy | NLP-based Named Entity Recognition for PHI (patient info) detection |
| Microsoft Presidio | Advanced PII detection and anonymization (supported mode) |
| pydicom | DICOM medical image anonymization |
| Regex | Pattern-based identifier redaction |
| RBAC | Role-based access control (doctors, admins, testers) |
| Audit Logging | HIPAA-aligned traceability for all patient data actions |
| Encryption | Sensitive data encrypted at rest in the database |

### DevOps & Testing
| Technology | Purpose |
|---|---|
| Docker | Containerised deployment |
| GitHub Actions | CI/CD pipeline (automated testing on push) |
| PyTest | Unit and integration testing |
| Postman | API endpoint testing |

---

## ✨ New Features (This Week's Updates)

- 🧾 **MongoDB Seed Data Added** → Introduced detailed JSON seed files for all major collections (`users`, `patients`, `doctors`, `medical_files`, `ai_summaries`, `vectors`, and `audit_logs`). This provides structured initial data for testing, validation, and integration with the backend.
- 🧠 **Functional Requirements Wiki (Iteration 2)** → Updated wiki with new mandatory and recommended system requirements, following RFC 2119 standards (SHALL, SHOULD, MAY). A direct link to this page has been added to the main project wiki.
- ⚙️ **Environment Setup Enhancements** → Updated `.env.sample` with new variables for AI APIs, logging, DICOM handling, caching, and email notifications.
- 🩺 **Data Audit Logger Integrated** → `medical_data_collector.py` now automatically logs new patient data actions using `data_audit_logger.py`. This improves traceability and supports HIPAA compliance tracking.
- 💾 **Data Validation Improvements** → Introduced safety checks for filenames, data types, and duplicate record prevention.
- 📁 **Repository Structure Cleanup** → Organized files for better maintainability and updated documentation links.
- 🧩 **Medical Data Collector Upgrade** → Enhanced to save structured patient data to JSON files and support integration with MongoDB collections.

---

## 📊 UML Diagrams

To better understand the system, we created diagrams:

- **Use Case Diagram**
- **System Architecture**
- **Sequence Diagram**

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
- **Data Management Plan** → Explains what data is stored, how it's structured, and how it's secured.
- **Functional Requirements (Iteration 2)** → Updated and maintained in the project **Wiki**, with links from the main page.

---

## 🧩 Environment Setup

The environment configuration file (`.env.sample`) now includes settings for:

- MongoDB and PostgreSQL databases
- AWS S3 file storage with versioning enabled
- OpenAI API and Hugging Face API keys for AI summarization
- Audio transcription service API key
- DICOM file paths for medical imaging storage and processing
- Redis URL for Celery task queue and response caching
- Anonymization mode (`regex_spacy` or `presidio`)
- Logging, audit trail, and encryption controls
- SMTP and email notification settings
- CORS origins for React frontend (`localhost:3000`)

Refer to the **Environment Setup Guide** in `/docs/` for installation and configuration steps.

---

## 📌 Future Enhancements

- Confidence scores for AI-generated summaries.
- Export summaries as **PDF/CSV** directly from the dashboard.
- Real-time notifications via **WebSockets**.
- Integration with **hospital EHR systems**.
- Automatic backup of patient data and audit logs to secure cloud storage.

---

*Last updated: 06/2026*
