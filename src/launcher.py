# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module dcr: Entry Point Functionality.

This is the entry point to the application DCR.
"""
from __future__ import annotations

import argparse
import locale
import os
import sys
import traceback
from pathlib import Path

import dcr_core.cls_process as process
import dcr_core.core_glob as glob
import dcr_core.core_utils as utils

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------
ARG_DOCUMENT_ID = "document_id"
ARG_INPUT_SOURCE = "input_source"
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

    Returns:
        dict[str, bool]: The command line arguments.
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
        "InputSource",
        help="the name of a document file or of a file directory containing the document files to process",
        metavar="input_source",
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

    args[ARG_INPUT_SOURCE] = parsed_args.InputSource

    if not (os.path.isdir(args[ARG_INPUT_SOURCE]) or os.path.isfile(args[ARG_INPUT_SOURCE])):
        utils.terminate_fatal(
            f"The specified input source is neither a file nor a file directory: {args[ARG_INPUT_SOURCE]}",
        )

    args[ARG_IS_DELETE_AUXILIARY_FILES] = parsed_args.auxiliary

    args[ARG_IS_VERBOSE] = parsed_args.verbose

    args[ARG_OUTPUT_DIRECTORY] = parsed_args.output

    if not args[ARG_OUTPUT_DIRECTORY]:
        args[ARG_OUTPUT_DIRECTORY] = args[ARG_INPUT_SOURCE] + "_accepted"

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

    document_files = []

    if os.path.isfile(args[ARG_INPUT_SOURCE]):
        document_files.append(args[ARG_INPUT_SOURCE])
    else:
        for file in os.listdir(args[ARG_INPUT_SOURCE]):
            document_files.append(os.path.join(args[ARG_INPUT_SOURCE], file))
        if not document_files:
            utils.terminate_fatal(
                f"The document file directory specified doesn't contain any files: {args[ARG_INPUT_SOURCE]}",
            )

    for document in document_files:
        try:
            for file in Path(args[ARG_OUTPUT_DIRECTORY]).glob(Path(document).stem + "*"):
                os.remove(file)
            process.Process().document(
                full_name_in=document,
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
        except AttributeError as exc:
            utils.progress_msg(bool(args[ARG_IS_VERBOSE]), "-" * 80)
            utils.progress_msg(bool(args[ARG_IS_VERBOSE]), f"Abort processing document file {document}")
            utils.progress_msg(bool(args[ARG_IS_VERBOSE]), f"AttributeError: {str(exc)}")
            utils.progress_msg(bool(args[ARG_IS_VERBOSE]), "-" * 80)
            traceback.print_exc()
            utils.progress_msg(bool(args[ARG_IS_VERBOSE]), "=" * 80)
        except KeyError as exc:
            utils.progress_msg(bool(args[ARG_IS_VERBOSE]), "-" * 80)
            utils.progress_msg(bool(args[ARG_IS_VERBOSE]), f"Abort processing document file {document}")
            utils.progress_msg(bool(args[ARG_IS_VERBOSE]), f"KeyError: {str(exc)}")
            utils.progress_msg(bool(args[ARG_IS_VERBOSE]), "-" * 80)
            traceback.print_exc()
            utils.progress_msg(bool(args[ARG_IS_VERBOSE]), "=" * 80)
        except RuntimeError as exc:
            utils.progress_msg(bool(args[ARG_IS_VERBOSE]), "-" * 80)
            utils.progress_msg(bool(args[ARG_IS_VERBOSE]), f"Abort processing document file {document}")
            utils.progress_msg(bool(args[ARG_IS_VERBOSE]), f"RuntimeError: {str(exc)}")
            utils.progress_msg(bool(args[ARG_IS_VERBOSE]), "-" * 80)
            traceback.print_exc()
            utils.progress_msg(bool(args[ARG_IS_VERBOSE]), "=" * 80)

    print("End   launcher.py")

    glob.logger.info("End   launcher.py")
    glob.logger.debug(glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Program start.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # not testable
    main(sys.argv)
