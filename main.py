import logging
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
from _config import *
from web_app.edit_pdf import create_pdf
from time import sleep
from fastapi_utils.tasks import repeat_every
from pathlib import Path
import arrow

# todo hide /docs route
# todo insert logs

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


@app.on_event("startup")
@repeat_every(seconds=60 * 30)
def remove_files():
    logging.info("APP STARTED")
    Path(os.path.join(os.getcwd(), "static_download")).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(os.getcwd(), "web_app", "tmp")).mkdir(parents=True, exist_ok=True)
    files_path = os.path.join(os.getcwd(), "static_download")
    files_path_tmp = os.path.join(os.getcwd(), "web_app", "tmp")

    now = arrow.now()
    # now = arrow.now().shift(hours=+20)

    for file in Path(files_path).glob('*'):
        if file.is_file():
            file_time = arrow.get(file.stat().st_mtime)
            if file_time < now:
                try:
                    os.unlink(file.absolute())
                except:
                    logging.error(f"can't delete file {file.absolute()}")

    for file in Path(files_path_tmp).glob('*'):
        if file.is_file():
            file_time = arrow.get(file.stat().st_mtime)
            if file_time < now:
                try:
                    os.unlink(file.absolute())
                except:
                    logging.error(f"can't delete file {file.absolute()}")



@app.post("/create-pdf")
# @limiter.limit("10/minute")
async def homepage(request: Request):
    data = await request.json()
    value = "files/" + create_pdf(data)
    return value
    # json_compatible_item_data = jsonable_encoder(value)
    # return JSONResponse(content=json_compatible_item_data)




def remove_file(path: str) -> None:
    sleep(60)
    try:
        os.unlink(path)
    except:
        logging.error(f"can't delete file {path.absolute()}")


@app.get("/files/{filename}")
async def file(request: Request, filename, background_tasks: BackgroundTasks):
    path_to_file = os.path.join(os.getcwd(), "static_download", filename)

    if not isfile(path_to_file):
        return Response(status_code=404)

    response = FileResponse(path_to_file, media_type='application/octet-stream', filename=filename)
    background_tasks.add_task(remove_file, path_to_file)
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8637)
