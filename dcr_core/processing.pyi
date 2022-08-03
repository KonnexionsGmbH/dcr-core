def pandoc_process(full_name_in: str, full_name_out: str, language_pandoc: str) -> tuple[str, str]: ...
def parser_process(
    full_name_in: str,
    full_name_out: str,
    no_pdf_pages: int,
    document_id: int = ...,
    file_name_orig: str = ...,
) -> tuple[str, str]: ...
def pdf2image_process(
    full_name_in: str,
) -> tuple[str, str, list[tuple[str, str]]]: ...
def pdflib_process(
    full_name_in: str,
    full_name_out: str,
    document_opt_list: str,
    page_opt_list: str,
) -> tuple[str, str]: ...
def tesseract_process(full_name_in: str, full_name_out: str, language_tesseract: str) -> tuple[str, str, list[str]]: ...
def tokenizer_process(
    full_name_in: str,
    full_name_out: str,
    pipeline_name: str,
    document_id: int = ...,
    file_name_orig: str = ...,
    no_lines_footer: int = ...,
    no_lines_header: int = ...,
    no_lines_toc: int = ...,
) -> tuple[str, str]: ...
