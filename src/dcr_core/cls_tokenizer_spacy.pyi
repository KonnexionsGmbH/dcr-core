# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module stub file."""
from __future__ import annotations

import spacy.tokens

import dcr_core.cls_nlp_core as nlp_core

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

    def __init__(self) -> None:
        self._column_no = 0
        self._column_span = 0
        self._coord_llx = 0.0
        self._coord_urx = 0.0
        self._document_id = 0
        self._document_json: nlp_core.NLPCore.DocumentJSON = {}
        self._file_name_next = ""
        self._file_name_orig = ""
        self._line_type = ""
        self._nlp: spacy.Language = None
        self._no_lines_footer = 0
        self._no_lines_header = 0
        self._no_lines_in_doc = 0
        self._no_lines_in_page = 0
        self._no_lines_in_para = 0
        self._no_lines_toc = 0
        self._no_pages_in_doc = 0
        self._no_paras_in_doc = 0
        self._no_paras_in_page = 0
        self._no_sents_in_doc = 0
        self._no_sents_in_page = 0
        self._no_tokens_in_doc = 0
        self._no_tokens_in_page = 0
        self._no_tokens_in_para = 0
        self._no_tokens_in_sent = 0
        self._page_no = 0
        self._para_lines: list[str] = []
        self._para_no = 0
        self._para_no_prev = 0
        self._para_text = ""
        self._pipeline_name = ""
        self._processing_ok = False
        self._row_no = 0
        self._sent_no = 0
        self._sentence = ""
        self._text_parser_line: dict[str, str] = {}
        self._text_parser_page: dict[str, str] = {}
        self._text_parser_para: dict[str, str] = {}
        self._token_paras: TokenizerSpacy.TokenParas = []
        self._token_sents: TokenizerSpacy.TokenSents = []
        self._token_tokens: TokenizerSpacy.TokenTokens = []
        self.token_pages: TokenizerSpacy.TokenPages = []
        self._exist = False
    def _finish_document(self) -> None: ...
    def _finish_page(self) -> None: ...
    def _finish_para(self) -> None: ...
    def _finish_sent(self) -> None: ...
    @staticmethod
    def _get_token_attributes(token: spacy.tokens.Token) -> TokenToken: ...
    def _init_document(self) -> None: ...
    def _init_page(self) -> None: ...
    def _init_para(self) -> None: ...
    def _init_sent(self) -> None: ...
    def _process_page(self) -> None: ...
    def _process_para(self) -> None: ...
    def _process_sents(self) -> None: ...
    def _process_tokens(self) -> None: ...
    def exists(self) -> bool: ...
    def process_document(
        self,
        document_id: int,
        document_json: nlp_core.NLPCore.DocumentJSON,
        file_name_next: str,
        file_name_orig: str,
        no_lines_footer: int,
        no_lines_header: int,
        no_lines_toc: int,
        pipeline_name: str,
    ) -> None: ...
    def processing_ok(self) -> bool: ...
