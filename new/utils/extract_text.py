import io
import logging
import os
import traceback

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from PIL import Image
from google.cloud import vision

module_directory = os.path.dirname(__file__)


def pdf_to_text_api(file_path):
    try:
        if file_path is not None:
            text_data = ""

            pdf_manager = PDFResourceManager()
            string_io = io.StringIO()
            pdf_to_text = TextConverter(pdf_manager, string_io, codec='utf-8', laparams=LAParams())
            interpreter = PDFPageInterpreter(pdf_manager, pdf_to_text)
            for page in PDFPage.get_pages(open(file_path, 'rb')):
                interpreter.process_page(page)
                text_data = string_io.getvalue()

            return str(text_data).strip().replace('\n', '').replace('\f', '')
        else:
            return None

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to get text from pdf: %s", e)
        return None


def image_to_text_api(image_data, court_name):
    try:
        if image_data is not None:
            filename = module_directory + '/../data_files/image_files/' + court_name + '.png'
            im = Image.open(io.BytesIO(image_data))
            im.save(filename)

            with io.open(filename, 'rb') as image_file:
                content = image_file.read()

            client = vision.ImageAnnotatorClient()
            texts = client.text_detection(image=vision.types.Image(content=content)).text_annotations

            return str(texts[0].description).strip().replace(' ', '')
        else:
            return None

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to text from image: %s", e)
        return None
