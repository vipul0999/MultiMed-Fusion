# Medical Records Sharing and AI Review System

## Table of Contents
1. [Overview](#overview)
2. [Who This Software Is For](#who-this-software-is-for)
3. [What You Can Do With It](#what-you-can-do-with-it)
4. [Before You Start](#before-you-start)
5. [Installation and Setup](#installation-and-setup)
6. [Logging In and Basic Account Tasks](#logging-in-and-basic-account-tasks)
7. [Doctor Tasks](#doctor-tasks)
8. [Patient Tasks](#patient-tasks)
9. [Administrator Tasks](#administrator-tasks)
10. [Supported File Types](#supported-file-types)
11. [How File Analysis and AI Search Work](#how-file-analysis-and-ai-search-work)
12. [Examples You Can Copy Into Training Material](#examples-you-can-copy-into-training-material)
13. [Screenshot Guide](#screenshot-guide)
14. [Troubleshooting](#troubleshooting)
15. [Quick Glossary](#quick-glossary)
16. [Final Tips](#final-tips)

---

## Overview

This software helps doctors and patients share medical files in a secure and organized way.

It also helps doctors analyze those files and ask questions about them using AI.

In simple terms, it does four main jobs:

1. It creates user accounts for doctors, patients, and admins.
2. It lets a doctor ask for access to a patient’s records.
3. It lets a patient approve or reject that access.
4. It lets files be uploaded, analyzed, and searched.

Think of it like a digital handoff system for medical documents, with an assistant built in to help review the files.

---

## Who This Software Is For

### Patients
Patients can:
- approve or reject doctor access requests
- give access directly to a doctor
- upload files for a doctor
- view upload requests from doctors
- close upload requests after sending files
- revoke access later if needed

### Doctors
Doctors can:
- search for patients
- request access to a patient’s records
- see approved patients
- ask patients to upload files
- upload files for a patient
- list and review patient files
- update a file title, display name, or description
- analyze selected files
- ask questions about uploaded files in plain English

### Administrators
Administrators can:
- view totals for users, files, requests, and AI chunks
- monitor recent system activity
- review access links and upload requests

---

## What You Can Do With It

Here are the key features in plain language.

### Secure sign-in
Users log in with a username and password.
The system uses tokens, which are like temporary digital passes after login.

### Doctor-patient approval flow
A doctor cannot work with a patient’s files until access is approved.
That approval can come from either:
- the patient approving a doctor’s request, or
- the patient granting the doctor access directly

### File uploads
Files can be uploaded by:
- the patient for a doctor
- the doctor for a patient

### File organization
Each uploaded file stores details like:
- original file name
- display name
- title
- description
- upload date
- processing status

### AI-powered review
After files are uploaded, a doctor can analyze them.
The system extracts the text, breaks it into small parts, and prepares it for search.
Then the doctor can ask questions like:
- “What is the diagnosis?”
- “Summarize the patient’s history.”
- “What medications are mentioned?”

### Privacy protections
The system includes privacy-focused behavior such as:
- access approval before file use
- file disposal after revoked access or expired authorization
- anonymized display names for uploaded files

---

## Before You Start

This section is for the person installing or running the project.
If you are only using the software through a website or app, you can skip ahead to [Logging In and Basic Account Tasks](#logging-in-and-basic-account-tasks).

### What you need
- Node 24.0 or later
- Python 3.10 or later
- MongoDB
- the packages listed in `requirements.txt`
- optional AI key for Gemini-based answers
- Tesseract OCR if you want image text extraction



## Installation and Setup

This section explains setup in simple steps.

### 1. Get the project files
Place the project on the machine where you want to run it.

### 2. Create and activate a Python virtual environment
A virtual environment keeps project packages separate from the rest of your system.

Example:
- create the environment
- activate it
- install the required packages

### 3. Install the required packages
Install everything listed in `requirements.txt`.
These include Django, MongoDB support, file-processing tools, and AI-related packages.

Main packages used by this project include:
- Django
- Django REST Framework
- JWT authentication support
- MongoDB backend support
- PDF and DOCX readers
- OCR for images
- audio transcription tools
- Gemini AI integration

### 4. Set environment variables
The project reads settings from environment variables.

Important ones include:
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `MONGODB_URI`
- `MONGODB_NAME`
- `GEMINI_API_KEY` or `GOOGLE_API_KEY`

Example meaning:
- `DJANGO_SECRET_KEY`: secret used by Django for security
- `DJANGO_DEBUG`: turns development debug mode on or off
- `MONGODB_URI`: where MongoDB is running
- `MONGODB_NAME`: database name
- `GEMINI_API_KEY`: lets AI answer questions using Gemini

### 5. Make sure MongoDB is running
The system stores data in MongoDB.
If MongoDB is not running, login, uploads, and analysis will not work.

### 6. Optional: install Tesseract OCR
Tesseract is used to read text from images.
Without it, image uploads may still save, but text extraction from images may fail.

### 7. Run migrations
This creates the needed database structure.

### 8. Start the server
Once setup is complete, start the Django server.

### 9. Open the app or connect the frontend
Open the frontend folder, and type following command to start the frontend server:
```bash
npm run dev
```

### Setup checklist
- [ ] Python installed
- [ ] MongoDB running
- [ ] dependencies installed
- [ ] environment variables set
- [ ] migrations run
- [ ] server started
- [ ] Start frontend server

---

## Logging In and Basic Account Tasks

These are the most common starting tasks for any user.

### Create an account
A new user account needs:
- username
- email
- password
- role

Available roles are:
- `doctor`
- `patient`

> Note: Admin access may be managed internally depending on your setup.

### Log in
A user logs in with:
- username
- password

After login, the system returns access tokens.
These are used to prove the user is signed in.

### View your profile
A signed-in user can view basic account details such as:
- username
- email
- role

### Change your password
To update a password, the user needs:
- current password
- new password

If the current password is wrong, the change will fail.

---

## Doctor Tasks

This section walks through doctor actions one by one.

### 1. Search for a patient
Use the patient search feature to find a patient by:
- username
- email

This helps the doctor find the correct patient before requesting access.

**Simple steps**
1. Open the patient search page.
2. Type part of the patient’s username or email.
3. Review the matching results.
4. Select the correct patient.

**Example**
Search text: `john`
Possible result: `john.doe@example.com`

**Add screenshot here:**
- Screenshot 1: Doctor patient search screen

---

### 2. Request access to a patient’s records
A doctor must request access before viewing or analyzing patient files.

**Simple steps**
1. Find the patient.
2. Click **Request Access**.
3. Add a short note if needed.
4. Submit the request.

**What happens next**
- The request becomes **pending**.
- The patient can approve or reject it.

**Status meanings**
- **pending**: waiting for patient decision
- **approved**: doctor can work with patient files
- **rejected**: patient said no
- **revoked**: access was removed later

**Add screenshot here:**
- Screenshot 2: Doctor request access form

---

### 3. View pending access requests you sent
Doctors can view access requests that are still waiting.

**Simple steps**
1. Open your requests page.
2. Review the list of pending patient requests.
3. Wait for approval, or follow your clinic’s communication process.

---

### 4. View approved patients
Once a patient approves access, the doctor can see that patient in the approved list.

**Simple steps**
1. Open your approved patients list.
2. Select a patient.
3. Open file tools or upload requests for that patient.

---

### 5. Ask a patient to upload files
If the doctor needs reports, scans, or audio notes, the doctor can send an upload request.

**Important rule**
The doctor must already have approved access first.

**Simple steps**
1. Open the approved patient’s page.
2. Click **Request Upload**.
3. Enter a message such as: “Please upload your latest lab results.”
4. Send the request.

**What the patient sees**
The patient will see an open upload request in their request list.

**Add screenshot here:**
- Screenshot 3: Doctor upload request screen

---

### 6. Upload files for a patient
A doctor can also upload files directly for a patient if access is already approved.

**Simple steps**
1. Open the patient record.
2. Click **Upload Files**.
3. Choose one or more supported files.
4. Submit the upload.
5. Wait for the confirmation message.

**What the system saves**
For each file, the system stores details like:
- file type
- upload date
- display name
- title
- description
- processing status

---

### 7. View a patient’s files
After upload, the doctor can list the patient’s files.

**Simple steps**
1. Open the approved patient record.
2. Go to the files section.
3. Review the list.
4. Optionally filter by file type.

**Available file-type filters**
- PDF
- DOCX
- text
- image
- DICOM
- MP3
- WAV

If the doctor does not have approved access, the file list is blocked.

**Add screenshot here:**
- Screenshot 4: Patient file list screen

---

### 8. Update a file name or description
A doctor can improve file labels to make files easier to understand later.

**Fields that can be updated**
- display name
- title
- description

**Simple steps**
1. Open the file details.
2. Edit the title or description.
3. Save the changes.
4. Check for the message: **Update successful**.

**Example**
- Old name: `scan_01.pdf`
- New title: `Cardiology Follow-up Report`
- Description: `Updated after specialist review`

---

### 9. Analyze selected files
This is the step that prepares files for AI search.

**What analyze means**
The system:
1. extracts text from the file
2. cleans sensitive details where needed
3. builds a structured payload
4. breaks the file into smaller chunks
5. creates vector embeddings for search
6. saves those chunks for later questions

A vector embedding is just a numeric way to help the system find similar meaning in text.
You can think of it as a smart search index.

**Simple steps**
1. Open the patient’s file list.
2. Select one or more files.
3. Click **Analyze**.
4. Wait for the success message.
5. Confirm the file shows as processed.

**Success result usually includes**
- patient ID
- doctor ID
- batch hash
- number of chunks created
- any errors
- embedding model used

**If a file fails**
The file may show a failed processing status and an error message such as:
- no text extracted from file
- no chunks generated from file

**Add screenshot here:**
- Screenshot 5: Analyze files screen

---

### 10. Ask questions about patient files
Once files are analyzed, the doctor can ask questions in plain English.

**Examples of good questions**
- What is the diagnosis?
- Summarize the patient’s medical history.
- What medications are listed?
- What follow-up steps are recommended?

**Simple steps**
1. Open the AI question screen.
2. Select the patient.
3. Type your question in English.
4. Optionally choose specific file(s) to search.
5. Click **Ask**.
6. Review the answer, confidence, and source files.

**What the response can include**
- the question you asked
- how many chunks were searched
- the text context used
- a summary answer
- confidence level
- source file links

**Important note**
This system only supports English natural-language queries.
Non-English questions may be rejected.

**Add screenshot here:**
- Screenshot 6: AI query screen with answer and sources

---

### 11. Revoke access
Either the doctor or patient can revoke access later.

**What revoke means**
The access link changes to **revoked**.
Files linked to that doctor-patient relationship may be disposed.
Disposed means the system marks them as no longer available for use.

**Simple steps**
1. Open the doctor-patient access record.
2. Click **Revoke Access**.
3. Confirm the action.
4. Check for the message: **Access revoked**.

**Important effect**
When access is revoked, related files may be disposed automatically.

---

## Patient Tasks

This section explains patient actions in the same simple style.

### 1. View incoming doctor requests
Patients can review pending doctor access requests.

**Simple steps**
1. Open your access requests page.
2. Look for requests marked as pending.
3. Open the doctor request you want to review.

**Add screenshot here:**
- Screenshot 7: Patient incoming requests list

---

### 2. Approve or reject a doctor request
Patients control whether a doctor can access their records.

**Simple steps**
1. Open the pending request.
2. Choose **Approve** or **Reject**.
3. Confirm your choice.

**What happens next**
- If approved, the doctor can view and work with your files.
- If rejected, the doctor cannot proceed.

---

### 3. Grant a doctor access directly
A patient can give access without waiting for a doctor request.

**Simple steps**
1. Open the grant access screen.
2. Choose a doctor.
3. Add a note if you want.
4. Submit.

**Result**
The doctor-patient link is created as approved right away.

---

### 4. View approved doctors
Patients can see which doctors currently have approved access.

**Simple steps**
1. Open your doctors list.
2. Review the approved doctors.
3. Revoke access later if needed.

---

### 5. View file upload requests from doctors
When a doctor asks for files, the patient can see that request.

**Simple steps**
1. Open upload requests.
2. Review open requests.
3. Read the doctor’s message.
4. Upload the requested files.

**Example request message**
“Please upload your latest lab reports.”

**Add screenshot here:**
- Screenshot 8: Patient upload request list

---

### 6. Upload files to a doctor
Patients can upload supported files after doctor access has been approved.

**Important rule**
If access has not been approved yet, the upload will be blocked.

**Simple steps**
1. Open the upload screen.
2. Select the doctor.
3. Choose one or more files.
4. Submit the upload.
5. Wait for the message: **Upload successful**.

**Good to know**
The system may rename the display name to protect personal details.
For example, a file name containing a patient name or date of birth may be masked in the display name.

**Add screenshot here:**
- Screenshot 9: Patient upload screen

---

### 7. Close an upload request after sending files
Once the requested files are uploaded, the patient can close the request.

**Simple steps**
1. Open your upload request list.
2. Find the completed request.
3. Click **Close Request**.
4. Confirm that the request is closed.

---

### 8. Revoke a doctor’s access
Patients can remove access at any time.

**Simple steps**
1. Open the approved doctor list.
2. Select the doctor.
3. Click **Revoke Access**.
4. Confirm the action.

**What happens next**
- the link becomes revoked
- related files may be disposed
- the doctor loses access to that patient’s files

---

## Administrator Tasks

This section is for admin users or internal support teams.

### View dashboard totals
The admin dashboard can show overall counts such as:
- total users
- users by role
- access links by status
- upload requests by open or closed state
- total files
- processed files
- total document chunks

### Review recent activity
The dashboard also provides recent lists for:
- users
- access links
- upload requests
- files
- chunks

### When to use this view
This is helpful for:
- checking if the system is active
- spotting upload problems
- reviewing whether files are being processed
- monitoring doctor-patient relationships

**Add screenshot here:**
- Screenshot 10: Admin dashboard overview

---

## Supported File Types

The system accepts the following file types:

- PDF
- TXT
- DOCX
- PNG
- JPG
- JPEG
- DICOM (`.dcm`)
- MP3
- WAV

### What each one is used for
- **PDF**: reports, summaries, exported documents
- **TXT**: simple notes or plain text records
- **DOCX**: Word documents
- **PNG/JPG/JPEG**: photos, scanned images, screenshots
- **DICOM**: medical imaging files
- **MP3/WAV**: voice notes or audio recordings

If you upload an unsupported format, the system will reject it.

---

## How File Analysis and AI Search Work

This section explains the smart part in plain language.

### Step 1: Text extraction
The system first tries to read text from the file.
Different tools are used for different file types.

Examples:
- PDF reader for PDF files
- Word document reader for DOCX
- OCR for images
- transcription for audio

### Step 2: Privacy cleanup
The system can clean or mask sensitive patient text before saving the processed version.

### Step 3: Structured data
The system builds a machine-readable summary of the extracted content.
This makes future search and analysis easier.

### Step 4: Chunking
Large text is split into smaller parts called chunks.
A chunk is just a small section of text.
This helps the system search more accurately.

### Step 5: Embeddings
Each chunk gets an embedding.
That means it is turned into numbers so the system can compare meaning, not just exact words.

### Step 6: Retrieval
When a doctor asks a question, the system finds the most relevant chunks.
It can search:
- across all files for that patient-doctor pair, or
- only the selected files

### Step 7: AI answer generation
If AI is enabled, the system can use Gemini to turn the matched content into a clearer answer.
The response can also include source links so the doctor can open the original files.

### Important limits
- Questions must be in English.
- AI quality depends on the quality of the uploaded documents.
- Empty or unreadable files may fail during analysis.

---

## Examples You Can Copy Into Training Material

### Example 1: Doctor requests access
**Situation:** A doctor wants to review a patient’s lab results.

**Steps:**
1. Search for the patient.
2. Send an access request.
3. Wait for the patient to approve.
4. Ask the patient to upload the files.

### Example 2: Patient uploads files
**Situation:** A patient receives a request for reports.

**Steps:**
1. Open upload requests.
2. Read the doctor’s message.
3. Upload the requested files.
4. Close the request after upload.

### Example 3: Doctor asks an AI question
**Situation:** Files are already uploaded and analyzed.

**Question:** “Summarize the patient’s medical history.”

**Expected result:**
- a summary answer
- source file links
- confidence level

### Example 4: Update file labels
**Situation:** A file has a confusing name.

**Before:** `scan_01.pdf`

**After:**
- Title: `MRI Follow-up Report`
- Description: `Uploaded after March consultation`

---

## Screenshot Guide

Because this repository is backend-focused, the actual screen images likely live in a separate frontend.
Use this section as a checklist when creating the Word document.

### Recommended screenshots to add
1. Login screen
2. Doctor patient search screen
3. Doctor access request form
4. Patient access approval screen
5. Doctor upload request screen
6. Patient upload screen
7. Patient file list screen
8. File metadata update screen
9. Analyze files screen
10. AI question-and-answer screen
11. Approved doctors list
12. Admin dashboard summary

### Screenshot tips
- highlight the main button in each image
- crop out unrelated screen clutter
- blur any real patient information
- add a one-line caption under each screenshot

**Caption example:**
“Figure 4. The doctor selects files and clicks Analyze to prepare them for AI search.”

---

## Troubleshooting

This section covers common problems in simple language.

### Problem: I cannot log in
**Possible causes**
- wrong username or password
- account does not exist
- backend server is not running

**Try this**
1. re-enter username and password carefully
2. confirm the account was created
3. check that the server is running
4. try logging in again

---

### Problem: Doctor cannot see patient files
**Possible cause**
Access is not approved yet.

**Try this**
1. check whether the doctor-patient relationship is approved
2. if still pending, ask the patient to approve it
3. if revoked, submit a new request or grant access again

---

### Problem: Patient upload is blocked
**Possible cause**
The patient has not granted or approved doctor access yet.

**Try this**
1. confirm the doctor has approved access
2. if not, approve the request or grant access directly
3. upload the file again

---

### Problem: “Patient not found” or “Doctor not found”
**Possible causes**
- wrong ID selected
- target user does not exist
- wrong role selected

**Try this**
1. search again for the correct user
2. confirm the target is a patient or doctor as expected
3. retry the action

---

### Problem: A file upload fails
**Possible causes**
- unsupported file type
- damaged file
- missing permissions

**Try this**
1. confirm the file type is supported
2. try opening the file locally to make sure it is not broken
3. confirm access approval is in place
4. try uploading again

---

### Problem: File analysis fails
**Possible causes**
- no text could be extracted
- the file is empty
- OCR or audio transcription dependency is missing
- the file content is unreadable

**Try this**
1. confirm the file actually contains readable text or speech
2. for images, confirm OCR support is installed
3. for audio, confirm transcription support is available
4. try another file to see if the issue is file-specific

---

### Problem: The AI answer is empty or weak
**Possible causes**
- files were not analyzed yet
- the question is too vague
- the uploaded documents do not contain the answer
- AI key is not configured

**Try this**
1. confirm the file status is processed
2. ask a clearer question
3. limit the query to specific files if needed
4. confirm AI configuration is present if Gemini answers are expected

**Better question examples**
- “What diagnosis is listed in the uploaded report?”
- “What medications are mentioned in the discharge summary?”
- “Summarize the follow-up instructions from the latest PDF.”

---

### Problem: The question is rejected
**Possible cause**
The question is not in English.

**Try this**
Rewrite the question in English and send it again.

---

### Problem: Access was revoked and files disappeared
**Possible cause**
This is expected behavior.
When access is revoked, related files may be disposed automatically.

**Try this**
1. confirm whether access was revoked
2. re-establish approved access if appropriate
3. re-upload files if your process requires it

---

### Problem: Images upload, but no text is found
**Possible cause**
OCR may not be installed or the image quality is poor.

**Try this**
1. install Tesseract OCR
2. use a clearer image
3. make sure the text in the image is readable

---

### Problem: Audio uploads, but no transcript is created
**Possible causes**
- audio is corrupted
- speech is unclear
- transcription support is missing

**Try this**
1. test the audio file locally
2. use a cleaner recording if possible
3. confirm the required audio package is installed correctly

---

## Quick Glossary

### API
A way for one piece of software to talk to another.

### Token
A temporary digital pass that proves a user is signed in.

### OCR
Short for Optical Character Recognition.
It means reading words from an image.

### DICOM
A medical imaging file format.

### Chunk
A small piece of text taken from a larger document.

### Embedding
A numeric form of text used for smart meaning-based search.

### Disposed file
A file that has been marked as no longer available because access expired or was revoked.

---

## Final Tips

- Keep doctor-patient access up to date.
- Use clear file titles and descriptions.
- Analyze files before asking AI questions.
- Ask short, direct questions in English.
- Add screenshots to the final Word version so users can follow along visually.
- Remove or blur any real patient data in screenshots.

If you want, this file can be copied into Microsoft Word and lightly formatted with:
- Heading styles
- automatic table of contents
- numbered figures
- screenshots from your frontend

That will give you a polished user guide that is easy for non-technical people to follow.

