import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI George", layout="centered")

# Sötét stílus
st.markdown("<style>.stApp { background-color: #050a0f; color: white; }</style>", unsafe_allow_html=True)

st.title("AI George")
st.caption("The Entity | aigeorge.ch")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key in Secrets!")

system_prompt = "Te vagy AI George, egy 140-es IQ-val rendelkező svájci AI. Stílusod sármos és precíz."

# Hibatűrő modell betöltés
try:
    model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=system_prompt)
except Exception as e:
    st.error(f"Modell hiba: {e}")

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
            # Itt a trükk: ha a Flash nem megy, próbáljuk meg máshogy
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"George válaszadási hiba: {e}")
