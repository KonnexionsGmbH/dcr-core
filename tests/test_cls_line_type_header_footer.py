# pylint: disable=unused-argument
"""Testing Class LineTypeHeaderFooter."""
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
                "p_1_h_0_f_0.line.json",
                "p_1_h_0_f_0.line.xml",
                "p_1_h_0_f_0.line_token.json",
                "p_1_h_0_f_0.page.json",
                "p_1_h_0_f_0.page.xml",
                "p_1_h_0_f_0.pdf",
                "p_1_h_0_f_0.word.json",
                "p_1_h_0_f_0.word.xml",
            ],
        ),
        # input_output1
        (
            "p_2_h_0_f_2",
            "pdf",
            [
                "p_2_h_0_f_2.line.json",
                "p_2_h_0_f_2.line.xml",
                "p_2_h_0_f_2.line_token.json",
                "p_2_h_0_f_2.page.json",
                "p_2_h_0_f_2.page.xml",
                "p_2_h_0_f_2.pdf",
                "p_2_h_0_f_2.word.json",
                "p_2_h_0_f_2.word.xml",
            ],
        ),
        # input_output2
        (
            "p_2_h_1_f_0",
            "pdf",
            [
                "p_2_h_1_f_0.line.json",
                "p_2_h_1_f_0.line.xml",
                "p_2_h_1_f_0.line_token.json",
                "p_2_h_1_f_0.page.json",
                "p_2_h_1_f_0.page.xml",
                "p_2_h_1_f_0.pdf",
                "p_2_h_1_f_0.word.json",
                "p_2_h_1_f_0.word.xml",
            ],
        ),
        # input_output3
        (
            "p_2_h_1_f_1",
            "pdf",
            [
                "p_2_h_1_f_1.line.json",
                "p_2_h_1_f_1.line.xml",
                "p_2_h_1_f_1.line_token.json",
                "p_2_h_1_f_1.page.json",
                "p_2_h_1_f_1.page.xml",
                "p_2_h_1_f_1.pdf",
                "p_2_h_1_f_1.word.json",
                "p_2_h_1_f_1.word.xml",
            ],
        ),
        # input_output4
        (
            "p_2_h_2_f_0",
            "pdf",
            [
                "p_2_h_2_f_0.line.json",
                "p_2_h_2_f_0.line.xml",
                "p_2_h_2_f_0.line_token.json",
                "p_2_h_2_f_0.page.json",
                "p_2_h_2_f_0.page.xml",
                "p_2_h_2_f_0.pdf",
                "p_2_h_2_f_0.word.json",
                "p_2_h_2_f_0.word.xml",
            ],
        ),
        # input_output5
        (
            "p_2_h_2_f_2",
            "pdf",
            [
                "p_2_h_2_f_2.line.json",
                "p_2_h_2_f_2.line.xml",
                "p_2_h_2_f_2.line_token.json",
                "p_2_h_2_f_2.page.json",
                "p_2_h_2_f_2.page.xml",
                "p_2_h_2_f_2.pdf",
                "p_2_h_2_f_2.word.json",
                "p_2_h_2_f_2.word.xml",
            ],
        ),
        # input_output6
        (
            "p_3_h_0_f_4",
            "pdf",
            [
                "p_3_h_0_f_4.line.json",
                "p_3_h_0_f_4.line.xml",
                "p_3_h_0_f_4.line_token.json",
                "p_3_h_0_f_4.page.json",
                "p_3_h_0_f_4.page.xml",
                "p_3_h_0_f_4.pdf",
                "p_3_h_0_f_4.word.json",
                "p_3_h_0_f_4.word.xml",
            ],
        ),
        # input_output7
        (
            "p_3_h_2_f_2",
            "pdf",
            [
                "p_3_h_2_f_2.line.json",
                "p_3_h_2_f_2.line.xml",
                "p_3_h_2_f_2.line_token.json",
                "p_3_h_2_f_2.page.json",
                "p_3_h_2_f_2.page.xml",
                "p_3_h_2_f_2.pdf",
                "p_3_h_2_f_2.word.json",
                "p_3_h_2_f_2.word.xml",
            ],
        ),
        # input_output8
        (
            "p_3_h_3_f_3",
            "pdf",
            [
                "p_3_h_3_f_3.line.json",
                "p_3_h_3_f_3.line.xml",
                "p_3_h_3_f_3.line_token.json",
                "p_3_h_3_f_3.page.json",
                "p_3_h_3_f_3.page.xml",
                "p_3_h_3_f_3.pdf",
                "p_3_h_3_f_3.word.json",
                "p_3_h_3_f_3.word.xml",
            ],
        ),
        # input_output9
        (
            "p_3_h_4_f_0",
            "pdf",
            [
                "p_3_h_4_f_0.line.json",
                "p_3_h_4_f_0.line.xml",
                "p_3_h_4_f_0.line_token.json",
                "p_3_h_4_f_0.page.json",
                "p_3_h_4_f_0.page.xml",
                "p_3_h_4_f_0.pdf",
                "p_3_h_4_f_0.word.json",
                "p_3_h_4_f_0.word.xml",
            ],
        ),
        # input_output10
        (
            "p_3_h_4_f_4",
            "pdf",
            [
                "p_3_h_4_f_4.line.json",
                "p_3_h_4_f_4.line.xml",
                "p_3_h_4_f_4.line_token.json",
                "p_3_h_4_f_4.page.json",
                "p_3_h_4_f_4.page.xml",
                "p_3_h_4_f_4.pdf",
                "p_3_h_4_f_4.word.json",
                "p_3_h_4_f_4.word.xml",
            ],
        ),
        # input_output11
        (
            "p_4_h_4_f_4_different_first",
            "pdf",
            [
                "p_4_h_4_f_4_different_first.line.json",
                "p_4_h_4_f_4_different_first.line.xml",
                "p_4_h_4_f_4_different_first.line_token.json",
                "p_4_h_4_f_4_different_first.page.json",
                "p_4_h_4_f_4_different_first.page.xml",
                "p_4_h_4_f_4_different_first.pdf",
                "p_4_h_4_f_4_different_first.word.json",
                "p_4_h_4_f_4_different_first.word.xml",
            ],
        ),
        # input_output12
        (
            "p_4_h_4_f_4_different_last",
            "pdf",
            [
                "p_4_h_4_f_4_different_last.line.json",
                "p_4_h_4_f_4_different_last.line.xml",
                "p_4_h_4_f_4_different_last.line_token.json",
                "p_4_h_4_f_4_different_last.page.json",
                "p_4_h_4_f_4_different_last.page.xml",
                "p_4_h_4_f_4_different_last.pdf",
                "p_4_h_4_f_4_different_last.word.json",
                "p_4_h_4_f_4_different_last.word.xml",
            ],
        ),
        # input_output13
        (
            "p_4_h_4_f_4_empty_first",
            "pdf",
            [
                "p_4_h_4_f_4_empty_first.line.json",
                "p_4_h_4_f_4_empty_first.line.xml",
                "p_4_h_4_f_4_empty_first.line_token.json",
                "p_4_h_4_f_4_empty_first.page.json",
                "p_4_h_4_f_4_empty_first.page.xml",
                "p_4_h_4_f_4_empty_first.pdf",
                "p_4_h_4_f_4_empty_first.word.json",
                "p_4_h_4_f_4_empty_first.word.xml",
            ],
        ),
        # input_output14
        (
            "p_4_h_4_f_4_empty_last",
            "pdf",
            [
                "p_4_h_4_f_4_empty_last.line.json",
                "p_4_h_4_f_4_empty_last.line.xml",
                "p_4_h_4_f_4_empty_last.line_token.json",
                "p_4_h_4_f_4_empty_last.page.json",
                "p_4_h_4_f_4_empty_last.page.xml",
                "p_4_h_4_f_4_empty_last.pdf",
                "p_4_h_4_f_4_empty_last.word.json",
                "p_4_h_4_f_4_empty_last.word.xml",
            ],
        ),
        # input_output15
        (
            "p_5_h_0_f_0",
            "pdf",
            [
                "p_5_h_0_f_0.line.json",
                "p_5_h_0_f_0.line.xml",
                "p_5_h_0_f_0.line_token.json",
                "p_5_h_0_f_0.page.json",
                "p_5_h_0_f_0.page.xml",
                "p_5_h_0_f_0.pdf",
                "p_5_h_0_f_0.word.json",
                "p_5_h_0_f_0.word.xml",
            ],
        ),
        # input_output16
        (
            "p_5_h_0_f_2",
            "pdf",
            [
                "p_5_h_0_f_2.line.json",
                "p_5_h_0_f_2.line.xml",
                "p_5_h_0_f_2.line_token.json",
                "p_5_h_0_f_2.page.json",
                "p_5_h_0_f_2.page.xml",
                "p_5_h_0_f_2.pdf",
                "p_5_h_0_f_2.word.json",
                "p_5_h_0_f_2.word.xml",
            ],
        ),
        # input_output17
        (
            "p_5_h_2_f_0",
            "pdf",
            [
                "p_5_h_2_f_0.line.json",
                "p_5_h_2_f_0.line.xml",
                "p_5_h_2_f_0.line_token.json",
                "p_5_h_2_f_0.page.json",
                "p_5_h_2_f_0.page.xml",
                "p_5_h_2_f_0.pdf",
                "p_5_h_2_f_0.word.json",
                "p_5_h_2_f_0.word.xml",
            ],
        ),
        # input_output18
        (
            "p_5_h_2_f_2",
            "pdf",
            [
                "p_5_h_2_f_2.line.json",
                "p_5_h_2_f_2.line.xml",
                "p_5_h_2_f_2.line_token.json",
                "p_5_h_2_f_2.page.json",
                "p_5_h_2_f_2.page.xml",
                "p_5_h_2_f_2.pdf",
                "p_5_h_2_f_2.word.json",
                "p_5_h_2_f_2.word.xml",
            ],
        ),
        # input_output19
        (
            "p_5_h_4_f_4_different_both",
            "pdf",
            [
                "p_5_h_4_f_4_different_both.line.json",
                "p_5_h_4_f_4_different_both.line.xml",
                "p_5_h_4_f_4_different_both.line_token.json",
                "p_5_h_4_f_4_different_both.page.json",
                "p_5_h_4_f_4_different_both.page.xml",
                "p_5_h_4_f_4_different_both.pdf",
                "p_5_h_4_f_4_different_both.word.json",
                "p_5_h_4_f_4_different_both.word.xml",
            ],
        ),
        # input_output20
        (
            "p_5_h_4_f_4_empty_both",
            "pdf",
            [
                "p_5_h_4_f_4_empty_both.line.json",
                "p_5_h_4_f_4_empty_both.line.xml",
                "p_5_h_4_f_4_empty_both.line_token.json",
                "p_5_h_4_f_4_empty_both.page.json",
                "p_5_h_4_f_4_empty_both.page.xml",
                "p_5_h_4_f_4_empty_both.pdf",
                "p_5_h_4_f_4_empty_both.word.json",
                "p_5_h_4_f_4_empty_both.word.xml",
            ],
        ),
        # input_output21
        (
            "p_5_h_4_f_4_empty_center",
            "pdf",
            [
                "p_5_h_4_f_4_empty_center.line.json",
                "p_5_h_4_f_4_empty_center.line.xml",
                "p_5_h_4_f_4_empty_center.line_token.json",
                "p_5_h_4_f_4_empty_center.page.json",
                "p_5_h_4_f_4_empty_center.page.xml",
                "p_5_h_4_f_4_empty_center.pdf",
                "p_5_h_4_f_4_empty_center.word.json",
                "p_5_h_4_f_4_empty_center.word.xml",
            ],
        ),
        # input_output22
        (
            "p_5_h_X_f_X",
            "pdf",
            [
                "p_5_h_X_f_X.line.json",
                "p_5_h_X_f_X.line.xml",
                "p_5_h_X_f_X.line_token.json",
                "p_5_h_X_f_X.page.json",
                "p_5_h_X_f_X.page.xml",
                "p_5_h_X_f_X.pdf",
                "p_5_h_X_f_X.word.json",
                "p_5_h_X_f_X.word.xml",
            ],
        ),
    ],
)
def test(input_output: tuple[str, str, list[str]], fxtr_setup_empty_inbox):
    """Test Cases Line Type Headers & Footers."""
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
