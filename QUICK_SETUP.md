# Quick Setup Guide - Where to Set DATABASE_URL

## ❌ DON'T Put DATABASE_URL in Code

**Never hardcode your DATABASE_URL in `config.py` or any code file!**

## ✅ DO Set DATABASE_URL in Vercel Environment Variables

### Step 1: Get Your Neon Connection String

1. Go to [Neon Console](https://console.neon.tech)
2. Select your project
3. Click "Connection Details" or "Connection String"
4. Copy the connection string

It should look like:
```
postgresql://username:password@ep-xxxxx-pooler.region.aws.neon.tech/neondb?sslmode=require
```

**Important:** 
- Remove any `psql` command wrapper
- Use the **pooler** endpoint (ends with `-pooler`) for serverless
- Make sure it includes `?sslmode=require`

### Step 2: Set in Vercel Dashboard

**If DATABASE_URL doesn't exist:**
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click on your project
3. Go to **Settings** → **Environment Variables**
4. Click **Add New**
5. Enter:
   - **Key:** `DATABASE_URL`
   - **Value:** Your Neon connection string (without `psql` wrapper)
   - **Environment:** Select all (Production, Preview, Development)
6. Click **Save**

**If DATABASE_URL already exists (you'll see an error):**
1. Go to **Settings** → **Environment Variables**
2. Find `DATABASE_URL` in the list
3. Click on it to **Edit**
4. Update the **Value** with the correct format (remove `psql` wrapper)
5. Click **Save**
6. See [UPDATE_ENV_VAR.md](./UPDATE_ENV_VAR.md) for detailed steps

### Step 3: Redeploy

After adding environment variables:
1. Go to **Deployments** tab
2. Click the **⋯** menu on latest deployment
3. Click **Redeploy**

Or push a new commit to trigger redeploy.

## Correct Format Examples

### ✅ Correct (for Vercel Environment Variable):
```
postgresql://neondb_owner:password@ep-morning-rice-a4xrs2n6-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require
```

### ❌ Wrong (don't use):
```
psql 'postgresql://...'  ← Remove psql wrapper
postgresql://...'        ← Remove quotes
```

## How It Works

1. **Config file** (`app/core/config.py`) reads from environment:
   ```python
   DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
   ```

2. **Vercel** provides the environment variable when your app runs

3. **Your app** uses the value from Vercel, not from code

## Security Note

- ✅ Environment variables are secure (not in code)
- ✅ Different values for different environments
- ✅ Can be updated without code changes
- ❌ Never commit secrets to Git

## Checklist

- [ ] Removed DATABASE_URL from config.py (if you added it)
- [ ] Got connection string from Neon (pooler endpoint)
- [ ] Removed `psql` wrapper and quotes
- [ ] Added to Vercel Environment Variables
- [ ] Selected all environments (Production, Preview, Development)
- [ ] Redeployed the application
- [ ] Tested the connection

## Troubleshooting

### Still getting 500 error?
1. Check Vercel logs: Dashboard → Your Project → Functions → View Logs
2. Verify DATABASE_URL format is correct
3. Make sure you redeployed after adding the variable
4. Check that `psycopg2-binary` is in requirements.txt (already added)

### Connection string format issues?
- Must start with `postgresql://` or `postgres://`
- Must include `?sslmode=require`
- No spaces, no quotes, no `psql` command
- Use pooler endpoint for serverless

