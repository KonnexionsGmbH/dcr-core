# pylint: disable=unused-argument
"""Testing Class LineTypeHeaderFooter."""
import pytest

import dcr_core.cls_process as process
import dcr_core.cls_setup as setup
import dcr_core.core_glob as glob
import dcr_core.core_utils as utils

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Cases Line Type Headers & Footers - Coverage.
# -----------------------------------------------------------------------------
def test(fxtr_rmdir_opt, fxtr_setup_empty_inbox):
    """Test Cases Line Type Headers & Footers - Coverage."""
    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        setup.Setup._DCR_CFG_SECTION_CORE_ENV_TEST,
        [
            (setup.Setup._DCR_CFG_LT_FOOTER_MAX_LINES, "0"),
            (setup.Setup._DCR_CFG_LT_HEADER_MAX_LINES, "0"),
            (setup.Setup._DCR_CFG_VERBOSE_LT_HEADER_FOOTER, "true"),
        ],
    )

    # -------------------------------------------------------------------------
    directory_name = glob.setup.directory_inbox
    stem_name = "p_5_h_4_f_4_empty_center"
    file_extension = "pdf"

    full_name = utils.get_full_name_from_components(directory_name, stem_name, file_extension)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            (stem_name, file_extension),
        ],
        target_path=directory_name,
    )

    # -------------------------------------------------------------------------
    instance = process.Process()

    instance.document(full_name, is_delete_auxiliary_files=False)
