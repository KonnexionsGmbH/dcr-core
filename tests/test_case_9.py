# pylint: disable=unused-argument
"""Testing Cases."""
import os

import pytest

import dcr_core
import dcr_core.cls_process

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Case 1.
# -----------------------------------------------------------------------------
def test_case_1(fxtr_setup_empty_inbox):
    """Test Case 1."""
    # -------------------------------------------------------------------------
    directory_name = dcr_core.core_glob.setup.directory_inbox
    stem_name = "case_1_pdf_wrong_route_inbox"
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

    with pytest.raises(RuntimeError) as e:
        instance.document_process(full_name)

    assert e.type == RuntimeError, f"Wrong PDF format - file={full_name}"
    assert str(e.value)[0:6] == "01.903", f"Wrong PDF format - file={full_name}"


# -----------------------------------------------------------------------------
# Test Case 2.
# -----------------------------------------------------------------------------
def test_case_2(fxtr_setup_empty_inbox):
    """Test Case 2."""
    # -------------------------------------------------------------------------
    directory_name = dcr_core.core_glob.setup.directory_inbox
    stem_name = "case_2_docx_route_inbox_pandoc_pdflib"
    file_extension = "docx"

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
    pytest.helpers.verify_content_of_directory(
        directory_name,
        [],
        [
            os.path.basename(full_name),
            stem_name + ".line.json",
            stem_name + ".line.xml",
            stem_name + ".line_token.json",
            stem_name + ".page.json",
            stem_name + ".page.xml",
            stem_name + "." + dcr_core.core_glob.FILE_TYPE_PDF,
            stem_name + ".word.json",
            stem_name + ".word.xml",
        ],
    )


# -----------------------------------------------------------------------------
# Test Case 3.
# -----------------------------------------------------------------------------
def test_case_3(fxtr_setup_empty_inbox):
    """Test Case 3."""
    # -------------------------------------------------------------------------
    directory_name = dcr_core.core_glob.setup.directory_inbox
    stem_name = "case_3_pdf_text_route_inbox_pdflib"
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
    pytest.helpers.verify_content_of_directory(
        directory_name,
        [],
        [
            os.path.basename(full_name),
            stem_name + ".line.json",
            stem_name + ".line.xml",
            stem_name + ".line_list_number.json",
            stem_name + ".line_token.json",
            stem_name + ".page.json",
            stem_name + ".page.xml",
            stem_name + "." + dcr_core.core_glob.FILE_TYPE_PDF,
            stem_name + ".word.json",
            stem_name + ".word.xml",
        ],
    )


# -----------------------------------------------------------------------------
# Test Case 4.
# -----------------------------------------------------------------------------
def test_case_4(fxtr_setup_empty_inbox):
    """Test Case 4."""
    # -------------------------------------------------------------------------
    directory_name = dcr_core.core_glob.setup.directory_inbox
    stem_name = "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib"
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
    pytest.helpers.verify_content_of_directory(
        directory_name,
        [],
        [
            os.path.basename(full_name),
            stem_name + "_0.line.json",
            stem_name + "_0.line.xml",
            stem_name + "_0.line_table.json",
            stem_name + "_0.line_token.json",
            stem_name + "_0.page.json",
            stem_name + "_0.page.xml",
            stem_name + "_0." + dcr_core.core_glob.FILE_TYPE_PDF,
            stem_name + "_0.word.json",
            stem_name + "_0.word.xml",
            stem_name + "_1." + dcr_core.core_glob.FILE_TYPE_JPEG,
        ],
    )


# -----------------------------------------------------------------------------
# Test Case 5.
# -----------------------------------------------------------------------------
def test_case_5(fxtr_setup_empty_inbox):
    """Test Case 5."""
    # -------------------------------------------------------------------------
    directory_name = dcr_core.core_glob.setup.directory_inbox
    stem_name = "case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib"
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
    pytest.helpers.verify_content_of_directory(
        directory_name,
        [],
        [
            os.path.basename(full_name),
            stem_name + "_0.line.json",
            stem_name + "_0.line.xml",
            stem_name + "_0.line_heading.json",
            stem_name + "_0.line_list_bullet.json",
            stem_name + "_0.line_list_number.json",
            stem_name + "_0.line_token.json",
            stem_name + "_0.page.json",
            stem_name + "_0.page.xml",
            stem_name + "_0." + dcr_core.core_glob.FILE_TYPE_PDF,
            stem_name + "_0.word.json",
            stem_name + "_0.word.xml",
            stem_name + "_1." + dcr_core.core_glob.FILE_TYPE_JPEG,
            stem_name + "_2." + dcr_core.core_glob.FILE_TYPE_JPEG,
        ],
    )


# -----------------------------------------------------------------------------
# Test Case 6.
# -----------------------------------------------------------------------------
def test_case_6(fxtr_setup_empty_inbox):
    """Test Case 6."""
    # -------------------------------------------------------------------------
    directory_name = dcr_core.core_glob.setup.directory_inbox
    stem_name = "case_6_jpg_route_inbox_tesseract_pdflib"
    file_extension = "jpg"

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
    pytest.helpers.verify_content_of_directory(
        directory_name,
        [],
        [
            os.path.basename(full_name),
            stem_name + ".line.json",
            stem_name + ".line.xml",
            stem_name + ".line_token.json",
            stem_name + ".page.json",
            stem_name + ".page.xml",
            stem_name + "." + dcr_core.core_glob.FILE_TYPE_PDF,
            stem_name + ".word.json",
            stem_name + ".word.xml",
        ],
    )


# -----------------------------------------------------------------------------
# Test Case 7.
# -----------------------------------------------------------------------------
def test_case_7(fxtr_setup_empty_inbox):
    """Test Case 7."""
    # -------------------------------------------------------------------------
    directory_name = dcr_core.core_glob.setup.directory_inbox
    stem_name = "case_7_cfg_wrong_extension"
    file_extension = "cfg"

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

    with pytest.raises(RuntimeError) as e:
        instance.document_process(full_name)

    assert e.type == RuntimeError, f"Unknown file extension - file={full_name}"
    assert str(e.value)[0:6] == "01.901", f"Unknown file extension - file={full_name}"
