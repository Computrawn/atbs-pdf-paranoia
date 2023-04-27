#! python3
# pdf_paranoia.py — An exercise in manipulating PDFs.
# For more information, see project_details.txt.

import fnmatch
import logging
import os
import sys
from send2trash import send2trash
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


def encrypt_pdfs():
    """Encrypt all pdfs in pdf_list."""
    pdfs = find_pdfs(user_path)
    cmd_line_password = sys.argv[1]

    for pdf in pdfs:
        pdf_reader = PdfReader(pdf)
        pdf_writer = PdfWriter()

        if not pdf_reader.is_encrypted:
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)
            pdf_writer.encrypt(cmd_line_password)

            with open(f"{pdf[:-4]}_encrypted.pdf", "wb") as enc_file:
                pdf_writer.write(enc_file)


def trash_originals():
    """If PDF encryption is successful, send original to trash."""
    updated_pdf_paths = find_pdfs(user_path)
    encrypted_pdfs = []
    for pdf in updated_pdf_paths:
        pdf_reader = PdfReader(pdf)

        if pdf_reader.is_encrypted:
            encrypted_pdfs.append(pdf)

    for pdf in encrypted_pdfs:
        send2trash(f"{pdf[:-14]}.pdf")


encrypt_pdfs()
trash_originals()
