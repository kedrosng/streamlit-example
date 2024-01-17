import streamlit as st
import requests

st.set_page_config(page_title="EnChat", page_icon=":robot:")


price_table = """
| Model Parameter Count | $/1M input tokens | $/1M output tokens |
|-----------------------|-------------------|--------------------|
| 7B                    | $0.07             | $0.28              |
| 13B                   | $0.14             | $0.56              |
| 34B                   | $0.35             | $1.40              |
| 70B                   | $0.70             | $2.80              |

**Online Model Pricing**

| Online Model Parameter Count | $/1000 requests | $/1M output tokens |
|------------------------------|-----------------|--------------------|
| 7B                           | $5              | $0.28              |
| 70B                          | $5              | $2.80              |
"""
st.title("Home")

st.sidebar.markdown("## Pricing Information")
st.sidebar.markdown(price_table)

# Function to clear the chat
def clear_chat():
    st.session_state.chat_history = []
    chat_placeholder.empty()  # Clear the chat display

# Button to clear the chat
if st.button('Clear Chat'):
    clear_chat()