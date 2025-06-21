import streamlit as st
from enrichment_engine import comprehensive_lead_enrichment
from utils import send_email_with_gmail
import json

st.set_page_config(
    page_title="AI Lead Enrichment Stack",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI Lead Enrichment Stack")
st.markdown("**Powered by ChatGPT Intelligence** - Get comprehensive lead insights from multiple APIs")

# Sidebar for input
with st.sidebar:
    st.header("🔍 Lead Information")
    name = st.text_input("Full Name*", placeholder="e.g., Deepinder Goyal")
    email = st.text_input("Email (optional)", placeholder="e.g., ceo@zomato.com")
    company = st.text_input("Company (optional)", placeholder="e.g., Zomato")
    domain = st.text_input("Company Domain (optional)", placeholder="e.g., zomato.com")
    
    st.markdown("---")
    
    enrich_button = st.button("🚀 Enrich Lead", type="primary", use_container_width=True)

# Main content area
if enrich_button and name:
    with st.spinner("🤖 ChatGPT is analyzing data from multiple APIs..."):
        # Get comprehensive enrichment
        lead_data = comprehensive_lead_enrichment(
            name=name,
            email=email if email else None,
            company=company if company else None,
            domain=domain if domain else None
        )
    
    if "error" in lead_data and "ai_analysis" not in lead_data:
        st.error(f"❌ Enrichment failed: {lead_data['error']}")
    else:
        # Display the results
        st.success("✅ Lead enrichment completed successfully!")
        
        # Show basic info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Lead Name", lead_data.get("lead_name", name))
        with col2:
            st.metric("Company", lead_data.get("company_name", company or "N/A"))
        with col3:
            data_sources = lead_data.get("data_sources", [])
            st.metric("Data Sources", len(data_sources))
        
        # Hunter.io Emails Section (if found)
        if lead_data.get("hunter_emails"):
            st.header("📧 Hunter.io Discovered Emails")
            
            hunter_emails = lead_data["hunter_emails"]
            
            # Display in a nice table format
            if hunter_emails:
                st.write(f"Found **{len(hunter_emails)}** email(s) from the domain:")
                
                for i, email_data in enumerate(hunter_emails[:10], 1):  # Show first 10
                    with st.expander(f"📧 Email {i}: {email_data.get('value', 'N/A')}", expanded=i <= 3):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**👤 Contact Info:**")
                            st.write(f"• **Name:** {email_data.get('first_name', '')} {email_data.get('last_name', '')}".strip() or 'N/A')
                            st.write(f"• **Email:** {email_data.get('value', 'N/A')}")
                            st.write(f"• **Position:** {email_data.get('position', 'N/A')}")
                            st.write(f"• **Department:** {email_data.get('department', 'N/A')}")
                            st.write(f"• **Seniority:** {email_data.get('seniority', 'N/A')}")
                        
                        with col2:
                            st.write("**🔍 Verification Info:**")
                            confidence = email_data.get('confidence', 'N/A')
                            if confidence != 'N/A':
                                st.write(f"• **Confidence:** {confidence}%")
                                # Color code confidence
                                if confidence >= 90:
                                    st.success("🟢 High Confidence")
                                elif confidence >= 70:
                                    st.warning("🟡 Medium Confidence")
                                else:
                                    st.error("🔴 Low Confidence")
                            
                            linkedin_url = email_data.get('linkedin')
                            if linkedin_url and linkedin_url != 'N/A':
                                st.write(f"• **LinkedIn:** [Profile]({linkedin_url})")
                            
                            verification = email_data.get('verification', {})
                            if verification:
                                st.write(f"• **Verified:** {verification.get('date', 'N/A')}")
                                st.write(f"• **Status:** {verification.get('status', 'N/A')}")
            
            st.markdown("---")
        
        # Main analysis from ChatGPT
        st.header("🧠 ChatGPT Lead Analysis")
        
        if "ai_analysis" in lead_data:
            # Display ChatGPT's analysis in a nice format
            analysis = lead_data["ai_analysis"]
            
            # Create a container with custom styling
            with st.container():
                st.markdown("""
                <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #1f77b4;">
                """, unsafe_allow_html=True)
                
                # Split analysis into sections if it contains numbered sections or emojis
                if any(marker in analysis for marker in ["1.", "2.", "🎯", "💼", "🏢"]):
                    # Split by double newlines or emoji sections
                    sections = analysis.split("\n\n")
                    for section in sections:
                        if section.strip():
                            st.markdown(section.strip())
                            if len(sections) > 3:  # Only add separators if there are multiple sections
                                st.markdown("---")
                else:
                    st.markdown(analysis)
                
                st.markdown("</div>", unsafe_allow_html=True)
        
        # Tabs for additional data
        tab1, tab2 = st.tabs(["🔍 Raw API Data", "📊 Data Sources"])
        
        with tab1:
            st.subheader("Raw API Data")
            if "raw_api_data" in lead_data:
                # Show data sources that were successful
                for source, data in lead_data["raw_api_data"].items():
                    with st.expander(f"{source.replace('_', ' ').title()} Data"):
                        if isinstance(data, dict) and "error" not in data:
                            st.json(data)
                        elif isinstance(data, dict) and "error" in data:
                            st.error(f"Error: {data['error']}")
                        else:
                            st.json(data)
        
        with tab2:
            st.subheader("Data Sources Used")
            data_sources = lead_data.get("data_sources", [])
            
            for source in data_sources:
                source_name = source.replace("_", " ").title()
                if source in lead_data.get("raw_api_data", {}):
                    source_data = lead_data["raw_api_data"][source]
                    if isinstance(source_data, dict) and "error" in source_data:
                        st.error(f"❌ {source_name}: {source_data['error']}")
                    else:
                        st.success(f"✅ {source_name}: Data retrieved successfully")
                        
                        # Show brief summary of what was found
                        if source == "peopledatalabs" and source_data.get("data"):
                            person = source_data["data"]
                            st.write(f"   📋 Found: {person.get('full_name', 'N/A')} - {person.get('job_title', 'N/A')}")
                        elif source == "apollo" and source_data.get("person"):
                            person = source_data["person"]
                            st.write(f"   📋 Found: {person.get('name', 'N/A')} - {person.get('title', 'N/A')}")
                        elif source == "hunter" and source_data.get("data"):
                            emails_count = len(source_data["data"].get("emails", []))
                            st.write(f"   📧 Found: {emails_count} email(s)")
                        elif source == "google_searches":
                            total_results = 0
                            for query_data in source_data.values():
                                if isinstance(query_data, dict) and "results" in query_data:
                                    total_results += len(query_data["results"].get("organic_results", []))
                            st.write(f"   🔍 Found: {total_results} search results")
                else:
                    st.warning(f"⚠️ {source_name}: No data")
        
        # Email functionality - Always available after lead enrichment
        st.markdown("---")
        st.header("📧 Send Email Report")
        
        # Email input directly in the main area
        col1, col2 = st.columns([3, 1])
        
        with col1:
            email_recipient = st.text_input("📧 Enter email address to send this report:", 
                                          placeholder="your@email.com", 
                                          key="email_recipient_main")
        
        with col2:
            st.write("")  # Empty space for alignment
            st.write("")  # Empty space for alignment
            send_report_button = st.button("📧 Send Report", type="primary", use_container_width=True)
        
        if send_report_button:
            if email_recipient and email_recipient.strip():
                # Create email content
                email_subject = f"Lead Enrichment Report: {lead_data.get('lead_name', name)}"
                
                # Include Hunter emails in the report
                hunter_emails_text = ""
                if lead_data.get("hunter_emails"):
                    hunter_emails_text = "\n\nHUNTER.IO DISCOVERED EMAILS:\n"
                    for i, email_data in enumerate(lead_data["hunter_emails"][:5], 1):
                        name_str = f"{email_data.get('first_name', '')} {email_data.get('last_name', '')}".strip()
                        hunter_emails_text += f"{i}. {name_str} ({email_data.get('value', 'N/A')}) - {email_data.get('position', 'N/A')} - Confidence: {email_data.get('confidence', 'N/A')}%\n"
                
                # Format email body as HTML for better presentation
                analysis_html = lead_data.get('ai_analysis', 'No analysis available').replace('\n', '<br>')
                
                email_body = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <h1 style="color: #1f77b4; border-bottom: 2px solid #1f77b4;">🎯 AI Lead Enrichment Report</h1>
    
    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0;">
        <h3>📋 Lead Information</h3>
        <p><strong>Name:</strong> {lead_data.get('lead_name', name)}</p>
        <p><strong>Company:</strong> {lead_data.get('company_name', company or 'N/A')}</p>
        <p><strong>Data Sources:</strong> {', '.join(lead_data.get('data_sources', []))}</p>
    </div>
    
    <h3 style="color: #28a745;">🧠 ChatGPT Analysis</h3>
    <div style="background-color: #e9ecef; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">
        {analysis_html}
    </div>
    
    {f'''
    <h3 style="color: #dc3545;">📧 Hunter.io Discovered Emails</h3>
    <div style="background-color: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107;">
        {hunter_emails_text.replace(chr(10), '<br>')}
    </div>
    ''' if hunter_emails_text else ''}
    
    <hr style="margin: 30px 0; border: none; border-top: 1px solid #dee2e6;">
    
    <div style="text-align: center; color: #6c757d; font-size: 12px;">
        <p><strong>Generated by AI Lead Enrichment Stack</strong></p>
        <p>🤖 Powered by ChatGPT + Multiple APIs</p>
        <p>PeopleDataLabs • Apollo.io • Hunter.io • SERP API</p>
    </div>
</body>
</html>
"""
                
                # Show sending status
                with st.spinner("📧 Sending email..."):
                    result = send_email_with_gmail(email_recipient, email_subject, email_body)
                
                if result is True:
                    st.success("✅ Email sent successfully!")
                    st.balloons()
                else:
                    st.error(f"❌ Email failed: {result}")
                    st.write("**Debug Info:**")
                    st.write(f"- Recipient: {email_recipient}")
                    st.write(f"- Subject: {email_subject}")
                    st.write("- Check EMAIL_TROUBLESHOOTING.md for help")
            else:
                st.error("❌ Please enter a valid email address to send the report.")

elif enrich_button and not name:
    st.error("❌ Please enter a name to enrich the lead.")

# Instructions
if not enrich_button:
    st.markdown("---")
    st.header("🚀 How It Works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🔍 Data Collection**
        - PeopleDataLabs (Professional data)
        - Apollo.io (Contact verification)
        - Hunter.io (Email discovery)
        - Google Search (Recent insights)
        """)
    
    with col2:
        st.markdown("""
        **🤖 AI Analysis**
        - ChatGPT analyzes all data
        - Finds social media profiles
        - Creates engagement strategies
        - Suggests conversation starters
        """)
    
    with col3:
        st.markdown("""
        **📊 Actionable Results**
        - Comprehensive lead profile
        - Hunter.io email discoveries
        - Contact recommendations
        - Email reports available
        """)
    
    st.markdown("---")
    st.header("✨ New Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🔗 Social Media Research**
        - LinkedIn profile discovery
        - Twitter/X handles
        - CrunchBase profiles
        - Personal websites & blogs
        """)
    
    with col2:
        st.markdown("""
        **📧 Hunter.io Email Display**
        - Separate email section
        - Confidence scoring
        - Contact verification
        - LinkedIn profile links
        """)

# Footer
st.markdown("---")
st.markdown("**🤖 Powered by ChatGPT** | Integrates PeopleDataLabs, Apollo, Hunter.io, SERP API") 