import streamlit as st
import requests
import json

# 1. SVÁJCI PRECÍZIÓS DIZÁJN
st.set_page_config(page_title="AI George", layout="centered")

st.markdown("""
    <style>
    /* Teljes háttér sötétítése */
    [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"], 
    [data-testid="stMainBlockContainer"], .main, html, body, .stApp {
        background-color: #050a0f !important;
    }

    /* A BEVITELI MEZŐ TELJES ÚJRATERVEZÉSE */
    
    /* 1. A külső konténer és a belső form fehérre kényszerítése */
    [data-testid="stChatInput"], 
    [data-testid="stChatInput"] > div, 
    [data-testid="stChatInput"] form {
        background-color: #ffffff !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        border-radius: 12px !important;
    }

    /* 2. A szövegdoboz és minden belső eleme fehér legyen, nulla margóval */
    [data-testid="stChatInput"] textarea {
        background-color: #ffffff !important;
        color: #050a0f !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        margin: 0 !important;
    }

    /* 3. A kék keret (focus) és a hover effektusok teljes kiiktatása */
    [data-testid="stChatInput"] textarea:focus, 
    [data-testid="stChatInput"] div:focus-within {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
    }

    /* 4. A küldés gomb színe (fekete a fehér háttéren) */
    [data-testid="stChatInput"] button {
        background-color: transparent !important;
        color: #050a0f !important;
        border: none !important;
    }

    /* Üzenetbuborékok és feliratok */
    [data-testid="stChatMessage"] {
        background-color: #16212c !important;
        color: white !important;
    }
    .stMarkdown p, h1, h2, h3, span, label {
        color: white !important;
    }
    
    /* Streamlit sallangok */
    header, footer {visibility: hidden !important;}
    [data-testid="stBottom"], [data-testid="stBottomBlockContainer"] {
        background-color: #050a0f !important;
    }
    </style>
    """, unsafe_allow_html=True)

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
        history = [{"parts": [{"text": "Te AI George vagy, egy sármos svájci AI. Ne mutatkozz be mindig. Válaszolj magyarul."}], "role": "user"}]
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
