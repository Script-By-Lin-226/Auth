# How to Update Existing Environment Variable in Vercel

## The Error
"A variable with the name `DATABASE_URL` already exists"

This means you've already added `DATABASE_URL` to Vercel, but you need to **update** it with the correct format.

## Solution: Update the Existing Variable

### Step 1: Go to Environment Variables

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click on your project
3. Go to **Settings** → **Environment Variables**
4. Find `DATABASE_URL` in the list

### Step 2: Update the Value

1. Click on the **DATABASE_URL** row
2. Click **Edit** or the **pencil icon**
3. Update the **Value** field with the correct format:

**Correct Format (remove psql wrapper):**
```
postgresql://neondb_owner:npg_0EYOQjR9HATq@ep-morning-rice-a4xrs2n6-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require
```

**What to remove:**
- ❌ Remove `psql` command
- ❌ Remove single quotes `'`
- ❌ Remove `channel_binding=require` (optional, but keep `sslmode=require`)

**What to keep:**
- ✅ The full connection string starting with `postgresql://`
- ✅ `?sslmode=require` at the end

### Step 3: Save and Redeploy

1. Click **Save**
2. Go to **Deployments** tab
3. Click **⋯** on the latest deployment
4. Click **Redeploy**

## Quick Format Check

### ❌ Wrong (what you might have now):
```
psql 'postgresql://neondb_owner:npg_0EYOQjR9HATq@ep-morning-rice-a4xrs2n6-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
```

### ✅ Correct (what it should be):
```
postgresql://neondb_owner:npg_0EYOQjR9HATq@ep-morning-rice-a4xrs2n6-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require
```

## Alternative: Delete and Re-add

If you can't edit it:

1. Click on `DATABASE_URL` row
2. Click **Delete** or **Remove**
3. Click **Add New**
4. Enter:
   - **Key:** `DATABASE_URL`
   - **Value:** Your corrected connection string
   - **Environment:** Select all (Production, Preview, Development)
5. Click **Save**
6. **Redeploy**

## Verify It's Correct

After updating, your DATABASE_URL should:
- ✅ Start with `postgresql://` or `postgres://`
- ✅ Include username and password
- ✅ Include host (ep-xxxxx-pooler...)
- ✅ Include database name (neondb)
- ✅ End with `?sslmode=require`
- ✅ No `psql` command
- ✅ No quotes
- ✅ No spaces

## Test After Update

1. Redeploy your app
2. Visit your Vercel URL
3. Try to register a new user
4. Check Vercel function logs if there are errors

The connection should work now!

