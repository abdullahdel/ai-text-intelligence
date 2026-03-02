# AI Text Intelligence

AI Text Intelligence is a minimal backend application built with FastAPI that analyzes text using OpenAI's API.

The application:
- Accepts text via a REST API
- Sends the text to OpenAI for analysis
- Returns sentiment and a short summary
- Handles basic error cases (empty input, API errors)

This project is built as part of a structured backend learning process.

---

## Tech Stack

- Python 3.11+
- FastAPI
- Uvicorn
- OpenAI API
- python-dotenv

---

## Project Structure

ai-text-intelligence/
│
├── app/
│   ├── main.py
│   ├── models.py
│   └── services/
│       └── analyzer.py
│
├── .env (not tracked)
├── requirements.txt
└── README.md

---

## Setup

1. Clone repository

git clone <your-repo-url>
cd ai-text-intelligence

2. Create virtual environment

python -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows

3. Install dependencies

pip install -r requirements.txt

4. Create `.env` file in project root

OPENAI_API_KEY=your_openai_key_here

5. Start server

uvicorn app.main:app --reload

Server runs at:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs

---

## API Endpoints

### GET /

Returns API status.

Response:

{
"status": "running"
}

---

### POST /analyze

Request body:

{
"text": "Your text here"
}

Response:

{
"analysis": "Stimmung: positiv. Zusammenfassung: ..."
}

Error example:

{
"error": "Text darf nicht leer sein."
}

---
### GET /analyses

Returns the most recent analyses (limited to 10 by default).

Response example:

[
{
"id": 3,
"input_text": "Hello world",
"analysis": "Stimmung: positiv...",
"created_at": "2026-03-02 14:21:03"
}
]

### GET /analyses/{id}

Returns a single analysis by ID.

Response example:

{
"id": 3,
"input_text": "Hello world",
"analysis": "Stimmung: positiv...",
"created_at": "2026-03-02 14:21:03"
}

If the ID does not exist, the API returns:

Status code: 404

## Error Handling

The application handles:
- Empty input validation
- OpenAI API errors (try/except)
- Environment variable loading

---

## Future Improvements

- Database integration (SQLite)
- Request history endpoint
- Async implementation
- Deployment (Render / Railway)