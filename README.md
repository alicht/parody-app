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

4. Set up environment variables:
   Create a `.env` file in the project root and add your NewsAPI key:
   ```
   NEWSAPI_KEY=your_newsapi_key_here
   ```
   
   Get your free API key from https://newsapi.org/

## Running Locally

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

You can check the health status at: `http://localhost:8000/health`

API documentation will be available at: `http://localhost:8000/docs`

## API Keys Configuration

The application uses environment variables for API keys. These are loaded from a `.env` file in the project root.

### Required API Keys:

- **NEWSAPI_KEY**: Your NewsAPI key for fetching news headlines
  - Get your free API key from https://newsapi.org/
  - The app will fallback to RSS feeds if NewsAPI is unavailable

### Optional API Keys:

- `FIREBASE_CREDENTIALS`: Path to Firebase service account credentials JSON (for future features)
- Additional API keys can be added as needed

Example `.env` file:

```
NEWSAPI_KEY=your_newsapi_key_here
FIREBASE_CREDENTIALS=path/to/credentials.json
```

## Testing

Run all tests:
```bash
pytest -v
```

Run tests with coverage:
```bash
pytest --cov=app -v
```

Run specific test file:
```bash
pytest tests/test_filters.py -v
```

The project includes comprehensive test coverage for:
- Content filtering functions (tragedy detection)
- News fetching modules
- API endpoints