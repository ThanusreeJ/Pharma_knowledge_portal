"""
Analytics Dashboard Page
"""
import streamlit as st
from utils.data_fetchers import fetch_analytics_data, fetch_pharma_news, fetch_clinical_trials
from components.cards import kpi_card
from utils.formatters import format_number
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def show():
    st.markdown('<h2 class="gradient-header">📊 Analytics Dashboard</h2>', unsafe_allow_html=True)
    st.markdown("Real-time pharmaceutical industry metrics and insights")
    
    # Fetch analytics data
    with st.spinner("📈 Loading analytics..."):
        data = fetch_analytics_data()
    
    # KPI Cards
    st.markdown("### 📌 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        kpi_card(
            label="FDA Approved Drugs",
            value=format_number(data.get("total_drugs", 0)),
            icon="💊"
        )
    
    with col2:
        kpi_card(
            label="Active Clinical Trials",
            value=format_number(data.get("active_trials", 0)),
            icon="🔬"
        )
    
    with col3:
        kpi_card(
            label="Research Papers (This Month)",
            value=format_number(data.get("recent_papers", 0)),
            icon="📚"
        )
    
    with col4:
        kpi_card(
            label="News Articles (Today)",
            value=format_number(data.get("news_count", 0)),
            icon="📰"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts
    st.markdown("### 📈 Trends & Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Clinical trials by phase
        st.markdown("#### Clinical Trials by Phase")
        
        phase_data = {
            "Phase": ["Phase 1", "Phase 2", "Phase 3", "Phase 4"],
            "Count": [1250, 2340, 1890, 980]
        }
        
        fig1 = px.pie(
            phase_data,
            values="Count",
            names="Phase",
            color_discrete_sequence=["#6366F1", "#8B5CF6", "#A855F7", "#C084FC"],
            hole=0.4
        )
        
        fig1.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E5E7EB", size=12)
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Drug approvals trend
        st.markdown("#### Monthly FDA Approvals Trend")
        
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        approvals = [45, 52, 48, 61, 55, 58]
        
        fig2 = go.Figure()
        
        fig2.add_trace(go.Scatter(
            x=months,
            y=approvals,
            mode='lines+markers',
            line=dict(color='#6366F1', width=3),
            marker=dict(size=10, color='#8B5CF6'),
            fill='tozeroy',
            fillcolor='rgba(99, 102, 241, 0.1)'
        ))
        
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E5E7EB"),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
            margin=dict(l=0, r=0, t=20, b=0)
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # Daily updates
    st.markdown("### 🔔 Daily Updates")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="New Clinical Trials (Today)",
            value="23",
            delta="5 vs yesterday",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="Research Papers Published",
            value="187",
            delta="12 vs yesterday",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            label="FDA Announcements",
            value="4",
            delta="-1 vs yesterday",
            delta_color="inverse"
        )
    
    # Top therapeutic areas
    st.markdown("### 🎯 Top Therapeutic Areas")
    
    areas_data = pd.DataFrame({
        "Therapeutic Area": ["Oncology", "Cardiology", "Neurology", "Immunology", "Infectious Disease"],
        "Active Trials": [3450, 2890, 2340, 2120, 1980],
        "Recent Papers": [5670, 4230, 3890, 3450, 3120]
    })
    
    fig3 = go.Figure()
    
    fig3.add_trace(go.Bar(
        name='Active Trials',
        x=areas_data["Therapeutic Area"],
        y=areas_data["Active Trials"],
        marker_color='#6366F1'
    ))
    
    fig3.add_trace(go.Bar(
        name='Recent Papers',
        x=areas_data["Therapeutic Area"],
        y=areas_data["Recent Papers"],
        marker_color='#8B5CF6'
    ))
    
    fig3.update_layout(
        barmode='group',
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E5E7EB"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    
    # Refresh button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Analytics", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
