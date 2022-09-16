# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module stub file."""
from __future__ import annotations

import dcr_core.cls_nlp_core as nlp_core

class LineTypeTable:
    Column = dict[str, float | int | object | str]
    Columns = list[Column]
    Row = dict[str, Columns | float | int | str]
    Rows = list[Row]
    Table = dict[str, float | int | Rows]
    Tables = list[Table]

    def __init__(
        self,
        file_name_curr: str = "",
    ) -> None:
        self._column_no = 0
        self._column_no_prev = 0
        self._columns: LineTypeTable.Columns = []
        self._first_column_llx = 0.0
        self._first_row_llx = 0.0
        self._first_row_urx = 0.0
        self._is_table_open = 0
        self._last_column_urx = 0
        self._line_no_max = 0
        self._lines_json: list[nlp_core.NLPCore.LineJSON] = []
        self._no_columns_table = 0
        self._page_idx = 0
        self._page_no_from = 0
        self._page_no_till = 0
        self._row_no = 0
        self._row_no_prev = 0
        self._rows: LineTypeTable.Rows = []
        self._tables: LineTypeTable.Tables = []
        self.no_tables = 0
        self._exist = False
    def _finish_row(self) -> None: ...
    def _finish_table(self) -> None: ...
    def _process_line(self, line_json: nlp_core.NLPCore.LineJSON) -> str: ...
    def _process_page(self) -> None: ...
    def _reset_document(self) -> None: ...
    def _reset_row(self) -> None: ...
    def _reset_table(self) -> None: ...
    def exists(self) -> bool: ...
    def process_document(
        self,
        directory_name: str,
        document_id: int,
        file_name_curr: str,
        file_name_orig: str,
    ) -> None: ...
