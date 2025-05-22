from fastapi import FastAPI, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from logger import LoggerMiddleware, get_logs
from cache import get_cache, set_cache

from like import get_likes_for_tweet
from like_batcher import add_like, start_batch_flusher
from logger import LoggerMiddleware

import models, schemas, crud
from database import SessionLocal, engine

# --- Create database tables ---
models.Base.metadata.create_all(bind=engine)

# --- FastAPI app initialization ---
app = FastAPI(
    title="TwitterClone API",
    description="API for managing tweets and users",
    version="1.0",
    openapi_tags=[
        {"name": "Users", "description": "Operations related to user accounts"},
        {"name": "Tweets", "description": "Tweet posting, editing, deleting"},
        {"name": "Search", "description": "Search users, tweets, and hashtags"},
        {"name": "Likes", "description": "Track who liked what"}
    ]
)

# --- Start background batch flusher ---
start_batch_flusher(get_db)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Logger Middleware ---
app.add_middleware(LoggerMiddleware)

# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- USER ROUTES ---
@app.get("/users/", response_model=list[schemas.User], tags=["Users"], summary="List All Accounts")
def read_users(db: Session = Depends(get_db)):
    cache_key = "users_list"
    cached = get_cache(cache_key)
    if cached:
        return cached

    users = crud.get_users(db=db)
    set_cache(cache_key, users)
    return users

@app.post("/users/", response_model=schemas.User, tags=["Users"], summary="Create Account")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User], tags=["Users"], summary="List All Accounts")
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db=db)

@app.get("/users/search/", tags=["Users"], summary="Search for Account")
def search_users(username: str, db: Session = Depends(get_db)):
    return crud.search_users_by_username(db=db, username=username)

@app.post("/login/", tags=["Users"], summary="Login User")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or user.password != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful", "user_id": user.id, "username": user.username}

# --- TWEET ROUTES ---
@app.get("/tweets/", response_model=list[schemas.Tweet], tags=["Tweets"], summary="List All Tweets")
def read_tweets(db: Session = Depends(get_db)):
    cache_key = "tweets_list"
    cached = get_cache(cache_key)
    if cached:
        return cached

    tweets = crud.get_tweets(db=db)
    set_cache(cache_key, tweets)
    return tweets

@app.post("/tweets/", response_model=schemas.Tweet, tags=["Tweets"], summary="Create Tweet")
def create_tweet(tweet: schemas.TweetCreate, user_id: int = Query(...), db: Session = Depends(get_db)):
    return crud.create_tweet(db=db, tweet=tweet, user_id=user_id)

@app.get("/tweets/", response_model=list[schemas.Tweet], tags=["Tweets"], summary="List All Tweets")
def read_tweets(db: Session = Depends(get_db)):
    return crud.get_tweets(db=db)

@app.put("/tweets/{tweet_id}", response_model=schemas.Tweet, tags=["Tweets"], summary="Update Tweet")
def update_tweet(tweet_id: int, tweet: schemas.TweetCreate, db: Session = Depends(get_db)):
    return crud.update_tweet(db=db, tweet_id=tweet_id, content=tweet.content)

@app.delete("/tweets/{tweet_id}", tags=["Tweets"], summary="Delete Tweet")
def delete_tweet(tweet_id: int, db: Session = Depends(get_db)):
    return crud.delete_tweet(db=db, tweet_id=tweet_id)

# --- LIKE ROUTES ---
@app.post("/likes/", tags=["Likes"], summary="Like a Tweet (buffered)")
def like_tweet(tweet_id: int = Body(...)):
    add_like(tweet_id)
    return {"message": "Like buffered."}

@app.get("/likes/{tweet_id}", tags=["Likes"], summary="Get all likes for a tweet")
def get_likes(tweet_id: int, db: Session = Depends(get_db)):
    return get_likes_for_tweet(db, tweet_id)

# --- SEARCH ROUTES ---
@app.get("/tweets/search/", tags=["Search"], summary="Search Tweets")
def search_tweets(q: str, db: Session = Depends(get_db)):
    return crud.search_tweets(db=db, query=q)

@app.get("/hashtags/search/", tags=["Search"], summary="Search Hashtags")
def search_hashtags(tag: str, db: Session = Depends(get_db)):
    return crud.search_hashtags(db=db, tag=tag)

# --- Static files and index ---
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", tags=["Users"], summary="Serve Index Page")
def serve_index():
    return FileResponse("static/index.html")

@app.get("/logs", tags=["Logger"], summary="API request logs")
def logs():
    return get_logs()
