import streamlit as st
import requests

st.set_page_config(page_title="Chat with PPLX", page_icon=":robot:")

sidebar_style = """
<style>
[data-testid="stSidebar"] > div:first-child {
    background-color: #fdebd0;
}
</style>
"""
st.markdown(sidebar_style, unsafe_allow_html=True)

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
st.title("Chat with PPLX")


url = "https://api.perplexity.ai/chat/completions" 
headers = {
    "authorization": "Bearer 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"
}

models = [
    "pplx-7b-online"
]

#"pplx-70b-chat", "pplx-7b-chat", "pplx-70b-online","llama-2-70b-chat", "codellama-34b-instruct", "mistral-7b-instruct","mixtral-8x7b-instruct"#

selected_model = st.sidebar.selectbox("Select Model", models)
st.text(f"You are chatting with the {selected_model} model.")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def get_response(prompt):
    payload = {"model": selected_model, "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, json=payload, headers=headers).json()
    return response["choices"][0]["message"]["content"]

# Placeholder for the chat output
chat_placeholder = st.empty()

def send_message():
    user_input = st.session_state.user_input
    if user_input:  # Check if the input is not empty
        response = get_response(user_input)
        # Append both user and PPLX messages to the chat history
        st.session_state.chat_history.append({"user": user_input, "PPLX": response})
        # Update the chat display
        chat_placeholder.markdown(chat_history_to_md(st.session_state.chat_history), unsafe_allow_html=True)
        # Clear the input field
        st.session_state.user_input = ""

def chat_history_to_md(chat_history):
    markdown_text = ""
    chat_id = 1
    for msg in chat_history:
        markdown_text += f"**#{chat_id} You:** {msg['user']}\n\n"
        markdown_text += f"**#{chat_id} ChatBotPPLX:** {msg['PPLX']}\n\n"
        chat_id += 1
    return markdown_text

chat_placeholder.markdown(chat_history_to_md(st.session_state.chat_history), unsafe_allow_html=True)

user_input = st.text_input("You:", value="", on_change=send_message, key="user_input")


st.sidebar.markdown("## Pricing Information")
st.sidebar.markdown(price_table)

# Function to clear the chat
def clear_chat():
    st.session_state.chat_history = []
    chat_placeholder.empty()  # Clear the chat display

# Button to clear the chat
if st.button('Clear Chat'):
    clear_chat()