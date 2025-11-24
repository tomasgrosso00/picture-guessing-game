# Setting Environment Variables in Render

## How to Set the Admin Password

1. **Go to your Render Dashboard**
   - Visit https://dashboard.render.com
   - Click on your `picture-guessing-game` service

2. **Navigate to Environment**
   - Click on "Environment" in the left sidebar
   - Or go to the "Settings" tab → "Environment Variables"

3. **Add Environment Variable**
   - Click "Add Environment Variable"
   - Add this variable:

   **Admin Password:**
   - Key: `ADMIN_PASSWORD`
   - Value: `your-secure-password-here` (choose a strong password!)

   **Optional - Secret Key (recommended):**
   - Key: `SECRET_KEY`
   - Value: `generate-a-random-string-here` (for session security)

4. **Save and Redeploy**
   - Click "Save Changes"
   - Render will automatically redeploy your service
   - Wait 1-2 minutes for redeployment

5. **Test It**
   - Visit your app URL
   - Go to `/admin` (or click admin link)
   - Login with the password you just set

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

