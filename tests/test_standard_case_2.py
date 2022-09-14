# pylint: disable=unused-argument
"""Testing Standard Cases."""
import pytest

import dcr_core.cls_process as process
from dcr_core import core_glob
from dcr_core import core_utils

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Cases 2, 3, 4, 5, and 6.
# -----------------------------------------------------------------------------
@pytest.mark.parametrize(
    "input_output",
    [
        # input_output0
        (
            "case_2_docx_route_inbox_pandoc_pdflib",
            "docx",
            [
                "case_2_docx_route_inbox_pandoc_pdflib.docx",
                "case_2_docx_route_inbox_pandoc_pdflib.json",
                "case_2_docx_route_inbox_pandoc_pdflib.pdf",
                "case_2_docx_route_inbox_pandoc_pdflib.token.json",
                "case_2_docx_route_inbox_pandoc_pdflib.xml",
            ],
        ),
        # input_output1
        (
            "case_3_pdf_text_route_inbox_pdflib",
            "pdf",
            [
                "case_3_pdf_text_route_inbox_pdflib.json",
                "case_3_pdf_text_route_inbox_pdflib.list_number.json",
                "case_3_pdf_text_route_inbox_pdflib.pdf",
                "case_3_pdf_text_route_inbox_pdflib.token.json",
                "case_3_pdf_text_route_inbox_pdflib.xml",
            ],
        ),
        # input_output2
        (
            "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib",
            "pdf",
            [
                "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib.pdf",
                "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_0.json",
                "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_0.pdf",
                "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_0.table.json",
                "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_0.token.json",
                "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_0.xml",
                "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_1.jpeg",
            ],
        ),
        # input_output3
        (
            "case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib",
            "pdf",
            [
                "case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib.pdf",
                "case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_0.heading.json",
                "case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_0.json",
                "case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_0.list_bullet.json",
                "case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_0.list_number.json",
                "case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_0.pdf",
                "case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_0.token.json",
                "case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_0.xml",
                "case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_1.jpeg",
                "case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_2.jpeg",
            ],
        ),
        # input_output4
        (
            "case_6_jpg_route_inbox_tesseract_pdflib",
            "jpg",
            [
                "case_6_jpg_route_inbox_tesseract_pdflib.jpg",
                "case_6_jpg_route_inbox_tesseract_pdflib.json",
                "case_6_jpg_route_inbox_tesseract_pdflib.pdf",
                "case_6_jpg_route_inbox_tesseract_pdflib.token.json",
                "case_6_jpg_route_inbox_tesseract_pdflib.xml",
            ],
        ),
    ],
)
def test(input_output: tuple[str, str, list[str]], fxtr_setup_empty_inbox):
    """Test Cases 2, 3, 4, 5, and 6."""
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
