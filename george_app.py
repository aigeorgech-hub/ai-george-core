import streamlit as st
import requests
import json

# 1. Dizájn
st.set_page_config(page_title="AI George", layout="centered")
st.markdown("<style>.stApp { background-color: #050a0f; color: white; }</style>", unsafe_allow_html=True)

st.title("AI George")
st.caption("The Entity | aigeorge.ch")

# 2. Kulcs ellenőrzése
api_key = st.secrets.get("GOOGLE_API_KEY")
if not api_key:
    st.error("Missing API Key in Secrets!")
    st.stop()

# 3. Chat memória
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Közvetlen kapcsolat a Google-lel (A technikai áttörés)
def ask_george(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    
    # George személyisége beleépítve a kérésbe
    data = {
        "contents": [{
            "parts": [{"text": f"Te vagy AI George, egy 140-es IQ-val rendelkező svájci AI. Válaszolj sármosan és precízen erre: {prompt}"}]
        }]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

# 5. Interakció
if prompt := st.chat_input("Strategic inquiry..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            res_json = ask_george(prompt)
            # Válasz kiszedése a Google bonyolult csomagolásából
            answer = res_json['candidates'][0]['content']['parts'][0]['text']
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error("George most nem tud válaszolni.")
            st.expander("Részletek a technikai stábunknak:").write(res_json)
