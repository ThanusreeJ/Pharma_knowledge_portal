"""
Events Page - Curated Resource Directory
"""
import streamlit as st
from components.cards import event_card # Reuse generic card or create simple resource card

def resource_card(title, description, url, badges=None, icon="🔗"):
    """Custom card for resources with external links"""
    st.markdown(f"""
    <div class="card" style="padding: 1.5rem; margin-bottom: 1rem; border-radius: 12px; background: var(--card-bg); border: 1px solid rgba(128, 128, 128, 0.1);">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div style="flex-grow: 1;">
                <h4 style="margin: 0 0 0.5rem 0; color: var(--text-primary);">{icon} {title}</h4>
                <p style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 0.8rem;">{description}</p>
                {" ".join([f'<span style="background: rgba(99, 102, 241, 0.1); color: #6366F1; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; margin-right: 6px;">{b}</span>' for b in (badges or [])])}
            </div>
            <a href="{url}" target="_blank" style="text-decoration: none;">
                <button style="background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%); color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: 500; font-size: 0.9rem; margin-left: 1rem;">
                    Open ↗
                </button>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show():
    st.markdown('<h2 class="gradient-header">📅 Pharma Events & Opportunities</h2>', unsafe_allow_html=True)
    st.markdown("Verified platforms to find upcoming hackathons, conferences, and training in 2026")
    
    # Tabs for event types
    tab1, tab2, tab3 = st.tabs(["🏆 Hackathon Platforms", "🎤 Conference Directories", "🎓 Training & Workshops"])
    
    with tab1:
        st.markdown("### 💻 Find Healthcare & Pharma Hackathons")
        st.info("💡 Best platforms to find verified competitions and coding challenges")
        
        resource_card(
            "Devpost: Health Hackathons",
            "The world's largest hackathon platform. Directly search for active 'Health' and 'Life Sciences' challenges.",
            "https://devpost.com/hackathons?themes[]=Health",
            badges=["Global", "Virtual & In-person", "Huge Community"],
            icon="🚀"
        )
        
        resource_card(
            "Reskilll: Innovation Challenges",
            "Platform for student and professional hackathons, often partnering with major tech and pharma companies.",
            "https://reskilll.com/", 
            badges=["Student Focused", "Innovation", "Tech meets Pharma"],
            icon="💡"
        )
        
        resource_card(
            "MIT Hacking Medicine",
            "Premier healthcare innovation ecosystem. Hosts the famous 'Grand Hack' and other global events.",
            "https://hackingmedicine.mit.edu/",
            badges=["Prestigious", "Innovation", "MIT"],
            icon="🏥"
        )

        resource_card(
            "HackerEarth: Healthcare Challenges",
            "Major platform hosting corporate hackathons for big pharma and healthcare tech companies.",
            "https://www.hackerearth.com/challenges/hackathon/",
            badges=["Corporate", "Hiring Opportunities", "Global"],
            icon="💻"
        )
        
        st.markdown("---")
        st.markdown("#### 🔍 Upcoming Highlight (2026)")
        st.markdown("""
        - **BioHackathon Europe**: Annual event for bioinformatics and life sciences standards. [Visit Website](https://www.biohackathon-europe.org/)
        - **Health Systems Innovation Lab (HSIL)**: Developing high-value health system solutions. [Learn More](https://www.hsph.harvard.edu/health-systems-innovation-lab/)
        """)

    with tab2:
        st.markdown("### 🎤 Global Pharmaceutical Conferences (2026 Directory)")
        st.info("💡 Curated directories and major event hubs")
        
        resource_card(
            "BIO International Convention",
            "The largest global event for the biotechnology industry. A must-attend for pharma networking.",
            "https://www.bio.org/events",
            badges=["Largest Global Event", "Biotech", "Networking"],
            icon="🌍"
        )
        
        resource_card(
            "EuroPharma Congress 2026",
            "Leading forum for Pharma researchers and professors. Covers pharmacology and toxicology.",
            "https://europe.pharmaceuticalconferences.com/",
            badges=["Europe", "Research", "Academic"],
            icon="🇪🇺"
        )
        
        resource_card(
            "TechTarget Healthcare Conference Calendar",
            "Comprehensive list of top healthcare IT and pharma conferences for 2026.",
            "https://www.techtarget.com/searchhealthit/tip/Top-healthcare-conferences-to-attend",
            badges=["Directory", "Health Tech", "Updated List"],
            icon="📅"
        )

        resource_card(
            "J.P. Morgan Healthcare Conference",
            "The premier investment symposium for the healthcare industry, held annually in San Francisco.",
            "https://www.jpmorgan.com/solutions/cib/insights/health-care-conference",
            badges=["Investment", "Industry Leaders", "San Francisco"],
            icon="�"
        )
        
    
    with tab3:
        st.markdown("### � Regulatory Training & Clinical Workshops")
        st.info("� Official sources for FDA training and clinical research certification")
        
        resource_card(
            "FDA CDERLearn",
            "Official FDA training and education for drug regulation. Free online courses and case studies.",
            "https://www.fda.gov/drugs/resources-training-health-professionals/cderlearn-training-and-education",
            badges=["Official FDA", "Regulatory", "Free"],
            icon="🏛️"
        )

        resource_card(
            "NIH Clinical Research Training",
            "Comprehensive, free online training in clinical research from the National Institutes of Health.",
            "https://clinicalcenter.nih.gov/training/training.html",
            badges=["NIH", "Clinical Research", "Free"],
            icon="�"
        )
        
        resource_card(
            "Coursera: Clinical Trials Specializations",
            "Professional certifications from Johns Hopkins and other top universities.",
            "https://www.coursera.org/search?query=clinical%20trials",
            badges=["Certification", "University Level", "Flexible"],
            icon="🎓"
        )
        
        resource_card(
            "SOCRA (Society of Clinical Research Associates)",
            "Workshops, conferences, and certification for clinical research professionals.",
            "https://www.socra.org/",
            badges=["Professional Society", "Certification", "Networking"],
            icon="�"
        )
            
    st.markdown("<br>", unsafe_allow_html=True)
    st.warning("⚠️ **Note:** External links open in a new tab. Verify registration details on the official event websites.")
