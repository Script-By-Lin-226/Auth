from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
import os

# SET UP DATABASE URL
DATABASE_URL = settings.DATABASE_URL

# Determine if we're using PostgreSQL or SQLite
is_postgres = DATABASE_URL.startswith('postgresql://') or DATABASE_URL.startswith('postgres://')

# SQL ENGINE configuration
if is_postgres:
    # PostgreSQL configuration (for Neon, Supabase, etc.)
    # Neon requires SSL, so we ensure it's enabled
    if 'sslmode' not in DATABASE_URL:
        # Add SSL mode if not present
        separator = '&' if '?' in DATABASE_URL else '?'
        DATABASE_URL = f"{DATABASE_URL}{separator}sslmode=require"
    
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Verify connections before using
        pool_recycle=300,    # Recycle connections after 5 minutes
        echo=False
    )
else:
    # SQLite configuration (for local development)
    engine = create_engine(
        DATABASE_URL,
        connect_args={'check_same_thread': False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

