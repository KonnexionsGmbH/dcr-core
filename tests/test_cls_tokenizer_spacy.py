"""Testing Class TokenizerSpacy."""
import pytest

import dcr_core
import dcr_core.cls_tokenizer_spacy

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Cases TokenizerSpacy - Coverage.
# -----------------------------------------------------------------------------
def test():
    """Test Cases TokenizerSpacy - Coverage."""
    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr_core.cls_tokenizer_spacy.TokenizerSpacy()

    assert expt.type == SystemExit, "Instance of Setup is missing"
    assert expt.value.code == 1, "Instance of Setup is missing"

    dcr_core.core_glob.setup = dcr_core.cls_setup.Setup()

    # -------------------------------------------------------------------------
    instance = dcr_core.cls_tokenizer_spacy.TokenizerSpacy()

    instance.exists()
