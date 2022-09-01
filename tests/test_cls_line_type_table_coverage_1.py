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
def test(fxtr_rmdir_opt, fxtr_setup_empty_inbox):
    """Test Cases Line Type Table - Coverage."""
    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_CORE_ENV_TEST,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_TABLE, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_VERBOSE_LT_TABLE, "true"),
        ],
    )

    # -------------------------------------------------------------------------
    directory_name = dcr_core.core_glob.setup.directory_inbox
    stem_name = "docx_table"
    file_extension = "pdf"

    full_name = dcr_core.core_utils.get_full_name_from_components(directory_name, stem_name, file_extension)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            (stem_name, file_extension),
        ],
        target_path=directory_name,
    )

    # -------------------------------------------------------------------------
    instance = dcr_core.cls_process.Process()

    instance.document(full_name)
