#!/usr/bin/env python3
# pdf_paranoia.py — An exercise in manipulating PDFs.
# For more information, see README.md

import fnmatch
import logging
import os

# import sys
from send2trash import send2trash
from PyPDF2 import PdfReader, PdfWriter

logging.basicConfig(
    level=logging.DEBUG,
    filename="logging.txt",
    format="%(asctime)s -  %(levelname)s -  %(message)s",
)
logging.disable(logging.CRITICAL)  # Note out to enable logging.


def find_pdfs(path):
    """Use os.walk and fnmatch.filter to create list of absolute paths
    for all PDFs nested in user-defined directory."""
    pdf_paths = [
        root + "/" + filename
        for root, _, filenames in os.walk(path)
        for filename in fnmatch.filter(filenames, "*.pdf")
    ]
    return pdf_paths


def encrypt_pdfs(pdf_path):
    """Encrypt all pdfs in pdf_list."""
    # cmd_line_password = sys.argv[1]
    cmd_line_password = "password"

    for pdf in pdf_path:
        pdf_reader = PdfReader(pdf)
        pdf_writer = PdfWriter()

        if not pdf_reader.is_encrypted:
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)
            pdf_writer.encrypt(cmd_line_password)

            with open(f"{pdf[:-4]}_encrypted.pdf", "wb") as enc_file:
                pdf_writer.write(enc_file)


def trash_originals(user_path):
    """If PDF encryption is successful, send original to trash."""
    encrypted_pdfs = [
        pdf for pdf in find_pdfs(user_path) if PdfReader(pdf).is_encrypted
    ]
    for pdf in encrypted_pdfs:
        send2trash(f"{pdf[:-14]}.pdf")


def main():
    user_path = input("Please type path to top-level directory here: ")
    encrypt_pdfs(find_pdfs(user_path))
    trash_originals(user_path)


if __name__ == "__main__":
    main()
