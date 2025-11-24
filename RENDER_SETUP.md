# Step-by-Step Render Deployment Guide

## Step 1: Prepare Your Code ✅ (Already Done!)

I've prepared your code for deployment:
- ✅ Created `.gitignore` to exclude unnecessary files
- ✅ Updated `app.py` to use Render's PORT environment variable
- ✅ Created `runtime.txt` for Python version

## Step 2: Initialize Git Repository

Run these commands in your terminal:

```bash
cd /Users/tomas.grosso/Documents/GitHub/tgrosso/team-photo-game

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Picture Guessing Game"
```

## Step 3: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `picture-guessing-game` (or any name you like)
3. Description: "Team picture guessing game"
4. Choose: **Public** (free) or **Private** (your choice)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **"Create repository"**

## Step 4: Push to GitHub

After creating the repo, GitHub will show you commands. Use these:

```bash
# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/picture-guessing-game.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 5: Deploy on Render

1. **Go to Render**: https://render.com
2. **Sign up** (free) - You can use GitHub to sign up (easiest!)
3. **Click "New +"** → **"Web Service"**
4. **Connect GitHub** (if not already connected):
   - Click "Connect GitHub"
   - Authorize Render
   - Select your GitHub account
5. **Select Repository**:
   - Find `picture-guessing-game` in the list
   - Click "Connect"
6. **Configure Service**:
   - **Name**: `picture-guessing-game` (or any name)
   - **Region**: Choose closest to you (e.g., `Oregon (US West)`)
   - **Branch**: `main`
   - **Root Directory**: (leave empty)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python3 app.py`
7. **Click "Create Web Service"**
8. **Wait for deployment** (takes 2-3 minutes)
9. **Get your URL**: You'll see something like `https://picture-guessing-game.onrender.com`

## Step 6: Test Your App

1. Visit your Render URL
2. Upload a test picture
3. Share the URL with your team!

## Important Notes

- **Free tier limitation**: App spins down after 15 min of inactivity
- **First wake-up**: Takes ~30 seconds when someone visits after inactivity
- **Data persistence**: Game data is stored in `data/game_data.json` (persists between deployments)
- **Uploads**: Pictures are stored in `static/uploads/` (persists between deployments)

## Troubleshooting

If deployment fails:
1. Check the **Logs** tab in Render dashboard
2. Common issues:
   - Missing dependencies → Check `requirements.txt`
   - Port issues → Already fixed in `app.py`
   - File permissions → Render handles this automatically

## Updating Your App

After making changes:
```bash
git add .
git commit -m "Your update message"
git push
```
Render will automatically redeploy!

