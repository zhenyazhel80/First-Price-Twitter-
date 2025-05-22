import time
from typing import Any, Dict
from threading import Lock

cache_store: Dict[str, Dict[str, Any]] = {}  # key: {value, timestamp}
cache_lock = Lock()
CACHE_TTL = 60  # seconds

def get_cache(key: str):
    with cache_lock:
        entry = cache_store.get(key)
        if entry:
            if time.time() - entry["timestamp"] < CACHE_TTL:
                return entry["value"]
            else:
                del cache_store[key]
        return None

def set_cache(key: str, value: Any):
    with cache_lock:
        cache_store[key] = {"value": value, "timestamp": time.time()}
