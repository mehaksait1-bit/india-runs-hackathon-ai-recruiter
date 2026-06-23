from docx import Document

def read_jd(path):

    doc = Document(path)

    text = ""

    for para in doc.paragraphs:
        text += para.text + " "

    return text