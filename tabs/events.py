"""
Events Page - Dynamic Events via NewsAPI with Strict Filtering & Fallback
"""
import streamlit as st
from utils.data_fetchers import fetch_pharma_news
from components.cards import news_card
from datetime import datetime
from utils.formatters import truncate_text

def smart_filter(articles, strict_mode=True):
    """
    Filters articles for events.
    - strict_mode=True: Enforces future year (2026/27) AND event keywords.
    - strict_mode=False: Only enforces event keywords (for recent/past events).
    """
    valid_events = []
    
    # Keywords that suggest an actionable event
    event_indicators = [
        "register", "registration", "deadline", "apply", "scheduled", 
        "to be held", "dates announced", "call for", "open for", "submit", "join us",
        "hackathon", "competition", "challenge", "summit", "conference"
    ]
    
    # Keywords that suggest noise/news/reports
    noise_indicators = [
        "market report", "earnings", "stocks", "shares", "finance", 
        "robbery", "crime", "police", "quarterly", "revenue", "profit",
        "analysis", "forecast", "growth", "cagr", "dividend"
    ]
    
    current_year = str(datetime.now().year)
    next_year = str(datetime.now().year + 1)
    
    for article in articles:
        title = article.get("title", "").lower()
        desc = (article.get("description", "") or "").lower()
        text = f"{title} {desc}"
        
        # 1. Check for Future Year (Critical for "Upcoming" in Strict Mode)
        has_future_year = next_year in text or (current_year in text and any(m in text for m in ["dec", "nov", "oct", "sep", "aug"]))
        
        # 2. Check for Event Context
        is_event_related = any(kw in text for kw in event_indicators)
        
        # 3. Check for Noise
        is_noise = any(kw in text for kw in noise_indicators)
        
        if is_noise:
            continue
            
        if strict_mode:
            # Must have Future Year + Event Context
            if has_future_year and is_event_related:
                valid_events.append(article)
        else:
            # Just needs to be relevant and not noise (for past/fallback)
            if is_event_related:
                valid_events.append(article)
            
    return valid_events

def show():
    st.markdown('<h2 class="gradient-header">📅 Dynamic Pharma Events</h2>', unsafe_allow_html=True)
    st.markdown("Real-time feed of opportunities. Auto-filtered for quality.")
    
    tab1, tab2, tab3 = st.tabs(["🏆 Hackathons", "🎤 Conferences", "🎓 Workshops"])
    
    # Helper to fetch and display
    def fetch_and_display(query, tab_name, icon="📅", allow_fallback=False):
        with st.spinner(f"🔍 Scanning global news for {tab_name}..."):
            # Fetch a larger batch
            raw_news = fetch_pharma_news(query, page_size=40)
            
            # 1. Try Strict Filtering (Upcoming 2026/Future)
            upcoming_events = smart_filter(raw_news, strict_mode=True)
            
            # 2. If no upcoming, get Recent/Past (Relaxed Filter)
            past_events = []
            if not upcoming_events and allow_fallback:
                past_events = smart_filter(raw_news, strict_mode=False)

        # Display Logic
        if upcoming_events:
            st.success(f"✅ Found {len(upcoming_events)} confirmed upcoming events")
            display_cards(upcoming_events, icon)
        elif past_events:
            st.warning(f"⚠️ No confirmed 'future' {tab_name} found yet.")
            st.info(f"📜 Showing {len(past_events)} recent {tab_name} & announcements instead:")
            display_cards(past_events, icon="📰")
        else:
            st.warning(f"No specific '{tab_name}' found in live news right now.")
            st.markdown("Try refreshing later or check major news outlets.")

    def display_cards(articles, icon):
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

    with tab1:
        st.markdown("### 💻 Hackathons & Challenges")
        # Query: Broad enough to catch events
        q = '(hackathon OR competition OR challenge) AND ("pharmaceutical" OR "drug discovery" OR "bioinformatics" OR "clinical trials")'
        # Enable fallback for Hackathons since they are rare
        fetch_and_display(q, "hackathons", "🚀", allow_fallback=True)

    with tab2:
        st.markdown("### 🎤 Conferences & Summits")
        q = '(conference OR summit OR congress) AND ("pharmaceutical" OR "biotech" OR "drug development")'
        fetch_and_display(q, "conferences", "🗓️", allow_fallback=True)
    
    with tab3:
        st.markdown("### 🎓 Training & Workshops")
        q = '(workshop OR webinar OR training) AND (FDA OR "regulatory affairs" OR "clinical trials")'
        fetch_and_display(q, "workshops", "🎓", allow_fallback=True)
            
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Live Feed", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
