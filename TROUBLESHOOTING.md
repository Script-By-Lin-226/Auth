# Troubleshooting 500 Errors on Vercel

## Common Causes and Solutions

### 1. Database Connection Issues

**Symptoms:**
- 500 Internal Server Error
- FUNCTION_INVOCATION_FAILED
- Connection timeout errors

**Solutions:**

#### Check DATABASE_URL Format
Your DATABASE_URL should be:
```
postgresql://username:password@host:port/database?sslmode=require
```

**Common mistakes:**
- ❌ Includes `psql` command wrapper
- ❌ Missing `?sslmode=require`
- ❌ Has quotes around the string
- ❌ Wrong credentials

#### Verify in Vercel
1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Check `DATABASE_URL` value
3. Make sure it's exactly: `postgresql://user:pass@host/db?sslmode=require`
4. No extra characters, no quotes

### 2. Missing Dependencies

**Check requirements.txt includes:**
```
psycopg2-binary==2.9.9
```

If missing, add it and redeploy.

### 3. Check Vercel Function Logs

1. Go to Vercel Dashboard → Your Project
2. Click **Functions** tab
3. Click on a failed function
4. Check **Logs** for the actual error message

Common errors you might see:
- `ModuleNotFoundError` - Missing dependency
- `OperationalError` - Database connection failed
- `AttributeError` - Code issue
- `ImportError` - Import path issue

### 4. Database Not Initialized

**Solution:** The app will create tables automatically on first request. If you want to pre-create them:

1. Connect to your Neon database
2. Run the SQL to create tables (see below)

### 5. Connection Pool Exhausted

**For Neon:** Use the **pooler** endpoint (ends with `-pooler`)

Example:
```
postgresql://user:pass@ep-xxx-pooler.region.aws.neon.tech/db?sslmode=require
```

## Step-by-Step Debugging

### Step 1: Check Environment Variables
```bash
# In Vercel Dashboard, verify:
- SECRET_KEY is set
- DATABASE_URL is set and correct format
- All other env vars are set
```

### Step 2: Check Function Logs
1. Go to Vercel → Your Project → Functions
2. Find the failed function
3. Click to view logs
4. Look for the actual error message

### Step 3: Test Database Connection

You can test your DATABASE_URL locally:
```python
import psycopg2

DATABASE_URL = "your-connection-string-here"

try:
    conn = psycopg2.connect(DATABASE_URL)
    print("✅ Connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

### Step 4: Verify Tables Exist

Connect to Neon and check:
```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';
```

Should show: `user` and `post` tables

If tables don't exist, create them:
```sql
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL
);

CREATE TABLE post (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL
);
```

## Quick Fixes

### Fix 1: Update DATABASE_URL
1. Get correct connection string from Neon
2. Remove `psql` wrapper and quotes
3. Ensure `?sslmode=require` is at the end
4. Update in Vercel
5. Redeploy

### Fix 2: Add Missing Dependency
1. Check `requirements.txt` has `psycopg2-binary==2.9.9`
2. Commit and push
3. Vercel will redeploy automatically

### Fix 3: Check Logs for Specific Error
1. View function logs in Vercel
2. Find the actual error message
3. Search for that error in this guide

## Still Not Working?

1. **Check Vercel Logs** - Most important step!
2. **Verify DATABASE_URL** - Test it locally
3. **Check Neon Dashboard** - Ensure database is active
4. **Try Simple Test** - Create a minimal endpoint to test DB connection

## Test Endpoint

Add this to test database connection:

```python
@app.get("/test-db")
async def test_db():
    try:
        from app.core.database import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return {"status": "Database connected"}
    except Exception as e:
        return {"status": "Database error", "error": str(e)}
```

Then visit: `https://your-app.vercel.app/test-db`

