from datetime import datetime
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# This will store logs in memory
request_logs = []

class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_logs.append({
            "time": datetime.utcnow().isoformat(),
            "method": request.method,
            "path": request.url.path
        })
        return await call_next(request)

def get_logs():
    return request_logs
