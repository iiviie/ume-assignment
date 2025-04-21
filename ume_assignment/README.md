# UME Assignment - Action Suggester API

A Django-based API service that analyzes text messages using Google's Gemini AI to understand their tone and intent, and suggests relevant actions.

## Features

- Text analysis using Google's Gemini AI
- Action suggestion based on message intent
- Database logging of all queries and analyses
- RESTful API endpoints
- Swagger documentation

## Prerequisites

- Docker and Docker Compose
- PostgreSQL
- Google Gemini API key

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd ume-assignment
```

2. Create a `.env` file in the project root with the following variables:
```env
DJANGO_SECRET_KEY=your_django_secret_key_here
GEMINI_API_KEY=your_gemini_api_key_here
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
```

3. Start the services using Docker Compose:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000/api/analyze`

## API Endpoints

### Analyze Text
- **URL**: `/api/analyze/`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Request Body**:
```json
{
    "query": "Your text message here"
}
```
- **Response**:
```json
{
    "query": "Your text message here",
    "analysis": {
        "tone": "Identified Tone",
        "intent": "Identified Intent"
    },
    "suggested_actions": [
        {
            "action_code": "ACTION_CODE",
            "display_text": "Action Description"
        }
    ]
}
```

### Example using Postman
1. Open Postman
2. Create a new POST request to `http://localhost:8000/api/analyze/`
3. Set the Content-Type header to `application/json`
4. Add the following JSON body:
```json
{
    "query": "I want to order a pizza"
}
```
5. Send the request

## Available Actions

The API can suggest the following actions:
- `ORDER_FOOD`: Order Food Online
- `FIND_RECIPE`: Find Recipes
- `ASK_HELP`: Get Help
- `SHARE_NEWS`: Share News
- `SCHEDULE_MEETING`: Schedule a Meeting
- `SEARCH_INFO`: Search for Information

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DEBUG` | Django debug mode | Yes |
| `DJANGO_SECRET_KEY` | Django secret key | Yes |
| `GEMINI_API_KEY` | Google Gemini API key | Yes |

## LLM Provider

This project uses Google's Gemini AI (specifically the `gemini-2.0-flash-lite` model) for text analysis. To get an API key:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add the key to your `.env` file

## API Documentation

Swagger documentation is available at:
- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`

## Database

The project uses PostgreSQL as the database. The database configuration is handled through Docker Compose, with the following default settings:
- Database name: `action_suggester`
- Username: `postgres`
- Password: `postgres`
- Host: `db`
- Port: `5432`

## Development

To run the project locally without Docker:

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Start the development server:
```bash
python manage.py runserver
``` 