import logging
import traceback

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO


def pdf_to_text_api(file_path):
    try:
        text_data = ""

        pdf_manager = PDFResourceManager()
        string_io = StringIO()
        pdf_to_text = TextConverter(pdf_manager, string_io, codec='utf-8', laparams=LAParams())
        interpreter = PDFPageInterpreter(pdf_manager, pdf_to_text)
        for page in PDFPage.get_pages(open(file_path, 'rb')):
            interpreter.process_page(page)
            text_data = string_io.getvalue()

        return str(text_data).strip().replace('\n', '').replace('\f', '')

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to parse the html: %s", e)
        return "FAILED"
