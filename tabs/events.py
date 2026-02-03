"""
Events Page - Hackathons, Conferences, Workshops
"""
import streamlit as st
import json
from pathlib import Path
from components.cards import event_card
from datetime import datetime


def load_events():
    """Load events from JSON file"""
    events_file = Path(__file__).parent.parent / "data" / "events.json"
    try:
        with open(events_file, 'r') as f:
            return json.load(f)
    except:
        return []


def show():
    st.markdown('<h2 class="gradient-header">📅 Events & Opportunities</h2>', unsafe_allow_html=True)
    st.markdown("Upcoming hackathons, conferences, and workshops in pharma & healthcare")
    
    # Load events
    events = load_events()
    
    if not events:
        st.error("❌ Could not load events data")
        return
    
    # Tabs for event types
    tab1, tab2, tab3, tab4 = st.tabs(["🏆 All Events", "💻 Hackathons", "🎤 Conferences", "🎓 Workshops"])
    
    with tab1:
        st.markdown("### All Upcoming Events")
        
        # Filter upcoming events
        upcoming = [e for e in events if e.get("status") == "upcoming"]
        
        if upcoming:
            st.success(f"✅ {len(upcoming)} upcoming events")
            
            for event in upcoming:
                event_card(
                    name=event.get("name", "N/A"),
                    date=event.get("date", "N/A"),
                    location=event.get("location", "N/A"),
                    event_type=event.get("type", "event"),
                    url=event.get("url", "#"),
                    description=event.get("description")
                )
        else:
            st.info("No upcoming events at the moment")
        
        st.markdown("---")
        st.markdown("### Recent Events")
        
        past = [e for e in events if e.get("status") == "past"]
        
        if past:
            for event in past:
                event_card(
                    name=event.get("name", "N/A") + " (Past)",
                    date=event.get("date", "N/A"),
                    location=event.get("location", "N/A"),
                    event_type=event.get("type", "event"),
                    url=event.get("url", "#"),
                    description=event.get("description")
                )
    
    with tab2:
        st.markdown("### 💻 Hackathons")
        
        hackathons = [e for e in events if e.get("type") == "hackathon" and e.get("status") == "upcoming"]
        
        if hackathons:
            st.success(f"✅ {len(hackathons)} upcoming hackathons")
            
            for event in hackathons:
                event_card(
                    name=event.get("name", "N/A"),
                    date=event.get("date", "N/A"),
                    location=event.get("location", "N/A"),
                    event_type="hackathon",
                    url=event.get("url", "#"),
                    description=event.get("description")
                )
        else:
            st.info("No upcoming hackathons. Check back soon!")
        
        st.markdown("---")
        st.markdown("#### 🔍 Find More Hackathons")
        st.markdown("""
        - [Devpost - Healthcare Hackathons](https://devpost.com/hackathons?themes[]=Health)
        - [Hacking Medicine](https://hackingmedicine.mit.edu/)
        - [Major League Hacking](https://mlh.io/seasons/2026/events)
        """)
    
    with tab3:
        st.markdown("### 🎤 Conferences")
        
        conferences = [e for e in events if e.get("type") == "conference" and e.get("status") == "upcoming"]
        
        if conferences:
            st.success(f"✅ {len(conferences)} upcoming conferences")
            
            for event in conferences:
                event_card(
                    name=event.get("name", "N/A"),
                    date=event.get("date", "N/A"),
                    location=event.get("location", "N/A"),
                    event_type="conference",
                    url=event.get("url", "#"),
                    description=event.get("description")
                )
        else:
            st.info("No upcoming conferences. Check back soon!")
        
        st.markdown("---")
        st.markdown("#### 🔍 Find More Conferences")
        st.markdown("""
        - [BIO Events Calendar](https://www.bio.org/events)
        - [Pharma Conferences](https://www.pharmaceutical-conferences.com/)
        - [Clinical Trials Arena Events](https://www.clinicaltrialsarena.com/events/)
        """)
    
    with tab4:
        st.markdown("### 🎓 Workshops")
        
        workshops = [e for e in events if e.get("type") == "workshop" and e.get("status") == "upcoming"]
        
        if workshops:
            st.success(f"✅ {len(workshops)} upcoming workshops")
            
            for event in workshops:
                event_card(
                    name=event.get("name", "N/A"),
                    date=event.get("date", "N/A"),
                    location=event.get("location", "N/A"),
                    event_type="workshop",
                    url=event.get("url", "#"),
                    description=event.get("description")
                )
        else:
            st.info("No upcoming workshops. Check back soon!")
        
        st.markdown("---")
        st.markdown("#### 🔍 Find More Workshops")
        st.markdown("""
        - [FDA Training & Continuing Education](https://www.fda.gov/training-and-continuing-education)
        - [NCBI Workshops](https://www.ncbi.nlm.nih.gov/home/workshops/)
        - [Coursera Pharmaceutical Courses](https://www.coursera.org/courses?query=pharmaceutical)
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 **Note:** Events are curated and updated regularly. Click links to verify dates and registration.")
