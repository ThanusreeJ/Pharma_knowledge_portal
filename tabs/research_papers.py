"""
Research Papers Page
"""
import streamlit as st
from utils.data_fetchers import fetch_research_papers
from components.cards import paper_card


def show():
    st.markdown('<h2 class="gradient-header">📚 Research Papers</h2>', unsafe_allow_html=True)
    st.markdown("Search pharmaceutical research papers from PubMed")
    
    # Search interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "Search papers",
            placeholder="e.g., cancer immunotherapy, diabetes treatment, COVID-19...",
            label_visibility="collapsed"
        )
    
    with col2:
        max_results = st.selectbox(
            "Results",
            options=[5, 10, 20, 50],
            index=1,
            label_visibility="collapsed"
        )
    
    query = search_query if search_query else "pharmaceutical drug development"
    
    # Fetch papers
    with st.spinner("🔍 Searching PubMed database..."):
        papers = fetch_research_papers(query=query, max_results=max_results)
    
    if not papers:
        st.warning("⚠️ No papers found. Try a different search term.")
        return
    
    st.success(f"✅ Found {len(papers)} papers")
    
    # Display papers
    for paper in papers:
        title = paper.get("title", "No title")
        authors = paper.get("authors", [])
        author_str = ", ".join(authors[:3])
        if len(authors) > 3:
            author_str += " et al."
        
        journal = paper.get("journal", "N/A")
        date = paper.get("date", "N/A")
        url = paper.get("url", "#")
        
        paper_card(
            title=title,
            authors=author_str if author_str else "Unknown authors",
            journal=journal,
            date=date,
            url=url
        )
    
    # Refresh button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Results", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
