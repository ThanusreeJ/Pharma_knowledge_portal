"""
Clinical Trials Page
"""
import streamlit as st
from utils.data_fetchers import fetch_clinical_trials
import pandas as pd


def show():
    st.markdown('<h2 class="gradient-header">🔬 Clinical Trials</h2>', unsafe_allow_html=True)
    st.markdown("Search clinical trials from ClinicalTrials.gov database")
    
    # Search interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "Search by condition, drug, or sponsor",
            placeholder="e.g., diabetes, cancer, Alzheimer's...",
            label_visibility="collapsed"
        )
    
    with col2:
        page_size = st.selectbox(
            "Results",
            options=[5, 10, 20, 50],
            index=1,
            label_visibility="collapsed"
        )
    
    query = search_query if search_query else "cancer"
    
    # Fetch trials
    with st.spinner("🔍 Searching clinical trials..."):
        trials = fetch_clinical_trials(query=query, page_size=page_size)
    
    if not trials:
        st.warning("⚠️ No trials found. Try a different search term.")
        return
    
    st.success(f"✅ Found {len(trials)} trials")
    
    # Display as cards
    for trial in trials:
        with st.container():
            st.markdown(f"""
            <div class="news-card fade-in">
                <div class="news-title">{trial.get('title', 'N/A')}</div>
                <div class="news-meta">
                    <span class="badge" style="background: #6366F120; color: #6366F1; border-color: #6366F150;">
                        {trial.get('nct_id', 'N/A')}
                    </span>
                    <span class="badge" style="background: #10B98120; color: #10B981; border-color: #10B98150;">
                        {trial.get('phase', 'N/A')}
                    </span>
                    <span class="badge" style="background: #F59E0B20; color: #F59E0B; border-color: #F59E0B50;">
                        {trial.get('status', 'N/A')}
                    </span>
                </div>
                <div class="news-meta" style="margin-top: 0.5rem;">
                    <span>👥 Enrollment: {trial.get('enrollment', 'N/A')}</span>
                </div>
                <div style="margin-top: 0.75rem;">
                    <a href="{trial.get('url', '#')}" target="_blank" style="font-size: 0.9rem;">
                        View on ClinicalTrials.gov →
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Refresh button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Results", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
