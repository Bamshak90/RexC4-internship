import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS mentioned_messages (
    id SERIAL PRIMARY KEY,
    message_id BIGINT NOT NULL,
    message_text TEXT,
    user_id BIGINT NOT NULL,
    username VARCHAR(255),
    first_name VARCHAR(255),
    group_id BIGINT,
    group_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS group_creators (
    id SERIAL PRIMARY KEY,
    group_id BIGINT UNIQUE NOT NULL,
    group_name VARCHAR(255),
    added_by_user_id BIGINT,
    added_by_username VARCHAR(255),
    added_by_full_name VARCHAR(255),
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS message_counters (
    id SERIAL PRIMARY KEY,
    chat_type VARCHAR(50) NOT NULL,
    chat_id BIGINT UNIQUE NOT NULL,
    total_count BIGINT DEFAULT 0
);
""")

conn.commit()

cur.close()
conn.close()

print("Tables created successfully.")