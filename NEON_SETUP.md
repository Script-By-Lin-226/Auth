# Neon Database Setup Guide

## Setting up Neon Database for Vercel

### Step 1: Create Neon Database

1. Go to [Neon Console](https://console.neon.tech)
2. Sign up or log in
3. Create a new project
4. Note your connection string

### Step 2: Get Connection String

Neon provides connection strings in this format:
```
postgresql://username:password@ep-xxxxx.us-east-2.aws.neon.tech/neondb?sslmode=require
```

### Step 3: Set Environment Variable in Vercel

1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add `DATABASE_URL` with your Neon connection string
3. Make sure to include `?sslmode=require` at the end
4. Select **Production**, **Preview**, and **Development** environments
5. Click **Save**

### Step 4: Verify Connection String Format

Your `DATABASE_URL` should look like:
```
postgresql://username:password@ep-xxxxx.region.aws.neon.tech/neondb?sslmode=require
```

**Important:**
- Must start with `postgresql://` or `postgres://`
- Must include `?sslmode=require` for SSL
- No spaces in the connection string

### Step 5: Initialize Database Tables

The app will automatically create tables on first run. If you need to manually initialize:

```python
# Run this once to create tables
from app.core.database_init import init_db
init_db()
```

Or the app will create them automatically when it starts.

## Troubleshooting

### Error: "connection refused" or "timeout"
- Check your Neon connection string is correct
- Verify `sslmode=require` is in the URL
- Check Neon dashboard to ensure database is active

### Error: "relation does not exist"
- Tables haven't been created yet
- The app will create them automatically on first request
- Or run the initialization script manually

### Error: "SSL connection required"
- Make sure `?sslmode=require` is in your DATABASE_URL
- Neon requires SSL connections

### Error: "FUNCTION_INVOCATION_FAILED"
- Check Vercel function logs for detailed error
- Verify all environment variables are set
- Check that `psycopg2-binary` is in requirements.txt
- Ensure DATABASE_URL format is correct

## Connection String Examples

### Standard Neon Connection
```
postgresql://user:password@ep-xxxxx.us-east-2.aws.neon.tech/neondb?sslmode=require
```

### With Pooling (Recommended for serverless)
```
postgresql://user:password@ep-xxxxx-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require
```

**Note:** Use the pooler endpoint for better performance with serverless functions.

## Environment Variables Checklist

Make sure you have these set in Vercel:

- [ ] `SECRET_KEY` - Random secure string
- [ ] `DATABASE_URL` - Your Neon connection string with `?sslmode=require`
- [ ] `ALGORITHM` - `HS256` (optional)
- [ ] `ACCESS_TOKEN_EXPIRE_MINUTES` - `60` (optional)
- [ ] `REFRESH_TOKEN_EXPIRE_DAYS` - `7` (optional)

## Testing Connection

After deployment, test your connection by:
1. Visiting your Vercel URL
2. Try to register a new user
3. Check Vercel function logs for any errors

## Common Issues

### Issue: Database tables not created
**Solution:** The app creates tables automatically. If they don't exist, check:
- Database connection is working
- User has CREATE TABLE permissions
- Check Vercel logs for errors

### Issue: Connection pool exhausted
**Solution:** Use Neon's connection pooler endpoint (ends with `-pooler`)

### Issue: Slow queries
**Solution:** 
- Use connection pooler
- Enable `pool_pre_ping` (already configured)
- Set appropriate `pool_recycle` (already set to 300 seconds)

