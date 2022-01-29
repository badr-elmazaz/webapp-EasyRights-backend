import logging

from fillpdf import fillpdfs
from uuid import uuid4
import os
from config import *
from pathlib import Path

#setting logger
#setting logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
Path(os.path.join(os.getcwd(), "logs")).mkdir(parents=True, exist_ok=True)
file_handler = logging.FileHandler(os.path.join(os.getcwd(), "logs", "edit_pdf.log"))
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
logger.addHandler(file_handler)
file_handler.setFormatter(formatter)

def create_pdf(data: list[dict]):
    if data:
        data_dict={}
        file_name = str(uuid4()) + ".pdf"
        path_to_file = os.path.join(os.getcwd(), "web_app", "tmp", file_name)
        for d in data:
            data_dict.update(d["answer"])
        modulo_path=os.path.join(os.getcwd(), "web_app", "static", "modulo.pdf")
        fillpdfs.write_fillable_pdf(modulo_path, path_to_file, data_dict)
        file_name2 = str(uuid4()) + ".pdf"
        path_to_file2 = os.path.join(os.getcwd(), "static_download", file_name2)
        fillpdfs.flatten_pdf(path_to_file, path_to_file2)
        try:
            os.unlink(path_to_file)
        except:
            logger.error(f"can't delete file {path_to_file}")
        logger.info(f"File created: {file_name2}")
        return file_name2

