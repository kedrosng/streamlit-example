import requests
from bardapi import Bard, SESSION_HEADERS
import streamlit as st
import json


session = requests.Session()
psid = st.text_input("Enter __Secure-1PSID value:")
psidts = st.text_input("Enter __Secure-1PSIDTS value:")
token = psid
session.cookies.set("__Secure-1PSID", token)
#session.cookies.set( "__Secure-1PSIDCC", "ABTWhQEdIisXan1iW4sYI4WxH-fugcaeNUV_F3Wg7a8CqH-U2G1yx0vbpxYk5fvSOLXyGYokyA")
session.cookies.set("__Secure-1PSIDTS", psidts)
session.headers = SESSION_HEADERS
bard = Bard(token=token, session=session, timeout=30)
#new_cookies = bard.update_1PSIDTS()
#print('New cookies:', new_cookies)
#print(new_cookies.get("__Secure-1PSIDTS"))
#print(new_cookies.get("__Secure-1PSIDCC"))
#print(new_cookies.get("__Secure-3PSIDTS"))

#token = "ewiguUbsFv4Y2Iwt_nPikDZ9GLaiRipbRV0fSXj4WIOKyGmi4nLMOnuujMU0vSfRvFXSSA."
#session.cookies.set("__Secure-1PSID", "ewiguUbsFv4Y2Iwt_nPikDZ9GLaiRipbRV0fSXj4WIOKyGmi4nLMOnuujMU0vSfRvFXSSA.")
#session.cookies.set( "__Secure-1PSIDCC", "ABTWhQHyagW_Ybo6WJ8jJz1Ezi-AQOkjfDzOWUJDHZ7qSVSWG57Aaai1UWdttFimXYRptA5_pQ")
#session.cookies.set("__Secure-1PSIDTS", "sidts-CjIBPVxjSt7g0nnelJmIMozERAakcdpT4dInWEVHaC6iNFLuWtoKB3o-maUI2ndovnThEhAA")
#session.headers = SESSION_HEADERS

bard = Bard(token=token, session=session)
st.title("Google Bard - With Internet Access")
# Streamlit user input for queries.
user_query = st.text_input("Enter your query:","")

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