CREATE DATABASE IF NOT EXISTS complaint_system;
USE complaint_system;

CREATE TABLE IF NOT EXISTS complaints (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255),
  department VARCHAR(100),
  category VARCHAR(100),
  description TEXT,
  priority VARCHAR(50),
  status VARCHAR(50) DEFAULT 'Pending',
  notes TEXT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  file_url VARCHAR(255)
);

-- MySQL (prior to v8.0.29): You can't use IF NOT EXISTS for columns.
-- Before running the next line, always check if the 'email' column exists.
-- To check, run:
--   DESCRIBE complaints;
-- If 'email' is NOT present in the results, run the following:
-- ALTER TABLE complaints ADD COLUMN email VARCHAR(255);

SHOW DATABASES;
SHOW TABLES;
DESCRIBE complaints;

-- Example insert (uncomment to use)
-- INSERT INTO complaints (name, department, category, description, priority)
-- VALUES ('Rahul', 'IT', 'Network', 'Wi-Fi not working', 'High');

SELECT * FROM complaints;