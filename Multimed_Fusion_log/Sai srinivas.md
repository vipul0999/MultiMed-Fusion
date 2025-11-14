### **Daily Log: September 5, 2025**

#### **Tasks Done:**

* **About the Developers Data Collection**
    * **Description:** Collected personal information, including GitHub usernames, profile links, strengths, and computing interests, from all team members.
    * **Purpose:** To populate the "About the Developers" wiki page as required by the assignment, ensuring each member's contributions are documented.
    * **File:** [wikipage](https://github.com/vipul0999/MultiMed-Fusion/wiki/About-the-developers)

* **Initial Research: Stakeholders & Customers for "Multimed Fusion"**
    * **Description:** Conducted preliminary research on potential stakeholders and end-users for the "Multimed Fusion" project.
    * **Purpose:** To begin identifying the key groups who will be impacted by or will use our product. This research will be crucial for defining project requirements and user stories.
    * **Potential Stakeholders** : Doctors , Physicians , Medical residants , Interns ,Medical Researchers , Lab operaters .
    * **Customers** : Hosiptal Adminstrators , Patients , IT and Data Managers , Government , Manafacturers.
      

      ### **Daily Log: September 8, 2025**

      #**Task- Functional Requirements Draft – Iteration 1**


---

## Requirements  

1. The system **SHALL** allow users to upload medical documents, including lab reports, images, and audio notes.  
2. The system **SHALL** securely store uploaded files in a database or storage system.  
3. The system **SHALL** automatically anonymize patient data (e.g., name, SSN, address) before saving files.  
4. The system **SHALL NOT** store patient-identifiable information in plain text.  
5. The system **SHALL** process uploaded files with an AI engine to generate a consolidated medical summary.  
6. The system **SHALL** include references (links or pointers) back to the original files in the AI-generated summary.  
7. The system **SHALL** provide summaries in a readable format for doctors (structured text or PDF).  
8. The system **SHALL** support multiple file types (e.g., PDF, JPEG, MP3).  
9. The system **SHALL** ensure that uploaded files are only accessible to authorized users.  
10. The system **SHALL** log all file uploads and summary generations for audit purposes.  
11. The system **SHOULD** provide role-based access control (doctor vs. patient).  
12. The system **SHOULD** allow patients to review anonymized files before storage.  
13. The system **SHOULD** provide versioning of summaries when files are re-uploaded or updated.  
14. The system **MAY** allow export of summaries to external systems (EHR/EMR).  
15. The system **MAY** include visualization features for medical images (e.g., highlight key findings).  

---

## References  

- [RFC 2119 – Key words for use in RFCs to Indicate Requirement Levels](https://www.rfc-editor.org/rfc/rfc2119)   
- [HIPAA Privacy Rule (for anonymization requirements)](https://www.hhs.gov/hipaa/for-professionals/privacy/index.html)



  # MultiMed Fusion – Frontend Features

### **Daily Log: September 10, 2025**



* **User Authentication & Access**
  * **Description:** Will implement login, signup, and password reset flows with session timeout handling. Will add role-based dashboards (Doctor / Patient) and multi-factor authentication.  
  * **Purpose:** To ensure secure access and tailored user experiences based on roles.  
  * **Files/Modules (Planned):** `LoginPage.jsx`, `SignupPage.jsx`, `PasswordReset.jsx`, `DashboardRouter.jsx`

---

* **File Upload & Management**
  * **Description:** Will build drag-and-drop file upload for web, camera upload for mobile, and audio recorder integration. Will add support for multi-file upload with progress tracking and a preview modal for PDFs, images, and audio.  
  * **Purpose:** To enable doctors and patients to easily upload and manage lab reports, medical images, and voice notes.  
  * **Files/Modules (Planned):** `UploadComponent.jsx`, `FilePreviewModal.jsx`, `AudioRecorder.jsx`

---

* **Anonymization & Data Privacy**
  * **Description:** Will create an anonymization confirmation screen, automatic removal of PHI (names, IDs, addresses), and a toggle to view/hide sensitive information. Will integrate patient consent UI with digital signatures.  
  * **Purpose:** To protect patient privacy and comply with data protection standards.  
  * **Files/Modules (Planned):** `AnonymizationScreen.jsx`, `PrivacyToggle.jsx`, `ConsentForm.jsx`

---

* **Doctor’s Summary Dashboard**
  * **Description:** Will design a unified AI-generated summary view with expandable sections (labs, imaging, notes) and clickable references to original files. Will integrate a timeline view for patient history and download/export options.  
  * **Purpose:** To help doctors save time while retaining access to detailed reports.  
  * **Files/Modules (Planned):** `SummaryDashboard.jsx`, `SummarySection.jsx`, `TimelineView.jsx`

---

* **Patient Dashboard**
  * **Description:** Will build a secure dashboard for patients to view uploaded history, see anonymization status, access simplified AI summaries, and track access logs. Will enable sharing requests with doctors or caregivers.  
  * **Purpose:** To give patients control and visibility over their medical data.  
  * **Files/Modules (Planned):** `PatientDashboard.jsx`, `AccessLogs.jsx`, `SharingRequest.jsx`

---

* **Collaboration & Communication**
  * **Description:** Will implement doctor-to-doctor notes, secure chat between patients and doctors, and annotation tools for medical images. Will add audio-to-text transcription for notes and team access controls.  
  * **Purpose:** To enable seamless collaboration across medical teams.  
  * **Files/Modules (Planned):** `DoctorNotes.jsx`, `ChatComponent.jsx`, `ImageAnnotation.jsx`

---

* **Notifications & Alerts**
  * **Description:** Will develop push notifications (mobile) and email alerts for new summaries. Will add reminders for pending reviews and urgent flags for critical findings.  
  * **Purpose:** To ensure timely communication of important medical information.  
  * **Files/Modules (Planned):** `NotificationService.js`, `AlertsPanel.jsx`

---

* **Search & Filtering**
  * **Description:** Will build search functionality across all files with filters (file type, date range). Will add AI-powered natural language search (e.g., “latest MRI scan”).  
  * **Purpose:** To allow doctors and patients to quickly locate relevant reports.  
  * **Files/Modules (Planned):** `SearchBar.jsx`, `FilterPanel.jsx`, `SmartSearch.jsx`

---

* **Settings & Preferences**
  * **Description:** Will add dark/light mode toggle, language localization, accessibility controls (font size), and notification preferences. Will integrate profile management for doctors and patients.  
  * **Purpose:** To personalize the app experience for each user.  
  * **Files/Modules (Planned):** `SettingsPage.jsx`, `ProfilePage.jsx`, `ThemeToggle.jsx`

---

* **Mobile-Specific Features**
  * **Description:** Will implement offline mode for cached summaries, biometric login (Face ID/Touch ID), quick uploads from camera and voice recorder, and optimized mobile-friendly summary view.  
  * **Purpose:** To provide a seamless and secure mobile experience.  
  * **Files/Modules (Planned):** `OfflineMode.jsx`, `BiometricAuth.jsx`, `MobileSummaryView.jsx`

---

* **Security & Compliance (Frontend Layer)**
  * **Description:** Will configure session expiry alerts, automatic logout on inactivity, and audit log viewer for doctors/admins. Will add UI indicator for end-to-end encryption and screenshot masking on mobile.  
  * **Purpose:** To align the frontend experience with security and compliance requirements.  
  * **Files/Modules (Planned):** `SecurityBanner.jsx`, `AuditLogs.jsx`, `SessionManager.js`
 

  # MultiMed Fusion – Frontend Features Log

### **Daily Log: September 12, 2025**

---

## **User Authentication & Access**
**Description:** Will implement login, signup, and password reset flows with session timeout handling. Will add role-based dashboards (Doctor / Patient) and multi-factor authentication.  
**Purpose:** To ensure secure access and tailored user experiences based on roles.  
**Files/Modules (Planned):** `LoginPage.jsx`, `SignupPage.jsx`, `PasswordReset.jsx`, `DashboardRouter.jsx`  

---

## **File Upload & Management**
**Description:** Will build drag-and-drop file upload for web, camera upload for mobile, and audio recorder integration. Will add support for multi-file upload with progress tracking and a preview modal for PDFs, images, and audio.  
**Purpose:** To enable doctors and patients to easily upload and manage lab reports, medical images, and voice notes.  
**Files/Modules (Planned):** `UploadComponent.jsx`, `FilePreviewModal.jsx`, `AudioRecorder.jsx`  

---

## **Anonymization & Data Privacy**
**Description:** Will create an anonymization confirmation screen, automatic removal of PHI (names, IDs, addresses), and a toggle to view/hide sensitive information. Will integrate patient consent UI with digital signatures.  
**Purpose:** To protect patient privacy and comply with data protection standards.  
**Files/Modules (Planned):** `AnonymizationScreen.jsx`, `PrivacyToggle.jsx`, `ConsentForm.jsx`  

---

## **Doctor’s Summary Dashboard**
**Description:** Will design a unified AI-generated summary view with expandable sections (labs, imaging, notes) and clickable references to original files. Will integrate a timeline view for patient history and download/export options.  
**Purpose:** To help doctors save time while retaining access to detailed reports.  
**Files/Modules (Planned):** `SummaryDashboard.jsx`, `SummarySection.jsx`, `TimelineView.jsx`  

---

## **Patient Dashboard**
**Description:** Will build a secure dashboard for patients to view uploaded history, see anonymization status, access simplified AI summaries, and track access logs. Will enable sharing requests with doctors or caregivers.  
**Purpose:** To give patients control and visibility over their medical data.  
**Files/Modules (Planned):** `PatientDashboard.jsx`, `AccessLogs.jsx`, `SharingRequest.jsx`  

---

## **Collaboration & Communication**
**Description:** Will implement doctor-to-doctor notes, secure chat between patients and doctors, and annotation tools for medical images. Will add audio-to-text transcription for notes and team access controls.  
**Purpose:** To enable seamless collaboration across medical teams.  
**Files/Modules (Planned):** `DoctorNotes.jsx`, `ChatComponent.jsx`, `ImageAnnotation.jsx`  

---

## **Notifications & Alerts**
**Description:** Will develop push notifications (mobile) and email alerts for new summaries. Will add reminders for pending reviews and urgent flags for critical findings.  
**Purpose:** To ensure timely communication of important medical information.  
**Files/Modules (Planned):** `NotificationService.js`, `AlertsPanel.jsx`  

---

## **Search & Filtering**
**Description:** Will build search functionality across all files with filters (file type, date range). Will add AI-powered natural language search (e.g., “latest MRI scan”).  
**Purpose:** To allow doctors and patients to quickly locate relevant reports.  
**Files/Modules (Planned):** `SearchBar.jsx`, `FilterPanel.jsx`, `SmartSearch.jsx`  

---

## **Settings & Preferences**
**Description:** Will add dark/light mode toggle, language localization, accessibility controls (font size), and notification preferences. Will integrate profile management for doctors and patients.  
**Purpose:** To personalize the app experience for each user.  
**Files/Modules (Planned):** `SettingsPage.jsx`, `ProfilePage.jsx`, `ThemeToggle.jsx`  

---

## **Mobile-Specific Features**
**Description:** Will implement offline mode for cached summaries, biometric login (Face ID/Touch ID), quick uploads from camera and voice recorder, and optimized mobile-friendly summary view.  
**Purpose:** To provide a seamless and secure mobile experience.  
**Files/Modules (Planned):** `OfflineMode.jsx`, `BiometricAuth.jsx`, `MobileSummaryView.jsx`  

---

## **Security & Compliance (Frontend Layer)**
**Description:** Will configure session expiry alerts, automatic logout on inactivity, and audit log viewer for doctors/admins. Will add UI indicator for end-to-end encryption and screenshot masking on mobile.  
**Purpose:** To align the frontend experience with security and compliance requirements.  
**Files/Modules (Planned):** `SecurityBanner.jsx`, `AuditLogs.jsx`, `SessionManager.js`  

---

## **Prototype Image**
Below is the prototype mockup describing all planned frontend features:  

![MultiMed Fusion Frontend Prototype]
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/58f987e6-7e1e-439a-8a0b-be02f31dec93" />


### **Daily Log: September 15, 2025**

# Use Case: Multi Med Fusion

## 1. Goal
The doctor wants to get a quick, accurate summary of a patient's medical history to save time and review all information from various files.

## 2. Actors
- **Primary Actor:** Doctor  
- **System:** The AI Medical Summary Tool  

## 3. Preconditions
- The doctor has an active account and is logged into the system.  
- The patient's medical files (e.g., lab reports, images, audio notes) are available and accessible to the doctor.  
- The system's AI is operational and ready to process new data.  

## 4. Main Flow
1. The doctor navigates to the patient's record.  
2. The doctor selects the medical files to be processed (e.g., uploads new files or selects existing ones from a list).  
3. The doctor clicks the **"Generate Summary"** button.  
4. The system anonymizes the uploaded files by removing patient-identifying information.  
5. The system sends the anonymized files to the AI for analysis.  
6. The AI processes the files and generates a summary.  
7. The system receives the AI-generated summary.  
8. The system displays the summary to the doctor, including links back to the original source files for verification.  

## 5. Postconditions
- An AI-generated summary is successfully created and stored in the patient's record.  
- The original, uploaded files remain anonymized to ensure patient privacy.  

## 6. Alternative and Exception Flows
- **No Files Selected:** The system displays a message, *"Please select one or more files to generate a summary."* The process ends.  
- **File Format Not Supported:** The system alerts the doctor with an error message, *"Unsupported file type. Please upload a lab report, medical image, or audio note."* The process ends.  
- **AI Processing Error:** If the AI fails to generate a summary, the system displays an error message, *"Unable to generate a summary at this time. Please try again later or contact support."*  
- **AI Generates Vague/Incomplete Summary:** The doctor has the option to flag the summary as incomplete or unhelpful. This feedback is logged for future AI model improvement.  

---

### **Daily Log: September 17, 2025**
# MultiMed Fusion – Proposed Prototypes

### Semester Prototype Agreement

This page outlines the list of prototypes that will be developed for **MultiMed Fusion** by the end of this semester. This list serves as an agreement between the development team and the mentor. Each prototype will demonstrate a core aspect of the system and will act as a foundation for further development next semester.

---

## **Prototypes to be Delivered**

### 1. **User Authentication & Access**
- Prototype login and signup pages (Doctor & Patient roles).
- Basic session management and role-based dashboard redirection.
- Password reset workflow (mock, no backend integration yet).

---

### 2. **File Upload & Management**
- Web prototype for uploading files (PDF, image).
- Mobile prototype for camera-based upload (mocked workflow).
- Basic preview of uploaded files (static rendering).

---

### 3. **Anonymization & Privacy Controls**
- Mock anonymization flow (upload → anonymization confirmation screen).
- Toggle to view/hide personally identifiable details (prototype only).

---

### 4. **Doctor’s Summary Dashboard**
- Static dashboard mockup showing unified AI-generated summary.
- Expandable sections for labs, imaging, and notes.
- Clickable placeholders linking back to uploaded files.

---

### 5. **Patient Dashboard**
- Prototype patient-facing dashboard for uploaded files and summaries.
- Privacy indicator showing anonymized files.
- Sharing request mockup for allowing access to doctors.

---

### 6. **Notifications & Alerts**
- Prototype notification panel (UI only).
- Mock push/email alert for new summaries (no live service).

---

### 7. **Search & Filtering**
- Simple prototype search bar with static results.
- Filter panel UI (file type, date range).

---

### 8. **Mobile-Specific Prototype**
- Mobile wireframe showing biometric login (mock only).
- Mobile summary card view optimized for small screens.

---

## **Stretch Goals (If Time Permits)**
- Collaboration mockup: doctor-to-doctor notes and chat UI.  
- Offline mode UI demonstration.  
- Initial localization setup (multi-language toggle).  


---

### **Notes**
- These prototypes are UI/UX only (mockups or limited front-end functionality).  
- Full backend integration, AI summarization, and real anonymization will be addressed in later development cycles.  
- This ensures realistic progress while building a solid foundation for next semester.




# MultiMed Fusion – Daily Log

### **Daily Log: September 19, 2025**

#### ** Models and Pages for a Professional Application**

---

## **Core Models**

1. **User Model**
   - Fields: `id`, `name`, `email`, `role (Doctor/Patient/Admin)`, `passwordHash`, `createdAt`
   - Purpose: Manage authentication and roles.

2. **Patient Model**
   - Fields: `id`, `name`, `dob`, `gender`, `contactInfo`, `medicalHistory`
   - Purpose: Store patient details for doctors’ reference.

3. **Doctor Model**
   - Fields: `id`, `name`, `specialization`, `hospitalAffiliation`, `licenseNumber`
   - Purpose: Manage doctor profiles and credentials.

4. **File Model**
   - Fields: `id`, `patientId`, `fileType (PDF/Image/Audio)`, `filePath`, `uploadedBy`, `uploadedAt`
   - Purpose: Track medical files uploaded by users.

5. **Summary Model**
   - Fields: `id`, `patientId`, `doctorId`, `summaryText`, `createdAt`
   - Purpose: Store AI-generated summaries linked to original files.

6. **Anonymization Model**
   - Fields: `id`, `fileId`, `status (anonymized/pending)`, `removedFields`
   - Purpose: Track privacy compliance.

7. **Notification Model**
   - Fields: `id`, `userId`, `type (email/push)`, `message`, `status`, `createdAt`
   - Purpose: Manage system alerts.

8. **AuditLog Model**
   - Fields: `id`, `action`, `userId`, `timestamp`, `details`
   - Purpose: Track security and compliance events.

---

## **Frontend Pages**

1. **Landing Page**
   - Intro to MultiMed Fusion
   - Login/Signup options

2. **Authentication Pages**
   - Login
   - Signup
   - Password Reset
   - MFA Verification

3. **Doctor Dashboard**
   - Summary view (labs, images, notes)
   - Timeline view
   - File references
   - Notifications

4. **Patient Dashboard**
   - Uploaded files list
   - Privacy indicator (anonymized status)
   - AI summaries (simplified language)
   - Sharing requests

5. **File Management Pages**
   - Upload (drag-drop, camera, audio)
   - File preview (PDF, image, audio player)

6. **Anonymization Pages**
   - Anonymization confirmation
   - Toggle sensitive data on/off
   - Patient consent page

7. **Collaboration Pages**
   - Doctor-to-doctor notes
   - Chat interface
   - Image annotation tools

8. **Search & Filter Page**
   - Search bar with AI-assisted queries
   - Filters (file type, date, doctor)

9. **Notifications Page**
   - Alerts for new summaries
   - Critical flags

10. **Settings Page**
    - Profile management
    - Dark/Light mode
    - Language localization
    - Notification preferences

11. **Mobile-Specific Views**
    - Biometric login
    - Mobile-friendly summary cards
    - Offline mode

12. **Admin Pages (Future)**
    - Audit logs viewer
    - System monitoring

---

## **Purpose**
This structure of **models + pages** ensures:
- Scalable backend with proper data models.
- Professional, user-friendly frontend for doctors and patients.
- Compliance-ready features (privacy, security, audit logs).
- A clear roadmap for incremental feature delivery.

---


### **Daily Log: September 22 , 2025**
### **Backend Features & Technologies**

The backend is the brain of the application, handling all the logic, data processing, and security.

* **RESTful API:** The core of the backend is a RESTful API built to handle requests from the frontend. This API will manage user authentication, file uploads, AI processing triggers, and data retrieval.
* **Microservices Architecture:** To ensure scalability and maintainability, the backend can be broken down into specialized services:
    * **User Service:** Handles user authentication, profile management, and role-based access control (doctor, admin).
    * **File Upload Service:** Manages secure file uploads, validation, and storage. It will be responsible for sending files to the Anonymization Service.
    * **Anonymization Service:** A dedicated service that uses a library or AI to identify and remove PII from the uploaded medical documents.
    * **AI Processing Service:** Triggers the AI model to analyze the anonymized files and generate a summary. This service can be an isolated environment to handle the computational load.
    * **Data Service:** Manages the database, handling all read and write operations for patient records, summaries, and file metadata.
* **Technology Stack:**
    * **Backend Framework:** Python with **Django** or **Flask** for rapid development and extensive library support.
    * **Database:** **PostgreSQL** is a great choice for its robust support for structured and unstructured data, ensuring data integrity and security.
    * **AI/ML:** **TensorFlow** or **PyTorch** can be used to build and deploy the custom AI model for summarization. Pre-trained models like **GPT-3** or similar large language models can be used via their APIs, trained on medical data to improve accuracy.
    * **File Storage:** **Amazon S3** or **Google Cloud Storage** for secure and scalable storage of encrypted medical files.
    * **Task Queue:** **Celery** with **Redis** to manage background tasks like file anonymization and AI processing, preventing the user interface from freezing during long operations.

---

### **Data Models**

The database schema is the blueprint for how data is stored and organized.

* **`User` Model:**
    * `id` (Primary Key)
    * `username` (string, unique)
    * `password_hash` (string)
    * `email` (string, unique)
    * `is_doctor` (boolean)
    * `created_at` (datetime)
* **`Patient` Model:**
    * `id` (Primary Key)
    * `doctor_id` (Foreign Key to `User`)
    * `anonymized_id` (string, unique, generated by the system)
    * `created_at` (datetime)
* **`File` Model:**
    * `id` (Primary Key)
    * `patient_id` (Foreign Key to `Patient`)
    * `file_name` (string)
    * `file_type` (string, e.g., 'PDF', 'DICOM', 'MP3')
    * `storage_url` (string, a link to the encrypted file in S3)
    * `is_anonymized` (boolean, defaults to False)
    * `upload_date` (datetime)
* **`Summary` Model:**
    * `id` (Primary Key)
    * `patient_id` (Foreign Key to `Patient`)
    * `summary_text` (text)
    * `source_files` (JSON array of `File` IDs)
    * `created_at` (datetime)

---

### **Web Pages**

These are the user-facing parts of the application, designed to be simple and intuitive.

* **1. Login/Authentication Page:**
    * **Purpose:** Allows doctors to securely log in or register.
    * **Inputs:** Username/email and password.
    * **Logic:** Validates credentials against the `User` model. If successful, redirects to the Dashboard.
* **2. Doctor Dashboard Page:**
    * **Purpose:** The main hub for the doctor, providing an an overview of their patients.
    * **Content:** A list of the doctor's patients, with options to add a new patient or view an existing one.
* **3. Patient Profile Page:**
    * **Purpose:** Displays all information and files for a single patient.
    * **Sections:**
        * **Patient Details:** Anonymized patient ID.
        * **Summary Section:** Displays the latest AI-generated summary with a button to generate a new one. Links within the summary will allow the doctor to view the original source files.
        * **File Upload Section:** A drag-and-drop or browse interface for uploading new medical files.
        * **File List:** A list of all uploaded files for the patient, showing their status (e.g., 'Anonymized', 'Processing', 'Summary Generated').
* **4. Summary View Page:**
    * **Purpose:** Dedicated page to display a single, full-text summary with a clean, readable layout.
    * **Content:** The full summary text and clickable links to the source files, enabling quick verification.
* **5. Settings Page:**
    * **Purpose:** Allows the doctor to manage their profile and account settings.
    * **Features:** Change password, update email, and potentially manage notification preferences.

# MultiMed Fusion – Requirement Engineering Daily Log

---

### **Daily Log: September 26, 2025**

## **Day 1 – Requirement Elicitation**
- **Tasks:**
  - Conducted stakeholder interviews (doctors, patients, hospital IT staff).
  - Reviewed existing medical systems for pain points.
  - Identified key user needs: faster summaries, data privacy, multi-modal support.
- **Outputs:**
  - Initial user stories (Doctor → “I want a single summary”, Patient → “I want anonymized data”).
  - Stakeholder list: Doctors, Patients, Hospital Admins, Researchers, IT Managers.

---

## **Day 2 – Requirement Analysis**
- **Tasks:**
  - Classified requirements into **Functional** and **Non-Functional**.
  - Resolved conflicts (Doctors want full details, Patients want anonymization).
  - Created priority levels (High: Authentication, Upload, Summary; Medium: Collaboration, Notifications).
- **Outputs:**
  - Requirement categories table.
  - Preliminary system scope defined.

---

## **Day 3 – Requirement Specification**
- **Tasks:**
  - Wrote Software Requirement Specification (SRS) draft in structured format.
  - Converted user stories into use cases.
  - Added acceptance criteria for each use case.
- **Outputs:**
  - **Functional Requirements**: Auth, Upload, Anonymization, Summarization, Dashboards, Search.
  - **Non-Functional Requirements**: Security, Privacy, Scalability, Usability, Performance.
  - UML Use Case Diagram (planned).

---

## **Day 4 – Requirement Validation**
- **Tasks:**
  - Conducted walkthrough session with mentor.
  - Validated feasibility of prototypes with available tools (React, Django, FastAPI).
  - Checked compliance with privacy regulations (HIPAA-style anonymization).
- **Outputs:**
  - Reviewed requirements checklist.
  - Approval for Semester Prototype Plan.

---

## **Day 5 – Requirement Management**
- **Tasks:**
  - Set up GitHub Wiki for living requirement document.
  - Linked “Prototypes Agreement” page from the main repo.
  - Created change log format for tracking evolving requirements.
- **Outputs:**
  - Requirement traceability matrix (RTM) structure.
  - Wiki page update: [Requirements Page](https://github.com/your-username/MultiMed-Fusion/wiki/Requirements)

---

## **Purpose**
This daily requirement engineering log ensures:
- Continuous alignment between stakeholders and developers.  
- A professional, traceable process of requirement gathering.  
- A realistic scope for semester prototypes.  

---




---

### **Daily Log: September 24, 2025**

## **Planned Full Interface **

---

### 1. **Landing Page**
- Entry page with project branding and navigation.
- Includes login and signup buttons.
- Provides a short overview of MultiMed Fusion.

---

### 2. **Authentication Pages**
- **Login:** Email, password, and MFA code entry.  
- **Signup:** Name, email, password, and role selection (Doctor/Patient).  
- **Password Reset:** Input email to receive reset instructions.  

---

### 3. **Doctor Dashboard**
- AI-generated medical summary.  
- Expandable sections for labs, imaging, and notes.  
- Patient history timeline.  
- Quick access links to original files.  
- Notifications panel for new reports.  

---

### 4. **Patient Dashboard**
- List of uploaded files.  
- Privacy indicator showing anonymized status.  
- Simplified summaries in patient-friendly language.  
- Option to share access with doctors or caregivers.  

---

### 5. **File Upload Page**
- Drag-and-drop upload feature for web.  
- Camera and audio upload for mobile.  
- Progress bar for uploads.  
- File preview (PDF, image, audio).  

---

### 6. **Anonymization Page**
- Confirmation screen before saving files.  
- Toggle to anonymize data (hide PHI).  
- Patient consent form (digital signature).  

---

### 7. **Collaboration Page**
- Doctor-to-doctor notes.  
- Secure chat between patients and doctors.  
- Image annotation tools.  
- Audio-to-text transcription for notes.  

---

### 8. **Search & Filter Page**
- Search bar for quick queries.  
- Filters for file type and date range.  
- AI-powered natural language search (e.g., “latest MRI scan”).  

---

### 9. **Notifications Panel**
- Alerts for new summaries.  
- Reminders for pending reviews.  
- Urgent flags for critical findings.  

---

### 10. **Settings Page**
- Profile management (doctor and patient).  
- Dark/Light mode toggle.  
- Language localization options.  
- Notification preferences.  
- Accessibility controls (font size, color contrast).  

---

### 11. **Mobile-Specific Views**
- Biometric login (Face ID/Touch ID).  
- Mobile-optimized summary cards.  
- Offline mode to view cached summaries.  

---

### 12. **Admin & Security Pages (Future)**
- Audit log viewer for administrators.  
- System monitoring tools.  
- Access control management.  
- Indicators for encryption and compliance.  

---

## **Purpose**
This daily log defines the **entire planned interface** of MultiMed Fusion in text format.  
It serves as a blueprint for building both the **web** and **mobile applications** in a professional and structured way.  

---

# MultiMed Fusion – Non-Functional Requirements Daily Log

---

### **Daily Log: September 29, 2025**

## **Identified Non-Functional Requirements**

---

### 1. **Performance**
- The system shall generate AI summaries within **5 seconds** for average-sized files.  
- File uploads shall support up to **100 MB per file** without timeouts.  
- The mobile app shall load the dashboard in under **2 seconds** on 4G networks.  

---

### 2. **Scalability**
- The system shall support **up to 10,000 concurrent users** without performance degradation.  
- Cloud infrastructure shall allow scaling of storage and processing on demand.  

---

### 3. **Security**
- All communication shall be **encrypted (HTTPS, TLS 1.2+)**.  
- User sessions shall expire automatically after **15 minutes of inactivity**.  
- The system shall support **multi-factor authentication (MFA)**.  
- Sensitive data (patient PHI) shall never be displayed without anonymization toggle.  

---

### 4. **Privacy & Compliance**
- All uploaded files shall be anonymized before storage.  
- The system shall comply with **HIPAA-style standards** for handling medical data.  
- Patient consent shall be required before any data sharing.  

---

### 5. **Usability**
- Interfaces shall be **intuitive and consistent** across web and mobile.  
- The system shall provide **multi-language support** (English, Spanish, others in future).  
- Accessibility features shall include **screen reader compatibility, adjustable font sizes, and high-contrast mode**.  

---

### 6. **Reliability & Availability**
- The system shall provide **99.9% uptime** during semester prototype testing.  
- Summaries and files shall be cached locally to handle temporary outages.  
- System shall auto-recover from crashes without data loss.  

---

### 7. **Maintainability**
- Codebase shall follow **modular architecture** (separating frontend, backend, AI services).  
- Documentation shall be maintained in the GitHub wiki for every release.  
- Unit tests shall cover at least **70% of frontend and backend modules**.  

---

### 8. **Portability**
- The application shall run on **modern web browsers (Chrome, Firefox, Safari, Edge)**.  
- Mobile app shall support **iOS 15+ and Android 11+**.  
- Deployment shall be containerized using **Docker** for portability.  

---

## **Purpose**
This daily log documents the **non-functional requirements (NFRs)** of MultiMed Fusion.  
It ensures the project is not only feature-complete (functional requirements) but also professional, secure, scalable, and user-friendly.  

---

# MultiMed Fusion – Use Case Daily Log

---

### **Daily Log: October 1, 2025**

## **Use Cases Matching Functional Requirements**

---

### 1. **User Authentication & Access**
- **Actors:** Doctor, Patient, System  
- **Description:** A user logs in or signs up to access the system. The system verifies credentials and redirects based on role.  
- **Precondition:** User must have valid account or register successfully.  
- **Postcondition:** User is authenticated and granted access to their dashboard.  

---

### 2. **File Upload & Management**
- **Actors:** Doctor, Patient  
- **Description:** A user uploads medical files (PDFs, images, audio). System stores and prepares them for processing.  
- **Precondition:** User is logged in.  
- **Postcondition:** Files are uploaded, stored securely, and ready for processing.  

---

### 3. **Anonymization of Patient Data**
- **Actors:** Patient, System  
- **Description:** System anonymizes uploaded files to remove PHI before storage.  
- **Precondition:** File is uploaded.  
- **Postcondition:** An anonymized copy is stored, ensuring privacy compliance.  

---

### 4. **AI Summary Generation**
- **Actors:** Doctor, System  
- **Description:** System generates an AI summary of uploaded files and provides links back to originals.  
- **Precondition:** Files are uploaded and processed.  
- **Postcondition:** Summary is displayed on the doctor’s dashboard.  

---

### 5. **Doctor’s Summary Dashboard**
- **Actors:** Doctor  
- **Description:** Doctor views AI-generated summary, explores sections (labs, imaging, notes), and accesses original files.  
- **Precondition:** AI summary is available.  
- **Postcondition:** Doctor saves time by reviewing summarized results.  

---

### 6. **Patient Dashboard**
- **Actors:** Patient  
- **Description:** Patient views uploaded history, simplified summaries, and anonymization status.  
- **Precondition:** Patient has uploaded files or received summaries.  
- **Postcondition:** Patient can understand medical history in simplified form.  

---

### 7. **Notifications & Alerts**
- **Actors:** Doctor, Patient, System  
- **Description:** System notifies users of new summaries, urgent findings, or pending reviews.  
- **Precondition:** User is logged in.  
- **Postcondition:** User is informed and takes necessary action.  

---

### 8. **Search & Filtering**
- **Actors:** Doctor, Patient  
- **Description:** User searches for medical records using keywords, filters, or natural language queries.  
- **Precondition:** Files/summaries are available in the system.  
- **Postcondition:** Search results are displayed with relevant filters applied.  

---

### 9. **Collaboration & Communication**
- **Actors:** Doctor, Patient  
- **Description:** Doctors exchange notes, annotate medical images, and chat securely with patients.  
- **Precondition:** Users are logged in with correct permissions.  
- **Postcondition:** Communication is logged securely, aiding collaboration.  

---

### 10. **Settings & Preferences**
- **Actors:** Doctor, Patient  
- **Description:** User customizes profile, themes, language, and notification preferences.  
- **Precondition:** User is authenticated.  
- **Postcondition:** Preferences are applied to enhance user experience.  

---

## **Purpose**
This daily log captures the **use cases directly mapped to functional requirements** of MultiMed Fusion.  
It ensures **traceability** between what the system is expected to do (requirements) and how users will interact with it (use cases).  

---

# MultiMed Fusion – Use Case Daily Log

---

### **Daily Log: October 3 , 2025**

## **List of Use Cases**

---

### **UC-01: User Authentication & Access**
- **Actors:** Doctor, Patient, System  
- **Description:** A user signs up or logs in with role-based access.  
- **Precondition:** User provides valid credentials.  
- **Postcondition:** User is redirected to the appropriate dashboard.  

---

### **UC-02: File Upload**
- **Actors:** Doctor, Patient  
- **Description:** Upload medical files (PDF, image, audio) via web or mobile.  
- **Precondition:** User is logged in.  
- **Postcondition:** File is stored and available for processing.  

---

### **UC-03: Data Anonymization**
- **Actors:** Patient, System  
- **Description:** System removes personally identifiable information (PHI).  
- **Precondition:** File uploaded.  
- **Postcondition:** Anonymized file stored securely.  

---

### **UC-04: AI Summary Generation**
- **Actors:** Doctor, System  
- **Description:** System generates a summary from multiple uploaded files.  
- **Precondition:** Files are uploaded and processed.  
- **Postcondition:** Doctor sees unified AI-generated summary with links to originals.  

---

### **UC-05: Doctor Dashboard**
- **Actors:** Doctor  
- **Description:** Doctor views summaries, expandable details, timeline view.  
- **Precondition:** Summaries are available.  
- **Postcondition:** Doctor reviews patient information efficiently.  

---

### **UC-06: Patient Dashboard**
- **Actors:** Patient  
- **Description:** Patient views their uploaded files and simplified summaries.  
- **Precondition:** Patient account exists with files uploaded.  
- **Postcondition:** Patient accesses history and summaries.  

---

### **UC-07: Notifications & Alerts**
- **Actors:** Doctor, Patient, System  
- **Description:** System sends alerts for new summaries, urgent findings, and pending reviews.  
- **Precondition:** System processes files or detects events.  
- **Postcondition:** User receives timely notification.  

---

### **UC-08: Search & Filtering**
- **Actors:** Doctor, Patient  
- **Description:** Search across files using keywords, filters, or natural language queries.  
- **Precondition:** Files and summaries exist in the system.  
- **Postcondition:** User retrieves relevant search results.  

---

### **UC-09: Collaboration & Communication**
- **Actors:** Doctor, Patient  
- **Description:** Secure chat, notes sharing, and annotation tools for medical images.  
- **Precondition:** Users logged in with permissions.  
- **Postcondition:** Notes/annotations saved and shared securely.  

---

### **UC-10: Settings & Preferences**
- **Actors:** Doctor, Patient  
- **Description:** Manage profile, language, theme, notification preferences.  
- **Precondition:** User is authenticated.  
- **Postcondition:** Settings saved and applied to UI.  

---

### **UC-11: Mobile-Specific Features**
- **Actors:** Doctor, Patient  
- **Description:** Biometric login, offline mode, mobile-optimized summary cards.  
- **Precondition:** User has mobile app.  
- **Postcondition:** User securely accesses features on mobile.  

---

### **UC-12: Admin & Security (Future)**
- **Actors:** Admin, System  
- **Description:** Admin views audit logs and manages user access.  
- **Precondition:** Admin role required.  
- **Postcondition:** Compliance and security verified.  

---

## **Purpose**
This daily log captures the **complete list of use cases** mapped to the functional requirements of MultiMed Fusion.  
It ensures **traceability** and provides a foundation for building **UML Use Case Diagrams**.  

---
# MultiMed Fusion – Data Management Plan  
### **Daily Commit Log: October 5, 2025**

---

## **1. Data Summary**

The MultiMed Fusion platform will manage medical information uploaded by doctors and patients.  
This data will include text files, lab reports, images, and audio notes — all anonymized and stored securely.

Below is a simplified, human-friendly summary of the data to be stored (from the ER Diagram):

| **Entity** | **Description** | **Key Fields** |
|-------------|-----------------|----------------|
| **User** | Stores doctor and patient login information | user_id, name, email, role, password_hash, created_at |
| **Doctor** | Stores doctor-specific information | doctor_id, user_id (FK), specialization, hospital_affiliation |
| **Patient** | Stores patient profile and demographics | patient_id, user_id (FK), dob, gender, contact_info, medical_history |
| **File** | Stores uploaded medical files | file_id, patient_id (FK), file_name, file_type, upload_path, uploaded_by, uploaded_at |
| **Anonymization** | Tracks PHI removal and data privacy | anon_id, file_id (FK), status, removed_fields, verified_by |
| **Summary** | AI-generated medical summaries | summary_id, patient_id (FK), doctor_id (FK), summary_text, created_at |
| **Notification** | Stores alerts sent to users | notif_id, user_id (FK), type, message, status, created_at |
| **Chat / Notes** | Manages collaboration messages between doctors/patients | chat_id, sender_id, receiver_id, message, timestamp |
| **Audit Log** | Records all security events | log_id, user_id (FK), action, timestamp, details |

---

## **2. ER Diagram Overview**

**Description:**  
The system follows a **relational database model (PostgreSQL / MySQL)**, linking key entities (Users, Patients, Doctors, Files, Summaries, Notifications, Logs) through primary and foreign keys.

**Core Relationships:**
- A **User** can be either a Doctor or a Patient (1–1 relationship).  
- A **Patient** can have multiple **Files** and **Summaries** (1–M).  
- A **Doctor** can create multiple **Summaries** for different Patients (1–M).  
- Each **File** has one **Anonymization record** (1–1).  
- A **User** can receive many **Notifications** (1–M).  
- All user activities are tracked through **Audit Logs**.

---

## **3. Data Security Plan**

### **Access Restriction**
- Role-based access control (RBAC):  
  - Doctors can view and summarize patient files assigned to them.  
  - Patients can view only their own anonymized data.  
  - Admins can view system logs but not medical content.  
- Access permissions validated through API middleware before every database request.

### **Encryption**
- All user credentials stored using **bcrypt password hashing**.  
- Sensitive data (patient details, files, summaries) encrypted at rest using **AES-256**.  
- All communication (frontend ↔ backend ↔ storage) via **HTTPS (TLS 1.2+)**.  
- File storage (S3 or similar) configured with encryption and signed URLs.

### **Data Backup & Recovery**
- Daily automated backups of all databases.  
- Redundant file storage for recovery from system failures.  
- Audit trails for every data modification.

---

## **4. Mapping Functional Requirements to Data Storage**

| **Functional Requirement** | **Related Data Entities** | **Storage Description** |
|-----------------------------|----------------------------|--------------------------|
| User Authentication & Access | User | Stores credentials, roles, timestamps |
| File Upload & Management | File, Patient, Doctor | Stores uploaded file metadata, linked to patient/doctor |
| Data Anonymization | Anonymization, File | Tracks PHI removal and anonymization status |
| AI Summary Generation | Summary, File | Stores generated text summaries linked to original data |
| Doctor Dashboard | Summary, Patient | Displays summaries and links to patient data |
| Patient Dashboard | Patient, File, Summary | Displays history and anonymization info |
| Notifications & Alerts | Notification | Stores messages and alerts for users |
| Collaboration & Chat | Chat / Notes, User | Manages secure messaging between doctors and patients |
| Security & Compliance | Audit Log, User | Records all actions and changes for accountability |

---

## **5. Summary**

This **Data Management Plan** defines how MultiMed Fusion will:
- Collect, store, and secure sensitive medical information.
- Maintain privacy through anonymization and encryption.
- Ensure traceability between stored data and system functionalities.

This document serves as the **foundation for database design and implementation** during the next development phase.

---



# MultiMed Fusion – Non-Functional Requirements Daily Log

---

### **Daily Log: October 8, 2025**

## **Purpose**
The goal of this daily log is to describe the **Non-Functional Requirements I-2 (NFRs)** that define how the MultiMed Fusion system should perform, operate, and maintain quality.  
While functional requirements specify *what* the system does, these NFRs define *how well* it performs those functions.

---

## **1. Performance Requirements**
- The system should process uploaded medical files and generate AI summaries within **5 seconds** for average file sizes (≤ 25MB).  
- The web and mobile dashboards must load in **under 3 seconds** under normal load.  
- The backend should handle **up to 10 concurrent summary requests per doctor** without latency above 2 seconds.  
- The database must execute queries and return results within **1 second** for 95% of requests.  
- Upload and download operations must maintain stable performance across different file types (PDF, image, audio).  

---

## **2. Scalability Requirements**
- The architecture must support scaling from **hundreds to thousands of users** with minimal reconfiguration.  
- Horizontal scaling of the backend (using FastAPI/Django) should be supported through containerization (Docker, Kubernetes).  
- File storage should be **cloud-based (AWS S3 or equivalent)** to handle increasing medical data.  
- AI summary generation services should scale independently of other modules using microservice design.  

---

## **3. Security Requirements**
- All data transmission shall occur over **HTTPS (TLS 1.2 or higher)**.  
- Passwords must be stored using **bcrypt or Argon2 hashing**.  
- Patient data and medical records shall be **encrypted at rest (AES-256)**.  
- Sessions should expire automatically after **15 minutes of inactivity**.  
- Role-based access control (RBAC) shall restrict data visibility based on user type (Doctor, Patient, Admin).  
- Multi-factor authentication (MFA) shall be implemented for doctors and admins.  

---

## **4. Privacy & Compliance Requirements**
- The system must comply with **HIPAA-like privacy standards** for data protection.  
- Personal Health Information (PHI) must be anonymized before storage or processing.  
- Access to patient data must require explicit consent (digital approval).  
- Data logs and audit trails must be maintained for accountability.  

---

## **5. Usability Requirements**
- The system interface should be **intuitive, clean, and user-friendly** for non-technical users.  
- The design shall maintain **consistency across web and mobile platforms**.  
- Accessibility features:  
  - Support for screen readers (ARIA labels).  
  - Adjustable font size and high-contrast themes.  
  - Keyboard navigation support.  
- The app shall support **multi-language localization (English, Spanish)** in future updates.  

---

## **6. Reliability & Availability Requirements**
- The system shall achieve **99.9% uptime** during active deployment.  
- It must gracefully handle network interruptions (offline caching for mobile users).  
- Auto-retry mechanisms should ensure file uploads resume after disconnection.  
- Backup services should run daily, ensuring recovery within **30 minutes** in case of data loss.  
- Any failed service (e.g., summary generation) should be automatically restarted by a monitoring tool.  

---

## **7. Maintainability Requirements**
- The project shall follow **modular and component-based architecture**.  
- Code must adhere to **PEP8 (Python)** and **ESLint (React)** style guidelines.  
- Documentation must be updated with each major commit in the GitHub Wiki.  
- Unit and integration tests should cover at least **70% of all modules**.  
- CI/CD pipelines will automate testing and deployment (GitHub Actions).  

---

## **8. Portability Requirements**
- The system should be deployable on multiple environments (AWS, Azure, GCP, local).  
- Docker containers will be used to ensure portability and consistency.  
- The frontend must work on **major browsers** (Chrome, Firefox, Safari, Edge).  
- The mobile app must support **Android 11+** and **iOS 15+**.  

---

## **9. Interoperability Requirements**
- The system must integrate smoothly with third-party AI and transcription APIs.  
- Export formats must include **PDF**, **TXT**, and **JSON** for data exchange.  
- RESTful APIs should follow **OpenAPI standards** for future scalability and interoperability.  

---

## **10. Auditability & Logging**
- Every critical action (upload, summary creation, data deletion) must be logged.  
- Logs should include user ID, timestamp, and activity type.  
- Logs will be stored securely and monitored for suspicious activity.  
- Admin users can view system audit trails via the Audit Dashboard.  

---

### **Conclusion**
These **Non-Functional Requirements** ensure that MultiMed Fusion is not only feature-complete but also **secure, fast, maintainable, scalable, and compliant** with medical data standards.  
They set clear expectations for performance and quality throughout the system’s lifecycle.  

# MultiMed Fusion – iOS Application Development Methodology Log

---

### **Daily Log: October 10, 2025**



## **1. Planning & Setup**
- **Tasks:**
  - Installed and configured **Xcode 16.0** environment.  
  - Created a new project named `MultiMedFusion_iOS` using the **Storyboard** interface and **Swift** language.  
  - Set the **minimum deployment target to iOS 15.0** for compatibility.  
  - Defined project folder structure:  
    - `Model/` – Data models  
    - `View/` – Storyboard UI layouts  
    - `Controller/` – ViewControllers  
    - `Services/` – API calls, authentication, and AI summary services  

- **Purpose:**  
  To establish a clean and scalable base structure for development.

---

## **2. UI/UX Design Phase**
- **Tasks:**
  - Designed main screens in Storyboard:  
    - Login Screen  
    - Signup Screen  
    - Dashboard (Doctor & Patient Views)  
    - File Upload Screen  
    - Summary View Screen  
    - Settings Screen  
  - Used **Auto Layout** and **Stack Views** to ensure responsiveness on different devices.  
  - Applied consistent **color palette and font hierarchy** following Apple’s Human Interface Guidelines.  

- **Purpose:**  
  To create a clean, accessible, and user-friendly interface.

---

## **3. Model Development**
- **Tasks:**
  - Defined Swift data models:  
    - `User`, `Patient`, `Doctor`, `File`, `Summary`, and `Notification`.  
  - Used `Codable` protocol for JSON encoding/decoding with API integration.  
  - Established sample mock data for testing during early stages.  

- **Purpose:**  
  To handle structured data efficiently within the app.

---

## **4. Controller & Business Logic Implementation**
- **Tasks:**
  - Created ViewControllers:  
    - `LoginViewController`, `SignupViewController`, `DashboardViewController`, `UploadViewController`, `SummaryViewController`, `SettingsViewController`.  
  - Connected **IBOutlets** and **IBActions** between UI and code.  
  - Implemented local data validation and navigation between screens using `UINavigationController`.  
  - Integrated mock backend responses for AI summaries.  

- **Purpose:**  
  To implement navigation flow and app logic based on the functional requirements.

---

## **5. API Integration**
- **Tasks:**
  - Created **APIService.swift** to handle REST API communication (with Django/FastAPI backend).  
  - Configured network calls using **URLSession**.  
  - Managed authentication tokens for secure data requests.  
  - Implemented upload and summary endpoints for testing (mock mode initially).  

- **Purpose:**  
  To connect the mobile frontend with backend services securely.

---

## **6. Data Persistence**
- **Tasks:**
  - Integrated **Core Data** for offline storage of summaries and uploaded file metadata.  
  - Configured local caching to access summaries when offline.  
  - Added data synchronization when the network is restored.  

- **Purpose:**  
  To ensure reliability and smooth user experience even in offline mode.

---

## **7. Security Implementation**
- **Tasks:**
  - Enabled **Face ID / Touch ID** authentication using `LocalAuthentication` framework.  
  - Secured API keys and tokens using **Keychain Services**.  
  - Implemented session timeout and logout after inactivity.  
  - Ensured all communication uses **HTTPS with TLS encryption**.  

- **Purpose:**  
  To guarantee user privacy and data protection.

---

## **8. Testing & Quality Assurance**
- **Tasks:**
  - Conducted **unit testing** for models and controllers using **XCTest**.  
  - Performed **UI testing** using Xcode’s automated test recorder.  
  - Verified performance metrics (loading times, memory usage).  
  - Conducted beta testing on TestFlight with selected users.  

- **Purpose:**  
  To ensure app reliability and usability before release.

---

## **9. Deployment & Distribution**
- **Tasks:**
  - Configured **App IDs, Certificates, and Provisioning Profiles** in Apple Developer Portal.  
  - Prepared build for release using **Xcode Organizer**.  
  - Deployed internal beta through **TestFlight**.  
  - Planned public release submission to **App Store Connect** after mentor review.  

- **Purpose:**  
  To make the app ready for end-user testing and production deployment.

---

## **10. Maintenance & Future Improvements**
- **Planned Enhancements:**
  - Real AI summary integration via FastAPI backend.  
  - Multi-language localization (English/Spanish).  
  - Enhanced analytics for user engagement.  
  - Dark mode and accessibility improvements.  

- **Purpose:**  
  To ensure the app evolves with user feedback and remains maintainable over time.

---

### **Conclusion**
This daily log documents the **entire method of developing the MultiMed Fusion iOS application**, following a structured **agile, MVC-based workflow** using **Swift, Xcode, and Core Data**.  
Each phase ensures high quality, security, and usability, aligning with both **functional and non-functional requirements** of the project.

---

### **Commit Message**
> **Commit:** Added daily log describing iOS app development method and workflow.  
> **Author:** MultiMed Fusion Dev Team  
> **Date:** September 16, 2025  
> **Purpose:** Define structured approach for iOS app development using Swift and Xcode.

---

### **Daily Log: October 13 , 2025**

## **Purpose**
This Data Management Plan defines **what data will be stored, how it will be structured, and how it will be secured** within the MultiMed Fusion system.  
It aligns with the project’s goal of combining medical files (PDFs, images, and audio) into AI-generated summaries while ensuring patient privacy, data integrity, and accessibility.

---

## **1. Summary of Data to be Stored**

The MultiMed Fusion system will store **three main categories of data**:  
1. **User & Access Data** – authentication, roles, and profiles.  
2. **Medical Data** – uploaded files, anonymized information, and AI summaries.  
3. **System Data** – notifications, logs, and collaboration records.

### **Entities and Fields (Human-Friendly Summary)**

| **Entity** | **Description** | **Key Fields / Attributes** |
|-------------|-----------------|------------------------------|
| **User** | Stores account details for doctors, patients, and admins | `user_id`, `name`, `email`, `password_hash`, `role`, `created_at` |
| **Doctor** | Professional details linked to user | `doctor_id`, `user_id (FK)`, `specialization`, `hospital_affiliation` |
| **Patient** | Patient profile and demographics | `patient_id`, `user_id (FK)`, `dob`, `gender`, `contact_info`, `medical_history` |
| **File** | Uploaded medical files (PDFs, images, audio) | `file_id`, `patient_id (FK)`, `file_name`, `file_type`, `storage_path`, `upload_timestamp`, `uploaded_by` |
| **Anonymization** | Tracks privacy and PHI removal | `anon_id`, `file_id (FK)`, `status`, `removed_fields`, `verified_by` |
| **Summary** | AI-generated medical summaries | `summary_id`, `patient_id (FK)`, `doctor_id (FK)`, `summary_text`, `created_at`, `linked_files` |
| **Notification** | Alerts sent to users | `notif_id`, `user_id (FK)`, `message`, `type`, `status`, `created_at` |
| **Chat / Notes** | Secure communication between users | `chat_id`, `sender_id`, `receiver_id`, `message_text`, `timestamp` |
| **Audit Log** | Tracks all security and system events | `log_id`, `user_id (FK)`, `action`, `timestamp`, `ip_address`, `details` |

---

## **2. ER Diagram (Relational Data Model)**

### **Diagram Description (for a Non-Technical Reader):**
- **Users** can be **Doctors** or **Patients** (1:1).  
- **Patients** can have multiple **Files** and **Summaries** (1:Many).  
- **Doctors** can generate multiple **Summaries** for different Patients (1:Many).  
- **Each File** is linked to one **Anonymization record** (1:1).  
- **Users** receive multiple **Notifications** (1:Many).  
- **All actions** (uploads, deletions, updates) are logged in **Audit Logs**.  
- **Chats** record conversations between doctors and patients.  



---

## **3. Initial Data Security Plan**

Security is critical due to the sensitive nature of medical data.  
Below are the planned strategies for securing data within MultiMed Fusion.

### **A. Access Restriction**
- **Role-Based Access Control (RBAC):**
  - **Doctor:** Can view and summarize assigned patient data.  
  - **Patient:** Can view only their anonymized files and summaries.  
  - **Admin:** Can monitor logs but cannot view medical data.  
- Access validated through JWT tokens and backend middleware (FastAPI/Django).

### **B. Encryption**
- **Data in Transit:** All communications use **HTTPS (TLS 1.3)**.  
- **Data at Rest:** Stored in an **encrypted cloud database (PostgreSQL with AES-256 encryption)**.  
- **File Storage:** Stored in **S3-compatible storage** with encrypted access URLs and signed tokens.  
- **Credentials:** Hashed using **bcrypt**; no plain-text passwords stored.  

### **C. Privacy and Compliance**
- Compliant with **HIPAA-style data handling** standards.  
- All PHI (Patient Health Information) removed before vectorization or storage.  
- Anonymization process verified through the **Anonymization table** with status tracking.  
- Audit trails record all data access and modification activities.  

### **D. Backup and Recovery**
- Automated daily backups of the database and files.  
- Redundant cloud storage for recovery in case of system failures.  
- Version control for summaries to track history and avoid data loss.  

---

## **4. Mapping of Functional Requirements to Data Storage**

| **Functional Requirement** | **Relevant Data Entities** | **Storage Explanation** |
|-----------------------------|-----------------------------|--------------------------|
| **User Authentication & Access** | `User`, `Doctor`, `Patient` | Stores login credentials, roles, and access permissions. |
| **File Upload & Management** | `File`, `Patient`, `Doctor` | Stores uploaded medical files and metadata linked to users. |
| **Data Anonymization** | `Anonymization`, `File` | Tracks anonymization process and removed sensitive fields. |
| **AI Summary Generation** | `Summary`, `File` | Stores AI-generated summaries mapped to original medical files. |
| **Doctor Dashboard** | `Summary`, `Patient` | Fetches summaries and linked patient data for visualization. |
| **Patient Dashboard** | `Patient`, `File`, `Summary` | Displays patient’s anonymized files and AI summaries. |
| **Notifications & Alerts** | `Notification` | Stores system and user alerts about new summaries or uploads. |
| **Collaboration & Chat** | `Chat / Notes`, `User` | Manages secure communication between doctors and patients. |
| **Security & Audit Logs** | `Audit Log`, `User` | Records all user actions and system events for traceability. |

---

## **5. Future Data Enhancements**
- Integrate **vector embeddings storage** for AI-driven search and summarization.  
- Add **image metadata extraction** for radiology or lab image indexing.  
- Implement **token-based access sharing** for doctors to share temporary data views.  
- Enable **data export** in standardized formats (FHIR / HL7).  

---
---

# MultiMed Fusion – Comprehensive Data Management Plan

---

### **Daily Log: October 15 , 2025**

## **Objective**
To define a **complete Data Management Plan (DMP)** for the MultiMed Fusion system, outlining how data will be **collected, stored, secured, managed, and mapped** to the system’s functional requirements.  
This ensures that the system is efficient, secure, compliant, and scalable as it handles sensitive multi-modal medical data.

---

## **1. Overview**

**MultiMed Fusion** collects diverse data types such as:  
- **Structured data:** User profiles, roles, permissions.  
- **Unstructured data:** Lab reports, medical images, audio notes.  
- **AI-generated summaries:** Textual outputs from processed data.  

This DMP establishes policies for:
1. Data structure and relationships  
2. Storage method (SQL + NoSQL hybrid)  
3. Security, privacy, and encryption  
4. Backup, recovery, and lifecycle management  
5. Mapping between stored data and functional requirements  

---

## **2. Data Categories**

| **Category** | **Description** | **Examples** |
|---------------|-----------------|---------------|
| **User Data** | Information for authentication and profiles | Name, Email, Role, Credentials |
| **Patient Data** | Demographics and health-related records | DOB, Gender, History, Contact |
| **Medical Files** | Uploaded files in multiple formats | PDFs, DICOM images, audio |
| **AI Summaries** | Processed summaries from uploaded data | Text summaries, linked file references |
| **Anonymization Data** | Records of removed PHI | File status, removed fields, verification |
| **System Logs & Notifications** | Operational and event logs | Login, upload, access, alerts |

---

## **3. Data Model Summary**

### **Relational (SQL) Entities**
Used for **structured and relational data**, such as users, permissions, logs, and AI summaries.

| **Entity** | **Key Fields** | **Purpose** |
|-------------|----------------|--------------|
| **User** | user_id, name, email, password_hash, role | Stores authentication data |
| **Doctor** | doctor_id, user_id (FK), specialization | Links to user, adds medical details |
| **Patient** | patient_id, user_id (FK), dob, gender | Stores patient profiles |
| **Summary** | summary_id, doctor_id (FK), patient_id (FK), summary_text | Stores AI-generated summaries |
| **Audit Log** | log_id, user_id, action, timestamp | Tracks all system activity |

### **NoSQL (Document-based) Collections**
Used for **unstructured or multi-format data** such as uploaded files, anonymization details, and communications.

| **Collection** | **Example Fields** | **Purpose** |
|----------------|--------------------|--------------|
| **files** | `_id`, `patientId`, `filePath`, `fileType`, `uploadedAt` | Stores metadata for uploaded files |
| **anonymization** | `_id`, `fileId`, `status`, `removedFields` | Tracks data privacy and PHI removal |
| **chat_notes** | `_id`, `senderId`, `receiverId`, `message`, `timestamp` | Handles secure doctor-patient communication |
| **notifications** | `_id`, `userId`, `message`, `type`, `createdAt` | Sends system alerts and updates |

---

## **4. ER Diagram (Conceptual Model)**

**High-Level Relationships:**
- A **User** can be either a **Doctor** or a **Patient**.  
- Each **Patient** can have multiple **Files** and **Summaries**.  
- Each **File** has an **Anonymization record** (1–1).  
- **Doctors** generate **Summaries** for **Patients** (1–M).  
- **Audit Logs** track every user’s activity.  
- **Chats** and **Notifications** connect users asynchronously.

*(You can add your diagram here once created in Draw.io or Lucidchart)*  
`![ER Diagram](images/multimed_fusion_er.png)`

---

## **5. Data Security Plan**

### **A. Access Control**
- **Role-Based Access Control (RBAC):**  
  - **Doctor:** Access assigned patients and summaries only.  
  - **Patient:** Access own records and anonymized data.  
  - **Admin:** Manage users and logs, no medical data access.
- All endpoints validated via backend middleware and JWT tokens.

### **B. Encryption**
- **In Transit:** HTTPS (TLS 1.3) for all API communications.  
- **At Rest:** AES-256 encryption for all stored files and database fields.  
- **Authentication:** Passwords stored using bcrypt hashing.

### **C. Anonymization**
- All PHI (names, IDs, addresses) automatically removed before file processing.  
- Anonymization status stored in the `anonymization` collection.  
- Verification logs recorded in audit trails.

### **D. Audit & Logging**
- Every file upload, access, or modification is logged in `audit_log`.  
- Logs include timestamps, user IDs, and actions.  
- Regular reviews by admin for suspicious activity.

---

## **6. Backup and Recovery Plan**

| **Type** | **Frequency** | **Description** |
|-----------|----------------|-----------------|
| **Database Backup** | Daily | Automated snapshots of SQL and NoSQL databases. |
| **File Backup** | Daily | Redundant storage (S3 + secondary region). |
| **Disaster Recovery** | On Failure | System auto-switch to backup environment. |
| **Audit Log Retention** | 1 year | Stored for compliance and traceability. |

---

## **7. Data Lifecycle Management**

1. **Collection:** Files, forms, and notes uploaded by authorized users.  
2. **Storage:** Data stored in encrypted cloud databases.  
3. **Processing:** AI models create summaries (temporary compute layer).  
4. **Access:** Controlled via tokens and permissions.  
5. **Archival:** Inactive data archived after 1 year.  
6. **Deletion:** Patient-requested data deletion per privacy policy.

---

## **8. Data Mapping to Functional Requirements**

| **Functional Requirement** | **Data Source / Entity** | **Storage Type** | **Description** |
|-----------------------------|--------------------------|------------------|-----------------|
| User Authentication | User | SQL | Stores login and identity data |
| File Upload & Management | Files | NoSQL | Handles unstructured medical files |
| Data Anonymization | Anonymization | NoSQL | Tracks privacy and PHI removal |
| AI Summary Generation | Summary | SQL | Stores structured summary data |
| Doctor Dashboard | Summary, Patient | SQL | Fetches summaries linked to patients |
| Patient Dashboard | Patient, Files | SQL + NoSQL | Displays history and anonymized files |
| Notifications | Notifications | NoSQL | Alerts for uploads and summaries |
| Chat Communication | Chat_Notes | NoSQL | Real-time secure communication |
| Audit & Security | Audit_Log | SQL | Tracks every access or modification |

---

## **9. Data Compliance & Ethics**

- Aligns with **HIPAA** and **GDPR** principles for medical data privacy.  
- Patients retain **ownership and access control** of their medical data.  
- Every data access logged for transparency.  
- Data shared with AI modules is anonymized by default.  
- Regular **security audits** ensure ongoing compliance.

---

## **10. Tools & Technologies**

| **Layer** | **Technology** | **Purpose** |
|------------|----------------|-------------|
| **Backend** | FastAPI / Django | Data access, API security |
| **Database (Relational)** | PostgreSQL | Structured data storage |
| **Database (NoSQL)** | MongoDB Atlas | Unstructured medical files |
| **File Storage** | AWS S3 (Encrypted) | Secure file handling |
| **Authentication** | JWT + OAuth2 | Secure user session management |
| **Encryption** | AES-256, bcrypt | Data and password protection |
| **Backup** | AWS Backup + Cron Jobs | Redundancy and recovery |
| **Monitoring** | Grafana + CloudWatch | Health and security monitoring |

---

## **11. Future Data Improvements**
- Implement **vector embeddings** for AI-driven similarity search (Pinecone / FAISS).  
- Add **FHIR-compatible data export** for integration with hospital systems.  
- Develop **automated PHI detection models** for faster anonymization.  
- Enable **data lineage visualization** to track AI usage history.

---



---

### **Daily Log: October  17, 2025**

## **Objective**
To document the process and method used to **convert the existing MultiMed Fusion web application** into a **fully functional mobile application** for iOS and Android platforms.  
The mobile version aims to preserve all core features — AI summaries, file upload, anonymization, and dashboards — while optimizing the experience for smaller screens and offline access.

---

## **1. Background**
The MultiMed Fusion web app was originally developed using:
- **Frontend:** React (with TailwindCSS)
- **Backend:** FastAPI / Django
- **Database:** PostgreSQL and MongoDB (hybrid)

To increase accessibility for doctors and patients, the decision was made to develop a **mobile version** using the existing backend APIs while redesigning the frontend for native mobile experiences.

---

## **2. Chosen Mobile Development Approach**

| **Option** | **Description** | **Decision** |
|-------------|----------------|---------------|
| **Native (Swift & Kotlin)** | Separate codebases for iOS and Android | ❌ Too time-consuming |
| **Cross-Platform (React Native)** | Single codebase using React principles | ✅ Selected |
| **Hybrid WebView** | Embed existing web UI into a container app | ❌ Limited offline and hardware access |

**Decision:** Use **React Native with Expo** to maximize code reuse from the web React app, ensuring cross-platform deployment.

---

## **3. Setup & Configuration**
- Installed **React Native CLI** and **Expo** for fast prototyping.  
- Cloned the existing **frontend repo** and modularized components for reuse.  
- Connected the app to the existing **FastAPI backend** using Axios.  
- Configured **React Navigation** for screen transitions.  
- Set up development environments for both:
  - **iOS (Xcode Simulator)**
  - **Android (Android Studio Emulator)**

---

## **4. UI & UX Redesign**
- Reworked layouts for **mobile responsiveness** and touch-based navigation.  
- Simplified dashboard menus and grouped key actions (Upload, Summary, Settings).  
- Added **tab navigation** and **bottom navigation bar** for easier access.  
- Integrated **native modules** for:
  - Camera access (file upload)
  - Microphone access (audio notes)
  - Local notifications

**Major Screens Designed:**
1. **Login & Signup**
2. **Doctor Dashboard**
3. **Patient Dashboard**
4. **File Upload (Camera / File Picker)**
5. **AI Summary View**
6. **Anonymization Confirmation**
7. **Notifications**
8. **Settings**

---

## **5. API Integration**
- Reused backend **REST APIs** developed for the web app.  
- Integrated endpoints for:
  - Authentication (JWT-based)
  - File upload
  - Summary retrieval
  - Anonymization status check
  - Notifications  
- Added **interceptors** for secure token handling and automatic logout on token expiry.  

Example Code:
```javascript
axios.get(`${API_URL}/summary/${patientId}`, {
  headers: { Authorization: `Bearer ${token}` }
})
.then(response => setSummary(response.data))
.catch(error => console.error(error)) ;



---

### **Daily Log: October 27, 2025**

## **Objective**
To outline the process of **data seeding** for the **MultiMed Fusion** platform.  
This step initializes the project database with **sample doctors, patients, medical files, summaries, and anonymized records** to support early development, testing, and UI/UX demonstrations before real data integration.

---

## **1. Purpose of Data Seeding**
- To **simulate real-world medical workflows** in a controlled environment.  
- To allow front-end developers to **test dashboards, search, uploads, and summaries** with live-like data.  
- To provide **AI developers** with initial sample records for model integration and testing.  
- To ensure **database integrity and schema validation** across all modules before production.  

---

## **2. Seeding Environment**
| **Environment** | **Database** | **Description** |
|------------------|--------------|-----------------|
| **Local Development** | PostgreSQL + MongoDB | For backend and frontend developer testing. |
| **Staging** | MongoDB Atlas (Cloud) | Used for integration with mobile and web clients. |

**Tools Used:**
- `pgAdmin` for SQL data import  
- `MongoDB Compass` for NoSQL collections  
- Python **seed scripts** via FastAPI for automated data injection  
- JSON seed files for portability

---

## **3. Data Sets to be Seeded**

### **A. User Data**
| **Role** | **Fields** | **Example Values** |
|-----------|------------|--------------------|
| Doctor | `name`, `email`, `specialization`, `hospital` | "Dr. John Smith", "Cardiology", "City Medical Center" |
| Patient | `name`, `dob`, `gender`, `contact` | "Jane Doe", "1990-05-14", "Female" |

**Purpose:** To populate dashboards and enable role-based login testing.

---

### **B. Medical Files (NoSQL Collection: `files`)**
```json
{
  "_id": "file001",
  "patientId": "patient001",
  "uploadedBy": "doctor001",
  "fileName": "Blood_Test_Report.pdf",
  "fileType": "lab_report",
  "filePath": "s3://fusion/files/file001.pdf",
  "anonymized": true,
  "uploadedAt": "2025-09-21T09:30:00Z"
}



---

### **Daily Log: October 29, 2025**


---

## **1. Purpose**
- Prevent testing on live or production databases.  
- Provide realistic, anonymized data to test core workflows.  
- Maintain consistent data for automated testing, UI development, and backend integration.  
- Allow seamless re-seeding whenever schema updates occur.

---

## **2. Seeding Policy**
### **Rules**
- Use only synthetic, randomly generated data (via Faker or manual creation).  
- No personally identifiable or real patient health information (PHI).  
- All seed files must follow the **ER schema** and remain version-controlled.  
- Updated seed files committed after every schema or field change.

### **Environments**
| **Environment** | **Database Type** | **Purpose** |
|------------------|-------------------|--------------|
| Local Dev | PostgreSQL + MongoDB | Developer testing |
| Staging | MongoDB Atlas | Integration with mobile app |
| CI/CD | SQLite (mock) | Automated test runs |

---

## **3. Database Overview**
MultiMed Fusion uses a **hybrid database model**:

| **Type** | **Purpose** | **Technology** |
|-----------|-------------|----------------|
| SQL | Structured data: users, summaries, logs | PostgreSQL |
| NoSQL | Unstructured data: files, anonymization, chat | MongoDB |

---

## **4. SQL Seed Data (`fusion_seed.sql`)**

Example content for relational tables:
```sql
-- Users
INSERT INTO users (user_id, name, email, role, password_hash)
VALUES
('doctor001', 'Dr. John Smith', 'dr.smith@fusion.com', 'doctor', 'hashedpass123'),
('patient001', 'Jane Doe', 'jane@fusion.com', 'patient', 'hashedpass456');

-- Doctors
INSERT INTO doctors (doctor_id, user_id, specialization, hospital_affiliation)
VALUES ('doctor001', 'doctor001', 'Cardiology', 'City Medical Center');

-- Patients
INSERT INTO patients (patient_id, user_id, dob, gender)
VALUES ('patient001', 'patient001', '1990-05-14', 'Female');

-- Summaries
INSERT INTO summaries (summary_id, doctor_id, patient_id, summary_text, created_at)
VALUES
('sum001', 'doctor001', 'patient001', 'Blood report indicates normal glucose levels.', NOW());

-- Audit Logs
INSERT INTO audit_logs (log_id, user_id, action, timestamp)
VALUES ('log001', 'doctor001', 'created_summary', NOW());


# MultiMed Fusion – Final Project Report & Future Tasks (Daily Log)

---

### **Daily Log: October 31 , 2025**



---

## **1. Project Overview**
**MultiMed Fusion** is a smart healthcare platform designed to **collect, process, and summarize multi-format medical data** — including lab reports, images, and voice notes — using **AI-based summarization and secure data management**.

The system aims to:
- Save doctors’ time by generating **automated summaries**.  
- Protect patient privacy through **data anonymization**.  
- Provide secure dashboards for both doctors and patients.  
- Offer seamless integration across **web and mobile platforms**.

---

## **2. Core Features Developed**

| **Category** | **Features Implemented** |
|---------------|---------------------------|
| **User Authentication** | Role-based login (Doctor/Patient/Admin), JWT authentication, password reset |
| **Data Upload & Management** | Multi-file upload (PDF, image, audio), drag-and-drop, upload progress tracking |
| **AI Summary Generation** | Automatic generation of medical summaries with links to source files |
| **Anonymization & Privacy** | Removal of PHI (names, addresses, IDs), patient consent forms, privacy toggle |
| **Dashboards** | Doctor and Patient dashboards with summary history and file links |
| **Notifications** | Real-time alerts for new summaries, urgent flags, and collaboration updates |
| **Collaboration Tools** | Doctor-to-doctor notes, secure chat, and image annotation support |
| **Security & Compliance** | End-to-end encryption, session timeout, audit logs, HIPAA-style compliance |
| **Mobile Application** | Cross-platform React Native app (Expo) with offline caching and biometric login |
| **Database System** | Hybrid model using PostgreSQL (structured data) and MongoDB (unstructured data) |
| **Data Seeding** | Full seed dataset (SQL + JSON) for safe testing and continuous integration |

---

## **3. Technical Architecture**

### **Frontend:**
- **Web:** React + Tailwind CSS  
- **Mobile:** React Native (Expo)  
- **State Management:** Redux Toolkit  
- **API Integration:** Axios + JWT  

### **Backend:**
- **Framework:** FastAPI (Python)  
- **Auth & Security:** OAuth2 + bcrypt + JWT  
- **AI Integration:** FastAPI endpoint linked to NLP model for summaries  

### **Database:**
- **Relational (SQL):** PostgreSQL (Users, Summaries, Logs)  
- **Non-Relational (NoSQL):** MongoDB Atlas (Files, Anonymization, Chats, Notifications)  

### **Storage:**
- AWS S3 for medical file storage with signed URLs  
- Daily backups to secondary cloud storage  

---

## **4. Data Management Highlights**
- **Data Management Plan** implemented with encryption at rest and transit.  
- **Hybrid Schema Design:** SQL for structured data, NoSQL for flexible file metadata.  
- **Dummy Data System:** Seed scripts for both PostgreSQL and MongoDB created.  
- **Anonymization Pipeline:** Automatically removes PHI before file storage.  
- **Audit Trail:** Tracks every system event (uploads, deletions, modifications).  

---

## **5. Mobile App Conversion Summary**
- Converted web app to mobile using **React Native + Expo**.  
- Integrated camera, voice recorder, and offline mode for doctors.  
- Reused existing APIs and authentication logic.  
- Added **biometric login**, local caching, and background sync for summaries.  
- Tested across both **Android (API 33)** and **iOS 16** simulators.

---

## **6. Data Seeding & Dummy Data Implementation**
- Created **fusion_seed.sql** (for PostgreSQL) and **fusion_nosql_seed.json** (for MongoDB).  
- Populated synthetic data for:
  - Users (doctors/patients)
  - Medical files (PDFs, images)
  - AI summaries
  - Notifications
  - Audit logs  
- Provided shell and Python scripts to load, clear, and reseed data easily.  
- Verified seed data integrity through dashboard and API tests.

---

## **7. Non-Functional Achievements**

| **Category** | **Target Achieved** |
|---------------|--------------------|
| **Performance** | Avg summary generation < 5 sec for 25MB input |
| **Usability** | Responsive, accessible, mobile-first UI |
| **Reliability** | 99.9% uptime goal, auto recovery setup |
| **Security** | End-to-end TLS, bcrypt password hashing, role-based access |
| **Scalability** | Containerized backend (Docker-ready), MongoDB Atlas auto-scaling |
| **Maintainability** | Modular architecture, 70%+ test coverage planned |
| **Portability** | Works across macOS, Windows, Linux, iOS, Android |

---

## **8. Testing Summary**
- Unit and integration testing completed for APIs and UI.  
- Mobile app tested via **TestFlight** (iOS) and **Google Play Internal Testing** (Android).  
- Dummy seed data validated through web and mobile dashboards.  
- Security audits simulated using mock penetration tools (e.g., OWASP ZAP).  

---

# MultiMed Fusion – Proposed List of Prototypes (Semester Plan)

---

### **Daily Log November 3 , 2025**



## **1. Purpose**
The proposed prototypes represent **tangible, functional versions** of key modules in the MultiMed Fusion system.  
Each prototype will demonstrate the **core functionality**, **data flow**, and **user experience**, forming a foundation for full-scale development next semester.

---

## **2. Prototype Goals**
- Build working models of critical system components.  
- Demonstrate AI-driven medical summary generation.  
- Validate anonymization and security workflows.  
- Provide end-to-end connectivity between frontend, backend, and database.  
- Prepare the system for real-world testing with dummy data.  

---

## **3. Proposed Prototypes (Semester Deliverables)**

### **A. Prototype 1 – User Authentication & Role-Based Access**
**Description:**  
Develop login, signup, and password reset functionality with distinct dashboards for doctors and patients.  

**Expected Outcome:**  
- Secure authentication using JWT tokens.  
- Role-based navigation and session timeout handling.  
- Basic dashboard redirection post-login.

**Planned Files/Modules:**  
`LoginPage.jsx`, `SignupPage.jsx`, `DashboardRouter.jsx`

---

### **B. Prototype 2 – File Upload & Anonymization**
**Description:**  
Implement secure file upload system supporting PDFs, images, and audio notes. Include anonymization logic that automatically removes PHI before storage.

**Expected Outcome:**  
- Drag-and-drop upload for web; camera upload for mobile.  
- Preview of uploaded file and anonymization confirmation.  
- PHI removal validation using mock rules.  

**Planned Files/Modules:**  
`UploadComponent.jsx`, `AnonymizationScreen.jsx`, `FilePreviewModal.jsx`

---

### **C. Prototype 3 – AI Summary Generation**
**Description:**  
Develop the initial AI module for generating readable summaries of uploaded medical data.  

**Expected Outcome:**  
- Text summarization via mock FastAPI endpoint.  
- Summary stored and displayed on Doctor Dashboard.  
- Integration with dummy data and file references.

**Planned Files/Modules:**  
`SummaryDashboard.jsx`, `SummaryAPI.py`, `AIService.js`

---

### **D. Prototype 4 – Doctor & Patient Dashboards**
**Description:**  
Create role-specific dashboards showing uploaded files, summaries, and notifications.

**Expected Outcome:**  
- **Doctor Dashboard:** View summaries, add notes, verify anonymization.  
- **Patient Dashboard:** View uploaded history and AI summaries.  
- Interactive components with sample seed data.

**Planned Files/Modules:**  
`DoctorDashboard.jsx`, `PatientDashboard.jsx`, `AccessLogs.jsx`

---

### **E. Prototype 5 – Notifications & Collaboration Tools**
**Description:**  
Develop the foundation for communication between doctors and patients with system alerts and secure chat.

**Expected Outcome:**  
- Real-time notifications for summary creation and file uploads.  
- Secure message exchange using WebSocket or mock API.  
- Notification panel integrated into dashboard.

**Planned Files/Modules:**  
`ChatComponent.jsx`, `NotificationService.js`, `AlertsPanel.jsx`

---

### **F. Prototype 6 – Data Management & Seeding**
**Description:**  
Prepare full seed datasets (SQL + NoSQL) to populate dashboards and test features safely.

**Expected Outcome:**  
- Dummy doctor, patient, file, and summary data.  
- SQL dump and JSON files for both databases.  
- Scripts for automated loading and reset.

**Planned Files/Modules:**  
`fusion_seed.sql`, `fusion_nosql_seed.json`, `load_seed_data.py`

---

### **G. Prototype 7 – Mobile App Conversion (Phase 1)**
**Description:**  
Convert the web interface into a mobile app using React Native with shared backend services.  

**Expected Outcome:**  
- Login and summary viewing available on mobile.  
- Camera upload and offline access demo.  
- Mobile-friendly UI aligned with system branding.

**Planned Files/Modules:**  
`MobileLoginScreen.jsx`, `MobileSummaryView.jsx`, `OfflineMode.jsx`

---


# MultiMed Fusion – Frontend Feature Implementation Log

---

### **Daily Log: November  5 , 2025**


---


```jsx
// UploadComponent.jsx
import React, { useState } from "react";
import axios from "axios";

const UploadComponent = () => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [previewURLs, setPreviewURLs] = useState([]);
  const [anonymize, setAnonymize] = useState(true);
  const [uploadStatus, setUploadStatus] = useState("");

  // Handle file selection
  const handleFileChange = (e) => {
    const files = Array.from(e.target.files);
    setSelectedFiles(files);
    setPreviewURLs(files.map((file) => URL.createObjectURL(file)));
  };

  // Handle file upload
  const handleUpload = async () => {
    const formData = new FormData();
    selectedFiles.forEach((file) => formData.append("files", file));
    formData.append("anonymize", anonymize);

    try {
      setUploadStatus("Uploading...");
      const response = await axios.post("http://localhost:8000/api/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setUploadStatus(`✅ Upload successful: ${response.data.message}`);
    } catch (error) {
      setUploadStatus("❌ Upload failed. Please try again.");
      console.error(error);
    }
  };

  return (
    <div className="max-w-md mx-auto p-4 rounded-2xl shadow-md bg-white">
      <h2 className="text-xl font-bold mb-4 text-center text-blue-600">Upload Medical Files</h2>

      {/* File Input */}
      <input
        type="file"
        multiple
        onChange={handleFileChange}
        className="block w-full text-sm text-gray-500 border border-gray-300 rounded-lg cursor-pointer mb-3"
      />

      {/* Anonymization Toggle */}
      <div className="flex items-center justify-between mb-3">
        <label className="text-gray-700 font-medium">Anonymize Before Upload</label>
        <input
          type="checkbox"
          checked={anonymize}
          onChange={() => setAnonymize(!anonymize)}
          className="w-5 h-5 text-blue-600"
        />
      </div>

      {/* Preview Section */}
      {previewURLs.length > 0 && (
        <div className="mb-3">
          <h3 className="text-gray-600 font-medium mb-1">Preview:</h3>
          <div className="grid grid-cols-3 gap-2">
            {previewURLs.map((url, index) => (
              <img
                key={index}
                src={url}
                alt="File Preview"
                className="w-full h-24 object-cover rounded-lg border"
              />
            ))}
          </div>
        </div>
      )}

      {/* Upload Button */}
      <button
        onClick={handleUpload}
        className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
      >
        Upload
      </button>

      {/* Upload Status */}
      {uploadStatus && (
        <p className="mt-3 text-center text-sm text-gray-700">{uploadStatus}</p>
      )}
    </div>
  );
};

export default UploadComponent;



---

### **Daily Log: November  7 , 2025**



---



## **1. Seed Script Implemented:** `seed_users.py`

```python
"""
seed_users.py – Script to seed dummy users into PostgreSQL for MultiMed Fusion
Author: MultiMed Fusion Dev Team
Date: September 26, 2025
"""

import psycopg2
from psycopg2 import sql
from datetime import datetime
import bcrypt

# Database connection
conn = psycopg2.connect(
    host="localhost",
    database="multimed_fusion",
    user="postgres",
    password="admin123"
)
cur = conn.cursor()

# Helper function for password hashing
def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Dummy user data
users = [
    {
        "user_id": "user001",
        "name": "Dr. John Smith",
        "email": "dr.john@fusion.com",
        "role": "doctor",
        "password": hash_password("Doctor@123"),
        "created_at": datetime.now()
    },
    {
        "user_id": "user002",
        "name": "Dr. Emily Carter",
        "email": "dr.emily@fusion.com",
        "role": "doctor",
        "password": hash_password("Doctor@321"),
        "created_at": datetime.now()
    },
    {
        "user_id": "user003",
        "name": "Jane Doe",
        "email": "jane.doe@fusion.com",
        "role": "patient",
        "password": hash_password("Patient@123"),
        "created_at": datetime.now()
    },
    {
        "user_id": "user004",
        "name": "Adam Lee",
        "email": "adam.lee@fusion.com",
        "role": "patient",
        "password": hash_password("Patient@321"),
        "created_at": datetime.now()
    },
    {
        "user_id": "user005",
        "name": "Admin User",
        "email": "admin@fusion.com",
        "role": "admin",
        "password": hash_password("Admin@123"),
        "created_at": datetime.now()
    }
]

# Create table if not exists
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    role VARCHAR(20) CHECK (role IN ('doctor', 'patient', 'admin')),
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# Insert users
for u in users:
    cur.execute(
        sql.SQL("""
            INSERT INTO users (user_id, name, email, role, password_hash, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id) DO NOTHING;
        """),
        (u["user_id"], u["name"], u["email"], u["role"], u["password"], u["created_at"])
    )

conn.commit()
cur.close()
conn.close()

print("User seed data successfully inserted into database!")


# MultiMed Fusion – Network Security Implementation Daily Log

---

### **Daily Log: November 10, 2025**


## **Goals**
1. Protect all communication between the **frontend (React / React Native)** and **backend (FastAPI)** through encryption.  
2. Prevent data leaks or manipulation during data transfer.  
3. Implement authentication, access control, and intrusion prevention measures.  
4. Align all communication protocols with **HIPAA-style compliance** for medical data security.

---

## **1. HTTPS (SSL/TLS) Encryption**
- All frontend and backend communication will use **HTTPS only**.  
- SSL certificates will be generated using **Let’s Encrypt** for production deployment.  
- In local development, self-signed certificates will simulate secure connections.  
- Backend API endpoint configured as `https://api.multimedfusion.com`.  
- HTTP requests automatically redirected to HTTPS using Nginx reverse proxy.  

**Outcome:**  
Secure data transmission between user devices and the backend server, ensuring no sensitive information is transferred over unsecured channels.

---

## **2. Authentication and Access Control**
- Implemented **JWT (JSON Web Token)** authentication for all API endpoints.  
- Tokens include user role (doctor, patient, admin) and expiration time.  
- Tokens expire after inactivity, requiring re-authentication for added safety.  
- Role-based permissions:  
  - **Doctor:** Upload and view anonymized medical files, generate summaries.  
  - **Patient:** View personal files and respond to doctor requests.  
  - **Admin:** Monitor logs and oversee data compliance.

**Outcome:**  
Only authorized users can access or modify specific types of data, ensuring isolation between patient and doctor accounts.

---

## **3. Data Encryption Standards**
- **Passwords:** Encrypted using `bcrypt` before being stored in the PostgreSQL database.  
- **Sensitive Data:** Encrypted using **AES-256** for fields like patient identifiers.  
- **Data in Transit:** Encrypted through **TLS 1.3**, the latest secure transport layer protocol.  
- **Backups:** Database dumps are encrypted and stored in AWS S3 with restricted access.  

**Outcome:**  
Even if the network or database is compromised, all stored data remains unreadable without proper encryption keys.

---

## **4. Firewall and Network Segmentation**
- Configured **firewall rules** to allow only necessary ports (e.g., 443 for HTTPS, 22 for SSH).  
- Restricted database and API access to trusted internal network IPs.  
- FastAPI and PostgreSQL servers placed in separate private subnets for isolation.  
- Future plan to integrate **AWS Security Groups** and **VPC Network ACLs** for granular control.  

**Outcome:**  
Prevents direct public access to internal systems, reducing attack surfaces.

---

## **5. API Rate Limiting and Intrusion Detection**
- Configured API rate limiting using **FastAPI middleware** to prevent brute-force or spam attacks.  
- Integrated monitoring tools (e.g., **Fail2Ban**, **UFW logs**) to detect unauthorized login attempts.  
- Audit logs maintained for every user action in the system.  

**Outcome:**  
Reduces risk of denial-of-service (DoS) attacks and identifies suspicious activities in real time.

---

## **6. Secure Session Management**
- Implemented automatic logout after 15 minutes of inactivity.  
- Sessions are refreshed securely through short-lived JWTs.  
- Backend invalidates tokens when users log out manually.  

**Outcome:**  
Prevents unauthorized access through expired or stolen tokens.

---

## **7. Data Anonymization for Network Transfers**
- Before any file or record is transmitted to AI services or summaries, all personally identifiable information (PII) is removed.  
- Only anonymized versions are sent for processing or analysis.  
- Network monitoring ensures no PHI is transmitted through unsecured APIs.  

**Outcome:**  
Maintains compliance with patient privacy requirements across all communication layers.

---

## **8. Testing and Validation**
| **Test Case** | **Expected Result** | **Status** |
|----------------|--------------------|-------------|
| HTTP to HTTPS redirection | Redirects automatically | Passed |
| JWT token verification | Invalid tokens blocked |  Passed |
| Encrypted passwords check | Bcrypt hash stored correctly | Passed |
| API access control | Only authorized roles allowed | Passed |
| Network vulnerability scan | No open or unsafe ports found | Passed |

---

## **9. Next Steps**
1. Set up **SSL/TLS automation** for certificate renewal using Certbot.  
2. Deploy **Nginx reverse proxy** for load balancing and HTTPS routing.  
3. Integrate **audit logging dashboard** for real-time network activity monitoring.  
4. Add **multi-factor authentication (MFA)** for critical user roles.  
5. Conduct **penetration testing** using OWASP ZAP and report findings.  

---

## **10. Summary**
The network security plan ensures that MultiMed Fusion maintains confidentiality, integrity, and availability of medical data.  
By combining HTTPS, encryption, JWT-based authentication, and firewall isolation, the project establishes a **robust foundation for secure medical data handling** across both web and mobile platforms.

---

# MultiMed Fusion – Software Requirements Specification (SRS)

---

### **1. Project Information**

**Project Title:**  
MultiMed Fusion – Multi-Modal Medical Data & AI Summary System

**Goal:**  
To build a secure platform for doctors and patients to upload, anonymize, and summarize medical data (reports, images, audio) using AI.



**Problem Statement:**  
Medical data is scattered and time-consuming to review. MultiMed Fusion solves this by collecting all medical files in one place, anonymizing them, and generating AI summaries for faster understanding.

---

### **2. Design**

**Use Cases:**  
1. Upload medical files  
2. Anonymize sensitive data  
3. Generate AI summaries  
4. Search and filter reports  
5. Doctor–patient file requests  
6. View dashboard and notifications  

---

**Functional Requirements:**  
- Secure file upload and storage  
- Automatic PHI anonymization  
- AI summarization with original file links  
- Search and filter functionality  
- Role-based access (Doctor/Patient/Admin)  
- Notifications and dashboard access  

---

**Non-Functional Requirements:**  
- **Security:** HTTPS, JWT, and encryption  
- **Usability:** Simple, responsive UI  
- **Performance:** Fast upload and AI response  
- **Reliability:** 99.9% uptime goal  
- **Compliance:** Privacy-focused, HIPAA-style  

---

**Data Management Plan:**  
- Databases: PostgreSQL (users, summaries) and MongoDB (files, logs).  
- Data stored: user info, files, summaries, messages, logs.  
- All sensitive data encrypted in transit and at rest.  
- Dummy seed data used for development (SQL + JSON).

---

**Proposed Prototypes (This Semester):**  
1. File Upload & Storage  
2. Data Anonymization  
3. AI Summarization  
4. Search & Filter  
5. Doctor–Patient Communication  
6. Notifications  
7. Dashboard Overview  
8. Mobile Prototype (Phase 1)

---

### **3. Meeting Minutes Summary**

- **Aug 29:** Project idea, tech stack decided.  
- **Sep 5:** Architecture and data flow finalized.  
- **Sep 10:** Prototype plan created.  
- **Sep 20:** Network security plan discussed.  
- **Sep 28:** Progress review and SRS completion.

---

### **4. Conclusion**

MultiMed Fusion will deliver secure, AI-powered medical data management with working prototypes for upload, anonymization, summarization, and dashboards by semester end.

---

# MultiMed Fusion – JSON Seed Data Creation Log

---

### **Daily Log: November 14, 2025**


## **Files Created**
1. `users.json`  
2. `files.json`  
3. `summaries.json`  
4. `anonymization.json`  
5. `notifications.json`

Each file is formatted for **native MongoDB import** using `mongoimport`.

---

## **1. users.json**

```json
[
  {
    "_id": "user001",
    "name": "Dr. John Smith",
    "email": "dr.john@fusion.com",
    "role": "doctor"
  },
  {
    "_id": "user003",
    "name": "Jane Doe",
    "email": "jane.doe@fusion.com",
    "role": "patient"
  }
]

