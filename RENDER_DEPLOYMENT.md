# Deployment Instructions for Render

## Prerequisites
- GitHub repository with your code pushed
- Render account (https://render.com)
- Google Gemini API key

## Step 1: Prepare Your Files
✅ Already done. The following files have been created:
- `render.yaml` - Render configuration
- `.streamlit/config.toml` - Streamlit production settings

## Step 2: Push to GitHub
```bash
git add render.yaml .streamlit/config.toml
git commit -m "Add Render deployment configuration"
git push origin main
```

## Step 3: Create a Web Service on Render

1. **Go to Render Dashboard:**
   - Visit https://dashboard.render.com
   - Click **New +** → **Web Service**

2. **Connect GitHub Repository:**
   - Select **Deploy an existing repository**
   - Click **Connect** next to your GitHub repo
   - If not listed, authorize Render to access GitHub

3. **Configure the Service:**
   - **Name:** `contract-risk-analyzer`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port 10000 --server.address 0.0.0.0`
   - **Plan:** Select "Free" or "Starter" (Free tier has limitations)

4. **Set Environment Variables:**
   - Click **Environment** or **Add Environment Variable**
   - Add:
     ```
     GEMINI_API_KEY=your_actual_api_key_here
     STREAMLIT_SERVER_HEADLESS=true
     ```

5. **Advanced Settings (Optional):**
   - Health Check Path: `/`
   - Keep default other settings

6. **Deploy:**
   - Click **Create Web Service**
   - Render will build and deploy your app
   - You'll get a URL like: `https://contract-risk-analyzer.onrender.com`

## Step 4: Verify Deployment

- Wait for build to complete (5-10 minutes)
- Check the **Logs** tab for any errors
- Your app should be live at the provided URL
- Test uploading a contract and running analysis

## Alternative: Using render.yaml

If you want Render to automatically detect settings from `render.yaml`:
1. Render will auto-detect `render.yaml` if it exists in the root
2. Just push the file and create a Web Service
3. Render will read the configuration automatically

## Notes

- **First deployment takes longer** due to dependencies
- **Free tier may have cold starts** (app sleeps after inactivity)
- **File uploads are temporary** - stored in `/tmp` directory
- **API calls count** toward your Gemini API quota
- **Storage is ephemeral** - files don't persist after restart

## Troubleshooting

**App won't start (Build fails):**
- Check Logs tab in Render dashboard
- Ensure all dependencies in `requirements.txt` are compatible
- Try running locally first: `streamlit run app.py`

**API key not working:**
- Verify `GEMINI_API_KEY` is set in Environment Variables
- Make sure it's set as a secret (not public)
- Test key locally with: `python check_models.py`

**Uploads not working:**
- Uploaded files stored in `./uploaded_files/` 
- Directory created automatically on startup
- Files deleted when app restarts (normal behavior)

**Slow performance:**
- Free tier has limited resources
- Consider upgrading to Starter or Pro
- Optimize contract file size (< 5MB recommended)

## Keeping Your Deployment Updated

After making changes locally:
```bash
git add .
git commit -m "Update: your changes"
git push origin main
```

Render will **auto-redeploy** on each push (if auto-deploy is enabled).

To disable auto-deploy or manage deployments:
- Go to your service on Render dashboard
- Settings → Auto-Deploy (toggle on/off)
- Manual Deploy: Click **Deploy** button in dashboard
