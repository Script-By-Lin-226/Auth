import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from slowapi.middleware import SlowAPIMiddleware
from app.core.config import settings
from app.api.v1 import auth
from app.core.database import Base, engine
from app.middleware.rate_limit import limiter
import os

# Import models to register them with Base before creating tables
from app.models.user import User
from app.models.post import Post

# Create tables - handle both serverless and non-serverless
# This is done lazily - won't fail app startup if DB is unavailable
def init_database():
    try:
        Base.metadata.create_all(bind=engine, checkfirst=True)
    except Exception as e:
        # Log error but don't fail the app startup
        # Database will be initialized on first request
        import logging
        logging.warning(f"Database initialization deferred: {e}")

# Try to initialize, but don't block app startup
try:
    init_database()
except Exception:
    pass  # Will be retried on first database request

app = FastAPI(title="FastAPI", version="1.0")
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
# CORS configuration - update origins for production
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",") if os.getenv("ALLOWED_ORIGINS") else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    https_only=os.getenv("VERCEL") is not None,  # HTTPS only in production
    same_site="lax",
)

# Serve static files
static_dir = os.path.join(os.path.dirname(__file__), "templates", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Serve HTML files
templates_dir = os.path.join(os.path.dirname(__file__), "templates")

@app.get("/")
async def read_root():
    html_path = os.path.join(templates_dir, "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return {"message": "Welcome to FastAPI"}

@app.get("/login")
async def login_page():
    html_path = os.path.join(templates_dir, "login.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return {"message": "Login page"}

@app.get("/register")
async def register_page():
    html_path = os.path.join(templates_dir, "register.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return {"message": "Register page"}

@app.get("/feed-page")
async def feed_page():
    html_path = os.path.join(templates_dir, "feed.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return {"message": "Feed page"}

@app.get("/admin-panel")
async def admin_panel_page():
    html_path = os.path.join(templates_dir, "admin-panel.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return {"message": "Admin panel page"}

app.include_router(auth.router)

