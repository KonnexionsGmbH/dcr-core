# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module stub file."""
import dcr_core.cls_nlp_core as nlp_core

class LineTypeToc:
    def __init__(
        self,
        file_name_curr: str = "",
    ) -> None:
        self._file_name_curr: str = ""
        self._is_toc_existing: bool = False
        self._lines_json: list[nlp_core.LineJSON] = []
        self._page_no = 0
        self._strategy = ""
        self._toc_candidates: list[list[int]] = []
        self.no_lines_toc: int = 0
        self._exist = False
    def _check_toc_candidate(self) -> None: ...
    def _init_toc_candidate(self) -> None: ...
    def _process_page_lines(self) -> None: ...
    def _process_page_table(self) -> None: ...
    def _process_toc_candidate_line_line(self, line_json: nlp_core.LineJSON, page_no_toc: int) -> None: ...
    def _process_toc_candidate_table_line(self, line_json: nlp_core.LineJSON) -> None: ...
    def _store_results(self) -> None: ...
    def exists(self) -> bool: ...
    def process_document(
        self,
        file_name_curr: str,
    ) -> None: ...
