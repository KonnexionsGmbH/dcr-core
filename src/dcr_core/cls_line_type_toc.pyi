from __future__ import annotations

import cls_nlp_core

class LineTypeToc:
    no_lines_toc: int

    parser_line_pages_json: cls_nlp_core.NLPCore.ParserLineLines

    def __init__(self, file_name_curr: str) -> None: ...
    def exists(self) -> bool: ...
    def process_document(self, file_name_curr: str, parser_line_pages_json: cls_nlp_core.NLPCore.ParserLinePages) -> None: ...
