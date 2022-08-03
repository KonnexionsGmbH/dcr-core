from __future__ import annotations

from dcr_core import cls_line_type_headers_footers
from dcr_core import cls_line_type_heading
from dcr_core import cls_line_type_list_bullet
from dcr_core import cls_line_type_list_number
from dcr_core import cls_line_type_table
from dcr_core import cls_line_type_toc
from dcr_core import cls_setup
from dcr_core import cls_text_parser
from dcr_core import cls_tokenizer_spacy

FILE_TYPE_PANDOC: list[str]
FILE_TYPE_TESSERACT: list[str]
RETURN_OK: tuple[str, str]

line_type_headers_footers: cls_line_type_headers_footers.LineTypeHeaderFooters
line_type_heading: cls_line_type_heading.LineTypeHeading
line_type_list_bullet: cls_line_type_list_bullet.LineTypeListBullet
line_type_list_number: cls_line_type_list_number.LineTypeListNumber
line_type_table: cls_line_type_table.LineTypeTable
line_type_toc: cls_line_type_toc.LineTypeToc
setup: cls_setup.Setup
text_parser: cls_text_parser.TextParser
tokenizer_spacy: cls_tokenizer_spacy.TokenizerSpacy
