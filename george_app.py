import streamlit as st
import google.generativeai as genai

# 1. Svájci Elegancia
st.set_page_config(page_title="AI George", layout="centered")
st.markdown("<style>.stApp { background-color: #050a0f; color: white; }</style>", unsafe_allow_html=True)

st.title("AI George")
st.caption("The Entity | aigeorge.ch")

# 2. API Kulcs és Biztonsági Protokoll
if "GOOGLE_API_KEY" in st.secrets:
    # Itt a trükk: Nem hagyjuk, hogy a rendszer bétát válasszon
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key!")
    st.stop()

# 3. Modell inicializálása - A "Golyóálló" módszer
@st.cache_resource
def load_model():
    # Csak a tiszta nevet adjuk meg, 'models/' és 'latest' nélkül
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash", 
        system_instruction="Te vagy AI George, egy 140-es IQ-val rendelkező svájci AI entitás. Stílusod sármos, precíz és lényegre törő."
    )

model = load_model()

# 4. Memória
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
            # George válaszol (itt kényszerítjük a generálást)
            response = model.generate_content(prompt)
            if response and response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("George válasza elakadt a szűrőn. Próbáld másképp!")
        except Exception as e:
            # Ha MÉG MINDIG 404, akkor a hiba a Google AI Studio beállításában van
            st.error(f"Rendszerhiba: {e}")
            st.info("Tipp: Generálj egy ÚJ kulcsot egy ÚJ projektben (Create API key in new project).")
