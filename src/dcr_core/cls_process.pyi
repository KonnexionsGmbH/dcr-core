# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module stub file."""
from typing import ClassVar

class Process:
    ERROR_01_901: ClassVar[str]
    ERROR_01_903: ClassVar[str]
    ERROR_21_901: ClassVar[str]
    ERROR_31_902: ClassVar[str]
    ERROR_31_903: ClassVar[str]
    ERROR_31_911: ClassVar[str]
    ERROR_41_901: ClassVar[str]
    ERROR_41_911: ClassVar[str]
    ERROR_51_901: ClassVar[str]
    ERROR_61_901: ClassVar[str]
    ERROR_61_902: ClassVar[str]
    ERROR_61_903: ClassVar[str]
    ERROR_71_901: ClassVar[str]
    PANDOC_PDF_ENGINE_LULATEX: ClassVar[str]
    PANDOC_PDF_ENGINE_XELATEX: ClassVar[str]

    def __init__(self) -> None:
        self._document_id = None
        self._full_name_in = None
        self._full_name_in_directory = None
        self._full_name_in_extension = None
        self._full_name_in_extension_int = None
        self._full_name_in_next_step = None
        self._full_name_in_pandoc = None
        self._full_name_in_parser = None
        self._full_name_in_pdf2image = None
        self._full_name_in_pdflib = None
        self._full_name_in_stem_name = None
        self._full_name_in_tesseract = None
        self._full_name_in_tokenizer = None
        self._full_name_orig = None
        self._is_delete_auxiliary_files = None
        self._is_lt_footer_required = None
        self._is_lt_header_required = None
        self._is_lt_heading_required = None
        self._is_lt_list_bullet_required = None
        self._is_lt_list_number_required = None
        self._is_lt_table_required = None
        self._is_lt_toc_required = None
        self._is_pandoc = None
        self._is_pdf2image = None
        self._is_tesseract = None
        self._is_verbose = None
        self._language_pandoc = None
        self._language_spacy = None
        self._language_tesseract = None
        self._no_lines_footer = None
        self._no_lines_header = None
        self._no_lines_toc = None
        self._no_pdf_pages = None
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
        is_lt_table_required: bool = ...,
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
        is_lt_table_required: bool = ...,
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
