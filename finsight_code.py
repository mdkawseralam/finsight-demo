import streamlit as st
import pandas as pd
import openai

# --- PAGE CONFIG ---
st.set_page_config(page_title="FinSight | ACI Prototype", layout="wide", page_icon="📊")

# Custom CSS to make it look corporate
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #004a99; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 FinSight: Automated Financial Narrative Engine")
st.subheader("Prototype for Management Review")

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3222/3222764.png", width=100)
    st.header("Control Panel")
    api_key = st.text_input("Enter OpenAI API Key", type="password", help="Needed to run the AI engine")
    
    st.divider()
    brand = st.selectbox("Select Business Unit", ["Savlon", "Mortein", "Harphic", "Logistics"])
    report_date = st.date_input("Reporting Month")
    st.info("Note: This prototype uses GPT-4o for high-accuracy financial reasoning.")

# --- DATA LAYERS ---
col1, col2 = st.columns([1, 1])

with col1:
    st.write("### 📥 Input Layers")
    upload_file = st.file_uploader("Layer 1 & 2: Upload Excel (Actuals vs Budget)", type=["xlsx"])
    
    # Context Area
    context_text = st.text_area(
        "Layer 3: Qualitative Context (Root Causes)", 
        placeholder="e.g. 4-day strike in Chittagong, Dettol promo in Modern Trade...",
        height=150
    )

    use_demo = st.checkbox("Use Demo Data (Savlon June 2024)")

# --- LOGIC ENGINE ---
if st.button("Generate Executive Commentary"):
    if not api_key:
        st.warning("⚠️ Please enter an API Key in the sidebar to proceed.")
    else:
        # 1. Prepare Data
        if use_demo:
            data_payload = "Sales: 82.5M (Bud: 100M), GP: 38% (Bud: 40%), Vol Impact: -15M, Price: +2.5M"
            context_payload = "10-day production halt on 500ml SKU; Chittagong transport strike; Dettol B1G1 promo."
        elif upload_file:
            df = pd.read_excel(upload_file)
            data_payload = df.to_string()
            context_payload = context_text
        else:
            st.error("Please upload a file or select 'Use Demo Data'.")
            st.stop()

        # 2. AI Synthesis
        client = openai.OpenAI(api_key=api_key)
        
        with st.spinner('AI is analyzing variances and mapping root causes...'):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a Senior Finance Business Partner. Write a 3-layer variance report: What moved, Why (Drivers), and Root Cause (Context). Use professional, concise corporate English."},
                        {"role": "user", "content": f"Data: {data_payload}\nContext: {context_payload}"}
                    ]
                )
                
                report = response.choices[0].message.content

                # --- OUTPUT ---
                with col2:
                    st.write("### 📄 Generated Narrative")
                    st.markdown(report)
                    st.download_button("📩 Export to Word", report, file_name=f"FinSight_{brand}_Report.md")
            except Exception as e:
                st.error(f"AI Error: {e}")

# --- FOOTER ---
st.divider()
st.caption("FinSight Prototype | Developed for Internal Management Review")