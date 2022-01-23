from fastapi import FastAPI, Request
import uvicorn
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/")
@limiter.limit("5/minute")
async def homepage(request: Request):
    return "Hey"


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8636)