# pylint: disable=unused-argument
"""Testing Class LineTypeTable."""
import pytest

import dcr_core
import dcr_core.cls_line_type_header_footer
import dcr_core.cls_line_type_toc
import dcr_core.cls_process
import dcr_core.cls_text_parser

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Cases Line Type Table - Coverage.
# -----------------------------------------------------------------------------
@pytest.mark.issue
def test(fxtr_rmdir_opt, fxtr_setup_empty_inbox):
    """Test Cases Line Type Table - Coverage."""
    # -------------------------------------------------------------------------
    try:
        del dcr_core.core_glob.text_parser
    except (AttributeError, NameError):
        pass

    with pytest.raises(SystemExit) as expt:
        dcr_core.cls_line_type_table.LineTypeTable()

    assert expt.type == SystemExit, "Instance of TextParser is missing"
    assert expt.value.code == 1, "Instance of TextParser is missing"

    dcr_core.core_glob.text_parser = dcr_core.cls_text_parser.TextParser()

    # -------------------------------------------------------------------------
    try:
        del dcr_core.core_glob.line_type_header_footer
    except (AttributeError, NameError):
        pass

    with pytest.raises(SystemExit) as expt:
        dcr_core.cls_line_type_table.LineTypeTable()

    assert expt.type == SystemExit, "Instance of LineTypeHeaderFooter is missing"
    assert expt.value.code == 1, "Instance of LineTypeHeaderFooter is missing"

    dcr_core.core_glob.line_type_header_footer = dcr_core.cls_line_type_header_footer.LineTypeHeaderFooter()

    # -------------------------------------------------------------------------
    try:
        del dcr_core.core_glob.line_type_toc
    except (AttributeError, NameError):
        pass

    with pytest.raises(SystemExit) as expt:
        dcr_core.cls_line_type_table.LineTypeTable()

    assert expt.type == SystemExit, "Instance of LineTypeToc is missing"
    assert expt.value.code == 1, "Instance of LineTypeToc is missing"

    dcr_core.core_glob.line_type_toc = dcr_core.cls_line_type_toc.LineTypeToc()

    # -------------------------------------------------------------------------
    instance = dcr_core.cls_line_type_table.LineTypeTable()

    instance.exists()
