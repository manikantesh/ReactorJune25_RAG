"""
Database Setup Script for Legal AI Assistant

Initializes the PostgreSQL database and creates necessary tables.
"""

import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost:5432/legal_ai_db')

def create_tables():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    # Create cases table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS cases (
        id SERIAL PRIMARY KEY,
        case_name TEXT,
        court TEXT,
        date DATE,
        jurisdiction TEXT,
        case_type TEXT,
        citation TEXT,
        judges TEXT,
        parties TEXT,
        key_facts TEXT,
        legal_issues TEXT,
        holding TEXT,
        reasoning TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')
    
    # Create precedents table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS precedents (
        id SERIAL PRIMARY KEY,
        case_id INTEGER REFERENCES cases(id),
        precedent_text TEXT,
        analysis TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')
    
    conn.commit()
    cur.close()
    conn.close()
    print("Database tables created successfully.")

if __name__ == "__main__":
    create_tables() 