# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module stub file."""
from __future__ import annotations

import collections.abc

import dcr_core.cls_nlp_core as nlp_core

class TextParser:
    def __init__(self) -> None:
        self._directory_name: str = ""
        self._document_id: int = 0
        self._environment_variant: str = ""
        self._file_name_curr: str = ""
        self._file_name_orig: str = ""
        self._full_name: str = ""
        self._is_lt_footer_required = False
        self._is_lt_header_required = False
        self._is_lt_heading_required = False
        self._is_lt_list_bullet_required = False
        self._is_lt_list_number_required = False
        self._is_lt_table_required = False
        self._is_lt_toc_required = False
        self._no_pdf_pages: int = 0
        self._parse_result_container_fonts: list[nlp_core.FontJSON] = []
        self._parse_result_container_lines: list[nlp_core.LineJSON] = []
        self._parse_result_container_pages: list[nlp_core.PageJSON] = []
        self._parse_result_container_paras: list[nlp_core.ParaJSON] = []
        self._parse_result_container_words: list[nlp_core.WordJSON] = []
        self._parse_result_container_words_line: list[str] = []
        self._parse_result_container_words_para: list[str] = []
        self._parse_result_font = ""
        self._parse_result_glyph_is_empty: bool = False
        self._parse_result_index_page: int = 0
        self._parse_result_llx: float = 0.0
        self._parse_result_no_fonts: int = 0
        self._parse_result_no_lines: int = 0
        self._parse_result_no_lines_in_page: int = 0
        self._parse_result_no_lines_in_para: int = 0
        self._parse_result_no_paras: int = 0
        self._parse_result_no_paras_in_page: int = 0
        self._parse_result_no_titles: int = 0
        self._parse_result_no_words: int = 0
        self._parse_result_no_words_in_line: int = 0
        self._parse_result_no_words_in_page: int = 0
        self._parse_result_no_words_in_para: int = 0
        self._parse_result_size = 0.00
        self._parse_result_table: bool = False
        self._parse_result_table_cell: int = 0
        self._parse_result_table_cell_is_empty: bool = False
        self._parse_result_table_col_span: int = 0
        self._parse_result_table_col_span_prev: int = 0
        self._parse_result_table_row: int = 0
        self._parse_result_text: str = ""
        self._parse_result_urx: float = 0.0
        self.no_errors: int = 0
        self.parse_result_no_pages = 0
        self.parse_result_titles: list[str] = []
        self._exist = True
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
    def _parse_tag_font(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def _parse_tag_fonts(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def _parse_tag_glyph(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def _parse_tag_line(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def _parse_tag_page(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def _parse_tag_pages(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def _parse_tag_para(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def _parse_tag_resources(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def _parse_tag_row(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def _parse_tag_table(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def _parse_tag_text(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def _parse_tag_title(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def _parse_tag_word(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None: ...
    def exists(self) -> bool: ...
    @classmethod
    def from_file(
        cls,
        file_encoding: str,
        full_name: str,
    ) -> None: ...
    def parse_tag_document(
        self,
        directory_name: str,
        document_id: int,
        environment_variant: str,
        file_name_curr: str,
        file_name_next: str,
        file_name_orig: str,
        is_lt_footer_required: bool,
        is_lt_header_required: bool,
        is_lt_heading_required: bool,
        is_lt_list_bullet_required: bool,
        is_lt_list_number_required: bool,
        is_lt_table_required: bool,
        is_lt_toc_required: bool,
        no_pdf_pages: int,
        parent: collections.abc.Iterable[str],
        parent_tag: str,
    ) -> None: ...
