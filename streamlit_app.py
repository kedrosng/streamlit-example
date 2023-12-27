import streamlit as st
import requests 

url = "https://api.perplexity.ai/chat/completions"
headers = {
  "authorization": "Bearer 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"
}

def ask_chatgpt(prompt, model):
  payload = {
    "model": model,
    "messages": [
      {"role": "user", "content": prompt}
    ]
  }

  response = requests.post(url, json=payload, headers=headers)
  return response.json()["choices"][0]["message"]["content"]

st.title("Chat with PPLX")

# Initialize chat history
if "messages" not in st.session_state:
  st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
  st.text_area(message["role"] + ":", value=message["content"], disabled=True)

# Model selection
model = st.selectbox("Select Model", ["pplx-70b-online", "pplx-7b-online", "pplx-70b-chat"])

user_input = st.text_input("You:")

if st.button("Send"):
  response = ask_chatgpt(user_input, model)
  
  # Add user message to chat history
  st.session_state.messages.append({"role": "You", "content": user_input})
  
  # Add assistant response to chat history
  st.session_state.messages.append({"role": "PPLX", "content": response})
