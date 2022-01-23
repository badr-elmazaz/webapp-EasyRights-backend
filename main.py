from os.path import isfile

import uvicorn
from fastapi import FastAPI, Request
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
# from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.background import BackgroundTasks
import os
from config import *
from web_app.edit_pdf import create_pdf

# todo hide /docs route

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/create-pdf")
@limiter.limit("8/minute")
async def homepage(request: Request):
    data = await request.json()
    value = "files/" + create_pdf(data)
    return value
    # json_compatible_item_data = jsonable_encoder(value)
    # return JSONResponse(content=json_compatible_item_data)


@app.get("/pdf")
@limiter.limit("8/minute")
async def homepage(request: Request):
    return FileResponse(r".\web_app\static\newflat.pdf", media_type='application/octet-stream',
                        filename="alfredogay.pdf")


def remove_file(path: str) -> None:
    os.unlink(path)


@app.get("/files/{filename}")
async def file(request: Request, filename, background_tasks: BackgroundTasks):
    path_to_file = './static_download/' + filename

    if not isfile(path_to_file):
        return Response(status_code=404)

    response = FileResponse(path_to_file, media_type='application/octet-stream', filename=filename)
    background_tasks.add_task(remove_file, path_to_file)
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8636)
