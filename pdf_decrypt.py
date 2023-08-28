#!/usr/bin/env python3
# pdf_decrypt.py — An exercise in manipulating PDFs.
# For more information, see README.md

import logging
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.errors import FileNotDecryptedError
from pdf_encrypt import find_pdfs


logging.basicConfig(
    level=logging.DEBUG,
    filename="logging.txt",
    format="%(asctime)s -  %(levelname)s -  %(message)s",
)
logging.disable(logging.CRITICAL)  # Note out to enable logging.


def decrypt_pdfs(pdf_list):
    """If encrpyted file found, try to decrypt with user-defined password."""
    password = input("Please type password here: ")

    try:
        for pdf in pdf_list:
            pdf_reader = PdfReader(pdf)
            pdf_writer = PdfWriter()

            if pdf_reader.is_encrypted:
                pdf_reader.decrypt(password)

            for page in pdf_reader.pages:
                pdf_writer.add_page(page)

            with open(f"{pdf[:-14]}_decrpyted.pdf", "wb") as f:
                pdf_writer.write(f)

    except FileNotDecryptedError:
        print(f"Password {password} is incorrect.")


def main():
    decrypt_pdfs(find_pdfs(input("Please type path to top-level directory here: ")))


if __name__ == "__main__":
    main()
