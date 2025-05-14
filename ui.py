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

section_4_checklist = [
    "Personal data is processed only for a lawful purpose.",
    "Lawful purpose means a purpose not expressly forbidden by law.",
    "Lawful purpose must be backed by explicit consent from the Data Principal or fall under legitimate uses.",
]
section_5_checklist = [
    "A notice is given before or at the time of requesting consent.",
    "Notice clearly mentions what personal data is being collected.",
    "Notice clearly mentions the purpose for which the personal data is proposed to be processed.",
    "Notice describes how the Data Principal can exercise her rights under Section 6(4) and Section 13.",
    "Notice explains how the Data Principal can file a complaint with the Data Protection Board.",
    "For data collected before commencement of the Act, retrospective notice is given as soon as reasonably practicable.",
    "Retrospective notice includes: data processed, purpose, rights under Section 6(4) and 13, and complaint mechanism.",
    "Data Fiduciary may continue processing pre-Act personal data until consent is withdrawn.",
    "Notice must be available in English or any language under the Eighth Schedule of the Constitution."
]

# --- Section 6 Checklist ---
section_6_checklist = [
    # A. Nature and Validity of Consent (Section 6(1))
    "Consent is free — voluntarily given, not coerced or forced.",
    "Consent is specific to a clearly defined purpose.",
    "Consent is informed — based on full disclosure before collection.",
    "Consent is unconditional — not bundled with unrelated terms.",
    "Consent is unambiguous — clear in intent and meaning.",
    "Consent is given through clear affirmative action (e.g., ticking a box, clicking 'I agree').",
    "Consent is limited strictly to the specified purpose.",
    "Only personal data necessary for the specified purpose is processed.",

    # B. Consent Request Requirements (Section 6(3))
    "Consent request is written in clear and plain language.",
    "Consent request is available in English or one of the 22 Eighth Schedule languages.",
    "Consent request includes contact details of the Data Protection Officer (DPO) or authorized representative.",

    # C. Legal Integrity of Consent (Section 6(2))
    "Any clause in the consent request that infringes on the Act is void to that extent.",

    # D. Withdrawal and Post-Withdrawal Compliance (Section 6(4), 6(5), 6(6))
    "Consent can be withdrawn at any time by the Data Principal.",
    "Consequences of withdrawal (e.g., loss of service) are borne by the Data Principal.",
    "Withdrawal does not affect the legality of processing done before the withdrawal.",
    "Processing of personal data must stop upon withdrawal, unless legally mandated to continue.",

    # E. Consent Manager Requirements (Section 6(7), 6(8), 6(9))
    "Consent can be given, managed, and withdrawn through a Consent Manager.",
    "Consent Manager acts on behalf of the Data Principal and is accountable to them.",
    "Consent Manager is registered with the Data Protection Board of India.",
    "Consent Manager enables easy management of consent (granting, auditing, withdrawing).",

    # F. Record-Keeping and Proof of Validity (Section 6(10))
    "Data Fiduciary must demonstrate that valid notice was provided to the Data Principal.",
    "Data Fiduciary must prove that consent was validly obtained."
]
section_7_checklist = [
    "Personal data is processed without consent only if it falls within specific legal grounds under Section 7.",
    "Each legitimate use must be necessary, proportionate, and in accordance with applicable laws or standards.",

    # (a) Voluntary Provision
    "Data Principal voluntarily provided personal data for a specified purpose and did not object to its use for that purpose.",

    # (b) State-Issued Subsidies/Benefits
    "Processing is done by the State or its instrumentalities to issue a subsidy, benefit, service, certificate, licence or permit.",
    "Data Principal has previously consented for such processing by the State or its instrumentalities.",
    "Personal data is sourced from officially maintained registers or databases and notified by the Central Government.",
    "Processing follows standards or policies notified by the Central Government or law for personal data governance.",

    # (c) State Function
    "Processing is necessary for the performance of any legal function by the State or its instrumentalities related to sovereignty, integrity, or security of India.",

    # (d) Statutory Obligation
    "Processing is required under any law for disclosing information to the State or its instrumentalities, subject to applicable provisions.",

    # (e) Court Order
    "Processing is required to comply with a judgment, decree, or order under Indian or foreign law related to civil or contractual claims.",

    # (f) Medical Emergency
    "Processing is required to respond to a medical emergency involving threat to life or health of the Data Principal or another person.",

    # (g) Epidemic or Public Health
    "Processing is required to provide medical treatment or health services during an epidemic, outbreak, or other public health threat.",

    # (h) Disaster or Public Order
    "Processing is required to ensure safety or provide assistance or services during a disaster or public order breakdown.",
    "Disaster is as defined under clause (d) of Section 2 of the Disaster Management Act, 2005.",

    # (i) Employment-Related Purposes
    "Processing is necessary for employment-related purposes or to safeguard the employer from loss or liability.",
    "Examples include prevention of corporate espionage, protection of IP, or provision of services/benefits to employees."
]
section_8_checklist = [
    "Data Fiduciary is accountable for compliance with the Act even if processing is done by a Data Processor.",
    "Data Fiduciary may engage a Data Processor only under a valid contract.",
    "If personal data is used to make decisions about or is disclosed to another Fiduciary, ensure completeness, accuracy, and consistency.",
    "Implement appropriate technical and organisational measures to ensure compliance with the Act and rules.",
    "Ensure reasonable security safeguards to prevent personal data breaches.",
    "Notify the Board and affected Data Principals of a personal data breach in prescribed form and manner.",
    "Erase personal data upon withdrawal of consent or if the specified purpose is no longer being served, unless retention is legally required.",
    "Cause Data Processor to erase data shared with them once consent is withdrawn or purpose is no longer served.",
    "The purpose is deemed no longer served if the Data Principal does not approach the Fiduciary or exercise any rights for a prescribed time.",
    "Publish business contact details of the Data Protection Officer or responsible contact person.",
    "Establish an effective grievance redressal mechanism.",
    "Clarify that Data Principal inactivity implies purpose is no longer served (as per clause 8)."
]

# --- Sentence-wise GPT match function ---
    
def match_sentence_to_checklist4(sentence, checklist_items):
    prompt = f"""
    You are a DPDPA compliance expert. Your job is to determine whether the following policy sentence complies and fulfills any obligations listed under Section 4 (Grounds for Processing Personal Data) of the Digital Personal Data Protection Act, 2023 (India).

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
       
    Only count a checklist item as matched if the sentence **explicitly and unambiguously** addresses the legal obligation — either through exact terminology or unmistakable legal phrasing.
    
    DO NOT match if:
    - The sentence **implies** or **suggests** compliance without clearly stating it.
    
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


# --- Full analyzer using sentence loop for Section 4 only ---
def analyze_policy_section4(policy_text):
    policy_sentences = sent_tokenize(policy_text)
    match_results = []

    for sentence in policy_sentences:
        if len(sentence.strip().split()) < 5:  # Skip vague/short phrases
            continue
        result = match_sentence_to_checklist4(sentence, section_4_checklist)
        for match in result.get("Matched Items", []):
            match_results.append({
                "Sentence": sentence.strip(),
                "Checklist Item": match["Checklist Item"].strip(),
                "Justification": match["Justification"].strip()
            })

    # Deduplicate matched checklist items
    matched_items = {}
    for r in match_results:
        if r["Checklist Item"] not in matched_items:
            matched_items[r["Checklist Item"]] = r

    matched_count = len(matched_items)
    total_items = len(section_4_checklist)

    # Classification logic
    if matched_count == total_items:
        match_level = "Fully Compliant"
        points = 1.0
        severity = "N/A"
    elif matched_count == 0:
        match_level = "Non-Compliant"
        points = 0.0
        severity = "Major"
    elif matched_count == 1:
        match_level = "Partially Compliant"
        points = 0.75
        severity = "Minor"
    elif matched_count <= 3:
        match_level = "Partially Compliant"
        points = 0.5
        severity = "Medium"
    else:
        match_level = "Partially Compliant"
        points = 0.25
        severity = "Major"

    # Suggested Rewrites
    missing_items = [item for item in section_4_checklist if item not in matched_items]
    if missing_items:
        suggested_rewrite = "### Suggested Rewrite for Missing Items:\n" + \
            "\n".join([f"- Add this statement: *{item}*" for item in missing_items])
    else:
        suggested_rewrite = "All checklist items are covered."

    # Final Output
    final_output = {
        "DPDPA Section": "Section 4 — Grounds for Processing Personal Data",
        "DPDPA Section Meaning": "",
        "Checklist Items Matched": list(set(matched_items.keys())),
        "Matched Sentences": list(matched_items.values()),
        "Match Level": match_level,
        "Severity": severity,
        "Compliance Points": points,
        "Suggested Rewrite": suggested_rewrite
    }
    return final_output
def match_sentence_to_checklist5(sentence, checklist_items):
    prompt = f"""
    You are a DPDPA compliance expert. Your job is to determine whether the following policy sentence complies and fulfills any obligations listed under Section 5 (Notice) of the Digital Personal Data Protection Act, 2023 (India).

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
       
    Only count a checklist item as matched if the sentence **explicitly and unambiguously** addresses the legal obligation — either through exact terminology or unmistakable legal phrasing.
    
    DO NOT match if:
    - The sentence **implies** or **suggests** compliance without clearly stating it.
    
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


# --- Full analyzer using sentence loop for Section 4 only ---
def analyze_policy_section5(policy_text):
    policy_sentences = sent_tokenize(policy_text)
    match_results = []

    for sentence in policy_sentences:
        if len(sentence.strip().split()) < 5:  # Skip vague/short phrases
            continue
        result = match_sentence_to_checklist5(sentence, section_5_checklist)
        for match in result.get("Matched Items", []):
            match_results.append({
                "Sentence": sentence.strip(),
                "Checklist Item": match["Checklist Item"].strip(),
                "Justification": match["Justification"].strip()
            })

    # Deduplicate matched checklist items
    matched_items = {}
    for r in match_results:
        if r["Checklist Item"] not in matched_items:
            matched_items[r["Checklist Item"]] = r

    matched_count = len(matched_items)
    total_items = len(section_5_checklist)

    # Classification logic
    if matched_count == total_items:
        match_level = "Fully Compliant"
        points = 1.0
        severity = "N/A"
    elif matched_count == 0:
        match_level = "Non-Compliant"
        points = 0.0
        severity = "Major"
    elif matched_count == 1:
        match_level = "Partially Compliant"
        points = 0.75
        severity = "Minor"
    elif matched_count <= 3:
        match_level = "Partially Compliant"
        points = 0.5
        severity = "Medium"
    else:
        match_level = "Partially Compliant"
        points = 0.25
        severity = "Major"

    # Suggested Rewrites
    missing_items = [item for item in section_5_checklist if item not in matched_items]
    if missing_items:
        suggested_rewrite = "### Suggested Rewrite for Missing Items:\n" + \
            "\n".join([f"- Add this statement: *{item}*" for item in missing_items])
    else:
        suggested_rewrite = "All checklist items are covered."

    # Final Output
    final_output = {
        "DPDPA Section": "Section 5 — Notice",
        "DPDPA Section Meaning": "",
        "Checklist Items Matched": list(set(matched_items.keys())),
        "Matched Sentences": list(matched_items.values()),
        "Match Level": match_level,
        "Severity": severity,
        "Compliance Points": points,
        "Suggested Rewrite": suggested_rewrite
    }
    return final_output

def match_sentence_to_checklist6(sentence, checklist_items):
    prompt = f"""
    You are a DPDPA compliance expert. Your job is to determine whether the following policy sentence complies and fulfills any obligations listed under Section 6 (Consent and Its Management)of the Digital Personal Data Protection Act, 2023 (India).

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
    policy_sentences = sent_tokenize(policy_text)
    match_results = []

    for sentence in policy_sentences:
        if len(sentence.strip().split()) < 5:  # Skip vague/short phrases
            continue
        result = match_sentence_to_checklist6(sentence, section_6_checklist)
        for match in result.get("Matched Items", []):
            match_results.append({
                "Sentence": sentence.strip(),
                "Checklist Item": match["Checklist Item"].strip(),
                "Justification": match["Justification"].strip()
            })

    # Deduplicate matched checklist items
    matched_items = {}
    for r in match_results:
        if r["Checklist Item"] not in matched_items:
            matched_items[r["Checklist Item"]] = r

    matched_count = len(matched_items)
    total_items = len(section_6_checklist)

    # Classification logic
    if matched_count == total_items:
        match_level = "Fully Compliant"
        points = 1.0
        severity = "N/A"
    elif matched_count == 0:
        match_level = "Non-Compliant"
        points = 0.0
        severity = "Major"
    elif matched_count == 1:
        match_level = "Partially Compliant"
        points = 0.75
        severity = "Minor"
    elif matched_count <= 3:
        match_level = "Partially Compliant"
        points = 0.5
        severity = "Medium"
    else:
        match_level = "Partially Compliant"
        points = 0.25
        severity = "Major"

    # Suggested Rewrites
    missing_items = [item for item in section_6_checklist if item not in matched_items]
    if missing_items:
        suggested_rewrite = "### Suggested Rewrite for Missing Items:\n" + \
            "\n".join([f"- Add this statement: *{item}*" for item in missing_items])
    else:
        suggested_rewrite = "All checklist items are covered."

    # Final Output
    final_output = {
        "DPDPA Section": "Section 6 — Consent",
        "DPDPA Section Meaning": "This section outlines the requirements for obtaining and managing consent from data principals for the processing of their personal data.",
        "Checklist Items Matched": list(set(matched_items.keys())),
        "Matched Sentences": list(matched_items.values()),
        "Match Level": match_level,
        "Severity": severity,
        "Compliance Points": points,
        "Suggested Rewrite": suggested_rewrite
    }
    return final_output
    
def match_sentence_to_checklist7(sentence, checklist_items):
    prompt = f"""
    You are a DPDPA compliance expert. Your job is to determine whether the following policy sentence complies and fulfills any obligations listed under Section 7 (Certain Legitimate Uses) of the Digital Personal Data Protection Act, 2023 (India).

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
       
    Only count a checklist item as matched if the sentence **explicitly and unambiguously** addresses the legal obligation — either through exact terminology or unmistakable legal phrasing.
    
    DO NOT match if:
    - The sentence **implies** or **suggests** compliance without clearly stating it.
    
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
def analyze_policy_section7(policy_text):
    policy_sentences = sent_tokenize(policy_text)
    match_results = []

    for sentence in policy_sentences:
        if len(sentence.strip().split()) < 5:  # Skip vague/short phrases
            continue
        result = match_sentence_to_checklist7(sentence, section_7_checklist)
        for match in result.get("Matched Items", []):
            match_results.append({
                "Sentence": sentence.strip(),
                "Checklist Item": match["Checklist Item"].strip(),
                "Justification": match["Justification"].strip()
            })

    # Deduplicate matched checklist items
    matched_items = {}
    for r in match_results:
        if r["Checklist Item"] not in matched_items:
            matched_items[r["Checklist Item"]] = r

    matched_count = len(matched_items)
    total_items = len(section_7_checklist)

    # Classification logic
    if matched_count == total_items:
        match_level = "Fully Compliant"
        points = 1.0
        severity = "N/A"
    elif matched_count == 0:
        match_level = "Non-Compliant"
        points = 0.0
        severity = "Major"
    elif matched_count == 1:
        match_level = "Partially Compliant"
        points = 0.75
        severity = "Minor"
    elif matched_count <= 3:
        match_level = "Partially Compliant"
        points = 0.5
        severity = "Medium"
    else:
        match_level = "Partially Compliant"
        points = 0.25
        severity = "Major"

    # Suggested Rewrites
    missing_items = [item for item in section_7_checklist if item not in matched_items]
    if missing_items:
        suggested_rewrite = "### Suggested Rewrite for Missing Items:\n" + \
            "\n".join([f"- Add this statement: *{item}*" for item in missing_items])
    else:
        suggested_rewrite = "All checklist items are covered."

    # Final Output
    final_output = {
        "DPDPA Section": "Section 7 — Certain Legitimate Uses",
        "DPDPA Section Meaning": "",
        "Checklist Items Matched": list(set(matched_items.keys())),
        "Matched Sentences": list(matched_items.values()),
        "Match Level": match_level,
        "Severity": severity,
        "Compliance Points": points,
        "Suggested Rewrite": suggested_rewrite
    }
    return final_output
    
def match_sentence_to_checklist8(sentence, checklist_items):
    prompt = f"""
    You are a DPDPA compliance expert. Your job is to determine whether the following policy sentence complies and fulfills any obligations listed under Section 8 (General Obligations of Data Fiduciary) of the Digital Personal Data Protection Act, 2023 (India).

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
       
    Only count a checklist item as matched if the sentence **explicitly and unambiguously** addresses the legal obligation — either through exact terminology or unmistakable legal phrasing.
    
    DO NOT match if:
    - The sentence **implies** or **suggests** compliance without clearly stating it.
    
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
def analyze_policy_section8(policy_text):
    policy_sentences = sent_tokenize(policy_text)
    match_results = []

    for sentence in policy_sentences:
        if len(sentence.strip().split()) < 5:  # Skip vague/short phrases
            continue
        result = match_sentence_to_checklist8(sentence, section_8_checklist)
        for match in result.get("Matched Items", []):
            match_results.append({
                "Sentence": sentence.strip(),
                "Checklist Item": match["Checklist Item"].strip(),
                "Justification": match["Justification"].strip()
            })

    # Deduplicate matched checklist items
    matched_items = {}
    for r in match_results:
        if r["Checklist Item"] not in matched_items:
            matched_items[r["Checklist Item"]] = r

    matched_count = len(matched_items)
    total_items = len(section_8_checklist)

    # Classification logic
    if matched_count == total_items:
        match_level = "Fully Compliant"
        points = 1.0
        severity = "N/A"
    elif matched_count == 0:
        match_level = "Non-Compliant"
        points = 0.0
        severity = "Major"
    elif matched_count == 1:
        match_level = "Partially Compliant"
        points = 0.75
        severity = "Minor"
    elif matched_count <= 3:
        match_level = "Partially Compliant"
        points = 0.5
        severity = "Medium"
    else:
        match_level = "Partially Compliant"
        points = 0.25
        severity = "Major"

    # Suggested Rewrites
    missing_items = [item for item in section_8_checklist if item not in matched_items]
    if missing_items:
        suggested_rewrite = "### Suggested Rewrite for Missing Items:\n" + \
            "\n".join([f"- Add this statement: *{item}*" for item in missing_items])
    else:
        suggested_rewrite = "All checklist items are covered."

    # Final Output
    final_output = {
        "DPDPA Section": "Section 8 — General Obligations of Data Fiduciary",
        "DPDPA Section Meaning": "",
        "Checklist Items Matched": list(set(matched_items.keys())),
        "Matched Sentences": list(matched_items.values()),
        "Match Level": match_level,
        "Severity": severity,
        "Compliance Points": points,
        "Suggested Rewrite": suggested_rewrite
    }
    return final_output

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
                        if section == "Section 4 — Grounds for Processing Personal Data":
                            st.markdown(f"Inside if Analyzing: {section}")
                            validated_section = analyze_policy_section4(policy_text)
                            results.append(validated_section)
                        elif section == "Section 5 — Notice":
                            st.markdown(f"Inside if Analyzing: {section}")
                            validated_section = analyze_policy_section5(policy_text)
                            results.append(validated_section)
                        elif section == "Section 6 — Consent":
                            st.markdown(f"Inside if Analyzing: {section}")
                            validated_section = analyze_policy_section6(policy_text)
                            results.append(validated_section)
                        elif section == "Section 7 — Certain Legitimate Uses":
                            st.markdown(f"Inside if Analyzing: {section}")
                            validated_section = analyze_policy_section7(policy_text)
                            results.append(validated_section)
                        elif section == "Section 8 — General Obligations of Data Fiduciary":
                            st.markdown(f"Inside if Analyzing: {section}")
                            validated_section = analyze_policy_section8(policy_text)
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

                        elif row['DPDPA Section'] == "Section 4 — Grounds for Processing Personal Data" and "Checklist Items" not in row:
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
                        
                        elif row['DPDPA Section'] == "Section 5 — Notice" and "Checklist Items" not in row:
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
                        elif row['DPDPA Section'] == "Section 7 — Certain Legitimate Uses" and "Checklist Items" not in row:
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
                        elif row['DPDPA Section'] == "Section 8 — General Obligations of Data Fiduciary" and "Checklist Items" not in row:
                            # st.markdown(f"**Match Level:** {row['Match Level']} | **Score:** {row['Compliance Score']}")
                            st.markdown(f"**Match Level:** {row.get('Match Level', '')} | **Score:** {row.get('Compliance Points', row.get('Compliance Score', 'N/A'))}")
                            st.markdown("**Matched Checklist Items:**")
                            for item in row["Checklist Items Matched"]:
                                st.markdown(f"- ✅ {item}")
                            st.markdown("**Matched Sentences & Justifications:**")
                            for s in row["Matched Sentences"]:
                                st.markdown(f"- **Sentence:** {s['Sentence']}")
                                st.markdown(f"  - **Checklist Item:** {s['Checklist Item']}")
                                st.markdown(f"  - **Justification:** {s['Justification']}"

            
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
