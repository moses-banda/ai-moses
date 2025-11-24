# ai-moses
who answered my call?
# AI Moses - Personal Voice Agent

A voice agent that answers your phone calls as you, with your voice, personality, and real-time context awareness.

## Features
- 🎙️ Custom voice cloning (your voice)
- 🧠 Personal language model (your tone, vocabulary, speech patterns)
- 📞 Twilio integration (answers calls automatically)
- 💾 PostgreSQL database (caller profiles, conversation history)
- 🔄 Dynamic status updates (tells callers what you're doing)
- 👤 Caller-specific responses (different tone for mom vs recruiter vs friend)

## Setup

### Prerequisites
- Python 3.9+
- PostgreSQL
- Twilio account
- OpenAI API key
- ngrok

### Installation

1. Clone the repo:
```bash
git clone https://github.com/moses-banda/ai-moses.git
cd ai-moses
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

5. Initialize database:
```bash
psql -U postgres -d ai_moses -f db/schema.sql
```

6. Run the server:
```bash
python src/main.py
```

7. In another terminal, expose with ngrok:
```bash
ngrok http 5000
```

## Project Structure
```
ai-moses/
├── src/                 # Main application code
├── config/              # Configuration files
├── db/                  # Database schemas
├── training_data/       # Your voice samples & transcripts
├── logs/                # Call logs
├── scripts/             # Utility scripts
└── tests/               # Unit tests
```
```

**`src/__init__.py`** (empty file):
```
# src package
```

**`config/__init__.py`** (empty file):
```
# config package
```

**`.env.example`** (template, so others know what env vars needed):
```

