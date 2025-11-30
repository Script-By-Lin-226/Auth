# Deployment Guide for Vercel

## Prerequisites
- Vercel account
- Git repository (GitHub, GitLab, or Bitbucket)

## Environment Variables

Set these in your Vercel project settings:

```
SECRET_KEY=your-secret-key-here (use a strong random string)
DATABASE_URL=your-database-url (for production, use PostgreSQL or similar)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
```

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

