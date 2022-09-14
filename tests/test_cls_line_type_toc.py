# pylint: disable=unused-argument
"""Testing Class LineTypeToc."""
import pytest

import dcr_core.cls_process as process
from dcr_core import core_glob
from dcr_core import core_utils

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
                "pdf_toc_line_bullet_list.json",
                "pdf_toc_line_bullet_list.xml",
                "pdf_toc_line_bullet_list.list_bullet.json",
                "pdf_toc_line_bullet_list.list_number.json",
                "pdf_toc_line_bullet_list.token.json",
                "pdf_toc_line_bullet_list.pdf",
            ],
        ),
        # input_output1
        (
            "pdf_toc_table_bullet_list",
            "pdf",
            [
                "pdf_toc_table_bullet_list.json",
                "pdf_toc_table_bullet_list.xml",
                "pdf_toc_table_bullet_list.list_bullet.json",
                "pdf_toc_table_bullet_list.list_number.json",
                "pdf_toc_table_bullet_list.token.json",
                "pdf_toc_table_bullet_list.pdf",
            ],
        ),
    ],
)
def test(input_output: tuple[str, str, list[str]], fxtr_setup_empty_inbox):
    """Test Cases Line Type Toc."""
    # -------------------------------------------------------------------------
    directory_name = core_glob.setup.directory_inbox
    (stem_name, file_extension, test_files) = input_output

    full_name = core_utils.get_full_name_from_components(directory_name, stem_name, file_extension)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            (stem_name, file_extension),
        ],
        target_path=directory_name,
    )

    # -------------------------------------------------------------------------
    instance = process.Process()

    instance.document(full_name, is_delete_auxiliary_files=False)

    # -------------------------------------------------------------------------
    pytest.helpers.verify_created_files(directory_name, test_files)
