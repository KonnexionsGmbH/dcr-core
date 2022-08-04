from dcr_core import cls_nlp_core

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

    def __init__(self) -> None:
        self.no_lines_footer: int = 0
        self.no_lines_header: int = 0
        ...
    def exists(self) -> bool: ...
    def process_document(
        self,
        file_name_curr: str,
        no_pdf_pages: int,
        parser_line_pages_json: cls_nlp_core.NLPCore.ParserLinePages,
    ) -> None: ...
