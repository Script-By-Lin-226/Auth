"""
Database initialization script
Run this to initialize the database schema
"""
from app.core.database import Base, engine
from app.models.user import User
from app.models.post import Post

def init_db():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine, checkfirst=True)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise

if __name__ == "__main__":
    init_db()

