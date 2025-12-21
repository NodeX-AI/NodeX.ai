ALTER TABLE users 
ALTER COLUMN current_model DROP DEFAULT;

ALTER TABLE users 
ALTER COLUMN current_model SET DEFAULT 'grok4fast';
