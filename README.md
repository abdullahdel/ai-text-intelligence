# AI Text Intelligence

AI Text Intelligence is a fullstack application that analyzes user-provided text using an AI model and stores the results in a database.  
The project demonstrates a production-style backend built with FastAPI and PostgreSQL, integrated with the OpenAI API.

The application allows users to submit text for analysis, stores the results, and provides a history view of previous analyses through a REST API and a simple frontend interface.

---

## Features

- AI-powered text sentiment and summary analysis
- Integration of OpenAI API for natural language processing
- REST API built with FastAPI
- PostgreSQL database for persistent storage
- Database connection pooling
- Pagination support for analysis history
- Response validation with Pydantic
- Centralized error handling
- Structured logging
- Interactive frontend built with HTML, CSS and JavaScript
- Clickable analysis history
- Detail view for previous analyses

---

## Tech Stack

### Backend
- Python
- FastAPI
- PostgreSQL
- psycopg2
- OpenAI API

### Frontend
- HTML
- CSS
- JavaScript
- Fetch API

---

## Architecture

The project follows a layered backend architecture:

API Layer (FastAPI Endpoints)  
↓  
Service Logic  
↓  
Database Layer  
↓  
PostgreSQL

Key architectural concepts implemented:

- REST API design
- Response validation
- Structured logging
- Connection pooling
- Centralized error handling
- Pagination for API endpoints

---

## API Endpoints

### Analyze text

POST /analyze

Request

{
"text": "Your text here"
}

Response

{
"analysis": "Sentiment: positive. Summary: ..."
}

---

### Get analysis history

GET /analyses

Supports pagination:

GET /analyses?limit=5&offset=0

---

### Get single analysis

GET /analyses/{id}

---

## Screenshot

![Application Screenshot](screenshot.png)

---

## Run locally

Clone repository

git clone https://github.com/abdullahdel/ai-text-intelligence

Install dependencies

pip install -r requirements.txt

Run server

uvicorn app.main:app --reload

Open browser

http://127.0.0.1:8000

---

## Live Demo

https://ai-text-intelligence-api.onrender.com

---

## Author

Abdullah Talal  
LMU Munich – Computer Science