import streamlit as st
import requests

st.set_page_config(page_title="Chat with PPLX", page_icon=":robot:") 

st.title("Chat with PPLX")

url = "https://api.perplexity.ai/chat/completions"
headers = {
  "authorization": "Bearer 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"  
}

models = ["pplx-7b-chat", "pplx-70b-chat", "pplx-7b-online", "pplx-70b-online",
          "llama-2-70b-chat", "codellama-34b-instruct", "mistral-7b-instruct",  
          "mixtral-8x7b-instruct"]

selected_model = st.sidebar.selectbox("Select Model", models)

def ask_chatgpt(prompt, model):
  payload = {
    "model": model,
    "messages": [{"role": "user", "content": prompt}]
  }
  
  response = requests.post(url, json=payload, headers=headers)
  return response.json()["choices"][0]["message"]["content"]

# Initialize chat history like the Counter example
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You:")  

if st.button("Send"):
  response = ask_chatgpt(user_input, selected_model)
  st.session_state.chat_history.append({"user": user_input, "PPLX": response})

for message in st.session_state.chat_history:
  st.markdown("You: " + message["user"]) 
  st.markdown("PPLX: " + message["PPLX"])