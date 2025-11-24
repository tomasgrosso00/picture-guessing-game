# Hosting Options for Picture Guessing Game

## Free Hosting Options (No Payment Required)

### 1. **Render** (Recommended - Easiest)
- **Free tier**: Yes, with limitations
- **Setup**: Very easy, connects to GitHub
- **Limitations**: Spins down after 15 min inactivity (takes ~30 sec to wake up)
- **Steps**:
  1. Push code to GitHub
  2. Go to https://render.com
  3. Create account (free)
  4. New → Web Service
  5. Connect GitHub repo
  6. Build command: `pip install -r requirements.txt`
  7. Start command: `python3 app.py`
  8. Environment: Python 3
  9. Deploy!

### 2. **Railway**
- **Free tier**: Yes, $5/month credit (usually enough for small apps)
- **Setup**: Easy, connects to GitHub
- **Steps**:
  1. Push code to GitHub
  2. Go to https://railway.app
  3. New Project → Deploy from GitHub
  4. Select repo
  5. Add Python service
  6. Deploy!

### 3. **Fly.io**
- **Free tier**: Yes, generous free tier
- **Setup**: Requires CLI but good docs
- **Steps**:
  1. Install Fly CLI
  2. `fly launch`
  3. Follow prompts

### 4. **PythonAnywhere**
- **Free tier**: Yes, but limited
- **Setup**: Web-based, beginner-friendly
- **Limitations**: Only accessible during free tier hours, limited resources

## Quick Fixes for Local Network Access

Before hosting, try these:

### 1. Check Firewall
```bash
# Check if firewall is blocking
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
```

### 2. Allow Python through Firewall
- System Settings → Network → Firewall → Options
- Add Python to allowed apps
- Or temporarily disable firewall to test

### 3. Verify Same Network
- Both devices must be on same Wi-Fi network
- Try: `ping 192.168.68.102` from other device

### 4. Test from Mac Terminal
```bash
# From your Mac, test if accessible
curl http://192.168.68.102:5001
```

## Recommended: Render (Free & Easy)

1. **Create GitHub repo** (if not already):
   ```bash
   cd team-photo-game
   git init
   git add .
   git commit -m "Initial commit"
   # Create repo on GitHub, then:
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Render**:
   - Sign up at https://render.com (free)
   - New → Web Service
   - Connect GitHub
   - Select your repo
   - Settings:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `python3 app.py`
     - Environment: Python 3
   - Deploy!

3. **Get your URL**: `https://your-app-name.onrender.com`

**Note**: Free tier spins down after inactivity, but first wake-up is usually quick.

## Cost Comparison

- **Render Free**: $0/month (with limitations)
- **Railway Free**: $0/month (with $5 credit)
- **Fly.io Free**: $0/month (generous free tier)
- **PythonAnywhere Free**: $0/month (limited hours)

All free tiers are sufficient for a small team game!

