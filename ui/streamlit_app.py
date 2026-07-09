from __future__ import annotations

import os

import requests
import streamlit as st


API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Clinical Research Synthesizer", layout="wide")
st.title("Clinical Research Synthesizer")

question = st.text_area("Clinical question", value="Should eligible adults with heart failure receive an SGLT2 inhibitor?", height=110)
require_approval = st.checkbox("Pause for clinician approval before adjudication", value=False)
approved = st.checkbox("Clinician approved adjudication", value=True)

if st.button("Run synthesis", type="primary"):
    with st.spinner("Running drafter, critic, and adjudicator agents..."):
        response = requests.post(
            f"{API_URL}/query",
            json={"question": question, "require_human_approval": require_approval, "approved": approved},
            timeout=120,
        )
    if response.ok:
        payload = response.json()
        st.metric("Confidence", payload.get("confidence"))
        st.subheader("Final answer")
        st.write(payload.get("answer"))
        st.subheader("Agent audit trail")
        st.json(payload.get("audit_log"))
        st.subheader("Citations")
        st.dataframe(payload.get("citations", []), use_container_width=True)
        st.subheader("Report")
        st.markdown(payload.get("report_markdown") or "")
    else:
        st.error(response.text)
