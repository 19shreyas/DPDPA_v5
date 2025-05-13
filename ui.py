import streamlit as st

def set_custom_css():
    st.markdown("""
    <style>
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #2E2E38;
        color: white !important;
    }
    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Main text and headers */
    section.main div.block-container {
        color: #2E2E38 !important;
    }
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #2E2E38 !important;
    }

    /* Fix for input text color */
    input, textarea, select, div[role="textbox"] {
        color: #2E2E38 !important;
        caret-color: #2E2E38
    }

    /* Fix for selectbox and dropdowns */
    .stSelectbox div, .stRadio div, .stCheckbox div, .stTextInput div, .stDownloadButton div {
        color: #2E2E38 !important;
    }

    /* Fix file uploader text inside black box */
    .stFileUploader div, .stFileUploader span {
    color: white !important;
    }
    /* --- Force white text in selectbox/multiselect dropdowns with dark bg --- */
    div[data-baseweb="select"] {
        color: white !important;
    }
    
    div[data-baseweb="select"] * {
        color: white !important;
    }


    /* Fix Browse files button text inside file uploader */
    .stFileUploader button,
    .stFileUploader label {
    color: black !important;
    font-weight: 500;
    }

    /* Fix download and regular buttons */
    .stButton > button, .stDownloadButton > button {
        color: white !important;
        background-color: #1a9afa;
        font-weight: 600;
        border-radius: 6px;
        border: none;
    }
    
        
    /* Only for actual input and textarea fields */
    input, textarea {
        background-color: #FFFFFF !important;
        color: #2E2E38 !important;
        border: 1px solid #2E2E38 !important;
        border-radius: 6px !important;
        caret-color: #2E2E38
    }
    /* Additional fix for Streamlit's internal markdown editor (if used) */
    div[contenteditable="true"] {
        caret-color: #2E2E38 !important;
        color: #2E2E38 !important;
    }

    
    /* For Streamlit selectboxes */
    div[data-baseweb="select"] {
        background-color: #2E2E38 !important;
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
    }
    div[data-baseweb="select"] * {
        color: white !important;
    }

    /* === Fix Streamlit checkbox visibility === */
    div[data-baseweb="checkbox"] > label > div {
        background-color: white !important;
        border: 2px solid #2E2E38 !important;
        border-radius: 4px !important;
        width: 20px !important;
        height: 20px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-right: 10px !important;
    }
    
    /* Show checkmark when selected */
    div[data-baseweb="checkbox"] svg {
        stroke: #2E2E38 !important;
        stroke-width: 2.5px !important;
    }
    /* === FIX: Cursor visibility in text areas === */
    textarea,
    .stTextArea textarea,
    div[role="textbox"],
    .stTextInput input {
        background-color: #FFFFFF !important;
        color: #2E2E38 !important;
        caret-color: #2E2E38 !important;
        border: 1px solid #2E2E38 !important;
        border-radius: 6px !important;
    }
    
    /* Explicit caret fix for editable areas */
    div[contenteditable="true"] {
        caret-color: #2E2E38 !important;
        color: #2E2E38 !important;
    }


    </style>
    """, unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.set_page_config(page_title="DPDPA Compliance Tool", layout="wide")
set_custom_css()
st.sidebar.markdown("<h1 style='font-size:42px; font-weight:700;'>Navigation</h1>", unsafe_allow_html=True)

menu = st.sidebar.radio("", [
    "Homepage",
    "Policy Compliance Checker",
    "Policy Generator",
    "Dashboard & Reports",
    "Knowledge Assistant",
    "Admin Settings"
])
st.sidebar.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
#st.sidebar.image(".images/EY-Parthenon_idpWq1a8hl_0.png", width=250)
st.sidebar.markdown("""
    <div style='padding: 0px 12px 0px 0px;'>
        <img src='https://i.postimg.cc/j2dv9kZ2/EY-Parthenon-idp-Wq1a8hl-0.png' width='200'>
    </div>
""", unsafe_allow_html=True)
# --- Homepage ---
if menu == "Homepage":
    st.title("DPDPA Compliance Tool")
    st.markdown("""
    Welcome to the Digital Personal Data Protection Act (DPDPA) Compliance Platform.
    Use the navigation panel to begin generating or matching your policy to India's latest data protection laws.
    """)

# --- Policy Generator ---
elif menu == "Policy Generator":
    st.title("Create a new Policy")
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Full Policy Generator", "Section-wise Generator", "Lifecycle-wise Template", 
        "GPT Draft Assistant", "Saved Drafts"])

    with tab1:
        st.subheader("Full Policy Generator")
        st.text_area("Enter your complete policy draft:", height=300)
        st.button("Generate Suggestions with GPT")

    with tab2:
        st.subheader("Section-wise Generator")
        section = st.selectbox("Choose Section", ["Notice", "Consent", "Data Principal Rights", "Security"])
        st.text_area(f"Draft for {section}:", height=200)
        st.button("Suggest Completion")

    with tab3:
        st.subheader("Lifecycle-wise Template")
        st.markdown("Fill stage-specific privacy info:")
        stages = ["Collection", "Processing", "Storage", "Sharing", "Erasure"]
        for stage in stages:
            st.text_area(f"{stage} Stage", key=stage)

    with tab4:
        st.subheader("GPT-Assisted Draft Builder")
        prompt = st.text_input("Describe your need (e.g. privacy for HR data):")
        st.button("Generate Draft")

    with tab5:
        st.subheader("Saved Drafts")
        st.dataframe({"Draft": ["HR Policy", "Marketing Policy"], "Last Modified": ["2025-05-10", "2025-05-01"]})

# --- Policy Compliance Checker ---
elif menu == "Policy Compliance Checker":
    #st.title("Match Policy to DPDPA")
    st.markdown("<h1 style='font-size:38px; font-weight:800;'>Match Policy to DPDPA</h1>", unsafe_allow_html=True)
    
    #st.header("1. Upload Your Policy Document")
    st.markdown("<h3 style='font-size:24px; font-weight:700;'>1. Upload Your Policy Document</h3>", unsafe_allow_html=True)
    upload_option = st.radio("Choose input method:", ["Upload File", "Paste Policy Text"], index=0)
    if upload_option == "Upload File":
        policy_file = st.file_uploader("Upload .docx or .txt file", type=["docx", "txt"])
        policy_text = None
    else:
        policy_text = st.text_area("Paste your policy text here:", height=250)
        policy_file = None

    #st.header("2. Choose Matching Level")
    st.markdown("<h3 style='font-size:24px; font-weight:700;'>2. Choose Matching Level</h3>", unsafe_allow_html=True)
    match_level = st.radio("How do you want to match?", [
        "Document-level Match (default)", "Clause-level Match"], index=0)

    #st.header("3. Select Scope of Evaluation")
    st.markdown("<h3 style='font-size:24px; font-weight:700;'>3. Select Scope of Evaluation</h3>", unsafe_allow_html=True)
    scope = st.selectbox("", [
        "DPDP Act 2023 (default)", "DPDP Rules 2025", "DPDP Act + Rules", "Custom Sections"], index=0)
    if scope == "Custom Sections":
        custom_sections = st.multiselect("Select specific sections to match against", [
        "Section 4 — Grounds for Processing Personal Data", "Section 5 — Notice", "Section 6 — Consent", "Section 7 — Certain Legitimate Uses",
        "Section 8 — General Obligations of Data Fiduciary", "Section 9 — Processing of Personal Data of Children", "Section 10 — Additional Obligations of Significant Data Fiduciaries"])
    else:
        custom_sections = []

    #st.header("4. Industry Context (Optional)")
    st.markdown("<h3 style='font-size:24px; font-weight:700;'>4. Industry Context (Optional)</h3>", unsafe_allow_html=True)
    industry = st.selectbox("", ["General", "Automotive", "Healthcare", "Fintech", "Other"])
    if industry == "Other":
        custom_industry = st.text_input("Specify your industry")
    else:
        custom_industry = None

    #st.header("5. Run Compliance Check")
    st.markdown("<h3 style='font-size:24px; font-weight:700;'>5. Run Compliance Check</h3>", unsafe_allow_html=True)
    if st.button("Run Compliance Check"):
        if policy_file or policy_text:
            with st.spinner("Running GPT-based compliance evaluation..."):
                st.success("Compliance check complete.")
                st.metric("Overall Compliance", "78%")
                st.markdown("""
                ### Clause-wise Evaluation:
                - **Section 5 (Notice):** ✅ Matched
                - **Section 7 (Children’s Data):** ❌ Missing Guardian Consent Clause
                - **Section 9 (Breach):** ⚠️ Breach timeline undefined
                """)
        else:
            st.warning("Please upload a file or paste policy text.")

    #st.header("6. Generate / Export Output")
    st.markdown("<h3 style='font-size:24px; font-weight:700;'>6. Generate / Export Output</h3>", unsafe_allow_html=True)
    export_format = st.selectbox("Choose export format", ["PDF", "CSV", "JSON"])
    if st.button("Download Output"):
        st.success("Export ready (simulated). File will include compliance results and recommendations.")

# --- Dashboard & Reports ---
elif menu == "Dashboard & Reports":
    st.title("Dashboard & Reports")
    st.metric("Overall Compliance", "82%", "+7%")
    st.progress(0.82)
    st.subheader("Risk & GPT Insights")
    st.write("\n- Consent missing in 2 sections\n- Breach response undefined\n")
    st.subheader("Activity Tracker")
    st.dataframe({"Task": ["Upload Policy", "Review Results"], "Status": ["Done", "Pending"]})
    st.download_button("Download Full Report", "Sample Report Data...", file_name="dpdpa_report.txt")

# --- Knowledge Assistant ---
elif menu == "Knowledge Assistant":
    st.title("Knowledge Assistant")
    with st.expander("📘 DPDPA + DPDP Rules Summary"):
        st.markdown("Digital Personal Data Protection Act focuses on consent, purpose limitation, etc.")
    with st.expander("📖 Policy Glossary"):
        st.write({"Data Principal": "The individual to whom personal data relates."})
    with st.expander("🔍 Clause-by-Clause Reference"):
        st.markdown("Section 5: Notice - Clear, itemised, accessible...")
    with st.expander("🆘 Help Centre"):
        st.write("Email: support@dpdpatool.com | Call: +91-XXX-XXX")

# --- Admin Settings ---
elif menu == "Admin Settings":
    st.title("Admin Settings")
    st.subheader("User & Role Management")
    st.write("Admin | Reviewer | Editor")
    st.subheader("Organization Profile")
    st.text_input("Organization Name")
    st.text_input("Sector")
    st.subheader("Audit Log Controls")
    st.checkbox("Enable audit logs")
    st.subheader("Data Backup & Export")
    st.button("Download Backup")
