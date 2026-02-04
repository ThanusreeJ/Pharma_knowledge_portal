"""
Events Page - Hackathons, Conferences, Workshops
"""
import streamlit as st
from utils.data_fetchers import fetch_pharma_news
from components.cards import news_card
from datetime import datetime
from utils.formatters import truncate_text


def show():
    st.markdown('<h2 class="gradient-header">📅 Events & Opportunities</h2>', unsafe_allow_html=True)
    st.markdown("Latest news about upcoming hackathons, conferences, and workshops")
    
    # Tabs for event types
    tab1, tab2, tab3 = st.tabs(["🏆 Hackathons", "🎤 Conferences", "🎓 Workshops"])
    
    with tab1:
        st.markdown("### 💻 Upcoming Hackathons & Challenges")
        st.info("💡 Showing latest announcements for upcoming and open competitions")
        
        with st.spinner("🔍 Searching for open hackathons..."):
            # Query focused on FUTURE events and REGISTRATION
            # Stricter filters: Removed generic "healthcare", added specific pharma terms
            hackathon_news = fetch_pharma_news(
                query='(hackathon OR competition OR challenge) AND ("pharmaceutical" OR "drug discovery" OR "bioinformatics" OR "pharmacovigilance" OR "clinical trials") AND ("upcoming" OR "register" OR "apply" OR "deadline" OR "announced") -"generative ai" -"chatgpt" -"crypto" -"blockchain"', 
                page_size=15
            )
        
        if hackathon_news:
            st.success(f"✅ Found {len(hackathon_news)} opportunities")
            
            for article in hackathon_news:
                title = article.get("title", "No title")
                description = article.get("description", "No description available")
                # Filter out snippets that look like past reports
                if "concluded" in description.lower() or "winner" in description.lower() or "held on" in description.lower():
                    continue
                    
                source = article.get("source", {}).get("name", "Unknown")
                published_at = article.get("publishedAt", "")
                url = article.get("url", "#")
                
                try:
                    date_obj = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                    formatted_date = date_obj.strftime("%B %d, %Y")
                except:
                    formatted_date = published_at
                
                news_card(
                    title=f"🚀 {title}",
                    description=truncate_text(description, 200),
                    source=source,
                    date=f"Posted: {formatted_date}",
                    url=url
                )
        else:
            st.info("No upcoming hackathon announcements found right now.")

    with tab2:
        st.markdown("### 🎤 Upcoming Conferences & Summits")
        st.info("💡 Showing latest announcements for scheduled conferences")
        
        with st.spinner("🔍 Searching for upcoming conferences..."):
            # Query focused on UPCOMING events
            # Added exclusions for purely tech/AI conferences unless pharma focused
            conf_news = fetch_pharma_news(
                query='(conference OR summit OR congress) AND (pharmaceutical OR "drug development" OR "medicinal chemistry" OR pharmacovigilance) AND ("scheduled" OR "to be held" OR "registration open" OR "dates announced") -"report" -"results" -"market report" -"ai summit"', 
                page_size=15
            )
        
        if conf_news:
            st.success(f"✅ Found {len(conf_news)} announcements")
            
            for article in conf_news:
                title = article.get("title", "No title")
                description = article.get("description", "No description available")
                # Filter out past event reports
                if "recap" in title.lower() or "highlights" in title.lower():
                    continue

                source = article.get("source", {}).get("name", "Unknown")
                published_at = article.get("publishedAt", "")
                url = article.get("url", "#")
                
                try:
                    date_obj = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                    formatted_date = date_obj.strftime("%B %d, %Y")
                except:
                    formatted_date = published_at
                
                news_card(
                    title=f"🗓️ {title}",
                    description=truncate_text(description, 200),
                    source=source,
                    date=f"Posted: {formatted_date}",
                    url=url
                )
        else:
            st.info("No upcoming conference announcements found.")
    
    with tab3:
        st.markdown("### 🎓 Upcoming Workshops & Training")
        
        with st.spinner("🔍 Searching for training opportunities..."):
            # Query focused on TRAINING and WORKSHOPS
            workshop_news = fetch_pharma_news(
                query='(workshop OR webinar OR training) AND (FDA OR "clinical trials" OR "regulatory affairs" OR "good manufacturing practice" OR GMP) AND ("upcoming" OR "register" OR "join us" OR "session")', 
                page_size=15
            )
        
        if workshop_news:
            st.success(f"✅ Found {len(workshop_news)} opportunities")
            
            for article in workshop_news:
                title = article.get("title", "No title")
                # Filter out obvious past reports
                if "report" in title.lower() or "summary" in title.lower():
                    continue
                    
                description = article.get("description", "No description available")
                source = article.get("source", {}).get("name", "Unknown")
                published_at = article.get("publishedAt", "")
                url = article.get("url", "#")
                
                try:
                    date_obj = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                    formatted_date = date_obj.strftime("%B %d, %Y")
                except:
                    formatted_date = published_at
                
                news_card(
                    title=f"🎓 {title}",
                    description=truncate_text(description, 200),
                    source=source,
                    date=f"Posted: {formatted_date}",
                    url=url
                )
        else:
            st.info("No upcoming workshop announcements found.")
            
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Events News", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
