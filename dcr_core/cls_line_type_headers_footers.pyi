# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module stub file."""
import dcr_core.cls_nlp_core

class LineTypeHeaderFooters:
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
        self._exist: bool = False
        self._file_name_curr: str = ""
        self._irregular_footer_cand: LineTypeHeaderFooters.Candidate = (0, 0)
        self._irregular_footer_cand_fp: LineTypeHeaderFooters.Candidates = []
        self._irregular_footer_cands: LineTypeHeaderFooters.Candidates = []
        self._irregular_header_cand: LineTypeHeaderFooters.Candidate = (0, 0)
        self._irregular_header_cand_fp: LineTypeHeaderFooters.Candidates = []
        self._irregular_header_cands: LineTypeHeaderFooters.Candidates = []
        self._is_irregular_footer: bool = False
        self._is_irregular_header: bool = False
        self._line_data: LineTypeHeaderFooters.LineData = []
        self._line_data_max: int = 0
        self._lsd_data: LineTypeHeaderFooters.LSDData = []
        self._no_irregular_footer: int = 0
        self._no_irregular_header: int = 0
        self._page_ind: int = 0
        self._page_max: int = 0
        self._parser_line_lines_json: dcr_core.cls_nlp_core.NLPCore.ParserLineLines = []
        self._result_data: LineTypeHeaderFooters.ResultData = {}
        self.line_pages_json: dcr_core.cls_nlp_core.NLPCore.ParserLinePages = []
        self.no_lines_footer: int = 0
        self.no_lines_header: int = 0
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
        line_pages_json: dcr_core.cls_nlp_core.NLPCore.ParserLinePages,
        file_name_curr: str = "",
    ) -> None: ...
