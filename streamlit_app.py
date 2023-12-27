import streamlit as st
import requests 

url = "https://api.perplexity.ai/chat/completions"
headers = {
  "authorization": "Bearer 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"
}

def ask_chatgpt(prompt):
  payload = {
    "model": "pplx-70b-online",
    "messages": [
      {"role": "user", "content": prompt}
    ]
  }

  response = requests.post(url, json=payload, headers=headers)
  return response.json()["choices"][0]["message"]["content"]

st.title("Chat with PPLX")
user_input = st.text_input("You:")

if st.button("Send"):
  response = ask_chatgpt(user_input)
  st.text_area("PPLX:", value=response)