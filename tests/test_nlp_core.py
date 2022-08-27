# pylint: disable=unused-argument
"""Testing Class NLPCore."""
import pytest

import dcr_core
import dcr_core.cls_process

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Cases NNLPCore - Coverage.
# -----------------------------------------------------------------------------
def test_nlp_core_coverage(fxtr_rmdir_opt, fxtr_setup_empty_inbox):
    """Test Cases NLPCore - Coverage."""
    # -------------------------------------------------------------------------
    instance_e = dcr_core.cls_nlp_core.NLPCore()

    instance_e.exists()
