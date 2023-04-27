#! python3
# pdf_decrypt.py — An exercise in manipulating PDFs.
# For more information, see second paragraph of project_details.txt.

import fnmatch
import logging
import os
from PyPDF2 import PdfReader, PdfWriter


logging.basicConfig(
    level=logging.DEBUG,
    filename="logging.txt",
    format="%(asctime)s -  %(levelname)s -  %(message)s",
)
logging.disable(logging.CRITICAL)  # Note out to enable logging.


user_path = input("Please type path to top-level directory here: ")


def find_pdfs(path):
    """Use os.walk and fnmatch.filter to create list of absolute paths
    for all PDFs nested in user-defined directory."""
    pdf_paths = [
        root + "/" + filename
        for root, _, filenames in os.walk(path)
        for filename in fnmatch.filter(filenames, "*.pdf")
    ]
    return pdf_paths


def decrypt_pdfs():
    """If encrpyted file found, try to decrypt with user-defined password."""
    pdf_list = find_pdfs(user_path)
    password = input("Please type password here: ")
    for pdf in pdf_list:
        pdf_reader = PdfReader(pdf)
        pdf_writer = PdfWriter()

        try:
            if pdf_reader.is_encrypted:
                pdf_reader.decrypt(password)

            for page in pdf_reader.pages:
                pdf_writer.add_page(page)

            with open(f"{pdf[:-14]}_decrpyted.pdf", "wb") as f:
                pdf_writer.write(f)

        except Exception as e:
            print(f"{e}: Password {password} is incorrect.")


decrypt_pdfs()
