import asyncpg
from typing import Optional, List, Tuple

from config.config import PG_URL

class PostgresDB:
    def __init__(self):
        self.pool = None
    
    async def connect(self):
        self.pool = await asyncpg.create_pool(PG_URL)
    
    # === USER METHODS ===
    async def add_user(self, telegram_id: int) -> None: #
        async with self.pool.acquire() as conn:
            await conn.execute("INSERT INTO users (telegram_id) VALUES ($1) ON CONFLICT (telegram_id) DO NOTHING", telegram_id)
    
    async def get_user(self, telegram_id: int) -> Optional[asyncpg.Record]: #
        async with self.pool.acquire() as conn:
            return await conn.fetchrow("SELECT * FROM users WHERE telegram_id = $1", telegram_id)
    
    async def update_user_model(self, telegram_id: int, new_model: str) -> None: #
        async with self.pool.acquire() as conn:
            await conn.execute("UPDATE users SET current_model = $1 WHERE telegram_id = $2", new_model, telegram_id)
    
    async def get_user_model(self, telegram_id: int) -> Optional[str]: #
        async with self.pool.acquire() as conn:
            return await conn.fetchval("SELECT current_model FROM users WHERE telegram_id = $1", telegram_id)
        
    
    # === MESSAGE METHODS ===
    async def add_message(self, user_id: int, message_text: str, ai_response: str, model_used: str) -> int: #
        async with self.pool.acquire() as conn:
            return await conn.fetchval( "INSERT INTO messages (user_id, message_text, ai_response, model_used) VALUES ($1, $2, $3, $4) RETURNING id",
                                       user_id, message_text, ai_response, model_used)
    
    async def get_user_messages(self, telegram_id: int, limit: int = 10) -> List[asyncpg.Record]:
        async with self.pool.acquire() as conn:
            return await conn.fetch("SELECT m.message_text, m.ai_response, m.model_used, m.created_at FROM messages m JOIN users u ON m.user_id = u.telegram_id WHERE u.telegram_id = $1 ORDER BY m.created_at DESC LIMIT $2",
                                    telegram_id, limit) # DESC - sort in descending order
    
    async def get_user_recent_messages(self, telegram_id: int, model: str,limit: int = 10) -> List[Tuple[str, str]]: #
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("SELECT message_text, ai_response FROM messages WHERE user_id = $1 AND model_used = $2 ORDER BY created_at ASC LIMIT $3",
                                    telegram_id, model, limit) # ASC - sort in ascending order
            return [(row['message_text'], row['ai_response']) for row in rows]

    async def get_user_message_count(self, telegram_id: int) -> int: #
        async with self.pool.acquire() as conn:
            return await conn.fetchval("SELECT COUNT(*) FROM messages WHERE user_id = $1", telegram_id)
        
    # === STATISTICS METHODS === 
    async def get_user_stats(self, telegram_id: int) -> dict: #
        async with self.pool.acquire() as conn:
            total_messages = await conn.fetchval("SELECT COUNT(*) FROM messages WHERE user_id = $1", telegram_id)
            
            model_stats = await conn.fetch("SELECT model_used, COUNT(*) as count FROM messages WHERE user_id = $1 GROUP BY model_used", telegram_id)
            
            last_activity = await conn.fetchval("SELECT MAX(created_at) FROM messages WHERE user_id = $1", telegram_id)
            
            return {
                'total_messages': total_messages,
                'model_stats': {row['model_used']: row['count'] for row in model_stats},
                'last_activity': last_activity
            }
    
    async def get_global_stats(self) -> dict: #
        async with self.pool.acquire() as conn:
            total_users = await conn.fetchval("SELECT COUNT(*) FROM users")
            total_messages = await conn.fetchval("SELECT COUNT(*) FROM messages")
            popular_model = await conn.fetchval("SELECT model_used FROM messages GROUP BY model_used ORDER BY COUNT(*) DESC LIMIT 1")
            
            return {
                'total_users': total_users,
                'total_messages': total_messages,
                'popular_model': popular_model
            }
    
    # ===== ADMIN METHODS =====
    async def delete_user_messages(self, telegram_id: id) -> int: #
        async with self.pool.acquire() as conn:
            return await conn.execute("DELETE FROM messages WHERE user_id = $1", telegram_id)
    
    async def delete_user(self, telegram_id: int) -> bool: #
        async with self.pool.acquire() as conn:
            result = await conn.execute("DELETE FROM users WHERE telegram_id = $1", telegram_id)
            return "DELETE 1" in result
        
DB = PostgresDB()