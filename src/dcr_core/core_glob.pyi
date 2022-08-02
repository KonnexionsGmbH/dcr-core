from __future__ import annotations

from typing import List
from typing import Tuple

import cls_line_type_headers_footers
import cls_line_type_heading
import cls_line_type_list_bullet
import cls_line_type_list_number
import cls_line_type_table
import cls_line_type_toc
import cls_setup
import cls_text_parser
import cls_tokenizer_spacy

FILE_ENCODING_DEFAULT: str
FILE_TYPE_JPEG: str
FILE_TYPE_JPG: str
FILE_TYPE_JSON: str
FILE_TYPE_PANDOC: List[str]
FILE_TYPE_PDF: str
FILE_TYPE_PNG: str
FILE_TYPE_TESSERACT: List[str]
FILE_TYPE_TIF: str
FILE_TYPE_TIFF: str
FILE_TYPE_XML: str
INFORMATION_NOT_YET_AVAILABLE: str
LOGGER_FATAL_HEAD: str
LOGGER_FATAL_TAIL: str
LOGGER_PROGRESS_UPDATE: str
RETURN_OK: Tuple[str, str]

line_type_headers_footers: cls_line_type_headers_footers.LineTypeHeaderFooters
line_type_heading: cls_line_type_heading.LineTypeHeading
line_type_list_bullet: cls_line_type_list_bullet.LineTypeListBullet
line_type_list_number: cls_line_type_list_number.LineTypeListNumber
line_type_table: cls_line_type_table.LineTypeTable
line_type_toc: cls_line_type_toc.LineTypeToc
setup: cls_setup.Setup
text_parser: cls_text_parser.TextParser
tokenizer_spacy: cls_tokenizer_spacy.TokenizerSpacy
