# pylint: disable=unused-argument
"""Testing Class LineTypeTable."""
import pytest

import dcr_core.cls_process as process
import dcr_core.cls_setup as setup
from dcr_core import core_glob
from dcr_core import core_utils

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Cases Line Type Table - Coverage.
# -----------------------------------------------------------------------------
def test(fxtr_rmdir_opt, fxtr_setup_empty_inbox):
    """Test Cases Line Type Table - Coverage."""
    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        setup.Setup._DCR_CFG_SECTION_CORE_ENV_TEST,
        [
            (setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_TABLE, "false"),
            (setup.Setup._DCR_CFG_VERBOSE_LT_TABLE, "true"),
        ],
    )

    # -------------------------------------------------------------------------
    directory_name = core_glob.setup.directory_inbox
    stem_name = "docx_table"
    file_extension = "pdf"

    full_name = core_utils.get_full_name_from_components(directory_name, stem_name, file_extension)

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
