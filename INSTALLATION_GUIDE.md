# 🛠️ AI Lead Enrichment - Complete Installation Guide

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows 10/11
- **Python**: 3.11 or higher
- **Shell**: PowerShell (recommended)
- **Internet**: Stable connection required
- **Disk Space**: ~100MB for dependencies

### Required Accounts
You'll need free accounts from these services:
- [PeopleDataLabs](https://www.peopledatalabs.com/)
- [Apollo.io](https://www.apollo.io/)
- [Hunter.io](https://hunter.io/)
- [SERP API](https://serpapi.com/)
- [OpenAI](https://platform.openai.com/)
- Gmail (with app-specific password)

## 🚀 Step-by-Step Installation

### Step 1: Python Installation

#### Check Current Python Version
```powershell
python --version
```

#### Install Python 3.11+ (if needed)
1. Download from [python.org](https://www.python.org/downloads/)
2. Run installer with "Add to PATH" checked
3. Verify installation:
```powershell
python --version
pip --version
```

### Step 2: Create Project Directory

```powershell
# Navigate to your desired location
cd C:\Users\%USERNAME%\Desktop

# Create project folder
mkdir "AI Lead Enrichment"
cd "AI Lead Enrichment"

# Create subfolder
mkdir lead_enrichment
cd lead_enrichment
```

### Step 3: Install Dependencies

```powershell
# Install required packages
pip install streamlit==1.28.0
pip install openai==1.3.0
pip install requests==2.31.0
pip install python-dotenv==1.0.0

# Verify installations
pip list | findstr "streamlit openai requests python-dotenv"
```

### Step 4: Download Project Files

Create these files in your `lead_enrichment` folder:

#### 4.1 Create `requirements.txt`
```txt
streamlit==1.28.0
openai==1.3.0
requests==2.31.0
python-dotenv==1.0.0
```

#### 4.2 Download Core Files
You need these files in your `lead_enrichment` directory:
- `enrichment_engine.py`
- `utils.py`
- `ui_app.py`

### Step 5: Get API Keys

#### 5.1 PeopleDataLabs API Key
1. Visit [PeopleDataLabs](https://www.peopledatalabs.com/)
2. Sign up for free account
3. Navigate to Dashboard → API Keys
4. Copy your API key
5. **Free Tier**: 1000 requests/month

#### 5.2 Apollo.io API Key
1. Visit [Apollo.io](https://www.apollo.io/)
2. Create free account
3. Go to Settings → API Keys
4. Generate new API key
5. **Free Tier**: 200 requests/month

#### 5.3 Hunter.io API Key
1. Visit [Hunter.io](https://hunter.io/)
2. Sign up for free account
3. Go to API section
4. Copy your API key
5. **Free Tier**: 25 requests/month

#### 5.4 SERP API Key
1. Visit [SERP API](https://serpapi.com/)
2. Create free account
3. Dashboard → API Key
4. Copy your key
5. **Free Tier**: 100 searches/month

#### 5.5 OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create account
3. Add payment method (required)
4. Go to API Keys section
5. Create new secret key
6. **Pricing**: Pay-per-use (~$0.01/request)

#### 5.6 Gmail App Password
1. Enable 2-Factor Authentication on Gmail
2. Go to Google Account Settings
3. Security → 2-Step Verification
4. App passwords → Generate
5. Select "Mail" and your device
6. Copy the 16-character password

### Step 6: Configure API Keys

#### 6.1 Edit `enrichment_engine.py`
Open the file and replace these lines:
```python
# API Keys (Replace with your actual keys)
PEOPLEDATALABS_API_KEY = "your_actual_pdl_key_here"
APOLLO_API_KEY = "your_actual_apollo_key_here"
HUNTER_API_KEY = "your_actual_hunter_key_here"
SERP_API_KEY = "your_actual_serp_key_here"
```

#### 6.2 Edit `utils.py`
Replace these lines:
```python
# API Keys
OPENAI_API_KEY = "your_actual_openai_key_here"
SENDER_EMAIL_ID = "your_email@gmail.com"
APP_PASSWORD = "your_16_char_app_password"
```

### Step 7: Test Installation

#### 7.1 Test Python Dependencies
```powershell
python -c "import streamlit, openai, requests; print('All packages installed successfully!')"
```

#### 7.2 Test API Keys
```powershell
# Navigate to your project directory
cd "C:\Users\%USERNAME%\Desktop\AI Lead Enrichment\lead_enrichment"

# Run the application
streamlit run ui_app.py
```

#### 7.3 Verify Application Launch
- Browser should open automatically
- URL: `http://localhost:8501`
- You should see the AI Lead Enrichment interface

### Step 8: First Test Run

#### 8.1 Test with Sample Data
1. **Name**: "Elon Musk"
2. **Company**: "Tesla"
3. Click "🔍 Enrich Lead"

#### 8.2 Expected Results
- ✅ Debug messages showing API keys loaded
- ✅ Progress indicators for each API
- ✅ Results displayed in sections
- ✅ No error messages

## 🔧 Configuration Options

### Environment Variables (Alternative)

If you prefer using `.env` file:

#### Create `.env` file
```env
PEOPLEDATALABS_API_KEY=your_pdl_key
APOLLO_API_KEY=your_apollo_key
HUNTER_API_KEY=your_hunter_key
SERP_API_KEY=your_serp_key
OPENAI_API_KEY=your_openai_key
SENDER_EMAIL_ID=your_email@gmail.com
APP_PASSWORD=your_app_password
```

#### Modify code to use .env
Uncomment the environment variable loading sections in both files.

### Port Configuration

Change Streamlit port if needed:
```powershell
streamlit run ui_app.py --server.port 8502
```

## 🐛 Troubleshooting Installation

### Common Issues

#### 1. Python Not Found
**Error**: `'python' is not recognized`
**Solution**:
```powershell
# Try python3 instead
python3 --version

# Or add Python to PATH manually
```

#### 2. Permission Errors
**Error**: `Permission denied installing packages`
**Solution**:
```powershell
# Install with user flag
pip install --user streamlit openai requests python-dotenv
```

#### 3. Package Installation Fails
**Error**: Various pip errors
**Solution**:
```powershell
# Update pip first
python -m pip install --upgrade pip

# Then install packages
pip install -r requirements.txt
```

#### 4. Streamlit Won't Start
**Error**: `ModuleNotFoundError: No module named 'streamlit'`
**Solution**:
```powershell
# Verify installation
pip show streamlit

# Reinstall if needed
pip uninstall streamlit
pip install streamlit
```

#### 5. Browser Doesn't Open
**Error**: Streamlit runs but no browser
**Solution**:
- Manually open: `http://localhost:8501`
- Or use: `streamlit run ui_app.py --server.headless false`

#### 6. API Key Errors
**Error**: `ValueError: API_KEY is not set`
**Solution**:
- Double-check API key configuration
- Ensure no extra spaces or quotes
- Verify keys are active in respective dashboards

### Verification Commands

#### Check File Structure
```powershell
dir
# Should show: enrichment_engine.py, utils.py, ui_app.py, requirements.txt
```

#### Test Individual Components
```powershell
# Test Python imports
python -c "import streamlit; print('Streamlit OK')"
python -c "import openai; print('OpenAI OK')"
python -c "import requests; print('Requests OK')"
```

#### Check API Connectivity
```powershell
# Test internet connection
ping google.com

# Test specific API endpoints (optional)
curl -I https://api.peopledatalabs.com
```

## 📊 Resource Usage

### Disk Space
- Python packages: ~80MB
- Project files: ~50KB
- Total: ~80MB

### Memory Usage
- Streamlit app: ~100MB
- API responses: ~10MB
- Total: ~110MB RAM

### Network Usage
- Initial setup: ~80MB download
- Per enrichment: ~1MB data transfer

## 🔄 Updates and Maintenance

### Updating Dependencies
```powershell
# Update all packages
pip install --upgrade streamlit openai requests python-dotenv

# Or update individually
pip install --upgrade streamlit
```

### Backup Configuration
```powershell
# Copy your configured files to backup location
copy enrichment_engine.py enrichment_engine_backup.py
copy utils.py utils_backup.py
```

### Monitoring API Usage
- Check your API dashboards regularly
- Monitor monthly limits
- Set up usage alerts if available

## ✅ Installation Checklist

- [ ] Python 3.11+ installed
- [ ] Project directory created
- [ ] Dependencies installed
- [ ] All project files downloaded
- [ ] API keys obtained from all 6 services
- [ ] API keys configured in code files
- [ ] Gmail app password set up
- [ ] Application launches successfully
- [ ] Test enrichment completed
- [ ] No error messages
- [ ] Results display properly

## 🚀 Next Steps

Once installation is complete:

1. **Read the [Documentation](DOCUMENTATION.md)** for detailed usage
2. **Test with known contacts** to verify accuracy
3. **Monitor API usage** to stay within limits
4. **Explore all features** including email reports
5. **Set up regular backups** of your configuration

## 📞 Support

### Getting Help

If you encounter issues:

1. **Check this troubleshooting section**
2. **Verify all prerequisites are met**
3. **Test each component individually**
4. **Check API service status pages**
5. **Review error messages carefully**

### Reporting Problems

When reporting issues, include:
- Operating system version
- Python version
- Error messages (full text)
- Steps to reproduce
- API service status

---

**Installation Time**: ~30 minutes
**Difficulty**: Beginner-friendly
**Support**: Community-driven

*Happy lead enriching! 🎯* 