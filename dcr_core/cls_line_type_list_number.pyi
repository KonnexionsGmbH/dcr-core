import collections
import re

from dcr_core import cls_nlp_core

class LineTypeListNumber:
    Entry = dict[str, int | str]
    Entries = list[Entry]

    List = dict[str, Entries | float | int | object | str]
    Lists = list[List]

    RuleExtern = tuple[str, str, collections.abc.Callable[[str, str], bool], list[str]]
    RuleIntern = tuple[
        str,
        re.Pattern[str],
        collections.abc.Callable[[str, str], bool],
        list[str],
        str,
    ]

    def __init__(self, file_name_curr: str) -> None:
        self.no_lists = None
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
