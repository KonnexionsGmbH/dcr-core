# pylint: disable=unused-argument
"""Testing Class LineTypeToc."""
import pytest

import dcr_core
import dcr_core.cls_line_type_header_footer
import dcr_core.cls_process
import dcr_core.cls_text_parser

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Cases Line Type Toc.
# -----------------------------------------------------------------------------
@pytest.mark.parametrize(
    "input_output",
    [
        # input_output0
        (
            "pdf_toc_line_bullet_list",
            "pdf",
            [
                "pdf_toc_line_bullet_list.line.json",
                "pdf_toc_line_bullet_list.line.xml",
                "pdf_toc_line_bullet_list.line_list_bullet.json",
                "pdf_toc_line_bullet_list.line_list_number.json",
                "pdf_toc_line_bullet_list.line_token.json",
                "pdf_toc_line_bullet_list.page.json",
                "pdf_toc_line_bullet_list.page.xml",
                "pdf_toc_line_bullet_list.pdf",
                "pdf_toc_line_bullet_list.word.json",
                "pdf_toc_line_bullet_list.word.xml",
            ],
        ),
        # input_output1
        (
            "pdf_toc_table_bullet_list",
            "pdf",
            [
                "pdf_toc_table_bullet_list.line.json",
                "pdf_toc_table_bullet_list.line.xml",
                "pdf_toc_table_bullet_list.line_list_bullet.json",
                "pdf_toc_table_bullet_list.line_list_number.json",
                "pdf_toc_table_bullet_list.line_token.json",
                "pdf_toc_table_bullet_list.page.json",
                "pdf_toc_table_bullet_list.page.xml",
                "pdf_toc_table_bullet_list.pdf",
                "pdf_toc_table_bullet_list.word.json",
                "pdf_toc_table_bullet_list.word.xml",
            ],
        ),
    ],
)
def test(input_output: tuple[str, str, list[str]], fxtr_setup_empty_inbox):
    """Test Cases Line Type Toc."""
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

    instance.document(full_name)

    # -------------------------------------------------------------------------
    pytest.helpers.verify_created_files(directory_name, test_files)
