# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module stub file."""
import logging

import dcr_core.cls_line_type_header_footer as lt_hf
import dcr_core.cls_line_type_heading as lt_h
import dcr_core.cls_line_type_list_bullet as lt_lb
import dcr_core.cls_line_type_list_number as lt_ln
import dcr_core.cls_line_type_table as lt_tab
import dcr_core.cls_line_type_toc as lt_toc
import dcr_core.cls_nlp_core as cls_nlp_core
import dcr_core.cls_setup as core_setup
import dcr_core.cls_text_parser as parser
import dcr_core.cls_tokenizer_spacy as tokenizer

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

line_type_header_footer: lt_hf.LineTypeHeaderFooter
line_type_heading: lt_h.LineTypeHeading
line_type_list_bullet: lt_lb.LineTypeListBullet
line_type_list_number: lt_ln.LineTypeListNumber
line_type_table: lt_tab.LineTypeTable
line_type_toc: lt_toc.LineTypeToc
logger: logging.Logger
nlp_core: cls_nlp_core.NLPCore
setup: core_setup.Setup
text_parser: parser.TextParser
tokenizer_spacy: tokenizer.TokenizerSpacy

def initialise_logger(logger_name: str = ...) -> None: ...
