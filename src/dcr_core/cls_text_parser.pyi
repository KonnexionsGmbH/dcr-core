# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module stub file."""
from __future__ import annotations

import collections.abc

import dcr_core.cls_nlp_core as nlp_core

class TextParser:
    def __init__(self) -> None:
        self._directory_name = ""
        self._document_id = 0
        self._environment_variant = ""
        self._file_name_curr = ""
        self._file_name_orig = ""
        self._full_name = ""
        self._is_lt_footer_required = False
        self._is_lt_header_required = False
        self._is_lt_heading_required = False
        self._is_lt_list_bullet_required = False
        self._is_lt_list_number_required = False
        self._is_lt_table_required = False
        self._is_lt_toc_required = False
        self._no_pdf_pages = 0
        self._parse_result_container_fonts: list[nlp_core.NLPCore.FontJSON] = []
        self._parse_result_container_lines: list[nlp_core.NLPCore.LineJSON] = []
        self._parse_result_container_pages: list[nlp_core.NLPCore.PageJSON] = []
        self._parse_result_container_paras: list[nlp_core.NLPCore.ParaJSON] = []
        self._parse_result_container_words: list[nlp_core.NLPCore.WordJSON] = []
        self._parse_result_line_word_no_first = 0
        self._parse_result_line_word_no_last = 0
        self._parse_result_no_fonts = 0
        self._parse_result_no_lines = 0
        self._parse_result_no_lines_page = 0
        self._parse_result_no_lines_para = 0
        self._parse_result_no_pages = 0
        self._parse_result_no_paras = 0
        self._parse_result_no_paras_page = 0
        self._parse_result_no_words = 0
        self._parse_result_no_words_line = 0
        self._parse_result_no_words_para = 0
        self._parse_result_no_words_page = 0
        self._parse_result_page_line_no_first = 0
        self._parse_result_page_line_no_last = 0
        self._parse_result_page_para_no_first = 0
        self._parse_result_page_para_no_last = 0
        self._parse_result_page_word_no_first = 0
        self._parse_result_page_word_no_last = 0
        self._parse_result_para_line_no_first = 0
        self._parse_result_para_line_no_last = 0
        self._parse_result_para_word_no_first = 0
        self._parse_result_para_word_no_last = 0
        self._parse_result_container_words_line: list[str] = []
        self._parse_result_container_words_para: list[str] = []
        self._parse_result_font = ""
        self._parse_result_glyph_is_empty = False
        self._parse_result_index_page = 0
        self._parse_result_llx: float = 0.0
        self._parse_result_no_titles = 0
        self._parse_result_size = 0.00
        self._parse_result_table = False
        self._parse_result_table_cell = 0
        self._parse_result_table_cell_is_empty = False
        self._parse_result_table_col_span = 0
        self._parse_result_table_col_span_prev = 0
        self._parse_result_table_row = 0
        self._parse_result_text = ""
        self._parse_result_urx = 0.0
        self.no_errors = 0
        self.parse_result_no_pages = 0
        self.parse_result_titles: list[str] = []
        self._exist = False
    @staticmethod
    def _create_config() -> nlp_core.NLPCore.ConfigJSON: ...
    def _create_params(self) -> nlp_core.NLPCore.ParamsJSON: ...
    @staticmethod
    def _debug_xml_element_all(event: str, parent_tag: str, attrib: dict[str, str], text: collections.abc.Iterable[str | None]) -> None: ...
    def _debug_xml_element_text(self) -> None: ...
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
