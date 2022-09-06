# pylint: disable=unused-argument
"""Testing Class LineTypeHeading."""
import pytest

import dcr_core.cls_line_type_header_footer
import dcr_core.cls_line_type_list_bullet
import dcr_core.cls_line_type_list_number
import dcr_core.cls_line_type_table
import dcr_core.cls_line_type_toc
import dcr_core.cls_process
import dcr_core.cls_text_parser

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Cases Line Type Heading.
# -----------------------------------------------------------------------------
@pytest.mark.parametrize(
    "input_output",
    [
        # input_output0
        (
            "docx_heading",
            "pdf",
            [
                "docx_heading.line.json",
                "docx_heading.line.xml",
                "docx_heading.line_heading.json",
                "docx_heading.line_list_number.json",
                "docx_heading.line_table.json",
                "docx_heading.line_token.json",
                "docx_heading.page.json",
                "docx_heading.page.xml",
                "docx_heading.pdf",
                "docx_heading.word.json",
                "docx_heading.word.xml",
            ],
        ),
    ],
)
def test(input_output: tuple[str, str, list[str]], fxtr_setup_empty_inbox):
    """Test Cases Line Type Heading."""
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

    instance.document(full_name, is_delete_auxiliary_files=False)

    # -------------------------------------------------------------------------
    pytest.helpers.verify_created_files(directory_name, test_files)
