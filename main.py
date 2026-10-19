import os
import sys
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from groq import Groq

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("Chatbot")

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    logger.critical("FATAL: 'GROQ_API_KEY' environment variable is missing!")
    sys.exit(1)

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
groq_client = Groq(api_key=GROQ_API_KEY)

app = FastAPI(title="Groq Real-Time AI Chatbot")

@app.get("/")
async def get_root():
    """Serves the frontend testing interface."""
    html_path = os.path.join("static", "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h3>Error: static/index.html not found.</h3>", status_code=404)


@app.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket client connected.")

    conversation_history = [
        {"role": "system", "content": "You are a helpful, concise AI assistant powered by Groq and Llama."}
    ]

    try:
        while True:
            user_prompt = await websocket.receive_text()
            if not user_prompt.strip():
                continue
            
            logger.info(f"User prompt received: {user_prompt}")
            conversation_history.append({"role": "user", "content": user_prompt})

            stream = groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=conversation_history,
                stream=True
            )

            full_assistant_reply = ""
            for chunk in stream:
                token = chunk.choices[0].delta.content or ""
                if token:
                    full_assistant_reply += token
                    await websocket.send_text(token)

            conversation_history.append({"role": "assistant", "content": full_assistant_reply})
            await websocket.send_text("[[END_OF_STREAM]]")

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected gracefully.")
    except Exception as e:
        logger.error(f"Error occurred during chat stream: {str(e)}")
        try:
            await websocket.send_text(f"\n[Error: {str(e)}]")
            await websocket.send_text("[[END_OF_STREAM]]")
        except Exception:
            pass