from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime
import models, schemas

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- USER FUNCTIONS ---

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(models.User).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def search_users_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username.ilike(f"%{username}%")).all()


# --- TWEET FUNCTIONS ---

def create_tweet(db: Session, tweet: schemas.TweetCreate, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_tweet = models.Tweet(
        content=tweet.content,
        owner_id=user_id
    )
    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)
    return db_tweet

def get_tweets(db: Session):
    return db.query(models.Tweet).all()

def get_tweets_by_user(db: Session, user_id: int):
    return db.query(models.Tweet).filter(models.Tweet.owner_id == user_id).all()

def update_tweet(db: Session, tweet_id: int, content: str):
    tweet = db.query(models.Tweet).filter(models.Tweet.id == tweet_id).first()
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    tweet.content = content
    tweet.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(tweet)
    return tweet

def delete_tweet(db: Session, tweet_id: int):
    tweet = db.query(models.Tweet).filter(models.Tweet.id == tweet_id).first()
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    db.delete(tweet)
    db.commit()
    return tweet

def search_tweets(db: Session, query: str):
    return db.query(models.Tweet).filter(models.Tweet.content.ilike(f"%{query}%")).all()

def search_hashtags(db: Session, tag: str):
    pattern = f"%#{tag.lower()}%"
    return db.query(models.Tweet).filter(models.Tweet.content.ilike(pattern)).all()


# --- LIKE FUNCTION ---

def like_tweet(db: Session, user_id: int, tweet_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    tweet = db.query(models.Tweet).filter(models.Tweet.id == tweet_id).first()

    if not user or not tweet:
        raise HTTPException(status_code=404, detail="User or Tweet not found")

    existing_like = db.query(models.Like).filter_by(user_id=user_id, tweet_id=tweet_id).first()
    if existing_like:
        raise HTTPException(status_code=400, detail="Tweet already liked")

    like = models.Like(user_id=user_id, tweet_id=tweet_id)
    db.add(like)
    db.commit()
    db.refresh(like)
    return like
