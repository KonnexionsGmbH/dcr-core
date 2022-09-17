# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module stub file."""
import pathlib

import dcr_core.cls_nlp_core as nlp_core

ERROR_00_901 = ""
ERROR_00_902 = ""
ERROR_01_901 = ""
ERROR_01_903 = ""
ERROR_21_901 = ""
ERROR_31_902 = ""
ERROR_31_903 = ""
ERROR_31_911 = ""
ERROR_41_901 = ""
ERROR_41_911 = ""
ERROR_51_901 = ""
ERROR_61_901 = ""
ERROR_61_902 = ""
ERROR_61_903 = ""
ERROR_61_904 = ""
ERROR_61_905 = ""
ERROR_71_901 = ""

def check_exists_object(
    is_line_type_header_footer: bool = False,
    is_line_type_heading: bool = False,
    is_line_type_list_bullet: bool = False,
    is_line_type_list_number: bool = False,
    is_line_type_table: bool = False,
    is_line_type_toc: bool = False,
    is_nlp_core: bool = False,
    is_setup: bool = False,
    is_text_parser: bool = False,
) -> None: ...
def create_config() -> nlp_core.NLPCore.ConfigJSON: ...
def get_components_from_full_name(
    full_name: str,
) -> tuple[str, str, str]: ...
def get_full_name_from_components(directory_name: pathlib.Path | str, stem_name: str = "", file_extension: str = "") -> str: ...
def get_os_independent_name(name: pathlib.Path | str | None) -> str: ...
def get_stem_name(file_name: pathlib.Path | str | None) -> str: ...
def progress_msg(is_verbose: bool, msg: str) -> None: ...
def progress_msg_core(msg: str) -> None: ...
def terminate_fatal(error_msg: str) -> None: ...
