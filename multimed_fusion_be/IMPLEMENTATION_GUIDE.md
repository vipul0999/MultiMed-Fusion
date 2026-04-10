# Chat Query System - Implementation Guide

## Overview
This document describes the rewritten `DoctorChatQueryView` and related services for medical file analysis with semantic search and Gemini AI integration.

## Key Features

### 1. **Per-File Chunking** ✅
- Each file generates its own independent chunks
- No chunks mixing between different files
- Each chunk tracks exactly which file it came from via `source_file_ids` and `source_file_names`
- File-specific hash ensures unique chunk IDs per file

### 2. **Fast File Processing** ✅
- **PDF**: `pypdf` (lightweight, fast)
- **DOCX**: `python-docx` (pure Python, no external dependencies)
- **Audio**: `faster-whisper` (optimized Whisper for CPU, uses INT8 quantization)
- **Images**: `pytesseract` + `Pillow` (OCR with Tesseract, fast on laptops)

### 3. **Advanced Semantic Retrieval** ✅
- Cosine similarity on normalized embeddings
- Filters chunks by specific file IDs (if provided)
- Only returns relevant chunks based on semantic similarity
- Minimum score threshold support

### 4. **Gemini AI Integration** ✅
- Sends retrieved chunks + question to Gemini 2.5 Flash
- Generates contextual answers based only on provided documents
- Privacy-aware: refuses to reveal PII
- Tracks confidence and source documentation

### 5. **File ID Filtering** ✅
- Query can specify `file_ids` parameter
- Only chunks from specified files are retrieved
- Strict filtering - no cross-file retrieval unless explicitly requested

---

## API Endpoint

### POST `/api/files/doctor/chat-query/`

#### Request Body
```json
{
  "patient_id": "<patient_id>",
  "doctor_id": "<doctor_id>",
  "message": "What is the patient's diagnosis?",
  "file_ids": ["<file_id_1>", "<file_id_2>"],  // Optional: filter to specific files
  "top_k": 5  // Optional: number of chunks (default 5, max 20)
}
```

#### Response
```json
{
  "message": "Query processed successfully.",
  "patient_id": "<patient_id>",
  "doctor_id": "<doctor_id>",
  "query": "What is the patient's diagnosis?",
  "chunks_retrieved": 3,
  "chunks": [
    {
      "chunk_id": "abc123:0",
      "chunk_index": 0,
      "score": 0.8456,
      "text": "[SOURCE_FILE=diagnosis.pdf]\n...",
      "source_file_names": ["diagnosis.pdf"],
      "source_file_ids": ["file_id_1"]
    }
  ],
  "context": "Plain text context from chunks...",
  "gemini_response": {
    "success": true,
    "answer": "Based on the provided documents, the patient's diagnosis is...",
    "chunks_used": 3,
    "error": null
  }
}
```

---

## File Processing Pipeline

### 1. Upload & Analysis Flow

**Endpoint**: `POST /api/files/doctor/analyze-files/`

```python
# Request
{
  "patient_id": "<patient_id>",
  "file_ids": ["file_1", "file_2", "file_3"]
}

# Process each file:
# 1. Extract text using fast libraries
# 2. Split into chunks (1200 chars, 200 char overlap)
# 3. Generate embeddings for each chunk
# 4. Store in DB with individual file tracking
```

### 2. Document Structure After Analysis

```
PatientDocChunk
├── chunk_id: "abc123:0" (file-specific hash + index)
├── text: "[SOURCE_FILE=medical_report.pdf]\n..."
├── source_file_ids: ["file_id_1"]  // ✅ Only this file
├── source_file_names: ["medical_report.pdf"]
├── embedding: [0.12, 0.45, ...]  // Vector for similarity
└── embedding_model: "BAAI/bge-small-en-v1.5"
```

### 3. Query & Retrieval Flow

```
User Question
    ↓
Generate Embedding (same model)
    ↓
Search for similar chunks (cosine similarity)
    ↓
Filter by file_ids if provided (strict filtering)
    ↓
Sort by relevance score
    ↓
Return top-k chunks with context
    ↓
Send to Gemini with instructions
    ↓
Return AI-generated answer + source chunks
```

---

## New Files Created

### 1. `medfiles/utils/extract_image.py`
Extract text from images using OCR (Tesseract via pytesseract)

```python
extract_text_from_image(path: str) -> str
```

### 2. `medfiles/services/gemini_service.py`
Handles communication with Gemini API

```python
send_chunks_to_gemini(
    question: str,
    chunks: list[dict],
    model: str = "gemini-2.5-flash",
    api_key_env: str = "GEMINI_API_KEY",
) -> Dict[str, Any]
```

---

## Modified Files

### 1. `medfiles/utils/transcribe_audio.py`
Implemented using faster-whisper (lightweight, CPU-optimized)

### 2. `medfiles/utils/extract_pdf.py` & `extract_docx.py`
Added error handling and cleaner implementation

### 3. `medfiles/utils/extract_text.py`
Added image OCR support alongside existing formats

### 4. `medfiles/utils/retrieval.py`
**Major rewrite** - Added file ID filtering and improved semantic search

```python
top_k_chunks(
    patient_id: str,
    doctor_id: str,
    query: str,
    file_ids: Optional[list[str]] = None,  # NEW: strict file filtering
    k: int = 5,
    min_score: float = -1.0,
) -> list[dict]
```

### 5. `medfiles/services/analyze_files.py`
**Major rewrite** - Per-file chunking instead of batch-based

```python
analyze_and_store_chunks(
    doctor,
    patient,
    files: List[PatientFile]
) -> dict
```

Each file gets unique chunks with individual file tracking.

### 6. `medfiles/services/chat_query.py`
Updated to use new retrieval and Gemini service

### 7. `medfiles/views.py` - `DoctorChatQueryView`
**Complete rewrite** with file filtering and Gemini integration

### 8. `medfiles/serializers.py` - `DoctorChatQuerySerializer`
Added optional `file_ids` field for filtering

### 9. `requirements.txt`
Added new dependencies:
- `faster-whisper==1.0.3` (audio)
- `pytesseract==0.3.10` (OCR)
- `Pillow==10.2.0` (image processing)
- `google-generativeai==0.3.0` (Gemini API)

---

## Chunk ID Structure

### Per-File Basis
```
file_hash = SHA256(filename)[:16]
chunk_id = f"{file_hash}:{chunk_index}"

Example: "abc123def456:0", "abc123def456:1"
         (same file)     (same file, different chunk)
```

### Different Files
```
file_1: "abc123def456:0", "abc123def456:1"
file_2: "xyz789uvw012:0", "xyz789uvw012:1"
```

Each file has its own namespace for chunks.

---

## Example Usage

### Step 1: Upload and Analyze Files
```bash
POST /api/files/doctor/analyze-files/
{
  "patient_id": "patient_1",
  "file_ids": ["file_123", "file_456"]
}
```

Response:
```json
{
  "batch_hash": "abc...",
  "chunks_created": 24,
  "errors": []
}
```

### Step 2: Query with Specific Files
```bash
POST /api/files/doctor/chat-query/
{
  "patient_id": "patient_1",
  "doctor_id": "doctor_1",
  "message": "What medications is the patient taking?",
  "file_ids": ["file_123"],  # Only from this file
  "top_k": 5
}
```

Response:
```json
{
  "chunks_retrieved": 2,
  "chunks": [...],
  "gemini_response": {
    "success": true,
    "answer": "According to the medical report in file_123, the patient is taking..."
  }
}
```

### Step 3: Query All Files
```bash
POST /api/files/doctor/chat-query/
{
  "patient_id": "patient_1",
  "doctor_id": "doctor_1",
  "message": "Summarize the patient's medical history",
  // file_ids omitted - searches across all files
  "top_k": 10
}
```

---

## Configuration

### Environment Variables
```bash
GOOGLE_API_KEY=your_gemini_api_key
# or
GEMINI_API_KEY=your_gemini_api_key

# Optional: Model selection
GEMINI_MODEL=gemini-2.5-flash  # Default
```

### System Requirements
- Python 3.10+
- Tesseract OCR (for image processing)
  - Ubuntu: `sudo apt-get install tesseract-ocr`
  - macOS: `brew install tesseract`
  - Windows: Download installer from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

---

## Chunk Retrieval Strategy

### Semantic Similarity (Cosine)
1. Convert question to embedding using same model
2. Compare with all chunk embeddings
3. Calculate cosine similarity (dot product on normalized vectors)
4. Filter by file_ids if provided
5. Apply minimum score threshold
6. Sort by score (highest first)
7. Return top-k

### Why This Works
- **Accurate**: Embeddings capture semantic meaning
- **Fast**: O(n) complexity, can scale to thousands of chunks
- **Flexible**: File filtering prevents irrelevant results
- **Reliable**: Normalized embeddings ensure consistent similarity scores

---

## Privacy & Safety

### PII Protection
The Gemini prompt includes instructions to refuse revealing:
- Full names
- Phone numbers
- Email addresses
- Social Security Numbers (SSN)
- Physical addresses
- Any other sensitive personal data

### Context Limitation
- Chunks are processed in isolation
- Information from unrelated files won't contaminate results
- Each file has its own namespace of chunks

### Document Verification
- All answers include source file names and chunk IDs
- Medical professionals can verify claim sources
- Traceable audit trail in database

---

## Performance Tips

### For Laptop Deployment
1. **Audio**: Use `faster-whisper` with `base` model (default)
   - CPU-optimized with INT8 quantization
   - ~5-10 seconds per minute of audio

2. **OCR**: Tesseract is fast on CPU
   - Most images process in <1 second
   - Can handle batch processing

3. **Embeddings**: `fastembed` with ONNX runtime
   - Fast inference without GPU
   - Batch processing for efficiency

4. **Chunk Size**: Balanced at 1200 characters
   - Not too small (noisy retrieval)
   - Not too large (lost context)

---

## Troubleshooting

### "No relevant chunks found"
- Verify files were analyzed with `analyze-files` endpoint
- Check file extraction worked (should show in logs)
- Try broader query terms

### Gemini quota exceeded
- Response includes error details
- Falls back to showing chunks without AI answer
- Check API quota at console.cloud.google.com

### OCR not working
- Ensure Tesseract is installed on system
- Set `TESSDATA_PREFIX` if needed

### Audio transcription fails
- Verify audio format is supported (MP3, WAV, M4A, OGG, FLAC)
- Check file permissions
- Try `base` model (faster, more compatible)

---

## Future Enhancements

1. **Hybrid Search**: Combine semantic + BM25 keyword search
2. **MMR (Max Marginal Relevance)**: Reduce duplicate chunk results
3. **Caching**: Cache embeddings for faster retrieval
4. **Custom Models**: Support fine-tuned embeddings
5. **Document QA**: Extract specific fields from documents
6. **Multi-language**: Support non-English documents

---

## API Reference

### `top_k_chunks()`
```python
from medfiles.utils.retrieval import top_k_chunks

chunks = top_k_chunks(
    patient_id="patient_123",
    doctor_id="doctor_456",
    query="Patient's allergies?",
    file_ids=["file_1", "file_2"],  # Optional filter
    k=5,
    min_score=-1.0
)
# Returns: list[dict] with {score, chunk_id, text, source_file_names, ...}
```

### `send_chunks_to_gemini()`
```python
from medfiles.services.gemini_service import send_chunks_to_gemini

result = send_chunks_to_gemini(
    question="What is the diagnosis?",
    chunks=chunks_from_retrieval,
    model="gemini-2.5-flash"
)
# Returns: {ok: bool, answer: str, chunks_used: int, error: str}
```

### `analyze_and_store_chunks()`
```python
from medfiles.services.analyze_files import analyze_and_store_chunks

result = analyze_and_store_chunks(
    doctor=doctor_obj,
    patient=patient_obj,
    files=[file1, file2, file3]
)
# Returns: {batch_hash, chunks_created, errors, embedding_model}
```

---

Generated: February 23, 2026

