# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module stub file."""
from __future__ import annotations

import logging

import dcr_core.cls_line_type_header_footer as lt_hf
import dcr_core.cls_line_type_heading as lt_h
import dcr_core.cls_line_type_list_bullet as lt_lb
import dcr_core.cls_line_type_list_number as lt_ln
import dcr_core.cls_line_type_table as lt_tab
import dcr_core.cls_line_type_toc as lt_toc
import dcr_core.cls_nlp_core as nlp_core
import dcr_core.cls_setup as setup
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

inst_lt_h: lt_h.LineTypeHeading
inst_lt_hf: lt_hf.LineTypeHeaderFooter
inst_lt_lb: lt_lb.LineTypeListBullet
inst_lt_ln: lt_ln.LineTypeListNumber
inst_lt_tab: lt_tab.LineTypeTable
inst_lt_toc: lt_toc.LineTypeToc
inst_nlp_core: nlp_core.NLPCore
inst_parser: parser.TextParser
inst_setup: setup.Setup
inst_tokenizer: tokenizer.TokenizerSpacy

logger: logging.Logger

def initialise_logger() -> None: ...
