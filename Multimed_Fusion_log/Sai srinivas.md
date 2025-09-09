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
