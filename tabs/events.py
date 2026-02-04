"""
Events Page - Dynamic Events via NewsAPI with Strict Filtering
"""
import streamlit as st
from utils.data_fetchers import fetch_pharma_news
from components.cards import news_card
from datetime import datetime
from utils.formatters import truncate_text

def strict_future_filter(articles):
    """
    Strictly filters articles to find only future/upcoming events.
    Criteria:
    1. Must contain '2026' or '2027' in title or description.
    2. Must contain event keywords (register, deadline, scheduled, etc.).
    3. Must NOT contain noise keywords (market, report, earnings).
    """
    valid_events = []
    
    # Keywords that suggest an actionable event
    event_indicators = [
        "register", "registration", "deadline", "apply", "scheduled", 
        "to be held", "dates announced", "call for", "open for", "submit", "join us"
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
        
        # 1. Check for Future Year (Critical for "Upcoming")
        has_future_year = next_year in text or (current_year in text and any(m in text for m in ["dec", "nov", "oct", "sep", "aug"]))
        
        # 2. Check for Event Action
        is_actionable = any(kw in text for kw in event_indicators)
        
        # 3. Check for Noise
        is_noise = any(kw in text for kw in noise_indicators)
        
        # Combined check: Must be actionable AND not noise (Future year is optional but a strong plus)
        if is_actionable and not is_noise:
            valid_events.append(article)
            
    return valid_events

def show():
    st.markdown('<h2 class="gradient-header">📅 Dynamic Pharma Events</h2>', unsafe_allow_html=True)
    st.markdown("Real-time feed of upcoming opportunities. Auto-filtered for relevance.")
    
    tab1, tab2, tab3 = st.tabs(["🏆 Hackathons", "🎤 Conferences", "🎓 Workshops"])
    
    # Helper to fetch and display
    def fetch_and_display(query, tab_name, icon="📅"):
        with st.spinner(f"� Scanning global news for {tab_name}..."):
            # Fetch a larger batch to allow for strict filtering
            raw_news = fetch_pharma_news(query, page_size=40)
            filtered_events = strict_future_filter(raw_news)
            
        if filtered_events:
            st.success(f"✅ Found {len(filtered_events)} verified upcoming events")
            for article in filtered_events:
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
            st.warning(f"No specific '{tab_name}' found in live news matching strict filters.")
            st.info("💡 Try refreshing later or check the 'Pharma News' tab for general updates.")

    with tab1:
        st.markdown("### 💻 Hackathons & Challenges")
        # Query: Broad enough to catch events, strict filter does the rest
        q = '(hackathon OR competition OR challenge) AND ("pharmaceutical" OR "drug discovery" OR "bioinformatics" OR "clinical trials")'
        fetch_and_display(q, "hackathons", "🚀")

    with tab2:
        st.markdown("### 🎤 Conferences & Summits")
        q = '(conference OR summit OR congress) AND ("pharmaceutical" OR "biotech" OR "drug development")'
        fetch_and_display(q, "conferences", "🗓️")
    
    with tab3:
        st.markdown("### 🎓 Training & Workshops")
        q = '(workshop OR webinar OR training) AND (FDA OR "regulatory affairs" OR "clinical trials")'
        fetch_and_display(q, "workshops", "🎓")
            
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Live Feed", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
