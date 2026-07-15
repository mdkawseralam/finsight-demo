import streamlit as st
import pandas as pd
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
    .sidebar-hint {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        color: #78716C;
        line-height: 1.5;
        margin-top: 0.4rem;
        margin-bottom: 0.6rem;
    }
    .sidebar-hint a { color: #1F4B3F; text-decoration: underline; }

    /* Radio button styling */
    div[role="radiogroup"] label {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.82rem !important;
        color: #14100C !important;
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
    .stSelectbox > div > div {
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
    st.markdown(
        '<div class="sidebar-hint">Paste an OpenAI or Anthropic (Claude) API key. Keys are used only in this session and never stored.</div>',
        unsafe_allow_html=True
    )

    provider = st.radio(
        "Provider",
        ["OpenAI", "Anthropic (Claude)"],
        horizontal=True,
        label_visibility="collapsed"
    )

    key_label = "OpenAI API Key" if provider == "OpenAI" else "Claude API Key"
    key_placeholder = "sk-..." if provider == "OpenAI" else "sk-ant-..."
    key_link = "platform.openai.com/api-keys" if provider == "OpenAI" else "console.anthropic.com"

    api_key = st.text_input(
        key_label,
        type="password",
        placeholder=key_placeholder,
        label_visibility="visible"
    )
    st.markdown(
        f'<div class="sidebar-hint">Get one at <a href="https://{key_link}" target="_blank">{key_link}</a></div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="sidebar-section">Note</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='font-family: Inter, sans-serif; font-size: 0.76rem; color: #5C5852; line-height: 1.6;'>
        Data is processed in-session and not stored. Human review is mandatory before external distribution.
    </div>
    """, unsafe_allow_html=True)


# --- MAIN CONTENT ---
col_input, col_output = st.columns([1, 1.15], gap="large")

with col_input:
    # LAYER 01
    st.markdown("""
    <div class="layer-eyebrow">
        <span class="layer-num">01</span>
        <span class="layer-label">What Moved · Financial Data</span>
    </div>
    <div class="layer-title">Variance detection</div>
    <div class="layer-desc">Provide month-end P&amp;L data — Actuals vs Budget vs LY. Upload an Excel file or paste the numbers directly.</div>
    """, unsafe_allow_html=True)

    input_mode = st.radio(
        "Input mode",
        ["Upload Excel", "Paste data"],
        horizontal=True,
        label_visibility="collapsed"
    )

    upload_file = None
    pasted_data = None

    if input_mode == "Upload Excel":
        upload_file = st.file_uploader(" ", type=["xlsx"], label_visibility="collapsed")
    else:
        pasted_data = st.text_area(
            "Paste data",
            placeholder=(
                "Paste your variance data here. Example:\n\n"
                "Sales: 82.5M (Budget: 100M · LY: 95M)\n"
                "GP: 38% (Budget: 40% · LY: 39%)\n"
                "Volume impact: -15M\n"
                "Price impact: +2.5M\n"
                "Mix impact: -3M\n"
                "A&P: 8.2M (Budget: 12M)\n"
                "Trade spend: 6.5M (Budget: 5.5M)"
            ),
            height=180,
            label_visibility="collapsed"
        )

    # LAYER 02
    st.markdown("""
    <div class="layer-eyebrow">
        <span class="layer-num">02</span>
        <span class="layer-label">Why It Moved · Driver Split</span>
    </div>
    <div class="layer-title">Volume · Price · Mix decomposition</div>
    <div class="layer-desc">Read from the same input above — include Volume / Price / Mix / Channel splits in your Excel or pasted data.</div>
    """, unsafe_allow_html=True)

    # LAYER 03
    st.markdown("""
    <div class="layer-eyebrow">
        <span class="layer-num">03</span>
        <span class="layer-label">Root Cause · Business Context</span>
    </div>
    <div class="layer-title">Qualitative context</div>
    <div class="layer-desc">Include brand, SBU, reporting month, and any qualitative context — stock-outs, competitor moves, A&amp;P shifts, distribution gaps.</div>
    """, unsafe_allow_html=True)

    context_text = st.text_area(
        "Context",
        placeholder=(
            "Include the following in your context — Brand, SBU, Reporting Month, and qualitative notes.\n\n"
            "Example:\n"
            "Brand: [Your Brand] · SBU: [Your SBU] · Month: [MMM YYYY]\n\n"
            "- 11-day stock-out of [SKU] in [Region] during Week 2\n"
            "- Competitor launched 20% off campaign starting [date]\n"
            "- A&P underspent by 30% vs plan in the same window\n"
            "- Modern Trade channel outperformed due to promotional lift\n"
            "- Distribution gap in [Region] — 15% fewer active outlets vs LY"
        ),
        height=200,
        label_visibility="collapsed"
    )

    use_demo = st.checkbox("Run with demo data")
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


# --- LOGIC ENGINE ---
if generate:
    if not api_key:
        st.warning(f"Please enter your {key_label} in the sidebar to proceed.")
    else:
        # 1. Prepare Data
        if use_demo:
            data_payload = "Sales: 82.5M (Budget: 100M, LY: 95M), GP: 38% (Budget: 40%), Volume impact: -15M, Price impact: +2.5M, Mix: -3M, A&P: 8.2M (Budget: 12M)"
            context_payload = "Brand: Savlon Handwash · SBU: Toiletries · Month: June 2024. 10-day production halt on 500ml SKU; Chattogram transport strike in W2; competitor Dettol ran a B1G1 promo across Modern Trade; A&P underspent by 32% vs plan."
        elif upload_file is not None:
            df = pd.read_excel(upload_file)
            data_payload = df.to_string()
            context_payload = context_text
        elif pasted_data:
            data_payload = pasted_data
            context_payload = context_text
        else:
            st.error("Please upload an Excel file, paste your data, or enable 'Run with demo data'.")
            st.stop()

        # 2. AI Synthesis
        system_prompt = (
            "You are a Senior Finance Business Partner writing month-end variance commentary "
            "for group leadership. Structure the report in three explicit layers:\n\n"
            "LAYER 1 — WHAT MOVED: State the material variances (>5% or >BDT 2Mn) with magnitude and direction.\n"
            "LAYER 2 — WHY IT MOVED: Decompose into Volume / Price / Mix / Channel / A&P / Trade Spend drivers.\n"
            "LAYER 3 — ROOT CAUSE: Connect the numerical drivers to the qualitative business context provided.\n\n"
            "Close with 2–3 recommended actions. Use professional, concise corporate English. "
            "Do not use bullet emojis or decorative symbols."
        )
        user_content = f"Financial Data:\n{data_payload}\n\nBusiness Context:\n{context_payload}"

        with st.spinner('Analysing variances · mapping drivers · synthesising narrative...'):
            try:
                if provider == "OpenAI":
                    import openai
                    client = openai.OpenAI(api_key=api_key)
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_content}
                        ]
                    )
                    report = response.choices[0].message.content
                else:
                    import anthropic
                    client = anthropic.Anthropic(api_key=api_key)
                    response = client.messages.create(
                        model="claude-sonnet-4-5",
                        max_tokens=2000,
                        system=system_prompt,
                        messages=[{"role": "user", "content": user_content}]
                    )
                    report = response.content[0].text

                output_placeholder.markdown(f"""
                <div class="report-container">
                    <div class="report-header">
                        <span class="report-title">Variance Commentary</span>
                        <span class="report-stamp">Generated {datetime.now().strftime('%d %b %Y · %H:%M')}</span>
                    </div>
                    <div class="report-body">{report}</div>
                </div>
                """, unsafe_allow_html=True)

                with col_output:
                    st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)
                    st.download_button(
                        "Export to Report",
                        report,
                        file_name=f"FinSight_Commentary_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
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