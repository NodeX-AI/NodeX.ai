ALTER TABLE users 
ADD COLUMN current_language VARCHAR(10) DEFAULT 'ru';
---
-- удаление модели gemma3

UPDATE users 
SET current_model = 'grok4fast' 
WHERE current_model = 'gemma';

DELETE FROM messages 
WHERE model_used = 'gemma';

-- удаление модели deepseek r1t2 chimera

UPDATE users 
SET current_model = 'grok4fast' 
WHERE current_model = 'deepseek';

DELETE FROM messages 
WHERE model_used = 'deepseek';

-- удаление модели nemotron nano 9b v2

UPDATE users 
SET current_model = 'grok4fast' 
WHERE current_model = 'nemotron';

DELETE FROM messages 
WHERE model_used = 'nemotron';

--