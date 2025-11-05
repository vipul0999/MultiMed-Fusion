# Basic SQL Schema and Summay Query

```sql
DROP VIEW IF EXISTS summary;
DROP VIEW IF EXISTS get_patient_event_count;
DROP TABLE IF EXISTS fusion_event;
DROP TABLE IF EXISTS patient;

CREATE TABLE patient (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  mrn TEXT NOT NULL UNIQUE
);

CREATE TABLE fusion_event (
  id INTEGER PRIMARY KEY,
  patient_id INTEGER NOT NULL REFERENCES patient(id) ON DELETE CASCADE,
  modality TEXT NOT NULL CHECK (modality IN ('lab','note','image')),
  content TEXT NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_fusion_event_patient_id ON fusion_event(patient_id);

INSERT INTO patient (id, name, mrn) VALUES
  (1, 'Charan', 'MRN001'),
  (2, 'Hasini', 'MRN002');

INSERT INTO fusion_event (id, patient_id, modality, content) VALUES
  (1, 1, 'lab', 'HbA1c=6.8'),
  (2, 1, 'note', 'Shortness of breath'),
  (3, 2, 'image', 'Chest X-ray normal');

CREATE VIEW summary AS
SELECT
  p.name,
  COUNT(f.id) AS total_events,
  MAX(f.created_at) AS last_event_at
FROM patient p
LEFT JOIN fusion_event f ON f.patient_id = p.id
GROUP BY p.name;

-- "Function" substitute for SQLite: a view returning per-patient counts
CREATE VIEW get_patient_event_count AS
SELECT
  p.name AS patient_name,
  COUNT(f.id) AS event_count
FROM patient p
LEFT JOIN fusion_event f ON f.patient_id = p.id
GROUP BY p.name;

-- Examples
SELECT * FROM summary;
SELECT * FROM get_patient_event_count WHERE patient_name = 'Charan';

SELECT * FROM summary;
