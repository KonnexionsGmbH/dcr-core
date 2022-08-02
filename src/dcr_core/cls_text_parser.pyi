from __future__ import annotations

import collections.abc
from typing import List

import cls_nlp_core

class TextParser:
    parse_result_line_lines: cls_nlp_core.NLPCore.ParserLineLines
    parse_result_line_pages: cls_nlp_core.NLPCore.ParserLinePages
    parse_result_no_pages_in_doc: int
    parse_result_titles: List[str]

    def __init__(self) -> None: ...
    def exists(self) -> bool: ...
    @classmethod
    def from_files(
        cls, file_encoding: str, full_name_line: str = ..., full_name_page: str = ..., full_name_word: str = ...
    ) -> TextParser: ...
    def parse_tag_document(
        self,
        directory_name: str,
        document_id: int,
        environment_variant: str,
        file_name_curr: str,
        file_name_next: str,
        file_name_orig: str,
        no_pdf_pages: int,
        parent: collections.abc.Iterable[str],
        parent_tag: str,
    ) -> None: ...
