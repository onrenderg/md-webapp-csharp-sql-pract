import os
import asyncio
import re
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

# Set environment variable directly in the file
os.environ['DATABASE_URL'] = (
    "postgresql://neondb_owner:npg_cgKWXQH35abk@ep-summer-hall-a1ljuhxz-pooler.ap-southeast-1.aws.neon.tech/neondb"
)

async def async_main() -> None:
    # Use asyncpg dialect for SQLAlchemy
    db_url = re.sub(r'^postgresql:', 'postgresql+asyncpg:', os.getenv('DATABASE_URL'))

    # Create an async SQLAlchemy engine
    engine = create_async_engine(db_url, echo=True)

    async with engine.connect() as conn:
        # Query to list all user tables
        query = text("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_type = 'BASE TABLE' AND table_schema NOT IN ('pg_catalog', 'information_schema');
        """)
        result = await conn.execute(query)
        tables = result.fetchall()

        print("Tables in the database:")
        for schema, name in tables:
            print(f"- {schema}.{name}")

    await engine.dispose()

# Run the async function
asyncio.run(async_main())

# pip install sqlalchemy asyncpg



# output 
⚡ ~ python sql.py
# 2025-09-09 06:03:15,975 INFO sqlalchemy.engine.Engine select pg_catalog.version()
# 2025-09-09 06:03:15,976 INFO sqlalchemy.engine.Engine [raw sql] ()
# 2025-09-09 06:03:16,846 INFO sqlalchemy.engine.Engine select current_schema()
# 2025-09-09 06:03:16,846 INFO sqlalchemy.engine.Engine [raw sql] ()
# 2025-09-09 06:03:17,716 INFO sqlalchemy.engine.Engine show standard_conforming_strings
# 2025-09-09 06:03:17,716 INFO sqlalchemy.engine.Engine [raw sql] ()
# 2025-09-09 06:03:18,371 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2025-09-09 06:03:18,371 INFO sqlalchemy.engine.Engine
#             SELECT table_schema, table_name
#             FROM information_schema.tables
#             WHERE table_type = 'BASE TABLE' AND table_schema NOT IN ('pg_catalog', 'information_schema');

# 2025-09-09 06:03:18,371 INFO sqlalchemy.engine.Engine [generated in 0.00029s] ()
# Tables in the database:
# - public.places
# 2025-09-09 06:03:19,057 INFO sqlalchemy.engine.Engine ROLLBACK
# ⚡ ~
# ⚡ ~ 