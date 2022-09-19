# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module stub file."""
from typing import ClassVar

class Process:
    PANDOC_PDF_ENGINE_LULATEX: ClassVar[str]
    PANDOC_PDF_ENGINE_XELATEX: ClassVar[str]

    def __init__(self) -> None:
        self._document_id = 0
        self._full_name_in = ""
        self._full_name_in_directory = ""
        self._full_name_in_extension = ""
        self._full_name_in_extension_int = ""
        self._full_name_in_next_step = ""
        self._full_name_in_pandoc = ""
        self._full_name_in_parser_line = None
        self._full_name_in_parser_page = None
        self._full_name_in_parser_word = None
        self._full_name_in_pdf2image = ""
        self._full_name_in_pdflib = ""
        self._full_name_in_stem_name = ""
        self._full_name_in_tesseract = ""
        self._full_name_in_tokenizer_line = None
        self._full_name_in_tokenizer_page = None
        self._full_name_in_tokenizer_word = None
        self._full_name_orig = ""
        self._is_delete_auxiliary_files = False
        self._is_lt_footer_required = False
        self._is_lt_header_required = False
        self._is_lt_heading_required = False
        self._is_lt_list_bullet_required = False
        self._is_lt_list_number_required = False
        self._is_lt_toc_required = False
        self._is_pandoc = False
        self._is_pdf2image = False
        self._is_tesseract = False
        self._is_verbose = False
        self._language_pandoc = ""
        self._language_spacy = ""
        self._language_tesseract = ""
        self._no_lines_footer = 0
        self._no_lines_header = 0
        self._no_lines_toc = 0
        self._no_pdf_pages = 0
        self._exist = False
    def _document_check_extension(self) -> None: ...
    def _document_delete_auxiliary_file(self, full_name: str) -> None: ...
    def _document_init(self) -> None: ...
    def _document_pandoc(self) -> None: ...
    def _document_parser(self) -> None: ...
    def _document_parser_tetml_type(
        self,
        full_name_in_parser: str,
        full_name_in_tokenizer: str,
        tetml_type: str,
        is_parsing_line: bool,
        is_parsing_page: bool,
        is_parsing_word: bool,
    ) -> None: ...
    def _document_pdf2image(self) -> None: ...
    def _document_pdflib(self) -> None: ...
    def _document_tesseract(self) -> None: ...
    def _document_tokenizer(self) -> None: ...
    def document(
        self,
        full_name_in: str,
        document_id: int = ...,
        full_name_orig: str = ...,
        is_delete_auxiliary_files: bool = ...,
        is_lt_footer_required: bool = ...,
        is_lt_header_required: bool = ...,
        is_lt_heading_required: bool = ...,
        is_lt_list_bullet_required: bool = ...,
        is_lt_list_number_required: bool = ...,
        is_lt_toc_required: bool = ...,
        is_verbose: bool = ...,
        language_pandoc: str = ...,
        language_spacy: str = ...,
        language_tesseract: str = ...,
        output_directory: str = ...,
    ) -> None: ...
    @classmethod
    def pandoc(cls, full_name_in: str, full_name_out: str, language_pandoc: str) -> tuple[str, str]: ...
    @classmethod
    def parser(
        cls,
        full_name_in: str,
        full_name_out: str,
        no_pdf_pages: int,
        document_id: int = ...,
        full_name_orig: str = ...,
        is_lt_footer_required: bool = ...,
        is_lt_header_required: bool = ...,
        is_lt_heading_required: bool = ...,
        is_lt_list_bullet_required: bool = ...,
        is_lt_list_number_required: bool = ...,
        is_lt_toc_required: bool = ...,
    ) -> tuple[str, str]: ...
    @classmethod
    def pdf2image(cls, full_name_in: str) -> tuple[str, str, list[tuple[str, str]]]: ...
    @classmethod
    def pdflib(cls, full_name_in: str, full_name_out: str, document_opt_list: str, page_opt_list: str) -> tuple[str, str]: ...
    @classmethod
    def tesseract(cls, full_name_in: str, full_name_out: str, language_tesseract: str) -> tuple[str, str, list[str]]: ...
    @classmethod
    def tokenizer(
        cls,
        full_name_in: str,
        full_name_out: str,
        pipeline_name: str,
        document_id: int = ...,
        full_name_orig: str = ...,
        no_lines_footer: int = ...,
        no_lines_header: int = ...,
        no_lines_toc: int = ...,
    ) -> tuple[str, str]: ...
