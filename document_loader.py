import tempfile

from dotenv import load_dotenv
import os
from pathlib import Path
from langchain_community.document_loaders import (TextLoader, PyPDFLoader)
load_dotenv()

def load_text_file():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
        temp_file.write(
            b"Hello, this is a sample text file.\nThis file is used to demonstrate the TextLoader."
        )
        temp_file_path = temp_file.name

    try:
        loader = TextLoader(temp_file_path)
        documents = loader.load()

        # for doc in documents:
        #     print('Document Content')
        #     print(doc)
        #     print(doc.page_content)
        return documents
    finally:
        os.remove(temp_file_path)


def load_pdf_file():
    loader = PyPDFLoader(file_path='docs/langchain_demo.pdf')
    documents = loader.load()
    for doc in documents:
        print('Document Content')
        print(doc)
        print(doc.metadata)
    return documents


if __name__ == "__main__":
    # load_text_file()
    load_pdf_file()

