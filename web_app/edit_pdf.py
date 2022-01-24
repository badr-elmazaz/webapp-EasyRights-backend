from fillpdf import fillpdfs
from uuid import uuid4


def create_pdf(data: list[dict]):
    print(data)
    data_dict={}
    file_name = str(uuid4()) + ".pdf"
    path_to_file = "./static_download/"+file_name
    for d in data:
        data_dict.update(d["answer"])
    fillpdfs.write_fillable_pdf(r".\web_app\static\modulo.pdf", path_to_file, data_dict)
    fillpdfs.flatten_pdf(path_to_file, path_to_file)
    return file_name

if __name__ == "__main__":
    fillpdfs.print_form_fields(r".\static\modulo.pdf")