# Railway Deployment Guide

## Prerequisites
1. Railway account (https://railway.app)
2. GitHub repository with your code
3. Cloudinary account for storage

## Deployment Steps

### 1. Prepare Repository
```bash
git add .
git commit -m "Add Railway deployment configuration"
git push origin main
```

### 2. Deploy to Railway

#### Option A: Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

#### Option B: Railway Dashboard
1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will auto-detect and deploy

### 3. Environment Variables
Set these in Railway dashboard:
```
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
PORT=8000
```

### 4. Custom Domain (Optional)
1. Go to your Railway project
2. Click "Settings" → "Domains"
3. Add your custom domain

## Files Added for Deployment
- `railway.json` - Railway configuration
- `Procfile` - Process definition
- `nixpacks.toml` - Build configuration
- `runtime.txt` - Python version
- `.railwayignore` - Files to exclude

## Monitoring
- Health check: `https://your-app.railway.app/health`
- API docs: `https://your-app.railway.app/docs`
- Logs available in Railway dashboard

## Troubleshooting
- Check Railway logs for deployment issues
- Ensure all environment variables are set
- Verify Cloudinary credentials