# 🔌 API Integration Guide - AI Lead Enrichment

## 📋 Overview

This guide covers all 6 API integrations used in the AI Lead Enrichment Stack, including setup, usage, limits, and best practices.

## 🔑 API Services Summary

| Service | Purpose | Free Tier | Upgrade Cost |
|---------|---------|-----------|--------------|
| 📊 PeopleDataLabs | Personal/Professional Data | 1000 req/month | $0.05/request |
| 🎯 Apollo.io | Contact Information | 200 req/month | $49/month |
| 📧 Hunter.io | Email Discovery | 25 req/month | $49/month |
| 🔍 SERP API | Google Search | 100 searches/month | $50/month |
| 🤖 OpenAI | AI Analysis | Pay-per-token | ~$0.01/request |
| 📤 Gmail SMTP | Email Sending | Free | Free |

## 📊 PeopleDataLabs API

### Setup & Configuration

#### Getting API Key
1. Visit [PeopleDataLabs](https://www.peopledatalabs.com/)
2. Sign up for free account
3. Navigate to Dashboard → API Keys
4. Copy your API key

#### Configuration
```python
PEOPLEDATALABS_API_KEY = "your_pdl_key_here"
PDL_BASE_URL = "https://api.peopledatalabs.com/v5/person/enrich"
```

### API Integration

#### Function Implementation
```python
def enrich_with_ppld(name, company, email=None):
    """Enrich lead data using PeopleDataLabs API"""
    
    # Build search parameters
    params = {
        'api_key': PEOPLEDATALABS_API_KEY,
        'name': name,
        'company': company
    }
    
    if email:
        params['email'] = email
    
    try:
        response = requests.get(PDL_BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"PeopleDataLabs API Error: {e}")
        return None
```

#### Response Format
```json
{
    "status": 200,
    "data": {
        "full_name": "John Doe",
        "first_name": "John",
        "last_name": "Doe",
        "linkedin_url": "https://linkedin.com/in/johndoe",
        "job_title": "CEO",
        "job_company_name": "Example Corp",
        "emails": ["john@example.com"],
        "education": [
            {
                "school": "Harvard University",
                "degree_name": "MBA",
                "start_date": "2010",
                "end_date": "2012"
            }
        ],
        "experience": [
            {
                "company": "Example Corp",
                "title": "CEO",
                "start_date": "2015",
                "end_date": null
            }
        ]
    }
}
```

#### Best Practices
- **Search Strategy**: Use name + company for best results
- **Rate Limiting**: 1000 requests/month on free tier
- **Data Quality**: Higher accuracy with LinkedIn profiles
- **Error Handling**: Always check status code and handle nulls

### Rate Limits & Costs
- **Free Tier**: 1000 requests/month
- **Paid Plans**: $0.05 per successful request
- **Enterprise**: Custom pricing for high volume

## 🎯 Apollo.io API

### Setup & Configuration

#### Getting API Key
1. Visit [Apollo.io](https://www.apollo.io/)
2. Create free account
3. Go to Settings → Integrations → API
4. Generate API key

#### Configuration
```python
APOLLO_API_KEY = "your_apollo_key_here"
APOLLO_BASE_URL = "https://api.apollo.io/v1/people/match"
```

### API Integration

#### Function Implementation
```python
def enrich_with_apollo(name, company):
    """Enrich lead data using Apollo.io API"""
    
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'X-Api-Key': APOLLO_API_KEY
    }
    
    data = {
        'first_name': name.split()[0] if name else '',
        'last_name': ' '.join(name.split()[1:]) if len(name.split()) > 1 else '',
        'organization_name': company
    }
    
    try:
        response = requests.post(APOLLO_BASE_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Apollo API Error: {e}")
        return None
```

#### Response Format
```json
{
    "person": {
        "id": "5f7b1234567890abcdef1234",
        "first_name": "John",
        "last_name": "Doe",
        "name": "John Doe",
        "linkedin_url": "https://linkedin.com/in/johndoe",
        "title": "CEO",
        "email": "john@example.com",
        "organization": {
            "id": "5f7b1234567890abcdef5678",
            "name": "Example Corp",
            "website_url": "https://example.com",
            "industry": "Technology"
        }
    }
}
```

#### Best Practices
- **Name Parsing**: Split first/last name properly
- **Company Matching**: Use exact company names
- **Data Validation**: Check for null values
- **Rate Limiting**: Monitor monthly usage

### Rate Limits & Costs
- **Free Tier**: 200 requests/month
- **Basic Plan**: $49/month (1000 credits)
- **Professional**: $79/month (3000 credits)
- **Organization**: $119/month (6000 credits)

## 📧 Hunter.io API

### Setup & Configuration

#### Getting API Key
1. Visit [Hunter.io](https://hunter.io/)
2. Sign up for free account
3. Go to Dashboard → API
4. Copy your API key

#### Configuration
```python
HUNTER_API_KEY = "your_hunter_key_here"
HUNTER_BASE_URL = "https://api.hunter.io/v2/domain-search"
```

### API Integration

#### Function Implementation
```python
def enrich_with_hunter(company):
    """Find emails using Hunter.io domain search"""
    
    # Extract domain from company name or use as domain
    domain = company.lower().replace(' ', '') + '.com'
    if '.' in company:
        domain = company
    
    params = {
        'domain': domain,
        'api_key': HUNTER_API_KEY,
        'limit': 10
    }
    
    try:
        response = requests.get(HUNTER_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('data', {}).get('emails', [])
    except requests.exceptions.RequestException as e:
        print(f"Hunter.io API Error: {e}")
        return []
```

#### Response Format
```json
{
    "data": {
        "domain": "example.com",
        "emails": [
            {
                "value": "john@example.com",
                "type": "personal",
                "confidence": 94,
                "sources": [
                    {
                        "domain": "linkedin.com",
                        "uri": "https://linkedin.com/in/johndoe",
                        "extracted_on": "2025-01-15",
                        "last_seen_on": "2025-06-15",
                        "still_on_page": true
                    }
                ],
                "first_name": "John",
                "last_name": "Doe",
                "position": "CEO",
                "position_raw": "Chief Executive Officer",
                "seniority": "executive",
                "department": "executive",
                "linkedin": "https://linkedin.com/in/johndoe",
                "twitter": null,
                "phone_number": null,
                "verification": {
                    "date": "2025-06-15",
                    "status": "accept_all"
                }
            }
        ]
    }
}
```

#### Confidence Scoring
- **90-100%**: 🟢 Very High (Green)
- **70-89%**: 🟡 High (Yellow)  
- **50-69%**: 🟠 Medium (Orange)
- **0-49%**: 🔴 Low (Red)

#### Best Practices
- **Domain Strategy**: Try company.com first, then variations
- **Verification**: Check verification status
- **Confidence**: Focus on 90%+ confidence emails
- **Rate Limiting**: Only 25 requests/month on free tier

### Rate Limits & Costs
- **Free Tier**: 25 requests/month
- **Starter**: $49/month (1000 requests)
- **Growth**: $99/month (5000 requests)
- **Business**: $199/month (20000 requests)

## 🔍 SERP API (Google Search)

### Setup & Configuration

#### Getting API Key
1. Visit [SERP API](https://serpapi.com/)
2. Create free account
3. Dashboard → API Key
4. Copy your key

#### Configuration
```python
SERP_API_KEY = "your_serp_key_here"
SERP_BASE_URL = "https://serpapi.com/search"
```

### API Integration

#### Function Implementation
```python
def google_search(query):
    """Perform Google search using SERP API"""
    
    params = {
        'engine': 'google',
        'q': query,
        'api_key': SERP_API_KEY,
        'num': 10
    }
    
    try:
        response = requests.get(SERP_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for result in data.get('organic_results', []):
            results.append({
                'title': result.get('title', ''),
                'link': result.get('link', ''),
                'snippet': result.get('snippet', '')
            })
        
        return results
    except requests.exceptions.RequestException as e:
        print(f"SERP API Error: {e}")
        return []
```

#### Search Strategies
```python
# Multiple search queries for comprehensive results
search_queries = [
    f"{name} {company} LinkedIn",
    f"{name} {company} contact email",
    f"{name} CEO {company} profile"
]
```

#### Response Format
```json
{
    "organic_results": [
        {
            "position": 1,
            "title": "John Doe - CEO at Example Corp | LinkedIn",
            "link": "https://linkedin.com/in/johndoe",
            "snippet": "John Doe is CEO at Example Corp. Connect with John on LinkedIn.",
            "date": "2025-06-15"
        }
    ]
}
```

#### Best Practices
- **Query Optimization**: Use specific search terms
- **Multiple Searches**: Try different query combinations
- **Result Filtering**: Focus on LinkedIn, company sites
- **Rate Limiting**: 100 searches/month on free tier

### Rate Limits & Costs
- **Free Tier**: 100 searches/month
- **Starter**: $50/month (5000 searches)
- **Production**: $150/month (15000 searches)
- **Enterprise**: Custom pricing

## 🤖 OpenAI API

### Setup & Configuration

#### Getting API Key
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create account and add payment method
3. Go to API Keys section
4. Create new secret key

#### Configuration
```python
OPENAI_API_KEY = "your_openai_key_here"

def get_openai_client():
    """Initialize OpenAI client"""
    from openai import OpenAI
    return OpenAI(api_key=OPENAI_API_KEY)
```

### API Integration

#### Function Implementation
```python
def ai_analyze_and_structure_lead_data(extracted_data, name, company):
    """Analyze lead data using ChatGPT"""
    
    client = get_openai_client()
    
    prompt = f"""
    Analyze this lead data for {name} at {company} and provide insights:
    
    Data: {json.dumps(extracted_data, indent=2)}
    
    Please provide:
    1. Professional summary
    2. Social media profiles found
    3. Contact recommendations
    4. Key insights
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a lead research expert."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return "AI analysis unavailable"
```

#### Token Management
```python
def extract_key_data_from_apis(ppld_data, apollo_data, hunter_data, serp_data):
    """Extract only essential data to reduce token usage"""
    
    extracted = {
        'personal_info': {},
        'professional_info': {},
        'emails_found': [],
        'search_results': []
    }
    
    # Extract key fields only
    if ppld_data and 'data' in ppld_data:
        data = ppld_data['data']
        extracted['personal_info'] = {
            'name': data.get('full_name'),
            'linkedin': data.get('linkedin_url'),
            'title': data.get('job_title'),
            'company': data.get('job_company_name')
        }
    
    # Similar extraction for other APIs...
    return extracted
```

#### Best Practices
- **Token Optimization**: Extract key data only
- **Prompt Engineering**: Clear, specific instructions
- **Error Handling**: Graceful fallbacks
- **Cost Monitoring**: Track token usage

### Rate Limits & Costs
- **Model**: GPT-4
- **Input Tokens**: $0.03 per 1K tokens
- **Output Tokens**: $0.06 per 1K tokens
- **Typical Request**: ~$0.01-0.03 per enrichment

## 📤 Gmail SMTP

### Setup & Configuration

#### Getting App Password
1. Enable 2-Factor Authentication on Gmail
2. Go to Google Account Settings
3. Security → 2-Step Verification → App passwords
4. Generate password for "Mail"

#### Configuration
```python
SENDER_EMAIL_ID = "your_email@gmail.com"
APP_PASSWORD = "your_16_char_app_password"
```

### Email Integration

#### Function Implementation
```python
def send_email_with_lead_data(recipient_email, subject, body):
    """Send email with lead enrichment data"""
    
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL_ID
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Add body
        msg.attach(MIMEText(body, 'html'))
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL_ID, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Email Error: {e}")
        return False
```

#### Email Templates
```python
def format_lead_email(enrichment_data, name, company):
    """Format enrichment data for email"""
    
    html_template = f"""
    <html>
    <body>
    <h2>Lead Enrichment Report: {name}</h2>
    <h3>Company: {company}</h3>
    
    <h4>🤖 AI Analysis</h4>
    <p>{enrichment_data.get('ai_analysis', 'N/A')}</p>
    
    <h4>📧 Emails Found</h4>
    <ul>
    {"".join([f"<li>{email}</li>" for email in enrichment_data.get('emails', [])])}
    </ul>
    
    <h4>🔗 Social Profiles</h4>
    <p>LinkedIn: {enrichment_data.get('linkedin', 'N/A')}</p>
    
    </body>
    </html>
    """
    
    return html_template
```

### Rate Limits & Costs
- **Gmail SMTP**: Free
- **Daily Limit**: 500 emails/day
- **Rate Limit**: 100 emails/hour
- **No additional costs**

## 🔄 API Orchestration

### Parallel Processing

#### Comprehensive Enrichment
```python
def comprehensive_lead_enrichment(name, company, email=None):
    """Execute all API calls and AI analysis"""
    
    print(f"🔍 Starting comprehensive enrichment for: {name}")
    
    # Step 1: Parallel API calls
    ppld_data = enrich_with_ppld(name, company, email)
    apollo_data = enrich_with_apollo(name, company)
    hunter_data = enrich_with_hunter(company)
    
    # Step 2: Google searches
    search_results = []
    queries = [
        f"{name} {company} LinkedIn",
        f"{name} {company} contact",
        f"{name} CEO {company}"
    ]
    
    for query in queries:
        results = google_search(query)
        search_results.extend(results)
    
    # Step 3: Extract key data
    extracted_data = extract_key_data_from_apis(
        ppld_data, apollo_data, hunter_data, search_results
    )
    
    # Step 4: AI analysis
    ai_analysis = ai_analyze_and_structure_lead_data(
        extracted_data, name, company
    )
    
    return {
        'ppld_data': ppld_data,
        'apollo_data': apollo_data,
        'hunter_data': hunter_data,
        'search_results': search_results,
        'ai_analysis': ai_analysis,
        'extracted_data': extracted_data
    }
```

### Error Handling Strategy

#### Graceful Degradation
```python
def safe_api_call(api_function, *args, **kwargs):
    """Safely call API with error handling"""
    try:
        return api_function(*args, **kwargs)
    except Exception as e:
        print(f"API call failed: {e}")
        return None

# Usage
ppld_data = safe_api_call(enrich_with_ppld, name, company, email)
apollo_data = safe_api_call(enrich_with_apollo, name, company)
```

## 📊 Monitoring & Analytics

### Usage Tracking

#### API Call Monitoring
```python
import datetime

def log_api_usage(api_name, status, tokens_used=0):
    """Log API usage for monitoring"""
    timestamp = datetime.datetime.now()
    print(f"[{timestamp}] {api_name}: {status} (Tokens: {tokens_used})")
    
    # Optional: Save to file or database
    with open('api_usage.log', 'a') as f:
        f.write(f"{timestamp},{api_name},{status},{tokens_used}\n")
```

#### Cost Calculation
```python
def calculate_enrichment_cost(enrichment_data):
    """Calculate approximate cost per enrichment"""
    
    costs = {
        'peopledatalabs': 0.05 if enrichment_data.get('ppld_data') else 0,
        'apollo': 0.25 if enrichment_data.get('apollo_data') else 0,  # $49/200
        'hunter': 1.96 if enrichment_data.get('hunter_data') else 0,  # $49/25
        'serp': 0.50 if enrichment_data.get('search_results') else 0,  # $50/100
        'openai': 0.02 if enrichment_data.get('ai_analysis') else 0   # Estimated
    }
    
    total_cost = sum(costs.values())
    return total_cost, costs
```

## 🛡️ Security Best Practices

### API Key Management
```python
import os
from cryptography.fernet import Fernet

def encrypt_api_key(api_key):
    """Encrypt API key for storage"""
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted = f.encrypt(api_key.encode())
    return encrypted, key

def decrypt_api_key(encrypted_key, key):
    """Decrypt API key"""
    f = Fernet(key)
    decrypted = f.decrypt(encrypted_key)
    return decrypted.decode()
```

### Rate Limiting
```python
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self):
        self.calls = defaultdict(list)
        self.limits = {
            'peopledatalabs': (1000, 30*24*3600),  # 1000 per month
            'apollo': (200, 30*24*3600),           # 200 per month
            'hunter': (25, 30*24*3600),            # 25 per month
            'serp': (100, 30*24*3600),             # 100 per month
        }
    
    def can_make_call(self, api_name):
        """Check if API call is within rate limits"""
        now = time.time()
        limit, window = self.limits.get(api_name, (float('inf'), 3600))
        
        # Clean old calls
        cutoff = now - window
        self.calls[api_name] = [t for t in self.calls[api_name] if t > cutoff]
        
        return len(self.calls[api_name]) < limit
    
    def record_call(self, api_name):
        """Record an API call"""
        self.calls[api_name].append(time.time())
```

## 🔮 Advanced Features

### Caching Strategy
```python
import json
import hashlib
from datetime import datetime, timedelta

class APICache:
    def __init__(self, cache_duration_hours=24):
        self.cache = {}
        self.cache_duration = timedelta(hours=cache_duration_hours)
    
    def get_cache_key(self, api_name, params):
        """Generate cache key"""
        key_data = f"{api_name}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, api_name, params):
        """Get cached result"""
        key = self.get_cache_key(api_name, params)
        if key in self.cache:
            data, timestamp = self.cache[key]
            if datetime.now() - timestamp < self.cache_duration:
                return data
        return None
    
    def set(self, api_name, params, data):
        """Cache result"""
        key = self.get_cache_key(api_name, params)
        self.cache[key] = (data, datetime.now())
```

### Async Processing
```python
import asyncio
import aiohttp

async def async_api_call(session, url, params=None, headers=None):
    """Make async API call"""
    try:
        async with session.get(url, params=params, headers=headers) as response:
            return await response.json()
    except Exception as e:
        print(f"Async API Error: {e}")
        return None

async def async_comprehensive_enrichment(name, company):
    """Async version of comprehensive enrichment"""
    async with aiohttp.ClientSession() as session:
        tasks = [
            async_peopledatalabs_call(session, name, company),
            async_apollo_call(session, name, company),
            async_hunter_call(session, company),
        ]
        
        results = await asyncio.gather(*tasks)
        return results
```

## 📈 Performance Optimization

### Response Time Optimization
- **Parallel Processing**: Execute API calls simultaneously
- **Caching**: Store results for repeated queries
- **Data Extraction**: Reduce ChatGPT token usage
- **Connection Pooling**: Reuse HTTP connections

### Cost Optimization
- **Smart Caching**: Avoid duplicate API calls
- **Selective Enrichment**: Skip APIs when data exists
- **Batch Processing**: Group similar requests
- **Token Management**: Optimize ChatGPT prompts

---

## 📞 API Support Contacts

### Service Support
- **PeopleDataLabs**: support@peopledatalabs.com
- **Apollo.io**: help@apollo.io
- **Hunter.io**: hello@hunter.io
- **SERP API**: hello@serpapi.com
- **OpenAI**: help@openai.com
- **Gmail**: Google Support

### Status Pages
- [PeopleDataLabs Status](https://status.peopledatalabs.com/)
- [Apollo Status](https://status.apollo.io/)
- [Hunter Status](https://status.hunter.io/)
- [OpenAI Status](https://status.openai.com/)

---

**Last Updated**: June 2025
**Version**: 1.0.0

*Complete API integration guide for the AI Lead Enrichment Automation Stack* 