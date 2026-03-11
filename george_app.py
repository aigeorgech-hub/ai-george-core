import streamlit as st
import requests
import json

# 1. Külsőségek
st.set_page_config(page_title="AI George", layout="centered")
st.markdown("<style>.stApp { background-color: #050a0f; color: white; }</style>", unsafe_allow_html=True)

st.title("AI George")
st.caption("The Entity | aigeorge.ch")

api_key = st.secrets.get("GOOGLE_API_KEY")

# 2. Chat memória
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. A Beszélgetés Logikája
if prompt := st.chat_input("Strategic inquiry..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Próbáljuk meg a legfrissebb stabil nevet (gemini-1.5-flash-latest)
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": f"Te vagy AI George, egy svájci AI. Válaszolj: {prompt}"}]}]
        }
        
        res = requests.post(url, json=payload)
        data = res.json()

        if res.status_code == 200:
            answer = data['candidates'][0]['content']['parts'][0]['text']
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.error(f"Hiba kód: {res.status_code}")
            st.write("A Google válasza: ", data.get("error", {}).get("message", "Ismeretlen hiba"))
            
            # EZ A MENTŐÖV: Kilistázzuk, mit enged a Google
            st.info("George nyomozást indít... Itt a lista a használható modelljeidről:")
            list_url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
            models_data = requests.get(list_url).json()
            
            if "models" in models_data:
                for m in models_data["models"]:
                    st.code(m["name"])
            else:
                st.warning("Még a modelleket sem sikerült lekérni. Biztos jó az API kulcsod?")
