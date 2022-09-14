"""Testing Class TokenizerSpacy."""
import pytest

import dcr_core.cls_setup as setup
import dcr_core.cls_tokenizer_spacy as tokenizer
from dcr_core import core_glob

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
    try:
        del core_glob.setup
    except (AttributeError, NameError):
        pass

    with pytest.raises(SystemExit) as expt:
        tokenizer.TokenizerSpacy()

    assert expt.type == SystemExit, "Instance of Setup is missing"
    assert expt.value.code == 1, "Instance of Setup is missing"

    core_glob.setup = setup.Setup()

    # -------------------------------------------------------------------------
    instance = tokenizer.TokenizerSpacy()

    instance.exists()
