from flask import Flask, request, jsonify, render_template_string
import requests
from groq import Groq

# =========================
# CONFIGURATION
GROQ_API_KEY = "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"
NEWS_API_KEY = "2e3f64b4d09e465f8ae2ec32b2ff53ab"

client = Groq(api_key=GROQ_API_KEY)

app = Flask(__name__)

# =========================
# HTML FRONTEND
# =========================


HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>AI Stock Market Assistant</title>

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

body{
    font-family:'Poppins',sans-serif;
    background:#020617;
    overflow:hidden;
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    color:white;
    position:relative;
}

/* Animated Background */

body::before{
    content:'';
    position:absolute;
    width:200%;
    height:200%;
    background:
    radial-gradient(circle at 20% 20%, rgba(56,189,248,0.15), transparent 25%),
    radial-gradient(circle at 80% 30%, rgba(34,197,94,0.15), transparent 25%),
    radial-gradient(circle at 50% 80%, rgba(168,85,247,0.15), transparent 25%);
    animation:bgMove 15s linear infinite;
    z-index:0;
}

@keyframes bgMove{
    0%{
        transform:translate(0,0);
    }
    50%{
        transform:translate(-10%,-10%);
    }
    100%{
        transform:translate(0,0);
    }
}

/* Stock Line Animation */

.stock-lines{
    position:absolute;
    width:100%;
    height:100%;
    overflow:hidden;
    z-index:0;
}

.line{
    position:absolute;
    width:200%;
    height:2px;
    background:linear-gradient(90deg,
        transparent,
        #22c55e,
        #38bdf8,
        transparent);
    opacity:0.3;
    animation:moveLine linear infinite;
}

.line:nth-child(1){
    top:20%;
    animation-duration:8s;
}

.line:nth-child(2){
    top:40%;
    animation-duration:12s;
}

.line:nth-child(3){
    top:60%;
    animation-duration:10s;
}

.line:nth-child(4){
    top:80%;
    animation-duration:14s;
}

@keyframes moveLine{
    from{
        transform:translateX(-50%) scaleY(1);
    }

    50%{
        transform:translateX(0%) scaleY(3);
    }

    to{
        transform:translateX(50%) scaleY(1);
    }
}

/* Main Container */

.container{
    position:relative;
    z-index:2;
    width:95%;
    max-width:1100px;
    height:92vh;
    background:rgba(255,255,255,0.05);
    backdrop-filter:blur(25px);
    border:1px solid rgba(255,255,255,0.1);
    border-radius:30px;
    overflow:hidden;
    box-shadow:
        0 0 30px rgba(56,189,248,0.15),
        inset 0 0 30px rgba(255,255,255,0.02);
}

/* Header */

.header{
    padding:25px;
    display:flex;
    justify-content:space-between;
    align-items:center;
    border-bottom:1px solid rgba(255,255,255,0.08);
    background:rgba(255,255,255,0.02);
}

.logo{
    display:flex;
    align-items:center;
    gap:18px;
}

.logo-icon{
    width:60px;
    height:60px;
    border-radius:18px;
    background:linear-gradient(135deg,#38bdf8,#22c55e);
    display:flex;
    justify-content:center;
    align-items:center;
    font-size:28px;
    box-shadow:0 0 25px rgba(56,189,248,0.6);
    animation:pulse 2s infinite;
}

@keyframes pulse{
    0%{
        transform:scale(1);
    }
    50%{
        transform:scale(1.05);
    }
    100%{
        transform:scale(1);
    }
}

.logo h1{
    font-size:28px;
    font-weight:600;
}

.status{
    color:#22c55e;
    font-size:14px;
}

/* Market Ticker */

.market-bar{
    display:flex;
    gap:40px;
    padding:14px 30px;
    overflow:hidden;
    white-space:nowrap;
    border-bottom:1px solid rgba(255,255,255,0.05);
    background:rgba(255,255,255,0.03);
    animation:tickerMove 20s linear infinite;
}

@keyframes tickerMove{
    from{
        transform:translateX(100%);
    }
    to{
        transform:translateX(-100%);
    }
}

.market-item{
    font-size:15px;
    font-weight:500;
}

.green{
    color:#22c55e;
}

.red{
    color:#ef4444;
}

/* Chat Area */

.chat-box{
    height:calc(100% - 200px);
    overflow-y:auto;
    padding:30px;
    display:flex;
    flex-direction:column;
    gap:20px;
}

.message{
    max-width:75%;
    padding:18px 22px;
    border-radius:22px;
    line-height:1.7;
    animation:fadeIn 0.3s ease;
}

.user-message{
    align-self:flex-end;
    background:linear-gradient(135deg,#2563eb,#38bdf8);
    box-shadow:0 0 20px rgba(59,130,246,0.4);
}

.bot-message{
    align-self:flex-start;
    background:rgba(255,255,255,0.08);
    border:1px solid rgba(255,255,255,0.06);
    box-shadow:0 0 20px rgba(255,255,255,0.03);
}

@keyframes fadeIn{
    from{
        opacity:0;
        transform:translateY(15px);
    }
    to{
        opacity:1;
        transform:translateY(0);
    }
}

/* Input Area */

.input-area{
    position:absolute;
    bottom:0;
    width:100%;
    padding:20px;
    display:flex;
    gap:15px;
    background:rgba(255,255,255,0.03);
    border-top:1px solid rgba(255,255,255,0.05);
}

input{
    flex:1;
    padding:18px;
    border:none;
    outline:none;
    border-radius:18px;
    background:rgba(255,255,255,0.08);
    color:white;
    font-size:16px;
}

input::placeholder{
    color:#94a3b8;
}

button{
    padding:18px 30px;
    border:none;
    border-radius:18px;
    background:linear-gradient(135deg,#38bdf8,#22c55e);
    color:white;
    font-size:16px;
    font-weight:600;
    cursor:pointer;
    transition:0.3s;
    box-shadow:0 0 20px rgba(56,189,248,0.4);
}

button:hover{
    transform:translateY(-3px);
    box-shadow:0 0 35px rgba(56,189,248,0.7);
}

::-webkit-scrollbar{
    width:6px;
}

::-webkit-scrollbar-thumb{
    background:#334155;
    border-radius:20px;
}

</style>
</head>

<body>

<div class="container">

    <div class="header">

        <div class="logo">

            <div class="logo-icon">
                📈
            </div>

            <div>
                <h1>AI Stock Market Bot</h1>
                <div class="status">
                    ● Live Market Intelligence
                </div>
            </div>

        </div>

    </div>

    <div class="market-bar">

        <div class="market-item">
            NASDAQ <span class="green">+1.25%</span>
        </div>

        <div class="market-item">
            S&P 500 <span class="green">+0.82%</span>
        </div>

        <div class="market-item">
            Bitcoin <span class="red">-2.14%</span>
        </div>

        <div class="market-item">
            Gold <span class="green">+0.45%</span>
        </div>

    </div>

    <div class="chat-box" id="chat-box">

        <div class="message bot-message">
            👋 Welcome! Ask me about stocks, crypto, finance, or world news.
        </div>

    </div>

    <div class="input-area">

        <input
            type="text"
            id="message"
            placeholder="Ask about stock market, crypto, finance..."
        >

        <button onclick="sendMessage()">
            Send
        </button>

    </div>

</div>

<script>

async function sendMessage(){

    let input = document.getElementById("message");
    let message = input.value;

    if(message.trim() === ""){
        return;
    }

    let chatBox = document.getElementById("chat-box");

    chatBox.innerHTML += `
        <div class="message user-message">
            ${message}
        </div>
    `;

    input.value = "";

    chatBox.scrollTop = chatBox.scrollHeight;

    let response = await fetch("/chat",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            message:message
        })
    });

    let data = await response.json();

    chatBox.innerHTML += `
        <div class="message bot-message">
            ${data.reply}
        </div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;
}

</script>

</body>
</html>"""

# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

# =========================
# FETCH WORLD NEWS
# =========================

def get_world_news():

    try:

        url = f"https://newsapi.org/v2/top-headlines?category=business&language=en&pageSize=5&apiKey={NEWS_API_KEY}"

        response = requests.get(url)

        data = response.json()

        news_text = ""

        for article in data["articles"]:

            title = article["title"]

            news_text += f"- {title}\\n"

        return news_text

    except Exception:

        return "Unable to fetch world news."

# =========================
# CHAT ROUTE
# =========================

@app.route("/chat", methods=["POST"])
def chat():

    try:

        user_message = request.jsnews ["message"]

        latest_news = get_world_news()

        prompt = f"""
        You are a smart stock market AI assistant.

        Latest Business News:
        {latest_news}

        User Question:
        {user_message}

        Explain in simple English.
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a finance and stock market expert."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1000
        )

        answer = response.choices[0].message.content

        return jsonify({
            "reply": answer
        })

    except Exception as e:

        return jsonify({
            "reply": str(e)
        })

# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(debug=True) # type: ignore