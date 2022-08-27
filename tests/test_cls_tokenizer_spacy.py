"""Testing Class TokenizerSpacy."""
import dcr_core
import dcr_core.cls_tokenizer_spacy

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
    instance_e = dcr_core.cls_tokenizer_spacy.TokenizerSpacy()

    instance_e.exists()
