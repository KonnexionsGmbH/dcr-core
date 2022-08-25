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
    ERROR_41_901: ClassVar[str]
    ERROR_51_901: ClassVar[str]
    ERROR_61_901: ClassVar[str]
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
        self._full_name_in_parser_line = None
        self._full_name_in_parser_page = None
        self._full_name_in_parser_word = None
        self._full_name_in_pdf2image = None
        self._full_name_in_pdflib = None
        self._full_name_in_stem_name = None
        self._full_name_in_tokenizer_line = None
        self._full_name_in_tokenizer_page = None
        self._full_name_in_tokenizer_word = None
        self._full_names_in_tesseract = None
        self._full_name_orig = None
        self._is_process_pandoc = None
        self._is_process_pdf2image = None
        self._is_process_tesseract = None
        self._language_pandoc = None
        self._language_spacy = None
        self._language_tesseract = None
        self._no_pdf_pages = None
    def _document_process_check_extension(self) -> None: ...
    def _document_process_init(self) -> None: ...
    def _document_process_pandoc(self) -> None: ...
    def _document_process_parser(self) -> None: ...
    def _document_process_parser_tetml_type(self, full_name_in_parser: str, full_name_in_tokenizer: str, tetml_type: str) -> None: ...
    def _document_process_pdf2image(self) -> None: ...
    def _document_process_pdflib(self) -> None: ...
    def _document_process_tesseract(self) -> None: ...
    def _document_process_tokenizer(self) -> None: ...
    def document_process(
        self,
        full_name_in: str,
        language_pandoc: str = ...,
        language_tesseract: str = ...,
    ) -> None: ...
    @classmethod
    def pandoc_process(cls, full_name_in: str, full_name_out: str, language_pandoc: str) -> tuple[str, str]: ...
    @classmethod
    def parser_process(
        cls, full_name_in: str, full_name_out: str, no_pdf_pages: int, document_id: int = ..., file_name_orig: str = ...
    ) -> tuple[str, str]: ...
    @classmethod
    def pdf2image_process(cls, full_name_in: str) -> tuple[str, str, list[tuple[str, str]]]: ...
    @classmethod
    def pdflib_process(cls, full_name_in: str, full_name_out: str, document_opt_list: str, page_opt_list: str) -> tuple[str, str]: ...
    @classmethod
    def tesseract_process(cls, full_name_in: str, full_name_out: str, language_tesseract: str) -> tuple[str, str, list[str]]: ...
    @classmethod
    def tokenizer_process(
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
