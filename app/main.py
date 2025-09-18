from fastapi import FastAPI, BackgroundTasks
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import asyncio
from typing import Dict, List

from app.news_fetcher import fetch_headlines
from app.filters import is_tragedy
from app.db import init_db, save_article, get_recent_articles, get_article_count

# Load environment variables from .env file
load_dotenv()

# Global flag to control polling
polling_active = False
polling_task = None


async def poll_headlines():
    """Background task to poll headlines and filter for tragedies"""
    global polling_active
    
    while polling_active:
        try:
            # Fetch headlines
            headlines = fetch_headlines()
            
            # Filter for tragedies and save to database
            new_articles = 0
            for headline in headlines:
                if is_tragedy(headline['title']):
                    article = save_article(headline['title'], headline['url'])
                    if article:
                        new_articles += 1
                        print(f"Saved tragedy article: {headline['title'][:50]}...")
            
            if new_articles > 0:
                print(f"Saved {new_articles} new tragedy articles to database")
            
            # Wait 5 minutes before next poll
            await asyncio.sleep(300)
            
        except Exception as e:
            print(f"Error in polling task: {e}")
            await asyncio.sleep(60)  # Wait 1 minute on error


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    global polling_active, polling_task
    
    # Startup
    print("Initializing database...")
    init_db()
    print(f"Database ready. Current article count: {get_article_count()}")
    
    # Start polling in background
    polling_active = True
    polling_task = asyncio.create_task(poll_headlines())
    print("Started headline polling task")
    
    yield
    
    # Shutdown
    polling_active = False
    if polling_task:
        polling_task.cancel()
        try:
            await polling_task
        except asyncio.CancelledError:
            pass
    print("Stopped headline polling task")


app = FastAPI(lifespan=lifespan, title="Parody News App")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/articles")
async def get_articles(limit: int = 50) -> Dict:
    """
    Get recent tragedy articles from database
    
    Args:
        limit: Maximum number of articles to return (default 50, max 100)
    """
    # Limit to reasonable maximum
    limit = min(limit, 100)
    
    articles = get_recent_articles(limit)
    
    return {
        "count": len(articles),
        "total_in_db": get_article_count(),
        "articles": [
            {
                "id": article.id,
                "title": article.title,
                "url": article.url,
                "detected_at": article.detected_at.isoformat()
            }
            for article in articles
        ]
    }


@app.post("/poll")
async def trigger_poll(background_tasks: BackgroundTasks) -> Dict:
    """Manually trigger a headline poll"""
    
    async def poll_once():
        try:
            headlines = fetch_headlines()
            new_articles = 0
            
            for headline in headlines:
                if is_tragedy(headline['title']):
                    article = save_article(headline['title'], headline['url'])
                    if article:
                        new_articles += 1
            
            print(f"Manual poll: saved {new_articles} new articles")
            return new_articles
            
        except Exception as e:
            print(f"Error in manual poll: {e}")
            return 0
    
    background_tasks.add_task(poll_once)
    
    return {
        "message": "Poll triggered",
        "current_article_count": get_article_count()
    }