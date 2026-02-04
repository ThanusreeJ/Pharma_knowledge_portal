"""
Events Page - Curated 2026 Events & Training
"""
import streamlit as st
from datetime import datetime

def event_card(title, date, location, description, url, badges=None, icon="�"):
    """
    Custom card for specific events with dates and registration links
    """
    badges_html = " ".join([
        f'<span style="background: rgba(99, 102, 241, 0.1); color: #6366F1; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; margin-right: 6px;">{b}</span>' 
        for b in (badges or [])
    ])
    
    st.markdown(f"""
    <div class="card" style="padding: 1.5rem; margin-bottom: 1rem; border-radius: 12px; background: var(--card-bg); border: 1px solid rgba(128, 128, 128, 0.1);">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div style="flex-grow: 1;">
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 1.2rem; margin-right: 0.5rem;">{icon}</span>
                    <h4 style="margin: 0; color: var(--text-primary);">{title}</h4>
                </div>
                <div style="margin-bottom: 0.8rem; color: var(--text-secondary); font-size: 0.9rem;">
                    <strong>🗓️ {date}</strong> &nbsp; | &nbsp; 📍 {location}
                </div>
                <p style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 1rem; line-height: 1.5;">{description}</p>
                {badges_html}
            </div>
            <a href="{url}" target="_blank" style="text-decoration: none;">
                <button style="background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%); color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: 500; font-size: 0.9rem; margin-left: 1rem; white-space: nowrap;">
                    View Details ↗
                </button>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show():
    st.markdown('<h2 class="gradient-header">📅 Upcoming 2026 Pharma Events</h2>', unsafe_allow_html=True)
    st.markdown("Planned upcoming hackathons, conferences, and confirmed training sessions for 2026.")
    
    tab1, tab2, tab3 = st.tabs(["🏆 Hackathons", "🎤 Conferences", "🎓 Training & Workshops"])
    
    with tab1:
        st.markdown("### 💻 Upcoming Hackathons (2026)")
        st.info("💡 Confirmed upcoming challenges for healthcare innovation")
        
        event_card(
            title="HSIL Hackathon 2026: Building High-Value Health Systems",
            date="April 10-11, 2026",
            location="Global / Hybrid",
            description="Leveraging AI to design solutions that strengthen health systems. Hosted by the Health Systems Innovation Lab at Harvard.",
            url="https://www.hsph.harvard.edu/health-systems-innovation-lab/",
            badges=["AI & Health", "Harvard", "Global"],
            icon="🏥"
        )
        
        event_card(
            title="FOSSEE OSHW Hackathon 2026",
            date="Feb 16 - Mar 16, 2026",
            location="Virtual / IIT Bombay",
            description="Open Source Hardware Hackathon focusing on affordable healthcare and assistive devices. Free registration.",
            url="https://fossee.in/", 
            badges=["Open Source", "Medical Devices", "Free"],
            icon="�️"
        )
        
        event_card(
            title="Biomaterials Hackathon 2026",
            date="March 13-15, 2026",
            location="Eindhoven, Netherlands",
            description="Innovate with biomaterials to address real-world health challenges like personalized implants and ATMPs.",
            url="https://smartbiomaterials.nl/",
            badges=["Biotech", "In-person", "Innovation"],
            icon="🧬"
        )

        st.markdown("---")
        st.markdown("#### 🔍 Platforms for More")
        st.markdown("[Devpost Health](https://devpost.com/hackathons?themes[]=Health) | [Reskilll](https://reskilll.com/) | [MIT Hacking Medicine](https://hackingmedicine.mit.edu/)")

    with tab2:
        st.markdown("### 🎤 Major Conferences (Registration Open)")
        st.info("💡 Key industry gatherings confirmed for 2026")
        
        event_card(
            title="SCOPE Summit 2026",
            date="Feb 2-5, 2026",
            location="Orlando, FL",
            description="New Date! The Summit for Clinical Ops Executives. Strategy and innovation in clinical trials.",
            url="https://www.scopesummit.com/",
            badges=["Clinical Ops", "Networking", "Feb 2026"],
            icon="🔬"
        )
        
        event_card(
            title="Pharma Forum 2026",
            date="March 22-25, 2026",
            location="Boston, MA",
            description="The premier conference for meeting and event management professionals in life sciences.",
            url="https://informaconnect.com/pharma-forum/",
            badges=["Life Sciences", "Management", "Boston"],
            icon="🤝"
        )
        
        event_card(
            title="INTERPHEX 2026",
            date="April 21-23, 2026",
            location="New York, NY",
            description="The leading global event that fuses industry innovation with expert-led technical education.",
            url="https://www.interphex.com/",
            badges=["Manufacturing", "Biotech", "NYC"],
            icon="🏭"
        )

        event_card(
            title="BIO International Convention 2026",
            date="June 22-25, 2026",
            location="San Diego, CA",
            description="The largest global event for the biotechnology industry. Registration opens Feb 2026.",
            url="https://www.bio.org/events/bio-international-convention",
            badges=["Biggest Event", "Biotech", "San Diego"],
            icon="🌍"
        )
        
    
    with tab3:
        st.markdown("### 🎓 Confirmed Training & Workshops")
        st.info("💡 Official regulatory and clinical training opportunities")
        
        event_card(
            title="FDA CDERLearn: Drug Regulation Training",
            date="On-Demand / 2026",
            location="Online (Free)",
            description="Official FDA training modules for industry. Covers marketing authorization, clinical study sponsorship, and CMC.",
            url="https://www.fda.gov/drugs/resources-training-health-professionals/cderlearn-training-and-education",
            badges=["Official FDA", "Regulatory", "Free"],
            icon="🏛️"
        )

        event_card(
            title="FDA Food Traceability Rule Training",
            date="Spring 2026 (Bi-monthly)",
            location="Online & In-person",
            description="New workshop series by N.C. State & experts to help comply with the FDA Food Traceability Rule.",
            url="https://www.fda.gov/food/food-safety-modernization-act-fsma/fsma-final-rule-requirements-additional-traceability-records-certain-foods",
            badges=["Compliance", "Food Safety", "New Rule"],
            icon="🥗"
        )
        
        event_card(
            title="NIH Clinical Research Training",
            date="Ongoing 2026",
            location="Online (Free)",
            description="Comprehensive, free online training in clinical research from the National Institutes of Health.",
            url="https://clinicalcenter.nih.gov/training/training.html",
            badges=["NIH", "Clinical Trials", "Certification"],
            icon="⚕️"
        )
            
    st.markdown("<br>", unsafe_allow_html=True)
    st.warning("⚠️ **Note:** All dates and locations are based on current announcements and subject to change by organizers.")
