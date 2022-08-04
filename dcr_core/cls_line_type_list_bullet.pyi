from dcr_core import cls_nlp_core

class LineTypeListBullet:
    Entry = dict[str, int | str]
    Entries = list[Entry]

    List = dict[str, Entries | float | int | str]
    Lists = list[List]

    def __init__(self) -> None:
        self.no_lists: int = 0
        ...
    def exists(self) -> bool: ...
    def process_document(
        self,
        directory_name: str,
        document_id: int,
        environment_variant: str,
        file_name_curr: str,
        file_name_orig: str,
        parser_line_pages_json: cls_nlp_core.NLPCore.ParserLinePages,
    ) -> None: ...
