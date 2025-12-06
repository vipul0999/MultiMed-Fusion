# Environment Setup – `.env.sample`

To make our project easy to configure, we use an environment file called `.env`.  
This file holds important settings such as database connections, storage paths, and API keys.  

We have created a `.env.sample` file as a template. Developers should **copy it to `.env`** and fill in their own values.  
> ⚠️ Never commit the real `.env` file to GitHub — only `.env.sample` should be shared.

---

## Example `.env.sample`

Below is our template with placeholder values:

```text
# -------------------------
# General App Settings
# -------------------------
FLASK_ENV=development              # Flask environment (development/production)
APP_ENV=development                # Custom environment flag
SECRET_KEY=replace_with_secret     # Security key for sessions
JWT_SECRET=replace_with_jwt_secret # Secret key for JWT tokens

# -------------------------
# Database (choose one)
# -------------------------
MONGODB_URI=mongodb://user:pass@localhost:27017/multimed_fusion_db
DATABASE_URL=postgresql://user:pass@localhost:5432/multimed_fusion_db

# -------------------------
# File Storage (AWS S3 or similar)
# -------------------------
S3_BUCKET=your-bucket-name
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
S3_REGION=us-east-1

# -------------------------
# AI Models / APIs
# -------------------------
HUGGINGFACE_API_KEY=hf_xxx
OPENAI_API_KEY=sk-xxx
MODEL_ENDPOINT=http://localhost:8000/predict_summary

# -------------------------
# Audio Transcription
# -------------------------
TRANSCRIBE_API_KEY=your_transcription_service_key

# -------------------------
# DICOM Paths (for medical images)
# -------------------------
DICOM_STORAGE_PATH=/data/dicom
DICOM_TEMP_PATH=/tmp/dicom_processing

# -------------------------
# Background Tasks / Cache
# -------------------------
REDIS_URL=redis://localhost:6379/0
CACHE_EXPIRY=3600                  # Cache expiration time in seconds

# -------------------------
# Logging & Controls
# -------------------------
LOG_LEVEL=INFO
ENABLE_ANONYMIZATION=true
MAX_UPLOAD_SIZE_MB=200
ENABLE_ADMIN_MONITORING=true       # Toggle for health check/monitoring APIs

# -------------------------
# Frontend / CORS Settings
# -------------------------
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# -------------------------
# Email / Notifications
# -------------------------
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your_email@example.com
EMAIL_PASS=your_email_password
