import os
import requests
import feedparser
from typing import List, Dict, Optional


def fetch_from_newsapi() -> Optional[List[Dict[str, str]]]:
    """
    Fetch headlines from NewsAPI using the API key from environment.
    
    Returns:
        List of dicts with 'title' and 'url' keys, or None if request fails.
    """
    api_key = os.getenv('NEWSAPI_KEY')
    
    if not api_key:
        print("Warning: NEWSAPI_KEY not found in environment variables")
        return None
    
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            'apiKey': api_key,
            'country': 'us',
            'pageSize': 20
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('status') != 'ok':
            print(f"NewsAPI returned status: {data.get('status')}")
            return None
        
        articles = data.get('articles', [])
        headlines = []
        
        for article in articles:
            if article.get('title') and article.get('url'):
                headlines.append({
                    'title': article['title'],
                    'url': article['url']
                })
        
        return headlines
        
    except requests.RequestException as e:
        print(f"Error fetching from NewsAPI: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error with NewsAPI: {e}")
        return None


def fetch_from_rss() -> List[Dict[str, str]]:
    """
    Fetch headlines from BBC and CNN RSS feeds.
    
    Returns:
        List of dicts with 'title' and 'url' keys.
    """
    rss_feeds = [
        'http://feeds.bbci.co.uk/news/rss.xml',
        'http://rss.cnn.com/rss/cnn_topstories.rss'
    ]
    
    headlines = []
    
    for feed_url in rss_feeds:
        try:
            feed = feedparser.parse(feed_url)
            
            if feed.bozo:
                print(f"Warning: Error parsing feed {feed_url}: {feed.bozo_exception}")
                continue
            
            for entry in feed.entries[:10]:  # Limit to 10 items per feed
                if hasattr(entry, 'title') and hasattr(entry, 'link'):
                    headlines.append({
                        'title': entry.title,
                        'url': entry.link
                    })
                    
        except Exception as e:
            print(f"Error fetching RSS feed {feed_url}: {e}")
            continue
    
    return headlines


def fetch_headlines() -> List[Dict[str, str]]:
    """
    Fetch headlines from NewsAPI with RSS fallback.
    
    First attempts to fetch from NewsAPI. If that fails,
    falls back to fetching from RSS feeds.
    
    Returns:
        List of dicts with 'title' and 'url' keys.
    """
    # Try NewsAPI first
    headlines = fetch_from_newsapi()
    
    if headlines:
        print(f"Fetched {len(headlines)} headlines from NewsAPI")
        return headlines
    
    # Fallback to RSS feeds
    print("NewsAPI failed, falling back to RSS feeds")
    headlines = fetch_from_rss()
    print(f"Fetched {len(headlines)} headlines from RSS feeds")
    
    return headlines