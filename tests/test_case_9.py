# pylint: disable=unused-argument
"""Testing Cases."""
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
        instance.file_process(full_name)

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

    instance.file_process(full_name)


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

    instance.file_process(full_name)


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

    instance.file_process(full_name)


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

    instance.file_process(full_name)


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

    instance.file_process(full_name)


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
        instance.file_process(full_name)

    assert e.type == RuntimeError, f"Unknown file extension - file={full_name}"
    assert str(e.value)[0:6] == "01.901", f"Unknown file extension - file={full_name}"
