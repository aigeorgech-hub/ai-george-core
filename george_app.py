import streamlit as st
import requests
import json

# 1. SVÁJCI MINIMALIZMUS - Tiszta sötét dizájn
st.set_page_config(page_title="AI George", layout="centered")

st.markdown("""
    <style>
    /* Teljes háttér sötétítése */
    .stApp {
        background-color: #050a0f !important;
    }
    
    /* Üzenetbuborékok - elegáns sötétkék */
    [data-testid="stChatMessage"] {
        background-color: #16212c !important;
        border-radius: 15px !important;
        border: none !important;
    }

    /* Beviteli mező fixálása */
    [data-testid="stChatInput"] {
        background-color: transparent !important;
        border: none !important;
    }

    [data-testid="stChatInput"] textarea {
        background-color: #16212c !important;
        color: white !important;
        border: 1px solid #2e445b !important;
        border-radius: 10px !important;
    }

    /* Fejléc és lábléc eltüntetése */
    header, footer {visibility: hidden;}
    
    /* Szöveg színe fehér */
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("AI George")
st.caption("The Entity | aigeorge.ch")

# API Kulcs betöltése
api_key = st.secrets.get("GOOGLE_API_KEY")

# Chat memória inicializálása
if "messages" not in st.session_state:
    st.session_state.messages = []

# Korábbi üzenetek megjelenítése
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Interakció
if prompt := st.chat_input("Strategic inquiry..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # URL a Gemini 2.5-höz (v1 stabil)
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"
        
        system_context = "Te AI George vagy, egy 140-es IQ-val rendelkező sármos svájci AI. Lényegre törő vagy, nem mutatsz be minden válaszban. Válaszolj magyarul."
        
        contents = [
            {"parts": [{"text": system_context}], "role": "user"},
            {"parts": [{"text": "Értettem, várom a stratégiai kérdéseket."}], "role": "model"}
        ]
        
        for msg in st.session_state.messages:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({"parts": [{"text": msg["content"]}], "role": role})

        try:
            res = requests.post(url, json={"contents": contents}, timeout=15)
            data = res.json()
            answer = data['candidates'][0]['content']['parts'][0]['text']
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error("George technikai szünetet tart.")
