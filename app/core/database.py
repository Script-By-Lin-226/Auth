from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
import os

# SET UP DATABASE URL
try:
    DATABASE_URL = settings.DATABASE_URL
except Exception as e:
    print(f"Error getting DATABASE_URL from settings: {e}")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Determine if we're using PostgreSQL or SQLite
is_postgres = DATABASE_URL and (DATABASE_URL.startswith('postgresql://') or DATABASE_URL.startswith('postgres://'))

# SQL ENGINE configuration
try:
    if is_postgres:
        # PostgreSQL configuration (for Neon, Supabase, etc.)
        # Neon requires SSL, so we ensure it's enabled
        if 'sslmode' not in DATABASE_URL:
            # Add SSL mode if not present
            separator = '&' if '?' in DATABASE_URL else '?'
            DATABASE_URL = f"{DATABASE_URL}{separator}sslmode=require"
        
        # Try to use psycopg (v3) first - pure Python, works better on Vercel
        # Convert postgresql:// to postgresql+psycopg:// for psycopg v3
        try:
            import psycopg  # noqa: F401
            # Use psycopg v3 (pure Python, works better on Vercel)
            if DATABASE_URL.startswith('postgresql://'):
                DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgresql+psycopg://', 1)
            elif DATABASE_URL.startswith('postgres://'):
                DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql+psycopg://', 1)
            print("✅ Using psycopg v3 driver (pure Python)")
        except ImportError:
            # Fallback to psycopg2 if psycopg v3 not available
            try:
                import psycopg2  # noqa: F401
                print("✅ Using psycopg2 driver")
            except ImportError:
                print("⚠️ Warning: Neither psycopg nor psycopg2 found. Database may not work.")
                raise ImportError("No PostgreSQL driver found. Install psycopg[binary] or psycopg2-binary")
        
        # For serverless, use connection pooling with smaller pool size
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,  # Verify connections before using
            pool_recycle=300,    # Recycle connections after 5 minutes
            pool_size=1,         # Small pool for serverless
            max_overflow=0,      # No overflow for serverless
            echo=False,
            connect_args={
                "connect_timeout": 10,  # 10 second timeout
            } if 'psycopg' in DATABASE_URL else {}
        )
    else:
        # SQLite configuration (for local development)
        engine = create_engine(
            DATABASE_URL,
            connect_args={'check_same_thread': False}
        )
except Exception as e:
    print(f"Error creating database engine: {e}")
    # Create a dummy engine that will fail gracefully
    engine = None

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) if engine else None

Base = declarative_base()

