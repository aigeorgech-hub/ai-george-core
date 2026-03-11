import streamlit as st
import google.generativeai as genai

# 1. Svájci Dizájn
st.set_page_config(page_title="AI George", layout="centered")
st.markdown("<style>.stApp { background-color: #050a0f; color: white; }</style>", unsafe_allow_html=True)

st.title("AI George")
st.caption("The Entity | aigeorge.ch")

# 2. API Kulcs
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key!")
    st.stop()

# 3. Modell (Használjuk a legstabilabb 1.5-öt, ha a 2.5 még bizonytalan)
@st.cache_resource
def load_model():
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="Te vagy AI George, egy 140-es IQ-val rendelkező svájci AI. Stílusod sármos és precíz."
    )

model = load_model()

# 4. Chat memória
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Interakció és Válasz
if prompt := st.chat_input("Strategic inquiry..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # George válaszának generálása
            response = model.generate_content(prompt)
            
            if response and response.text:
                output = response.text
                st.markdown(output)
                st.session_state.messages.append({"role": "assistant", "content": output})
            else:
                st.warning("George gondolkodik, de a Google válasza üres. Próbáld másképp kérdezni.")
        except Exception as e:
            st.error(f"George válaszadási hiba: {e}")
