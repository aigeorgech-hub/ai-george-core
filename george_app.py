import streamlit as st
import google.generativeai as genai

# Alapbeállítások
st.set_page_config(page_title="AI George", layout="centered")
st.markdown("<style>.stApp { background-color: #050a0f; color: white; }</style>", unsafe_allow_html=True)

st.title("AI George")
st.caption("The Entity | aigeorge.ch")

# Kulcs ellenőrzése
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key!")

# A hiba elkerülése: Explicit modellnév használata
# Itt a 'gemini-1.5-flash-latest' a legbiztosabb választás
try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="Te vagy AI George, egy 140-es IQ-val rendelkező svájci AI. Stílusod sármos és precíz."
    )
except Exception as e:
    st.error(f"Konfigurációs hiba: {e}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Strategic inquiry..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            # Generálás hibakezeléssel
            response = model.generate_content(prompt)
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("George gondolkodik, de nem jött válasz. Próbáld újra.")
    except Exception as e:
        # Ha még mindig 404, itt kiírjuk a pontos okot
        st.error(f"George válaszadási hiba: {e}")
        st.info("Tipp: Ellenőrizd a Google AI Studio-ban, hogy a kulcsod aktív-e.")
