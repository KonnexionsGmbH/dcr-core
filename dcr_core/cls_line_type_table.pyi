from __future__ import annotations

from typing import Dict
from typing import List

from dcr_core import cls_nlp_core

class LineTypeTable:
    Column = Dict[str, float | int | object | str]
    Columns = List[Column]
    Row = Dict[str, Columns | float | int | str]
    Rows = List[Row]
    Table = Dict[str, float | int | Rows]
    Tables = List[Table]

    def __init__(self, file_name_curr: str) -> None: ...
    def exists(self) -> bool: ...
    def process_document(
        self,
        directory_name: str,
        document_id: int,
        file_name_curr: str,
        file_name_orig: str,
        parser_line_pages_json: cls_nlp_core.NLPCore.ParserLinePages,
    ) -> None: ...
