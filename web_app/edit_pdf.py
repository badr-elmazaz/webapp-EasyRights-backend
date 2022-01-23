from fillpdf import fillpdfs
import pdfrw

fillpdfs.print_form_fields(".\static\modulo.pdf")
# print(fillpdfs.get_form_fields(".\static\modulo.pdf"))



data_dict = {
'Nome': 'Badr',
'Cognome': 'El Mazaz',
"Indicare lo Stato estero di provenienza": "Pescina",
"3": "X",
"C1_2_4": "X"
}
#
fillpdfs.write_fillable_pdf(".\static\modulo.pdf", ".\static\\new.pdf", data_dict)

# # If you want it flattened:
# fillpdfs.flatten_pdf('new.pdf', 'newflat.pdf')
#
# ANNOT_KEY = '/Annots'
# ANNOT_FIELD_KEY = '/T'
# ANNOT_VAL_KEY = '/V'
# ANNOT_RECT_KEY = '/Rect'
# SUBTYPE_KEY = '/Subtype'
# WIDGET_SUBTYPE_KEY = '/Widget'
#
# template_pdf = pdfrw.PdfReader(".\static\modulo.pdf")
# print(template_pdf)
# for page in template_pdf.pages:
#     annotations = page[ANNOT_KEY]
#     if annotations:
#         for annotation in annotations:
#             if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
#                 if annotation[ANNOT_FIELD_KEY]:
#                     key = annotation[ANNOT_FIELD_KEY][1:-1]
#                     print(key)

#
# def fill_pdf(input_pdf_path, output_pdf_path, data_dict):
#     print("#####################")
#     template_pdf = pdfrw.PdfReader(input_pdf_path)
#
#     for page in template_pdf.pages:
#         annotations = page[ANNOT_KEY]
#         for annotation in annotations:
#             if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
#                 if annotation[ANNOT_FIELD_KEY]:
#                     key = annotation[ANNOT_FIELD_KEY][1:-1]
#                     if key in data_dict.keys():
#                         if type(data_dict[key]) == bool:
#                             if data_dict[key] == True:
#                                 annotation.update(pdfrw.PdfDict(
#                                     AS=pdfrw.PdfName('Yes')))
#                         else:
#                             annotation.update(
#                                 pdfrw.PdfDict(V='{}'.format(data_dict[key]))
#                             )
#                             annotation.update(pdfrw.PdfDict(AP=''))
#     template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
#     pdfrw.PdfWriter().write(output_pdf_path, template_pdf)

# fill_pdf(".\static\modulo.pdf", ".\static\\new.pdf", data_dict)

fillpdfs.flatten_pdf(".\static\\new.pdf", ".\static\\newflat.pdf")