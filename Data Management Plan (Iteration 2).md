## Data Summary

The MultiMed-Fusion project will process various medical data types. The following is an analysis of the prominent data types we'll process:

### **Patient Information**
- `patient_id (int)`: Unique id for each patient.
- `first_name (string)`: Patient's first name.
- `last_name (string)`: Patient's last name.
- `dob (Date)`: Date of birth.
- `gender (Character)`: The patient’s gender.
- `contact_info (string)`: Patient's address, phone number, and email details.

### **Doctor Information**
- `doctor_id (int)`: Unique id for doctor.
- `first_name (string)`: Doctor’s first name.
- `last_name (string)`: Doctor’s last name.
- `specialty (string)`: Specialization of doctor.
- `contact_info (string)`: Doctor’s address, phone number, and email details.
- `hospital_affiliation (string)`: Doctor’s hospital.

### **User Information**
- `id (int)`: Unique identifier for all users.
- `username (string)`: Username of users.
- `email (email)`: Email address of users.
- `is_doctor (bool)`: True if user is doctor.
- `is_patient (bool)`: True if user is patient.

### **Medical Files**
- `file_id (int)`: Unique identifier for each medical file.
- `file_type (string)`: Type of file (e.g., medical report, picture, or sound).
- `file_name (string)`: File name given to the file.
- `file_size (int)`: File size.
- `patient_id (int)`: Links the file to the specific patient.
- `file_path (string)`: Path of the file (location where medical files are stored).

### **AI-Generated Summaries**
- `summary_id (int)`: Unique summary ID for every AI-generated summary.
- `file_id (int)`: References the medical file that the summary describes.
- `summary_text (string)`: AI-generated summary of the medical file.
- `generation_date (date)`: Date when the summary was generated.

### **Audit Logs (Activity Tracking System)**
- `log_id (int)`: Unique log ID for every log entry.
- `user_id (int)`: ID of the user who initiated the action.
- `action_type (string)`: Defines the action (viewing, modifying, or deleting a record).
- `timestamp (datetime)`: The exact time the action was performed.
- `affected_data (string)`: Indicates what data was read or modified.

### **Vector Table**
- `vector_id (int)`: Unique identifier for each vector record.
- `file_id (int)`: ID of the medical file associated with this vector.
- `patient_id (int)`: References the patient linked to the medical file.
- `doctor_id (int)`: References the doctor associated with the medical file or analysis.
- `vector_data (vector)`: Stores the numeric embedding representing the content of the medical file.

## Entity-Relationship Diagram (ERD)

To better understand the way each of the different data elements is related to the others, we will create an Entity-Relationship Diagram (ERD). This will help visualize the relationships between different data entities.

### Entities:
- **Users**: Stores all user information (i.e., patient, doctor, admin).
- **Patient**: Stores most critical patient information, including name and contact details.
- **MedicalFile**: Stores the path or URI of medical records of the patient (reports, images, and audio).
- **Summary**: Automatically created summaries by AI providing descriptions of medical files.
- **AuditLog**: Records all system events (data change and access).
- **Doctor**: Doctor will access summary files and provide diagnosis.
- **Vector Table**: Stores vector embeddings generated from medical files for semantic search and AI analysis. Includes references to related patient and doctor records through `patient_id` and `doctor_id` columns.

### Relationships:
- A **User** can have multiple **Doctors**, **Patients**, and **Admins**.
- A **Patient** can have several **MedicalFiles**.
- A **Doctor** can have multiple **Patients**.
- **MedicalFile** can have several **Summaries** associated with it.
- **AuditLogs** track activity on **Patient**, **MedicalFile**, and **Summary** data.
- **Vector** can have multiple vectors for the same **Patient** and **Doctor**.

The ERD will provide a graphical description of how each one of the data elements is connected, via a NoSQL database.

<img width="2114" height="2386" alt="pic" src="https://github.com/user-attachments/assets/aa22878c-552b-44cc-9639-43cf5d6eb0ad" />

## Security Plan

### **Access Control:**
- **Role-Based Access Control (RBAC)**: Users shall be assigned roles (e.g., admin, doctors, and patients) with different levels of access based on their responsibilities.

### **Authentication:**
- Users shall need Multi-Factor Authentication (MFA) to gain access to the system, ensuring access to sensitive data is safe.

### **Data Encryption:**
- **At Rest**: All sensitive data will be encrypted when stored on servers, using strong encryption methods.
- **In Transit**: In-transit data over the internet will be encrypted with TLS, ensuring it cannot be intercepted.

### **Backup and Redundancy:**
- Data will be routinely backed up, encrypted, and kept in a location other than one place to ensure data recoverability in case of failure.

### **Compliance with HIPAA:**
- We will follow HIPAA guidelines to safeguard patient data and process it securely, as required by health information privacy law.

### **Audit Logging:**
- Any action in the system will be logged with complete transparency, ensuring accountability.

## Mapping of Functional Requirements

| **Functional Requirement** | **Data Storage Component**                       |
|----------------------------|-------------------------------------------------|
| Store and maintain user information (e.g., login credentials, roles) | **User Table**                                   |
| Store and maintain patient details | **Patient Table**                              |
| Store the metadata of medical files (e.g., images, reports) | **MedicalFile Table**                           |
| Store AI-generated summaries of medical files | **Summary Table**                             |
| Store system activity in audit logs | **AuditLog Table**                              |
| Store files securely with encryption | **Local Storage (Encrypted)**                  |
| Store vector embeddings related to medical files, including references to patients and doctors | **Vector Table** (contains `patient_id`, `doctor_id`, `vector`) |

---

