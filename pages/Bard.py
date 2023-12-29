import requests
from bardapi import Bard, SESSION_HEADERS
import streamlit as st
import json

session = requests.Session()
token = "dQigufHtC5Oj_0GMxZ5OdO10N_8dp_mQDwmT5YEb8a3goz8DOIB8JMZcyPf-RpdRai8IuA."
session.cookies.set("__Secure-1PSID", 'dQigufHtC5Oj_0GMxZ5OdO10N_8dp_mQDwmT5YEb8a3goz8DOIB8JMZcyPf-RpdRai8IuA.')
session.cookies.set( "__Secure-1PSIDCC", "ABTWhQEIzXCIPJ3zE0DuIjnWyz9_drMrKo595e_eurLwqJKsLHJJALKUucrLsSEyzdWF7gtI8-s")
session.cookies.set("__Secure-1PSIDTS", "sidts-CjEBPVxjSuQb_VTuETdeQebgZeeY40O0bdB4pYZZzss-N5sobqtNMQ6Fe62fCHoucRQ3EAA")
session.headers = SESSION_HEADERS

bard = Bard(token=token, session=session)
st.title("Google Bard - With Internet Access")
# Streamlit user input for queries.
user_query = st.text_input("Enter your query:", "How is the weather today in Seoul?")

# Get the answer from the Bard API using the user's query.
if user_query:
    weather_info = bard.get_answer(user_query)
    
    # Display images (if present).
    if "images" in weather_info:
        for img_url in weather_info["images"]:
            st.image(img_url)
    
    # Display the content.
    if weather_info:
        st.write(weather_info["content"])
    else:
        st.error("Could not retrieve the information.")
else:
    st.info("Please enter a query to get information.")