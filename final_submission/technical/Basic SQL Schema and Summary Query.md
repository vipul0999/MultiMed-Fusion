# Basic SQL Schema and Summay Query

```sql
DROP VIEW IF EXISTS summary;
DROP VIEW IF EXISTS get_patient_event_count;
DROP VIEW IF EXISTS get_patient_latest_event_detail;
DROP TABLE IF EXISTS fusion_event;
DROP TABLE IF EXISTS patient;

CREATE TABLE patient(id INT PRIMARY KEY,name TEXT,mrn TEXT UNIQUE);
CREATE TABLE fusion_event(id INT PRIMARY KEY,patient_id INT,modality TEXT,content TEXT,created_at TEXT);

INSERT INTO patient VALUES(1,'Charan','MRN001'),(2,'Hasini','MRN002');
INSERT INTO fusion_event VALUES
(1,1,'lab','HbA1c=6.8','2025-11-07 10:00'),
(2,1,'note','Shortness of breath','2025-11-07 12:00'),
(3,2,'image','Chest X-ray normal','2025-11-07 09:30');

CREATE VIEW summary AS
SELECT p.name,COUNT(f.id) total_events,MAX(f.created_at) last_event_at
FROM patient p LEFT JOIN fusion_event f ON f.patient_id=p.id GROUP BY p.name;

CREATE VIEW get_patient_event_count AS
SELECT p.name patient_name,COUNT(f.id) event_count
FROM patient p LEFT JOIN fusion_event f ON f.patient_id=p.id GROUP BY p.name;

CREATE VIEW get_patient_latest_event_detail AS
SELECT p.name patient_name,f.modality,f.content,f.created_at last_event_at
FROM patient p LEFT JOIN fusion_event f ON f.id=(
  SELECT f2.id FROM fusion_event f2 WHERE f2.patient_id=p.id ORDER BY f2.created_at DESC LIMIT 1
);

SELECT * FROM summary;
SELECT * FROM get_patient_event_count;
SELECT * FROM get_patient_latest_event_detail;

