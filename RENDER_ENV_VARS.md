# Setting Environment Variables in Render

## Password System

There are **two passwords**:
1. **Master Password** - Always works, for you (the admin)
   - Set via `MASTER_PASSWORD` environment variable
   - Default: `master-admin-2024` (change this!)
   - Use this password yourself

2. **Host Password** - Weekly password for game hosts
   - Set via `ADMIN_PASSWORD` environment variable  
   - Default: `admin123` (for local dev)
   - Give this to the weekly host, change it each week

## How to Set Secrets/Environment Variables

1. **Go to your Render Dashboard**
   - Visit https://dashboard.render.com
   - Click on your `picture-guessing-game` service

2. **Navigate to Environment**
   - Click on "Environment" in the left sidebar
   - Or go to the "Settings" tab → "Environment Variables"

3. **Add Variables**
   - Click "Add Environment Variable"
   - Add these variables:

   **Variable 1 - Master Password (for you):**
   - Key: `MASTER_PASSWORD`
   - Value: `your-secure-master-password` (choose a strong password!)

   **Variable 2 - Weekly Host Password:**
   - Key: `ADMIN_PASSWORD`
   - Value: `weekly-host-password-here` (change this each week!)

   **Variable 3 (Optional but recommended):**
   - Key: `SECRET_KEY`
   - Value: `generate-a-random-string-here` (for session security)

4. **Save and Redeploy**
   - Click "Save Changes"
   - Render will automatically redeploy your service
   - Wait 1-2 minutes for redeployment

## Generating a Secure SECRET_KEY

You can generate a random secret key using Python:

```python
import secrets
print(secrets.token_hex(32))
```

Or use an online generator: https://randomkeygen.com/

## Security Notes

- ✅ Never commit passwords to git
- ✅ Use strong, unique passwords
- ✅ The `.gitignore` already excludes `.env` files
- ✅ Environment variables are encrypted in Render

## Local Development

For local development, the app will use `admin123` as default if no environment variable is set. You can also create a `.env` file (it's already in `.gitignore`):

```bash
# .env file (don't commit this!)
ADMIN_PASSWORD=your-local-password
SECRET_KEY=your-local-secret-key
```

But you'd need to install `python-dotenv` and load it. For now, the default works fine for local testing.

