import logging
from os.path import isfile
import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
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
from logging.handlers import RotatingFileHandler
from config import *

# todo hide /docs route
# todo insert logs


app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# setting logger
logger = logging.getLogger(__name__)
Path(os.path.join(os.getcwd(), "logs")).mkdir(parents=True, exist_ok=True)
log_file = os.path.join(os.getcwd(), "logs", "api.log")
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
my_handler = RotatingFileHandler(log_file, mode='a', maxBytes=1000000,
                                 backupCount=2, encoding="utf-8", delay=0)
# my_handler = RotatingFileHandler(log_file, mode='a', maxBytes=10 * 1024 * 1024,
#                                  backupCount=2, encoding="utf-8", delay=0)
my_handler.setFormatter(formatter)
my_handler.setLevel(logging.INFO)
logger.addHandler(my_handler)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
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
                    logger.error(f"can't delete file {file.absolute()}")

    for file in Path(files_path_tmp).glob('*'):
        if file.is_file():
            file_time = arrow.get(file.stat().st_mtime)
            if file_time < now:
                try:
                    os.unlink(file.absolute())
                except:
                    logger.error(f"can't delete file {file.absolute()}")


@app.post("/create-pdf")
# @limiter.limit("10/minute")
async def pdf(request: Request):
    if not BLOCK_ALL_THEY_DIDNT_PAY_US:
        data = await request.json()
        logger.info(f"Data received: {data}")
        value = "files/" + create_pdf(data)
        return value


def remove_file(path: str) -> None:
    sleep(60)
    try:
        os.unlink(path)
    except:
        logging.error(f"can't delete file {path.absolute()}")


@app.get("/files/{filename}")
async def file(request: Request, filename, background_tasks: BackgroundTasks):
    if not BLOCK_ALL_THEY_DIDNT_PAY_US:
        path_to_file = os.path.join(os.getcwd(), "static_download", filename)

        if not isfile(path_to_file):
            return Response(status_code=404)

        response = FileResponse(path_to_file, media_type='application/octet-stream', filename=filename)
        background_tasks.add_task(remove_file, path_to_file)
        return response

@app.post("/block_all_they_didn_pay_us")
async def block(request: Request):
    BLOCK_ALL_THEY_DIDNT_PAY_US=True
    #todo make redis block it

@app.post("/unlock_this_shit")
async def block(request: Request):
    BLOCK_ALL_THEY_DIDNT_PAY_US=False


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8638)
