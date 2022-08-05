from dcr_core import cls_nlp_core

class LineTypeToc:
    def __init__(self) -> None:
        self._exist: bool = False
        self._file_name_curr: str = ""
        self._is_toc_existing: bool = False
        self._page_no: int = 0
        self._parser_line_lines_json: cls_nlp_core.NLPCore.ParserLineLines = []
        self._parser_no_pages_in_doc: int = 0
        self._strategy: str = ""
        self._toc_candidates: int = 0
        self.no_lines_toc: int = 0
        self.parser_line_pages_json: cls_nlp_core.NLPCore.ParserLinePages = []
        ...
    def _check_toc_candidate(self)->None: ...
    def _init_toc_candidate(self)->None: ...
    def _process_page_lines(self)->None: ...
    def _process_page_table(self)->None: ...
    def _process_toc_candidate_line_line(self, line_line: cls_nlp_core.NLPCore.ParserLineLine, page_no_toc: int) -> None: ...
    def _process_toc_candidate_table_line(self, line_line: cls_nlp_core.NLPCore.ParserLineLine) -> None: ...
    def _store_results(self)->None: ...
    def exists(self) -> bool: ...
    def process_document(
        self,
        file_name_curr: str,
        parser_line_pages_json: cls_nlp_core.NLPCore.ParserLinePages,
    ) -> None: ...
