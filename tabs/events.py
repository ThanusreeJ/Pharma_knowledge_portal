"""
Events Page - Hackathons, Conferences, Workshops
"""
import streamlit as st
from utils.data_fetchers import fetch_pharma_news
from components.cards import news_card
from datetime import datetime
from utils.formatters import truncate_text

def filter_events(articles, upcoming_keywords, past_keywords):
    """Filter articles into upcoming and past events based on keywords"""
    upcoming = []
    past = []
    
    for article in articles:
        title = article.get("title", "").lower()
        desc = article.get("description", "").lower() or ""
        text = f"{title} {desc}"
        
        # Skip irrelevant noise
        if any(x in text for x in ["market report", "earnings", "stocks", "shares", "finance", "robbery", "crime", "police"]):
            continue
            
        # Check for upcoming keywords
        is_upcoming = any(kw in text for kw in upcoming_keywords)
        
        if is_upcoming:
            upcoming.append(article)
        else:
            past.append(article)
            
    return upcoming, past

def render_event_section(articles, section_title, icon="📅"):
    """Render a list of event articles"""
    if articles:
        st.markdown(f"#### {section_title} ({len(articles)})")
        for article in articles:
            title = article.get("title", "No title")
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
                title=f"{icon} {title}",
                description=truncate_text(description, 200),
                source=source,
                date=f"Posted: {formatted_date}",
                url=url
            )
    else:
        st.info(f"No {section_title.lower()} found.")

def show():
    st.markdown('<h2 class="gradient-header">📅 Events & Opportunities</h2>', unsafe_allow_html=True)
    st.markdown("Latest pharma hackathons, conferences, and workshops (Live Feed)")
    
    # Tabs for event types
    tab1, tab2, tab3 = st.tabs(["🏆 Hackathons", "🎤 Conferences", "🎓 Workshops"])
    
    # Keywords for filtering
    upcoming_kw = ["upcoming", "register", "apply", "deadline", "scheduled", "to be held", "dates announced", "call for", "open for"]
    
    with tab1:
        st.markdown("### 💻 Hackathons & Challenges")
        
        with st.spinner("🔍 Curating hackathon updates..."):
            news = fetch_pharma_news(
                query='(hackathon OR competition OR challenge) AND ("pharmaceutical" OR "drug discovery" OR "bioinformatics" OR "clinical trials") -"market" -"shares"', 
                page_size=20
            )
            upcoming, past = filter_events(news, upcoming_kw, [])
        
        render_event_section(upcoming, "🚀 Upcoming & Open for Registration")
        st.markdown("---")
        render_event_section(past, "📜 Recent Hackathon News & Results", icon="📰")

    with tab2:
        st.markdown("### 🎤 Conferences & Summits")
        
        with st.spinner("🔍 Curating conference updates..."):
            news = fetch_pharma_news(
                query='(conference OR summit OR congress) AND ("pharmaceutical" OR "biotech" OR "drug development") -"market" -"earnings"', 
                page_size=20
            )
            upcoming, past = filter_events(news, upcoming_kw, [])
            
        render_event_section(upcoming, "🗓️ Scheduled Events")
        st.markdown("---")
        render_event_section(past, "📜 Recent Conference News", icon="📰")
    
    with tab3:
        st.markdown("### 🎓 Workshops & Training")
        
        with st.spinner("🔍 Curating workshops..."):
            news = fetch_pharma_news(
                query='(workshop OR webinar OR training) AND (FDA OR "regulatory affairs" OR "clinical trials" OR GMP) -"market" -"stocks"', 
                page_size=20
            )
            upcoming, past = filter_events(news, upcoming_kw, [])
            
        render_event_section(upcoming, "🎓 Open for Registration")
        st.markdown("---")
        render_event_section(past, "📜 Recent Training News", icon="📰")
            
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Events News", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
