import streamlit as st
import requests

st.set_page_config(page_title="Perplexity AI (Paid)", page_icon=":robot:")

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

url = "https://api.perplexity.ai/chat/completions"
headers = {"authorization": "Bearer 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"}
model_options = ["pplx-7b-online", "pplx-70b-chat", "pplx-7b-chat", "pplx-70b-online", "llama-2-70b-chat", "codellama-34b-instruct", "mistral-7b-instruct", "mixtral-8x7b-instruct"]

st.header("Perplexity AI (Paid)")

# Function to reset the state
def reset_state():
    for key in st.session_state:
        del st.session_state[key]

# Get the model from the session state or the user
if "model" not in st.session_state:
    st.session_state["model"] = st.selectbox('Select a model', model_options, index=model_options.index(st.session_state["model"]), key="model_select")

#st.markdown("You are chatting with the **{}** model.".format(st.session_state["model"]))

# Initialize the chat history in session state if it's not already set
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Placeholder for the chat output
chat_placeholder = st.empty()

# Function to send a message and get a response
def send_message(prompt):
    payload = {"model": st.session_state["model"], "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, json=payload, headers=headers).json()
    st.session_state["chat_history"].append({"role": "user", "content": prompt})
    st.session_state["chat_history"].append({"role": "assistant", "content": response["choices"][0]["message"]["content"]})
    update_chat_display()

# Function to update the chat display
def update_chat_display():
    chat_history = st.session_state["chat_history"]
    markdown_text = ""
    for i, message in enumerate(chat_history):
        role = message["role"]
        content = message["content"]
        if role == "user":
            markdown_text += f"**User** > {content}\n"
        else:
            markdown_text += f"**Assistant** > {content}\n"
    chat_placeholder.markdown(markdown_text)

# Function to clear the chat
def clear_chat():
    reset_state()
    update_chat_display()

# Add a text input for the user to enter their message
input_box = st.text_input("Type your message here...")

# Add a button to send the message and get a response
if st.button("Send"):
    send_message(input_box)

# Add a button to clear the chat
st.sidebar.button("Clear Chat", on_click=clear_chat)

# Add the pricing table to the sidebar
st.sidebar.markdown("## Pricing Information")
st.sidebar.markdown(price_table)

# Call the update_chat_display function to initialize the chat display
update_chat_display()