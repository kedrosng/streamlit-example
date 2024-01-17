import streamlit as st

st.set_page_config(page_title="EnChat", page_icon=":robot:")

st.title("Welcome to EnChat")

st.markdown("## AI Models and Pricing Information")

st.markdown("### Google Gemini AI")
st.markdown("""
Gemini AI is Google's most advanced and capable AI model. It is multimodal, meaning it can understand not just text but also images, videos, and audio. It is capable of completing complex tasks in math, physics, and other areas, as well as understanding and generating high-quality code in various programming languages. It is available in three different sizes: Ultra, Pro, and Nano[1][5][13].
""")

st.markdown("**Pricing for Google Gemini AI**")
st.markdown("""
| Model | Input Type | $/Unit |
|-------|------------|--------|
| Gemini Pro | Image Input | $0.0025 / image |
| Gemini Pro | Video Input | $0.002 / second |
| Gemini Pro | Text Input | $0.00025 / 1k characters |
| Gemini Pro | Text Output | $0.0005 / 1k characters[6][14] |
""", unsafe_allow_html=True)

st.markdown("### Mistral AI")
st.markdown("""
Mistral AI offers compute efficient, powerful AI models with a strong research focus. It provides a user-friendly interface, intuitive navigation, and a wide range of features, including content generation, accurate information provision, mobile app availability, and Chrome extension integration[3][11].
""")

st.markdown("**Pricing for Mistral AI**")
st.markdown("""
| Model | Input | Output |
|-------|-------|--------|
| mistral-tiny | 0.14€ / 1M tokens | 0.42€ / 1M tokens |
| mistral-small | 0.6€ / 1M tokens | 1.8€ / 1M tokens |
| mistral-medium | 2.5€ / 1M tokens | 7.5€ / 1M tokens[4] |
""", unsafe_allow_html=True)

st.markdown("### Perplexity AI")
st.markdown("""
Perplexity AI is an answer engine that aims to deliver accurate answers to questions using large language models.
""")

st.markdown("**Pricing for Perplexity AI**")
st.markdown("""
| Model Parameter Count | $/1M input tokens | $/1M output tokens |
|-----------------------|-------------------|--------------------|
| 7B | $0.07 | $0.28 |
| 13B | $0.14 | $0.56 |
| 34B | $0.35 | $1.40 |
| 70B | $0.70 | $2.80 |
""", unsafe_allow_html=True)
st.markdown("**Online Model Pricing**")
st.markdown("""
| Online Model Parameter Count | $/1000 requests | $/1M output tokens |
|------------------------------|-----------------|--------------------|
| 7B | $5 | $0.28 |
| 70B | $5 | $2.80 |
""", unsafe_allow_html=True)