# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module stub file."""
import collections

class NLPCore:
    EntryJSON = dict[str, int | str]
    FontJSON = dict[str, bool | float | int | str]
    WordJSON = dict[str, bool | float | int | str]
    LineJSON = dict[str, float | int | list[WordJSON] | str]
    ListJSON = dict[str, list[EntryJSON]]
    ParaJSON = dict[str, int | list[LineJSON] | str]
    PageJSON = dict[str, int | list[ParaJSON]]
    ConfigJSON = dict[str, bool | str]
    DocumentJSON = dict[str, bool | int | list[PageJSON] | str]
    ParamsJSON = dict[str, bool | int | str]

    def __init__(self) -> None:
        self.document_json: dict[str, bool | int | list[NLPCore.PageJSON] | str] = {}
    def exists(self) -> bool: ...
    @staticmethod
    def export_rule_file_heading(
        is_verbose: bool, file_name: str, file_encoding: str, json_indent: str, is_json_sort_keys: bool
    ) -> None: ...
    @staticmethod
    def export_rule_file_list_bullet(
        is_verbose: bool,
        file_name: str,
        file_encoding: str,
        json_indent: str,
        is_json_sort_keys: bool,
        environment_variant: str,
    ) -> None: ...
    @staticmethod
    def export_rule_file_list_number(
        is_verbose: bool,
        file_name: str,
        file_encoding: str,
        json_indent: str,
        is_json_sort_keys: bool,
        environment_variant: str,
    ) -> None: ...
    @staticmethod
    def get_lt_anti_patterns_default_heading() -> list[
        tuple[
            str,
            str,
        ]
    ]: ...
    @staticmethod
    def get_lt_anti_patterns_default_list_bullet(
        environment_variant: str,
    ) -> list[tuple[str, str]]: ...
    @staticmethod
    def get_lt_anti_patterns_default_list_number(environment_variant: str) -> list[tuple[str, str]]: ...
    @staticmethod
    def get_lt_rules_default_heading() -> list[tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str]]]: ...
    @staticmethod
    def get_lt_rules_default_list_bullet() -> dict[str, int]: ...
    @staticmethod
    def get_lt_rules_default_list_number() -> list[tuple[str, str, collections.abc.Callable[[str, str], bool], list[str]]]: ...
    @classmethod
    def is_asc_ignore(cls, _predecessor: str, _successor: str) -> bool: ...
    @classmethod
    def is_asc_lowercase_letters(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_lowercase_letters_token(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_romans(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_romans_token(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_strings(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_string_floats(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_string_floats_token(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_string_integers(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_string_integers_token(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_uppercase_letters(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_uppercase_letters_token(cls, predecessor: str, successor: str) -> bool: ...
