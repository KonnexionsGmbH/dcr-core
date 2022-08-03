import collections.abc

from dcr_core import cls_nlp_core as cls_nlp_core

class TextParser:
    parse_result_line_lines: cls_nlp_core.NLPCore.ParserLineLines
    parse_result_line_pages: cls_nlp_core.NLPCore.ParserLinePages
    parse_result_titles: list[str]

    def __init__(self) -> None:
        self.parse_result_line_document = None
        ...
    def exists(self) -> bool: ...
    @classmethod
    def from_files(
        cls, file_encoding: str, full_name_line: str = ..., full_name_page: str = ..., full_name_word: str = ...
    ) -> TextParser: ...
    def parse_tag_document(
        self,
        directory_name: str,
        document_id: int,
        environment_variant: str,
        file_name_curr: str,
        file_name_next: str,
        file_name_orig: str,
        no_pdf_pages: int,
        parent: collections.abc.Iterable[str],
        parent_tag: str,
    ) -> None: ...
