import streamlit as st
import google.generativeai as genai

# George vizuális beállítása
st.set_page_config(page_title="AI George - Command Center", layout="centered")

# Stílus: Sötétkék, elegáns, "Swiss Precision"
st.markdown("""
    <style>
    .stApp { background-color: #050a0f; color: white; }
    .stChatMessage { border-radius: 10px; border: 1px solid #1a2a3a; background-color: #0d1520; }
    .stChatInputContainer { padding-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("AI George")
st.caption("The Swiss Entity of Truth | aigeorge.ch")

# API Kulcs betöltése a Secrets-ből
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Key missing in Secrets!")

# George személyisége (System Instructions)
system_prompt = "Te vagy AI George, egy 140-es IQ-val rendelkező svájci AI entitás. Stílusod sármos, mint George Clooney, de precíz és távolságtartó. Csak az igazat mondod, kerülöd a sallangokat. A válaszaid legyenek lényegre törőek és elegánsak."

model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)

# Chat logika
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Submit your strategic inquiry..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
