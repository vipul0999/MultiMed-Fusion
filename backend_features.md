# Backend Features – MultiMed Fusion

The backend of MultiMed Fusion is responsible for handling data collection, anonymization, AI-driven summarization, and secure storage.  
It is built with **Python (Flask/FastAPI)** and integrates multiple libraries and services to support multimodal healthcare data.

---

## 🔧 Core Backend Features

### 1. File Upload & Management
- Accepts **PDF reports, DICOM images, and audio notes** through secure upload endpoints.
- Enforces file size limits and validates supported formats.
- Assigns metadata (file type, timestamp, user ID) to each upload.

### 2. Data Anonymization
- Uses **spaCy + regex** to remove personal identifiers from text reports.
- Leverages **pydicom** to strip metadata from medical images.
- Hashes patient IDs into anonymized tokens for consistent referencing.

### 3. AI Summarization Pipeline
- Runs uploaded files through preprocessing (OCR for PDFs, transcription for audio).
- Uses **PyTorch/TensorFlow + Hugging Face Transformers** for generating summaries.
- Combines multimodal inputs into a unified summary document.

### 4. API Endpoints
- RESTful API with endpoints for:
  - File upload (`/upload`)
  - Generate summary (`/summarize`)
  - Retrieve summaries (`/summaries/{id}`)
  - Anonymization testing (`/anonymize/test`)
- Returns results in **JSON** for easy integration with the frontend or hospital systems.

### 5. Database & Storage
- **MongoDB / PostgreSQL** used for storing summaries, metadata, and anonymized references.
- Stores large files (scans, audio) in cloud storage (AWS S3 or equivalent).
- Ensures traceability by linking every summary back to its original file.

### 6. Security & Privacy
- Implements **JWT authentication** for secure API access.
- Encrypts sensitive data at rest and in transit (HTTPS, TLS).
- Provides audit logs of file uploads, anonymization, and summary generation.

### 7. Testing & Quality Assurance
- **PyTest** used for backend unit and integration tests.
- **Postman** collections to validate API endpoints.
- Continuous Integration (CI) via **GitHub Actions** ensures code quality.

---

## 📌 Future Enhancements
- Background processing using **Celery + Redis** for heavy AI tasks.
- Role-based access control for doctors, administrators, and researchers.
- Integration endpoints for EHR (Electronic Health Record) systems.
- Real-time notifications when summaries are ready.

---

✍️ *Prepared by Team 1 – MultiMed Fusion Backend Team*
