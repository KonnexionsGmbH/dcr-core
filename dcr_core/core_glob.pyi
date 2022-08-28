# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module stub file."""
import logging

import dcr_core.cls_line_type_header_footer
import dcr_core.cls_line_type_heading
import dcr_core.cls_line_type_list_bullet
import dcr_core.cls_line_type_list_number
import dcr_core.cls_line_type_table
import dcr_core.cls_line_type_toc
import dcr_core.cls_setup
import dcr_core.cls_text_parser
import dcr_core.cls_tokenizer_spacy

FILE_ENCODING_DEFAULT: str
FILE_TYPE_JPEG: str
FILE_TYPE_JPG: str
FILE_TYPE_JSON: str
FILE_TYPE_PANDOC: list[str]
FILE_TYPE_PDF: str
FILE_TYPE_PNG: str
FILE_TYPE_TESSERACT: list[str]
FILE_TYPE_TIF: str
FILE_TYPE_TIFF: str
FILE_TYPE_XML: str
INFORMATION_NOT_YET_AVAILABLE: str
LOGGER_CFG_FILE: str
LOGGER_END: str
LOGGER_FATAL_HEAD: str
LOGGER_FATAL_TAIL: str
LOGGER_PROGRESS_UPDATE: str
LOGGER_START: str
RETURN_OK: tuple[str, str]

line_type_header_footer: dcr_core.cls_line_type_header_footer.LineTypeHeaderFooter
line_type_heading: dcr_core.cls_line_type_heading.LineTypeHeading
line_type_list_bullet: dcr_core.cls_line_type_list_bullet.LineTypeListBullet
line_type_list_number: dcr_core.cls_line_type_list_number.LineTypeListNumber
line_type_table: dcr_core.cls_line_type_table.LineTypeTable
line_type_toc: dcr_core.cls_line_type_toc.LineTypeToc
logger: logging.Logger
setup: dcr_core.cls_setup.Setup
text_parser: dcr_core.cls_text_parser.TextParser
tokenizer_spacy: dcr_core.cls_tokenizer_spacy.TokenizerSpacy

def initialise_logger(logger_name: str = ...) -> None: ...
