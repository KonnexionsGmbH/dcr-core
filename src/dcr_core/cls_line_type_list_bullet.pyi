from __future__ import annotations

import typing
from typing import Dict

import cls_nlp_core

class LineTypeListBullet:
    Entry = Dict[str, int | str]
    Entries = typing.List[Entry]

    List = Dict[str, Entries | float | int | str]
    Lists = typing.List[List]

    no_lists: int

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
