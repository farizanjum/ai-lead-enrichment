import requests
import json
import os
import streamlit as st
from utils import ai_analyze_and_structure_lead_data
from typing import Dict, Any, Optional

# Load API keys from environment variables or Streamlit secrets
try:
    # Try Streamlit secrets first (for Streamlit Cloud)
    PPLD_KEY = st.secrets.get("PEOPLEDATALABS_API_KEY")
    APOLLO_KEY = st.secrets.get("APOLLO_API_KEY") 
    HUNTER_KEY = st.secrets.get("HUNTER_API_KEY")
    SERP_API_KEY = st.secrets.get("SERP_API_KEY")
except:
    # Fallback to environment variables (for local development)
    PPLD_KEY = os.getenv("PEOPLEDATALABS_API_KEY")
    APOLLO_KEY = os.getenv("APOLLO_API_KEY") 
    HUNTER_KEY = os.getenv("HUNTER_API_KEY")
    SERP_API_KEY = os.getenv("SERP_API_KEY")

print("DEBUG: PEOPLEDATALABS_API_KEY loaded:", "YES" if PPLD_KEY else "NO")
print("DEBUG: APOLLO_API_KEY loaded:", "YES" if APOLLO_KEY else "NO")
print("DEBUG: HUNTER_API_KEY loaded:", "YES" if HUNTER_KEY else "NO")
print("DEBUG: SERP_API_KEY loaded:", "YES" if SERP_API_KEY else "NO")

def enrich_with_ppld(email=None, name=None, company=None):
    url = "https://api.peopledatalabs.com/v5/person/enrich"
    params = {
        "api_key": PPLD_KEY,
        "email": email,
        "name": name,
        "company": company,
    }
    response = requests.get(url, params=params)
    return response.json()

def enrich_with_apollo(email):
    url = f"https://api.apollo.io/v1/people/match"
    headers = {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'User-Agent': 'AI-Lead-Enrichment/1.0'
    }
    params = {
        'api_key': APOLLO_KEY,
        'email': email
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def enrich_with_hunter(domain):
    url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={HUNTER_KEY}"
    response = requests.get(url)
    return response.json()

def google_search(query):
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": SERP_API_KEY,
        "engine": "google",
    }
    res = requests.get(url, params=params)
    return res.json()

def comprehensive_lead_enrichment(
    name: str, 
    email: Optional[str] = None, 
    company: Optional[str] = None,
    domain: Optional[str] = None
) -> Dict[str, Any]:
    """
    Comprehensive lead enrichment that collects data from all APIs 
    and passes it through ChatGPT for intelligent analysis and structuring
    """
    print(f"🔍 Starting comprehensive enrichment for: {name}")
    
    # Collect all API data
    all_api_data = {}
    
    # 1. PeopleDataLabs enrichment
    print("📊 Fetching PeopleDataLabs data...")
    try:
        ppld_data = enrich_with_ppld(email=email, name=name, company=company)
        all_api_data["peopledatalabs"] = ppld_data
        print(f"✅ PeopleDataLabs: {'Success' if ppld_data.get('status') == 200 else 'Limited data'}")
    except Exception as e:
        print(f"❌ PeopleDataLabs error: {e}")
        all_api_data["peopledatalabs"] = {"error": str(e)}
    
    # 2. Apollo enrichment (if email provided)
    if email:
        print("🚀 Fetching Apollo data...")
        try:
            apollo_data = enrich_with_apollo(email)
            all_api_data["apollo"] = apollo_data
            print(f"✅ Apollo: {'Success' if apollo_data.get('person') else 'No match found'}")
        except Exception as e:
            print(f"❌ Apollo error: {e}")
            all_api_data["apollo"] = {"error": str(e)}
    
    # 3. Hunter.io domain search (if domain provided)
    if domain:
        print("🎯 Fetching Hunter.io data...")
        try:
            hunter_data = enrich_with_hunter(domain)
            all_api_data["hunter"] = hunter_data
            print(f"✅ Hunter.io: {hunter_data.get('data', {}).get('emails', 0)} emails found")
        except Exception as e:
            print(f"❌ Hunter.io error: {e}")
            all_api_data["hunter"] = {"error": str(e)}
    
    # 4. Google Search for additional context
    search_queries = [
        f'"{name}" {company if company else ""} LinkedIn',
        f'"{name}" {company if company else ""} CEO founder',
        f'{company if company else name} news recent'
    ]
    
    print("🔍 Performing Google searches...")
    all_api_data["google_searches"] = {}
    
    for i, query in enumerate(search_queries):
        try:
            search_results = google_search(query)
            all_api_data["google_searches"][f"query_{i+1}"] = {
                "query": query,
                "results": search_results
            }
            print(f"✅ Search {i+1}: {len(search_results.get('organic_results', []))} results")
        except Exception as e:
            print(f"❌ Search {i+1} error: {e}")
            all_api_data["google_searches"][f"query_{i+1}"] = {
                "query": query,
                "error": str(e)
            }
    
    # 5. Pass all data through ChatGPT for intelligent analysis
    print("🤖 Analyzing data with ChatGPT...")
    try:
        structured_lead_profile = ai_analyze_and_structure_lead_data(
            all_api_data=all_api_data,
            lead_name=name,
            company_name=company or ""
        )
        print("✅ ChatGPT analysis completed successfully!")
        
        # Add the raw API data for reference
        structured_lead_profile["raw_api_data"] = all_api_data
        
        return structured_lead_profile
        
    except Exception as e:
        print(f"❌ ChatGPT analysis error: {e}")
        return {
            "error": f"ChatGPT analysis failed: {str(e)}",
            "raw_api_data": all_api_data,
            "lead_summary": {
                "full_name": name,
                "company": company or "Unknown",
                "confidence_score": "Low - Analysis Error"
            }
        } 