# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module stub file."""
# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------
ARG_DOCUMENT_ID = None
ARG_INPUT_SOURCE = None
ARG_IS_DELETE_AUXILIARY_FILES = None
ARG_IS_VERBOSE = None
ARG_LANGUAGE_PANDOC = None
ARG_LANGUAGE_SPACY = None
ARG_LANGUAGE_TESSERACT = None
ARG_OUTPUT_DIRECTORY = None
LOCALE = None

def get_args() -> dict[str, str | list[str]]: ...
def main(argv: list[str]) -> None: ...
