# pylint: disable=unused-argument
"""Testing Standard Cases."""
import pytest

import dcr_core.cls_process

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
                "case_2_docx_route_inbox_pandoc_pdflib.line.json",
                "case_2_docx_route_inbox_pandoc_pdflib.line.xml",
                "case_2_docx_route_inbox_pandoc_pdflib.line_token.json",
                "case_2_docx_route_inbox_pandoc_pdflib.page.json",
                "case_2_docx_route_inbox_pandoc_pdflib.page.xml",
                "case_2_docx_route_inbox_pandoc_pdflib.pdf",
                "case_2_docx_route_inbox_pandoc_pdflib.word.json",
                "case_2_docx_route_inbox_pandoc_pdflib.word.xml",
            ],
        ),
        # input_output1
        (
            "case_3_pdf_text_route_inbox_pdflib",
            "pdf",
            [
                "case_3_pdf_text_route_inbox_pdflib.line.json",
                "case_3_pdf_text_route_inbox_pdflib.line.xml",
                "case_3_pdf_text_route_inbox_pdflib.line_list_number.json",
                "case_3_pdf_text_route_inbox_pdflib.line_token.json",
                "case_3_pdf_text_route_inbox_pdflib.page.json",
                "case_3_pdf_text_route_inbox_pdflib.page.xml",
                "case_3_pdf_text_route_inbox_pdflib.pdf",
                "case_3_pdf_text_route_inbox_pdflib.word.json",
                "case_3_pdf_text_route_inbox_pdflib.word.xml",
            ],
        ),
        # input_output2
        (
            "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib",
            "pdf",
            [
                "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib.pdf",
                "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_0.line.json",
                "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_0.line.xml",
                "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_0.line_table.json",
                "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_0.line_token.json",
                "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_0.page.json",
                "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_0.page.xml",
                "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_0.pdf",
                "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_0.word.json",
                "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_0.word.xml",
                "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_1.jpeg",
            ],
        ),
        # input_output3
        (
            "case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib",
            "pdf",
            [
                "case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib.pdf",
                "case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_0.line.json",
                "case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_0.line.xml",
                "case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_0.line_heading.json",
                "case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_0.line_list_bullet.json",
                "case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_0.line_list_number.json",
                "case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_0.line_token.json",
                "case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_0.page.json",
                "case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_0.page.xml",
                "case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_0.pdf",
                "case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_0.word.json",
                "case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_0.word.xml",
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
                "case_6_jpg_route_inbox_tesseract_pdflib.line.json",
                "case_6_jpg_route_inbox_tesseract_pdflib.line.xml",
                "case_6_jpg_route_inbox_tesseract_pdflib.line_token.json",
                "case_6_jpg_route_inbox_tesseract_pdflib.page.json",
                "case_6_jpg_route_inbox_tesseract_pdflib.page.xml",
                "case_6_jpg_route_inbox_tesseract_pdflib.pdf",
                "case_6_jpg_route_inbox_tesseract_pdflib.word.json",
                "case_6_jpg_route_inbox_tesseract_pdflib.word.xml",
            ],
        ),
    ],
)
def test(input_output: tuple[str, str, list[str]], fxtr_setup_empty_inbox):
    """Test Cases 2, 3, 4, 5, and 6."""
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
