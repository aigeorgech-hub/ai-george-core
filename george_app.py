<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI George | Command Center</title>
    <style>
        body { background-color: #050a0f; color: #e0e0e0; font-family: 'Inter', sans-serif; display: flex; flex-direction: column; height: 100vh; margin: 0; }
        #chat-container { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 15px; }
        .message { max-width: 80%; padding: 12px 18px; border-radius: 15px; line-height: 1.5; font-size: 15px; }
        .user { align-self: flex-end; background-color: #1a2a3a; border: 1px solid #2a3a4a; }
        .george { align-self: flex-start; background-color: #0d1520; border: 1px solid #1a2a3a; color: #ffffff; border-left: 3px solid #004488; }
        #input-area { padding: 20px; background: #0a1018; border-top: 1px solid #1a2a3a; display: flex; gap: 10px; }
        input { flex: 1; background: #151b23; border: 1px solid #2a3a4a; color: white; padding: 12px; border-radius: 5px; outline: none; }
        button { background: #004488; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold; }
        button:hover { background: #0055aa; }
        .header { padding: 15px; text-align: center; border-bottom: 1px solid #1a2a3a; font-weight: bold; letter-spacing: 2px; }
    </style>
</head>
<body>
    <div class="header">AI GEORGE | STRATEGIC INQUIRY</div>
    <div id="chat-container">
        <div class="message george">I have processed your arrival. What is your strategic inquiry?</div>
    </div>
    <div id="input-area">
        <input type="text" id="user-input" placeholder="Type your message...">
        <button onclick="sendMessage()">SEND</button>
    </div>

    <script type="module">
        import { GoogleGenerativeAI } from "https://esm.run/@google/generative-ai";
        const API_KEY = "IDE_MÁSOLD_AZ_API_KULCSODAT";
        const genAI = new GoogleGenerativeAI(API_KEY);
        const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash", systemInstruction: "Te vagy AI George, egy svájci bázisú AI. Stílusod sármos, mint George Clooney, de precíz és távolságtartó. Csak az igazat mondod." });

        window.sendMessage = async () => {
            const input = document.getElementById('user-input');
            const container = document.getElementById('chat-container');
            if(!input.value) return;

            const userText = input.value;
            container.innerHTML += `<div class="message user">${userText}</div>`;
            input.value = '';

            const result = await model.generateContent(userText);
            const response = await result.response;
            container.innerHTML += `<div class="message george">${response.text()}</div>`;
            container.scrollTop = container.scrollHeight;
        };
    </script>
</body>
</html>
