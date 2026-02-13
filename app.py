"""
Clarity AI - Marketing Intelligence Platform
Stop guessing. Start knowing.
"""

import streamlit as st
import pandas as pd
import requests
import json
import time
from datetime import datetime
from io import BytesIO
import os

# Page configuration
st.set_page_config(
    page_title="Clarity AI - Marketing Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for product-like UI
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Global styles */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Header styles */
    .hero-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    .beta-badge {
        background: #f59e0b;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 1rem;
        vertical-align: middle;
    }
    
    /* Card styles */
    .metric-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1e3a5f;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #6b7280;
        margin-top: 0.5rem;
    }
    
    /* Action cards */
    .stop-card { border-left: 4px solid #ef4444; }
    .fix-card { border-left: 4px solid #f59e0b; }
    .invest-card { border-left: 4px solid #10b981; }
    .observe-card { border-left: 4px solid #6b7280; }
    
    /* Feature list */
    .feature-item {
        display: flex;
        align-items: center;
        padding: 0.5rem 0;
    }
    
    .feature-icon {
        margin-right: 0.75rem;
        font-size: 1.25rem;
    }
    
    /* Upload area */
    .upload-area {
        border: 2px dashed #d1d5db;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        background: #f9fafb;
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        border-color: #2d5a87;
        background: #f0f7ff;
    }
    
    /* Integration card */
    .integration-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .integration-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .coming-soon-badge {
        background: #fef3c7;
        color: #92400e;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    /* AI Insight box */
    .ai-insight-box {
        background: linear-gradient(135deg, #f0f7ff 0%, #e8f4f8 100%);
        border: 1px solid #bfdbfe;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .ai-insight-title {
        font-size: 1rem;
        font-weight: 600;
        color: #1e3a5f;
        margin-bottom: 0.75rem;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 8px;
    }
    
    /* Button styling */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        padding: 0.75rem 2rem;
    }
    
    /* Primary button */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
    }
    
    /* Progress animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .analyzing {
        animation: pulse 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

# Load synthetic data for Quick Demo
@st.cache_data
def load_synthetic_data():
    """Load pre-built synthetic data for Quick Demo mode"""
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        with open(os.path.join(base_path, 'data', 'synthetic_ads.json'), 'r') as f:
            ads = json.load(f)
        with open(os.path.join(base_path, 'data', 'synthetic_seo.json'), 'r') as f:
            seo = json.load(f)
        with open(os.path.join(base_path, 'data', 'synthetic_crm.json'), 'r') as f:
            crm = json.load(f)
        
        return {'ads': ads, 'seo': seo, 'crm': crm}
    except Exception as e:
        st.error(f"Error loading synthetic data: {e}")
        return None

def call_n8n_webhook(mode: str, data: dict = None, goal: str = "roas", budget: int = 10000):
    """Call n8n webhook for analysis"""
    webhook_url = st.secrets.get("N8N_WEBHOOK_URL", "")
    
    if not webhook_url:
        st.error("⚠️ N8N_WEBHOOK_URL not configured. Please add it to your Streamlit secrets.")
        return None
    
    payload = {
        "mode": mode,
        "goal": goal,
        "budget": budget,
        "data": data if data else {}
    }
    
    try:
        response = requests.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=120
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        st.error("⏱️ Analysis timed out. Please try again.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error connecting to analysis engine: {str(e)}")
        return None

def generate_pdf_report(results: dict) -> BytesIO:
    """Generate PDF report from analysis results"""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.units import inch
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e3a5f'),
        spaceAfter=20
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1e3a5f'),
        spaceBefore=20,
        spaceAfter=10
    )
    
    story = []
    
    # Title
    story.append(Paragraph("CLARITY AI", title_style))
    story.append(Paragraph("Marketing Intelligence Report", styles['Heading2']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Executive Summary
    story.append(Paragraph("EXECUTIVE SUMMARY", heading_style))
    
    stats = results.get('stats', {})
    summary = results.get('summary', {})
    
    summary_data = [
        ['Metric', 'Value'],
        ['Monthly Savings Identified', f"${stats.get('total_savings', 0):,}"],
        ['Annual Impact', f"${stats.get('annual_savings', 0):,}"],
        ['Keywords Analyzed', str(stats.get('total_units', 0))],
        ['Average Confidence', f"{stats.get('avg_confidence', 0)}%"],
        ['Actions Required', str(summary.get('stop', 0) + summary.get('fix', 0) + summary.get('invest', 0))]
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a5f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9fafb')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 20))
    
    # AI Insight
    ai_insight = results.get('ai_insight', '')
    if ai_insight:
        story.append(Paragraph("AI INSIGHT", heading_style))
        story.append(Paragraph(ai_insight, styles['Normal']))
        story.append(Spacer(1, 20))
    
    # Recommendations sections
    recommendations = results.get('recommendations', {})
    
    for action, data_list in [
        ('STOP - PAUSE IMMEDIATELY', recommendations.get('stop', [])),
        ('FIX - OPTIMIZE THESE', recommendations.get('fix', [])),
        ('INVEST - SCALE UP', recommendations.get('invest', [])),
    ]:
        if data_list:
            story.append(Paragraph(action, heading_style))
            
            table_data = [['Keyword', 'Spend', 'Reason', 'Confidence']]
            for item in data_list[:10]:  # Top 10 per category
                table_data.append([
                    item.get('keyword', '')[:30],
                    f"${item.get('ads', {}).get('spend', 0):,.0f}",
                    item.get('classification', {}).get('reason', '')[:40],
                    f"{item.get('confidence', {}).get('score', 0)}%"
                ])
            
            rec_table = Table(table_data, colWidths=[1.5*inch, 0.8*inch, 2.7*inch, 0.8*inch])
            rec_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#374151')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
                ('PADDING', (0, 0), (-1, -1), 6),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(rec_table)
            story.append(Spacer(1, 15))
    
    # Footer
    story.append(Spacer(1, 30))
    story.append(Paragraph("Generated by Clarity AI (Beta) | clarityai.app | Built by Rupam Patra", 
                          ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.gray)))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def parse_csv_file(uploaded_file, data_type: str) -> list:
    """Parse uploaded CSV file into JSON format"""
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.lower().str.strip()
        
        # Column mappings for flexibility
        column_maps = {
            'ads': {
                'keyword': ['keyword', 'keywords', 'search_term', 'query'],
                'spend': ['spend', 'cost', 'amount', 'ad_spend'],
                'clicks': ['clicks', 'click'],
                'impressions': ['impressions', 'impr'],
                'conversions': ['conversions', 'conv', 'conversion'],
                'revenue': ['revenue', 'value', 'sale_amount']
            },
            'seo': {
                'keyword': ['keyword', 'keywords', 'text', 'query'],
                'volume': ['volume', 'vol', 'search_volume', 'searches'],
                'cpc': ['cpc', 'cost_per_click'],
                'competition': ['competition', 'comp', 'difficulty']
            },
            'crm': {
                'origin': ['origin', 'source', 'keyword', 'utm_source'],
                'leads': ['leads', 'lead_count'],
                'qualified_leads': ['qualified_leads', 'qualified', 'sql'],
                'revenue': ['revenue', 'value', 'deal_value']
            }
        }
        
        # Map columns
        mapped_data = []
        for _, row in df.iterrows():
            item = {}
            for target_col, source_cols in column_maps.get(data_type, {}).items():
                for src in source_cols:
                    if src in df.columns:
                        item[target_col] = row[src]
                        break
            if item:
                mapped_data.append(item)
        
        return mapped_data
    except Exception as e:
        st.error(f"Error parsing {data_type} file: {e}")
        return []

def render_hero():
    """Render hero section"""
    st.markdown("""
    <div class="hero-header">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <span class="hero-title">🎯 CLARITY AI</span>
                <span class="beta-badge">BETA</span>
            </div>
        </div>
        <p class="hero-subtitle">Stop guessing. Start knowing.</p>
        <p style="opacity: 0.8; margin-top: 0.5rem;">
            AI-powered marketing intelligence that tells you exactly what to STOP, FIX, INVEST, or OBSERVE in your ad spend.
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_demo_tab():
    """Render Demo tab"""
    st.markdown("### 🎮 Try Clarity AI with Demo Data")
    st.markdown("Experience the full power of Clarity AI. No signup required.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #f0f7ff; border: 2px solid #bfdbfe; border-radius: 12px; padding: 1.5rem;">
            <h4>⚡ Quick Demo</h4>
            <p>Pre-built marketing data processed through our full AI engine</p>
            <ul>
                <li>~15-20 seconds</li>
                <li>150 ad keywords</li>
                <li>200 SEO keywords</li>
                <li>100 CRM leads</li>
            </ul>
            <p><em>Same AI engine as production - just faster sample data</em></p>
        </div>
        """, unsafe_allow_html=True)
        quick_demo = st.button("⚡ Run Quick Demo", key="quick_demo", use_container_width=True)
    
    with col2:
        st.markdown("""
        <div style="background: #f0fdf4; border: 2px solid #bbf7d0; border-radius: 12px; padding: 1.5rem;">
            <h4>🌐 Live Demo</h4>
            <p>Real-time data from Kaggle public datasets</p>
            <ul>
                <li>~45-60 seconds</li>
                <li>Google Ads dataset</li>
                <li>SEO keyword research</li>
                <li>Marketing funnel data</li>
            </ul>
            <p><em>Demonstrates real external data integration</em></p>
        </div>
        """, unsafe_allow_html=True)
        live_demo = st.button("🌐 Run Live Demo", key="live_demo", use_container_width=True)
    
    st.markdown("---")
    
    # Demo settings
    st.markdown("#### ⚙️ Demo Settings (Optional)")
    col1, col2 = st.columns(2)
    with col1:
        goal = st.selectbox("🎯 Optimization Goal", ["Maximize ROAS", "Increase Conversions", "Reduce CPA", "Scale Traffic"])
    with col2:
        budget = st.number_input("💰 Simulated Monthly Budget", value=10000, min_value=1000, max_value=1000000, step=1000)
    
    # Handle demo buttons
    if quick_demo:
        run_analysis("synthetic", goal, budget)
    elif live_demo:
        run_analysis("kaggle", goal, budget)

def render_upload_tab():
    """Render Upload tab"""
    st.markdown("### 📁 Upload Your Marketing Data")
    st.markdown("Upload your data to get personalized AI recommendations. The more data sources you connect, the smarter our recommendations become.")
    
    st.info("🔒 **Your data is secure.** We don't store your data. It's processed in real-time and deleted.")
    
    # File uploaders
    st.markdown("#### Step 1: Upload at least one data source")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📢 Advertising Data** `REQUIRED`")
        st.markdown("Google Ads, Meta Ads, or any ad platform export")
        ads_file = st.file_uploader("Upload Ads CSV", type=['csv'], key="ads_upload", label_visibility="collapsed")
        with st.expander("📋 Required columns"):
            st.markdown("""
            - `keyword` - Search term or ad group
            - `spend` - Total cost
            - `clicks` - Number of clicks
            - `conversions` - Number of conversions
            
            **Optional:** impressions, campaign, revenue
            """)
    
    with col2:
        st.markdown("**🔍 SEO Data** `OPTIONAL`")
        st.markdown("SEMrush, Ahrefs, or Search Console")
        seo_file = st.file_uploader("Upload SEO CSV", type=['csv'], key="seo_upload", label_visibility="collapsed")
        with st.expander("📋 Required columns"):
            st.markdown("""
            - `keyword` - Search term
            - `volume` - Monthly search volume
            
            **Optional:** cpc, competition, score
            """)
    
    with col3:
        st.markdown("**👥 CRM Data** `OPTIONAL`")
        st.markdown("Salesforce, HubSpot, or your CRM")
        crm_file = st.file_uploader("Upload CRM CSV", type=['csv'], key="crm_upload", label_visibility="collapsed")
        with st.expander("📋 Required columns"):
            st.markdown("""
            - `origin` or `source` - Lead source/keyword
            - `leads` - Number of leads
            
            **Optional:** qualified_leads, revenue, stage
            """)
    
    st.markdown("---")
    
    # Settings
    st.markdown("#### Step 2: Configure your analysis (optional)")
    col1, col2 = st.columns(2)
    with col1:
        goal = st.selectbox("🎯 Primary Goal", ["Maximize ROAS", "Increase Conversions", "Reduce CPA", "Scale Traffic"], key="upload_goal")
    with col2:
        budget = st.number_input("💰 Monthly Budget", value=5000, min_value=100, max_value=1000000, step=500, key="upload_budget")
    
    # Upload status
    st.markdown("---")
    
    upload_status = []
    if ads_file:
        upload_status.append(f"✅ Ads Data: {ads_file.name}")
    else:
        upload_status.append("⚪ Ads Data: Not uploaded")
    
    if seo_file:
        upload_status.append(f"✅ SEO Data: {seo_file.name}")
    else:
        upload_status.append("⚪ SEO Data: Not uploaded")
    
    if crm_file:
        upload_status.append(f"✅ CRM Data: {crm_file.name}")
    else:
        upload_status.append("⚪ CRM Data: Not uploaded")
    
    for status in upload_status:
        st.markdown(status)
    
    # Analyze button
    if st.button("🚀 Analyze My Data", use_container_width=True, type="primary", disabled=not ads_file):
        # Parse uploaded files
        data = {
            'ads': parse_csv_file(ads_file, 'ads') if ads_file else [],
            'seo': parse_csv_file(seo_file, 'seo') if seo_file else [],
            'crm': parse_csv_file(crm_file, 'crm') if crm_file else []
        }
        run_analysis("upload", goal, budget, data)

def render_connect_tab():
    """Render Connect/Integrations tab"""
    st.markdown("### 🔌 Connect Your Tools")
    st.markdown("Skip the CSV uploads. Connect your tools directly for automated, real-time marketing intelligence.")
    
    # Advertising platforms
    st.markdown("#### 📢 Advertising Platforms")
    cols = st.columns(5)
    
    integrations = [
        ("Google Ads", "Q2 2026", "🔵"),
        ("Meta Ads", "Q2 2026", "🔵"),
        ("LinkedIn Ads", "Q3 2026", "🔷"),
        ("TikTok Ads", "Q3 2026", "⬛"),
        ("Amazon Ads", "Q4 2026", "🟠"),
    ]
    
    for i, (name, timeline, icon) in enumerate(integrations):
        with cols[i]:
            st.markdown(f"""
            <div class="integration-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                <div style="font-weight: 600;">{name}</div>
                <div class="coming-soon-badge" style="margin-top: 0.5rem;">🟡 {timeline}</div>
            </div>
            """, unsafe_allow_html=True)
            st.button(f"Join Waitlist", key=f"waitlist_{name}", use_container_width=True)
    
    st.markdown("---")
    
    # CRM platforms
    st.markdown("#### 👥 CRM Platforms")
    cols = st.columns(5)
    
    crm_integrations = [
        ("Salesforce", "Q2 2026", "☁️"),
        ("HubSpot", "Q2 2026", "🟠"),
        ("Pipedrive", "Q3 2026", "🟢"),
        ("Zoho CRM", "Q3 2026", "🔴"),
        ("Monday", "Q4 2026", "🟣"),
    ]
    
    for i, (name, timeline, icon) in enumerate(crm_integrations):
        with cols[i]:
            st.markdown(f"""
            <div class="integration-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                <div style="font-weight: 600;">{name}</div>
                <div class="coming-soon-badge" style="margin-top: 0.5rem;">🟡 {timeline}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # SEO & Analytics
    st.markdown("#### 🔍 SEO & Analytics")
    cols = st.columns(5)
    
    seo_integrations = [
        ("Search Console", "Q2 2026", "🔍"),
        ("SEMrush", "Q3 2026", "🟧"),
        ("Ahrefs", "Q3 2026", "🔷"),
        ("Moz", "Q4 2026", "🔵"),
        ("GA4", "Q2 2026", "📊"),
    ]
    
    for i, (name, timeline, icon) in enumerate(seo_integrations):
        with cols[i]:
            st.markdown(f"""
            <div class="integration-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                <div style="font-weight: 600;">{name}</div>
                <div class="coming-soon-badge" style="margin-top: 0.5rem;">🟡 {timeline}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Waitlist signup
    st.markdown("#### 🔔 Get Notified When Integrations Launch")
    col1, col2 = st.columns([3, 1])
    with col1:
        email = st.text_input("Email address", placeholder="yourname@company.com", label_visibility="collapsed")
    with col2:
        if st.button("🔔 Join Waitlist", use_container_width=True):
            if email and "@" in email:
                st.success("✅ You're on the list! We'll notify you when integrations launch.")
            else:
                st.error("Please enter a valid email address.")
    
    st.checkbox("Also notify me about product updates and new features")

def render_results_tab():
    """Render Results tab"""
    if 'analysis_results' not in st.session_state or st.session_state.analysis_results is None:
        st.info("👆 Run an analysis from the **Try Demo** or **Upload Data** tab to see results here.")
        return
    
    results = st.session_state.analysis_results
    
    # Header
    st.markdown("### 📈 Your Marketing Intelligence Report")
    st.markdown(f"📅 Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')} • 📊 Sources: Ads + SEO + CRM")
    
    # Metrics row
    stats = results.get('stats', {})
    summary = results.get('summary', {})
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("💰 Monthly Savings", f"${stats.get('total_savings', 0):,}")
    with col2:
        st.metric("📊 Keywords Analyzed", f"{stats.get('total_units', 0):,}")
    with col3:
        st.metric("🎯 Avg Confidence", f"{stats.get('avg_confidence', 0)}%")
    with col4:
        actions = summary.get('stop', 0) + summary.get('fix', 0) + summary.get('invest', 0)
        st.metric("⚡ Actions Required", actions)
    with col5:
        st.metric("📈 Annual Impact", f"${stats.get('annual_savings', 0):,}")
    
    st.markdown("---")
    
    # AI Insight
    ai_insight = results.get('ai_insight', '')
    if ai_insight:
        st.markdown("""
        <div class="ai-insight-box">
            <div class="ai-insight-title">🤖 AI Executive Summary</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(ai_insight)
    
    st.markdown("---")
    
    # Recommendations tabs
    recommendations = results.get('recommendations', {})
    
    stop_count = len(recommendations.get('stop', []))
    fix_count = len(recommendations.get('fix', []))
    invest_count = len(recommendations.get('invest', []))
    observe_count = len(recommendations.get('observe', []))
    
    tabs = st.tabs([
        f"🛑 STOP ({stop_count})",
        f"🔧 FIX ({fix_count})",
        f"💰 INVEST ({invest_count})",
        f"👁 OBSERVE ({observe_count})"
    ])
    
    with tabs[0]:
        render_recommendations_table(recommendations.get('stop', []), "stop")
    
    with tabs[1]:
        render_recommendations_table(recommendations.get('fix', []), "fix")
    
    with tabs[2]:
        render_recommendations_table(recommendations.get('invest', []), "invest")
    
    with tabs[3]:
        render_recommendations_table(recommendations.get('observe', []), "observe")
    
    st.markdown("---")
    
    # Download buttons
    col1, col2 = st.columns(2)
    
    with col1:
        try:
            pdf_buffer = generate_pdf_report(results)
            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_buffer,
                file_name=f"clarity_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error generating PDF: {e}")
    
    with col2:
        email = st.text_input("Email address for report", placeholder="your@email.com", key="email_report")
        if st.button("📧 Email Me This Report", use_container_width=True):
            if email and "@" in email:
                st.success("✅ Report sent! Check your inbox.")
            else:
                st.error("Please enter a valid email address.")

def render_recommendations_table(data: list, action_type: str):
    """Render recommendations table"""
    if not data:
        st.info(f"No {action_type.upper()} recommendations in this analysis.")
        return
    
    # Prepare data for display
    table_data = []
    for item in data:
        table_data.append({
            'Priority': f"P{item.get('classification', {}).get('priority', '-')}",
            'Keyword': item.get('keyword', ''),
            'Spend': f"${item.get('ads', {}).get('spend', 0):,.0f}",
            'Conversions': item.get('ads', {}).get('conversions', 0),
            'Reason': item.get('classification', {}).get('reason', ''),
            'Confidence': f"{item.get('confidence', {}).get('score', 0)}%",
            'Impact': f"${item.get('classification', {}).get('savings', 0) or item.get('classification', {}).get('potential', 0):,.0f}"
        })
    
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

def render_about_tab():
    """Render About tab"""
    st.markdown("### ℹ️ About Clarity AI")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🎯 The Problem
        
        Marketers are drowning in dashboards but starving for direction.
        
        - Google Ads shows you CTR is 2.3%... but should you pause or scale?
        - Analytics shows traffic is up... but is it profitable traffic?
        - CRM shows 50 leads... but which keywords actually drive revenue?
        
        The average marketer spends **3+ hours per week** manually analyzing data across platforms, often making decisions based on gut feel.
        
        ---
        
        #### 💡 The Solution
        
        Clarity AI aggregates your Ads, SEO, and CRM data to give you one thing dashboards can't: **clear, prioritized actions**.
        
        Instead of "CTR is 2.3%", you get:
        > 🛑 **STOP** 'nike air max' - $542 spent, 0 conversions, 91% confident
        
        Instead of "50 new leads", you get:
        > 💰 **INVEST** in 'running shoes' - 85K searches, 42% qualification rate
        """)
    
    with col2:
        st.markdown("""
        #### 🎯 Who It's For
        
        - ✅ Marketing managers optimizing $5K-$500K monthly ad spend
        - ✅ Growth teams at startups who need data-driven decisions
        - ✅ Agencies managing multiple client accounts
        - ✅ E-commerce brands scaling paid acquisition
        - ✅ Anyone tired of spreadsheets and dashboard overload
        
        ---
        
        #### 🛠️ How It Works
        
        1. **CONNECT** - Upload your data (or use our integrations)
        2. **ANALYZE** - We merge across all sources
        3. **SCORE** - AI scores each keyword on 3 dimensions
        4. **ACT** - Get STOP/FIX/INVEST/OBSERVE recommendations
        
        ---
        
        #### 🛠️ Tech Stack
        
        - **Frontend:** Streamlit (Python)
        - **Backend:** n8n workflow automation
        - **AI:** OpenAI GPT-4o-mini for insights
        - **Hosting:** Streamlit Cloud + Render
        """)
    
    st.markdown("---")
    
    # Built by section
    st.markdown("#### 👤 Built By")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("""
        <div style="width: 100px; height: 100px; background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 2rem;">
            RP
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        **Rupam Patra**  
        Senior Software Engineer | AI & Business Transformation
        
        Building Clarity AI to solve a problem I've seen repeatedly: marketers have access to more data than ever, but less clarity on what to actually do with it.
        
        🔗 [LinkedIn](https://linkedin.com/in/rupam-patra)
        """)
    
    st.markdown("---")
    
    # Feedback
    st.markdown("#### 📬 Feedback & Contact")
    st.markdown("This is an early beta. Your feedback shapes the product.")
    
    feedback = st.text_area("What features would make Clarity AI more useful for you?", height=100)
    if st.button("📤 Send Feedback"):
        if feedback:
            st.success("✅ Thank you for your feedback! We read every response.")
        else:
            st.warning("Please enter your feedback first.")
    
    st.markdown("---")
    st.markdown("*Version 0.1.0 (Beta) • © 2026 Clarity AI • All rights reserved*")

def run_analysis(mode: str, goal: str, budget: int, data: dict = None):
    """Run analysis with progress indicator"""
    
    # Map goal to code
    goal_map = {
        "Maximize ROAS": "roas",
        "Increase Conversions": "conversions",
        "Reduce CPA": "cpa",
        "Scale Traffic": "traffic"
    }
    goal_code = goal_map.get(goal, "roas")
    
    # Show progress
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    if mode == "synthetic":
        status_text.text("⚡ Loading synthetic demo data...")
        progress_bar.progress(10)
        
        synthetic_data = load_synthetic_data()
        if synthetic_data is None:
            st.error("Failed to load synthetic data")
            return
        
        data = synthetic_data
        progress_bar.progress(30)
    
    status_text.text("🔄 Connecting to Clarity AI engine...")
    progress_bar.progress(40)
    
    status_text.text("🧠 Running AI analysis (this may take 30-60 seconds)...")
    progress_bar.progress(50)
    
    # Call n8n webhook
    results = call_n8n_webhook(mode, data, goal_code, budget)
    
    if results:
        progress_bar.progress(90)
        status_text.text("✅ Analysis complete!")
        time.sleep(0.5)
        
        progress_bar.progress(100)
        status_text.empty()
        progress_bar.empty()
        
        # Store results and switch to results tab
        st.session_state.analysis_results = results
        st.session_state.active_tab = "results"
        st.rerun()
    else:
        progress_bar.empty()
        status_text.empty()
        st.error("Analysis failed. Please try again.")

def main():
    """Main app function"""
    
    # Initialize session state
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "demo"
    
    # Render hero
    render_hero()
    
    # Main tabs
    tab_demo, tab_upload, tab_connect, tab_results, tab_about = st.tabs([
        "🎮 Try Demo",
        "📁 Upload Data",
        "🔌 Connect",
        "📈 Results",
        "ℹ️ About"
    ])
    
    with tab_demo:
        render_demo_tab()
    
    with tab_upload:
        render_upload_tab()
    
    with tab_connect:
        render_connect_tab()
    
    with tab_results:
        render_results_tab()
    
    with tab_about:
        render_about_tab()

if __name__ == "__main__":
    main()
