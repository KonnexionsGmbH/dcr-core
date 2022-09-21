# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module stub file."""
from __future__ import annotations

import dcr_core.cls_nlp_core as nlp_core

class LineTypeHeaderFooter:
    CandLinesPage = list[tuple[int, str]]
    CandLinesPages = list[CandLinesPage]
    ResultDoc = list[tuple[bool, str, int]]
    ResultPages = list[list[bool]]
    VARIANT_FOOTER: str
    VARIANT_HEADER: str

    def __init__(
        self,
        file_name_curr: str = "",
    ) -> None:
        self._cand_lines_footer_pages: LineTypeHeaderFooter.CandLinesPages = []
        self._cand_lines_footer_template: LineTypeHeaderFooter.CandLinesPage = []
        self._cand_lines_header_pages: LineTypeHeaderFooter.CandLinesPages = []
        self._cand_lines_header_template: LineTypeHeaderFooter.CandLinesPage = []
        self._file_name_curr = file_name_curr
        self._is_complete_footer = False
        self._is_complete_header = False
        self._is_required_footer = False
        self._is_required_header = False
        self._is_result_footer = False
        self._is_result_header = False
        self._lines_json: list[nlp_core.NLPCore.LineJSON] = []
        self._line_no_page = 0
        self._no_pages = 0
        self._result_doc_footer: LineTypeHeaderFooter.ResultDoc = []
        self._result_doc_header: LineTypeHeaderFooter.ResultDoc = []
        self._result_pages_footer: LineTypeHeaderFooter.ResultPages = []
        self._result_pages_header: LineTypeHeaderFooter.ResultPages = []
        self.no_lines_footer = 0
        self.no_lines_header = 0
        self._exist = True
    def _apply_patterns(self) -> None: ...
    def _create_cand_from_page(self) -> None: ...
    def _create_cand_from_page_footer(self) -> None: ...
    def _create_cand_from_page_header(self) -> None: ...
    @staticmethod
    def _create_cand_template_page(lt_max_lines: int) -> LineTypeHeaderFooter.CandLinesPage: ...
    @staticmethod
    def _create_result_template(lt_max_lines: int) -> LineTypeHeaderFooter.ResultDoc: ...
    @staticmethod
    def _debug_lt(msg: str) -> None: ...
    def _init_cand(self) -> None: ...
    def _init_result_doc(self) -> None: ...
    def _pattern_levenshtein(
        self,
    ) -> None: ...
    def _pattern_levenshtein_distance(
        self,
        variant: str,
        lt_max_distance: int,
        cand_lines_pages: LineTypeHeaderFooter.CandLinesPages,
        result_doc: LineTypeHeaderFooter.ResultDoc,
        result_pages: LineTypeHeaderFooter.ResultPages,
    ) -> tuple[LineTypeHeaderFooter.ResultDoc, LineTypeHeaderFooter.ResultPages]: ...
    @staticmethod
    def _reset_result_pages(
        result_doc: LineTypeHeaderFooter.ResultDoc,
        result_pages: LineTypeHeaderFooter.ResultPages,
    ) -> LineTypeHeaderFooter.ResultPages: ...
    def _store_results(self) -> None: ...
    def _update_result_doc(
        self,
        result_doc: LineTypeHeaderFooter.ResultDoc,
        result_pages: LineTypeHeaderFooter.ResultPages,
    ) -> LineTypeHeaderFooter.ResultDoc: ...
    def exists(self) -> bool: ...
    def process_document(
        self,
        file_name_curr: str = ...,
    ) -> None: ...
