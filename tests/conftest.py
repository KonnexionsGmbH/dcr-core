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
import shutil

import pytest

import dcr_core.cls_setup
import dcr_core.core_glob

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
CONFIG_PARSER: configparser.ConfigParser = configparser.ConfigParser()

FILE_NAME_SETUP_CFG = "setup.cfg"
FILE_NAME_SETUP_CFG_BACKUP = "setup.cfg_backup"


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
    assert os.path.isdir(dcr_core.core_utils.get_os_independent_name(get_test_inbox_directory_name())), (
        "source directory '" + get_test_inbox_directory_name() + "' missing"
    )

    for ((source_stem, source_ext), (target_dir, target_file_comp, target_ext)) in file_list:
        source_file_name = source_stem if source_ext is None else source_stem + "." + source_ext
        source_file = dcr_core.core_utils.get_full_name_from_components(get_test_inbox_directory_name(), source_file_name)
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
        (dcr_core.cls_setup.Setup._DCR_CFG_JSON_INDENT, "4"),
        (dcr_core.cls_setup.Setup._DCR_CFG_JSON_SORT_KEYS, "false"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_EXPORT_RULE_FILE_HEADING, "tmp/lt_export_rule_heading.json"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_EXPORT_RULE_FILE_LIST_BULLET, "tmp/lt_export_rule_list_bullet.json"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_EXPORT_RULE_FILE_LIST_NUMBER, "tmp/lt_export_rule_list_number.json"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_FOOTER_MAX_DISTANCE, "3"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_FOOTER_MAX_LINES, "3"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_DISTANCE, "3"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_LINES, "3"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_HEADING_FILE_INCL_NO_CTX, "3"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_HEADING_FILE_INCL_REGEXP, "false"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_HEADING_MAX_LEVEL, "3"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_HEADING_MIN_PAGES, "2"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_HEADING_RULE_FILE, "data/lt_export_rule_heading_test.json"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_HEADING_TOLERANCE_LLX, "5"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_LIST_BULLET_MIN_ENTRIES, "2"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_LIST_BULLET_RULE_FILE, "data/lt_export_rule_list_bullet_test.json"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_LIST_BULLET_TOLERANCE_LLX, "5"),
        (dcr_core.cls_setup.Setup._DCR_CFG_LT_LIST_NUMBER_FILE_INCL_REGEXP, "false"),
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
        (dcr_core.cls_setup.Setup._DCR_CFG_VERBOSE_LT_HEADERS_FOOTERS, "false"),
        (dcr_core.cls_setup.Setup._DCR_CFG_VERBOSE_LT_HEADING, "false"),
        (dcr_core.cls_setup.Setup._DCR_CFG_VERBOSE_LT_LIST_BULLET, "false"),
        (dcr_core.cls_setup.Setup._DCR_CFG_VERBOSE_LT_LIST_NUMBER, "false"),
        (dcr_core.cls_setup.Setup._DCR_CFG_VERBOSE_LT_TABLE, "false"),
        (dcr_core.cls_setup.Setup._DCR_CFG_VERBOSE_LT_TOC, "false"),
        (dcr_core.cls_setup.Setup._DCR_CFG_VERBOSE_PARSER, "none"),
    ):
        CONFIG_PARSER[dcr_core.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST][config_param] = config_value


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
# Fixture - Setup empty database and empty inboxes.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_setup_empty_inbox(
    fxtr_mkdir,
    fxtr_rmdir_opt,
):
    """Fixture: Setup empty database and empty inboxes."""
    setup_cfg_backup()

    dcr_core.core_glob.setup = dcr_core.cls_setup.Setup()

    fxtr_rmdir_opt(dcr_core.core_glob.setup.directory_inbox)
    fxtr_mkdir(dcr_core.core_glob.setup.directory_inbox)

    yield

    fxtr_rmdir_opt(dcr_core.core_glob.setup.directory_inbox)

    setup_cfg_restore()


# -----------------------------------------------------------------------------
# Provide the directory name of the inbox with the test data.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def get_test_inbox_directory_name():
    """Provide the directory name of the inbox with the test data."""
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