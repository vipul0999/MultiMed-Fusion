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

