# Basic SQL Schema and Summay Query

```sql
CREATE TABLE patient (
  id INTEGER PRIMARY KEY,
  name TEXT,
  mrn TEXT
);

CREATE TABLE fusion_event (
  id INTEGER PRIMARY KEY,
  patient_id INTEGER REFERENCES patient(id),
  modality TEXT,
  content TEXT
);

INSERT INTO patient VALUES
  (1, 'Charan', 'MRN001'),
  (2, 'Hasini', 'MRN002');

INSERT INTO fusion_event VALUES
  (1, 1, 'lab', 'HbA1c=6.8'),
  (2, 1, 'note', 'Shortness of breath'),
  (3, 2, 'image', 'Chest X-ray normal');

CREATE VIEW summary AS
SELECT 
  p.name,
  COUNT(f.id) AS total_events
FROM patient p
LEFT JOIN fusion_event f ON f.patient_id = p.id
GROUP BY p.name;

SELECT * FROM summary;
