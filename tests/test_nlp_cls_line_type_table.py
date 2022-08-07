# pylint: disable=unused-argument
"""Testing Module nlp.cls_line_type_table."""

import dcr_core.cls_line_type_table
import dcr_core.cls_setup
import dcr_core.cls_text_parser
import dcr_core.cls_tokenizer_spacy
import dcr_core.core_glob
import dcr_core.core_utils
import pytest

import dcr.cfg.cls_setup
import dcr.cfg.glob
import dcr.db.cls_action
import dcr.db.cls_db_core
import dcr.db.cls_document
import dcr.db.cls_run
import dcr.launcher

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test LineType Heading - maximum version.
# -----------------------------------------------------------------------------
@pytest.mark.parametrize("create_extra_file_table", ["false", "true"])
def test_line_type_table_maximum(create_extra_file_table, fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test LineType Heading - maximum version."""
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("docx_table", "pdf"),
        ],
        target_path=dcr_core.core_glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr.cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
        ],
    )
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_TABLE, create_extra_file_table),
            (dcr_core.cls_setup.Setup._DCR_CFG_LT_FOOTER_MAX_LINES, "0"),
            (dcr_core.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_LINES, "0"),
            (dcr_core.cls_setup.Setup._DCR_CFG_LT_HEADING_MAX_LEVEL, "0"),
            (dcr_core.cls_setup.Setup._DCR_CFG_VERBOSE_LT_TABLE, "true"),
        ],
    )

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.check_json_line("docx_table.line.json", no_tables_in_document=4)

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_TOKENIZE])

    pytest.helpers.check_json_line("docx_table.line_token.json", no_tables_in_document=4)

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.info("=========> test_line_type_table_maximum_2 <=========")

    pytest.helpers.check_dbt_document(
        (
            1,
            (
                1,
                "tkn",
                "tokenizer     (nlp)",
                dcr_core.core_utils.get_os_independent_name("data\\inbox_test"),
                "",
                "",
                0,
                "docx_table.pdf",
                1,
                4,
                0,
                0,
                0,
                0,
                0,
                4,
                5,
                "end",
            ),
        )
    )

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.info("=========> test_line_type_table_maximum_3 <=========")

    expected_files = [
        "docx_table.line.json",
        "docx_table.line.xml",
        "docx_table.line_token.json",
        "docx_table.page.json",
        "docx_table.page.xml",
        "docx_table.pdf",
        "docx_table.word.json",
        "docx_table.word.xml",
    ]

    if create_extra_file_table == "true":
        expected_files.append(
            "docx_table.line_table.json",
        )

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            expected_files,
        ),
    )

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test LineType Heading - minimum version.
# -----------------------------------------------------------------------------
def test_line_type_table_minimum(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test LineType Heading - minimum version."""
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("docx_table", "pdf"),
        ],
        target_path=dcr_core.core_glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_TETML_PAGE, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_TETML_WORD, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_TOKENIZE_2_JSONFILE, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_TABLE, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_LT_FOOTER_MAX_LINES, "0"),
            (dcr_core.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_LINES, "0"),
            (dcr_core.cls_setup.Setup._DCR_CFG_LT_HEADING_MAX_LEVEL, "0"),
        ],
    )

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.check_json_line("docx_table.line.json", no_tables_in_document=4)

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_TOKENIZE])

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.info("=========> test_line_type_table_2_2 <=========")

    pytest.helpers.check_dbt_document(
        (
            1,
            (
                1,
                "tkn",
                "tokenizer     (nlp)",
                dcr_core.core_utils.get_os_independent_name("data\\inbox_test"),
                "",
                "",
                0,
                "docx_table.pdf",
                1,
                4,
                0,
                0,
                0,
                0,
                0,
                4,
                5,
                "end",
            ),
        )
    )

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.info("=========> test_line_type_table_2_3 <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "docx_table.pdf",
            ],
        ),
    )

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - line_type_table - coverage - exists.
# -----------------------------------------------------------------------------
def test_line_type_table_missing_dependencies_coverage_exists(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - line_type_table - coverage - exists."""
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore()

    # -------------------------------------------------------------------------
    dcr.cfg.glob.run = dcr.db.cls_run.Run(
        _row_id=1,
        action_code=dcr.db.cls_run.Run.ACTION_CODE_INBOX,
    )

    # -------------------------------------------------------------------------
    dcr.cfg.glob.action_curr = dcr.db.cls_action.Action(
        _row_id=1,
        action_code=dcr.db.cls_run.Run.ACTION_CODE_INBOX,
        id_run_last=1,
    )

    # -------------------------------------------------------------------------
    dcr.cfg.glob.document = dcr.db.cls_document.Document(
        action_code_last="", directory_name="", file_name="", id_language=0, id_run_last=0, _row_id=4711
    )

    # -------------------------------------------------------------------------
    dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    # -------------------------------------------------------------------------
    dcr_core.core_glob.text_parser = dcr_core.cls_text_parser.TextParser()

    # -------------------------------------------------------------------------
    instance = dcr_core.cls_line_type_table.LineTypeTable(
        file_name_curr=dcr.cfg.glob.action_curr.action_file_name,
    )

    instance.exists()

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - line_type_table - TextParser.
# -----------------------------------------------------------------------------
def test_line_type_table_missing_dependencies_text_parser(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - line_type_table - TextParser."""
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore()

    # -------------------------------------------------------------------------
    dcr.cfg.glob.run = dcr.db.cls_run.Run(
        _row_id=1,
        action_code=dcr.db.cls_run.Run.ACTION_CODE_INBOX,
    )

    # -------------------------------------------------------------------------
    dcr.cfg.glob.action_curr = dcr.db.cls_action.Action(
        _row_id=1,
        action_code=dcr.db.cls_run.Run.ACTION_CODE_INBOX,
        id_run_last=1,
    )

    # -------------------------------------------------------------------------
    dcr.cfg.glob.document = dcr.db.cls_document.Document(
        action_code_last="", directory_name="", file_name="", id_language=0, id_run_last=0, _row_id=4711
    )

    # -------------------------------------------------------------------------
    dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_text_parser=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr_core.cls_line_type_table.LineTypeTable(
            file_name_curr=dcr.cfg.glob.action_curr.action_file_name,
        )

    assert expt.type == SystemExit, "Instance of class 'TextParser' is missing"
    assert expt.value.code == 1, "Instance of class 'TextParser' is missing"

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)
