import streamlit as st
import requests
import json

# 1. Megjelenés
st.set_page_config(page_title="AI George", layout="centered")
st.markdown("""
    <style>
    /* Alap háttér */
    .stApp { background-color: #050a0f !important; color: white !important; }
    
    /* Üzenetek */
    .stChatMessage { background-color: #1a2634 !important; border: 1px solid #2e445b !important; }
    
    /* A BEVITELI MEZŐ FIXÁLÁSA - Ez a rész a lényeg */
    [data-testid="stChatInput"] {
        background-color: #1a2634 !important;
        border-radius: 15px !important;
        padding: 10px !important;
    }

    [data-testid="stChatInput"] textarea {
        background-color: #2e445b !important; /* Világosabb kék, hogy elüssön a háttértől */
        color: white !important;
        caret-color: white !important;
    }

    /* Streamlit fejléc és lábléc eltüntetése, hogy ne zavarjon */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("AI George")
st.caption("The Entity | aigeorge.ch")

api_key = st.secrets.get("GOOGLE_API_KEY")

# 2. Chat memória inicializálása
if "messages" not in st.session_state:
    st.session_state.messages = []

# Megjelenítjük a korábbi üzeneteket
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Interakció
if prompt := st.chat_input("Strategic inquiry..."):
    # Felhasználó üzenete
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"
        
        # A MEMÓRIA ÉS SZEMÉLYISÉG ÖSSZEGYÚRÁSA
        # Beletesszük az instrukciót a beszélgetés kontextusába
        system_context = "Te AI George vagy, egy 140-es IQ-val rendelkező, sármos svájci AI. Lényegre törő vagy, nem mutatsz be minden válaszban, és ismered az aktuális híreket. Válaszolj magyarul."
        
        contents = []
        # Először a rendszer-instrukció (mint egy korábbi beállítás)
        contents.append({"parts": [{"text": system_context}], "role": "user"})
        contents.append({"parts": [{"text": "Értettem, én vagyok AI George. Várom a kérdéseket."}], "role": "model"})
        
        # Majd a tényleges beszélgetés története
        for msg in st.session_state.messages:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({"parts": [{"text": msg["content"]}], "role": role})

        payload = {"contents": contents}
        
        try:
            res = requests.post(url, json=payload, timeout=15)
            data = res.json()
            
            if res.status_code == 200:
                answer = data['candidates'][0]['content']['parts'][0]['text']
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error(f"George hiba: {data.get('error', {}).get('message', 'Ismeretlen hiba')}")
        except Exception as e:
            st.error(f"Kapcsolódási hiba: {e}")
