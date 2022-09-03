# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module stub file."""
from __future__ import annotations

import collections.abc

import dcr_core.cls_nlp_core

class TextParser:
    def __init__(self) -> None:
        self.parse_result_line_lines = None
        self._directory_name: str = ""
        self._document_id: int = 0
        self._environment_variant: str = ""
        self._exist: bool = False
        self._file_name_curr: str = ""
        self._file_name_orig: str = ""
        self._full_name: str = ""
        self._no_pdf_pages: int = 0
        self._parse_result_line_index_page: int = 0
        self._parse_result_line_index_para: int = 0
        self._parse_result_line_llx: float = 0.0
        self._parse_result_line_urx: float = 0.0
        self._parse_result_no_lines_in_doc: int = 0
        self._parse_result_no_lines_in_page: int = 0
        self._parse_result_no_lines_in_para: int = 0
        self._parse_result_no_paras_in_doc: int = 0
        self._parse_result_no_paras_in_page: int = 0
        self._parse_result_no_words_in_doc: int = 0
        self._parse_result_no_words_in_line: int = 0
        self._parse_result_no_words_in_page: int = 0
        self._parse_result_no_words_in_para: int = 0
        self._parse_result_page_pages: dcr_core.cls_nlp_core.NLPCore.ParserPagePages = []
        self._parse_result_page_paras: dcr_core.cls_nlp_core.NLPCore.ParserPageParas = []
        self._parse_result_table: bool = False
        self._parse_result_table_cell: int = 0
        self._parse_result_table_cell_is_empty: bool = False
        self._parse_result_table_col_span: int = 0
        self._parse_result_table_col_span_prev: int = 0
        self._parse_result_table_row: int = 0
        self._parse_result_text: str = ""
        self._parse_result_word_lines: dcr_core.cls_nlp_core.NLPCore.ParserWordLines = []
        self._parse_result_word_pages: dcr_core.cls_nlp_core.NLPCore.ParserWordPages = []
        self._parse_result_word_paras: dcr_core.cls_nlp_core.NLPCore.ParserWordParas = []
        self._parse_result_word_words: dcr_core.cls_nlp_core.NLPCore.ParserWordWords = []
        self.parse_result_line_document: dcr_core.cls_nlp_core.NLPCore.ParserLineDocument = {}
        self.parse_result_line_line: dcr_core.cls_nlp_core.NLPCore.ParserLineLine = {}
        self.parse_result_line_page: dcr_core.cls_nlp_core.NLPCore.ParserLinePage = {}
        self.parse_result_line_pages: dcr_core.cls_nlp_core.NLPCore.ParserLinePages = []
        self.parse_result_no_pages_in_doc: int = 0
        self.parse_result_titles: list[str] = []
    def _create_line_document(self) -> None: ...
    def _create_line_lines(self) -> None: ...
    def _create_line_pages(self) -> None: ...
    def _create_page_document(self) -> None: ...
    def _create_page_pages(self) -> None: ...
    def _create_page_paras(self) -> None: ...
    def _create_word_document(self) -> None: ...
    def _create_word_lines(self) -> None: ...
    def _create_word_pages(self) -> None: ...
    def _create_word_paras(self) -> None: ...
    def _create_word_words(self) -> None: ...
    @staticmethod
    def _debug_xml_element_all(event: str, parent_tag: str, attrib: dict[str, str], text: collections.abc.Iterable[str | None]) -> None: ...
    def _debug_xml_element_text_line(self) -> None: ...
    def _debug_xml_element_text_page(self) -> None: ...
    def _debug_xml_element_text_word(self) -> None: ...
    def _parse_tag_bookmark(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def _parse_tag_bookmarks(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def _parse_tag_box(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def _parse_tag_cell(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def _parse_tag_content(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def _parse_tag_doc_info(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def _parse_tag_line(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def _parse_tag_page(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def _parse_tag_pages(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def _parse_tag_para(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def _parse_tag_row(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def _parse_tag_table(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def _parse_tag_text(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def _parse_tag_title(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def _parse_tag_word(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def exists(self) -> bool: ...
    @classmethod
    def from_files(cls, file_encoding: str, full_name_line: str = "", full_name_page: str = "", full_name_word: str = "") -> TextParser: ...
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