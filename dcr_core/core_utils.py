# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Miscellaneous helper functions."""
import datetime
import os
import pathlib
import sys
import traceback

import dcr_core


# ------------------------------------------------------------------
# Check the existence of objects.
# ------------------------------------------------------------------
def check_exists_object(  # noqa: C901
    is_line_type_headers_footers: bool = False,
    is_line_type_list_bullet: bool = False,
    is_line_type_list_number: bool = False,
    is_line_type_table: bool = False,
    is_line_type_toc: bool = False,
    is_setup: bool = False,
    is_text_parser: bool = False,
) -> None:
    """Check the existence of objects.

    Args:
        is_line_type_headers_footers (bool, optional):
            Check an object of class LineTypeHeadersFooters. Defaults to False.
        is_line_type_list_bullet (bool, optional):
            Check an object of class LineTypeListBullet. Defaults to False.
        is_line_type_list_number (bool, optional):
            Check an object of class LineTypeListNumber. Defaults to False.
        is_line_type_table (bool, optional):
            Check an object of class LineTypeTable. Defaults to False.
        is_line_type_toc (bool, optional):
            Check an object of class LineTypeToc. Defaults to False.
        is_setup (bool, optional):
            Check an object of class Setup. Defaults to False.
        is_text_parser (bool, optional):
            Check an object of class TextParser. Defaults to False.
    """
    if is_line_type_headers_footers:
        try:
            dcr_core.core_glob.line_type_headers_footers.exists()  # type: ignore
        except AttributeError:
            terminate_fatal(
                "The required instance of the class 'LineTypeHeadersFooters' does not yet exist.",
            )

    if is_line_type_list_bullet:
        try:
            dcr_core.core_glob.line_type_list_bullet.exists()  # type: ignore
        except AttributeError:
            terminate_fatal(
                "The required instance of the class 'LineTypeListBullet' does not yet exist.",
            )

    if is_line_type_list_number:
        try:
            dcr_core.core_glob.line_type_list_number.exists()  # type: ignore
        except AttributeError:
            terminate_fatal(
                "The required instance of the class 'LineTypeListNumber' does not yet exist.",
            )

    if is_line_type_table:
        try:
            dcr_core.core_glob.line_type_table.exists()  # type: ignore
        except AttributeError:
            terminate_fatal(
                "The required instance of the class 'LineTypeTable' does not yet exist.",
            )

    if is_line_type_toc:
        try:
            dcr_core.core_glob.line_type_toc.exists()  # type: ignore
        except AttributeError:
            terminate_fatal(
                "The required instance of the class 'LineTypeToc' does not yet exist.",
            )

    if is_setup:
        try:
            dcr_core.core_glob.setup.exists()  # type: ignore
        except AttributeError:
            terminate_fatal(
                "The required instance of the class 'Setup' does not yet exist.",
            )

    if is_text_parser:
        try:
            dcr_core.core_glob.text_parser.exists()
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
        full_name (str):
            Full file name of an existing file.

    Raises:
        FileNotFoundError:
            If file with full name doesn't exist.
        RuntimeError:
            If an infinite loop is encountered along the resolution path.

    Returns:
        tuple[str, str, str]:
            directory name, stem name, file extension.
    """
    try:
        if isinstance(full_name, str):
            full_name_int = pathlib.Path(full_name)
        else:
            full_name_int = full_name

        file_name_resolved: pathlib.Path = pathlib.Path(pathlib.Path.resolve(full_name_int, strict=True))

        return str(file_name_resolved.parent), file_name_resolved.stem, file_name_resolved.suffix[1:] if file_name_resolved.suffix else file_name_resolved.suffix
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"File {full_name} doesn't exist") from exc
    except RuntimeError as exc:
        raise RuntimeError(f"An infinite loop is encountered along the resolution path of {full_name}") from exc


# ------------------------------------------------------------------
# Get the full name of a file from its components.
# ------------------------------------------------------------------
def get_full_name_from_components(
    directory_name_in: pathlib.Path | str,
    stem_name_in: str = "",
    file_extension_in: str = "",
) -> str:
    """Get the full name of a file from its components.

    The possible components are directory name, stem name and file extension.

    Args:
        directory_name_in (pathlib.Path or str):
            Directory name or directory path.
        stem_name_in (str, optional):
            Stem name or file name including file extension. Defaults to "".
        file_extension_in (str, optional):
            File extension. Defaults to "".

    Returns:
        str:
            Full file name.
    """
    file_name = stem_name_in if file_extension_in == "" else stem_name_in + "." + file_extension_in

    if directory_name_in == "" and file_name == "":
        return ""

    if isinstance(directory_name_in, pathlib.Path):
        directory_name = str(directory_name_in)
    else:
        directory_name = directory_name_in

    if isinstance(file_name, pathlib.Path):
        file_name = str(file_name)

    return get_os_independent_name(str(os.path.join(directory_name, file_name)))


# ------------------------------------------------------------------
# Get the platform-independent name.
# ------------------------------------------------------------------
def get_os_independent_name(name: pathlib.Path | str | None) -> str:
    """Get the platform-independent name..

    Args:
        name (pathlib.Path | str | None):
            File name or file path.

    Returns:
        str:
            Platform-independent name.
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
        file_name (pathlib.Path | str | None):
            File name or file path.

    Returns:
        str:
            Stem name.
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
        is_verbose (bool):
            If true, processing results are reported.
        msg (str):
            Progress message.
    """
    if is_verbose:
        progress_msg_core(msg)


# ------------------------------------------------------------------
# Create a progress message.
# ------------------------------------------------------------------
def progress_msg_core(msg: str) -> None:
    """Create a progress message.

    Args:
        msg (str):
            Progress message.
    """
    final_msg = dcr_core.core_glob.LOGGER_PROGRESS_UPDATE + str(datetime.datetime.now()) + " : " + msg + "."

    print(final_msg)


# ------------------------------------------------------------------
# Terminate the application immediately.
# ------------------------------------------------------------------
def terminate_fatal(error_msg: str) -> None:
    """Terminate the application immediately.

    Args:
        error_msg (str):
            Error message.
    """
    print("")
    print(dcr_core.core_glob.LOGGER_FATAL_HEAD)
    print(dcr_core.core_glob.LOGGER_FATAL_HEAD, error_msg, dcr_core.core_glob.LOGGER_FATAL_TAIL, sep="")
    print(dcr_core.core_glob.LOGGER_FATAL_HEAD)

    traceback.print_exc(chain=True)

    sys.exit(1)
