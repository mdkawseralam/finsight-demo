import streamlit as st
import pandas as pd
import openai
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="FinSight — ACI FP&A",
    layout="wide",
    page_icon="◆",
    initial_sidebar_state="expanded"
)

# --- CUSTOM STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,600;1,8..60,400&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif;
        color: #1C1815;
    }
    .main { background-color: #EFECE2; }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1320px;
    }
    header[data-testid="stHeader"] { background: transparent; }
    footer, [data-testid="stFooter"] { display: none !important; }

    h1, h2, h3 {
        font-family: 'Source Serif 4', Georgia, serif;
        font-weight: 400;
        color: #14100C;
        letter-spacing: -0.02em;
    }

    /* Brand header */
    .brand-header {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        padding-bottom: 1.4rem;
        border-bottom: 1px solid #C9C3B4;
        margin-bottom: 2.5rem;
    }
    .brand-title {
        font-family: 'Source Serif 4', Georgia, serif;
        font-size: 2.8rem;
        font-weight: 400;
        color: #14100C;
        letter-spacing: -0.03em;
        line-height: 1;
    }
    .brand-mark {
        font-family: 'Source Serif 4', Georgia, serif;
        font-style: italic;
        font-weight: 300;
        color: #1F4B3F;
        margin-right: 0.35rem;
    }
    .brand-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 0.72rem;
        font-weight: 500;
        color: #5C5852;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        margin-top: 0.5rem;
    }
    .brand-meta {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        color: #78716C;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        text-align: right;
    }
    .brand-meta .dot { color: #1F4B3F; margin-right: 0.35rem; }

    /* Layer markers */
    .layer-eyebrow {
        display: flex;
        align-items: baseline;
        gap: 0.9rem;
        margin-top: 1.75rem;
        margin-bottom: 0.5rem;
    }
    .layer-num {
        font-family: 'Source Serif 4', Georgia, serif;
        font-style: italic;
        font-size: 1.8rem;
        font-weight: 300;
        color: #1F4B3F;
        line-height: 1;
        font-variant-numeric: tabular-nums;
    }
    .layer-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.68rem;
        font-weight: 600;
        color: #5C5852;
        text-transform: uppercase;
        letter-spacing: 0.2em;
    }
    .layer-title {
        font-family: 'Source Serif 4', Georgia, serif;
        font-size: 1.35rem;
        font-weight: 400;
        color: #14100C;
        margin: 0 0 0.35rem 0;
        letter-spacing: -0.01em;
    }
    .layer-desc {
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: #5C5852;
        margin-bottom: 0.9rem;
        line-height: 1.55;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #E8E4D6;
        border-right: 1px solid #C9C3B4;
    }
    .sidebar-section {
        font-family: 'Inter', sans-serif;
        font-size: 0.68rem;
        font-weight: 600;
        color: #5C5852;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        margin-top: 1.4rem;
        margin-bottom: 0.5rem;
    }

    /* Buttons */
    .stButton > button {
        background-color: #14100C;
        color: #F5F1E8;
        border: none;
        border-radius: 1px;
        height: 3.25rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        transition: all 0.15s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #1F4B3F;
        color: #F5F1E8;
    }
    .stDownloadButton > button {
        background-color: transparent;
        color: #14100C;
        border: 1px solid #14100C;
        border-radius: 1px;
        font-family: 'Inter', sans-serif;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        height: 2.6rem;
    }
    .stDownloadButton > button:hover {
        background-color: #14100C;
        color: #F5F1E8;
    }

    /* Inputs */
    .stTextInput input, .stTextArea textarea,
    .stSelectbox > div > div, .stDateInput input {
        border-radius: 1px !important;
        border: 1px solid #C9C3B4 !important;
        background-color: #FBFAF5 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
        color: #14100C !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #1F4B3F !important;
        box-shadow: 0 0 0 3px rgba(31, 75, 63, 0.08) !important;
    }
    [data-testid="stFileUploader"] section {
        background-color: #FBFAF5;
        border: 1px dashed #B8B2A3;
        border-radius: 1px;
    }
    [data-testid="stFileUploader"] section:hover {
        border-color: #1F4B3F;
    }

    /* Alerts */
    [data-testid="stAlert"] {
        border-radius: 1px;
        border-left: 3px solid #7B2C3B;
        background-color: #FBFAF5;
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
    }

    /* Report output */
    .report-container {
        background-color: #FBFAF5;
        border: 1px solid #C9C3B4;
        border-radius: 1px;
        padding: 2.4rem 2.75rem;
        margin-top: 0.5rem;
    }
    .report-header {
        border-bottom: 1px solid #C9C3B4;
        padding-bottom: 1.1rem;
        margin-bottom: 1.6rem;
        display: flex;
        justify-content: space-between;
        align-items: baseline;
    }
    .report-title {
        font-family: 'Source Serif 4', Georgia, serif;
        font-size: 1.35rem;
        font-weight: 400;
        color: #14100C;
        letter-spacing: -0.01em;
    }
    .report-stamp {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        color: #78716C;
        text-transform: uppercase;
        letter-spacing: 0.15em;
    }
    .report-body {
        font-family: 'Source Serif 4', Georgia, serif;
        font-size: 1.02rem;
        line-height: 1.78;
        color: #1C1815;
    }
    .report-body h1, .report-body h2, .report-body h3 {
        font-family: 'Source Serif 4', Georgia, serif;
        color: #14100C;
        margin-top: 1.4rem;
        margin-bottom: 0.6rem;
    }
    .report-empty {
        min-height: 420px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: #A8A29E;
        font-family: 'Source Serif 4', Georgia, serif;
        font-style: italic;
        font-size: 0.95rem;
    }

    /* Status strip */
    .status-strip {
        display: flex;
        justify-content: space-between;
        padding: 0.7rem 0;
        border-top: 1px solid #C9C3B4;
        margin-top: 3rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        color: #78716C;
        text-transform: uppercase;
        letter-spacing: 0.12em;
    }
</style>
""", unsafe_allow_html=True)


# --- BRAND HEADER ---
st.markdown(f"""
<div class="brand-header">
    <div>
        <div class="brand-title"><span class="brand-mark">◆</span>FinSight</div>
        <div class="brand-subtitle">Layered Variance Commentary Engine · ACI Finance &amp; Planning</div>
    </div>
    <div class="brand-meta">
        <span class="dot">●</span>Prototype · v0.1<br>
        {datetime.now().strftime('%d %b %Y').upper()}
    </div>
</div>
""", unsafe_allow_html=True)


# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div class="sidebar-section">Engine</div>', unsafe_allow_html=True)
    api_key = st.text_input(
        "OpenAI API Key", type="password",
        placeholder="sk-...",
        label_visibility="collapsed",
        help="Required to run the AI engine. Session-only."
    )

    st.markdown('<div class="sidebar-section">Reporting Scope</div>', unsafe_allow_html=True)
    brand = st.selectbox(
        "Business Unit",
        ["Savlon", "Septex", "SC Johnson Portfolio", "Colgate-Palmolive Portfolio", "Consolidated Toiletries"],
        label_visibility="collapsed"
    )
    report_date = st.date_input("Reporting Month", label_visibility="collapsed")

    st.markdown('<div class="sidebar-section">Model</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='font-family: JetBrains Mono, monospace; font-size: 0.78rem; color: #14100C; padding: 0.3rem 0;'>
        GPT-4o
        <div style='color: #78716C; font-size: 0.65rem; margin-top: 0.2rem; font-family: Inter, sans-serif; letter-spacing: 0.05em;'>Optimised for financial reasoning</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Note</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='font-family: Inter, sans-serif; font-size: 0.76rem; color: #5C5852; line-height: 1.6;'>
        Data is processed in-session and not stored. Human review is mandatory before external distribution.
    </div>
    """, unsafe_allow_html=True)


# --- MAIN CONTENT ---
col_input, col_output = st.columns([1, 1.15], gap="large")

with col_input:
    st.markdown("""
    <div class="layer-eyebrow">
        <span class="layer-num">01</span>
        <span class="layer-label">What Moved · Financial Data</span>
    </div>
    <div class="layer-title">Variance detection</div>
    <div class="layer-desc">Month-end P&amp;L — Actuals vs Budget vs LY, at brand, channel, or SKU level.</div>
    """, unsafe_allow_html=True)
    upload_file = st.file_uploader(" ", type=["xlsx"], label_visibility="collapsed")

    st.markdown("""
    <div class="layer-eyebrow">
        <span class="layer-num">02</span>
        <span class="layer-label">Why It Moved · Driver Split</span>
    </div>
    <div class="layer-title">Volume · Price · Mix decomposition</div>
    <div class="layer-desc">Read from the same upload — no extra input if PVM columns are present.</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="layer-eyebrow">
        <span class="layer-num">03</span>
        <span class="layer-label">Root Cause · Business Context</span>
    </div>
    <div class="layer-title">Qualitative context</div>
    <div class="layer-desc">Notes from brand, channel, supply chain — stock-outs, competitor actions, A&amp;P shifts, distribution gaps.</div>
    """, unsafe_allow_html=True)
    context_text = st.text_area(
        " ",
        placeholder="e.g. 11-day stock-out of Savlon 100ml in Chattogram (W2 June); Lifebuoy 20% off campaign from 5 June; A&P underspend of 30% vs plan in the same window.",
        height=140,
        label_visibility="collapsed"
    )

    use_demo = st.checkbox("Run with demo data (Savlon · June 2024)")
    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
    generate = st.button("Generate Executive Commentary")

with col_output:
    st.markdown("""
    <div class="layer-eyebrow">
        <span class="layer-num" style="font-style: normal;">→</span>
        <span class="layer-label">Output · Board-Ready Narrative</span>
    </div>
    <div class="layer-title">Generated commentary</div>
    <div class="layer-desc">Three-layer synthesis — what moved, why it moved, and the root cause — drafted in ACI's house tone.</div>
    """, unsafe_allow_html=True)

    output_placeholder = st.empty()
    output_placeholder.markdown("""
    <div class="report-container">
        <div class="report-empty">Awaiting inputs. The generated narrative will appear here.</div>
    </div>
    """, unsafe_allow_html=True)


# --- LOGIC ENGINE (unchanged core) ---
if generate:
    if not api_key:
        st.warning("Please enter an OpenAI API key in the sidebar to proceed.")
    else:
        if use_demo:
            data_payload = "Sales: 82.5M (Bud: 100M), GP: 38% (Bud: 40%), Vol Impact: -15M, Price: +2.5M"
            context_payload = "10-day production halt on 500ml SKU; Chittagong transport strike; Dettol B1G1 promo."
        elif upload_file:
            df = pd.read_excel(upload_file)
            data_payload = df.to_string()
            context_payload = context_text
        else:
            st.error("Please upload a file or select 'Run with demo data'.")
            st.stop()

        client = openai.OpenAI(api_key=api_key)

        with st.spinner('Analysing variances · mapping drivers · synthesising narrative...'):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a Senior Finance Business Partner. Write a 3-layer variance report: What moved, Why (Drivers), and Root Cause (Context). Use professional, concise corporate English."},
                        {"role": "user", "content": f"Data: {data_payload}\nContext: {context_payload}"}
                    ]
                )
                report = response.choices[0].message.content

                output_placeholder.markdown(f"""
                <div class="report-container">
                    <div class="report-header">
                        <span class="report-title">{brand} · Variance Commentary</span>
                        <span class="report-stamp">{report_date.strftime('%b %Y').upper()} · {datetime.now().strftime('%H:%M')}</span>
                    </div>
                    <div class="report-body">{report}</div>
                </div>
                """, unsafe_allow_html=True)

                with col_output:
                    st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)
                    st.download_button(
                        "Export to Report",
                        report,
                        file_name=f"FinSight_{brand.replace(' ', '_')}_{report_date.strftime('%Y_%m')}.md"
                    )
            except Exception as e:
                st.error(f"Engine error: {e}")


# --- STATUS STRIP ---
st.markdown("""
<div class="status-strip">
    <span>FinSight · Internal Prototype · ACI Finance &amp; Planning</span>
    <span>Human review required before distribution</span>
</div>
""", unsafe_allow_html=True)