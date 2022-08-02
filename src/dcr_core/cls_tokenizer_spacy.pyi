from __future__ import annotations

from typing import Dict
from typing import List

class TokenizerSpacy:
    TokenToken = Dict[str, bool | float | int | str]
    TokenTokens = List[TokenToken]
    TokenSent = Dict[str, float | int | None | str | TokenTokens]
    TokenSents = List[TokenSent]
    TokenPara = Dict[str, int | TokenSents]
    TokenParas = List[TokenPara]
    TokenPage = Dict[str, int | TokenParas]
    TokenPages = List[TokenPage]
    TokenDocument = Dict[str, int | TokenPages | str]

    token_pages: TokenizerSpacy.TokenParas

    def __init__(self) -> None: ...
    def exists(self) -> bool: ...
    def process_document(
        self,
        document_id: int,
        file_name_next: str,
        file_name_orig: str,
        no_lines_footer: int,
        no_lines_header: int,
        no_lines_toc: int,
        pipeline_name: str,
    ) -> None: ...
    def processing_ok(self) -> bool: ...
