ALTER TABLE users 
ALTER COLUMN image_model DROP DEFAULT;

ALTER TABLE users 
ALTER COLUMN image_model SET DEFAULT 'grok4fast';
