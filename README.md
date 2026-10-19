# Real-Time Groq AI Chatbot

An event-driven, high-performance WebSocket backend built with **FastAPI**, **Uvicorn**, and the **Groq Python SDK** (`llama-3.1-8b-instant` model), featuring real-time token streaming and active conversation memory.

---

## Features
- **Real-Time Token Streaming:** Words stream token-by-token instantly via WebSockets for a smooth typing experience.
- **Session Memory:** Tracks conversation history per active WebSocket session so the AI remembers context.
- **Secure Configuration:** Enforces environment variable loading (`python-dotenv`) and raises a startup error if the API key is missing.
- **Clean Architecture:** Separates backend FastAPI routing from frontend static HTML files.

---

## Project Structure
```text
groq-realtime-chatbot/
│
├── .env                  # Environment secrets (ignored by git)
├── .gitignore            # Git exclusion rules
├── requirements.txt      # Explicit project dependencies
├── README.md             # Project documentation
├── main.py               # FastAPI backend & WebSocket handler
└── static/
    └── index.html        # Frontend chat interface