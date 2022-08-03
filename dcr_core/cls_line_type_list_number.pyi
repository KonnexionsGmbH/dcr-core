from __future__ import annotations

import collections
import re
import typing
from typing import Dict
from typing import Tuple

from dcr_core import cls_nlp_core

class LineTypeListNumber:
    Entry = Dict[str, int | str]
    Entries = typing.List[Entry]

    List = Dict[str, Entries | float | int | object | str]
    Lists = typing.List[List]

    RuleExtern = Tuple[str, str, collections.abc.Callable[[str, str], bool], list[str]]
    RuleIntern = Tuple[
        str,
        re.Pattern[str],
        collections.abc.Callable[[str, str], bool],
        list[str],
        str,
    ]

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
