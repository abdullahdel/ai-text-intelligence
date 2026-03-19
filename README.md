# AI Text Intelligence

AI Text Intelligence is a fullstack web application for AI-powered text and document analysis.

Users can either enter text manually or upload `.txt` and text-based `.pdf` files for analysis. The backend processes the extracted content using the OpenAI API, stores the generated result in PostgreSQL, and provides access to previous analyses through a history and detail view.

The project demonstrates production-oriented backend concepts such as layered architecture, database persistence, connection pooling, structured logging, centralized error handling, request/response validation with FastAPI and Pydantic, file upload handling, unit and API testing, containerized local setup with Docker, and deployment of a fullstack application.

---

## Screenshot

![Application Screenshot](screenshot.png)

---

## Features

- AI-powered text analysis using the OpenAI API
- Manual text input
- `.txt` file upload support
- Text-based `.pdf` file upload support
- Fullstack web application with a custom frontend interface
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
- Source metadata tracking for analyses:
  - `manual` for text input
  - `file` for uploaded documents
- Improved UI with a clearer layout and scrollable result view
- Docker support for a containerized local setup
- Deployment on Render
- Unit tests for the service layer
- API tests for FastAPI endpoints

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

### Deployment / Tooling
- Render
- Docker

---

## Architecture

The backend follows a layered architecture:

- **API layer** for request handling and endpoint definitions
- **Service layer** for analysis logic and orchestration
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
- Separation of concerns through a service layer
- Containerized local setup with Docker

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
│   │   ├── analysis_service.py
│   │   └── analyzer.py
│   ├── utils/
│   │   ├── error_handler.py
│   │   └── logger.py
│   └── main.py
├── static/
│   └── index.html
├── tests/
│   ├── test_analysis_service.py
│   └── test_api.py
├── .dockerignore
├── .gitignore
├── .python-version
├── Dockerfile
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

Analyzes user-provided text entered manually through the frontend.

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

### `POST /upload-analyze`

Accepts a document upload, extracts its text content, and analyzes it using the same backend analysis flow.

#### Supported Input
- `.txt`
- text-based `.pdf`

#### Request
Multipart form-data with a file field named `file`.

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

Returns a single analysis entry by its ID, including source metadata.

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

- text input for manual analysis
- `.txt` and `.pdf` file upload for document-based analysis
- result display area
- analysis history list
- clickable detail view for previous analyses
- pagination with **Previous** and **Next**
- delete button for removing stored analyses
- reload button for refreshing history
- improved layout with a dedicated result panel and history panel
- document source display in history and detail view

---

## Stored Analysis Metadata

Each stored analysis includes:

- `input_text`
- `analysis`
- `source_type`
- `source_name`
- `created_at`

### Source Types
- `manual` → text entered directly in the textarea
- `file` → text extracted from an uploaded `.txt` or `.pdf` file

This allows the frontend to distinguish between manual input and uploaded file analyses in the history view and detail view.

---

## Environment Variables

Create a `.env` file in the project root and define the following variables:

```env
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=your_postgresql_connection_string
```

---

## Python Version

This project is pinned to Python 3.11.9 via:

```text
.python-version
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

## Docker Support

The project also includes Docker support for a containerized local setup.

### Build the image

```bash
docker build -t ai-text-intelligence .
```

### Run the container

```powershell
docker run -p 8000:8000 -e OPENAI_API_KEY="your_openai_api_key" -e DATABASE_URL="your_postgresql_connection_string" ai-text-intelligence
```

Then open:

```text
http://localhost:8000
```

---

## Testing

The project includes both **unit tests** and **API tests**.

### Test Coverage

- **Service-layer unit tests**
  - validate the logic in `analysis_service.py`
  - test success and error cases
  - use mocked dependencies instead of real OpenAI or database calls

- **API tests**
  - validate FastAPI endpoints and HTTP behavior
  - cover request handling, status codes, responses, upload behavior, and error cases

### Run tests

Install test dependencies locally if needed:

```bash
pip install pytest
```

Run all tests:

```bash
python -m pytest -q
```

Run only service-layer unit tests:

```bash
python -m pytest tests/test_analysis_service.py -q
```

Run only API tests:

```bash
python -m pytest tests/test_api.py -q
```

## Live Deployment

The project is deployed on Render:

**Live API / Demo:**  
https://ai-text-intelligence-api.onrender.com

---

## What This Project Demonstrates

This project was built to demonstrate practical backend engineering skills, including:

- API design and implementation
- AI API integration
- document upload handling for `.txt` and `.pdf` files
- database persistence with PostgreSQL
- connection pooling
- structured logging
- centralized error handling
- request and response validation
- pagination
- delete operations
- layered backend architecture
- service layer refactoring
- source metadata tracking
- unit testing for service logic
- API testing for FastAPI routes
- deployment of a fullstack application
- containerized local setup with Docker

---

## Author

**Abdullah Talal**  
B.Sc. Computer Science, LMU Munich