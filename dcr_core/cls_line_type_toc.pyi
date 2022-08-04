from dcr_core import cls_nlp_core

class LineTypeToc:
    def __init__(self) -> None:
        self.no_lines_toc: int = 0
        ...
    def exists(self) -> bool: ...
    def process_document(
        self,
        file_name_curr: str,
        parser_line_pages_json: cls_nlp_core.NLPCore.ParserLinePages,
    ) -> None: ...
