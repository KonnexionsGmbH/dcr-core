# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

# pylint: disable=redefined-outer-name
"""Test Configuration and Fixtures.

Setup test configuration and store fixtures.

Returns:
    [type]: None.
"""
import configparser
import os
import pathlib
import platform
import shutil

import pytest

import dcr_core.cls_setup
import dcr_core.core_glob
import dcr_core.core_utils

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
CONFIG_PARSER: configparser.ConfigParser = configparser.ConfigParser()

FILE_NAME_SETUP_CFG = "setup.cfg"
FILE_NAME_SETUP_CFG_BACKUP = "setup.cfg_backup"


# -----------------------------------------------------------------------------
# Compare the test files with the reference files.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def compare_with_reference_files(directory_name: str, reference_files: list[str]) -> None:  # noqa: C901
    """Compare the test files with the reference files.

    Args:
        directory_name: str:
            Name of the file directory to be checked.
        reference_files: list[str]:
            list of the reference file names.
    """
    reference_directory = get_test_files_reference_directory_name()

    for reference_file in reference_files:
        extension = pathlib.Path(reference_file).suffix.lower()[1:]

        if extension not in (dcr_core.core_glob.FILE_TYPE_JSON, dcr_core.core_glob.FILE_TYPE_XML):
            continue

        with open(
            dcr_core.core_utils.get_full_name_from_components(directory_name, reference_file),
            "r",
            encoding=dcr_core.core_glob.FILE_ENCODING_DEFAULT,
        ) as tst_file:
            tst_lines = tst_file.readlines()
            tst_len = len(tst_lines)

        with open(
            dcr_core.core_utils.get_full_name_from_components(reference_directory, reference_file),
            "r",
            encoding=dcr_core.core_glob.FILE_ENCODING_DEFAULT,
        ) as ref_file:
            ref_lines = ref_file.readlines()
            ref_len = len(ref_lines)

        if tst_len != ref_len:
            tst_file.close()
            ref_file.close()
            assert False, f"file {reference_file} has {tst_len} lines instead of {ref_len}"

        is_equal = True

        for i in range(ref_len):
            if tst_lines[i] == ref_lines[i]:
                continue

            if extension == dcr_core.core_glob.FILE_TYPE_JSON:
                # multiple lines
                if is_line_type('                                    "tknRank": ', tst_lines[i], ref_lines[i]):
                    continue
                # single line
                if is_line_type('    "documentFileName": ', tst_lines[i], ref_lines[i]) or is_line_type(
                    '    "documentId": ', tst_lines[i], ref_lines[i]
                ):
                    continue

            if extension == dcr_core.core_glob.FILE_TYPE_XML:
                # multiple lines
                # single line
                if (
                    is_line_type("<CreationDate>", tst_lines[i], ref_lines[i])  # pylint: disable=too-many-boolean-expressions
                    or is_line_type("<Creation platform=", tst_lines[i], ref_lines[i])
                    or is_line_type("<Document filename=", tst_lines[i], ref_lines[i])
                    or is_line_type(' <Font id="F0" name="LMRoman10-Regular" fullname="', tst_lines[i], ref_lines[i])
                    or is_line_type("<Options>tetml=", tst_lines[i], ref_lines[i])
                    or is_line_type("<Producer>", tst_lines[i], ref_lines[i])
                ):
                    continue

            print(f"line no. : {i}")
            print(f"test file: {tst_lines[i].rstrip()}")
            print(f"reference: {ref_lines[i].rstrip()}")
            is_equal = False

        tst_file.close()
        ref_file.close()

        assert is_equal, f"file {reference_file} does not match reference file"


# -----------------------------------------------------------------------------
# Delete the original configuration parameter value.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def config_param_delete(config_section: str, config_param: str) -> None:
    """Delete the original configuration parameter value.

    Args:
        config_section (str): Configuration section.
        config_param (str): Configuration parameter.
    """
    CONFIG_PARSER.read(dcr_core.cls_setup.Setup._DCR_CFG_FILE)

    del CONFIG_PARSER[config_section][config_param]

    with open(dcr_core.cls_setup.Setup._DCR_CFG_FILE, "w", encoding=dcr_core.core_glob.FILE_ENCODING_DEFAULT) as configfile:
        CONFIG_PARSER.write(configfile)


# -----------------------------------------------------------------------------
# modify configuration parameter values.
# -----------------------------------------------------------------------------
# noinspection PyProtectedMember
@pytest.helpers.register
def config_params_modify(
    config_section: str,
    config_params: list[tuple[str, str]],
) -> None:
    """Backup and modify configuration parameter values.

    Args:
        config_section (str): Configuration section.
        config_params (list[tuple[str, str]]): Configuration parameter modifications.
    """
    CONFIG_PARSER.read(dcr_core.cls_setup.Setup._DCR_CFG_FILE)

    for (config_param, config_value) in config_params:
        CONFIG_PARSER[config_section][config_param] = config_value

    with open(dcr_core.cls_setup.Setup._DCR_CFG_FILE, "w", encoding=dcr_core.core_glob.FILE_ENCODING_DEFAULT) as configfile:
        CONFIG_PARSER.write(configfile)


# -----------------------------------------------------------------------------
# Copy files from the sample test file directory.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def copy_files_4_pytest(file_list: list[tuple[tuple[str, str | None], tuple[pathlib.Path, list[str], str | None]]]) -> None:
    """Copy files from the sample test file directory.

    Args:
        file_list (list[
            tuple[
                tuple[str, str | None],
                tuple[pathlib.Path, list[str], str | None]
            ]
        ]): list of files to be copied.
    """
    assert os.path.isdir(dcr_core.core_utils.get_os_independent_name(get_test_files_source_directory_name())), (
        "source directory '" + get_test_files_source_directory_name() + "' missing"
    )

    for ((source_stem, source_ext), (target_dir, target_file_comp, target_ext)) in file_list:
        source_file_name = source_stem if source_ext is None else source_stem + "." + source_ext
        source_file = dcr_core.core_utils.get_full_name_from_components(get_test_files_source_directory_name(), source_file_name)
        assert os.path.isfile(source_file), "source file '" + str(source_file) + "' missing"

        assert os.path.isdir(dcr_core.core_utils.get_os_independent_name(target_dir)), "target directory '" + target_dir + "' missing"
        target_file_name = "_".join(target_file_comp) if target_ext is None else "_".join(target_file_comp) + "." + target_ext
        target_file = dcr_core.core_utils.get_full_name_from_components(target_dir, target_file_name)
        assert os.path.isfile(target_file) is False, "target file '" + str(target_file) + "' already existing"

        shutil.copy(source_file, target_file)
        assert os.path.isfile(target_file), "target file '" + str(target_file) + "' is missing"


# -----------------------------------------------------------------------------
# Copy files from the sample test file directory.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def copy_files_4_pytest_2_dir(
    source_files: list[tuple[str, str | None]],
    target_path: pathlib.Path,
) -> None:
    """Copy files from the sample test file directory.

    Args:
        source_files: list[tuple[str, str | None]]: Source file names.
        target_path: Path: Target directory.
    """
    for source_file in source_files:
        (source_stem, source_ext) = source_file
        copy_files_4_pytest([(source_file, (target_path, [source_stem], source_ext))])


# -----------------------------------------------------------------------------
# Fixture - Before any test.
# -----------------------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def fxtr_before_any_test():
    """Fixture Factory: Before any test."""
    CONFIG_PARSER.read(dcr_core.cls_setup.Setup._DCR_CFG_FILE)

    # -----------------------------------------------------------------------------
    # Configuration: dcr_core.
    # -----------------------------------------------------------------------------
    for (config_param, config_value) in (
        (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_HEADING, "true"),
        (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_LIST_BULLET, "true"),
        (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_LIST_NUMBER, "true"),
        (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_TABLE, "true"),
        (dcr_core.cls_setup.Setup._DCR_CFG_DIRECTORY_INBOX, "data/inbox_test"),
        (dcr_core.cls_setup.Setup._DCR_CFG_JSON_INDENT, "4"),
        (dcr_core.cls_setup.Setup._DCR_CFG_JSON_SORT_KEYS, "false"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_FOOTER_MAX_DISTANCE, "3"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_FOOTER_MAX_LINES, "3"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_DISTANCE, "3"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_LINES, "3"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_HEADING_FILE_INCL_NO_CTX, "3"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_HEADING_FILE_INCL_REGEXP, "true"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_HEADING_MAX_LEVEL, "3"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_HEADING_MIN_PAGES, "2"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_HEADING_RULE_FILE, "data/lt_export_rule_heading_test.json"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_HEADING_TOLERANCE_LLX, "5"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_LIST_BULLET_MIN_ENTRIES, "2"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_LIST_BULLET_RULE_FILE, "data/lt_export_rule_list_bullet_test.json"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_LIST_BULLET_TOLERANCE_LLX, "5"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_LIST_NUMBER_FILE_INCL_REGEXP, "true"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_LIST_NUMBER_MIN_ENTRIES, "2"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_LIST_NUMBER_RULE_FILE, "data/lt_export_rule_list_number_test.json"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_LIST_NUMBER_TOLERANCE_LLX, "5"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_TABLE_FILE_INCL_EMPTY_COLUMNS, "false"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_TOC_LAST_PAGE, "5"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_TOC_MIN_ENTRIES, "5"),
        (dcr_core.cls_setup.Setup._DCR_CFG_PDF2IMAGE_TYPE, dcr_core.cls_setup.Setup.PDF2IMAGE_TYPE_JPEG),
        (dcr_core.cls_setup.Setup._DCR_CFG_TESSERACT_TIMEOUT, "30"),
        (dcr_core.cls_setup.Setup._DCR_CFG_TETML_PAGE, "true"),
        (dcr_core.cls_setup.Setup._DCR_CFG_TETML_WORD, "true"),
        (dcr_core.cls_setup.Setup._DCR_CFG_TOKENIZE_2_DATABASE, "true"),
        (dcr_core.cls_setup.Setup._DCR_CFG_TOKENIZE_2_JSONFILE, "true"),
        (dcr_core.cls_setup.Setup._DCR_CFG_VERBOSE, "true"),
        (dcr_core.cls_setup.Setup._DCR_CFG_VERBOSE_LT_HEADER_FOOTER, "false"),
        (dcr_core.cls_setup.Setup._DCR_CFG_VERBOSE_LT_HEADING, "false"),
        (dcr_core.cls_setup.Setup._DCR_CFG_VERBOSE_LT_LIST_BULLET, "false"),
        (dcr_core.cls_setup.Setup._DCR_CFG_VERBOSE_LT_LIST_NUMBER, "false"),
        (dcr_core.cls_setup.Setup._DCR_CFG_VERBOSE_LT_TABLE, "false"),
        (dcr_core.cls_setup.Setup._DCR_CFG_VERBOSE_LT_TOC, "false"),
        (dcr_core.cls_setup.Setup._DCR_CFG_VERBOSE_PARSER, "none"),
    ):
        CONFIG_PARSER[dcr_core.cls_setup.Setup._DCR_CFG_SECTION_CORE_ENV_TEST][config_param] = config_value


# -----------------------------------------------------------------------------
# Fixture - Create a new directory.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_mkdir():
    """Fixture Factory: Create a new directory."""

    def _fxtr_mkdir(directory_name: str):
        """
        Fixture: Create a new directory.

        Args:
            directory_name (str): The directory name including path.
        """
        os.makedirs(directory_name, exist_ok=True)

    return _fxtr_mkdir


# -----------------------------------------------------------------------------
# Fixture - Delete a directory.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_rmdir():
    """Fixture Factory: Delete a directory."""

    def _fxtr_rmdir(directory_name: str):
        """
        Fixture: Delete a directory.

        Args:
            directory_name (str): The directory name including path.
        """
        shutil.rmtree(directory_name)

    return _fxtr_rmdir


# -----------------------------------------------------------------------------
# Fixture - Delete a directory if existing.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_rmdir_opt(fxtr_rmdir):
    """Fixture Factory: Delete a directory if existing."""

    def _fxtr_rmdir_opt(directory_name: str):
        """
        Fixture: Delete a directory if existing.

        Args:
            directory_name (str): The directory name including path.
        """
        if os.path.isdir(directory_name):
            fxtr_rmdir(directory_name)

    return _fxtr_rmdir_opt


# -----------------------------------------------------------------------------
# Fixture - an empty directory.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_setup_empty_inbox(
    fxtr_mkdir,
    fxtr_rmdir_opt,
):
    """Fixture: Setup an empty directory."""
    setup_cfg_backup()

    dcr_core.core_glob.setup = dcr_core.cls_setup.Setup()

    fxtr_rmdir_opt(dcr_core.core_glob.setup.directory_inbox)
    fxtr_mkdir(dcr_core.core_glob.setup.directory_inbox)

    yield

    setup_cfg_restore()


# -----------------------------------------------------------------------------
# Provide the file directory name where the reference files are located.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def get_test_files_reference_directory_name():
    """Provide reference file directory.

    Provide the file directory name where the reference files are
    located.
    """
    suffix = platform.system().upper()

    return "tests/__PYTEST_REFERENCES__" + suffix + "/"


# -----------------------------------------------------------------------------
# Provide the file directory name where the test files are located.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def get_test_files_source_directory_name():
    """Provide test file directory.

    Provide the file directory name where the test files are located.
    """
    return "tests/__PYTEST_FILES__/"


# -----------------------------------------------------------------------------
# Backup the 'setup.cfg' file.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def setup_cfg_backup() -> None:
    """Backup the 'setup.cfg' file."""
    if os.path.isfile(FILE_NAME_SETUP_CFG_BACKUP):
        shutil.copy2(FILE_NAME_SETUP_CFG_BACKUP, FILE_NAME_SETUP_CFG)
    else:
        shutil.copy2(FILE_NAME_SETUP_CFG, FILE_NAME_SETUP_CFG_BACKUP)


# -----------------------------------------------------------------------------
# Search for a substring optionally starting from a certain position.
# -----------------------------------------------------------------------------
def is_line_type(search: str, line_1: str, line_2: str, search_pos: int = 0) -> bool:
    """Search for a substring optionally starting from a certain position.

    Args:
        search (str):
            Searched substring.
        line_1 (str):
            First line.
        line_2 (str):
            Second line.
        search_pos (int, optional):
            Expected position of the search string in the rows - relative to 0. Defaults to 0.

    Returns:
        bool: _description_
    """
    if line_1.find(search) == search_pos and line_2.find(search) == search_pos:
        return True

    return False


# -----------------------------------------------------------------------------
# Restore the 'setup.cfg' file.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def setup_cfg_restore():
    """Restore the 'setup.cfg' file."""
    if os.path.isfile(FILE_NAME_SETUP_CFG_BACKUP):
        shutil.copy2(FILE_NAME_SETUP_CFG_BACKUP, FILE_NAME_SETUP_CFG)
        os.remove(FILE_NAME_SETUP_CFG_BACKUP)
    else:
        assert False, f"The backup copy {FILE_NAME_SETUP_CFG_BACKUP} is missing"


# -----------------------------------------------------------------------------
# Verify the content of a file directory.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def verify_content_of_directory(
    directory_name: str,
    expected_directories: list[str],
    expected_files: list[str],
) -> None:
    """Verify the content of a file directory.

    Args:
        directory_name: str:
                   Name of the file directory to be checked.
        expected_directories: list[str]:
                   list of the expected directory names.
        expected_files: list[str]:
                   list of the expected file names.
    """
    directory_content = os.listdir(directory_name)

    # check directory content against expectations
    for elem in directory_content:
        elem_path = dcr_core.core_utils.get_full_name_from_components(directory_name, elem)
        if os.path.isdir(elem_path):
            assert elem in expected_directories, f"directory {elem} was not expected"
        else:
            assert elem in expected_files, f"file {elem} was not expected"

    # check expected directories against directory content
    for elem in expected_directories:
        assert elem in directory_content, f"expected directory {elem} is missing"
        elem_path = dcr_core.core_utils.get_full_name_from_components(directory_name, elem)
        assert os.path.isdir(dcr_core.core_utils.get_os_independent_name(elem_path)), f"expected directory {elem} is a file"

    # check expected files against directory content
    for elem in expected_files:
        assert elem in directory_content, f"expected file {elem} is missing"
        elem_path = dcr_core.core_utils.get_full_name_from_components(directory_name, elem)
        assert os.path.isfile(elem_path), f"expected file {elem} is a directory"


# -----------------------------------------------------------------------------
# Verify the created files.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def verify_created_files(directory_name, test_files):
    """Verify the created files."""
    verify_content_of_directory(
        directory_name,
        [],
        test_files,
    )

    compare_with_reference_files(
        directory_name,
        test_files,
    )
