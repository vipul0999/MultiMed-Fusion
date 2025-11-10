# Patient Metric Extraction and Snapshot Generator

```sql
DROP VIEW IF EXISTS v_patient_health_snapshot;
DROP VIEW IF EXISTS v_latest_metric_per_patient;
DROP VIEW IF EXISTS v_metric_values;
DROP TABLE IF EXISTS fusion_event;
DROP TABLE IF EXISTS patient;

CREATE TABLE patient(id INTEGER PRIMARY KEY, name TEXT NOT NULL, mrn TEXT UNIQUE);
CREATE TABLE fusion_event(
  id INTEGER PRIMARY KEY,
  patient_id INTEGER NOT NULL,
  modality TEXT NOT NULL,
  content TEXT NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY(patient_id) REFERENCES patient(id)
);

INSERT INTO patient VALUES
  (1,'Karthik','MRN001'),
  (2,'Pavan','MRN002'),
  (3,'Mohit','MRN003');

INSERT INTO fusion_event VALUES
  (201,1,'lab','HbA1c=7.1','2025-11-10 08:05'),
  (202,1,'vitals','SpO2=93%','2025-11-10 08:20'),
  (203,2,'lab','CRP=5.0','2025-11-10 09:10'),
  (204,2,'vitals','HR=88','2025-11-10 09:15'),
  (205,3,'lab','LDL=118','2025-11-10 10:00'),
  (206,1,'lab','HbA1c=6.9','2025-11-10 12:00'),
  (207,3,'vitals','SpO2=97%','2025-11-10 12:30');

CREATE VIEW v_metric_values AS
SELECT
  p.name AS patient_name,
  LOWER(TRIM(SUBSTR(f.content, 1, INSTR(f.content,'=')-1))) AS metric,
  REPLACE(TRIM(SUBSTR(f.content, INSTR(f.content,'=')+1)), '%', '') AS value_raw,
  CAST(REPLACE(TRIM(SUBSTR(f.content, INSTR(f.content,'=')+1)), '%', '') AS REAL) AS value_num,
  f.created_at
FROM patient p
JOIN fusion_event f ON f.patient_id = p.id
WHERE INSTR(f.content,'=') > 0;

CREATE VIEW v_latest_metric_per_patient AS
SELECT v1.patient_name, v1.metric, v1.value_raw, v1.value_num, v1.created_at AS last_seen_at
FROM v_metric_values v1
WHERE v1.created_at = (
  SELECT MAX(v2.created_at)
  FROM v_metric_values v2
  WHERE v2.patient_name = v1.patient_name AND v2.metric = v1.metric
);

CREATE VIEW v_patient_health_snapshot AS
SELECT
  patient_name,
  GROUP_CONCAT(metric || ':' || value_raw, ' | ') AS latest_metrics
FROM (
  SELECT patient_name, metric, value_raw
  FROM v_latest_metric_per_patient
  ORDER BY patient_name, metric
)
GROUP BY patient_name;

SELECT * FROM v_metric_values;
SELECT * FROM v_latest_metric_per_patient;
SELECT * FROM v_patient_health_snapshot;
