# Patient Metric Extraction and Snapshot Generator

```sql
DROP VIEW IF EXISTS v_patient_health_snapshot;
DROP VIEW IF EXISTS v_patient_alerts;
DROP VIEW IF EXISTS v_latest_metric_per_patient;
DROP VIEW IF EXISTS v_metric_values;
DROP TABLE IF EXISTS fusion_event;
DROP TABLE IF EXISTS patient;

CREATE TABLE patient(id INTEGER PRIMARY KEY,name TEXT NOT NULL,mrn TEXT UNIQUE);
CREATE TABLE fusion_event(id INTEGER PRIMARY KEY,patient_id INTEGER NOT NULL,modality TEXT NOT NULL,content TEXT NOT NULL,created_at TEXT NOT NULL,FOREIGN KEY(patient_id) REFERENCES patient(id));

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
SELECT p.name AS patient_name,
       LOWER(TRIM(SUBSTR(f.content,1,INSTR(f.content,'=')-1))) AS metric,
       REPLACE(TRIM(SUBSTR(f.content,INSTR(f.content,'=')+1)),'%','') AS value_raw,
       CAST(REPLACE(TRIM(SUBSTR(f.content,INSTR(f.content,'=')+1)),'%','') AS REAL) AS value_num,
       f.created_at
FROM patient p JOIN fusion_event f ON f.patient_id=p.id
WHERE INSTR(f.content,'=')>0;

CREATE VIEW v_latest_metric_per_patient AS
SELECT patient_name,metric,value_raw,value_num,created_at AS last_seen_at
FROM (
  SELECT v.*,ROW_NUMBER() OVER(PARTITION BY patient_name,metric ORDER BY created_at DESC) rn
  FROM v_metric_values v
) WHERE rn=1;

CREATE VIEW v_patient_alerts AS
WITH mt(metric,min_ok,max_ok,delta_warn) AS (
  VALUES ('hba1c',4.0,6.0,0.3),('spo2',95.0,100.0,2.0),('crp',0.0,10.0,3.0),('hr',50.0,100.0,15.0),('ldl',0.0,100.0,20.0)
),
ranked AS (
  SELECT v.*,
         LAG(value_num) OVER(PARTITION BY patient_name,metric ORDER BY created_at DESC) AS prev_value,
         ROW_NUMBER() OVER(PARTITION BY patient_name,metric ORDER BY created_at DESC) AS rn
  FROM v_metric_values v
)
SELECT r.patient_name,r.metric,r.value_num,r.prev_value,(r.value_num-r.prev_value) AS delta,
       CASE
         WHEN r.value_num<mt.min_ok OR r.value_num>mt.max_ok THEN 'out_of_range'
         WHEN r.prev_value IS NOT NULL AND ABS(r.value_num-r.prev_value)>=mt.delta_warn THEN 'jump'
         ELSE 'ok'
       END AS status
FROM ranked r LEFT JOIN mt ON mt.metric=r.metric
WHERE r.rn=1;

CREATE VIEW v_patient_health_snapshot AS
SELECT patient_name,
       GROUP_CONCAT(metric||':'||printf('%g',value_num)||
         CASE status WHEN 'ok' THEN '' ELSE '('||status||')' END,' | ') AS latest_metrics
FROM (
  SELECT patient_name,metric,value_num,status
  FROM v_patient_alerts
  ORDER BY patient_name,metric
) GROUP BY patient_name;

SELECT * FROM v_metric_values;
SELECT * FROM v_latest_metric_per_patient;
SELECT * FROM v_patient_alerts;
SELECT * FROM v_patient_health_snapshot;_metric_per_patient;
SELECT * FROM v_patient_health_snapshot;
