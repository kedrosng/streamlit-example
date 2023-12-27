import streamlit as st
import requests

st.set_page_config(page_title="Intelligent Chat", page_icon=":robot:")

st.title("Intelligent Chat")

url = "https://api.perplexity.ai/chat/completions"  
headers = {
  "authorization": "Bearer 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"
}

models = ["pplx-7b-chat", "pplx-70b-chat", "pplx-7b-online", "pplx-70b-online",
          "llama-2-70b-chat", "codellama-34b-instruct", "mistral-7b-instruct",
          "mixtral-8x7b-instruct"]

selected_model = st.sidebar.selectbox("Select Model", models)  

conversations = {}
if "conversations" not in st.session_state:
    st.session_state.conversations = {}

def get_response(prompt, conversation_id):
    payload = {"model": selected_model, "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, json=payload, headers=headers).json()
    return response["choices"][0]["message"]["content"]

def add_conversation():
    conversation_id = "Chat#" + str(len(st.session_state.conversations) + 1)
    st.session_state.conversations[conversation_id] = []

def clear_conversations():
    st.session_state.conversations = {}

if "active_conversation" not in st.session_state and st.session_state.conversations:
    st.session_state.active_conversation = list(st.session_state.conversations.keys())[0]
elif not st.session_state.conversations:
    add_conversation()
    st.session_state.active_conversation = list(st.session_state.conversations.keys())[0]

conversation_tabs = st.sidebar.tabs(st.session_state.conversations.keys())
st.session_state.active_conversation = conversation_tabs[0]

if st.sidebar.button("Add Conversation"):
    add_conversation()
    st.experimental_rerun()

if st.sidebar.button("Clear All Conversations"):
    clear_conversations()
    st.experimental_rerun()

chat_id = 1
conversation = st.session_state.conversations[st.session_state.active_conversation]
for msg in conversation:
    st.markdown(f"**#{chat_id} You:** {msg['user']}")
    st.markdown(f"**#{chat_id} PPLX:** {msg['PPLX']}")
    chat_id += 1

st.markdown("")

user_input = st.text_input("You:", placeholder="Enter message...")

if st.button("Send"):
    response = get_response(user_input, st.session_state.active_conversation)
    conversation.append({"user": user_input, "PPLX": response})
    st.experimental_rerun()

st.text("")
st.text(f"You are chatting with the {selected_model} model.")