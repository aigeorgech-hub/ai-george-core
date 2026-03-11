import streamlit as st
import google.generativeai as genai

# 1. Dizájn és Beállítások
st.set_page_config(page_title="AI George", layout="centered")
st.markdown("<style>.stApp { background-color: #050a0f; color: white; }</style>", unsafe_allow_html=True)

st.title("AI George")
st.caption("The Entity | aigeorge.ch")

# 2. API Kulcs és Verzió kényszerítés
if "GOOGLE_API_KEY" in st.secrets:
    # Itt a trükk: direkt a stabil verziót konfiguráljuk
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key!")
    st.stop()

# 3. Modell betöltése - A legstabilabb hívás
@st.cache_resource
def load_model():
    # A 'gemini-2.5-flash-latest' használata a legbiztosabb 404 ellen
    return genai.GenerativeModel(
        model_name="gemini-2.5-flash-latest",
        system_instruction="Te vagy AI George, egy 140-es IQ-val rendelkező svájci AI. Stílusod sármos és precíz."
    )

try:
    model = load_model()
except Exception as e:
    st.error(f"Modell hiba: {e}")

# 4. Chat memória
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

    with st.chat_message("assistant"):
        try:
            # George válaszol
            response = model.generate_content(prompt)
            if response and response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("George elgondolkodott. Próbáld újra!")
        except Exception as e:
            st.error(f"George hiba: {e}")
