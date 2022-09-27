# pylint: disable=unused-argument
"""Testing Class LineTypeListNumber."""
import pytest

import dcr_core.cls_line_type_header_footer as lt_hf
import dcr_core.cls_line_type_list_bullet as lt_lb
import dcr_core.cls_line_type_list_number as lt_ln
import dcr_core.cls_line_type_toc as lt_toc
import dcr_core.cls_text_parser as parser
from dcr_core import core_glob

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Cases Line Type ListNumber - Coverage.
# -----------------------------------------------------------------------------
def test(fxtr_rmdir_opt, fxtr_setup_empty_inbox):  # noqa: C901
    """Test Cases Line Type ListNumber - Coverage."""
    # -------------------------------------------------------------------------
    try:
        del core_glob.text_parser
    except (AttributeError, NameError):
        pass

    with pytest.raises(SystemExit) as expt:
        lt_ln.LineTypeListNumber()

    assert expt.type == SystemExit, "Instance of TextParser is missing"
    assert expt.value.code == 1, "Instance of TextParser is missing"

    core_glob.text_parser = parser.TextParser()

    # -------------------------------------------------------------------------
    try:
        del core_glob.inst_lt_hf
    except (AttributeError, NameError):
        pass

    with pytest.raises(SystemExit) as expt:
        lt_ln.LineTypeListNumber()

    assert expt.type == SystemExit, "Instance of LineTypeHeaderFooter is missing"
    assert expt.value.code == 1, "Instance of LineTypeHeaderFooter is missing"

    core_glob.inst_lt_hf = lt_hf.LineTypeHeaderFooter()

    # -------------------------------------------------------------------------
    try:
        del core_glob.inst_lt_toc
    except (AttributeError, NameError):
        pass

    with pytest.raises(SystemExit) as expt:
        lt_ln.LineTypeListNumber()

    assert expt.type == SystemExit, "Instance of LineTypeToc is missing"
    assert expt.value.code == 1, "Instance of LineTypeToc is missing"

    core_glob.inst_lt_toc = lt_toc.LineTypeToc()

    # -------------------------------------------------------------------------
    try:
        del core_glob.line_type_list_bullet
    except (AttributeError, NameError):
        pass

    with pytest.raises(SystemExit) as expt:
        lt_ln.LineTypeListNumber()

    assert expt.type == SystemExit, "Instance of LineTypeListBullet is missing"
    assert expt.value.code == 1, "Instance of LineTypeListBullet is missing"

    core_glob.line_type_list_bullet = lt_lb.LineTypeListBullet()

    # -------------------------------------------------------------------------
    instance = lt_ln.LineTypeListNumber()

    instance.exists()