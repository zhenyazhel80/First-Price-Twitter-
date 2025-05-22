import time
from api.like_batcher import like_buffer, add_like, flush_likes_to_db
from api.models import Tweet

class MockDB:
    def __init__(self):
        self.tweets = {}

    def query(self, model):
        return self

    def filter(self, condition):
        self.current_id = condition.right.value
        return self

    def first(self):
        return self.tweets.get(self.current_id)

    def commit(self):
        pass

    def close(self):
        pass

def test_add_and_flush_likes():
    tweet_id = 123
    db = MockDB()
    db.tweets[tweet_id] = Tweet(id=tweet_id, likes=0)

    # Add 11 likes
    for _ in range(11):
        add_like(tweet_id)

    flush_likes_to_db(db)

    assert db.tweets[tweet_id].likes == 11
    assert tweet_id not in like_buffer
