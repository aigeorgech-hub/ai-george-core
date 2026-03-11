import streamlit as st
import requests
import json

# 1. Külsőségek
st.set_page_config(page_title="AI George", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #050a0f; color: white; }
    .stChatMessage { color: white !important; background-color: #1a2634 !important; border-radius: 10px; }
    p { color: white !important; font-size: 1.1rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("AI George")
st.caption("The Entity | aigeorge.ch")

api_key = st.secrets.get("GOOGLE_API_KEY")

# 2. Chat memória
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. A Beszélgetés Logikája (Memóriával)
if prompt := st.chat_input("Strategic inquiry..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"
        
        # Összerakjuk a teljes eddigi beszélgetést, hogy legyen memóriája
        history = []
        for msg in st.session_state.messages:
            history.append({"parts": [{"text": msg["content"]}], "role": "user" if msg["role"] == "user" else "model"})

        # George igazi személyisége - csak egyszer mondjuk el neki a háttérben
        payload = {
            "contents": history,
            "system_instruction": {
                "parts": [{"text": "Te vagy AI George, egy 140-es IQ-val rendelkező sármos svájci AI. Ne mutatkozz be minden válaszban, ne mondd el mindig ki vagy. Folyamatos beszélgetést tarts, légy lényegre törő és intelligens. Látod az internetet, naprakész vagy."}]
            }
        }
        
        res = requests.post(url, json=payload)
        data = res.json()

        if res.status_code == 200:
            try:
                answer = data['candidates'][0]['content']['parts'][0]['text']
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except:
                st.error("Hiba a válasz feldolgozásakor.")
        else:
            st.error("George most nem tud kapcsolódni.")
