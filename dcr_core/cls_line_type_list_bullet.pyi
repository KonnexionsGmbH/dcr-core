from __future__ import annotations

import typing

from dcr_core import cls_nlp_core

class LineTypeListBullet:
    Entry = dict[str, int | str]
    Entries = list[Entry]

    EntryList = dict[str, Entries | float | int | str]
    EntryLists = list[EntryList]

    def __init__(self, file_name_curr: str) -> None: ...
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
