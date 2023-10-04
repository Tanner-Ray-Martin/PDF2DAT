from . import constants
import os
from pypdf import PageObject, PdfReader
import re


def get_new_pdfs():
    return [
        os.path.join(constants.NEW_PDF_DIR, pdf_name)
        for pdf_name in os.listdir(constants.NEW_PDF_DIR)
    ]

def load_pdf(pdf_path:str):
    return PdfReader(pdf_path)

def dimenstion_str_to_float(text:str):
    text = text.replace("ft", "").strip()
    return float(text)

def get_page_text(page:PageObject):
    return page.extract_text().splitlines()

def is_dimension_location_line(line:str):
    return "dimension" in line.lower()

def get_dimension_location_from_line(line:str):
    for name in constants.PDF_LOCATION_KEYS:
        if name in line.lower():
            return name

def convert_dimension_text_2_object(line:str):
    data:dict[str, float] = dict()
    dimensions_in_line = re.findall(constants.PATTERN, line)
    for idx, dimension_text in enumerate(dimensions_in_line):
        dimension_value = dimenstion_str_to_float(dimension_text)
        dimension = constants.DIMENSION_KEYS[idx]
        data[dimension] = dimension_value
    return data

def format_dimension_float_as_dat(dimension_data:dict[str, float]):
    length = dimension_data.get("length")
    width = dimension_data.get("width")
    return "\n".join([
        f"{constants.DAT_FORMAT_PREFIX_1}{length}{constants.DAT_LENGHT_FORMAT}",
        f"{constants.DAT_FORMAT_PREFIX_1}{width}{constants.DAT_WIDTH_FORMAT}",
        f"{constants.DAT_FORMAT_PREFIX_2}{length}{constants.DAT_LENGHT_FORMAT}",
        f"{constants.DAT_FORMAT_PREFIX_2}{width}{constants.DAT_WIDTH_FORMAT}"
    ])

def create_dat_file_text(location:str, formatted_data:str):
    file_text_list = [constants.DAT_LOCATION_TEXT+location.title().strip()]
    file_text_list.append(constants.DAT_PREFIX)
    file_text_list.append(formatted_data)
    file_text_list.append(constants.DAT_POSTFIX)
    return "\n".join(file_text_list)

def save_text_to_dat_file_and_return_path(location:str, formatted_text:str):
    file_name = location+'.dat'
    file_path = os.path.join(constants.OUTPUT_DIR, file_name)
    with open(file_path, 'w') as fp:
        fp.write(formatted_text)
    return file_path

def move_pdf(pdf_path):
    pdf_name = os.path.basename(pdf_path)
    move_to_path = os.path.join(constants.OLD_PDF_DIR, pdf_name)
    try:
        os.rename(pdf_path, move_to_path)
        return True
    except:
        return False
    