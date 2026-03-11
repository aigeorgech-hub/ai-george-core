st.markdown("""
    <style>
    /* 1. A két szélső sáv és a teljes háttér kényszerítése */
    [data-testid="stAppViewContainer"], 
    [data-testid="stAppViewBlockContainer"],
    [data-testid="stMainBlockContainer"],
    .main, html, body, .stApp {
        background-color: #050a0f !important;
        width: 100% !important;
    }

    /* 2. A beviteli mező alatti sáv (ami még fehér lehetett a széleken) */
    [data-testid="stBottom"], [data-testid="stBottomBlockContainer"] {
        background-color: #050a0f !important;
        border: none !important;
    }

    /* 3. A beviteli mező (Input) stílusa */
    [data-testid="stChatInput"] {
        border: 1px solid #2e445b !important;
        border-radius: 15px !important;
        background-color: #16212c !important;
    }

    [data-testid="stChatInput"] textarea {
        background-color: transparent !important;
        color: white !important;
    }

    /* 4. Szövegek és buborékok */
    [data-testid="stChatMessage"] {
        background-color: #16212c !important;
        color: white !important;
    }
    
    .stMarkdown p, h1, h2, h3, span, label {
        color: white !important;
    }

    /* 5. Sallangok törlése */
    header, footer {visibility: hidden !important;}
    </style>
    """, unsafe_allow_html=True)
