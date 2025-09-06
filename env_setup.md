# Environment Setup – `.env.sample`

To make our project easy to configure, we use an environment file called `.env`.  
This file holds important settings such as database connections, storage paths, and API keys.  

We have created a `.env.sample` file as a template. Developers should **copy it to `.env`** and fill in their own values.  
> ⚠️ Never commit the real `.env` file to GitHub — only `.env.sample` should be shared.

---

## Example `.env.sample`

Below is our template with placeholder values:

```text
# General App Settings
FLASK_ENV=development            # Flask environment (development/production)
APP_ENV=development              # Custom environment flag
SECRET_KEY=replace_with_secret   # Security key for sessions

# Database (choose one)
MONGODB_URI=mongodb://user:pass@localhost:27017/multimed_fusion_db
DATABASE_URL=postgresql://user:pass@localhost:5432/multimed_fusion_db

# File Storage (Optional: AWS S3 or similar)
S3_BUCKET=your-bucket-name
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
S3_REGION=us-east-1

# AI Models / APIs
HUGGINGFACE_API_KEY=hf_xxx
OPENAI_API_KEY=sk-xxx
MODEL_ENDPOINT=http://localhost:8000/predict_summary

# Audio Transcription
TRANSCRIBE_API_KEY=your_transcription_service_key

# DICOM Paths (for medical images)
DICOM_STORAGE_PATH=/data/dicom
DICOM_TEMP_PATH=/tmp/dicom_processing

# Background Tasks
REDIS_URL=redis://localhost:6379/0

# Logging & Controls
LOG_LEVEL=INFO
ENABLE_ANONYMIZATION=true
MAX_UPLOAD_SIZE_MB=200
```

---

## Why These Variables Matter

- **App & Security:** `SECRET_KEY` keeps user sessions safe.  
- **Databases:** We included both **MongoDB** and **Postgres** options so developers can choose.  
- **Storage:** `S3_BUCKET` and AWS keys allow storing large medical files like scans and audio securely in the cloud.  
- **AI APIs:** Keys for **Hugging Face** or **OpenAI** allow us to use pre-trained models for summarization.  
- **Transcription:** A placeholder key for audio-to-text services (e.g., Whisper API).  
- **DICOM Paths:** Ensure all medical images are stored and processed in a controlled location.  
- **Background Tasks:** Redis is included in case we want to queue heavy AI tasks.  
- **Controls:** Flags like `ENABLE_ANONYMIZATION` enforce privacy rules before saving data.  

---

## Related Libraries in `requirements.txt`

These environment variables work together with our chosen Python libraries:  

- **Flask / FastAPI** → runs the backend server  
- **python-dotenv** → loads `.env` settings  
- **torch / transformers** → AI model support  
- **pydicom / opencv-python** → handle medical images  
- **spaCy / regex** → anonymize sensitive text  
- **SpeechRecognition / whisper** → convert audio notes into text  
- **pymongo / psycopg2** → connect to MongoDB or PostgreSQL  
- **boto3** → interact with AWS S3 storage  
- **redis / celery** → background task handling  

---

## Usage Instructions

1. Copy `.env.sample` to `.env` in your project folder:  
   ```bash
   cp .env.sample .env
   ```
2. Replace placeholder values with your own (database credentials, API keys).  
3. Run the project; the app will automatically load values from `.env`.  

---

✍️ *This file explains our environment setup in plain language, making it easy for every team member to understand what each variable is for and how it connects to the libraries we use.*
