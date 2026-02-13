"""
Clarity AI - Marketing Intelligence Platform
Stop guessing. Start knowing.
Professional UI v2.1
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

# Professional CSS
st.markdown("""
<style>
    /* Hide Streamlit defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hero Section */
    .hero-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0ea5e9 100%);
        padding: 3rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        opacity: 0.5;
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
    }
    
    .hero-badge {
        display: inline-block;
        background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
        color: white;
        padding: 0.35rem 1rem;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 1rem;
    }
    
    .hero-title {
        font-size: 2.75rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: rgba(255,255,255,0.9);
        margin-bottom: 1rem;
        font-weight: 500;
    }
    
    .hero-description {
        font-size: 1rem;
        color: rgba(255,255,255,0.7);
        max-width: 600px;
        line-height: 1.6;
    }
    
    /* Cards */
    .demo-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
        border: 1px solid #e2e8f0;
        height: 100%;
        transition: all 0.3s ease;
    }
    
    .demo-card:hover {
        box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04);
        transform: translateY(-2px);
    }
    
    .demo-card-quick {
        border-top: 4px solid #8b5cf6;
    }
    
    .demo-card-live {
        border-top: 4px solid #10b981;
    }
    
    .demo-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .demo-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.75rem;
    }
    
    .demo-description {
        color: #64748b;
        font-size: 0.95rem;
        margin-bottom: 1rem;
        line-height: 1.5;
    }
    
    .demo-features {
        list-style: none;
        padding: 0;
        margin: 0 0 1.5rem 0;
    }
    
    .demo-features li {
        padding: 0.4rem 0;
        color: #475569;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
    }
    
    .demo-features li::before {
        content: '✓';
        color: #10b981;
        font-weight: bold;
        margin-right: 0.75rem;
    }
    
    /* Stats Cards */
    .stat-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.25rem;
    }
    
    .stat-label {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 500;
    }
    
    /* AI Insight */
    .ai-insight {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 1px solid #bae6fd;
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin: 1.5rem 0;
    }
    
    .ai-insight-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .ai-insight-icon {
        font-size: 1.5rem;
        margin-right: 0.75rem;
    }
    
    .ai-insight-title {
        font-size: 1rem;
        font-weight: 600;
        color: #0369a1;
    }
    
    .ai-insight-text {
        color: #0c4a6e;
        line-height: 1.7;
        font-size: 0.95rem;
    }
    
    /* Integration Cards */
    .integration-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        transition: all 0.2s ease;
    }
    
    .integration-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .integration-icon {
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
    }
    
    .integration-name {
        font-weight: 600;
        color: #0f172a;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
    }
    
    .coming-soon-badge {
        display: inline-block;
        background: #fef3c7;
        color: #92400e;
        padding: 0.3rem 0.75rem;
        border-radius: 50px;
        font-size: 0.7rem;
        font-weight: 600;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: #f8fafc;
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.75rem 2rem;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.5rem;
    }
    
    .section-subheader {
        color: #64748b;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    
    /* Info boxes */
    .info-box {
        background: #f0f9ff;
        border: 1px solid #bae6fd;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        display: flex;
        align-items: center;
    }
    
    .info-box-icon {
        font-size: 1.25rem;
        margin-right: 0.75rem;
    }
    
    .info-box-text {
        color: #0369a1;
        font-size: 0.9rem;
    }
    
    /* Hide streamlit elements */
    div[data-testid="stDecoration"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Load synthetic data
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
        st.error(f"Error loading data: {e}")
        return None

def call_n8n_webhook(mode, data=None, goal="roas", budget=10000):
    webhook_url = st.secrets.get("N8N_WEBHOOK_URL", "")
    if not webhook_url:
        st.error("⚠️ Webhook URL not configured. Add N8N_WEBHOOK_URL to Streamlit secrets.")
        return None
    
    payload = {"mode": mode, "goal": goal, "budget": budget, "data": data or {}}
    
    try:
        response = requests.post(webhook_url, json=payload, headers={"Content-Type": "application/json"}, timeout=120)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. The analysis is taking longer than expected. Please try again.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Connection error: {str(e)}")
        return None

def generate_pdf_report(results):
    """Generate comprehensive PDF report with ALL details"""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
    from reportlab.lib.units import inch
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.6*inch, bottomMargin=0.6*inch, leftMargin=0.6*inch, rightMargin=0.6*inch)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=28, textColor=colors.HexColor('#0f172a'), spaceAfter=4, fontName='Helvetica-Bold')
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=14, textColor=colors.HexColor('#1e3a5f'), spaceAfter=4, fontName='Helvetica-Bold')
    tagline_style = ParagraphStyle('Tagline', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor('#64748b'), spaceAfter=20)
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#0f172a'), spaceBefore=20, spaceAfter=10, fontName='Helvetica-Bold')
    subheading_style = ParagraphStyle('SubHeading', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor('#475569'), spaceAfter=8, fontName='Helvetica-Bold')
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#334155'), leading=14)
    small_style = ParagraphStyle('Small', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#64748b'), leading=12)
    
    story = []
    
    # ========== HEADER ==========
    story.append(Paragraph("CLARITY AI", title_style))
    story.append(Paragraph("Marketing Intelligence Report", subtitle_style))
    story.append(Paragraph("Stop guessing. Start knowing.", tagline_style))
    
    # Report metadata
    meta_data = [
        ['Report Generated:', datetime.now().strftime('%B %d, %Y at %I:%M %p')],
        ['Analysis Mode:', results.get('mode', 'Demo').title()],
        ['Optimization Goal:', results.get('goal', 'ROAS').upper()],
        ['Monthly Budget:', f"${results.get('budget', 10000):,}"],
    ]
    meta_table = Table(meta_data, colWidths=[1.5*inch, 3*inch])
    meta_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#64748b')),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#0f172a')),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 20))
    
    # ========== EXECUTIVE SUMMARY ==========
    story.append(Paragraph("EXECUTIVE SUMMARY", heading_style))
    
    stats = results.get('stats', {})
    summary = results.get('summary', {})
    
    # Key metrics table
    metrics_data = [
        ['METRIC', 'VALUE', 'DESCRIPTION'],
        ['Monthly Savings', f"${stats.get('total_savings', 0):,}", 'Potential savings from pausing underperforming keywords'],
        ['Annual Impact', f"${stats.get('annual_savings', 0):,}", 'Projected 12-month savings opportunity'],
        ['Keywords Analyzed', str(stats.get('total_units', 0)), 'Total unique keywords processed'],
        ['Avg Confidence', f"{stats.get('avg_confidence', 0)}%", 'Average confidence score across recommendations'],
        ['Total Ad Spend', f"${stats.get('total_spend', 0):,}", 'Total advertising spend analyzed'],
    ]
    
    metrics_table = Table(metrics_data, colWidths=[1.5*inch, 1.2*inch, 3.3*inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 15))
    
    # Action summary
    story.append(Paragraph("ACTION BREAKDOWN", subheading_style))
    action_data = [
        ['Action', 'Count', 'Description'],
        ['🛑 STOP', str(summary.get('stop', 0)), 'Keywords to pause immediately - wasting budget'],
        ['🔧 FIX', str(summary.get('fix', 0)), 'Keywords needing optimization - underperforming'],
        ['💰 INVEST', str(summary.get('invest', 0)), 'Keywords to scale - high performers'],
        ['👁 OBSERVE', str(summary.get('observe', 0)), 'Keywords to monitor - gathering data'],
    ]
    
    action_table = Table(action_data, colWidths=[1*inch, 0.8*inch, 4.2*inch])
    action_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#475569')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#fee2e2')),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#fef3c7')),
        ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#dcfce7')),
        ('BACKGROUND', (0, 4), (-1, 4), colors.HexColor('#f1f5f9')),
    ]))
    story.append(action_table)
    story.append(Spacer(1, 20))
    
    # ========== AI INSIGHT ==========
    ai_insight = results.get('ai_insight', '')
    if ai_insight:
        story.append(Paragraph("AI-POWERED EXECUTIVE INSIGHT", heading_style))
        
        insight_data = [[Paragraph(ai_insight, body_style)]]
        insight_table = Table(insight_data, colWidths=[6*inch])
        insight_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f9ff')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#bae6fd')),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(insight_table)
        story.append(Spacer(1, 10))
    
    # ========== DETAILED RECOMMENDATIONS ==========
    recommendations = results.get('recommendations', {})
    
    sections = [
        ('🛑 STOP - PAUSE IMMEDIATELY', 'stop', colors.HexColor('#dc2626'), 
         'These keywords are wasting your budget. Pause them now to save money.'),
        ('🔧 FIX - OPTIMIZE THESE', 'fix', colors.HexColor('#d97706'),
         'These keywords have potential but need optimization to perform better.'),
        ('💰 INVEST - SCALE UP', 'invest', colors.HexColor('#16a34a'),
         'These keywords are your winners. Increase budget to maximize returns.'),
        ('👁 OBSERVE - MONITOR', 'observe', colors.HexColor('#64748b'),
         'These keywords need more data. Keep running and monitor performance.'),
    ]
    
    for section_title, key, header_color, description in sections:
        items = recommendations.get(key, [])
        
        story.append(PageBreak())
        story.append(Paragraph(section_title, heading_style))
        story.append(Paragraph(description, small_style))
        story.append(Paragraph(f"Total: {len(items)} keywords", small_style))
        story.append(Spacer(1, 10))
        
        if items:
            # Detailed table with all metrics
            table_data = [['P', 'Keyword', 'Spend', 'Conv', 'ROI', 'SEO Vol', 'Leads', 'Reason', 'Conf']]
            
            for item in items[:25]:  # Top 25 per category
                ads = item.get('ads', {})
                seo = item.get('seo', {})
                crm = item.get('crm', {})
                derived = item.get('derived', {})
                classification = item.get('classification', {})
                confidence = item.get('confidence', {})
                
                roi_val = derived.get('roi')
                roi_str = f"{roi_val:.1f}x" if roi_val else '-'
                
                seo_vol = seo.get('volume', 0)
                seo_str = f"{seo_vol/1000:.0f}K" if seo_vol >= 1000 else str(seo_vol) if seo_vol else '-'
                
                leads = crm.get('leads', 0)
                leads_str = str(leads) if leads else '-'
                
                table_data.append([
                    f"P{classification.get('priority', '-')}",
                    item.get('keyword', '')[:20],
                    f"${ads.get('spend', 0):,.0f}",
                    str(ads.get('conversions', 0)),
                    roi_str,
                    seo_str,
                    leads_str,
                    classification.get('reason', '')[:35],
                    f"{confidence.get('score', 0)}%"
                ])
            
            detail_table = Table(table_data, colWidths=[0.35*inch, 1.1*inch, 0.55*inch, 0.4*inch, 0.45*inch, 0.5*inch, 0.4*inch, 1.9*inch, 0.4*inch])
            detail_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), header_color),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 8),
                ('FONTSIZE', (0, 1), (-1, -1), 7),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LEFTPADDING', (0, 0), (-1, -1), 3),
                ('RIGHTPADDING', (0, 0), (-1, -1), 3),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
                ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                ('ALIGN', (2, 0), (6, -1), 'RIGHT'),
                ('ALIGN', (8, 0), (8, -1), 'CENTER'),
            ]))
            story.append(detail_table)
            
            if len(items) > 25:
                story.append(Spacer(1, 8))
                story.append(Paragraph(f"... and {len(items) - 25} more keywords in this category", small_style))
        else:
            story.append(Paragraph("No keywords in this category.", body_style))
    
    # ========== METHODOLOGY ==========
    story.append(PageBreak())
    story.append(Paragraph("METHODOLOGY & SCORING", heading_style))
    
    story.append(Paragraph("How Clarity AI Analyzes Your Data", subheading_style))
    story.append(Paragraph(
        "Clarity AI combines signals from your advertising platforms, SEO tools, and CRM to create a unified view of each keyword's performance. "
        "We calculate three core scores and a confidence level to ensure actionable recommendations.",
        body_style
    ))
    story.append(Spacer(1, 10))
    
    method_data = [
        ['Score', 'Weight', 'Factors'],
        ['Efficiency', '40%', 'ROI, CTR, Conversion Rate, Cost per Lead'],
        ['Opportunity', '30%', 'SEO Search Volume, Market Demand, Competition Level'],
        ['Quality', '30%', 'Lead Qualification Rate, Revenue per Lead, CRM Signals'],
        ['Confidence', '-', 'Data Completeness, Sample Size, Conversion Volume'],
    ]
    method_table = Table(method_data, colWidths=[1.2*inch, 0.8*inch, 4*inch])
    method_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a5f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
    ]))
    story.append(method_table)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("Classification Rules", subheading_style))
    rules_data = [
        ['Action', 'Triggered When'],
        ['STOP', 'Spend > $100 with zero conversions, ROI < 0.5x, CPL > $100'],
        ['FIX', 'High clicks + low conversions, CTR < 1.5%, Poor qualification rate'],
        ['INVEST', 'ROI >= 3x, High SEO volume + low spend, Efficiency > 70%'],
        ['OBSERVE', 'Confidence < 40%, Spend < $50, New keywords gathering data'],
    ]
    rules_table = Table(rules_data, colWidths=[1*inch, 5*inch])
    rules_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#475569')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
    ]))
    story.append(rules_table)
    
    # ========== FOOTER ==========
    story.append(Spacer(1, 40))
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#64748b'), alignment=1)
    story.append(Paragraph("—" * 50, footer_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Generated by Clarity AI | Marketing Intelligence Platform", footer_style))
    story.append(Paragraph("Built by Rupam Patra | linkedin.com/in/rupam-patra", footer_style))
    story.append(Spacer(1, 5))
    story.append(Paragraph("© 2026 Clarity AI | All Rights Reserved", footer_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def parse_csv_file(uploaded_file, data_type):
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.lower().str.strip()
        
        column_maps = {
            'ads': {'keyword': ['keyword', 'keywords', 'search_term'], 'spend': ['spend', 'cost'], 'clicks': ['clicks'], 'conversions': ['conversions', 'conv'], 'revenue': ['revenue', 'value']},
            'seo': {'keyword': ['keyword', 'text'], 'volume': ['volume', 'vol'], 'cpc': ['cpc'], 'competition': ['competition']},
            'crm': {'origin': ['origin', 'source', 'keyword'], 'leads': ['leads'], 'qualified_leads': ['qualified_leads', 'qualified'], 'revenue': ['revenue']}
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
        st.error(f"Error parsing file: {e}")
        return []

def render_hero():
    st.markdown("""
    <div class="hero-container">
        <div class="hero-content">
            <div class="hero-badge">BETA</div>
            <div class="hero-title">Clarity AI</div>
            <div class="hero-subtitle">Stop guessing. Start knowing.</div>
            <div class="hero-description">
                AI-powered marketing intelligence that analyzes your Ads, SEO, and CRM data 
                to tell you exactly what to STOP, FIX, INVEST, or OBSERVE — with confidence scores 
                so you know when to trust the recommendations.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_demo_tab():
    st.markdown('<div class="section-header">Try Clarity AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">Experience the full power of our marketing intelligence engine. No signup required.</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class="demo-card demo-card-quick">
            <div class="demo-title">Quick Demo</div>
            <div class="demo-description">
                Pre-built marketing dataset processed through our complete AI analysis pipeline.
                Perfect for seeing Clarity AI in action.
            </div>
            <ul class="demo-features">
                <li>Processes in ~15-20 seconds</li>
                <li>60 advertising keywords</li>
                <li>60 SEO keywords with volume data</li>
                <li>58 CRM leads with qualification rates</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        quick_demo = st.button("Run Quick Demo", key="quick_demo", use_container_width=True, type="primary")
    
    with col2:
        st.markdown("""
        <div class="demo-card demo-card-live">
            <div class="demo-title">Live Demo</div>
            <div class="demo-description">
                Real-time analysis using public Kaggle datasets. 
                Demonstrates our external data integration capabilities.
            </div>
            <ul class="demo-features">
                <li>Processes in ~45-60 seconds</li>
                <li>Real Google Ads performance data</li>
                <li>Live SEO keyword research data</li>
                <li>Marketing funnel conversion data</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        live_demo = st.button("Run Live Demo", key="live_demo", use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("##### Analysis Settings")
    col1, col2 = st.columns(2)
    with col1:
        goal = st.selectbox("Optimization Goal", ["Maximize ROAS", "Increase Conversions", "Reduce CPA", "Scale Traffic"], help="What's your primary marketing objective?")
    with col2:
        budget = st.number_input("Monthly Ad Budget ($)", value=10000, min_value=1000, max_value=1000000, step=1000, help="Your approximate monthly advertising spend")
    
    if quick_demo:
        run_analysis("synthetic", goal, budget)
    elif live_demo:
        run_analysis("kaggle", goal, budget)

def render_upload_tab():
    st.markdown('<div class="section-header">Analyze Your Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">Upload your marketing data for personalized AI recommendations.</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <span class="info-box-text"><strong>Your data is secure.</strong> Files are processed in real-time and never stored on our servers.</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("##### Step 1: Upload Your Data Files")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Advertising Data**")
        st.caption("Google Ads, Meta Ads, etc.")
        ads_file = st.file_uploader("Upload Ads CSV", type=['csv'], key="ads_upload", label_visibility="collapsed")
        if ads_file:
            st.success(f"Uploaded: {ads_file.name}")
        with st.expander("Required columns"):
            st.markdown("• `keyword` • `spend` • `clicks` • `conversions`")
    
    with col2:
        st.markdown("**SEO Data** *(Optional)*")
        st.caption("SEMrush, Ahrefs, etc.")
        seo_file = st.file_uploader("Upload SEO CSV", type=['csv'], key="seo_upload", label_visibility="collapsed")
        if seo_file:
            st.success(f"Uploaded: {seo_file.name}")
        with st.expander("Required columns"):
            st.markdown("• `keyword` • `volume`")
    
    with col3:
        st.markdown("**CRM Data** *(Optional)*")
        st.caption("Salesforce, HubSpot, etc.")
        crm_file = st.file_uploader("Upload CRM CSV", type=['csv'], key="crm_upload", label_visibility="collapsed")
        if crm_file:
            st.success(f"Uploaded: {crm_file.name}")
        with st.expander("Required columns"):
            st.markdown("• `origin` • `leads`")
    
    st.markdown("")
    st.markdown("##### Step 2: Configure Analysis")
    col1, col2 = st.columns(2)
    with col1:
        goal = st.selectbox("Primary Goal", ["Maximize ROAS", "Increase Conversions", "Reduce CPA", "Scale Traffic"], key="upload_goal")
    with col2:
        budget = st.number_input("Monthly Budget ($)", value=5000, min_value=100, step=500, key="upload_budget")
    
    st.markdown("")
    if st.button("Analyze My Data", use_container_width=True, type="primary", disabled=not ads_file):
        data = {
            'ads': parse_csv_file(ads_file, 'ads') if ads_file else [],
            'seo': parse_csv_file(seo_file, 'seo') if seo_file else [],
            'crm': parse_csv_file(crm_file, 'crm') if crm_file else []
        }
        run_analysis("upload", goal, budget, data)
    
    if not ads_file:
        st.caption("Upload at least your Ads data to begin analysis")

def render_connect_tab():
    st.markdown('<div class="section-header">Direct Integrations</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">Skip the CSV uploads. Connect your tools directly for automated, real-time intelligence.</div>', unsafe_allow_html=True)
    
    st.markdown("##### Advertising Platforms")
    cols = st.columns(5)
    ad_integrations = ["Google Ads", "Meta Ads", "LinkedIn Ads", "TikTok Ads", "Amazon Ads"]
    for i, name in enumerate(ad_integrations):
        with cols[i]:
            st.markdown(f"""
            <div class="integration-card">
                <div class="integration-name" style="font-size: 1rem; margin-bottom: 0.75rem; margin-top: 0.5rem;">{name}</div>
                <span class="coming-soon-badge">Coming Soon</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("##### CRM & Sales Platforms")
    cols = st.columns(5)
    crm_integrations = ["Salesforce", "HubSpot", "Pipedrive", "Zoho CRM", "Monday"]
    for i, name in enumerate(crm_integrations):
        with cols[i]:
            st.markdown(f"""
            <div class="integration-card">
                <div class="integration-name" style="font-size: 1rem; margin-bottom: 0.75rem; margin-top: 0.5rem;">{name}</div>
                <span class="coming-soon-badge">Coming Soon</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("##### SEO & Analytics")
    cols = st.columns(5)
    seo_integrations = ["Google Analytics", "Search Console", "SEMrush", "Ahrefs", "Moz"]
    for i, name in enumerate(seo_integrations):
        with cols[i]:
            st.markdown(f"""
            <div class="integration-card">
                <div class="integration-name" style="font-size: 1rem; margin-bottom: 0.75rem; margin-top: 0.5rem;">{name}</div>
                <span class="coming-soon-badge">Coming Soon</span>
            </div>
            """, unsafe_allow_html=True)
    


def render_results_tab():
    if 'analysis_results' not in st.session_state or not st.session_state.analysis_results:
        st.markdown('<div class="section-header">Results</div>', unsafe_allow_html=True)
        st.info("Run an analysis from the **Try Demo** or **Upload Data** tab to see your results here.")
        return
    
    results = st.session_state.analysis_results
    stats = results.get('stats', {})
    summary = results.get('summary', {})
    
    st.markdown('<div class="section-header">Marketing Intelligence Report</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-subheader">Generated {datetime.now().strftime("%B %d, %Y at %I:%M %p")} • Mode: {results.get("mode", "demo").title()}</div>', unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    metrics = [
        ("Monthly Savings", f"${stats.get('total_savings', 0):,}"),
        ("Keywords Analyzed", f"{stats.get('total_units', 0)}"),
        ("Avg Confidence", f"{stats.get('avg_confidence', 0)}%"),
        ("Actions Needed", f"{summary.get('stop', 0) + summary.get('fix', 0)}"),
        ("Annual Impact", f"${stats.get('annual_savings', 0):,}"),
    ]
    for col, (label, value) in zip([col1, col2, col3, col4, col5], metrics):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{value}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # AI Insight
    ai_insight = results.get('ai_insight', '')
    if ai_insight:
        st.markdown(f"""
        <div class="ai-insight">
            <div class="ai-insight-header">
                <span class="ai-insight-title">AI Executive Summary</span>
            </div>
            <div class="ai-insight-text">{ai_insight}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Recommendations Tabs
    recommendations = results.get('recommendations', {})
    
    tab_stop, tab_fix, tab_invest, tab_observe = st.tabs([
        f"STOP ({len(recommendations.get('stop', []))})",
        f"FIX ({len(recommendations.get('fix', []))})",
        f"INVEST ({len(recommendations.get('invest', []))})",
        f"OBSERVE ({len(recommendations.get('observe', []))})"
    ])
    
    def render_table(data, action_type):
        if not data:
            st.info(f"No {action_type} recommendations in this analysis.")
            return
        
        df = pd.DataFrame([{
            'Priority': f"P{item.get('classification', {}).get('priority', '-')}",
            'Keyword': item.get('keyword', ''),
            'Spend': f"${item.get('ads', {}).get('spend', 0):,.0f}",
            'Conversions': item.get('ads', {}).get('conversions', 0),
            'ROI': f"{item.get('derived', {}).get('roi', 0) or 0:.1f}x" if item.get('derived', {}).get('roi') else '-',
            'SEO Volume': f"{item.get('seo', {}).get('volume', 0):,}" if item.get('seo', {}).get('volume') else '-',
            'Leads': item.get('crm', {}).get('leads', 0) or '-',
            'Reason': item.get('classification', {}).get('reason', ''),
            'Confidence': f"{item.get('confidence', {}).get('score', 0)}%"
        } for item in data])
        
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    with tab_stop:
        st.markdown("**Keywords to pause immediately** — wasting budget with poor or no returns")
        render_table(recommendations.get('stop', []), "STOP")
    
    with tab_fix:
        st.markdown("**Keywords to optimize** — potential exists but performance needs improvement")
        render_table(recommendations.get('fix', []), "FIX")
    
    with tab_invest:
        st.markdown("**Keywords to scale** — strong performers with room to grow")
        render_table(recommendations.get('invest', []), "INVEST")
    
    with tab_observe:
        st.markdown("**Keywords to monitor** — gathering data or stable performance")
        render_table(recommendations.get('observe', []), "OBSERVE")
    
    # Download Section
    st.markdown("---")
    st.markdown("##### Download Report")
    
    try:
        pdf_buffer = generate_pdf_report(results)
        st.download_button(
            "Download Complete PDF Report",
            pdf_buffer,
            f"clarity_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            "application/pdf",
            use_container_width=True,
            type="primary"
        )
    except Exception as e:
        st.error(f"PDF generation error: {e}")

def render_about_tab():
    st.markdown('<div class="section-header">About Clarity AI</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        #### The Problem
        
        Marketers are **drowning in dashboards** but **starving for direction**.
        
        - Google Ads says CTR is 2.3%... but should you pause or scale?
        - Analytics shows traffic is up 15%... but is it profitable?
        - CRM shows 50 new leads... but which keywords actually drive revenue?
        
        The average marketing manager spends **5+ hours weekly** analyzing data across platforms, often making gut-feel decisions despite having more data than ever.
        
        ---
        
        #### The Solution
        
        Clarity AI connects your **Ads + SEO + CRM** data to deliver one thing dashboards can't: **clear, prioritized actions**.
        
        Instead of "CTR is 2.3%", you get:
        
        > **STOP** 'cheap sneakers' — $387 spent, 0 conversions, 89% confident
        
        > **INVEST** in 'marathon training shoes' — 5.2x ROI, 22K monthly searches
        """)
    
    with col2:
        st.markdown("""
        #### How It Works
        
        1. **Connect** — Upload your data or use our integrations
        2. **Aggregate** — We merge signals across all sources by keyword
        3. **Score** — AI calculates Efficiency, Opportunity & Quality scores
        4. **Act** — Get STOP/FIX/INVEST/OBSERVE with confidence levels
        
        ---
        
        #### Technology
        
        | Component | Technology |
        |-----------|------------|
        | Frontend | Streamlit |
        | Backend | n8n Workflow Automation |
        | AI Engine | OpenAI GPT-4o |
        | Hosting | Streamlit Cloud + Railway |
        
        ---
        
        #### Built By
        
        **Rupam Patra**  
        Senior Software Engineer | AI & Business Transformation
        
        [LinkedIn](https://linkedin.com/in/rupam-patra)
        """)
    
    st.markdown("---")
    st.caption("Clarity AI v1.0 (Beta) • © 2026 • All Rights Reserved")

def run_analysis(mode, goal, budget, data=None):
    goal_map = {"Maximize ROAS": "roas", "Increase Conversions": "conversions", "Reduce CPA": "cpa", "Scale Traffic": "traffic"}
    
    progress = st.progress(0, text="Initializing analysis...")
    
    if mode == "synthetic":
        progress.progress(15, text="Loading synthetic dataset...")
        data = load_synthetic_data()
        if not data:
            progress.empty()
            return
        time.sleep(0.3)
    
    progress.progress(30, text="Connecting to Clarity AI engine...")
    time.sleep(0.2)
    
    progress.progress(50, text="AI is analyzing your data...")
    
    results = call_n8n_webhook(mode, data, goal_map.get(goal, "roas"), budget)
    
    if results:
        progress.progress(90, text="Generating insights...")
        time.sleep(0.3)
        progress.progress(100, text="Analysis complete!")
        time.sleep(0.5)
        progress.empty()
        
        st.session_state.analysis_results = results
        st.session_state.active_tab = "results"
        st.balloons()
        st.rerun()
    else:
        progress.empty()

def main():
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "demo"
    
    render_hero()
    
    tabs = st.tabs(["Try Demo", "Upload Data", "Integrations", "Results", "About"])
    
    with tabs[0]:
        render_demo_tab()
    with tabs[1]:
        render_upload_tab()
    with tabs[2]:
        render_connect_tab()
    with tabs[3]:
        render_results_tab()
    with tabs[4]:
        render_about_tab()

if __name__ == "__main__":
    main()
