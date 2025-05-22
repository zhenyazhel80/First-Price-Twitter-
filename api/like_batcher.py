import time
from threading import Thread, Lock
import models

like_buffer = {}  # tweet_id: {"likes": count, "time": timestamp}
lock = Lock()
FLUSH_INTERVAL = 10  # seconds

def add_like(tweet_id: int):
    with lock:
        if tweet_id not in like_buffer:
            like_buffer[tweet_id] = {"likes": 1, "time": time.time()}
        else:
            like_buffer[tweet_id]["likes"] += 1

def flush_likes_to_db(db):
    with lock:
        to_flush = {}
        now = time.time()
        for tweet_id, data in list(like_buffer.items()):
            if data["likes"] > 10 or now - data["time"] > 60:
                to_flush[tweet_id] = data
                del like_buffer[tweet_id]

    for tweet_id, data in to_flush.items():
        tweet = db.query(models.Tweet).filter(models.Tweet.id == tweet_id).first()
        if tweet:
            tweet.likes += data["likes"]
            db.commit()

def start_batch_flusher(get_db_func):
    def flusher():
        while True:
            db = next(get_db_func())
            flush_likes_to_db(db)
            db.close()
            time.sleep(FLUSH_INTERVAL)

    thread = Thread(target=flusher, daemon=True)
    thread.start()
