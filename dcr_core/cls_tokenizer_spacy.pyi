class TokenizerSpacy:
    TokenToken = dict[str, bool | float | int | str]
    TokenTokens = list[TokenToken]
    TokenSent = dict[str, float | int | None | str | TokenTokens]
    TokenSents = list[TokenSent]
    TokenPara = dict[str, int | TokenSents]
    TokenParas = list[TokenPara]
    TokenPage = dict[str, int | TokenParas]
    TokenPages = list[TokenPage]
    TokenDocument = dict[str, int | TokenPages | str]

    token_pages: TokenizerSpacy.TokenParas

    def __init__(self) -> None:
        self._processing_ok = None
        self._pipeline_name = None
        ...
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
    def _finish_document(self) -> None: ...
