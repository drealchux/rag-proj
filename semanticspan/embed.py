import os
from datetime import datetime
from werkzeug.utils import secure_filename
from langchain_community.document_loaders import PyPDFLoader  # swapped
from langchain_text_splitters import RecursiveCharacterTextSplitter
from get_vector_db import get_vector_db

TEMP_FOLDER = os.getenv('TEMP_FOLDER', './_temp')

def allowed_file(filename):
    return filename.lower().endswith('.pdf')

def save_file(file):
    filename = f"{datetime.now().timestamp()}_{secure_filename(file.filename)}"
    file_path = os.path.join(TEMP_FOLDER, filename)
    file.save(file_path)
    return file_path

def load_and_split_data(file_path):
    loader = PyPDFLoader(file_path=file_path)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=7500, chunk_overlap=100)
    return text_splitter.split_documents(data)

def embed(file):
    if file and allowed_file(file.filename):
        file_path = save_file(file)
        chunks = load_and_split_data(file_path)
        db = get_vector_db()
        db.add_documents(chunks)
        # db.persist() — removed, chromadb 0.4+ auto-persists
        os.remove(file_path)
        return True
    return False