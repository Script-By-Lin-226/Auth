# Debugging Steps for 500 Error

Since your DATABASE_URL is already set up in Vercel, let's debug step by step:

## Step 1: Check the Health Endpoint

After redeploying, visit:
```
https://your-app.vercel.app/health
```

This will show you:
- ✅ If the app is running
- ✅ If DATABASE_URL is being read
- ✅ Database connection status
- ✅ Any error messages

## Step 2: Check Vercel Function Logs

1. Go to **Vercel Dashboard** → Your Project
2. Click **Functions** tab
3. Click on any function (or the failed one)
4. Click **View Logs** or check the **Logs** section
5. Look for error messages

**Common errors you might see:**

### Error: "ModuleNotFoundError: No module named 'psycopg2'"
**Fix:** Make sure `psycopg2-binary==2.9.9` is in `requirements.txt`

### Error: "could not connect to server"
**Fix:** Check DATABASE_URL format and ensure Neon database is active

### Error: "relation does not exist"
**Fix:** Tables need to be created - the app will create them automatically

### Error: "SSL connection required"
**Fix:** Make sure DATABASE_URL includes `?sslmode=require`

## Step 3: Verify DATABASE_URL Format

In Vercel Environment Variables, your DATABASE_URL should be:

**✅ Correct Format:**
```
postgresql://username:password@ep-xxxxx-pooler.region.aws.neon.tech/neondb?sslmode=require
```

**❌ Wrong Formats:**
```
psql 'postgresql://...'           ← Remove psql wrapper
'postgresql://...'                ← Remove quotes
postgresql://...                  ← Missing ?sslmode=require
postgresql://...?sslmode=require' ← Quote at the end
```

## Step 4: Test Database Connection

You can test your connection string format:

1. Copy your DATABASE_URL from Vercel
2. Test it locally:
```python
import psycopg2
conn = psycopg2.connect("your-database-url-here")
print("✅ Connection successful!")
conn.close()
```

## Step 5: Check What the Health Endpoint Shows

Visit `/health` and check the response:

**If database status is "connected":**
- ✅ Database is working
- The error might be elsewhere

**If database status is "error":**
- Check the error message
- Verify DATABASE_URL format
- Check Neon dashboard

**If database status is "engine_not_created":**
- DATABASE_URL format is wrong
- Check for `psql` wrapper or quotes

## Step 6: Common Issues and Fixes

### Issue: DATABASE_URL has wrong format
**Solution:** 
1. Go to Neon Console
2. Get connection string
3. Remove `psql` and quotes
4. Ensure `?sslmode=require` at end
5. Update in Vercel
6. Redeploy

### Issue: Missing psycopg2
**Solution:**
1. Check `requirements.txt` has `psycopg2-binary==2.9.9`
2. Commit and push
3. Vercel will redeploy

### Issue: Database not accessible
**Solution:**
1. Check Neon dashboard - is database active?
2. Check if you're using pooler endpoint (ends with `-pooler`)
3. Verify credentials are correct

## What to Share

If you're still getting errors, share:
1. The response from `/health` endpoint
2. The error message from Vercel function logs
3. First 50 characters of your DATABASE_URL (without password)

This will help identify the exact issue!

