from datetime import datetime
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, DateTime, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Create base class for models
Base = declarative_base()

# Database configuration
import os
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///parody.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Article(Base):
    """Article model for storing news headlines"""
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)
    detected_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Article(id={self.id}, title='{self.title[:30]}...')>"


def init_db():
    """Initialize the database and create tables"""
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully")


def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    except Exception:
        db.close()
        raise


def save_article(title: str, url: str) -> Optional[Article]:
    """
    Save a new article to the database.
    
    Args:
        title: Article title
        url: Article URL
        
    Returns:
        The saved Article object, or None if article already exists
    """
    db = SessionLocal()
    try:
        # Check if article already exists
        existing = db.query(Article).filter(Article.url == url).first()
        if existing:
            return None
        
        # Create and save new article
        article = Article(title=title, url=url)
        db.add(article)
        db.commit()
        db.refresh(article)
        return article
        
    except Exception as e:
        db.rollback()
        print(f"Error saving article: {e}")
        return None
    finally:
        db.close()


def get_recent_articles(limit: int = 50) -> List[Article]:
    """
    Get the most recent articles from the database.
    
    Args:
        limit: Maximum number of articles to return (default 50)
        
    Returns:
        List of Article objects ordered by detected_at descending
    """
    db = SessionLocal()
    try:
        articles = db.query(Article).order_by(desc(Article.detected_at)).limit(limit).all()
        return articles
    except Exception as e:
        print(f"Error fetching articles: {e}")
        return []
    finally:
        db.close()


def get_article_count() -> int:
    """Get total number of articles in database"""
    db = SessionLocal()
    try:
        count = db.query(Article).count()
        return count
    except Exception as e:
        print(f"Error counting articles: {e}")
        return 0
    finally:
        db.close()


# Initialize database tables when module is imported
if __name__ == "__main__":
    init_db()
    print(f"Database initialized. Current article count: {get_article_count()}")