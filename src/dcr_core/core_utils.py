"""Module core_utils: Helper functions."""
import datetime
import os
import pathlib
import sys
import traceback

import core_glob


# -----------------------------------------------------------------------------
# Check the existence of objects.
# -----------------------------------------------------------------------------
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
            core_glob.line_type_headers_footers.exists()
        except AttributeError:
            terminate_fatal(
                "The required instance of the class 'LineTypeHeadersFooters' does not yet exist.",
            )

    if is_line_type_list_bullet:
        try:
            core_glob.line_type_list_bullet.exists()
        except AttributeError:
            terminate_fatal(
                "The required instance of the class 'LineTypeListBullet' does not yet exist.",
            )

    if is_line_type_list_number:
        try:
            core_glob.line_type_list_number.exists()
        except AttributeError:
            terminate_fatal(
                "The required instance of the class 'LineTypeListNumber' does not yet exist.",
            )

    if is_line_type_table:
        try:
            core_glob.line_type_table.exists()
        except AttributeError:
            terminate_fatal(
                "The required instance of the class 'LineTypeTable' does not yet exist.",
            )

    if is_line_type_toc:
        try:
            core_glob.line_type_toc.exists()
        except AttributeError:
            terminate_fatal(
                "The required instance of the class 'LineTypeToc' does not yet exist.",
            )

    if is_setup:
        try:
            core_glob.setup.exists()
        except AttributeError:
            terminate_fatal(
                "The required instance of the class 'Setup' does not yet exist.",
            )

    if is_text_parser:
        try:
            core_glob.text_parser.exists()
        except AttributeError:
            terminate_fatal(
                "The required instance of the class 'TextParser' does not yet exist.",
            )


# -----------------------------------------------------------------------------
# Get the full name from a directory name or path and a file name or path.
# -----------------------------------------------------------------------------
def get_full_name(directory_name: pathlib.Path | str | None, file_name: pathlib.Path | str | None) -> str:
    """Get the full name from a directory name or path and a file name or path.

    Args:
        directory_name (pathlib.Path | str | None): Directory name or directory path.
        file_name (pathlib.Path | str | None): File name or file path.

    Returns:
        str: Full file name.
    """
    if directory_name is None and file_name is None:
        return ""

    if isinstance(directory_name, pathlib.Path):
        directory_name = str(directory_name)

    if isinstance(file_name, pathlib.Path):
        file_name = str(file_name)

    return get_os_independent_name(str(os.path.join(directory_name, file_name)))


# -----------------------------------------------------------------------------
# Get the platform-independent name.
# -----------------------------------------------------------------------------
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


# -----------------------------------------------------------------------------
# Get the stem name from a file name.
# -----------------------------------------------------------------------------
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


# -----------------------------------------------------------------------------
# Create a progress message.
# -----------------------------------------------------------------------------
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


# -----------------------------------------------------------------------------
# Create a progress message.
# -----------------------------------------------------------------------------
def progress_msg_core(msg: str) -> None:
    """Create a progress message.

    Args:
        msg (str):
                Progress message.
    """
    final_msg = core_glob.LOGGER_PROGRESS_UPDATE + str(datetime.datetime.now()) + " : " + msg + "."

    print(final_msg)


# -----------------------------------------------------------------------------
# Terminate the application immediately.
# -----------------------------------------------------------------------------
def terminate_fatal(error_msg: str) -> None:
    """Terminate the application immediately.

    Args:
        error_msg (str):
                Error message.
    """
    print("")
    print(core_glob.LOGGER_FATAL_HEAD)
    print(core_glob.LOGGER_FATAL_HEAD, error_msg, core_glob.LOGGER_FATAL_TAIL, sep="")
    print(core_glob.LOGGER_FATAL_HEAD)

    traceback.print_exc(chain=True)

    sys.exit(1)