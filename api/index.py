"""
Vercel serverless function entry point
"""
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set Vercel environment variable
os.environ["VERCEL"] = "1"

# Import with minimal error handling
try:
    # Import app - this will handle all initialization
    from app.app import app
    handler = app
except Exception as e:
    # If import fails, create a minimal error handler
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    import traceback
    
    error_app = FastAPI(title="Error App")
    
    @error_app.get("/{full_path:path}")
    async def error_handler(full_path: str):
        error_detail = str(e)
        trace = traceback.format_exc()
        return JSONResponse(
            status_code=500,
            content={
                "error": "Application failed to initialize",
                "message": error_detail,
                "traceback": trace,
                "help": "Check Vercel function logs for environment variable issues"
            }
        )
    
    handler = error_app

