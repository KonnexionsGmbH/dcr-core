# pylint: disable=unused-argument
"""Testing Class NLPCore."""
import dcr_core

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Cases NLPCore - Coverage.
# -----------------------------------------------------------------------------
def test_nlp_core_coverage():
    """Test Cases NLPCore - Coverage."""
    # -------------------------------------------------------------------------
    instance_e = dcr_core.cls_nlp_core.NLPCore()

    instance_e.exists()
