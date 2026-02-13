# 🎯 Clarity AI - Marketing Intelligence Platform

> **Stop guessing. Start knowing.**

AI-powered marketing intelligence that tells you exactly what to **STOP**, **FIX**, **INVEST**, or **OBSERVE** in your ad spend.

![Clarity AI](https://img.shields.io/badge/Status-Beta-yellow)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red)

## 🚀 Features

- **⚡ Quick Demo** - Try with pre-built synthetic data (~15-20 seconds)
- **🌐 Live Demo** - Real-time data from Kaggle public datasets (~45-60 seconds)
- **📁 Upload Mode** - Analyze your own marketing data
- **📥 PDF Reports** - Download professional reports
- **📧 Email Reports** - Get reports delivered to your inbox
- **🔌 Integrations** - Coming soon: Google Ads, Salesforce, HubSpot, and more

## 🎯 How It Works

1. **CONNECT** - Upload your Ads, SEO, and CRM data (or use demo mode)
2. **ANALYZE** - Our AI engine merges signals across all sources
3. **SCORE** - Each keyword is scored on Efficiency, Opportunity, and Quality
4. **ACT** - Get prioritized STOP/FIX/INVEST/OBSERVE recommendations

## 🛠️ Tech Stack

- **Frontend:** Streamlit (Python)
- **Backend:** n8n workflow automation
- **AI:** OpenAI GPT-4o-mini for insights generation
- **Hosting:** Streamlit Cloud + Render

## 📦 Installation

### Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/clarity-ai-app.git
cd clarity-ai-app

# Install dependencies
pip install -r requirements.txt

# Create secrets file
mkdir -p .streamlit
echo 'N8N_WEBHOOK_URL = "your-n8n-webhook-url"' > .streamlit/secrets.toml

# Run the app
streamlit run app.py
```

### Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Add secret: `N8N_WEBHOOK_URL` = your n8n webhook URL
5. Deploy!

## 📁 Project Structure

```
clarity-ai-app/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── data/
│   ├── synthetic_ads.json  # Demo ads data
│   ├── synthetic_seo.json  # Demo SEO data
│   └── synthetic_crm.json  # Demo CRM data
└── n8n/
    └── workflow_webhook.json  # n8n workflow (import to your n8n)
```

## 🔧 n8n Setup

1. Deploy n8n to Render (or use n8n Cloud)
2. Import `n8n/workflow_webhook.json`
3. Configure credentials:
   - Kaggle API (for live demo mode)
   - OpenAI API (for AI insights)
4. Activate the workflow
5. Copy the webhook URL to Streamlit secrets

## 📊 Data Format

### Ads Data (Required)
| Column | Description | Required |
|--------|-------------|----------|
| keyword | Search term or ad group | ✅ |
| spend | Total cost | ✅ |
| clicks | Number of clicks | ✅ |
| conversions | Number of conversions | ✅ |
| impressions | Number of impressions | Optional |
| campaign | Campaign name | Optional |
| revenue | Revenue generated | Optional |

### SEO Data (Optional)
| Column | Description | Required |
|--------|-------------|----------|
| keyword | Search term | ✅ |
| volume | Monthly search volume | ✅ |
| cpc | Cost per click | Optional |
| competition | Competition level | Optional |

### CRM Data (Optional)
| Column | Description | Required |
|--------|-------------|----------|
| origin | Lead source/keyword | ✅ |
| leads | Number of leads | ✅ |
| qualified_leads | Qualified lead count | Optional |
| revenue | Deal value | Optional |

## 🎯 Classification Logic

| Action | Trigger Conditions |
|--------|-------------------|
| 🛑 **STOP** | High spend + zero conversions, negative ROI, very high CPL |
| 🔧 **FIX** | Good traffic + low conversion, low CTR, targeting issues |
| 💰 **INVEST** | High ROI, high SEO demand + low ad coverage, quality leads |
| 👁 **OBSERVE** | New keywords, moderate performance, insufficient data |

## 👤 Built By

**Rupam Patra**  
Senior Software Engineer | AI & Business Transformation

- 🔗 [LinkedIn](https://linkedin.com/in/rupam-patra)

---

## 📄 License

MIT License - See LICENSE file for details.

---

*Built for MKTG 6620 - Assignment 5 | Northeastern University | February 2026*
