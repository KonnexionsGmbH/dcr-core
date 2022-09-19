# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Global constants and variables."""
from __future__ import annotations

import logging
import logging.config

import yaml

import dcr_core.cls_line_type_header_footer as lt_hf
import dcr_core.cls_line_type_heading as lt_h
import dcr_core.cls_line_type_list_bullet as lt_lb
import dcr_core.cls_line_type_list_number as lt_ln
import dcr_core.cls_line_type_toc as lt_toc
import dcr_core.cls_nlp_core as nlp_core
import dcr_core.cls_setup as setup
import dcr_core.cls_text_parser as parser
import dcr_core.cls_tokenizer_spacy as tokenizer
from dcr_core import core_utils

# ------------------------------------------------------------------
# Global Constants.
# ------------------------------------------------------------------
FILE_ENCODING_DEFAULT = "utf-8"

FILE_TYPE_JPEG = "jpeg"
FILE_TYPE_JPG = "jpg"
FILE_TYPE_JSON = "json"
FILE_TYPE_PANDOC: list[str] = [
    "csv",
    "docx",
    "epub",
    "html",
    "odt",
    "rst",
    "rtf",
]
FILE_TYPE_PDF = "pdf"
FILE_TYPE_PNG = "png"
FILE_TYPE_TESSERACT: list[str] = [
    "bmp",
    "gif",
    "jp2",
    "jpeg",
    "jpg",
    "png",
    "pnm",
    "tif",
    "tiff",
    "webp",
]
FILE_TYPE_TIF = "tif"
FILE_TYPE_TIFF = "tiff"
FILE_TYPE_XML = "xml"

INFORMATION_NOT_YET_AVAILABLE = "n/a"

LOGGER_CFG_FILE = "logging_cfg.yaml"
LOGGER_END = "End"
LOGGER_FATAL_HEAD = "FATAL ERROR: program abort =====> "
LOGGER_FATAL_TAIL = " <===== FATAL ERROR"
LOGGER_NAME = "dcr_core"
LOGGER_PROGRESS_UPDATE = "Progress update "
LOGGER_START = "Start"

RETURN_OK = ("ok", "")

# ------------------------------------------------------------------
# Global Variables.
# ------------------------------------------------------------------
inst_lt_h: lt_h.LineTypeHeading
inst_lt_hf: lt_hf.LineTypeHeaderFooter
inst_lt_lb: lt_lb.LineTypeListBullet
inst_lt_ln: lt_ln.LineTypeListNumber
inst_lt_toc: lt_toc.LineTypeToc
inst_nlp_core: nlp_core.NLPCore
inst_parser: parser.TextParser
inst_setup: setup.Setup
inst_tokenizer: tokenizer.TokenizerSpacy

logger: logging.Logger = logging.getLogger(LOGGER_NAME)


# -----------------------------------------------------------------------------
# Initialising the logging functionality.
# -----------------------------------------------------------------------------
def initialise_logger() -> None:
    """Initialise the root logging functionality."""
    with open(LOGGER_CFG_FILE, "r", encoding=FILE_ENCODING_DEFAULT) as file_handle:
        log_config = yaml.safe_load(file_handle.read())

    logging.config.dictConfig(log_config)
    logger.setLevel(logging.DEBUG)

    core_utils.progress_msg_core("The logger is configured and ready")
