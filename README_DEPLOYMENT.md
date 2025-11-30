# Deployment Guide for Vercel

## Prerequisites
- Vercel account
- Git repository (GitHub, GitLab, or Bitbucket)

## Environment Variables

### Required Variables

**SECRET_KEY** (Required)
- Generate a secure random string (minimum 32 characters)
- Used for session management and JWT signing
- Generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`

**DATABASE_URL** (Required)
- PostgreSQL connection string for production
- Format: `postgresql://username:password@host:port/database_name`
- See [ENV_VARIABLES.md](./ENV_VARIABLES.md) for database setup options

### Optional Variables (with defaults)

```
ALGORITHM=HS256                          # JWT algorithm (default: HS256)
ACCESS_TOKEN_EXPIRE_MINUTES=60            # Token expiration (default: 60)
REFRESH_TOKEN_EXPIRE_DAYS=7               # Refresh token expiration (default: 7)
ALLOWED_ORIGINS=https://your-app.vercel.app  # CORS origins (default: *)
```

**📖 For detailed environment variable guide, see [ENV_VARIABLES.md](./ENV_VARIABLES.md)**

## Deployment Steps

1. **Install Vercel CLI** (optional):
   ```bash
   npm i -g vercel
   ```

2. **Deploy to Vercel**:
   ```bash
   vercel
   ```

   Or connect your GitHub repository to Vercel dashboard.

3. **Set Environment Variables**:
   - Go to your Vercel project settings
   - Navigate to "Environment Variables"
   - Add all required variables

4. **Redeploy** after setting environment variables

## Database Setup

For production, you'll need a proper database. Options:
- **Vercel Postgres** (recommended)
- **Supabase**
- **PlanetScale**
- **Railway**

Update `DATABASE_URL` in environment variables accordingly.

## File Structure

```
/
├── api/
│   └── index.py          # Vercel serverless function
├── app/
│   ├── app.py            # FastAPI app
│   └── templates/       # Frontend files
├── vercel.json          # Vercel configuration
└── requirements.txt     # Python dependencies
```

## Notes

- The app automatically detects if it's running on Vercel
- API routes are prefixed with `/api` on Vercel
- Static files are served from `/static`
- HTML pages are served from root routes

## Troubleshooting

1. **Import errors**: Make sure all dependencies are in `requirements.txt`
2. **Database errors**: Check `DATABASE_URL` is set correctly
3. **CORS issues**: Already configured in `app.py`
4. **Static files not loading**: Check `vercel.json` routes configuration

