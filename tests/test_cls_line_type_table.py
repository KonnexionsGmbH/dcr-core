# pylint: disable=unused-argument
"""Testing Class LineTypeTable."""
import pytest

import dcr_core
import dcr_core.cls_process

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Cases Line Type Table.
# -----------------------------------------------------------------------------
@pytest.mark.parametrize(
    "input_output",
    [
        # input_output0
        (
            "docx_table",
            "pdf",
            [
                "docx_table.line.json",
                "docx_table.line.xml",
                "docx_table.line_table.json",
                "docx_table.line_token.json",
                "docx_table.page.json",
                "docx_table.page.xml",
                "docx_table.pdf",
                "docx_table.word.json",
                "docx_table.word.xml",
            ],
        ),
    ],
)
def test_line_type_table(input_output: tuple[str, str, list[str]], fxtr_setup_empty_inbox):
    """Test Cases Line Type Table."""
    # -------------------------------------------------------------------------
    directory_name = dcr_core.core_glob.setup.directory_inbox
    (stem_name, file_extension, test_files) = input_output

    full_name = dcr_core.core_utils.get_full_name_from_components(directory_name, stem_name, file_extension)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            (stem_name, file_extension),
        ],
        target_path=directory_name,
    )

    # -------------------------------------------------------------------------
    instance = dcr_core.cls_process.Process()

    instance.document_process(full_name)

    # -------------------------------------------------------------------------
    pytest.helpers.verify_created_files(directory_name, test_files)


# -----------------------------------------------------------------------------
# Test Cases Line Type Table - Coverage.
# -----------------------------------------------------------------------------
def test_line_type_table_coverage(fxtr_rmdir_opt, fxtr_setup_empty_inbox):
    """Test Cases Line Type Table - Coverage."""
    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_TABLE, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_VERBOSE_LT_TABLE, "true"),
        ],
    )

    # -------------------------------------------------------------------------
    directory_name = dcr_core.core_glob.setup.directory_inbox
    stem_name = "docx_table"
    file_extension = "pdf"

    full_name = dcr_core.core_utils.get_full_name_from_components(directory_name, stem_name, file_extension)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            (stem_name, file_extension),
        ],
        target_path=directory_name,
    )

    # -------------------------------------------------------------------------
    instance = dcr_core.cls_process.Process()

    instance.document_process(full_name)

    # -------------------------------------------------------------------------
    instance_e = dcr_core.cls_line_type_table.LineTypeTable()

    instance_e.exists()
