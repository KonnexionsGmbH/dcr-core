from dcr_core import cls_nlp_core

class LineTypeTable:
    Column = dict[str, float | int | object | str]
    Columns = list[Column]

    Row = dict[str, Columns | float | int | str]
    Rows = list[Row]

    Table = dict[str, float | int | Rows]
    Tables = list[Table]

    def __init__(self) -> None:
        self.no_tables: int = 0
        ...
    def exists(self) -> bool: ...
    def process_document(
        self,
        directory_name: str,
        document_id: int,
        file_name_curr: str,
        file_name_orig: str,
        parser_line_pages_json: cls_nlp_core.NLPCore.ParserLinePages,
    ) -> None: ...
