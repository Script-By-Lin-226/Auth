"""
Vercel serverless function entry point
"""
import sys
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set Vercel environment variable
os.environ["VERCEL"] = "1"

try:
    # Import models first to register them with Base
    from app.models.user import User
    from app.models.post import Post
    
    # Import app (this will import database and create engine)
    from app.app import app
    
    # Initialize database tables lazily (only when needed)
    # Don't fail if connection fails at startup - let it fail on first request
    def init_db_lazy():
        try:
            from app.core.database import Base, engine
            # Import all models to register them
            from app.models.user import User
            from app.models.post import Post
            Base.metadata.create_all(bind=engine, checkfirst=True)
            logger.info("Database tables initialized")
        except Exception as e:
            logger.warning(f"Database initialization deferred: {e}")
            # Don't raise - will be initialized on first request
    
    # Try to initialize, but don't fail if it doesn't work
    try:
        init_db_lazy()
    except Exception as e:
        logger.warning(f"Database initialization failed at startup: {e}")
        # Continue anyway - will be retried on first database request
    
    # Export the app for Vercel
    handler = app
    
except Exception as e:
    # Better error handling for debugging
    import traceback
    error_msg = f"Error initializing app: {e}"
    logger.error(error_msg)
    logger.error(traceback.format_exc())
    # Create a minimal error app to show the error
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    
    error_app = FastAPI()
    
    @error_app.get("/{full_path:path}")
    async def error_handler(full_path: str):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Application initialization failed",
                "message": str(e),
                "detail": "Check Vercel function logs for more details"
            }
        )
    
    handler = error_app

