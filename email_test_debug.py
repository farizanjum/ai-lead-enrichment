#!/usr/bin/env python3
"""
Email Test Debug Script
Run this to test and debug email functionality
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_email_config():
    """Test email configuration and troubleshoot issues"""
    
    print("🔍 EMAIL CONFIGURATION TEST")
    print("=" * 50)
    
    # Try to load email credentials
    try:
        import streamlit as st
        SENDER_EMAIL_ID = st.secrets.get("SENDER_EMAIL_ID")
        APP_PASSWORD = st.secrets.get("APP_PASSWORD")
        print("📋 Using Streamlit secrets")
    except:
        SENDER_EMAIL_ID = os.getenv("SENDER_EMAIL_ID")
        APP_PASSWORD = os.getenv("APP_PASSWORD")
        print("📋 Using environment variables")
    
    # Check credentials
    print(f"📧 Email: {SENDER_EMAIL_ID}")
    print(f"🔑 Password: {'***' + APP_PASSWORD[-4:] if APP_PASSWORD and len(APP_PASSWORD) > 4 else 'NOT SET'}")
    
    if not SENDER_EMAIL_ID or not APP_PASSWORD:
        print("\n❌ CONFIGURATION ERROR:")
        print("Email credentials are not set. Please set:")
        print("- SENDER_EMAIL_ID=your_gmail@gmail.com")
        print("- APP_PASSWORD=your_gmail_app_password")
        return False
    
    # Test SMTP connection
    print("\n🔗 TESTING SMTP CONNECTION...")
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
        print("✅ Connected to Gmail SMTP server")
        
        server.starttls()
        print("✅ TLS encryption started")
        
        server.login(SENDER_EMAIL_ID, APP_PASSWORD)
        print("✅ Gmail authentication successful")
        
        server.quit()
        print("✅ SMTP connection closed properly")
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ AUTHENTICATION FAILED: {e}")
        print("\n🔧 TROUBLESHOOTING STEPS:")
        print("1. Make sure you're using an App Password, not your regular Gmail password")
        print("2. Enable 2-Factor Authentication on your Gmail account")
        print("3. Generate a new App Password: https://myaccount.google.com/apppasswords")
        print("4. Use the 16-character app password (no spaces)")
        return False
        
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {e}")
        print("\n🔧 TROUBLESHOOTING STEPS:")
        print("1. Check your internet connection")
        print("2. Make sure Gmail SMTP isn't blocked by firewall")
        print("3. Try using a VPN if behind corporate firewall")
        return False

def send_test_email():
    """Send a test email"""
    
    print("\n📧 SENDING TEST EMAIL...")
    
    # Get test recipient
    test_email = input("Enter test email address (or press Enter to skip): ").strip()
    
    if not test_email:
        print("⏭️ Skipping test email send")
        return
    
    # Import the fixed email function
    try:
        from utils import send_email_with_gmail
        
        subject = "🧪 AI Lead Enrichment - Email Test"
        body = """
        <html>
        <body>
            <h2>✅ Email Test Successful!</h2>
            <p>Your AI Lead Enrichment email configuration is working properly.</p>
            <p><strong>Test Details:</strong></p>
            <ul>
                <li>SMTP Connection: ✅ Success</li>
                <li>Authentication: ✅ Success</li>
                <li>Email Delivery: ✅ Success</li>
            </ul>
            <p>🎉 You're ready to send lead enrichment reports!</p>
        </body>
        </html>
        """
        
        result = send_email_with_gmail(test_email, subject, body)
        
        if result is True:
            print("✅ Test email sent successfully!")
        else:
            print(f"❌ Test email failed: {result}")
            
    except Exception as e:
        print(f"❌ Error importing email function: {e}")

def main():
    """Main test function"""
    
    print("🚀 AI LEAD ENRICHMENT - EMAIL DEBUG TOOL")
    print("=" * 60)
    
    # Test configuration
    config_ok = test_email_config()
    
    if config_ok:
        print("\n🎉 EMAIL CONFIGURATION IS VALID!")
        send_test_email()
    else:
        print("\n❌ EMAIL CONFIGURATION NEEDS ATTENTION")
        print("\n📖 QUICK SETUP GUIDE:")
        print("1. Go to https://myaccount.google.com/apppasswords")
        print("2. Generate a new App Password for 'Mail'")
        print("3. Set environment variables:")
        print("   SENDER_EMAIL_ID=your_gmail@gmail.com")
        print("   APP_PASSWORD=your_16_char_app_password")
        print("4. Re-run this test script")

if __name__ == "__main__":
    main() 