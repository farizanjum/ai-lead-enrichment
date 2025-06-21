# 📧 Email Troubleshooting Guide - AI Lead Enrichment Stack

## 🚨 Common Email Issues & Solutions

### Issue 1: "Gmail authentication failed"

**Symptoms:**
- Error: `Gmail authentication failed. Check your email and app password`
- Emails not being sent
- SMTP authentication errors

**Solutions:**

#### ✅ Fix 1: Check App Password Format
Your Gmail app password should be **16 characters without spaces**.

**Current Configuration:**
```python
APP_PASSWORD = "shffrnhaustw qxvu"  # ❌ WRONG - has spaces
```

**Correct Configuration:**
```python
APP_PASSWORD = "shffrnhaustw qxvu"  # ✅ CORRECT - no spaces
```

#### ✅ Fix 2: Generate New App Password
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Security → 2-Step Verification
3. App passwords → Generate new password
4. Select "Mail" and your device
5. Copy the 16-character password (no spaces)
6. Update `APP_PASSWORD` in `utils.py`

#### ✅ Fix 3: Enable 2-Factor Authentication
Gmail App Passwords require 2FA to be enabled:
1. Go to Google Account → Security
2. Enable 2-Step Verification
3. Then generate App Password

### Issue 2: "Recipient email refused"

**Symptoms:**
- Error: `Recipient email refused`
- Specific email addresses rejected

**Solutions:**

#### ✅ Fix 1: Check Email Format
```python
# ❌ Invalid formats
"test@"
"@gmail.com"
"test.gmail.com"

# ✅ Valid formats
"test@gmail.com"
"user@company.com"
```

#### ✅ Fix 2: Verify Recipient Exists
- Test with a known working email first
- Try sending to your own email address

### Issue 3: "SMTP server disconnected"

**Symptoms:**
- Connection drops during sending
- Intermittent failures

**Solutions:**

#### ✅ Fix 1: Check Internet Connection
```powershell
ping smtp.gmail.com
```

#### ✅ Fix 2: Firewall/Antivirus
- Check if firewall is blocking SMTP (port 587)
- Temporarily disable antivirus to test

### Issue 4: Emails Not Appearing in Inbox

**Symptoms:**
- No error messages
- "Email sent successfully" but no email received

**Solutions:**

#### ✅ Fix 1: Check Spam/Junk Folder
- Gmail might filter automated emails
- Check recipient's spam folder

#### ✅ Fix 2: Check Email Formatting
- HTML emails might be filtered
- Try plain text format

## 🧪 Testing Email Functionality

### Method 1: Use Test Script
```powershell
cd "C:\Users\ayana\Desktop\AI Lead Enrichment\lead_enrichment"
python test_email.py
```

### Method 2: Manual Testing
```python
from utils import send_email_with_gmail

# Test with your own email
result = send_email_with_gmail(
    "your_email@gmail.com", 
    "Test Subject", 
    "<h1>Test Email</h1><p>This is a test.</p>"
)
print(result)
```

## 🔧 Step-by-Step Email Setup

### Step 1: Verify Gmail Account
- ✅ Gmail account active
- ✅ 2-Factor Authentication enabled
- ✅ App Password generated

### Step 2: Update Configuration
```python
# In utils.py
SENDER_EMAIL_ID = "your_actual_email@gmail.com"
APP_PASSWORD = "your16charapppassword"  # No spaces!
```

### Step 3: Test Connection
```powershell
python test_email.py
```

### Step 4: Verify in Streamlit
1. Run `streamlit run ui_app.py`
2. Enrich a lead
3. Check "Send email report"
4. Enter recipient email
5. Click "📧 Send Email Report"

## 📋 Email Configuration Checklist

- [ ] Gmail 2FA enabled
- [ ] App password generated (16 chars, no spaces)
- [ ] `SENDER_EMAIL_ID` updated in `utils.py`
- [ ] `APP_PASSWORD` updated in `utils.py`
- [ ] Test script runs successfully
- [ ] Recipient email format is valid
- [ ] Internet connection working
- [ ] Firewall allows SMTP traffic

## 🔍 Debugging Steps

### 1. Check Current Configuration
```python
from utils import SENDER_EMAIL_ID, APP_PASSWORD
print(f"Email: {SENDER_EMAIL_ID}")
print(f"Password length: {len(APP_PASSWORD)}")
print(f"Password has spaces: {' ' in APP_PASSWORD}")
```

### 2. Test SMTP Connection
```python
import smtplib
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    print("✅ SMTP connection successful")
    server.quit()
except Exception as e:
    print(f"❌ SMTP connection failed: {e}")
```

### 3. Test Authentication
```python
import smtplib
from utils import SENDER_EMAIL_ID, APP_PASSWORD

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(SENDER_EMAIL_ID, APP_PASSWORD)
    print("✅ Gmail authentication successful")
    server.quit()
except Exception as e:
    print(f"❌ Gmail authentication failed: {e}")
```

## 🚨 Emergency Fixes

### If Nothing Works:

#### Option 1: Generate New App Password
1. Delete current app password in Google Account
2. Generate new one
3. Update `utils.py` immediately
4. Test again

#### Option 2: Try Different Gmail Account
1. Use a different Gmail account
2. Set up 2FA and app password
3. Update configuration
4. Test

#### Option 3: Alternative Email Service
```python
# For Outlook/Hotmail
server = smtplib.SMTP('smtp-mail.outlook.com', 587)

# For Yahoo
server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
```

## 📞 Getting Help

### Error Messages to Look For:
- `Gmail authentication failed` → App password issue
- `Recipient email refused` → Invalid email format
- `SMTP server disconnected` → Network/firewall issue
- `Email sending failed` → General error

### Debug Output:
When testing, look for these messages:
```
📧 Attempting to send email to: recipient@email.com
📧 From: your_email@gmail.com
📧 Subject: Test Subject
📧 Logging into Gmail...
📧 Sending email...
✅ Email sent successfully!
```

## 🎯 Quick Fix Commands

### Test Email Immediately:
```powershell
cd "C:\Users\ayana\Desktop\AI Lead Enrichment\lead_enrichment"
python -c "from utils import send_email_with_gmail; print(send_email_with_gmail('your_email@gmail.com', 'Test', '<h1>Test</h1>'))"
```

### Check Configuration:
```powershell
python -c "from utils import SENDER_EMAIL_ID, APP_PASSWORD; print(f'Email: {SENDER_EMAIL_ID}'); print(f'Password: {APP_PASSWORD[:4]}...{APP_PASSWORD[-4:]}'); print(f'Length: {len(APP_PASSWORD)}')"
```

---

## 🎉 Success Indicators

When email is working correctly, you'll see:
- ✅ "Email sent successfully!" message
- 📧 Email appears in recipient's inbox
- 🎯 Formatted HTML email with lead data
- 📊 Hunter.io emails included in report

---

**Last Updated**: June 2025
**Version**: 1.0.0

*If you're still having issues after following this guide, the problem is likely with the Gmail app password setup. Generate a new one and try again!* 