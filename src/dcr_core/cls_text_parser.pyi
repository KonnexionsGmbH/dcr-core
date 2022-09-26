# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module stub file."""
import collections.abc

class TextParser:
    def __init__(self) -> None:
        self.no_errors: int = ...
    def exists(self) -> bool: ...
    @classmethod
    def from_file(
        cls,
        file_encoding: str,
        full_name: str,
    ) -> None: ...
    def parse_tag_document_line(
        self,
        parent: collections.abc.Iterable[str],
        parent_tag: str,
    ) -> None: ...
    def parse_tag_document_word(
        self,
        directory_name: str,
        document_id: int,
        environment_variant: str,
        file_name_curr: str,
        file_name_next: str,
        file_name_orig: str,
        is_lt_heading_required: bool,
        is_lt_list_bullet_required: bool,
        is_lt_list_number_required: bool,
        is_lt_toc_required: bool,
        no_pdf_pages: int,
        parent: collections.abc.Iterable[str],
        parent_tag: str,
    ) -> None: ...
