"""
SpendSignal.ai - Marketing Intelligence Platform
Stop wasting. Start knowing.
"""

import streamlit as st
import pandas as pd
import requests
import json
import time
from datetime import datetime
from io import BytesIO
import os

st.set_page_config(
    page_title="SpendSignal.ai - Marketing Intelligence",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===== DARK THEME CSS =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=JetBrains+Mono:wght@400;500&display=swap');

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ── Dark base ── */
    .stApp, .main, .block-container,
    [data-testid="stAppViewContainer"],
    section[data-testid="stSidebar"] {
        background-color: #0b1120 !important;
    }

    .main { padding: 0rem 1rem; }
    .block-container { padding-top: 1.5rem; max-width: 1200px; }
    * { font-family: 'DM Sans', sans-serif !important; }
    code, pre, .stCode { font-family: 'JetBrains Mono', monospace !important; }

    /* ── Global text → light ── */
    .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span,
    .stText, p, span, li, label, h1, h2, h3, h4, h5, h6,
    div[data-testid="stText"],
    [data-testid="stWidgetLabel"] label,
    [data-testid="stWidgetLabel"] p,
    .stRadio label, .stCheckbox label {
        color: #e2e8f0 !important;
    }

    /* ── Expander ── */
    [data-testid="stExpander"] { border-color: #1e293b !important; background: transparent !important; }
    [data-testid="stExpander"] details { border: 1px solid #1e293b !important; border-radius: 8px !important; background: #111827 !important; }
    [data-testid="stExpander"] summary { color: #94a3b8 !important; background: #111827 !important; border-radius: 8px !important; }
    [data-testid="stExpander"] summary span { color: #94a3b8 !important; font-size: 0.85rem !important; }
    [data-testid="stExpander"] summary svg { color: #64748b !important; }
    [data-testid="stExpander"] div[data-testid="stExpanderDetails"] { background: #111827 !important; }
    [data-testid="stExpander"] div[data-testid="stExpanderDetails"] p,
    [data-testid="stExpander"] div[data-testid="stExpanderDetails"] li { color: #94a3b8 !important; font-size: 0.83rem !important; }
    [data-testid="stExpander"] div[data-testid="stExpanderDetails"] code { color: #60a5fa !important; background: rgba(59,130,246,0.1) !important; padding: 1px 5px; border-radius: 3px; }

    /* ── Alert boxes ── */
    .stAlert p { color: inherit !important; }

    /* ── Color tokens ── */
    :root {
        --bg-base: #0b1120;
        --bg-card: #111827;
        --bg-elevated: #1a2332;
        --bg-input: #1e293b;
        --border: #1e293b;
        --border-hover: #334155;
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
        --text-muted: #64748b;
        --brand-500: #3b82f6;
        --brand-400: #60a5fa;
        --brand-300: #93c5fd;
        --brand-200: #bfdbfe;
        --brand-glow: rgba(59,130,246,0.15);
        --accent: #f59e0b;
        --success: #34d399;
        --success-dim: rgba(52,211,153,0.12);
        --danger: #f87171;
        --danger-dim: rgba(248,113,113,0.12);
        --warning: #fbbf24;
        --warning-dim: rgba(251,191,36,0.12);
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
        --shadow-md: 0 4px 16px rgba(0,0,0,0.4);
        --shadow-glow: 0 0 20px rgba(59,130,246,0.08);
    }

    /* ── Navbar ── */
    .spendsignal-nav {
        display: flex; align-items: center; justify-content: space-between;
        padding: 1rem 2rem;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 1px solid #1e293b;
        border-radius: var(--radius-lg);
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-md), var(--shadow-glow);
        position: relative; overflow: hidden;
    }
    .spendsignal-nav::before {
        content: ''; position: absolute; top: -60%; right: -5%;
        width: 350px; height: 350px;
        background: radial-gradient(circle, rgba(59,130,246,0.1) 0%, transparent 70%);
        pointer-events: none;
    }
    .spendsignal-nav .brand { display: flex; align-items: center; gap: 12px; }
    .spendsignal-nav .brand-logo {
        width: 44px; height: 44px;
        filter: drop-shadow(0 2px 10px rgba(59,130,246,0.35));
        flex-shrink: 0;
    }
    .spendsignal-nav .brand-name { font-size: 1.5rem; font-weight: 700; color: #ffffff !important; letter-spacing: -0.5px; }
    .spendsignal-nav .tagline { color: #94a3b8 !important; font-size: 0.85rem; font-weight: 500; }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px; background: var(--bg-card); padding: 5px;
        border-radius: var(--radius-md); border: 1px solid var(--border);
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px; border-radius: var(--radius-sm); font-weight: 600;
        font-size: 0.85rem; color: #64748b !important; background: transparent; border: none;
    }
    .stTabs [data-baseweb="tab"]:hover { color: #cbd5e1 !important; background: rgba(255,255,255,0.03); }
    .stTabs [aria-selected="true"] {
        background: var(--bg-elevated) !important; color: #60a5fa !important;
        box-shadow: var(--shadow-sm); border: 1px solid var(--border) !important;
    }
    .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }

    /* ── Demo cards ── */
    .demo-card {
        background: var(--bg-card); border: 1px solid var(--border);
        border-radius: var(--radius-lg); padding: 2rem; height: 100%;
        transition: all 0.3s ease; overflow: hidden;
    }
    .demo-card:hover { box-shadow: var(--shadow-md); border-color: var(--border-hover); transform: translateY(-2px); }
    .demo-card.quick { border-top: 3px solid var(--brand-500); }
    .demo-card.live { border-top: 3px solid var(--success); }
    .demo-card .card-badge {
        display: inline-flex; align-items: center; gap: 6px; padding: 5px 12px;
        border-radius: 20px; font-size: 0.72rem; font-weight: 600;
        letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 1rem;
    }
    .demo-card.quick .card-badge { background: rgba(59,130,246,0.12); color: #60a5fa !important; }
    .demo-card.live .card-badge { background: var(--success-dim); color: var(--success) !important; }
    .demo-card h3 { font-size: 1.25rem; font-weight: 700; color: #f1f5f9 !important; margin: 0 0 0.5rem 0; }
    .demo-card .card-desc { color: #94a3b8 !important; font-size: 0.9rem; line-height: 1.5; margin-bottom: 1.25rem; }
    .demo-card .specs { display: flex; flex-direction: column; gap: 8px; margin-bottom: 1rem; }
    .demo-card .spec-item { display: flex; align-items: center; gap: 10px; font-size: 0.85rem; color: #cbd5e1 !important; }
    .demo-card .spec-icon {
        width: 28px; height: 28px; border-radius: 8px;
        display: flex; align-items: center; justify-content: center; font-size: 0.75rem; flex-shrink: 0;
    }
    .demo-card.quick .spec-icon { background: rgba(59,130,246,0.1); }
    .demo-card.live .spec-icon { background: var(--success-dim); }
    .demo-card .card-footer {
        font-size: 0.78rem; color: #475569 !important; font-style: italic;
        padding-top: 0.75rem; border-top: 1px solid #1e293b;
    }

    /* ── Section headers ── */
    .section-header { display: flex; align-items: center; gap: 10px; margin-bottom: 0.25rem; }
    .section-header .icon-box {
        width: 36px; height: 36px; border-radius: 10px;
        display: flex; align-items: center; justify-content: center; font-size: 1.1rem; flex-shrink: 0;
    }
    .section-header h2 { font-size: 1.4rem; font-weight: 700; color: #f1f5f9 !important; margin: 0; }
    .section-subtitle { color: #94a3b8 !important; font-size: 0.9rem; margin-bottom: 1.5rem; line-height: 1.5; }

    /* ── AI insight box ── */
    .ai-insight-box-pro {
        background: linear-gradient(135deg, rgba(59,130,246,0.06) 0%, rgba(59,130,246,0.02) 100%);
        border: 1px solid rgba(59,130,246,0.2); border-radius: var(--radius-lg);
        padding: 1.5rem 2rem; margin: 1.5rem 0; position: relative;
    }
    .ai-insight-box-pro::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, #3b82f6, #60a5fa, #fbbf24);
        border-radius: var(--radius-lg) var(--radius-lg) 0 0;
    }
    .ai-insight-box-pro .insight-header {
        display: flex; align-items: center; gap: 8px; font-size: 0.85rem; font-weight: 600;
        color: #60a5fa !important; margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px;
    }

    /* ── Rec headers ── */
    .rec-header {
        display: flex; align-items: center; gap: 10px; padding: 0.75rem 1rem;
        border-radius: var(--radius-sm); margin-bottom: 1rem; font-weight: 600; font-size: 0.85rem;
    }
    .rec-header.stop { background: var(--danger-dim); color: var(--danger) !important; }
    .rec-header.fix { background: var(--warning-dim); color: var(--warning) !important; }
    .rec-header.invest { background: var(--success-dim); color: var(--success) !important; }
    .rec-header.observe { background: rgba(100,116,139,0.1); color: #94a3b8 !important; }

    /* ── Integration cards ── */
    .int-card {
        background: var(--bg-card); border: 1px solid var(--border);
        border-radius: var(--radius-md); padding: 1.5rem 1rem; text-align: center;
        transition: all 0.2s ease;
    }
    .int-card:hover { border-color: var(--border-hover); box-shadow: var(--shadow-sm); }
    .int-card .int-icon { font-size: 2rem; margin-bottom: 0.5rem; }
    .int-card .int-name { font-weight: 600; font-size: 0.9rem; color: #e2e8f0 !important; margin-bottom: 0.5rem; }
    .int-card .int-badge {
        display: inline-block; background: rgba(100,116,139,0.12); color: #64748b !important;
        padding: 3px 10px; border-radius: 20px; font-size: 0.7rem; font-weight: 600;
    }

    /* ── Coming soon ── */
    .coming-soon-banner {
        background: linear-gradient(135deg, rgba(59,130,246,0.08), rgba(59,130,246,0.03));
        border: 1px solid rgba(59,130,246,0.2); border-radius: var(--radius-lg);
        padding: 2rem; text-align: center; margin-bottom: 2rem;
    }
    .coming-soon-banner .cs-icon { font-size: 2.5rem; margin-bottom: 0.75rem; }
    .coming-soon-banner h3 { font-size: 1.3rem; font-weight: 700; color: #e2e8f0 !important; margin: 0 0 0.5rem 0; }
    .coming-soon-banner p { color: #94a3b8 !important; font-size: 0.9rem; max-width: 500px; margin: 0 auto; line-height: 1.5; }

    /* ── Upload headers ── */
    .upload-header { display: flex; align-items: center; gap: 6px; font-weight: 600; font-size: 0.9rem; color: #e2e8f0 !important; margin-bottom: 0.25rem; }
    .upload-header .req-badge { font-size: 0.65rem; background: var(--danger-dim); color: var(--danger) !important; padding: 2px 8px; border-radius: 4px; font-weight: 600; text-transform: uppercase; }
    .upload-header .opt-badge { font-size: 0.65rem; background: rgba(100,116,139,0.12); color: #64748b !important; padding: 2px 8px; border-radius: 4px; font-weight: 600; text-transform: uppercase; }
    .upload-source { font-size: 0.8rem; color: #64748b !important; margin-bottom: 0.75rem; }

    /* ── Info box ── */
    .info-box {
        display: flex; align-items: center; gap: 10px;
        background: rgba(59,130,246,0.06); border: 1px solid rgba(59,130,246,0.15);
        border-radius: var(--radius-sm); padding: 0.75rem 1rem;
        font-size: 0.85rem; color: #93c5fd !important; margin-bottom: 1.5rem;
    }

    /* ── About cards ── */
    .about-card {
        background: var(--bg-card); border: 1px solid var(--border);
        border-radius: var(--radius-lg); padding: 2rem; height: 100%;
    }
    .about-card h4 { font-size: 1.1rem; font-weight: 700; color: #f1f5f9 !important; margin: 0 0 1rem 0; }
    .about-card p, .about-card li { color: #94a3b8 !important; font-size: 0.9rem; line-height: 1.7; }
    .about-card strong { color: #cbd5e1 !important; }
    .about-card hr { border-color: #1e293b !important; }

    /* ── Author card ── */
    .author-card {
        background: linear-gradient(135deg, #0f172a, #1a2332);
        border: 1px solid var(--border); border-radius: var(--radius-lg);
        padding: 2rem; display: flex; align-items: center; gap: 1.5rem;
    }
    .author-card .avatar {
        width: 72px; height: 72px;
        background: linear-gradient(135deg, #3b82f6, #60a5fa);
        border-radius: 16px; display: flex; align-items: center; justify-content: center;
        font-size: 1.5rem; font-weight: 700; color: white !important;
        flex-shrink: 0; box-shadow: 0 4px 16px rgba(59,130,246,0.3);
    }
    .author-card .author-info h4 { color: #f1f5f9 !important; font-size: 1.1rem; margin: 0 0 4px 0; }
    .author-card .author-info p { color: #94a3b8 !important; font-size: 0.85rem; margin: 0; line-height: 1.5; }
    .author-card .author-info a { color: #60a5fa !important; text-decoration: underline; }

    /* ── Buttons ── */
    .stButton>button {
        border-radius: var(--radius-sm); font-weight: 600; padding: 0.6rem 1.5rem;
        font-size: 0.85rem; border: 1px solid var(--border); transition: all 0.2s ease;
        color: #e2e8f0 !important; background: var(--bg-elevated);
    }
    .stButton>button:hover { box-shadow: var(--shadow-md); transform: translateY(-1px); border-color: var(--border-hover); background: #243044; }
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #2563eb, #3b82f6) !important;
        color: white !important; border: none !important;
        box-shadow: 0 2px 12px rgba(59,130,246,0.3);
    }
    .stButton>button[kind="primary"]:hover { box-shadow: 0 4px 20px rgba(59,130,246,0.4); }

    /* ── Pills ── */
    .status-pill { display: inline-flex; align-items: center; gap: 6px; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 500; }
    .status-pill.ok { background: var(--success-dim); color: var(--success) !important; }
    .status-pill.pending { background: rgba(100,116,139,0.1); color: #64748b !important; }

    /* ── Misc ── */
    .divider { border: none; border-top: 1px solid #1e293b; margin: 1.5rem 0; }
    .settings-label { font-size: 0.75rem; font-weight: 600; color: #64748b !important; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem; }
    .app-footer { text-align: center; padding: 2rem 0 1rem; color: #475569 !important; font-size: 0.78rem; border-top: 1px solid #1e293b; margin-top: 2rem; }

    /* ── Streamlit widget overrides for dark ── */
    .stSelectbox label, .stNumberInput label, .stTextInput label, .stTextArea label {
        font-size: 0.85rem !important; font-weight: 600 !important; color: #cbd5e1 !important;
    }
    .stDataFrame { border-radius: var(--radius-md); overflow: hidden; }

    div[data-testid="stMetric"] {
        background: var(--bg-card) !important; border: 1px solid var(--border);
        border-radius: var(--radius-md); padding: 1rem; box-shadow: var(--shadow-sm);
    }
    div[data-testid="stMetric"] label { font-size: 0.75rem !important; text-transform: uppercase; letter-spacing: 0.3px; color: #64748b !important; }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] { color: #f1f5f9 !important; }
    .stDownloadButton>button { width: 100%; }

    /* Inputs */
    [data-baseweb="select"] > div { background-color: var(--bg-input) !important; border-color: var(--border) !important; color: #e2e8f0 !important; }
    [data-baseweb="input"] { background-color: var(--bg-input) !important; border-color: var(--border) !important; }
    [data-baseweb="input"] input { color: #e2e8f0 !important; }
    [data-baseweb="textarea"] textarea { background-color: var(--bg-input) !important; color: #e2e8f0 !important; border-color: var(--border) !important; }

    /* File uploader — compact layout for narrow columns */
    [data-testid="stFileUploader"] section,
    [data-testid="stFileUploaderDropzone"] {
        background-color: var(--bg-card) !important;
        border: 1px dashed var(--border) !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.5rem !important;
        min-height: auto !important;
        position: relative !important;
    }
    /* Hide every child of the dropzone, then un-hide the button */
    [data-testid="stFileUploader"] section > *,
    [data-testid="stFileUploaderDropzone"] > *,
    [data-testid="stFileUploaderDropzoneInstructions"] {
        display: none !important;
    }
    [data-testid="stFileUploader"] section > button,
    [data-testid="stFileUploaderDropzone"] > button,
    [data-testid="stFileUploader"] section [data-testid="stBaseButton-secondary"],
    [data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"] {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
        margin: 0 !important;
        color: #e2e8f0 !important;
        background: var(--bg-elevated) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        padding: 0.55rem 0.75rem !important;
        cursor: pointer !important;
    }
    /* Replace the default "Browse files" text with a clean "Choose file" label */
    [data-testid="stFileUploader"] section button > *,
    [data-testid="stFileUploaderDropzone"] button > * {
        display: none !important;
    }
    [data-testid="stFileUploader"] section button::before,
    [data-testid="stFileUploaderDropzone"] button::before {
        content: "📎 Choose file";
    }
    /* Show the file list after upload */
    [data-testid="stFileUploader"] [data-testid="stFileUploaderFile"],
    [data-testid="stFileUploader"] [data-testid="stFileUploaderFileData"] {
        display: flex !important;
    }
    [data-testid="stFileUploader"] [data-testid="stFileUploaderFileName"] {
        color: #e2e8f0 !important;
        font-size: 0.8rem !important;
    }

    /* Dataframe */
    .stDataFrame [data-testid="stDataFrameResizable"] { background: var(--bg-card) !important; }

    /* Empty state */
    .empty-state {
        text-align: center; padding: 4rem 2rem;
    }
    .empty-state .es-icon { font-size: 3rem; margin-bottom: 1rem; opacity: 0.6; }
    .empty-state h3 { color: #cbd5e1 !important; margin-bottom: 0.5rem; }
    .empty-state p { color: #64748b !important; font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)

# ===== DATA & API FUNCTIONS =====

@st.cache_data
def load_synthetic_data():
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

def call_n8n_webhook(mode, data=None, goal="roas", budget=10000):
    webhook_url = st.secrets.get("N8N_WEBHOOK_URL", "")
    if not webhook_url:
        st.error("N8N_WEBHOOK_URL not configured. Please add it to your Streamlit secrets.")
        return None
    payload = {"mode": mode, "goal": goal, "budget": budget, "data": data if data else {}}
    try:
        response = requests.post(webhook_url, json=payload, headers={"Content-Type": "application/json"}, timeout=120)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        st.error("Analysis timed out. Please try again.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to analysis engine: {str(e)}")
        return None

def generate_pdf_report(results):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.units import inch

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#1e3a5f'), spaceAfter=20)
    heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#1e3a5f'), spaceBefore=20, spaceAfter=10)

    story = []
    story.append(Paragraph("SPENDSIGNAL.AI", title_style))
    story.append(Paragraph("Marketing Intelligence Report", styles['Heading2']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", styles['Normal']))
    story.append(Spacer(1, 20))
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

    ai_insight = results.get('ai_insight', '')
    if ai_insight:
        story.append(Paragraph("AI INSIGHT", heading_style))
        story.append(Paragraph(ai_insight, styles['Normal']))
        story.append(Spacer(1, 20))

    recommendations = results.get('recommendations', {})
    for action, data_list in [
        ('STOP - PAUSE IMMEDIATELY', recommendations.get('stop', [])),
        ('FIX - OPTIMIZE THESE', recommendations.get('fix', [])),
        ('INVEST - SCALE UP', recommendations.get('invest', [])),
    ]:
        if data_list:
            story.append(Paragraph(action, heading_style))
            table_data = [['Keyword', 'Spend', 'Reason', 'Confidence']]
            for item in data_list[:10]:
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

    story.append(Spacer(1, 30))
    story.append(Paragraph("Generated by SpendSignal.ai | spendsignal.ai | Built by Rupam Patra",
                          ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.gray)))
    doc.build(story)
    buffer.seek(0)
    return buffer

def parse_csv_file(uploaded_file, data_type):
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.lower().str.strip()
        column_maps = {
            'ads': {'keyword': ['keyword','keywords','search_term','query'], 'spend': ['spend','cost','amount','ad_spend'], 'clicks': ['clicks','click'], 'impressions': ['impressions','impr'], 'conversions': ['conversions','conv','conversion'], 'revenue': ['revenue','value','sale_amount']},
            'seo': {'keyword': ['keyword','keywords','text','query'], 'volume': ['volume','vol','search_volume','searches'], 'cpc': ['cpc','cost_per_click'], 'competition': ['competition','comp','difficulty']},
            'crm': {'origin': ['origin','source','keyword','utm_source'], 'leads': ['leads','lead_count'], 'qualified_leads': ['qualified_leads','qualified','sql'], 'revenue': ['revenue','value','deal_value']}
        }
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

# ===== RENDER FUNCTIONS =====

def render_hero():
    st.markdown("""
    <div class="spendsignal-nav">
        <div class="brand">
            <svg class="brand-logo" width="48" height="48" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" aria-label="Spendsignal.ai">
                <defs>
                    <linearGradient id="ssBladeLight" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#93c5fd"/>
                        <stop offset="100%" stop-color="#3b82f6"/>
                    </linearGradient>
                    <linearGradient id="ssBladeDark" x1="100%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" stop-color="#2563eb"/>
                        <stop offset="100%" stop-color="#1e40af"/>
                    </linearGradient>
                </defs>
                <g transform="translate(50 50)">
                    <path d="M 0 -38 C 22 -38, 34 -22, 30 -4 C 22 -14, 10 -18, 0 -16 Z"
                          fill="url(#ssBladeDark)" transform="rotate(0)"/>
                    <path d="M 0 -38 C 22 -38, 34 -22, 30 -4 C 22 -14, 10 -18, 0 -16 Z"
                          fill="url(#ssBladeLight)" transform="rotate(90)"/>
                    <path d="M 0 -38 C 22 -38, 34 -22, 30 -4 C 22 -14, 10 -18, 0 -16 Z"
                          fill="url(#ssBladeDark)" transform="rotate(180)"/>
                    <path d="M 0 -38 C 22 -38, 34 -22, 30 -4 C 22 -14, 10 -18, 0 -16 Z"
                          fill="url(#ssBladeLight)" transform="rotate(270)"/>
                </g>
            </svg>
            <span class="brand-name">Spendsignal.ai</span>
        </div>
        <span class="tagline">AI-powered marketing intelligence — Know what to STOP, FIX, INVEST, or OBSERVE.</span>
    </div>
    """, unsafe_allow_html=True)

def render_demo_tab():
    st.markdown("""
    <div class="section-header">
        <div class="icon-box" style="background: rgba(59,130,246,0.1);">🎮</div>
        <h2>Try SpendSignal.ai with Demo Data</h2>
    </div>
    <p class="section-subtitle">Experience the full power of SpendSignal.ai. No signup required — pick a demo mode and see AI-powered recommendations in action.</p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="demo-card quick">
            <div class="card-badge">⚡ QUICK DEMO</div>
            <h3>Pre-built Sample Data</h3>
            <p class="card-desc">Pre-built marketing data processed through our full AI analysis engine. Best for a fast first look.</p>
            <div class="specs">
                <div class="spec-item"><div class="spec-icon">⏱</div><span>~15–20 seconds to complete</span></div>
                <div class="spec-item"><div class="spec-icon">📢</div><span>150 ad keywords analyzed</span></div>
                <div class="spec-item"><div class="spec-icon">🔍</div><span>200 SEO keywords mapped</span></div>
                <div class="spec-item"><div class="spec-icon">👥</div><span>100 CRM lead records</span></div>
            </div>
            <div class="card-footer">Same AI engine as production — just faster with sample data.</div>
        </div>
        """, unsafe_allow_html=True)
        quick_demo = st.button("⚡ Run Quick Demo", key="quick_demo", use_container_width=True)

    with col2:
        st.markdown("""
        <div class="demo-card live">
            <div class="card-badge">🌐 LIVE DEMO</div>
            <h3>Real-time External Data</h3>
            <p class="card-desc">Real-time data pulled from Kaggle public datasets. Demonstrates actual external data integration capabilities.</p>
            <div class="specs">
                <div class="spec-item"><div class="spec-icon">⏱</div><span>~45–60 seconds to complete</span></div>
                <div class="spec-item"><div class="spec-icon">📢</div><span>Google Ads dataset</span></div>
                <div class="spec-item"><div class="spec-icon">🔍</div><span>SEO keyword research data</span></div>
                <div class="spec-item"><div class="spec-icon">👥</div><span>Marketing funnel records</span></div>
            </div>
            <div class="card-footer">Demonstrates real external data integration pipeline.</div>
        </div>
        """, unsafe_allow_html=True)
        live_demo = st.button("🌐 Run Live Demo", key="live_demo", use_container_width=True)

    if quick_demo:
        run_analysis("synthetic", "Maximize ROAS", 10000)
    elif live_demo:
        run_analysis("kaggle", "Maximize ROAS", 10000)

def render_upload_tab():
    st.markdown("""
    <div class="section-header">
        <div class="icon-box" style="background: rgba(251,191,36,0.1);">📁</div>
        <h2>Upload Your Marketing Data</h2>
    </div>
    <p class="section-subtitle">Upload your data to get personalized AI recommendations. The more data sources you connect, the smarter the analysis.</p>
    """, unsafe_allow_html=True)

    st.markdown('<div class="info-box">🔒 <strong>Your data is secure.</strong> We don\'t store your data — it\'s processed in real-time and immediately deleted.</div>', unsafe_allow_html=True)
    st.markdown('<div class="settings-label">Upload at least one data source</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="upload-header">📢 Advertising Data <span class="req-badge">Required</span></div><div class="upload-source">Google Ads, Meta Ads, or any ad platform export</div>', unsafe_allow_html=True)
        ads_file = st.file_uploader("Upload Ads CSV", type=['csv'], key="ads_upload", label_visibility="collapsed")
        st.markdown("""
        <details style="background:#111827; border:1px solid #1e293b; border-radius:8px; padding:0; margin-top:4px;">
            <summary style="padding:10px 14px; cursor:pointer; color:#94a3b8; font-size:0.83rem; font-weight:500; list-style:none; display:flex; align-items:center; gap:6px;">
                <span style="font-size:0.75rem;">▸</span> Required columns
            </summary>
            <div style="padding:4px 14px 12px; color:#64748b; font-size:0.82rem; line-height:1.7;">
                <code style="color:#60a5fa; background:rgba(59,130,246,0.1); padding:1px 5px; border-radius:3px;">keyword</code> — Search term or ad group<br>
                <code style="color:#60a5fa; background:rgba(59,130,246,0.1); padding:1px 5px; border-radius:3px;">spend</code> — Total cost<br>
                <code style="color:#60a5fa; background:rgba(59,130,246,0.1); padding:1px 5px; border-radius:3px;">clicks</code> — Number of clicks<br>
                <code style="color:#60a5fa; background:rgba(59,130,246,0.1); padding:1px 5px; border-radius:3px;">conversions</code> — Number of conversions<br>
                <span style="color:#475569; font-style:italic;">Optional: impressions, campaign, revenue</span>
            </div>
        </details>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="upload-header">🔍 SEO Data <span class="opt-badge">Optional</span></div><div class="upload-source">SEMrush, Ahrefs, or Search Console</div>', unsafe_allow_html=True)
        seo_file = st.file_uploader("Upload SEO CSV", type=['csv'], key="seo_upload", label_visibility="collapsed")
        st.markdown("""
        <details style="background:#111827; border:1px solid #1e293b; border-radius:8px; padding:0; margin-top:4px;">
            <summary style="padding:10px 14px; cursor:pointer; color:#94a3b8; font-size:0.83rem; font-weight:500; list-style:none; display:flex; align-items:center; gap:6px;">
                <span style="font-size:0.75rem;">▸</span> Required columns
            </summary>
            <div style="padding:4px 14px 12px; color:#64748b; font-size:0.82rem; line-height:1.7;">
                <code style="color:#60a5fa; background:rgba(59,130,246,0.1); padding:1px 5px; border-radius:3px;">keyword</code> — Search term<br>
                <code style="color:#60a5fa; background:rgba(59,130,246,0.1); padding:1px 5px; border-radius:3px;">volume</code> — Monthly search volume<br>
                <span style="color:#475569; font-style:italic;">Optional: cpc, competition, score</span>
            </div>
        </details>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="upload-header">👥 CRM Data <span class="opt-badge">Optional</span></div><div class="upload-source">Salesforce, HubSpot, or your CRM</div>', unsafe_allow_html=True)
        crm_file = st.file_uploader("Upload CRM CSV", type=['csv'], key="crm_upload", label_visibility="collapsed")
        st.markdown("""
        <details style="background:#111827; border:1px solid #1e293b; border-radius:8px; padding:0; margin-top:4px;">
            <summary style="padding:10px 14px; cursor:pointer; color:#94a3b8; font-size:0.83rem; font-weight:500; list-style:none; display:flex; align-items:center; gap:6px;">
                <span style="font-size:0.75rem;">▸</span> Required columns
            </summary>
            <div style="padding:4px 14px 12px; color:#64748b; font-size:0.82rem; line-height:1.7;">
                <code style="color:#60a5fa; background:rgba(59,130,246,0.1); padding:1px 5px; border-radius:3px;">origin</code> or <code style="color:#60a5fa; background:rgba(59,130,246,0.1); padding:1px 5px; border-radius:3px;">source</code> — Lead source/keyword<br>
                <code style="color:#60a5fa; background:rgba(59,130,246,0.1); padding:1px 5px; border-radius:3px;">leads</code> — Number of leads<br>
                <span style="color:#475569; font-style:italic;">Optional: qualified_leads, revenue, stage</span>
            </div>
        </details>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    status_items = []
    if ads_file:
        status_items.append(f'<span class="status-pill ok">✅ Ads: {ads_file.name}</span>')
    else:
        status_items.append('<span class="status-pill pending">○ Ads: Not uploaded</span>')
    if seo_file:
        status_items.append(f'<span class="status-pill ok">✅ SEO: {seo_file.name}</span>')
    else:
        status_items.append('<span class="status-pill pending">○ SEO: Not uploaded</span>')
    if crm_file:
        status_items.append(f'<span class="status-pill ok">✅ CRM: {crm_file.name}</span>')
    else:
        status_items.append('<span class="status-pill pending">○ CRM: Not uploaded</span>')
    st.markdown(' &nbsp; '.join(status_items), unsafe_allow_html=True)
    st.markdown("")

    if st.button("🚀 Analyze My Data", use_container_width=True, type="primary", disabled=not ads_file):
        data = {
            'ads': parse_csv_file(ads_file, 'ads') if ads_file else [],
            'seo': parse_csv_file(seo_file, 'seo') if seo_file else [],
            'crm': parse_csv_file(crm_file, 'crm') if crm_file else []
        }
        run_analysis("upload", "Maximize ROAS", 5000, data)

def render_connect_tab():
    st.markdown("""
    <div class="section-header">
        <div class="icon-box" style="background: rgba(59,130,246,0.1);">🔌</div>
        <h2>Connect Your Tools</h2>
    </div>
    <p class="section-subtitle">Skip CSV uploads — connect your marketing tools directly for automated, real-time intelligence.</p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="coming-soon-banner">
        <div class="cs-icon">🚀</div>
        <h3>Integrations Coming Soon</h3>
        <p>We're building direct connections to the tools you already use. In the meantime, use the <strong>Upload Data</strong> tab to analyze your exported CSVs.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="settings-label">📢 Advertising Platforms</div>', unsafe_allow_html=True)
    cols = st.columns(5)
    for i, (name, timeline, icon) in enumerate([("Google Ads","Q2 2026","🔵"),("Meta Ads","Q2 2026","🔵"),("LinkedIn Ads","Q3 2026","🔷"),("TikTok Ads","Q3 2026","⬛"),("Amazon Ads","Q4 2026","🟠")]):
        with cols[i]:
            st.markdown(f'<div class="int-card"><div class="int-icon">{icon}</div><div class="int-name">{name}</div><div class="int-badge">🗓 {timeline}</div></div>', unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="settings-label">👥 CRM Platforms</div>', unsafe_allow_html=True)
    cols = st.columns(5)
    for i, (name, timeline, icon) in enumerate([("Salesforce","Q2 2026","☁️"),("HubSpot","Q2 2026","🟠"),("Pipedrive","Q3 2026","🟢"),("Zoho CRM","Q3 2026","🔴"),("Monday","Q4 2026","🟣")]):
        with cols[i]:
            st.markdown(f'<div class="int-card"><div class="int-icon">{icon}</div><div class="int-name">{name}</div><div class="int-badge">🗓 {timeline}</div></div>', unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="settings-label">🔍 SEO & Analytics</div>', unsafe_allow_html=True)
    cols = st.columns(5)
    for i, (name, timeline, icon) in enumerate([("Search Console","Q2 2026","🔍"),("SEMrush","Q3 2026","🟧"),("Ahrefs","Q3 2026","🔷"),("Moz","Q4 2026","🔵"),("GA4","Q2 2026","📊")]):
        with cols[i]:
            st.markdown(f'<div class="int-card"><div class="int-icon">{icon}</div><div class="int-name">{name}</div><div class="int-badge">🗓 {timeline}</div></div>', unsafe_allow_html=True)

def render_results_tab():
    if 'analysis_results' not in st.session_state or st.session_state.analysis_results is None:
        st.markdown("""
        <div class="empty-state">
            <div class="es-icon">📈</div>
            <h3>No Results Yet</h3>
            <p>Run an analysis from the <strong>Try Demo</strong> or <strong>Upload Data</strong> tab to see your marketing intelligence report here.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    results = st.session_state.analysis_results

    st.markdown("""
    <div class="section-header">
        <div class="icon-box" style="background: rgba(52,211,153,0.1);">📈</div>
        <h2>Marketing Intelligence Report</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"📅 Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')} &nbsp;·&nbsp; 📊 Sources: Ads + SEO + CRM")
    st.markdown("")

    stats = results.get('stats', {})
    summary = results.get('summary', {})

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: st.metric("💰 Monthly Savings", f"${stats.get('total_savings', 0):,}")
    with col2: st.metric("📊 Keywords Analyzed", f"{stats.get('total_units', 0):,}")
    with col3: st.metric("🎯 Avg Confidence", f"{stats.get('avg_confidence', 0)}%")
    with col4:
        actions = summary.get('stop', 0) + summary.get('fix', 0) + summary.get('invest', 0)
        st.metric("⚡ Actions Required", actions)
    with col5: st.metric("📈 Annual Impact", f"${stats.get('annual_savings', 0):,}")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    ai_insight = results.get('ai_insight', '')
    if ai_insight:
        st.markdown('<div class="ai-insight-box-pro"><div class="insight-header">🤖 AI Executive Summary</div></div>', unsafe_allow_html=True)
        st.markdown(ai_insight)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    recommendations = results.get('recommendations', {})
    stop_count = len(recommendations.get('stop', []))
    fix_count = len(recommendations.get('fix', []))
    invest_count = len(recommendations.get('invest', []))
    observe_count = len(recommendations.get('observe', []))

    tabs = st.tabs([f"🛑 STOP ({stop_count})", f"🔧 FIX ({fix_count})", f"💰 INVEST ({invest_count})", f"👁 OBSERVE ({observe_count})"])
    with tabs[0]:
        st.markdown('<div class="rec-header stop">🛑 Pause these immediately — burning budget with no return.</div>', unsafe_allow_html=True)
        render_recommendations_table(recommendations.get('stop', []), "stop")
    with tabs[1]:
        st.markdown('<div class="rec-header fix">🔧 These have potential but need optimization to perform.</div>', unsafe_allow_html=True)
        render_recommendations_table(recommendations.get('fix', []), "fix")
    with tabs[2]:
        st.markdown('<div class="rec-header invest">💰 Scale these up — they\'re your top performers.</div>', unsafe_allow_html=True)
        render_recommendations_table(recommendations.get('invest', []), "invest")
    with tabs[3]:
        st.markdown('<div class="rec-header observe">👁 Keep monitoring — not enough data for a confident call yet.</div>', unsafe_allow_html=True)
        render_recommendations_table(recommendations.get('observe', []), "observe")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    try:
        pdf_buffer = generate_pdf_report(results)
        st.download_button(label="📥 Download Full PDF Report", data=pdf_buffer, file_name=f"spendsignal_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf", mime="application/pdf", use_container_width=True)
    except Exception as e:
        st.error(f"Error generating PDF: {e}")

def render_recommendations_table(data, action_type):
    if not data:
        st.info(f"No {action_type.upper()} recommendations in this analysis.")
        return
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
    st.markdown('<div class="section-header"><div class="icon-box" style="background: rgba(59,130,246,0.1);">ℹ️</div><h2>About SpendSignal.ai</h2></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="about-card">
            <h4>🎯 The Problem</h4>
            <p>Marketers are drowning in dashboards but starving for direction.</p>
            <p>Google Ads shows CTR is 2.3%… but should you pause or scale? Analytics shows traffic is up… but is it profitable? CRM shows 50 leads… but which keywords drive revenue?</p>
            <p>The average marketer spends <strong>3+ hours/week</strong> manually analyzing data across platforms, often deciding on gut feel.</p>
            <hr>
            <h4>💡 The Solution</h4>
            <p>SpendSignal.ai aggregates your Ads, SEO, and CRM data to deliver one thing dashboards can't: <strong>clear, prioritized actions.</strong></p>
            <p>Instead of "CTR is 2.3%", you get:<br><span style="color:#f87171; font-weight:600;">🛑 STOP</span> <span style="color:#cbd5e1;">'nike air max' — $542 spent, 0 conversions, 91% confident</span></p>
            <p>Instead of "50 new leads", you get:<br><span style="color:#34d399; font-weight:600;">💰 INVEST</span> <span style="color:#cbd5e1;">in 'running shoes' — 85K searches, 42% qualification rate</span></p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="about-card">
            <h4>🎯 Who It's For</h4>
            <ul>
                <li>Marketing managers optimizing $5K–$500K monthly ad spend</li>
                <li>Growth teams at startups who need data-driven decisions</li>
                <li>Agencies managing multiple client accounts</li>
                <li>E-commerce brands scaling paid acquisition</li>
                <li>Anyone tired of spreadsheets and dashboard overload</li>
            </ul>
            <hr>
            <h4>🛠️ How It Works</h4>
            <ol>
                <li><strong>CONNECT</strong> — Upload your data (or use integrations)</li>
                <li><strong>ANALYZE</strong> — We merge across all sources</li>
                <li><strong>SCORE</strong> — AI scores each keyword on 3 dimensions</li>
                <li><strong>ACT</strong> — Get STOP / FIX / INVEST / OBSERVE actions</li>
            </ol>
            <hr>
            <h4>🛠️ Tech Stack</h4>
            <p><strong>Frontend:</strong> Streamlit (Python)<br><strong>Backend:</strong> n8n workflow automation<br><strong>AI:</strong> OpenAI GPT-4o-mini for insights<br><strong>Hosting:</strong> Streamlit Cloud + Render</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("""
    <div class="author-card">
        <div class="avatar">RP</div>
        <div class="author-info">
            <h4>Rupam Patra</h4>
            <p>Senior Software Engineer · AI & Business Transformation</p>
            <p style="margin-top: 6px;">Building SpendSignal.ai to solve a problem I've seen repeatedly: marketers have access to more data than ever, but less clarity on what to actually do with it.</p>
            <p style="margin-top: 8px;"><a href="https://linkedin.com/in/rupam-patra" target="_blank">🔗 LinkedIn</a></p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown('<div class="settings-label">📬 Feedback & Contact</div>', unsafe_allow_html=True)
    st.markdown("Your feedback shapes the product.")
    feedback = st.text_area("What features would make Spendsignal.ai more useful for you?", height=100)
    if st.button("📤 Send Feedback"):
        if feedback:
            st.success("✅ Thank you for your feedback! We read every response.")
        else:
            st.warning("Please enter your feedback first.")

    st.markdown('<div class="app-footer">Version 0.1.0 · © 2026 Spendsignal.ai · All rights reserved</div>', unsafe_allow_html=True)

def run_analysis(mode, goal, budget, data=None):
    goal_map = {"Maximize ROAS": "roas", "Increase Conversions": "conversions", "Reduce CPA": "cpa", "Scale Traffic": "traffic"}
    goal_code = goal_map.get(goal, "roas")

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

    status_text.text("🔄 Connecting to SpendSignal.ai engine...")
    progress_bar.progress(40)
    status_text.text("🧠 Running AI analysis (this may take 30-60 seconds)...")
    progress_bar.progress(50)

    results = call_n8n_webhook(mode, data, goal_code, budget)

    if results:
        progress_bar.progress(90)
        status_text.text("✅ Analysis complete!")
        time.sleep(0.5)
        progress_bar.progress(100)
        status_text.empty()
        progress_bar.empty()
        st.session_state.analysis_results = results
        st.session_state.active_tab = "results"
        st.session_state.show_results_inline = True
        st.rerun()
    else:
        progress_bar.empty()
        status_text.empty()
        st.error("Analysis failed. Please try again.")

# ===== MAIN =====

def main():
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "demo"
    if 'show_results_inline' not in st.session_state:
        st.session_state.show_results_inline = False

    render_hero()

    # If we just completed an analysis, show results directly
    if st.session_state.show_results_inline and st.session_state.analysis_results:
        st.session_state.show_results_inline = False
        render_results_tab()
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        if st.button("← Back to All Tabs", use_container_width=False):
            st.session_state.analysis_results = None
            st.rerun()
        return

    tab_demo, tab_upload, tab_connect, tab_results, tab_about = st.tabs([
        "🎮 Try Demo", "📁 Upload Data", "🔌 Connect", "📈 Results", "ℹ️ About"
    ])

    with tab_demo: render_demo_tab()
    with tab_upload: render_upload_tab()
    with tab_connect: render_connect_tab()
    with tab_results: render_results_tab()
    with tab_about: render_about_tab()

if __name__ == "__main__":
    main()
