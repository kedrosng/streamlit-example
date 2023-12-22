import streamlit as st
from perplexity import Perplexity

perplexity = Perplexity("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")

st.title("My Chatbot")

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []
    
user_input = st.text_input("You: ", key="input")
if user_input:
    output = perplexity.search(user_input)[0]["text"]
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

for i in range(len(st.session_state["generated"])):
    st.write(f"You: {st.session_state['past'][i]}")
    st.write(f"Bot: {st.session_state['generated'][i]}")
