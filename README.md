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

5. Initialize the database:
   ```bash
   python -m app.db
   ```
   
   This creates the SQLite database file (`parody.db`) and sets up the necessary tables.

## Running Locally

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Available Endpoints:

- `GET /health` - Health check endpoint
- `GET /articles` - Retrieve recent tragedy articles from database
  - Optional query param: `?limit=50` (max 100)
- `POST /poll` - Manually trigger headline polling
- `GET /docs` - Interactive API documentation (Swagger UI)

The application automatically polls for headlines every 5 minutes and stores tragedy-related articles in the database.

## API Keys Configuration

The application uses environment variables for API keys. These are loaded from a `.env` file in the project root.

### Required API Keys:

- **NEWSAPI_KEY**: Your NewsAPI key for fetching news headlines
  - Get your free API key from https://newsapi.org/
  - The app will fallback to RSS feeds if NewsAPI is unavailable

### Firebase Configuration (for push notifications):

- `FIREBASE_CREDENTIALS`: Path to Firebase service account credentials JSON
  - Default: `serviceAccountKey.json` in project root
  - Can be customized via environment variable

Example `.env` file:

```
NEWSAPI_KEY=your_newsapi_key_here
FIREBASE_CREDENTIALS=serviceAccountKey.json
```

## Firebase Setup for Push Notifications

To enable push notifications, you need to set up Firebase:

1. **Create a Firebase Project:**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Click "Create a project"
   - Follow the setup wizard

2. **Generate Service Account Key:**
   - In Firebase Console, go to Project Settings > Service Accounts
   - Click "Generate new private key"
   - Download the JSON file
   - Save it as `serviceAccountKey.json` in your project root

3. **Enable Cloud Messaging:**
   - In Firebase Console, go to Cloud Messaging
   - Note your project's Sender ID and Server Key for client configuration

4. **Configure Topics:**
   - The app uses the topic "tragedies" for broadcasting notifications
   - All clients should subscribe to this topic to receive notifications

**Note:** Without Firebase configuration, the app will still function but won't send push notifications.

## Database

The application uses SQLite for data persistence with SQLAlchemy ORM.

- **Database file**: `parody.db` (created automatically on first run)
- **Article model**: Stores headline, URL, and detection timestamp
- **Automatic deduplication**: Articles are uniquely identified by URL

To reset the database, simply delete `parody.db` and restart the application.

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