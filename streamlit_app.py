import streamlit as st
import requests

# Define the API URL and the headers including the authorization token
url = "https://api.perplexity.ai/chat/completions"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer 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"
}

# Create a text input box for user input
user_input = st.text_input("You:", key="user_input")

# When the user presses enter, send the input to the chatbot API
if user_input:
    payload = {
        "model": "mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": "Be precise and concise."
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    }

    # Make the POST request to the API
    response = requests.post(url, json=payload, headers=headers)

    # If the request is successful, display the response
    if response.status_code == 200:
        response_data = response.json()
        chatbot_response = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
        st.text_area("Chatbot:", value=chatbot_response, height=100, key="chatbot_response")
    else:
        st.error("Failed to get response from the chatbot API")

# Run the Streamlit app
if __name__ == '__main__':
    st.title("Chatbot Interface")