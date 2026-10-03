import streamlit as st

st.set_page_config(
    page_title="Content Repurposing Chain",
    page_icon="🔄",
    layout="wide"
)

st.title(" Content Repurposing Chain")

st.write(
    "Transform an article into a summary, LinkedIn post, "
    "and X/Twitter thread while preserving factual consistency."
)

st.divider()

article = st.text_area(
    "Paste your article",
    height=300,
    placeholder="PASTE A FACTUAL ARTICLE HERE"
)

if st.button(" Run Content Repurposing", type="primary"):

    if not article.strip():
        st.error("Please enter an article before running the pipeline.")

    else:
        st.success(" Application is working!")

        st.subheader("Input Article")
        st.write(article)

        st.info(
            "AI pipeline will be connected in the next step."
        )