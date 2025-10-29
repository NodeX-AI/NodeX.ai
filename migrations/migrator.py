import asyncpg
import asyncio
import os
from config.config import PG_URL
# Migrator is a script that must be run before the bot is launched in order to apply migrations.
async def apply_migrations():
    conn = await asyncpg.connect(PG_URL)
    
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS migrations (
            id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            applied_at TIMESTAMP DEFAULT NOW()
        )
    ''')
    
    applied = await conn.fetch("SELECT name FROM migrations")
    applied_names = {r['name'] for r in applied}
    
    migration_files = sorted([f for f in os.listdir('migrations') if f.endswith('.sql')])
    
    for filename in migration_files:
        if filename not in applied_names:
            print(f"Applying migration: {filename}")
            with open(f'migrations/{filename}', 'r') as f:
                sql = f.read()
                await conn.execute(sql)
                await conn.execute("INSERT INTO migrations (name) VALUES ($1)", filename)
                print(f"✅ Applied: {filename}")
    
    await conn.close()
    print("All migrations applied!")

if __name__ == "__main__":
    asyncio.run(apply_migrations())