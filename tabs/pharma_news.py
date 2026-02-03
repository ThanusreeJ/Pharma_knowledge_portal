"""
Pharma News Page
"""
import streamlit as st
from utils.data_fetchers import fetch_pharma_news
from components.cards import news_card, loading_skeleton
from utils.formatters import truncate_text
from datetime import datetime


def show():
    st.markdown('<h2 class="gradient-header">📰 Pharma News</h2>', unsafe_allow_html=True)
    st.markdown("Latest pharmaceutical industry news from around the world")
    
    # Search and filters
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "Search news",
            placeholder="e.g., COVID vaccine, FDA approval, drug trials...",
            label_visibility="collapsed"
        )
    
    with col2:
        page_size = st.selectbox(
            "Results",
            options=[5, 10, 20, 50],
            index=1,
            label_visibility="collapsed"
        )
    
    query = search_query if search_query else "pharmaceutical drug"
    
    # Fetch news
    with st.spinner("🔍 Fetching latest pharma news..."):
        articles = fetch_pharma_news(query=query, page_size=page_size)
    
    if not articles:
        st.warning("⚠️ No news articles found. Try a different search term or check your API key.")
        st.info("""
        **Tip:** Get a free NewsAPI key at https://newsapi.org/register
        
        Then create a `.env` file with:
        ```
        NEWSAPI_KEY=your_key_here
        ```
        """)
        return
    
    st.success(f"✅ Found {len(articles)} articles")
    
    # Display articles
    for article in articles:
        title = article.get("title", "No title")
        description = article.get("description", "No description available")
        source = article.get("source", {}).get("name", "Unknown")
        published_at = article.get("publishedAt", "")
        url = article.get("url", "#")
        
        # Format date
        try:
            date_obj = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
            formatted_date = date_obj.strftime("%B %d, %Y")
        except:
            formatted_date = published_at
        
        # Truncate description
        description = truncate_text(description, 200)
        
        news_card(
            title=title,
            description=description,
            source=source,
            date=formatted_date,
            url=url
        )
    
    # Refresh button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Refresh News", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
