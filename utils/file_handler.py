import fitz  # PyMuPDF
from io import BytesIO
from docx import Document
import pandas as pd

def read_pdf(content):
    pdf = fitz.open(stream=BytesIO(content), filetype="pdf")
    return "\n".join([page.get_text() for page in pdf])

def read_docx(content):
    doc = Document(BytesIO(content))
    return "\n".join([p.text for p in doc.paragraphs])

def read_excel(content):
    excel_data = pd.read_excel(BytesIO(content))
    return excel_data.to_string()

def read_file(file_content, mime_type):
    if mime_type == "application/pdf":
        return read_pdf(file_content)
    elif mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return read_docx(file_content)
    elif mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        return read_excel(file_content)
    else:
        return "Unsupported file type."
