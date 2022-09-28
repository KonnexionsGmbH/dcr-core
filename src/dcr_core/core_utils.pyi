# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module stub file."""
import pathlib

import dcr_core.cls_nlp_core as nlp_core

ERROR_00_901: str = ...
ERROR_00_902: str = ...
ERROR_01_901: str = ...
ERROR_01_903: str = ...
ERROR_21_901: str = ...
ERROR_31_902: str = ...
ERROR_31_903: str = ...
ERROR_31_911: str = ...
ERROR_41_901: str = ...
ERROR_41_911: str = ...
ERROR_51_901: str = ...
ERROR_61_901: str = ...
ERROR_61_902: str = ...
ERROR_61_903: str = ...
ERROR_61_904: str = ...
ERROR_61_905: str = ...
ERROR_61_906: str = ...
ERROR_61_907: str = ...
ERROR_61_908: str = ...
ERROR_71_907: str = ...

def check_exists_object(
    is_line_type_header_footer: bool = ...,
    is_line_type_heading: bool = ...,
    is_line_type_list_bullet: bool = ...,
    is_line_type_list_number: bool = ...,
    is_line_type_table: bool = ...,
    is_line_type_toc: bool = ...,
    is_nlp_core: bool = ...,
    is_setup: bool = ...,
    is_text_parser: bool = ...,
) -> None: ...
def create_config() -> nlp_core.NLPCore.ConfigJSON: ...
def get_components_from_full_name(
    full_name: str,
) -> tuple[str, str, str]: ...
def get_full_name_from_components(directory_name: pathlib.Path | str, stem_name: str = ..., file_extension: str = ...) -> str: ...
def get_os_independent_name(name: pathlib.Path | str | None) -> str: ...
def get_stem_name(file_name: pathlib.Path | str | None) -> str: ...
def progress_msg(is_verbose: bool, msg: str) -> None: ...
def progress_msg_core(msg: str) -> None: ...
def terminate_fatal(error_msg: str) -> None: ...
