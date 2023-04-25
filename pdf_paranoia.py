#! python3
# pdf_paranoia.py — An exercise in manipulating PDFs.
# For more information, see project_details.txt.

import fnmatch
import logging
import os
from send2trash import send2trash
from PyPDF2 import PdfReader, PdfWriter

logging.basicConfig(
    level=logging.DEBUG,
    filename="logging.txt",
    format="%(asctime)s -  %(levelname)s -  %(message)s",
)
# logging.disable(logging.CRITICAL)  # Note out to enable logging.


user_path = input("Please type path to top-level directory here: ")


def find_pdfs(path):
    """Use os.walk and fnmatch.filter to create list of absolute paths
    for all PDFs nested in user-defined directory."""
    pdf_paths = [
        root + "/" + filename
        for root, dirnames, filenames in os.walk(path)
        for filename in fnmatch.filter(filenames, "*.pdf")
    ]
    return pdf_paths


def encrypt_pdfs(pdfs):
    """Encrypt all pdfs in pdf_list."""
    # pdf_input_password = input("Please type password to encrypt files here: ")
    pdf_env_password = os.environ.get("PDF_PASS")
    for pdf in pdfs:
        pdf_reader = PdfReader(pdf)
        pdf_writer = PdfWriter()

        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
        # pdf_writer.encrypt(pdf_input_password)
        pdf_writer.encrypt(pdf_env_password)

        with open(f"{pdf}_encrypted.pdf", "wb") as enc_file:
            pdf_writer.write(enc_file)


def trash_originals(pdfs):
    """Send all unecrypted pdfs to trash."""
    for pdf in pdfs:
        send2trash(pdf)


pdf_list = find_pdfs(user_path)
encrypt_pdfs(pdf_list)
trash_originals(pdf_list)
