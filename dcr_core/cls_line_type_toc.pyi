from dcr_core import cls_nlp_core as cls_nlp_core

class LineTypeToc:
    parser_line_pages_json: cls_nlp_core.NLPCore.ParserLineLines

    def __init__(self, file_name_curr: str) -> None:
        self.no_lines_toc = None
        ...
    def exists(self) -> bool: ...
    def process_document(self, file_name_curr: str, parser_line_pages_json: cls_nlp_core.NLPCore.ParserLinePages) -> None: ...
