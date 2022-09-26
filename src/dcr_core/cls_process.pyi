# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module stub file."""

class Process:
    def document(
        self,
        full_name_in: str,
        document_id: int = ...,
        full_name_orig: str = ...,
        is_delete_auxiliary_files: bool = ...,
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
