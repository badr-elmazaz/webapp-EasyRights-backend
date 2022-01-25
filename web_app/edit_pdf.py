from fillpdf import fillpdfs
from uuid import uuid4
import os


def create_pdf(data: list[dict]):
    print(data)
    data_dict={}
    file_name = str(uuid4()) + ".pdf"
    path_to_file = ".\\static_download\\"
    path_to_file=path_to_file+file_name
    for d in data:
        data_dict.update(d["answer"])
    fillpdfs.write_fillable_pdf(r".\web_app\static\modulo.pdf", path_to_file, data_dict)
    file_name2 = str(uuid4()) + ".pdf"
    path_to_file2 = os.path.join(os.getcwd(), "static_download", file_name2)
    print(file_name2)
    fillpdfs.flatten_pdf(path_to_file, path_to_file2)
    try:
        os.unlink(path_to_file)
    except:
        pass
    return file_name2

if __name__ == "__main__":
    fillpdfs.print_form_fields(r".\static\modulo.pdf")