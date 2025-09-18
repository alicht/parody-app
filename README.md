# Parody App

A FastAPI-based parody news application.

## Setup Instructions

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Locally

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

You can check the health status at: `http://localhost:8000/health`

API documentation will be available at: `http://localhost:8000/docs`

## API Keys

Configure the following API keys as environment variables:

- `NEWS_API_KEY`: Your NewsAPI key (get from https://newsapi.org/)
- `FIREBASE_CREDENTIALS`: Path to Firebase service account credentials JSON
- Additional API keys as needed

Create a `.env` file in the project root and add your keys:

```
NEWS_API_KEY=your_key_here
FIREBASE_CREDENTIALS=path/to/credentials.json
```

## Development

Run tests:
```bash
pytest
```