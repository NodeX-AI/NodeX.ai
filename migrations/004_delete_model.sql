-- API больше не предоставляет доступ к модели minimax_m2
-- Меняем модель у пользователей
UPDATE users 
SET current_model = 'grok4fast' 
WHERE current_model = 'minimax';

-- Удаляем историю сообщений с этой моделью
DELETE FROM messages 
WHERE model_used = 'minimax';