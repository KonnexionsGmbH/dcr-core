# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module dcr: Entry Point Functionality.

This is the entry point to the application DCR.
"""
import argparse
import locale
import os
import sys

import dcr_core.cls_process as process
import dcr_core.core_glob as glob
import dcr_core.core_utils as utils

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------
ARG_DOCUMENT_ID = "document_id"
ARG_FULL_NAME_IN = "full_name_in"
ARG_FULL_NAME_ORIG = "full_name_orig"
ARG_IS_DELETE_AUXILIARY_FILES = "is_delete_auxiliary_files"
ARG_IS_VERBOSE = "is_verbose"
ARG_LANGUAGE_PANDOC = "language_pandoc"
ARG_LANGUAGE_SPACY = "language_spacy"
ARG_LANGUAGE_TESSERACT = "language_tesseract"
ARG_OUTPUT_DIRECTORY = "output_directory"

LOCALE = "en_US.UTF-8"


# -----------------------------------------------------------------------------
# Load the command line arguments into memory.
# -----------------------------------------------------------------------------
def get_args() -> dict[str, str | list[str]]:
    """Load the command line arguments.

    The command line arguments define the process steps to be executed.
    The valid arguments are:

        all   - Run the complete core processing of all new documents.
        db_c  - Create the database.
        db_u  - Upgrade the database.
        e_lt  - Export the line type rules.
        m_d   - Run the installation of the necessary 3rd party packages
                for development and run the development ecosystem.
        m_p   - Run the installation of the necessary 3rd party packages
                for production and compile all packages and modules.
        n_2_p - Convert non-pdf documents to pdf documents:             Pandoc
        ocr   - Convert image files to pdf documents:               Tesseract OCR / Tex Live.
        p_2_i - Convert pdf documents to image files:               pdf2image / Poppler.
        p_i   - Process the inbox directory.
        s_p_j - Store the parser result in a JSON file.
        tet   - Extract text and metadata from pdf documents:       PDFlib TET.
        tkn   - Create document tokens:                             spaCy.

    With the option all, the following process steps are executed
    in this order:

        1. p_i
        2. p_2_i
        3. n_2_p
        4. ocr
        5. tet
        6. s_p_j
        7. tkn

    Returns:
        dict[str, bool]: The processing steps based on CLI arguments.
    """
    glob.logger.debug(glob.LOGGER_START)

    args: dict[str, bool | str] = {}

    parser = argparse.ArgumentParser(
        description="Process a given document",
        prog="launcher",
        prefix_chars="--",
        usage="%(prog)s [options] file_name_in",
    )

    parser.add_argument(
        "FullNameIn",
        help="the full name of the document file to process",
        metavar="full_name_in",
        type=str,
    )

    parser.add_argument(
        "-a",
        "--auxiliary",
        default=False,
        help="delete the auxiliary files",
        metavar="AUXILIARY",
        type=bool,
    )

    parser.add_argument(
        "-o",
        "--output",
        default="data/inbox_dev/",
        help="the name of the directory containing the files to be created",
        metavar="OUTPUT DIRECTORY",
        type=str,
    )

    parser.add_argument(
        "-v",
        "--verbose",
        default=True,
        help="provide detailed progress messages",
        metavar="PROGRESS",
        type=bool,
    )

    parsed_args = parser.parse_args()

    args[ARG_FULL_NAME_IN] = parsed_args.FullNameIn

    if not os.path.isfile(args[ARG_FULL_NAME_IN]):
        utils.terminate_fatal(
            f"The document file specified does not exist: {args[ARG_FULL_NAME_IN]}",
        )

    args[ARG_IS_DELETE_AUXILIARY_FILES] = parsed_args.auxiliary

    args[ARG_IS_VERBOSE] = parsed_args.verbose

    args[ARG_OUTPUT_DIRECTORY] = parsed_args.output

    if not os.path.isdir(args[ARG_OUTPUT_DIRECTORY]):
        utils.terminate_fatal(
            f"The output directory specified does not exist: {args[ARG_OUTPUT_DIRECTORY]}",
        )

    glob.logger.debug(glob.LOGGER_END)

    return args


# -----------------------------------------------------------------------------
# Initialising the logging functionality.
# -----------------------------------------------------------------------------
def main(argv: list[str]) -> None:
    """Entry point.

    The processes to be carried out are selected via command line arguments.

    Args:
        argv (list[str]): Command line arguments.
    """
    # Initialise the logging functionality.
    glob.initialise_logger()

    glob.logger.debug(glob.LOGGER_START)
    glob.logger.debug("param argv=%s", argv)

    glob.logger.info("Start launcher.py")

    print("Start launcher.py")

    locale.setlocale(locale.LC_ALL, LOCALE)

    # Load the command line arguments.
    args = get_args()

    process.Process().document(
        full_name_in=args[ARG_FULL_NAME_IN],
        is_delete_auxiliary_files=bool(args[ARG_IS_DELETE_AUXILIARY_FILES]),
        is_lt_footer_required=True,
        is_lt_header_required=False,
        is_lt_heading_required=False,
        is_lt_list_bullet_required=False,
        is_lt_list_number_required=False,
        is_lt_table_required=False,
        is_lt_toc_required=False,
        is_verbose=bool(args[ARG_IS_VERBOSE]),
        output_directory=args[ARG_OUTPUT_DIRECTORY],
    )

    print("End   launcher.py")

    glob.logger.info("End   launcher.py")
    glob.logger.debug(glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Program start.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # not testable
    main(sys.argv)
