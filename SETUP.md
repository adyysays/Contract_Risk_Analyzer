# AI Contract Risk Analyzer Pro - SETUP GUIDE

## 🚀 Complete Installation & Setup Instructions

This guide walks you through setting up the **AI Contract Risk Analyzer Pro** application on your system.

---

## ✅ Pre-Installation Checklist

- [ ] Python 3.9 or higher installed
- [ ] Internet connection available
- [ ] Google Gemini API key obtained
- [ ] Administrator access (if needed for installations)
- [ ] 4GB+ RAM available
- [ ] 500MB+ disk space available

---

## 📋 Step-by-Step Installation

### Step 1: Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key and save it somewhere safe
4. ⚠️ Keep this key private - never share it!

### Step 2: Set Up Project Directory

```bash
# Navigate to your projects folder
cd "D:\Users\ABCD\OneDrive\Projects\Contract Risk Analyzer"

# Verify you're in the right directory
dir
```

### Step 3: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (macOS/Linux)
source venv/bin/activate
```

**Note:** Your terminal should now show `(venv)` prefix

### Step 4: Create .env File

In the project root directory, create a new file named `.env`:

Windows (PowerShell):
```powershell
@"
GEMINI_API_KEY=your_gemini_api_key_here
APP_TITLE=AI Contract Risk Analyzer Pro
DEBUG=False
MAX_FILE_SIZE=50
"@ | Out-File -Encoding utf8 .env
```

Or manually create the file with this content:
```
GEMINI_API_KEY=your_gemini_api_key_here
APP_TITLE=AI Contract Risk Analyzer Pro
DEBUG=False
MAX_FILE_SIZE=50
```

Replace `your_gemini_api_key_here` with your actual API key.

### Step 5: Install Dependencies

```bash
# Ensure pip is up to date
python -m pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

### Step 6: Verify Installation

```bash
# Check if all packages are installed
pip check

# Test Streamlit installation
streamlit --version

# Test Python modules
python -c "from modules.file_handler import FileHandler; print('✓ Modules installed correctly')"
```

### Step 7: Run the Application

```bash
# Start the Streamlit app
streamlit run app.py
```

Your browser should automatically open to `http://localhost:8501`

---

## 🔧 Troubleshooting Installation

### Problem: "Python not found"
**Solution:** Ensure Python is installed and added to PATH
```bash
python --version
```

### Problem: Virtual environment not activating
**Windows:**
```powershell
# If getting permission error, try:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
then venv\Scripts\activate
```

### Problem: "pip install" fails
**Solution:** Try upgrading pip and using specific Python version
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Problem: "ModuleNotFoundError" when running app
**Solution:** Ensure virtual environment is activated
```bash
# Check if activated (should show (venv) prefix)
which python  # or: where python (on Windows)

# Should point to venv folder
```

### Problem: Gemini API Key Error
**Solution:** Verify .env file is in project root
```bash
# Check .env exists and is readable
cat .env  # or: type .env (on Windows)
```

### Problem: Port 8501 already in use
**Solution:** Run Streamlit on different port
```bash
streamlit run app.py --server.port 8502
```

---

## 📦 Dependency Management

### If you need to add a new package:

```bash
# Add package
pip install package_name

# Update requirements.txt
pip freeze > requirements.txt
```

### To clean up old packages:

```bash
# See installed packages
pip list

# Uninstall unused package
pip uninstall package_name
```

---

## 🧪 Testing the Setup

Once the app is running:

1. **Test File Upload**
   - Create a sample text file with contract content
   - Upload via the "Upload Contract" page
   - Verify text extraction works

2. **Test API Connection**
   - Go to "Summary" page
   - Click "Generate Summary"
   - Should see AI-generated summary

3. **Test Risk Analysis**
   - Go to "Risk Analysis"
   - Click "Analyze Risks"
   - Should see risk metrics and charts

4. **Test Chatbot**
   - Go to "Chatbot" page
   - Ask a sample question
   - Should get AI-generated response

---

## 🛢️ Environment Variables Reference

### Required
- `GEMINI_API_KEY` - Your Google Gemini API key

### Optional
- `APP_TITLE` - Application title (default: "AI Contract Risk Analyzer Pro")
- `DEBUG` - Debug mode (default: False)
- `MAX_FILE_SIZE` - Maximum file size in MB (default: 50)
- `GA_POPULATION_SIZE` - GA population (default: 50)
- `GA_GENERATIONS` - GA generations (default: 20)

---

## 📂 Project Structure After Setup

```
Contract Risk Analyzer/
├── venv/                           # Virtual environment (created)
├── uploaded_files/                 # Uploaded contracts (auto-created)
├── app.py                          # ✓ Main Streamlit app
├── config.py                       # ✓ Configuration
├── requirements.txt                # ✓ Dependencies
├── .env                            # ✓ (Create with API key)
├── .env.example                    # ✓ Example .env
├── README.md                       # ✓ Full documentation
├── SETUP.md                        # ✓ This file
│
├── modules/                        # ✓ Core modules
│   ├── __init__.py
│   ├── file_handler.py
│   ├── gemini_client.py
│   ├── risk_analyzer.py
│   ├── rag_chatbot.py
│   ├── genetic_optimizer.py
│   └── visualizations.py
│
└── utils/                          # ✓ Utilities
    ├── __init__.py
    └── report_utils.py
```

---

## 🚀 Running the App in Different Ways

### Standard (with auto-reload):
```bash
streamlit run app.py
```

### For production/server:
```bash
streamlit run app.py --client.showErrorDetails=false --logger.level=error
```

### With specific port:
```bash
streamlit run app.py --server.port 8080
```

### Headless (for CI/CD):
```bash
streamlit run app.py --logger.level=debug --client.showErrorDetails=true
```

---

## 🔐 Security Notes

1. **API Key Security**
   - Never commit `.env` to git
   - Add `.env` to `.gitignore`
   - Use environment variables in production

2. **File Uploads**
   - Files stored temporarily in `uploaded_files/`
   - Clean up old files regularly
   - Production: implement file retention policy

3. **API Limits**
   - Monitor Gemini API usage
   - Set rate limits if needed
   - Consider implementing caching

---

## 📊 Performance Optimization

### For better performance:

1. **Reduce document size:** Limits < 100KB work fastest
2. **Use SSD:** Faster file I/O
3. **Increase RAM:** 8GB+ recommended
4. **Cache results:** App uses session state caching
5. **Batch processing:** Process multiple contracts sequentially

---

## 🆘 Getting Help

### If installation fails:

1. **Check Python version:**
   ```bash
   python --version  # Should be 3.9+
   ```

2. **Verify requirements installed:**
   ```bash
   pip check
   ```

3. **Check error logs:**
   - Look in terminal output
   - Check Streamlit logs in browser console

4. **Test individual modules:**
   ```bash
   python -c "from modules.file_handler import FileHandler; print('OK')"
   ```

---

## ✅ Successful Installation Checklist

After setup, verify everything works:

- [ ] Virtual environment created and activated
- [ ] All packages installed (`pip check` passes)
- [ ] `.env` file created with Gemini API key
- [ ] `app.py` runs without errors
- [ ] Browser opens to Streamlit UI
- [ ] File upload works
- [ ] Summary generation works
- [ ] Risk analysis works
- [ ] Chatbot initializes correctly

---

## 🔄 Updating the Application

To update the dependencies:

```bash
pip install --upgrade -r requirements.txt
```

To reset everything and reinstall:

```bash
# Deactivate and delete venv
deactivate
rm -r venv

# Create fresh environment
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📞 Support & Troubleshooting

For detailed troubleshooting, refer to:
- `README.md` - Full documentation
- Terminal output - Error messages and logs
- Streamlit docs - https://docs.streamlit.io/

---

**Version:** 1.0
**Last Updated:** March 2026
**Status:** Ready for Production ✅
