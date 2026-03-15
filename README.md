# AI Text Intelligence

AI Text Intelligence is a fullstack web application for AI-powered text analysis.

Users can submit text through a simple web interface, the backend processes the request using the OpenAI API, stores the generated result in PostgreSQL, and provides access to previous analyses through a REST API and a history view.

The project was built to demonstrate production-oriented backend concepts such as layered architecture, database persistence, connection pooling, structured logging, centralized error handling, request/response validation with FastAPI and Pydantic, and deployment of a fullstack application.

---

## Screenshot

![Application Screenshot](screenshot.png)

---

## Features

- AI-powered text analysis using the OpenAI API
- Fullstack web application with a simple frontend interface
- Frontend served directly by FastAPI
- REST API built with FastAPI
- PostgreSQL database for persistent storage
- Database connection pooling with `psycopg2.pool.SimpleConnectionPool`
- Request and response validation with Pydantic
- Pagination support for analysis history using `limit` and `offset`
- Centralized error handling
- Structured logging across API, service, and database layers
- Clickable history view for previous analyses
- Detail view for individual analyses
- Delete functionality for stored analyses
- Deployment on Render

---

## Tech Stack

### Backend
- Python
- FastAPI
- PostgreSQL
- psycopg2
- Pydantic
- OpenAI API

### Frontend
- HTML
- CSS
- JavaScript
- Fetch API

### Deployment
- Render

---

## Architecture

The backend follows a layered architecture:

- **API layer** for request handling and endpoint definitions
- **Service layer** for analysis logic and OpenAI integration
- **Database layer** for persistence and retrieval
- **PostgreSQL** as the persistent storage layer

### Core backend concepts demonstrated in this project

- REST API design with FastAPI
- Request and response validation with Pydantic
- PostgreSQL persistence
- Connection pooling
- Structured logging
- Centralized exception handling
- Pagination with `limit` and `offset`

---

## Project Structure

```text
ai-text-intelligence/
├── app/
│   ├── database/
│   │   └── database.py
│   ├── models/
│   │   └── models.py
│   ├── services/
│   │   └── analyzer.py
│   ├── utils/
│   │   ├── error_handler.py
│   │   └── logger.py
│   └── main.py
├── static/
│   └── index.html
├── .gitignore
├── README.md
├── requirements.txt
├── runtime.txt
└── screenshot.png
```

---

## API Endpoints

### `GET /`

Serves the frontend UI.

---

### `POST /analyze`

Analyzes user-provided text using the OpenAI API and stores the result in the database.

#### Request
```json
{
  "text": "Your text here"
}
```

#### Example Response
```json
{
  "analysis": "Generated analysis result"
}
```

---

### `GET /analyses`

Returns previously stored analyses with pagination support.

#### Example
```http
GET /analyses?limit=5&offset=0
```

---

### `GET /analyses/{id}`

Returns a single analysis entry by its ID.

#### Example
```http
GET /analyses/1
```

---

### `DELETE /analyses/{id}`

Deletes a stored analysis entry by its ID.

#### Example
```http
DELETE /analyses/1
```

#### Example Response
```json
{
  "message": "Analysis deleted"
}
```

---

## Frontend Functionality

The frontend provides:

- text input for submitting analyses
- result display area
- analysis history list
- clickable detail view for previous analyses
- pagination with **Previous** and **Next**
- delete button for removing stored analyses
- reload button for refreshing history

---

## Environment Variables

Create a `.env` file in the project root and define the following variables:

```env
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=your_postgresql_connection_string
```

---

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/abdullahdel/ai-text-intelligence.git
cd ai-text-intelligence
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root and add:

```env
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=your_postgresql_connection_string
```

### 4. Start the application

```bash
uvicorn app.main:app --reload
```

### 5. Open the application

```text
http://127.0.0.1:8000
```

---

## Live Deployment

The project is deployed on Render:

**Live API / Demo:**  
https://ai-text-intelligence-api.onrender.com

---

## What This Project Demonstrates

This project was built to demonstrate practical backend engineering skills, including:

- API design and implementation
- AI API integration
- database persistence with PostgreSQL
- connection pooling
- structured logging
- centralized error handling
- request and response validation
- pagination
- delete operations
- layered backend architecture
- deployment of a fullstack application

---

## Author

**Abdullah Talal**  
B.Sc. Computer Science, LMU Munich