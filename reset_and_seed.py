import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from api import models, database, crud, schemas

# --- SQLite Setup ---
DATABASE_URL = "sqlite:///./sqlitedb.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# --- Delete SQLite file if it exists ---
if os.path.exists("sqlitedb.db"):
    os.remove("sqlitedb.db")
    print("🧹 Old SQLite database deleted.")
else:
    print("⚠️ No existing SQLite database found.")

# --- Recreate tables ---
models.Base.metadata.create_all(bind=engine)
print("📦 SQLite database tables created.")

# --- Users to create ---
users_data = [
    {"username": "user1", "email": "user1@example.com", "password": "Strongpass123!"},
    {"username": "user2", "email": "user2@example.com", "password": "Strongpass123!"},
    {"username": "zhenya1", "email": "zhenya1@example.com", "password": "Strongpass123!"},
    {"username": "zhenya2", "email": "zhenya2@example.com", "password": "Strongpass123!"},
]

# --- Tweets to add ---
tweets_data = {
    "user1": ["Hi, I'm user1!", "Still tweeting..."],
    "user2": ["Tweet tweet", "Life is great!"],
    "zhenya1": ["Testing stuff", "FastAPI forever ❤️"],
}

# --- Open DB session and insert data ---
db: Session = database.SessionLocal()
created_users = {}

# Add users
for u in users_data:
    user_schema = schemas.UserCreate(**u)
    created = crud.create_user(db=db, user=user_schema)
    created_users[u["username"]] = created.id
print("✅ Users created.")

# Add tweets
for username, tweets in tweets_data.items():
    for content in tweets:
        tweet_schema = schemas.TweetCreate(content=content)
        crud.create_tweet(db=db, tweet=tweet_schema, user_id=created_users[username])
print("✅ Tweets added.")

db.close()
print("🌱 Seeding complete!")
