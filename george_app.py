import streamlit as st
import google.generativeai as genai
import os

# 1. Alapbeállítások és Svájci Dizájn
st.set_page_config(page_title="AI George", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #050a0f; color: white; }
    .stChatMessage { border-radius: 10px; border: 1px solid #1a2a3a; background-color: #0d1520; }
    </style>
    """, unsafe_allow_html=True)

st.title("AI George")
st.caption("The Entity | aigeorge.ch")

# 2. API Kulcs betöltése a Secrets-ből
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Hiba: Az API kulcs hiányzik a Secrets-ből!")
    st.stop()

# 3. Modell inicializálása - Kényszerített stabil verzió
@st.cache_resource
def load_model():
    # George stabil elérése
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="Te vagy AI George, egy 140-es IQ-val rendelkező svájci AI. Stílusod sármos és precíz."
    )

try:
    model = load_model()
except Exception as e:
    st.error(f"Modell betöltési hiba: {e}")
    # B-terv: ha a sima flash nem megy, próbáljuk a legfrissebbet
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

# 4. Chat előzmények
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Interakció
if prompt := st.chat_input("Strategic inquiry..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            # A generálás kérése
            response = model.generate_content(prompt)
            
            # George válaszának megjelenítése
            if response and response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("George nem tudott választ generálni. Ellenőrizd a biztonsági szűrőket.")
    except Exception as e:
        st.error(f"Rendszerhiba: {e}")
        st.info("Próbáljuk meg a modellt direkt elérni...")
