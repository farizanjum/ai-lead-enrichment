from openai import OpenAI
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Union, Dict, Any
import json
import streamlit as st
import logging

# Load OpenAI API key from environment variable or Streamlit secrets
try:
    # Try Streamlit secrets first (for Streamlit Cloud)
    OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY")
except:
    # Fallback to environment variables (for local development)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print("DEBUG: OPENAI_API_KEY loaded:", "YES" if OPENAI_API_KEY else "NO")

# Initialize OpenAI client
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    client = None
    print("WARNING: OpenAI client not initialized - API key missing")

# Load email credentials from environment variables or Streamlit secrets
try:
    # Try Streamlit secrets first (for Streamlit Cloud)
    SENDER_EMAIL_ID = st.secrets.get("SENDER_EMAIL_ID", "your_gmail_address@gmail.com")
    APP_PASSWORD = st.secrets.get("APP_PASSWORD", "your_gmail_app_password")
except:
    # Fallback to environment variables (for local development)
    SENDER_EMAIL_ID = os.getenv("SENDER_EMAIL_ID", "your_gmail_address@gmail.com")
    APP_PASSWORD = os.getenv("APP_PASSWORD", "your_gmail_app_password")

print("DEBUG: SENDER_EMAIL_ID loaded:", "YES" if SENDER_EMAIL_ID != "your_gmail_address@gmail.com" else "PLACEHOLDER")
print("DEBUG: APP_PASSWORD loaded:", "YES" if APP_PASSWORD != "your_gmail_app_password" else "PLACEHOLDER")

def safe_join(data, separator=', '):
    """Safely join data, handling None values and non-iterable types"""
    if not data:
        return 'N/A'
    if isinstance(data, (list, tuple)):
        return separator.join(str(item) for item in data if item is not None)
    return str(data)

def extract_hunter_emails(hunter_data):
    """Extract and format Hunter.io emails separately"""
    if not hunter_data or not hunter_data.get('emails'):
        return "No emails found"
    
    emails = hunter_data.get('emails', [])
    if not isinstance(emails, list):
        return "No valid emails found"
    
    emails_info = []
    for email_data in emails[:10]:  # Limit to first 10 emails
        if not isinstance(email_data, dict):
            continue
            
        first_name = email_data.get('first_name', '')
        last_name = email_data.get('last_name', '')
        name = f"{first_name} {last_name}".strip() if first_name or last_name else 'N/A'
        
        email = email_data.get('value', 'N/A')
        position = email_data.get('position', 'N/A')
        linkedin = email_data.get('linkedin', 'N/A')
        confidence = email_data.get('confidence', 'N/A')
        
        emails_info.append(f"  • {name} ({email}) - {position} - Confidence: {confidence}% - LinkedIn: {linkedin}")
    
    return "\n".join(emails_info) if emails_info else "No valid emails found"

def extract_key_data_from_apis(all_api_data: Dict[str, Any]) -> str:
    """Extract only the most important data from APIs to avoid token limits"""
    extracted_info = []
    
    # Extract from PeopleDataLabs (include NULL values)
    if "peopledatalabs" in all_api_data:
        if all_api_data["peopledatalabs"].get("data"):
            person = all_api_data["peopledatalabs"]["data"]
            # Safe extraction with NULL value handling
            location_names = person.get('location_names')
            location_str = safe_join(location_names) if location_names else 'N/A'
            
            skills = person.get('skills')
            skills_str = safe_join(skills[:5] if skills else [])
            
            emails = person.get('emails')
            email_str = 'N/A'
            if emails and isinstance(emails, list) and len(emails) > 0:
                email_str = emails[0].get('address', 'N/A') if isinstance(emails[0], dict) else 'N/A'
            
            education = person.get('education')
            education_str = 'N/A'
            if education and isinstance(education, list) and len(education) > 0:
                education_str = education[0].get('school', {}).get('name', 'N/A') if isinstance(education[0], dict) else 'N/A'
            
            ppld_info = f"""
PeopleDataLabs Profile:
- Name: {person.get('full_name') or 'N/A'}
- Job Title: {person.get('job_title') or 'N/A'}
- Company: {person.get('job_company_name') or 'N/A'}
- Location: {location_str}
- LinkedIn: {person.get('linkedin_url') or 'N/A'}
- Twitter: {person.get('twitter_url') or 'N/A'}
- Email: {email_str}
- Education: {education_str}
- Skills: {skills_str}
- Industry: {person.get('industry') or 'N/A'}
- Job Start Date: {person.get('job_start_date') or 'N/A'}
- Experience Level: {person.get('job_title_levels') or 'N/A'}
"""
            extracted_info.append(ppld_info)
        else:
            extracted_info.append("PeopleDataLabs Profile: No data found or limited results")
    
    # Extract from Apollo (include NULL values)
    if "apollo" in all_api_data:
        if all_api_data["apollo"].get("person"):
            apollo_person = all_api_data["apollo"]["person"]
            organization = apollo_person.get('organization', {})
            
            apollo_info = f"""
Apollo Profile:
- Name: {apollo_person.get('name') or 'N/A'}
- Title: {apollo_person.get('title') or 'N/A'}
- Company: {organization.get('name') if organization else 'N/A'}
- LinkedIn: {apollo_person.get('linkedin_url') or 'N/A'}
- Twitter: {apollo_person.get('twitter_url') or 'N/A'}
- Email: {apollo_person.get('email') or 'N/A'}
- Phone: {apollo_person.get('phone') or 'N/A'}
- Location: {apollo_person.get('city') or 'N/A'}
"""
            extracted_info.append(apollo_info)
        else:
            extracted_info.append("Apollo Profile: No person data found")
    
    # Extract from Hunter (include NULL values and detailed email info)
    if "hunter" in all_api_data:
        if all_api_data["hunter"].get("data"):
            hunter_data = all_api_data["hunter"]["data"]
            emails_detail = extract_hunter_emails(hunter_data)
            
            # Safe email count
            emails = hunter_data.get('emails', [])
            email_count = len(emails) if isinstance(emails, list) else 0
            
            hunter_info = f"""
Hunter.io Domain Analysis:
- Domain: {hunter_data.get('domain') or 'N/A'}
- Company: {hunter_data.get('organization') or 'N/A'}
- Total Emails Found: {email_count}
- Email Pattern: {hunter_data.get('pattern') or 'N/A'}
- Webmail: {hunter_data.get('webmail') or 'N/A'}
- Accept All: {hunter_data.get('accept_all') or 'N/A'}

Found Emails:
{emails_detail}
"""
            extracted_info.append(hunter_info)
        else:
            extracted_info.append("Hunter.io Domain Analysis: No data found")
    
    # Extract key Google search results (only titles and snippets)
    if "google_searches" in all_api_data:
        search_info = "Google Search Results:\n"
        for query_key, search_data in all_api_data["google_searches"].items():
            if "results" in search_data and search_data["results"].get("organic_results"):
                organic_results = search_data["results"].get("organic_results", [])
                if isinstance(organic_results, list):
                    search_info += f"\nQuery: {search_data.get('query', 'N/A')}\n"
                    for i, result in enumerate(organic_results[:3]):  # Only top 3 results
                        if isinstance(result, dict):
                            title = result.get('title', 'N/A')
                            snippet = result.get('snippet', 'N/A')
                            link = result.get('link', 'N/A')
                            search_info += f"- {title}: {snippet[:100]}... (Link: {link})\n"
        extracted_info.append(search_info)
    
    return "\n".join(extracted_info)

def ai_analyze_and_structure_lead_data(all_api_data: Dict[str, Any], lead_name: str, company_name: str = "") -> Dict[str, Any]:
    """
    Pass essential API data through ChatGPT for intelligent analysis and let ChatGPT decide the structure
    """
    # Extract only key data to avoid token limits
    essential_data = extract_key_data_from_apis(all_api_data)
    
    # Extract Hunter.io emails for separate display
    hunter_emails = []
    if "hunter" in all_api_data and all_api_data["hunter"].get("data", {}).get("emails"):
        emails = all_api_data["hunter"]["data"]["emails"]
        if isinstance(emails, list):
            hunter_emails = emails
    
    prompt = f"""
You are an expert lead researcher and sales intelligence analyst. I'm providing you with data about a lead: {lead_name} {f"from {company_name}" if company_name else ""}.

Your task is to analyze this data and provide comprehensive insights. You have access to web search and should use your knowledge to provide additional context and research.

IMPORTANT: Please also research and find their social media profiles including:
- LinkedIn (if not already provided)
- Twitter/X profile
- CrunchBase profile (if they're a founder/executive)
- Instagram (if relevant for business)
- Facebook business page
- Personal website/blog
- GitHub (if they're technical)
- Medium/Substack (if they write)

Here's the data I collected:

{essential_data}

Please provide a comprehensive lead analysis. Structure your response however you think is most useful for a sales/business development professional. Include:

1. 🎯 Lead Summary & Key Facts
2. 💼 Professional Background & Career Insights
3. 🏢 Company Analysis & Industry Context
4. 🔗 Social Media & Online Presence (research and find their profiles)
5. 📞 Contact Strategy & Engagement Recommendations
6. 💬 Conversation Starters & Value Propositions
7. 🧠 Personality & Communication Style Assessment
8. 🎯 Potential Pain Points & Business Challenges
9. 📊 Additional Research Insights & Industry Trends
10. ⚡ Quick Action Items for Outreach

Feel free to make intelligent inferences based on the data and your knowledge. Provide actionable insights that would help someone successfully engage with this lead.

Make your analysis detailed, practical, and engaging. Use emojis and formatting to make it easy to read. Don't worry about JSON format - just provide the best possible analysis in whatever structure works best.
"""

    try:
        if not client:
            return {
                "error": "OpenAI client not available - API key not configured",
                "ai_analysis": f"AI analysis not available, but here's what we found:\n\n{essential_data}",
                "lead_name": lead_name,
                "company_name": company_name,
                "hunter_emails": hunter_emails,
                "raw_api_data": all_api_data
            }
            
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,  # Higher temperature for more creative insights
            max_tokens=3000  # Limit response to avoid issues
        )
        
        analysis_content = response.choices[0].message.content or "No analysis generated"
        
        # Return in a simple structure
        return {
            "ai_analysis": analysis_content,
            "lead_name": lead_name,
            "company_name": company_name,
            "data_sources": list(all_api_data.keys()),
            "hunter_emails": hunter_emails,  # Separate Hunter.io emails
            "raw_api_data": all_api_data
        }
        
    except Exception as e:
        print(f"Error in AI analysis: {e}")
        return {
            "error": f"AI analysis failed: {str(e)}",
            "ai_analysis": f"Analysis failed, but here's what we found:\n\n{essential_data}",
            "lead_name": lead_name,
            "company_name": company_name,
            "hunter_emails": hunter_emails,
            "raw_api_data": all_api_data
        }

def fill_missing_info_with_ai(input_data):
    if not client:
        return json.dumps({"error": "OpenAI client not available"})
        
    prompt = f"""
    Fill in missing details based on the partial info:
    {input_data}
    
    Return as JSON with keys: name, email, company, LinkedIn, Twitter, website.
    """
    res = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content

def send_email_with_gmail(recipient: str, subject: str, body: str) -> Union[bool, str]:
    """Send email using Gmail SMTP with improved error handling"""
    
    # Validate credentials
    if SENDER_EMAIL_ID == "your_gmail_address@gmail.com" or APP_PASSWORD == "your_gmail_app_password":
        return "Please update SENDER_EMAIL_ID and APP_PASSWORD in utils.py with your actual Gmail credentials."
    
    # Validate inputs
    if not recipient or not subject or not body:
        return "Recipient, subject, and body must all be provided."
    
    # Validate email format
    if "@" not in recipient or "." not in recipient:
        return "Invalid recipient email format."
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = str(SENDER_EMAIL_ID)
        msg['To'] = str(recipient)
        msg['Subject'] = str(subject)
        
        # Add body as HTML for better formatting
        msg.attach(MIMEText(body, 'html'))
        
        print(f"📧 Attempting to send email to: {recipient}")
        print(f"📧 From: {SENDER_EMAIL_ID}")
        print(f"📧 Subject: {subject}")
        
        # Connect to Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        print("📧 Logging into Gmail...")
        server.login(str(SENDER_EMAIL_ID), str(APP_PASSWORD))
        
        print("📧 Sending email...")
        text = msg.as_string()
        server.sendmail(str(SENDER_EMAIL_ID), str(recipient), text)
        server.quit()
        
        print("✅ Email sent successfully!")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        error_msg = f"Gmail authentication failed. Check your email and app password. Error: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg
    except smtplib.SMTPRecipientsRefused as e:
        error_msg = f"Recipient email refused: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg
    except smtplib.SMTPServerDisconnected as e:
        error_msg = f"SMTP server disconnected: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg
    except Exception as e:
        error_msg = f"Email sending failed: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg 