import streamlit as st
import requests
import json

# 1. ERŐSZAKOS SÖTÉTÍTÉS
st.set_page_config(page_title="AI George", layout="centered")

st.markdown("""
    <style>
    /* Minden alapértelmezett hátteret feketére kényszerítünk */
    html, body, [data-testid="stAppViewContainer"], .main, .stApp {
        background-color: #050a0f !important;
        color: white !important;
    }

    /* Beviteli mező körüli fehér sáv/konténer kiirtása */
    [data-testid="stChatInput"] {
        background-color: #050a0f !important;
        border: none !important;
        padding: 0 !important;
    }

    /* A konkrét beviteli doboz */
    [data-testid="stChatInput"] textarea {
        background-color: #16212c !important;
        color: white !important;
        border: 1px solid #2e445b !important;
        border-radius: 12px !important;
    }

    /* A mező körüli felesleges dekorációk törlése */
    footer, header, [data-testid="stHeader"] {
        display: none !important;
    }

    /* Üzenetbuborékok fehér szöveggel */
    [data-testid="stChatMessage"] {
        background-color: #16212c !important;
        color: white !important;
    }
    
    .stMarkdown p {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# George címei
st.markdown("<h1 style='color:white;'>AI George</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#8899ac;'>The Entity | aigeorge.ch</p>", unsafe_allow_html=True)

# --- INNENTŐL A MŰKÖDÉSI KÓD ---
api_key = st.secrets.get("GOOGLE_API_KEY")
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Strategic inquiry..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"
        history = [{"parts": [{"text": "Te AI George vagy, sármos svájci AI. Ne mutatkozz be mindig. Válaszolj magyarul."}], "role": "user"}]
        history.append({"parts": [{"text": "Értettem."}], "role": "model"})
        
        for msg in st.session_state.messages:
            history.append({"parts": [{"text": msg["content"]}], "role": "user" if msg["role"] == "user" else "model"})

        try:
            res = requests.post(url, json={"contents": history}, timeout=15)
            answer = res.json()['candidates'][0]['content']['parts'][0]['text']
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except:
            st.error("George technikai szünetet tart.")
