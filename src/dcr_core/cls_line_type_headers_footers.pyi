from __future__ import annotations

from typing import Dict
from typing import List
from typing import Tuple

import cls_nlp_core

class LineTypeHeaderFooters:
    Candidate = Tuple[int, int]
    Candidates = List[Candidate]
    LineDataCell = Tuple[int, str]
    LineDataRow = Tuple[LineDataCell, LineDataCell]
    LineData = List[LineDataRow]
    LSDDataCell = Tuple[int, int, int]
    LSDDataRow = List[LSDDataCell]
    LSDData = List[LSDDataRow]
    ResultKey = Tuple[int, int]
    ResultData = Dict[ResultKey, str]

    no_lines_footer: int
    no_lines_header: int

    parser_line_pages_json: cls_nlp_core.NLPCore.ParserLinePages

    def __init__(self, file_name_curr: str) -> None:
        self._file_name_curr: str
        ...
    def exists(self) -> bool: ...
    def process_document(
        self, file_name_curr: str, no_pdf_pages: int, parser_line_pages_json: cls_nlp_core.NLPCore.ParserLinePages
    ) -> None: ...
