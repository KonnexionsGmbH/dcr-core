# pylint: disable=unused-argument
"""Testing Class TokenizerSpacy."""
import dcr_core

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Cases TokenizerSpacy - Coverage.
# -----------------------------------------------------------------------------
def test_tokenizer_spacy_coverage():
    """Test Cases TokenizerSpacy - Coverage."""
    # -------------------------------------------------------------------------
    instance_e = dcr_core.cls_nlp_core.TokenizerSpacy()

    instance_e.exists()
