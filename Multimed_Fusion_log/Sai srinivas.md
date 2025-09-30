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

