# Deploy Self-Healing Selenium Framework to Render

## Prerequisites
- GitHub account with this repository pushed
- Render account (https://render.com)

## Deployment Steps

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. Connect to Render
1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Select **"Connect a repository"**
4. Authorize GitHub and select this repository
5. Fill in the deployment settings:

### 3. Configuration in Render Dashboard

| Setting | Value |
|---------|-------|
| **Name** | `self-healing-selenium` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0` |
| **Instance Type** | Standard (or higher for better performance) |

### 4. Environment Variables (if needed)
Add any required environment variables in Render Dashboard:
- `PYTHONUNBUFFERED=true` (usually set automatically)

### 5. Deploy
- Click **"Create Web Service"**
- Render will automatically build and deploy

## Notes
- ✅ **Headless Chrome**: Already configured in `driver_factory.py`
- ✅ **Streamlit Server**: Configured to bind to `0.0.0.0` on Render's assigned port
- ✅ **Dependencies**: All required packages in `requirements.txt`

## Troubleshooting

### Chrome/Chromium issues
If you get "Chrome not found" errors:
1. Add a `build.sh` with system dependencies, or
2. Use the `render.yaml` alternative (see below)

### Alternative: Using render.yaml
Instead of manual configuration, Render can read from `render.yaml`:
1. Commit the `render.yaml` file
2. In Render, select "Use existing render.yaml"
3. Deploy will use the configuration from `render.yaml`

## Access Your App
Once deployed, your app will be available at:
```
https://{your-service-name}.onrender.com
```

Example: `https://self-healing-selenium.onrender.com`

## Limitations on Render
- Render has no display (X11) - that's why we use `--headless`
- Free tier has 15-minute request timeout
- Browser sessions may be limited - adjust timeouts in tests if needed
