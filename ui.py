import streamlit as st

import openai
import json
import pandas as pd
import re
def sent_tokenize(text):
    """A basic fallback sentence tokenizer using regex."""
    text = text.replace("\n", " ")
    return re.split(r'(?<=[.!?]) +', text)


# --- OpenAI Setup ---
api_key = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI(api_key=api_key)

# --- DPDPA Sections ---
dpdpa_sections = [
    "Section 4 — Grounds for Processing Personal Data",
    "Section 5 — Notice",
    "Section 6 — Consent",
    "Section 7 — Certain Legitimate Uses",
    "Section 8 — General Obligations of Data Fiduciary"
]

# --- DPDPA Legal Text ---
dpdpa_chapter_text = """CHAPTER II
OBLIGATIONS OF DATA FIDUCIARY

Section 4. Grounds for processing personal data.
Sub-section (1) of Section 4. -  A person may process the personal data of a Data Principal only in accordance with the provisions of this Act and for a lawful purpose—
  (a) for which the Data Principal has given her consent; or
  (b) for certain legitimate uses.

Sub-section (2) of Section 4. -  For the purposes of this section, the expression “lawful purpose” means any purpose which is not expressly forbidden by law.

Section 5. Notice.
Sub-section (1) of Section 5. - Every request made to a Data Principal under section 6 for consent shall be accompanied or preceded by a notice given by the Data Fiduciary to the Data Principal, informing her—
  (i) the personal data and the purpose for which the same is proposed to be processed;
  (ii) the manner in which she may exercise her rights under sub-section (4) of section 6 and section 13; and
  (iii) the manner in which the Data Principal may make a complaint to the Board, in such manner and as may be prescribed.

Sub-section (2) of Section 5. - Where a Data Principal has given her consent for processing personal data before the commencement of this Act—
  (a) the Data Fiduciary shall, as soon as reasonably practicable, give the Data Principal a notice with the above information;
  (b) the Data Fiduciary may continue processing unless the Data Principal withdraws her consent.

Sub-section (3) of Section 5. - The Data Fiduciary shall provide the notice in English or any language under the Eighth Schedule of the Constitution.

Section 6. Consent.
Sub-section (1) of Section 6. - Consent shall be free, specific, informed, unconditional, unambiguous, and signify agreement by clear affirmative action, limited to necessary personal data for the specified purpose.

Sub-section (2) of Section 6. - Any infringing part of consent shall be invalid to the extent of infringement.

Sub-section (3) of Section 6. - Every consent request must be in clear and plain language, accessible in English or Eighth Schedule languages, with Data Protection Officer contact where applicable.

Sub-section (4) of Section 6. - Data Principals can withdraw consent anytime, with ease comparable to giving consent.

Sub-section (5) of Section 6. - Withdrawal consequences must be borne by the Data Principal and do not affect prior lawful processing.

Sub-section (6) of Section 6. - After withdrawal, Data Fiduciaries and Processors must cease processing unless otherwise required by law.

Sub-section (7) of Section 6. - Consent can be managed through a Consent Manager registered with the Board.

Sub-section (8) of Section 6. - Consent Managers act on behalf of Data Principals and are accountable to them.

Sub-section (9) of Section 6. - Consent Managers must be registered as prescribed.

Sub-section (10) of Section 6. - Data Fiduciary must prove that notice was given and consent was valid, if challenged.

Section 7. Certain legitimate uses.
Personal data may be processed without consent for:
  (a) Voluntarily provided personal data for specified purposes without expressed objection.
  (b) Subsidy, benefit, certificate, etc., provided by the State.
  (c) Performance of State functions or in the interest of sovereignty, integrity, or security.
  (d) Legal obligations to disclose information.
  (e) Compliance with court orders or judgments.
  (f) Medical emergencies.
  (g) Public health emergencies.
  (h) Disaster situations.
  (i) Employment purposes like corporate espionage prevention.

Section 8. General obligations of Data Fiduciary.
Sub-section (1) of Section 8. - Data Fiduciary is responsible for compliance regardless of agreements with Processors.

Sub-section (2) of Section 8. - Data Fiduciary may engage Processors only under valid contracts.

Sub-section (3) of Section 8. - If personal data is used for decisions affecting Data Principals or disclosed, ensure completeness, accuracy, and consistency.

Sub-section (4) of Section 8. - Implement technical and organisational measures to ensure compliance.

Sub-section (5) of Section 8. - Protect personal data using reasonable security safeguards against breaches.

Sub-section (6) of Section 8. - Notify the Board and affected Data Principals in case of breaches, as prescribed.

Sub-section (7) of Section 8. - Erase personal data upon withdrawal of consent or when the specified purpose is no longer served, unless legally required to retain.

Sub-section (8) of Section 8. - "Specified purpose no longer served" deemed if Data Principal does not approach the Fiduciary within prescribed time.

Sub-section (9) of Section 8. - Publish business contact info of DPO or designated grievance redressal officer.

Sub-section (10) of Section 8. - Establish an effective grievance redressal mechanism.

Sub-section (11) of Section 8. - Clarification: lack of contact by Data Principal within time period implies specified purpose is no longer served.

"""
def validate_matches(gpt_output, policy_text):
    """Check that all GPT-claimed matched sentences exist in the actual policy."""
    for item in gpt_output["Checklist Items"]:
        valid_sentences = []
        for sentence in item["Matched Sentences"]:
            if sentence in policy_text:
                valid_sentences.append(sentence)
        if not valid_sentences:
            item["Matched"] = False
            item["Matched Sentences"] = []
            item["Justification"] = (
                "Original sentence not found in policy. Marked as unmatched."
            )
    return gpt_output


# --- Section 6 Checklist ---
section_6_checklist = [
    "Consent is free, specific, informed, unconditional, and unambiguous.",
    "Consent is given via clear affirmative action.",
    "Consent is limited to specified purpose only.",
    "Consent can be withdrawn at any time.",
    "Data Fiduciary shall cease processing upon withdrawal (unless legally required).",
    "Consent Manager is registered and functions independently.",
    "Consent Manager allows giving, managing, and withdrawing consent easily.",
    "Consent Manager logs consent history for audit.",
    "Data Fiduciary must honor withdrawal requests promptly.",
    "Retention of personal data stops unless required by law."
]

# --- Sentence-wise GPT match function ---
def match_sentence_to_checklist(sentence, checklist_items):
    prompt = f"""
You are a DPDPA compliance analyst. Your job is to determine whether the following policy sentence fulfills any obligations listed under Section 6 of the DPDPA (Consent and Its Management).

---

**Policy Sentence:**
\"{sentence}\"

---

**Checklist Items:**
{chr(10).join([f"{i+1}. {item}" for i, item in enumerate(checklist_items)])}

---

**Important Instructions:**

1. Match ONLY if the sentence **explicitly** refers to the checklist item using clear legal language.
2. **DO NOT** infer, imply, interpret user behavior, or stretch meaning.
3. DO NOT mark a sentence as a match if it:
   - Merely describes UI/UX behavior (e.g., “you can save preferences”) without explicitly referencing **consent** or legal control.
   - Vaguely discusses data collection without mentioning **consent**, **affirmative action**, **withdrawal**, or **data principal control**.
   - Contains generic statements like “we collect data to improve services” or “we store information”.

4. Match ONLY IF:
   - The sentence clearly mentions: consent, withdrawal, specified purpose, unambiguous agreement, consent manager, etc.
   - The sentence reflects a **policy-level commitment**, not just a description of technical functionality.

Only count a checklist item as matched if the sentence **explicitly and unambiguously** addresses the legal obligation — either through exact terminology or unmistakable legal phrasing.

DO NOT match if:
- The sentence **implies** or **suggests** compliance without clearly stating it.
- It refers to **data/account controls** but does not mention **consent or legal intent**.
- It discusses user actions (e.g., “signing up”, “saving preferences”, “contacting support”) without framing them as part of **consent management**.
- The term “consent” or a legal synonym (e.g., “authorization”, “agreement”, “permission”) is **not present**, and the legal obligation is not unmistakably addressed.

---

**Examples that should NOT be matched:**
- “Users can delete data from their account” → ❌ Not equivalent to consent withdrawal.
- “We collect information when you use our services” → ❌ Does not indicate clear affirmative action.
- “You may adjust your settings” → ❌ Too vague to imply informed consent or legal control.

---

✅ Match only when the legal requirement is **explicit**, **contextually precise**, and **linguistically unambiguous**.

> **Ask yourself for each match:**  
> “Would a data protection auditor accept this as proof of compliance for this clause?”  
> If the answer is “maybe” or “only if interpreted generously,” then the item should **NOT** be marked as matched.

---

Please return your response strictly in the following JSON format:

{{
  "Matched Items": [
    {{
      "Checklist Item": "...",
      "Justification": "..."
    }}
  ]
}}

If no checklist item is clearly satisfied, return: "Matched Items": []
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return json.loads(response.choices[0].message.content)



# --- Full analyzer using sentence loop for Section 6 only ---
def analyze_policy_section6(policy_text):
    import re
    from collections import defaultdict

    # Enhanced sentence tokenizer
    def sent_tokenize(text):
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        text = re.sub(r'\n+', '\n', text)
        paragraphs = text.split('\n')
        sentences = []
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            if re.search(r'[a-zA-Z0-9]{3,}', para):
                sentences += re.split(r'(?<=[.!?]) +', para)
            else:
                sentences.append(para)
        return [s.strip() for s in sentences if s.strip()]

    # Checklist with IDs
    section_6_checklist = [
        {"id": "6.1", "item": "Consent is free, specific, informed, unconditional, and unambiguous."},
        {"id": "6.2", "item": "Consent is given via clear affirmative action."},
        {"id": "6.3", "item": "Consent is limited to specified purpose only."},
        {"id": "6.4", "item": "Consent can be withdrawn at any time."},
        {"id": "6.5", "item": "Data Fiduciary shall cease processing upon withdrawal (unless legally required)."},
        {"id": "6.6", "item": "Consent Manager is registered and functions independently."},
        {"id": "6.7", "item": "Consent Manager allows giving, managing, and withdrawing consent easily."},
        {"id": "6.8", "item": "Consent Manager logs consent history for audit."},
        {"id": "6.9", "item": "Data Fiduciary must honor withdrawal requests promptly."},
        {"id": "6.10", "item": "Retention of personal data stops unless required by law."}
    ]

    def build_sentence_prompt(sentence, checklist_items):
        checklist_str = "\n".join([f"{item['id']}. {item['item']}" for item in checklist_items])
        return f"""
You are a DPDPA Section 6 compliance analyst. Analyze the sentence below for matches against the checklist.

SENTENCE:
\"{sentence}\"

CHECKLIST:
{checklist_str}

RULES:
- Match ONLY if the sentence explicitly and clearly addresses the checklist item in legal terms.
- Do NOT infer meaning, interpret behavior, or rely on vague wording.
- Only match if the meaning is clear, contextual, and unambiguous.
- For each match, include:
  - checklist ID
  - full checklist text
  - justification
  - whether it is a 'full' or 'partial' match

OUTPUT FORMAT (JSON):
{{
  "Sentence": "...",
  "Matched Items": [
    {{
      "Checklist ID": "...",
      "Checklist Text": "...",
      "Justification": "...",
      "Match Type": "full" or "partial"
    }}
  ]
}}

If no match, return:
{{
  "Sentence": "...",
  "Matched Items": []
}}
"""

    def call_gpt(prompt):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return json.loads(response.choices[0].message.content)

    sentences = sent_tokenize(policy_text)
    all_sentence_matches = []

    for sentence in sentences:
        if len(sentence.split()) < 5:
            continue
        prompt = build_sentence_prompt(sentence, section_6_checklist)
        result = call_gpt(prompt)
        all_sentence_matches.append(result)

    checklist_to_sentences = defaultdict(list)
    for entry in all_sentence_matches:
        for match in entry["Matched Items"]:
            checklist_to_sentences[match["Checklist ID"]].append({
                "Sentence": entry["Sentence"],
                "Justification": match["Justification"],
                "Match Type": match["Match Type"]
            })

    final_output = []
    for item in section_6_checklist:
        checklist_id = item["id"]
        matches = checklist_to_sentences.get(checklist_id, [])
        final_output.append({
            "Checklist ID": checklist_id,
            "Checklist Text": item["item"],
            "Matched Sentences": [m["Sentence"] for m in matches],
            "Justifications": [m["Justification"] for m in matches],
            "Match Types": [m["Match Type"] for m in matches],
            "Status": "Matched" if matches else "Unmatched",
            "Suggested Rewrite": "" if matches else f"Add clear policy line addressing: {item['item']}"
        })

    matched_count = sum(1 for row in final_output if row["Status"] == "Matched")
    total_items = len(section_6_checklist)
    if matched_count == total_items:
        match_level, score, severity = "Fully Compliant", 1.0, "N/A"
    elif matched_count == 0:
        match_level, score, severity = "Non-Compliant", 0.0, "Major"
    elif matched_count == 1:
        match_level, score, severity = "Partially Compliant", 0.75, "Minor"
    elif matched_count <= 3:
        match_level, score, severity = "Partially Compliant", 0.5, "Medium"
    else:
        match_level, score, severity = "Partially Compliant", 0.25, "Major"

    return {
        "DPDPA Section": "Section 6 — Consent",
        "DPDPA Section Meaning": "This section outlines how organizations must obtain, manage, and revoke consent from data principals under the DPDPA.",
        "Checklist Items Matched": [row["Checklist ID"] for row in final_output if row["Status"] == "Matched"],
        "Matched Sentences": final_output,
        "Match Level": match_level,
        "Severity": severity,
        "Compliance Points": score,
        "Suggested Rewrite": "\n".join([row["Suggested Rewrite"] for row in final_output if row["Status"] == "Unmatched"])
    }



# --- GPT Function ---
def analyze_section(section_text, policy_text, full_chapter_text):
    prompt = f"""You are a DPDPA compliance expert. Your task is to assess whether an organization's policy complies with the Digital Personal Data Protection Act, 2023 (India) — specifically Sections 4 to 8 under Chapter II. 

To do this you must follow the "INSTRUCTIONS" given below. Focus only on current section for now.
You must base your analysis only on the DPDPA section under review. Do not bring in requirements from other DPDPA sections or rules unless explicitly instructed.
==========================================================
ORGANIZATION POLICY:
\"\"\"{policy_text}\"\"\"

DPDPA SECTION UNDER REVIEW:
\"\"\"{section_text}\"\"\"

==========================================================
INSTRUCTIONS:

1. **Understand the Law in Simple Terms**
   - Read the DPDPA Section carefully and explain it in your own words in simple, layman-friendly language.
   - Capture *every important legal requirement* from the section.

2. **Checklist Mapping**
   - Refer to the official checklist of obligations provided for this section. Only use the checklist below. Do not create or infer new checklist items. If a point is not in the checklist, ignore it even if it appears legally relevant.
   - For each checklist item do following- 
      - Go through the policy *sentence by sentence* and see if that sentence addresses the checklist item.
      - Each checklist item must be matched to one or more specific sentences individually. Do not combine multiple unrelated statements to justify a match.
      - **Only count an item as covered if it is explicitly and clearly mentioned in the policy with correct context. Vague, generic, or partial references must be marked as unmatched. Do not assume implied meaning — legal clarity is required.**
      - Before confirming a match, verify that the sentence appears verbatim in the policy text above.
      - Do not make assumptions or stretch interpretations.
      - Do not assume that generic statements (e.g., "we improve services") imply security, consent, breach notifications, etc.
      - Only match if the sentence **explicitly and clearly refers** to the legal requirement in the checklist.
      - If a sentence does **not** clearly mention keywords like “security,” “data breach,” “firewall,” “encryption,” or similar — it should **not** be matched for a checklist item about breach safeguards.
      - Every matched checklist item must cite the exact sentence(s) from the policy verbatim.
      - This needs to be shown in the output - "Checklist Items" - In this -  mention the checklist item, whether it matches or not, the sentence/s from policy to which this checklist item matches and what is the justification for it getting matched.
      - If no sentence exactly matches, mark the item as Matched: false.
      - You will be penalized if you claim a sentence exists in the policy when it does not. If unsure, leave Matched Sentences blank and set Matched: false.

3. **Classification**
   - Match Level:
     - "Fully Compliant": All checklist items are covered clearly.
     - "Partially Compliant": At least one item is missing or only vaguely mentioned.
     - "Non-Compliant": No checklist item is covered.
   - Severity (only for Partially Compliant):
     - Minor = 1 missing item
     - Medium = 2–3 missing items
     - Major = 4 or more missing / any critical clause missing
   - Compliance Points:
     - Fully Compliant = 1.0
     - Partially Compliant:
        - Minor = 0.75
        - Medium = 0.5
        - Major = 0.25
     - Non-Compliant = 0.0

4. **Suggested Rewrite**
   - This is an extremely important step so do this properly. For the section do the following points - 
      - Review the **checklist** for this section again and identify which items are **missing** from the policy.
      - For each missing item, write **1 sentence** that can be added to the policy to ensure compliance.
      - The rewrite should be a clear, implementable policy statement for each missing item.
      - Do not recommend additions beyond the missing checklist items. Rewrites should strictly address only those gaps.
==========================================================
OUTPUT FORMAT (strict JSON):
{{
  "DPDPA Section": "...",
  "DPDPA Section Meaning": "...",
  "Checklist Items": [
    {{
      "Item": "...",
      "Matched": true/false,
      "Matched Sentences": [ "Each sentence listed here **must appear exactly** in the policy text above. Do not invent or paraphrase any line. If unsure or if no exact sentence is found, leave this blank."],
      "Justification": "..."
    }},
    ...
  ],
  "Match Level": "...",
  "Severity": "...",
  "Compliance Points": "...",
  "Suggested Rewrite": "..."
}}

==========================================================
CHECKLIST TO USE:


**Section 4: Grounds for Processing Personal Data**

1. ☐ Personal data is processed **only** for lawful purposes.
2. ☐ Lawful purpose must be:

   * ☐ Backed by **explicit consent** from the Data Principal **OR**
   * ☐ Falls under **legitimate uses** as per Section 7.
3. ☐ Lawful purpose must **not be expressly forbidden** by any law.

**Section 5: Notice Before Consent**

1. ☐ Notice is provided **before or at the time** of requesting consent.
2. Notice must clearly mention:

   * ☐ What **personal data** is being collected.
   * ☐ The **purpose** of processing.
   * ☐ How to **exercise rights** under Section 6(4) and Section 13.
   * ☐ How to **lodge complaints** with the Board.
3. ☐ For existing data collected **before DPDPA**, retrospective notice must also be issued as soon as practicable with all points above.

**Section 6: Consent and Its Management**

1. ☐ Consent is **free, specific, informed, unconditional, and unambiguous**.
2. ☐ Consent is **given via clear affirmative action**.
3. ☐ Consent is **limited to specified purpose only**.
4. ☐ Consent can be **withdrawn** at any time.
5. ☐ Data Fiduciary shall **cease processing** upon withdrawal (unless legally required).
6. ☐ Consent Manager is available (if applicable):

   * ☐ Consent Manager is **registered** and functions independently.
   * ☐ Consent Manager allows:

     * ☐ Giving, managing, and withdrawing consent easily.
     * ☐ Logs consent history for audit.
7. ☐ Data Fiduciary must honor withdrawal requests promptly.
8. ☐ Retention of personal data stops unless required by law.

**Section 7: Legitimate Uses (No Consent Needed)**

Processing without consent is allowed **only** if it meets the following (tick applicable):

* ☐ For specified government subsidies/services/licenses.
* ☐ For State functions (e.g., national security, law enforcement).
* ☐ To comply with legal obligations.
* ☐ Under court orders or judgments.
* ☐ For medical emergencies or disasters.
* ☐ For employment-related purposes with safeguards.
* ☐ For corporate security or internal fraud prevention.
  Each use must:

  * ☐ Be **necessary** and **proportionate**.
  * ☐ Adhere to standards/rules to be prescribed.

**Section 8: General Obligations of Data Fiduciary**

1. ☐ Fiduciary is fully accountable for processing by itself or its Data Processor.
2. ☐ Processing must be under a valid **contract** with the Data Processor.
3. ☐ If data is to:

   * ☐ Influence decisions or
   * ☐ Be shared with other Fiduciaries,
     → Then data must be:

     * ☐ Complete
     * ☐ Accurate
     * ☐ Consistent
4. ☐ Implement **technical and organisational measures** for compliance.
5. ☐ Take **reasonable security safeguards** to prevent breaches.
6. ☐ Report data breaches to:

   * ☐ Data Protection Board
   * ☐ Affected Data Principals
7. ☐ Erase data when:

   * ☐ Consent is withdrawn, OR
   * ☐ Purpose is no longer being served
   * ☐ Also instruct Data Processor to erase it.
8. ☐ Define time periods for retention based on inactivity of Data Principal.
9. ☐ Publish business contact info of DPO or responsible officer.
10. ☐ Establish a grievance redressal mechanism."""
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content


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

    /* Force DataFrame cell background and text to be readable */
.css-1r6slb0 .element-container {
        background-color: white !important;
        color: black !important;
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
        "Section 8 — General Obligations of Data Fiduciary"])
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
        if policy_text:
            results = []
            with st.spinner("Running GPT-based compliance evaluation..."):
                for section in dpdpa_sections:
                    st.markdown(f"##### Analyzing: {section}")
                    try:
                        if section == "Section 6 — Consent":
                            validated_section = analyze_policy_section6(policy_text)
                            results.append(validated_section)
                        else:
                            section_response = analyze_section(section, policy_text, dpdpa_chapter_text)
                            parsed_section = json.loads(section_response)
                            validated_section = validate_matches(parsed_section, policy_text)
                            results.append(validated_section)

                        st.success(f"✅ Completed: {section}")

                    except Exception as e:
                        st.error(f"❌ Error analyzing {section}: {e}")
    
            st.markdown("---")
            if results:
                # Flatten results for table display (avoid [object Object])
                flat_data = []
                for row in results:
                    flat_data.append({
                        "DPDPA Section": row.get("DPDPA Section", ""),
                        "Meaning": row.get("DPDPA Section Meaning", "Not applicable"),
                        "Match Level": row.get("Match Level", ""),
                        "Severity": row.get("Severity", ""),
                        "Score": row.get("Compliance Points", row.get("Compliance Score", ""))
                    })

                df = pd.DataFrame(flat_data)
            
                # Display clean table
                st.success("✅ Full Analysis Complete!")
                st.dataframe(df.style.set_properties(**{
                    'background-color': 'white',
                    'color': 'black'
                }))
            
                # Show detailed expanders
                # Show detailed expanders
                for row in results:
                    with st.expander(f"🔍 {row['DPDPA Section']} — Full Checklist & Suggestions"):
                        if row['DPDPA Section'] == "Section 6 — Consent" and "Checklist Items" not in row:
                            # st.markdown(f"**Match Level:** {row['Match Level']} | **Score:** {row['Compliance Score']}")
                            st.markdown(f"**Match Level:** {row.get('Match Level', '')} | **Score:** {row.get('Compliance Points', row.get('Compliance Score', 'N/A'))}")
                            st.markdown("**Matched Checklist Items:**")
                            for item in row["Checklist Items Matched"]:
                                st.markdown(f"- ✅ {item}")
                            st.markdown("**Matched Sentences & Justifications:**")
                            for s in row["Matched Sentences"]:
                                st.markdown(f"- **Sentence:** {s['Sentence']}")
                                st.markdown(f"  - **Checklist Item:** {s['Checklist Item']}")
                                st.markdown(f"  - **Justification:** {s['Justification']}")
                        else:
                            st.markdown(f"**Meaning:** {row['DPDPA Section Meaning']}")
                            st.markdown(f"**Match Level:** {row['Match Level']} | **Severity:** {row.get('Severity', '')}")
                            st.markdown("**Checklist Items:**")
                            for item in row["Checklist Items"]:
                                st.markdown(f"- **{item['Item']}** → Matched: **{item['Matched']}**")
                                st.markdown(f"  - Sentences: {item['Matched Sentences']}")
                                st.markdown(f"  - Justification: {item['Justification']}")
                            st.markdown("**Suggested Rewrite:**")
                            st.markdown(row["Suggested Rewrite"])

            
                # Excel Download
                excel_filename = "DPDPA_Compliance_Report.xlsx"
                df.to_excel(excel_filename, index=False)
                with open(excel_filename, "rb") as f:
                    st.download_button("📥 Download Excel", f, file_name=excel_filename)
            
                # Score
                try:
                    scored_points = df['Score'].astype(float).sum()
                    total_points = len(dpdpa_sections)
                    score = (scored_points / total_points) * 100
                    st.metric("🎯 Overall Compliance", f"{score:.2f}%")
                except:
                    st.warning("⚠️ Could not compute score. Check data types.")

        else:
            st.warning("⚠️ Please paste policy text to proceed.")

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
