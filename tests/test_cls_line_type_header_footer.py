# pylint: disable=unused-argument
"""Testing Class LineTypeHeaderFooter."""
import pytest

import dcr_core.cls_process as process
import dcr_core.core_glob as glob
import dcr_core.core_utils as utils

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Cases Line Type Headers & Footers.
# -----------------------------------------------------------------------------
@pytest.mark.parametrize(
    "input_output",
    [
        # input_output0
        (
            "p_1_h_0_f_0",
            "pdf",
            [
                "p_1_h_0_f_0.json",
                "p_1_h_0_f_0.pdf",
                "p_1_h_0_f_0.token.json",
                "p_1_h_0_f_0.xml",
            ],
        ),
        # input_output1
        (
            "p_2_h_0_f_2",
            "pdf",
            [
                "p_2_h_0_f_2.json",
                "p_2_h_0_f_2.pdf",
                "p_2_h_0_f_2.token.json",
                "p_2_h_0_f_2.xml",
            ],
        ),
        # input_output2
        (
            "p_2_h_1_f_0",
            "pdf",
            [
                "p_2_h_1_f_0.json",
                "p_2_h_1_f_0.pdf",
                "p_2_h_1_f_0.token.json",
                "p_2_h_1_f_0.xml",
            ],
        ),
        # input_output3
        (
            "p_2_h_1_f_1",
            "pdf",
            [
                "p_2_h_1_f_1.json",
                "p_2_h_1_f_1.pdf",
                "p_2_h_1_f_1.token.json",
                "p_2_h_1_f_1.xml",
            ],
        ),
        # input_output4
        (
            "p_2_h_2_f_0",
            "pdf",
            [
                "p_2_h_2_f_0.json",
                "p_2_h_2_f_0.pdf",
                "p_2_h_2_f_0.token.json",
                "p_2_h_2_f_0.xml",
            ],
        ),
        # input_output5
        (
            "p_2_h_2_f_2",
            "pdf",
            [
                "p_2_h_2_f_2.json",
                "p_2_h_2_f_2.pdf",
                "p_2_h_2_f_2.token.json",
                "p_2_h_2_f_2.xml",
            ],
        ),
        # input_output6
        (
            "p_3_h_0_f_4",
            "pdf",
            [
                "p_3_h_0_f_4.json",
                "p_3_h_0_f_4.pdf",
                "p_3_h_0_f_4.token.json",
                "p_3_h_0_f_4.xml",
            ],
        ),
        # input_output7
        (
            "p_3_h_2_f_2",
            "pdf",
            [
                "p_3_h_2_f_2.json",
                "p_3_h_2_f_2.pdf",
                "p_3_h_2_f_2.token.json",
                "p_3_h_2_f_2.xml",
            ],
        ),
        # input_output8
        (
            "p_3_h_3_f_3",
            "pdf",
            [
                "p_3_h_3_f_3.json",
                "p_3_h_3_f_3.pdf",
                "p_3_h_3_f_3.token.json",
                "p_3_h_3_f_3.xml",
            ],
        ),
        # input_output9
        (
            "p_3_h_4_f_0",
            "pdf",
            [
                "p_3_h_4_f_0.json",
                "p_3_h_4_f_0.pdf",
                "p_3_h_4_f_0.token.json",
                "p_3_h_4_f_0.xml",
            ],
        ),
        # input_output10
        (
            "p_3_h_4_f_4",
            "pdf",
            [
                "p_3_h_4_f_4.json",
                "p_3_h_4_f_4.pdf",
                "p_3_h_4_f_4.token.json",
                "p_3_h_4_f_4.xml",
            ],
        ),
        # input_output11
        (
            "p_4_h_4_f_4_different_first",
            "pdf",
            [
                "p_4_h_4_f_4_different_first.json",
                "p_4_h_4_f_4_different_first.pdf",
                "p_4_h_4_f_4_different_first.token.json",
                "p_4_h_4_f_4_different_first.xml",
            ],
        ),
        # input_output12
        (
            "p_4_h_4_f_4_different_last",
            "pdf",
            [
                "p_4_h_4_f_4_different_last.json",
                "p_4_h_4_f_4_different_last.pdf",
                "p_4_h_4_f_4_different_last.token.json",
                "p_4_h_4_f_4_different_last.xml",
            ],
        ),
        # input_output13
        (
            "p_4_h_4_f_4_empty_first",
            "pdf",
            [
                "p_4_h_4_f_4_empty_first.json",
                "p_4_h_4_f_4_empty_first.pdf",
                "p_4_h_4_f_4_empty_first.token.json",
                "p_4_h_4_f_4_empty_first.xml",
            ],
        ),
        # input_output14
        (
            "p_4_h_4_f_4_empty_last",
            "pdf",
            [
                "p_4_h_4_f_4_empty_last.json",
                "p_4_h_4_f_4_empty_last.pdf",
                "p_4_h_4_f_4_empty_last.token.json",
                "p_4_h_4_f_4_empty_last.xml",
            ],
        ),
        # input_output15
        (
            "p_5_h_0_f_0",
            "pdf",
            [
                "p_5_h_0_f_0.json",
                "p_5_h_0_f_0.pdf",
                "p_5_h_0_f_0.token.json",
                "p_5_h_0_f_0.xml",
            ],
        ),
        # input_output16
        (
            "p_5_h_0_f_2",
            "pdf",
            [
                "p_5_h_0_f_2.json",
                "p_5_h_0_f_2.pdf",
                "p_5_h_0_f_2.token.json",
                "p_5_h_0_f_2.xml",
            ],
        ),
        # input_output17
        (
            "p_5_h_2_f_0",
            "pdf",
            [
                "p_5_h_2_f_0.json",
                "p_5_h_2_f_0.pdf",
                "p_5_h_2_f_0.token.json",
                "p_5_h_2_f_0.xml",
            ],
        ),
        # input_output18
        (
            "p_5_h_2_f_2",
            "pdf",
            [
                "p_5_h_2_f_2.json",
                "p_5_h_2_f_2.pdf",
                "p_5_h_2_f_2.token.json",
                "p_5_h_2_f_2.xml",
            ],
        ),
        # input_output19
        (
            "p_5_h_4_f_4_different_both",
            "pdf",
            [
                "p_5_h_4_f_4_different_both.json",
                "p_5_h_4_f_4_different_both.pdf",
                "p_5_h_4_f_4_different_both.token.json",
                "p_5_h_4_f_4_different_both.xml",
            ],
        ),
        # input_output20
        (
            "p_5_h_4_f_4_empty_both",
            "pdf",
            [
                "p_5_h_4_f_4_empty_both.json",
                "p_5_h_4_f_4_empty_both.pdf",
                "p_5_h_4_f_4_empty_both.token.json",
                "p_5_h_4_f_4_empty_both.xml",
            ],
        ),
        # input_output21
        (
            "p_5_h_4_f_4_empty_center",
            "pdf",
            [
                "p_5_h_4_f_4_empty_center.json",
                "p_5_h_4_f_4_empty_center.pdf",
                "p_5_h_4_f_4_empty_center.token.json",
                "p_5_h_4_f_4_empty_center.xml",
            ],
        ),
        # input_output22
        (
            "p_5_h_X_f_X",
            "pdf",
            [
                "p_5_h_X_f_X.json",
                "p_5_h_X_f_X.pdf",
                "p_5_h_X_f_X.token.json",
                "p_5_h_X_f_X.xml",
            ],
        ),
    ],
)
def test(input_output: tuple[str, str, list[str]], fxtr_setup_empty_inbox):
    """Test Cases Line Type Headers & Footers."""
    # -------------------------------------------------------------------------
    directory_name = glob.setup.directory_inbox
    (stem_name, file_extension, test_files) = input_output

    full_name = utils.get_full_name_from_components(directory_name, stem_name, file_extension)

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
