# Deployment Guide

This guide covers deploying the Parody App backend to Fly.io or running it with Docker.

## Prerequisites

- Docker installed locally
- Fly.io CLI (`flyctl`) installed for Fly.io deployment
- Environment variables configured in `.env` file

## Local Docker Testing

Build and run the Docker container locally:

```bash
# Build the image
docker build -t parody-app .

# Run the container
docker run -p 8000:8000 \
  -e NEWSAPI_KEY=your_api_key \
  -v $(pwd)/parody.db:/app/data/parody.db \
  -v $(pwd)/serviceAccountKey.json:/app/serviceAccountKey.json \
  parody-app
```

Test the API at http://localhost:8000/docs

## Deploying to Fly.io

### 1. Install Fly.io CLI

```bash
# macOS
brew install flyctl

# Or download from https://fly.io/install
```

### 2. Login to Fly.io

```bash
flyctl auth login
```

### 3. Launch the App

```bash
# Initialize the app (first time only)
flyctl launch

# Or deploy existing configuration
flyctl deploy
```

### 4. Set Secrets

```bash
# Set environment variables as secrets
flyctl secrets set NEWSAPI_KEY=your_newsapi_key_here

# For Firebase (upload the file first)
flyctl secrets set FIREBASE_CREDENTIALS=@serviceAccountKey.json
```

### 5. Create Persistent Volume

```bash
# Create volume for SQLite database
flyctl volumes create parody_data --size 1
```

### 6. Deploy

```bash
flyctl deploy
```

### 7. Monitor

```bash
# View logs
flyctl logs

# Check app status
flyctl status

# Open app in browser
flyctl open
```

## Deployment Features

The deployment configuration includes:

- **Automatic Polling**: The scheduler runs continuously, polling every 5 minutes
- **Persistent Database**: SQLite database stored in mounted volume
- **Health Checks**: Regular health endpoint monitoring
- **Auto-scaling**: Configured with soft/hard connection limits
- **HTTPS**: Automatic SSL/TLS with forced HTTPS redirect

## Environment Variables

Required environment variables for production:

- `NEWSAPI_KEY`: Your NewsAPI key for fetching headlines
- `FIREBASE_CREDENTIALS`: Path to Firebase service account JSON (optional)

## Database Persistence

The SQLite database is stored in `/app/data/` which is mounted to a persistent volume on Fly.io. This ensures data persists across deployments.

## Scheduler Operation

The Dockerfile runs both:
1. The FastAPI web server (port 8000)
2. The polling scheduler (python -m app.main)

Both processes share the same SQLite database for consistency.

## Troubleshooting

### Check Logs

```bash
flyctl logs --tail
```

### SSH into Container

```bash
flyctl ssh console
```

### Reset Database

```bash
flyctl ssh console -C "rm /app/data/parody.db"
flyctl restart
```

### Update Secrets

```bash
flyctl secrets list
flyctl secrets unset SECRET_NAME
flyctl secrets set SECRET_NAME=new_value
```

## Alternative: Render Deployment

If using Render instead of Fly.io:

1. Create `render.yaml`:

```yaml
services:
  - type: web
    name: parody-app
    env: docker
    plan: free
    healthCheckPath: /health
    envVars:
      - key: NEWSAPI_KEY
        sync: false
    disk:
      name: data
      mountPath: /app/data
      sizeGB: 1
```

2. Connect GitHub repo to Render
3. Set environment variables in Render dashboard
4. Deploy

## Monitoring

- Health endpoint: `https://your-app.fly.dev/health`
- Articles endpoint: `https://your-app.fly.dev/articles`
- API docs: `https://your-app.fly.dev/docs`

The app will automatically start polling for news and sending notifications once deployed.