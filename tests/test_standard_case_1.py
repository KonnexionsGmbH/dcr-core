# pylint: disable=unused-argument
"""Testing Standard Cases."""
import pytest

import dcr_core.cls_process

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Case 1.
# -----------------------------------------------------------------------------
def test(fxtr_setup_empty_inbox):
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
        instance.document(full_name)

    assert e.type == RuntimeError, f"Wrong PDF format - file={full_name}"
    assert str(e.value)[0:6] == "01.903", f"Wrong PDF format - file={full_name}"
