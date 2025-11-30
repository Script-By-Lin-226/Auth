"""
Vercel serverless function entry point
"""
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set Vercel environment variable
os.environ["VERCEL"] = "1"

try:
    from app.app import app
    
    # Initialize database tables on first import
    try:
        from app.core.database import Base, engine
        from app.models.user import User
        from app.models.post import Post
        Base.metadata.create_all(bind=engine, checkfirst=True)
    except Exception as e:
        # Log but don't fail - tables might already exist
        print(f"Database initialization: {e}")
    
    # Export the app for Vercel
    handler = app
except Exception as e:
    # Better error handling for debugging
    import traceback
    print(f"Error initializing app: {e}")
    print(traceback.format_exc())
    raise

