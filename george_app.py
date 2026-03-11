import streamlit as st
import requests
import json

# 1. ATOMBIZTOS SÖTÉTÍTÉS ÉS ELRENDEZÉS
st.set_page_config(page_title="AI George", layout="centered")

st.markdown("""
    <style>
    /* A teljes háttér kényszerítése */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main, html, body, .stApp {
        background-color: #050a0f !important;
    }

    /* A FEHÉR SÁV KIIRTÁSA (A beviteli mező alatti rész) */
    [data-testid="stBottom"] {
        background-color: transparent !important;
        border: none !important;
    }
    
    [data-testid="stBottomBlockContainer"] {
        background-color: #050a0f !important;
        border: none !important;
    }

    /* Beviteli mező (Input) doboza */
    [data-testid="stChatInput"] {
        border: 1px solid #2e445b !important;
        border-radius: 15px !important;
        background-color: #16212c !important;
    }

    [data-testid="stChatInput"] textarea {
        background-color: transparent !important;
        color: white !important;
    }

    /* Üzenetbuborékok fehér szöveggel */
    [data-testid="stChatMessage"] {
        background-color: #16212c !important;
        color: white !important;
    }
    
    /* Minden szöveg fehér */
    .stMarkdown p, h1, h2, h3, span, label {
        color: white !important;
    }

    /* Streamlit sallangok eltüntetése */
    header, footer {visibility: hidden !important;}
    </style>
    """, unsafe_allow_html=True)

# George megjelenése
st.markdown("<h1 style='text-align: center; color: white;'>AI George</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8899ac;'>The Entity | aigeorge.ch</p>", unsafe_allow_html=True)

# --- MŰKÖDÉSI KÓD ---
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
