from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import Like

def create_like(db: Session, user_id: int, tweet_id: int):
    existing = db.query(Like).filter(Like.user_id == user_id, Like.tweet_id == tweet_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tweet already liked by this user")

    like = Like(user_id=user_id, tweet_id=tweet_id)
    db.add(like)
    db.commit()
    db.refresh(like)
    return like

def get_likes_for_tweet(db: Session, tweet_id: int):
    return db.query(Like).filter(Like.tweet_id == tweet_id).all()
