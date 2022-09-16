# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module stub file."""
from __future__ import annotations

import dcr_core.cls_nlp_core as nlp_core

class LineTypeHeaderFooter:
    Candidate = tuple[int, int]
    Candidates = list[Candidate]
    LineDataCell = tuple[int, str]
    LineDataRow = tuple[LineDataCell, LineDataCell]
    LineData = list[LineDataRow]
    LSDDataCell = tuple[int, int, int]
    LSDDataRow = list[LSDDataCell]
    LSDData = list[LSDDataRow]
    ResultKey = tuple[int, int]
    ResultData = dict[ResultKey, str]

    def __init__(
        self,
        file_name_curr: str = "",
    ) -> None:
        self._file_name_curr = ""
        self._irregular_footer_cand: LineTypeHeaderFooter.Candidate = (0, 0)
        self._irregular_footer_cand_fp: LineTypeHeaderFooter.Candidates = []
        self._irregular_footer_cands: LineTypeHeaderFooter.Candidates = []
        self._irregular_header_cand: LineTypeHeaderFooter.Candidate = (0, 0)
        self._irregular_header_cand_fp: LineTypeHeaderFooter.Candidates = []
        self._irregular_header_cands: LineTypeHeaderFooter.Candidates = []
        self._is_irregular_footer = False
        self._is_irregular_header = False
        self._line_data: LineTypeHeaderFooter.LineData = []
        self._line_no_max = 0
        self._lines_json: list[nlp_core.NLPCore.LineJSON] = []
        self._lsd_data: LineTypeHeaderFooter.LSDData = []
        self._no_irregular_footer = 0
        self._no_irregular_header = 0
        self._page_idx = 0
        self._page_no_max = 0
        self._result_data: LineTypeHeaderFooter.ResultData = {}
        self.no_lines_footer = 0
        self.no_lines_header = 0
        self._exist = False
    def _calc_levenshtein(self) -> None: ...
    def _check_irregular_footer(self, line_ind: int, text: str) -> None: ...
    def _check_irregular_header(self, line_ind: int, text: str) -> None: ...
    def _determine_candidate(self, distance_max: int, line_ind: int) -> bool: ...
    def _process_page(self) -> None: ...
    def _store_irregulars(self) -> None: ...
    def _store_line_data_footer(self) -> None: ...
    def _store_line_data_header(self) -> None: ...
    def _store_results(self) -> None: ...
    def _swap_current_previous(self) -> None: ...
    def exists(self) -> bool: ...
    def process_document(
        self,
        file_name_curr: str = "",
    ) -> None: ...
