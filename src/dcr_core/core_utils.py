# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Miscellaneous helper functions."""
from __future__ import annotations

import datetime
import os
import pathlib
import sys
import traceback

from dcr_core import core_glob

# ------------------------------------------------------------------
# Global variables.
# ------------------------------------------------------------------
ERROR_00_901 = "00.901 Issue (utils): The file '{full_name}' cannot be found - FileNotFoundError"
ERROR_00_902 = (
    "00.902 Issue: An infinite loop is encountered along the resolution path of '{full_name}' - " + "RuntimeError - error: '{error_msg}'."
)
ERROR_01_901 = "01.901 Issue (p_i): Document rejected because of unknown file extension='{extension}'."
ERROR_01_903 = "01.903 Issue (p_i): Error with fitz.open() processing of file '{file_name}' " + "- RuntimeError - error: '{error_msg}'"

ERROR_21_901 = (
    "21.901 Issue (p_2_i): Processing file '{full_name}' with pdf2image failed - PDFPageCountError - "
    + "error type: '{error_type}' - error: '{error_msg}'"
)
ERROR_31_902 = "31.902 Issue (n_2_p): The file '{full_name}' cannot be converted to an " + "'PDF' document - FileNotFoundError"
ERROR_31_903 = (
    "31.903 Issue (n_2_p): The file '{full_name}' cannot be converted to an " + "'PDF' document - RuntimeError - error: '{error_msg}'"
)
ERROR_31_911 = "31.911 Issue (n_2_p): The pdf document {full_name} for PDFlib TET is an empty file"
ERROR_41_901 = "41.901 Issue (ocr): Converting the file '{full_name}' with Tesseract OCR failed - " + "RuntimeError - error: '{error_msg}'"
ERROR_41_911 = "41.911 Issue (ocr): Tesseract OCR has created an empty pdf file from the file {full_name}"
ERROR_51_901 = "51.901 Issue (tet): Opening document '{full_name}' - " + "error no: '{error_no}' - api: '{api_name}' - error: '{error_msg}'"
ERROR_61_901 = "61.901 Issue (s_p_j): Parsing the file '{full_name}' failed - FileNotFoundError"
ERROR_61_902 = "61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'"
ERROR_61_903 = "61.903 Issue (s_p_j): The number of unknown XML nodes is {no_errors} - details can be found in the log"
ERROR_71_901 = "71.901 Issue (tkn): Tokenizing the file '{full_name}' failed - FileNotFoundError"


# ------------------------------------------------------------------
# Check the existence of objects.
# ------------------------------------------------------------------
def check_exists_object(  # noqa: C901
    is_line_type_header_footer: bool = False,
    is_line_type_heading: bool = False,
    is_line_type_list_bullet: bool = False,
    is_line_type_list_number: bool = False,
    is_line_type_table: bool = False,
    is_line_type_toc: bool = False,
    is_nlp_core: bool = False,
    is_setup: bool = False,
    is_text_parser: bool = False,
) -> None:
    """Check the existence of objects.

    Args:
        is_line_type_header_footer (bool, optional):
            Check an object of class LineTypeHeaderFooter.
            Defaults to False.
        is_line_type_heading (bool, optional):
            Check an object of class LineTypeHeading.
            Defaults to False.
        is_line_type_list_bullet (bool, optional):
            Check an object of class LineTypeListBullet.
            Defaults to False.
        is_line_type_list_number (bool, optional):
            Check an object of class LineTypeListNumber.
            Defaults to False.
        is_line_type_table (bool, optional):
            Check an object of class LineTypeTable.
            Defaults to False.
        is_line_type_toc (bool, optional):
            Check an object of class LineTypeToc.
            Defaults to False.
        is_nlp_core (bool, optional):
            Check an object of class NLPCore.
            Defaults to False.
        is_setup (bool, optional):
            Check an object of class Setup.
            Defaults to False.
        is_text_parser (bool, optional): Check an object
            of class TextParser.
            Defaults to False.
    """
    if is_line_type_header_footer:
        try:
            core_glob.inst_lt_hf.exists()  # type: ignore
        except AttributeError:
            terminate_fatal(
                "The required instance of the class 'LineTypeHeaderFooter' does not yet exist.",
            )

    if is_line_type_heading:
        try:
            core_glob.inst_lt_h.exists()  # type: ignore
        except AttributeError:
            terminate_fatal(
                "The required instance of the class 'LineTypeHeading' does not yet exist.",
            )

    if is_line_type_list_bullet:
        try:
            core_glob.inst_lt_lb.exists()  # type: ignore
        except AttributeError:
            terminate_fatal(
                "The required instance of the class 'LineTypeListBullet' does not yet exist.",
            )

    if is_line_type_list_number:
        try:
            core_glob.inst_lt_ln.exists()  # type: ignore
        except AttributeError:
            terminate_fatal(
                "The required instance of the class 'LineTypeListNumber' does not yet exist.",
            )

    if is_line_type_table:
        try:
            core_glob.inst_lt_tab.exists()  # type: ignore
        except AttributeError:
            terminate_fatal(
                "The required instance of the class 'LineTypeTable' does not yet exist.",
            )

    if is_line_type_toc:
        try:
            core_glob.inst_lt_toc.exists()  # type: ignore
        except AttributeError:
            terminate_fatal(
                "The required instance of the class 'LineTypeToc' does not yet exist.",
            )

    if is_setup:
        try:
            core_glob.inst_setup.exists()  # type: ignore
        except AttributeError:
            terminate_fatal(
                "The required instance of the class 'Setup' does not yet exist.",
            )

    if is_nlp_core:
        try:
            core_glob.inst_nlp_core.exists()  # type: ignore
        except AttributeError:
            terminate_fatal(
                "The required instance of the class 'NLPCore' does not yet exist.",
            )

    if is_text_parser:
        try:
            core_glob.inst_parser.exists()
        except AttributeError:
            terminate_fatal(
                "The required instance of the class 'TextParser' does not yet exist.",
            )


# ------------------------------------------------------------------
# Break down the file name of an existing file into components.
# ------------------------------------------------------------------
def get_components_from_full_name(
    full_name: str,
) -> tuple[str, str, str]:
    """Break down the full name of an existing file into components.

    The possible components are directory name, stem name and file extension.

    Args:
        full_name (str): Full file name of an existing file.

    Raises:
        FileNotFoundError: If file with full name doesn't exist.
        RuntimeError: If an infinite loop is encountered along the resolution path.

    Returns:
        tuple[str, str, str]: directory name, stem name, file extension.
    """
    try:
        if isinstance(full_name, str):
            full_name_int = pathlib.Path(full_name)
        else:
            full_name_int = full_name

        file_name_resolved: pathlib.Path = pathlib.Path(pathlib.Path.resolve(full_name_int, strict=True))

        return (
            str(file_name_resolved.parent),
            file_name_resolved.stem,
            file_name_resolved.suffix[1:] if file_name_resolved.suffix else file_name_resolved.suffix,
        )
    except FileNotFoundError as exc:
        raise FileNotFoundError(ERROR_00_901.replace("{full_name}", full_name)) from exc
    except RuntimeError as exc:
        raise RuntimeError(ERROR_00_902.replace("{full_name}", full_name).replace("{error_msg}", str(exc))) from exc


# ------------------------------------------------------------------
# Get the full name of a file from its components.
# ------------------------------------------------------------------
def get_full_name_from_components(
    directory_name: pathlib.Path | str,
    stem_name: str = "",
    file_extension: str = "",
) -> str:
    """Get the full name of a file from its components.

    The possible components are directory name, stem name and file extension.

    Args:
        directory_name (pathlib.Path or str): Directory name or directory path.
        stem_name (str, optional): Stem name or file name including file extension.
            Defaults to "".
        file_extension (str, optional): File extension.
            Defaults to "".

    Returns:
        str: Full file name.
    """
    file_name_int = stem_name if file_extension == "" else stem_name + "." + file_extension

    if directory_name == "" and file_name_int == "":
        return ""

    if isinstance(directory_name, pathlib.Path):
        directory_name_int = str(directory_name)
    else:
        directory_name_int = directory_name

    if isinstance(file_name_int, pathlib.Path):
        file_name_int = str(file_name_int)

    return get_os_independent_name(str(os.path.join(directory_name_int, file_name_int)))


# ------------------------------------------------------------------
# Get the platform-independent name.
# ------------------------------------------------------------------
def get_os_independent_name(name: pathlib.Path | str | None) -> str:
    """Get the platform-independent name..

    Args:
        name (pathlib.Path | str | None): File name or file path.

    Returns:
        str: Platform-independent name.
    """
    if name is None:
        return ""

    if isinstance(name, str):
        return name.replace(("\\" if os.sep == "/" else "/"), os.sep)

    return str(name)


# ------------------------------------------------------------------
# Get the stem name from a file name.
# ------------------------------------------------------------------
def get_stem_name(file_name: pathlib.Path | str | None) -> str:
    """Get the stem name from a file name.

    Args:
        file_name (pathlib.Path | str | None): File name or file path.

    Returns:
        str: Stem name.
    """
    if file_name is None:
        return ""

    if isinstance(file_name, str):
        file_name = pathlib.Path(file_name)

    return file_name.stem


# ------------------------------------------------------------------
# Create a progress message.
# ------------------------------------------------------------------
def progress_msg(is_verbose: bool, msg: str) -> None:
    """Create a progress message.

    Args:
        is_verbose (bool): If true, processing results are reported.
        msg (str): Progress message.
    """
    if is_verbose:
        progress_msg_core(msg)


# ------------------------------------------------------------------
# Create a progress message.
# ------------------------------------------------------------------
def progress_msg_core(msg: str) -> None:
    """Create a progress message.

    Args:
        msg (str): Progress message.
    """
    final_msg = core_glob.LOGGER_PROGRESS_UPDATE + str(datetime.datetime.now()) + " : " + msg + "."

    print(final_msg)


# ------------------------------------------------------------------
# Terminate the application immediately.
# ------------------------------------------------------------------
def terminate_fatal(error_msg: str) -> None:
    """Terminate the application immediately.

    Args:
        error_msg (str): Error message.
    """
    print("")
    print(core_glob.LOGGER_FATAL_HEAD)
    print(core_glob.LOGGER_FATAL_HEAD, error_msg, core_glob.LOGGER_FATAL_TAIL, sep="")
    print(core_glob.LOGGER_FATAL_HEAD)

    traceback.print_exc(chain=True)

    sys.exit(1)
