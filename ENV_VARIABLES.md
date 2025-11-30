# Environment Variables Guide

## Required Environment Variables

These are **essential** for your app to work properly:

### 1. SECRET_KEY
**Required: YES** | **Type: String**

A secret key used for:
- Session management
- JWT token signing
- Cookie encryption

**How to generate:**
```bash
# Using Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Or using OpenSSL
openssl rand -hex 32
```

**Example:**
```
SECRET_KEY=your-super-secret-key-minimum-32-characters-long-random-string
```

**⚠️ Important:** Never commit this to Git! Use a strong, random string.

---

### 2. DATABASE_URL
**Required: YES** | **Type: String**

Database connection string. Format depends on your database:

**For SQLite (Development only - not recommended for production):**
```
DATABASE_URL=sqlite:///./test.db
```

**For PostgreSQL (Recommended for production):**
```
DATABASE_URL=postgresql://username:password@host:port/database_name
```

**For Vercel Postgres:**
```
DATABASE_URL=postgres://default:password@host.vercel-storage.com:5432/verceldb
```

**For Supabase:**
```
DATABASE_URL=postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres
```

**For PlanetScale:**
```
DATABASE_URL=mysql://username:password@host.planetscale.com/database?sslaccept=strict
```

---

## Optional Environment Variables

These have default values but can be customized:

### 3. ALGORITHM
**Required: NO** | **Default: `HS256`** | **Type: String**

JWT token algorithm. Usually keep as `HS256`:
```
ALGORITHM=HS256
```

---

### 4. ACCESS_TOKEN_EXPIRE_MINUTES
**Required: NO** | **Default: `60`** | **Type: Integer**

How long access tokens are valid (in minutes):
```
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

**Recommended values:**
- Development: `60` (1 hour)
- Production: `30` (30 minutes) or `15` (15 minutes) for better security

---

### 5. REFRESH_TOKEN_EXPIRE_DAYS
**Required: NO** | **Default: `7`** | **Type: Integer**

How long refresh tokens are valid (in days):
```
REFRESH_TOKEN_EXPIRE_DAYS=7
```

**Recommended values:**
- Development: `7` (1 week)
- Production: `30` (1 month) or `7` (1 week)

---

### 6. ALLOWED_ORIGINS
**Required: NO** | **Default: `*` (all origins)** | **Type: String (comma-separated)**

CORS allowed origins. For production, specify your domain:
```
ALLOWED_ORIGINS=https://your-app.vercel.app,https://www.yourdomain.com
```

**For multiple origins (comma-separated, no spaces):**
```
ALLOWED_ORIGINS=https://app1.vercel.app,https://app2.vercel.app
```

**For development (allow all):**
```
ALLOWED_ORIGINS=*
```

---

## Complete Example for Vercel

Here's a complete example of all environment variables you should set:

```env
# Required
SECRET_KEY=your-generated-secret-key-here-minimum-32-chars
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Optional (with recommended values)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
ALLOWED_ORIGINS=https://your-app.vercel.app
```

---

## How to Set in Vercel

### Method 1: Vercel Dashboard

1. Go to your project on [Vercel Dashboard](https://vercel.com/dashboard)
2. Click on your project
3. Go to **Settings** → **Environment Variables**
4. Click **Add New**
5. Enter the variable name and value
6. Select environments (Production, Preview, Development)
7. Click **Save**
8. **Redeploy** your application

### Method 2: Vercel CLI

```bash
# Set a single variable
vercel env add SECRET_KEY

# Set multiple variables
vercel env add SECRET_KEY production
vercel env add DATABASE_URL production
vercel env add ALGORITHM production
```

---

## Environment-Specific Values

You can set different values for different environments:

### Production
```env
SECRET_KEY=production-secret-key
DATABASE_URL=postgresql://prod-db-url
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=https://your-app.vercel.app
```

### Preview (for pull requests)
```env
SECRET_KEY=preview-secret-key
DATABASE_URL=postgresql://preview-db-url
ACCESS_TOKEN_EXPIRE_MINUTES=60
ALLOWED_ORIGINS=*
```

### Development
```env
SECRET_KEY=dev-secret-key
DATABASE_URL=sqlite:///./test.db
ACCESS_TOKEN_EXPIRE_MINUTES=60
ALLOWED_ORIGINS=*
```

---

## Quick Setup Checklist

- [ ] Generate a secure `SECRET_KEY` (32+ characters)
- [ ] Set up a production database (PostgreSQL recommended)
- [ ] Get your `DATABASE_URL` from your database provider
- [ ] Set `ALLOWED_ORIGINS` to your production domain
- [ ] Add all variables to Vercel
- [ ] Redeploy your application
- [ ] Test that everything works

---

## Security Best Practices

1. **Never commit secrets to Git** - Use environment variables
2. **Use strong SECRET_KEY** - Minimum 32 characters, random
3. **Use HTTPS in production** - Already configured
4. **Limit ALLOWED_ORIGINS** - Don't use `*` in production
5. **Use shorter token expiration** - Better security
6. **Rotate SECRET_KEY periodically** - Especially if compromised

---

## Troubleshooting

### "SECRET_KEY not set" error
- Make sure you've added `SECRET_KEY` in Vercel
- Redeploy after adding environment variables

### Database connection errors
- Check `DATABASE_URL` format is correct
- Verify database credentials
- Ensure database is accessible from Vercel

### CORS errors
- Check `ALLOWED_ORIGINS` includes your domain
- Make sure no trailing slashes in URLs
- Verify HTTPS is used in production

---

## Database Setup Recommendations

### Option 1: Vercel Postgres (Easiest)
1. Go to Vercel Dashboard → Your Project → Storage
2. Create a Postgres database
3. Copy the connection string
4. Use as `DATABASE_URL`

### Option 2: Supabase (Free tier available)
1. Create account at [supabase.com](https://supabase.com)
2. Create a new project
3. Go to Settings → Database
4. Copy the connection string
5. Use as `DATABASE_URL`

### Option 3: Railway (Simple setup)
1. Create account at [railway.app](https://railway.app)
2. Create a PostgreSQL service
3. Copy the connection string
4. Use as `DATABASE_URL`

