import json
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai

from prompts import FACT_EXTRACTION_PROMPT


# --------------------------------------------------
# Configuration
# --------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(
    page_title="Content Repurposing Chain",
    page_icon="🔄",
    layout="wide"
)

st.title("🔄 Content Repurposing Chain")

st.write(
    "Transform an article into a summary, LinkedIn post, "
    "and X/Twitter thread while preserving factual consistency."
)


# --------------------------------------------------
# API setup
# --------------------------------------------------

if not API_KEY:
    st.error(
        "GEMINI_API_KEY is not configured. "
        "Please add it to your .env file."
    )
    st.stop()

client = genai.Client(api_key=API_KEY)


# --------------------------------------------------
# Article input
# --------------------------------------------------

st.subheader("1️⃣ Source Article")

article = st.text_area(
    "Paste your article below",
    height=300,
    placeholder="Paste a factual article here..."
)


# --------------------------------------------------
# Fact extraction
# --------------------------------------------------

if st.button("🔍 Extract Facts", type="primary"):

    if not article.strip():
        st.error("Please enter an article before extracting facts.")
        st.stop()

    if len(article.strip()) < 100:
        st.warning(
            "The article is very short. Please provide a "
            "more complete article."
        )
        st.stop()

    with st.spinner("Extracting factual information..."):

        prompt = FACT_EXTRACTION_PROMPT.format(
            article=article
        )

        try:

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            raw_text = response.text.strip()

            # Remove Markdown code fences if the model adds them
            if raw_text.startswith("```"):
                raw_text = raw_text.replace("```json", "")
                raw_text = raw_text.replace("```", "")
                raw_text = raw_text.strip()

            facts = json.loads(raw_text)

        except json.JSONDecodeError:
            st.error(
                "The AI returned an invalid fact structure. "
                "Please try again."
            )
            st.stop()

        except Exception as e:
            st.error(f"AI request failed: {e}")
            st.stop()


    # --------------------------------------------------
    # Display Fact Ledger
    # --------------------------------------------------

    st.divider()

    st.subheader("2️⃣ Fact Ledger")

    categories = [
        ("People", "people"),
        ("Organizations", "organizations"),
        ("Dates", "dates"),
        ("Numbers", "numbers"),
        ("Amounts", "amounts"),
        ("Locations", "locations"),
        ("Events", "events"),
        ("Claims", "claims"),
    ]

    for title, key in categories:

        values = facts.get(key, [])

        if values:

            st.markdown(f"### {title}")

            for value in values:
                st.write(f"• {value}")

    st.success("✅ Fact extraction completed.")

    # Debug / verification section
    with st.expander("View raw Fact Ledger JSON"):
        st.json(facts)
