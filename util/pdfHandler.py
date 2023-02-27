from pdfminer.high_level import extract_text

def ConvertPDFtoText(path, filename):
    return extract_text(path+"/"+filename)

