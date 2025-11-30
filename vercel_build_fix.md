# Fixing psycopg2-binary Build Error on Vercel

## The Problem
Vercel's build environment sometimes has issues building `psycopg2-binary` from source.

## Solutions

### Solution 1: Use psycopg2-binary without version pinning (Recommended)

I've updated `requirements.txt` to use:
```
psycopg2-binary
```

Instead of:
```
psycopg2-binary==2.9.9
```

This allows Vercel to install a compatible version.

### Solution 2: Use psycopg (Alternative driver)

If Solution 1 doesn't work, you can use `psycopg` (version 3) which is pure Python:

**Update requirements.txt:**
```
psycopg[binary]
```

**Update database.py connection string format:**
```python
# Change postgresql:// to postgresql+psycopg://
DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgresql+psycopg://')
```

### Solution 3: Add build configuration

Create or update `vercel.json` to specify Python version:

```json
{
  "buildCommand": "pip install -r requirements.txt",
  "functions": {
    "api/index.py": {
      "runtime": "python3.9"
    }
  }
}
```

## Current Fix Applied

I've updated `requirements.txt` to use `psycopg2-binary` without version pinning, which should work better with Vercel's build system.

## Next Steps

1. **Commit and push** the updated `requirements.txt`
2. **Redeploy** on Vercel
3. **Check build logs** - it should install successfully now

If it still fails, we can try Solution 2 (using psycopg instead).

