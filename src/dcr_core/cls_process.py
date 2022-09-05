# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Main processing."""

import glob
import os.path
from typing import ClassVar

import defusedxml
import defusedxml.ElementTree
import fitz
import pdf2image
import pypandoc
import PyPDF2
import pytesseract
from pdf2image.exceptions import PDFPageCountError

import dcr_core.cls_nlp_core
import dcr_core.cls_setup
import dcr_core.cls_text_parser
import dcr_core.core_glob
import dcr_core.core_utils
import dcr_core.PDFlib.TET


# pylint: disable=too-many-instance-attributes
class Process:
    """Process utility class."""

    # ------------------------------------------------------------------
    # Class variables.
    # ------------------------------------------------------------------
    ERROR_01_901: ClassVar[str] = "01.901 Issue (p_i): Document rejected because of unknown file extension='{extension}'."
    ERROR_01_903: ClassVar[str] = (
        "01.903 Issue (p_i): Error with fitz.open() processing of file '{file_name}' " + "- RuntimeError - error: '{error_msg}'."
    )

    ERROR_21_901: ClassVar[str] = (
        "21.901 Issue (p_2_i): Processing file '{full_name}' with pdf2image failed - PDFPageCountError - "
        + "error type: '{error_type}' - error: '{error_msg}'."
    )
    ERROR_31_902: ClassVar[str] = (
        "31.902 Issue (n_2_p): The file '{full_name}' cannot be converted to an " + "'PDF' document - FileNotFoundError"
    )
    ERROR_31_903: ClassVar[str] = (
        "31.903 Issue (n_2_p): The file '{full_name}' cannot be converted to an " + "'PDF' document - RuntimeError - error: '{error_msg}'."
    )
    ERROR_31_911: ClassVar[str] = "31.911 Issue (n_2_p): The number of pages of the PDF document {full_name} cannot be determined"
    ERROR_41_901: ClassVar[str] = (
        "41.901 Issue (ocr): Converting the file '{full_name}' with Tesseract OCR failed - " + "RuntimeError - error: '{error_msg}'."
    )
    ERROR_41_911: ClassVar[str] = "41.911 Issue (ocr): The number of pages of the PDF document {full_name} cannot be determined"
    ERROR_51_901: ClassVar[str] = (
        "51.901 Issue (tet): Opening document '{full_name}' - " + "error no: '{error_no}' - api: '{api_name}' - error: '{error_msg}'."
    )
    ERROR_61_901: ClassVar[str] = "61.901 Issue (s_p_j): Parsing the file '{full_name}' failed - FileNotFoundError"
    ERROR_71_901: ClassVar[str] = "71.901 Issue (tkn): Tokenizing the file '{full_name}' failed - FileNotFoundError"

    PANDOC_PDF_ENGINE_LULATEX: ClassVar[str] = "lulatex"
    PANDOC_PDF_ENGINE_XELATEX: ClassVar[str] = "xelatex"

    # ------------------------------------------------------------------
    # Initialise the instance.
    # ------------------------------------------------------------------
    def __init__(self) -> None:
        """Initialise the instance."""
        try:
            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)
        except AttributeError:
            dcr_core.core_glob.initialise_logger()
            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

        self._document_id: int = 0

        self._full_name_in: str = ""
        self._full_name_in_directory: str = ""
        self._full_name_in_extension: str = ""
        self._full_name_in_extension_int: str = ""
        self._full_name_in_next_step: str = ""
        self._full_name_in_pandoc: str = ""
        self._full_name_in_parser_line: str = ""
        self._full_name_in_parser_page: str = ""
        self._full_name_in_parser_word: str = ""
        self._full_name_in_pdf2image: str = ""
        self._full_name_in_pdflib: str = ""
        self._full_name_in_stem_name: str = ""
        self._full_name_in_tesseract: str = ""
        self._full_name_in_tokenizer_line: str = ""
        self._full_name_in_tokenizer_page: str = ""
        self._full_name_in_tokenizer_word: str = ""
        self._full_name_orig: str = ""

        self._is_pandoc: bool = False
        self._is_pdf2image: bool = False
        self._is_tesseract: bool = False

        self._language_pandoc: str = ""
        self._language_spacy: str = ""
        self._language_tesseract: str = ""

        self._no_lines_footer: int = 0
        self._no_lines_header: int = 0
        self._no_lines_toc: int = 0
        self._no_pdf_pages: int = 0

        self._exist = True

        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Check the document by the file extension and determine further
    # processing.
    # ------------------------------------------------------------------
    def _document_check_extension(self):
        """Document processing control.

        Check the document by the file extension and determine further
        processing.

        Raises:
            RuntimeError: ERROR_01_903
        """
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

        if self._full_name_in_extension_int == dcr_core.core_glob.FILE_TYPE_PDF:
            try:
                if bool("".join([page.get_text() for page in fitz.open(self._full_name_in)])):
                    self._full_name_in_pdflib = self._full_name_in
                else:
                    self._is_pdf2image = True
                    self._is_tesseract = True
                    self._full_name_in_pdf2image = self._full_name_in
            except RuntimeError as exc:
                raise RuntimeError(
                    Process.ERROR_01_903.replace("{file_name}", self._full_name_in).replace("{error_msg}", str(exc)),
                ) from exc
        elif self._full_name_in_extension_int in dcr_core.core_glob.FILE_TYPE_PANDOC:
            self._is_pandoc = True
            self._full_name_in_pandoc = self._full_name_in
        elif self._full_name_in_extension_int in dcr_core.core_glob.FILE_TYPE_TESSERACT:
            self._is_tesseract = True
            self._full_name_in_tesseract = self._full_name_in
        else:
            raise RuntimeError(Process.ERROR_01_901.replace("{extension}", self._full_name_in_extension_int))

        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Initialize the document recognition process.
    # ------------------------------------------------------------------
    def _document_init(self) -> None:
        """Initialize the document recognition process."""
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

        self._document_id: int = 0

        self._full_name_in: str = ""
        self._full_name_in_directory: str = ""
        self._full_name_in_extension: str = ""
        self._full_name_in_extension_int: str = ""
        self._full_name_in_next_step: str = ""
        self._full_name_in_pandoc: str = ""
        self._full_name_in_parser_line: str = ""
        self._full_name_in_parser_page: str = ""
        self._full_name_in_parser_word: str = ""
        self._full_name_in_pdf2image: str = ""
        self._full_name_in_pdflib: str = ""
        self._full_name_in_stem_name: str = ""
        self._full_name_in_tesseract: str = ""
        self._full_name_in_tokenizer_line: str = ""
        self._full_name_in_tokenizer_page: str = ""
        self._full_name_in_tokenizer_word: str = ""
        self._full_name_orig: str = ""

        self._is_pandoc: bool = False
        self._is_pdf2image: bool = False
        self._is_tesseract: bool = False

        self._language_pandoc: str = ""
        self._language_spacy: str = ""
        self._language_tesseract: str = ""

        self._no_lines_footer: int = 0
        self._no_lines_header: int = 0
        self._no_lines_toc: int = 0
        self._no_pdf_pages: int = 0

        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Convert the document to PDF format using Pandoc.
    # ------------------------------------------------------------------
    def _document_pandoc(self):
        """Convert the document to PDF format using Pandoc.

        Raises:
            RuntimeError: Any Pandoc issue.
        """
        if self._is_pandoc:
            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

            self._full_name_in_pdflib = dcr_core.core_utils.get_full_name_from_components(
                self._full_name_in_directory, self._full_name_in_stem_name, dcr_core.core_glob.FILE_TYPE_PDF
            )

            return_code, error_msg = Process.pandoc(
                self._full_name_in_pandoc,
                self._full_name_in_pdflib,
                self._language_pandoc,
            )
            if return_code != "ok":
                raise RuntimeError(error_msg)

            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Extract the text for all granularities from the PDF document.
    # ------------------------------------------------------------------
    def _document_parser(self):
        """Extract the text for all granularities from the PDF document."""
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

        self._full_name_in_tokenizer_line = dcr_core.core_utils.get_full_name_from_components(
            self._full_name_in_directory,
            self._full_name_in_stem_name + "." + dcr_core.cls_nlp_core.NLPCore.LINE_XML_VARIATION + dcr_core.core_glob.FILE_TYPE_JSON,
        )

        self._full_name_in_tokenizer_page = dcr_core.core_utils.get_full_name_from_components(
            self._full_name_in_directory,
            self._full_name_in_stem_name + "." + dcr_core.cls_nlp_core.NLPCore.PAGE_XML_VARIATION + dcr_core.core_glob.FILE_TYPE_JSON,
        )

        self._full_name_in_tokenizer_word = dcr_core.core_utils.get_full_name_from_components(
            self._full_name_in_directory,
            self._full_name_in_stem_name + "." + dcr_core.cls_nlp_core.NLPCore.WORD_XML_VARIATION + dcr_core.core_glob.FILE_TYPE_JSON,
        )

        for (full_name_in_parser, full_name_in_tokenizer, tetml_type, is_parsing_line, is_parsing_page, is_parsing_word,) in (
            (
                self._full_name_in_parser_line,
                self._full_name_in_tokenizer_line,
                dcr_core.cls_nlp_core.NLPCore.TETML_TYPE_LINE,
                True,
                False,
                False,
            ),
            (
                self._full_name_in_parser_page,
                self._full_name_in_tokenizer_page,
                dcr_core.cls_nlp_core.NLPCore.TETML_TYPE_PAGE,
                False,
                True,
                False,
            ),
            (
                self._full_name_in_parser_word,
                self._full_name_in_tokenizer_word,
                dcr_core.cls_nlp_core.NLPCore.TETML_TYPE_WORD,
                False,
                False,
                True,
            ),
        ):
            if (
                is_parsing_page
                and not dcr_core.core_glob.setup.is_tetml_page
                or is_parsing_word
                and not dcr_core.core_glob.setup.is_tetml_word
            ):
                continue

            self._document_parser_tetml_type(
                full_name_in_parser,
                full_name_in_tokenizer,
                tetml_type,
                is_parsing_line,
                is_parsing_page,
                is_parsing_word,
            )

            if is_parsing_line:
                self._no_lines_footer = dcr_core.core_glob.line_type_header_footer.no_lines_footer
                self._no_lines_header = dcr_core.core_glob.line_type_header_footer.no_lines_header
                self._no_lines_toc = dcr_core.core_glob.line_type_toc.no_lines_toc

        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Extract the text for a specific granularity from the PDF document.
    # ------------------------------------------------------------------
    def _document_parser_tetml_type(
        self,
        full_name_in_parser,
        full_name_in_tokenizer,
        tetml_type,
        is_parsing_line,
        is_parsing_page,
        is_parsing_word,
    ):
        """XML Parser processing.

        Extract the text for a specific granularity from the PDF
        document.

        Raises:
            RuntimeError: Any parser issue.
        """
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

        dcr_core.core_utils.progress_msg(dcr_core.core_glob.setup.is_verbose, f"Start of processing for tetml type '{tetml_type}'")

        dcr_core.core_glob.setup.is_parsing_line = is_parsing_line
        dcr_core.core_glob.setup.is_parsing_page = is_parsing_page
        dcr_core.core_glob.setup.is_parsing_word = is_parsing_word

        return_code, error_msg = Process.parser(
            full_name_in_parser,
            full_name_in_tokenizer,
            self._no_pdf_pages,
            self._document_id,
            self._full_name_orig,
        )
        if return_code != "ok":
            raise RuntimeError(error_msg)

        dcr_core.core_utils.progress_msg(dcr_core.core_glob.setup.is_verbose, f"End   of processing for tetml type '{tetml_type}'")

        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Convert the PDF document to an image file using pdf2image.
    # ------------------------------------------------------------------
    def _document_pdf2image(self):
        """Convert the PDF document to an image file using pdf2image.

        Raises:
            RuntimeError: Any pdf2image issue.
        """
        if self._is_pdf2image:
            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

            self._full_name_in_tesseract = dcr_core.core_utils.get_full_name_from_components(
                self._full_name_in_directory,
                self._full_name_in_stem_name
                + "_[0-9]*."
                + (
                    dcr_core.core_glob.FILE_TYPE_PNG
                    if dcr_core.core_glob.setup.pdf2image_type == dcr_core.cls_setup.Setup.PDF2IMAGE_TYPE_PNG
                    else dcr_core.core_glob.FILE_TYPE_JPEG
                ),
            )

            return_code, error_msg, _ = Process.pdf2image(
                self._full_name_in_pdf2image,
            )
            if return_code != "ok":
                raise RuntimeError(error_msg)

            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Extract the text and metadata from a PDF document to an XML file.
    # ------------------------------------------------------------------
    def _document_pdflib(self):
        """Extract the text and metadata from a PDF document to an XML file.

        Raises:
            RuntimeError: Any PDFlib TET issue.
        """
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

        # noinspection PyUnresolvedReferences
        self._no_pdf_pages = len(PyPDF2.PdfReader(self._full_name_in_pdflib).pages)
        if self._no_pdf_pages == 0:
            raise RuntimeError(f"The number of pages of the PDF document {self._full_name_in_pdflib} cannot be determined")

        self._full_name_in_parser_line = dcr_core.core_utils.get_full_name_from_components(
            self._full_name_in_directory,
            self._full_name_in_stem_name + "." + dcr_core.cls_nlp_core.NLPCore.LINE_XML_VARIATION + dcr_core.core_glob.FILE_TYPE_XML,
        )

        return_code, error_msg = Process.pdflib(
            full_name_in=self._full_name_in_pdflib,
            full_name_out=self._full_name_in_parser_line,
            document_opt_list=dcr_core.cls_nlp_core.NLPCore.LINE_TET_DOCUMENT_OPT_LIST,
            page_opt_list=dcr_core.cls_nlp_core.NLPCore.LINE_TET_PAGE_OPT_LIST,
        )
        if return_code != "ok":
            raise RuntimeError(error_msg)

        if dcr_core.core_glob.setup.is_tetml_page:
            self._full_name_in_parser_page = dcr_core.core_utils.get_full_name_from_components(
                self._full_name_in_directory,
                self._full_name_in_stem_name + "." + dcr_core.cls_nlp_core.NLPCore.PAGE_XML_VARIATION + dcr_core.core_glob.FILE_TYPE_XML,
            )
            return_code, error_msg = Process.pdflib(
                full_name_in=self._full_name_in_pdflib,
                full_name_out=self._full_name_in_parser_page,
                document_opt_list=dcr_core.cls_nlp_core.NLPCore.PAGE_TET_DOCUMENT_OPT_LIST,
                page_opt_list=dcr_core.cls_nlp_core.NLPCore.PAGE_TET_PAGE_OPT_LIST,
            )
            if return_code != "ok":
                raise RuntimeError(error_msg)

        if dcr_core.core_glob.setup.is_tetml_word:
            self._full_name_in_parser_word = dcr_core.core_utils.get_full_name_from_components(
                self._full_name_in_directory,
                self._full_name_in_stem_name + "." + dcr_core.cls_nlp_core.NLPCore.WORD_XML_VARIATION + dcr_core.core_glob.FILE_TYPE_XML,
            )
            return_code, error_msg = Process.pdflib(
                full_name_in=self._full_name_in_pdflib,
                full_name_out=self._full_name_in_parser_word,
                document_opt_list=dcr_core.cls_nlp_core.NLPCore.WORD_TET_DOCUMENT_OPT_LIST,
                page_opt_list=dcr_core.cls_nlp_core.NLPCore.WORD_TET_PAGE_OPT_LIST,
            )
            if return_code != "ok":
                raise RuntimeError(error_msg)

        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Convert one or more image files to a PDF file using Tesseract OCR.
    # ------------------------------------------------------------------
    def _document_tesseract(self):
        """Process the document with Tesseract OCR.

        Convert one or more image files to a PDF file using Tesseract
        OCR.

        Raises:
            RuntimeError: Any Tesseract OCR issue.
        """
        if self._is_tesseract:
            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

            if self._is_pdf2image:
                self._full_name_in_stem_name += "_0"

            self._full_name_in_pdflib = dcr_core.core_utils.get_full_name_from_components(
                self._full_name_in_directory, self._full_name_in_stem_name, dcr_core.core_glob.FILE_TYPE_PDF
            )

            return_code, error_msg, _ = Process.tesseract(
                self._full_name_in_tesseract,
                self._full_name_in_pdflib,
                self._language_tesseract,
            )
            if return_code != "ok":
                raise RuntimeError(error_msg)

            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Convert the PDF document to an image file using pdf2image.
    # ------------------------------------------------------------------
    def _document_tokenizer(self) -> None:
        """Tokenize the document with spaCy.

        Raises:
            RuntimeError: Any spaCy issue.
        """
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

        try:
            dcr_core.core_glob.tokenizer_spacy.exists()
        except AttributeError:
            dcr_core.core_glob.tokenizer_spacy = dcr_core.cls_tokenizer_spacy.TokenizerSpacy()

        self._full_name_in_next_step = dcr_core.core_utils.get_full_name_from_components(
            self._full_name_in_directory,
            self._full_name_in_stem_name + ".line_token." + dcr_core.core_glob.FILE_TYPE_JSON,
        )

        return_code, error_msg = Process.tokenizer(
            full_name_in=self._full_name_in_tokenizer_line,
            full_name_out=self._full_name_in_next_step,
            pipeline_name=self._language_spacy,
            document_id=self._document_id,
            full_name_orig=self._full_name_orig,
            no_lines_footer=self._no_lines_footer,
            no_lines_header=self._no_lines_header,
            no_lines_toc=self._no_lines_toc,
        )
        if return_code != "ok":
            raise RuntimeError(error_msg)

        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Document content recognition for a specific file.
    # ------------------------------------------------------------------
    def document(
        self,
        full_name_in: str,
        document_id: int = None,
        full_name_orig: str = None,
        language_pandoc: str = None,
        language_spacy: str = None,
        language_tesseract: str = None,
    ) -> None:
        """Document content recognition for a specific file.

        Args:
            full_name_in (str):
                Full file name of the document file.
            document_id (int, optional):
                Document identification.
                Defaults to "-1".
            full_name_orig (str, optional):
                Original full file name.
                Defaults to the full file name of the document file.
            language_pandoc (str, optional):
                Pandoc language code.
                Defaults to English.
            language_spacy (str, optional):
                spaCy language code.
                Defaults to English transformer pipeline (roberta-base)..
            language_tesseract (str, optional):
                Tesseract OCR language code.
                Defaults to English.

        Raises:
            RuntimeError: Any issue from Pandoc, pdf2image, PDFlib TET, spaCy, or Tesseract OCR.
        """
        # Initialise the logging functionality.
        dcr_core.core_glob.initialise_logger()

        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)
        dcr_core.core_glob.logger.debug("param full_name_in=%s", full_name_in)
        dcr_core.core_glob.logger.debug("param document_id =%i", document_id)

        self._document_init()

        self._document_id = document_id if document_id else -1
        self._full_name_in = full_name_in
        self._full_name_orig = full_name_orig if full_name_orig else full_name_in
        self._language_pandoc = language_pandoc if language_pandoc else dcr_core.cls_nlp_core.NLPCore.LANGUAGE_PANDOC_DEFAULT
        self._language_spacy = language_spacy if language_spacy else dcr_core.cls_nlp_core.NLPCore.LANGUAGE_SPACY_DEFAULT
        self._language_tesseract = language_tesseract if language_tesseract else dcr_core.cls_nlp_core.NLPCore.LANGUAGE_TESSERACT_DEFAULT

        dcr_core.core_glob.logger.debug("param full_name_orig    =%s", self._full_name_orig)
        dcr_core.core_glob.logger.debug("param language_pandoc   =%s", self._language_pandoc)
        dcr_core.core_glob.logger.debug("param language_spacy    =%s", self._language_spacy)
        dcr_core.core_glob.logger.debug("param language_tesseract=%s", self._language_tesseract)

        # Load the configuration parameters.
        dcr_core.core_glob.setup = dcr_core.cls_setup.Setup()

        (
            self._full_name_in_directory,
            self._full_name_in_stem_name,
            self._full_name_in_extension,
        ) = dcr_core.core_utils.get_components_from_full_name(self._full_name_in)

        self._full_name_in_extension_int = (
            self._full_name_in_extension.lower() if self._full_name_in_extension else self._full_name_in_extension
        )

        self._document_check_extension()

        self._document_pandoc()

        self._document_pdf2image()

        self._document_tesseract()

        self._document_pdflib()

        self._document_parser()

        self._document_tokenizer()

        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Converting a Non-PDF file to a PDF file.
    # ------------------------------------------------------------------
    @classmethod
    def pandoc(
        cls,
        full_name_in: str,
        full_name_out: str,
        language_pandoc: str,
    ) -> tuple[str, str]:
        """Convert a Non-PDF file to a PDF file.

        The following file formats are converted into
        PDF format here with the help of Pandoc:

        - csv - comma-separated values
        - docx - Office Open XML
        - epub - e-book file format
        - html - HyperText Markup Language
        - odt - Open Document Format for Office Applications
        - rst - reStructuredText (RST
        - rtf - Rich Text Format

        Args:
            full_name_in (str):
                    The directory name and file name of the input file.
            full_name_out (str):
                    The directory name and file name of the output file.
            language_pandoc (str):
                    The Pandoc name of the document language.

        Returns:
            tuple[str, str]:
                    ("ok", "") if the processing has been completed successfully,
                               otherwise a corresponding error code and error message.
        """
        try:
            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)
        except AttributeError:
            dcr_core.core_glob.initialise_logger()
            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

        dcr_core.core_glob.logger.debug("param full_name_in   =%s", full_name_in)
        dcr_core.core_glob.logger.debug("param full_name_out  =%s", full_name_out)
        dcr_core.core_glob.logger.debug("param language_pandoc=%s", language_pandoc)

        # Convert the document
        extra_args = [
            f"--pdf-engine={Process.PANDOC_PDF_ENGINE_XELATEX}",
            "-V",
            f"lang:{language_pandoc}",
        ]

        try:
            pypandoc.convert_file(
                full_name_in,
                dcr_core.core_glob.FILE_TYPE_PDF,
                extra_args=extra_args,
                outputfile=full_name_out,
            )

            if len(PyPDF2.PdfReader(full_name_out).pages) == 0:
                error_msg = Process.ERROR_31_911.replace("{full_name}", full_name_out)
                dcr_core.core_glob.logger.debug("return               =%s", (error_msg[:6], error_msg))
                dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)
                return error_msg[:6], error_msg

        except FileNotFoundError:
            error_msg = Process.ERROR_31_902.replace("{full_name}", full_name_in)
            dcr_core.core_glob.logger.debug("return               =%s", (error_msg[:6], error_msg))
            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)
            return error_msg[:6], error_msg
        except RuntimeError as err:
            error_msg = Process.ERROR_31_903.replace("{full_name}", full_name_in).replace("{error_msg}", str(err))
            dcr_core.core_glob.logger.debug("return               =%s", (error_msg[:6], error_msg))
            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)
            return error_msg[:6], error_msg

        dcr_core.core_glob.logger.debug("return               =%s", dcr_core.core_glob.RETURN_OK)
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

        return dcr_core.core_glob.RETURN_OK

    # ------------------------------------------------------------------
    # Extracting the text from the PDF document.
    # ------------------------------------------------------------------
    @classmethod
    def parser(
        cls,
        full_name_in: str,
        full_name_out: str,
        no_pdf_pages: int,
        document_id: int = -1,
        full_name_orig: str = dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE,
    ) -> tuple[str, str]:
        """Extract the text from the PDF document.

        From the line-oriented XML output file of PDFlib TET,
        the text and relevant metadata are extracted with the
        help of an XML parser and stored in a JSON file.

        Args:
            full_name_in (str):
                    The directory name and file name of the input file.
            full_name_out (str):
                    The directory name and file name of the output file.
            no_pdf_pages (int):
                    Total number of PDF pages.
            document_id (int, optional):
                    The identification number of the document.
                    Defaults to -1.
            full_name_orig (str, optional):
                    The file name of the originating document.
                    Defaults to dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE.

        Returns:
            tuple[str, str]:
                    ("ok", "") if the processing has been completed successfully,
                               otherwise a corresponding error code and error message.
        """
        try:
            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)
        except AttributeError:
            dcr_core.core_glob.initialise_logger()
            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

        dcr_core.core_glob.logger.debug("param document_id   =%i", document_id)
        dcr_core.core_glob.logger.debug("param full_name_orig=%s", full_name_orig)
        dcr_core.core_glob.logger.debug("param full_name_in  =%s", full_name_in)
        dcr_core.core_glob.logger.debug("param full_name_out =%s", full_name_out)
        dcr_core.core_glob.logger.debug("param no_pdf_pages  =%i", no_pdf_pages)

        try:
            # Create the Element tree object
            tree = defusedxml.ElementTree.parse(full_name_in)

            # Get the root Element
            root = tree.getroot()

            dcr_core.core_glob.text_parser = dcr_core.cls_text_parser.TextParser()

            for child in root:
                child_tag = child.tag[dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_FROM :]
                match child_tag:
                    case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_DOCUMENT:
                        dcr_core.core_glob.text_parser.parse_tag_document(
                            directory_name=os.path.dirname(full_name_in),
                            document_id=document_id,
                            environment_variant=dcr_core.core_glob.setup.environment_variant,
                            file_name_curr=os.path.basename(full_name_in),
                            file_name_next=full_name_out,
                            file_name_orig=full_name_orig,
                            no_pdf_pages=no_pdf_pages,
                            parent=child,
                            parent_tag=child_tag,
                        )
                    case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_CREATION:
                        pass
        except FileNotFoundError:
            error_msg = Process.ERROR_61_901.replace("{full_name}", full_name_in)
            dcr_core.core_glob.logger.debug("return              =%s", (error_msg[:6], error_msg))
            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)
            return error_msg[:6], error_msg

        dcr_core.core_glob.logger.debug("return              =%s", dcr_core.core_glob.RETURN_OK)
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

        return dcr_core.core_glob.RETURN_OK

    # ------------------------------------------------------------------
    # Converting a scanned PDF file to a set of image files.
    # ------------------------------------------------------------------
    @classmethod
    def pdf2image(
        cls,
        full_name_in: str,
    ) -> tuple[str, str, list[tuple[str, str]]]:
        """Convert a scanned PDF file to a set of image files.

        To extract the text from a scanned PDF document, it must
        first be converted into one or more image files, depending
        on the number of pages. Then these image files are converted
        into a normal PDF document with the help of an OCR programme.
        The input file for this method must be a scanned PDF document,
        which is then converted into image files with the help of PDF2Image.

        Args:
            full_name_in (str):
                    The directory name and file name of the input file.

        Returns:
            tuple[str, str, list[tuple[str,str]]]:
                    ("ok", "", [...]) if the processing has been completed successfully,
                                      otherwise a corresponding error code and error message.
        """
        try:
            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)
        except AttributeError:
            dcr_core.core_glob.initialise_logger()
            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

        dcr_core.core_glob.logger.debug("param full_name_in=%s", full_name_in)

        try:
            images = pdf2image.convert_from_path(full_name_in)

            children: list[tuple[str, str]] = []
            no_children = 0

            directory_name = os.path.dirname(full_name_in)
            stem_name = os.path.splitext(os.path.basename(full_name_in))[0]

            try:
                os.remove(
                    dcr_core.core_utils.get_full_name_from_components(
                        directory_name,
                        stem_name
                        + "_*."
                        + (
                            dcr_core.core_glob.FILE_TYPE_PNG
                            if dcr_core.core_glob.setup.pdf2image_type == dcr_core.cls_setup.Setup.PDF2IMAGE_TYPE_PNG
                            else dcr_core.core_glob.FILE_TYPE_JPEG
                        ),
                    )
                )
            except OSError:
                pass

            # Store the image pages
            for img in images:
                no_children += 1

                file_name_next = (
                    stem_name
                    + "_"
                    + str(no_children)
                    + "."
                    + (
                        dcr_core.core_glob.FILE_TYPE_PNG
                        if dcr_core.core_glob.setup.pdf2image_type == dcr_core.cls_setup.Setup.PDF2IMAGE_TYPE_PNG
                        else dcr_core.core_glob.FILE_TYPE_JPEG
                    )
                )

                full_name_next = dcr_core.core_utils.get_full_name_from_components(
                    directory_name,
                    file_name_next,
                )

                img.save(
                    full_name_next,
                    dcr_core.core_glob.setup.pdf2image_type,
                )

                children.append((file_name_next, full_name_next))
        except PDFPageCountError as err:
            error_msg = (
                Process.ERROR_21_901.replace("{full_name}", full_name_in)
                .replace("{error_type}", str(type(err)))
                .replace("{error_msg}", str(err))
            )
            dcr_core.core_glob.logger.debug("return            =%s", (error_msg[:6], error_msg, []))
            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)
            return error_msg[:6], error_msg, []

        dcr_core.core_glob.logger.debug(
            "return            =%s", (dcr_core.core_glob.RETURN_OK[0], dcr_core.core_glob.RETURN_OK[1], children)
        )
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

        return dcr_core.core_glob.RETURN_OK[0], dcr_core.core_glob.RETURN_OK[1], children

    # ------------------------------------------------------------------
    # Processing a PDF file with PDFlib TET.
    # ------------------------------------------------------------------
    @classmethod
    def pdflib(
        cls,
        full_name_in: str,
        full_name_out: str,
        document_opt_list: str,
        page_opt_list: str,
    ) -> tuple[str, str]:
        """Process a PDF file with PDFlib TET.

        The data from a PDF file is made available in XML files
        with the help of PDFlib TET. The granularity of the XML
        files can be word, line or paragraph depending on the
        document and page options selected.

        Args:
            full_name_in (str):
                    Directory name and file name of the input file.
            full_name_out (str):
                    Directory name and file name of the output file.
            document_opt_list (str):
                    Document level options:
                        word: engines={noannotation noimage text notextcolor novector}
                        line: engines={noannotation noimage text notextcolor novector}
                        page: engines={noannotation noimage text notextcolor novector} lineseparator=U+0020
            page_opt_list (str):
                    Page level options:
                        word: granularity=word tetml={elements={line}}
                        line: granularity=line
                        page: granularity=page

        Returns:
            tuple[str, str]:
                    ("ok", "") if the processing has been completed successfully,
                               otherwise a corresponding error code and error message.
        """
        try:
            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)
        except AttributeError:
            dcr_core.core_glob.initialise_logger()
            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

        dcr_core.core_glob.logger.debug("param full_name_in     =%s", full_name_in)
        dcr_core.core_glob.logger.debug("param full_name_out    =%s", full_name_out)
        dcr_core.core_glob.logger.debug("param document_opt_list=%s", document_opt_list)
        dcr_core.core_glob.logger.debug("param page_opt_list    =%s", page_opt_list)

        tet = dcr_core.PDFlib.TET.TET()

        doc_opt_list = f"tetml={{filename={{{full_name_out}}}}} {document_opt_list}"

        if (file_curr := tet.open_document(full_name_in, doc_opt_list)) == -1:
            error_msg = (
                Process.ERROR_51_901.replace("{full_name}", full_name_in)
                .replace("{error_no}", str(tet.get_errnum()))
                .replace("{api_name}", tet.get_apiname() + "()")
                .replace("{error_msg}", tet.get_errmsg())
            )
            dcr_core.core_glob.logger.debug("return                 =%s", (error_msg[:6], error_msg))
            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)
            return error_msg[:6], error_msg

        # get number of pages in the document */
        no_pages = tet.pcos_get_number(file_curr, "length:pages")

        # loop over pages in the document */
        for page_no in range(1, int(no_pages) + 1):
            tet.process_page(file_curr, page_no, page_opt_list)

        # This could be combined with the last page-related call
        tet.process_page(file_curr, 0, "tetml={trailer}")

        tet.close_document(file_curr)

        tet.delete()

        dcr_core.core_glob.logger.debug("return                 =%s", dcr_core.core_glob.LOGGER_END)
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

        return dcr_core.core_glob.RETURN_OK

    # ------------------------------------------------------------------
    # Converting image files to PDF files via OCR.
    # ------------------------------------------------------------------
    @classmethod
    def tesseract(
        cls,
        full_name_in: str,
        full_name_out: str,
        language_tesseract: str,
    ) -> tuple[str, str, list[str]]:
        """Convert image files to PDF files via OCR.

        The documents of the following document types are converted
        to the PDF format using Tesseract OCR:

        - bmp - bitmap image file
        - gif - Graphics Interchange Format
        - jp2 - JPEG 2000
        - jpeg - Joint Photographic Experts Group
        - png - Portable Network Graphics
        - pnm - portable any-map format
        - tif - Tag Image File Format
        - tiff - Tag Image File Format
        - webp - Image file format with lossless and lossy compression

        After processing with Tesseract OCR, the files split previously
        into multiple image files are combined into a single PDF document.

        Args:
            full_name_in (str):
                    The directory name and file name of the input file.
            full_name_out (str):
                    The directory name and file name of the output file.
            language_tesseract (str):
                    The Tesseract name of the document language.

        Returns:
            tuple[str, str, list[str]]:
                    ("ok", "", [...]) if the processing has been completed successfully,
                                      otherwise a corresponding error code and error message.
        """
        try:
            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)
        except AttributeError:
            dcr_core.core_glob.initialise_logger()
            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

        dcr_core.core_glob.logger.debug("param full_name_in      =%s", full_name_in)
        dcr_core.core_glob.logger.debug("param full_name_out     =%s", full_name_out)
        dcr_core.core_glob.logger.debug("param language_tesseract=%s", language_tesseract)

        children: list[str] = []

        pdf_writer = PyPDF2.PdfWriter()

        for full_name in sorted(glob.glob(full_name_in)):
            try:
                pdf = pytesseract.image_to_pdf_or_hocr(
                    extension="pdf",
                    image=full_name,
                    lang=language_tesseract,
                    timeout=dcr_core.core_glob.setup.tesseract_timeout,
                )

                with open(full_name_out, "w+b") as file_handle:
                    # PDF type is bytes by default
                    file_handle.write(pdf)

                if len(PyPDF2.PdfReader(full_name_out).pages) == 0:
                    error_msg = Process.ERROR_41_911.replace("{full_name_out}", full_name_out)
                    dcr_core.core_glob.logger.debug("return                  =%s", (error_msg[:6], error_msg, []))
                    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)
                    return error_msg[:6], error_msg, []

                pdf_reader = PyPDF2.PdfReader(full_name_out)

                for page in pdf_reader.pages:
                    # Add each page to the writer object
                    pdf_writer.add_page(page)

                children.append(full_name)

            except RuntimeError as err:
                error_msg = Process.ERROR_41_901.replace("{full_name}", full_name_in).replace("{error_msg}", str(err))
                dcr_core.core_glob.logger.debug("return                  =%s", (error_msg[:6], error_msg, []))
                dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)
                return error_msg[:6], error_msg, []

        # Write out the merged PDF
        with open(full_name_out, "wb") as file_handle:
            pdf_writer.write(file_handle)

        dcr_core.core_glob.logger.debug(
            "return                  =%s", (dcr_core.core_glob.RETURN_OK[0], dcr_core.core_glob.RETURN_OK[1], children)
        )
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

        return dcr_core.core_glob.RETURN_OK[0], dcr_core.core_glob.RETURN_OK[1], children

    # ------------------------------------------------------------------
    # Tokenizing the text from the PDF document.
    # ------------------------------------------------------------------
    @classmethod
    def tokenizer(
        cls,
        full_name_in: str,
        full_name_out: str,
        pipeline_name: str,
        document_id: int = -1,
        full_name_orig: str = "",
        no_lines_footer: int = -1,
        no_lines_header: int = -1,
        no_lines_toc: int = -1,
    ) -> tuple[str, str]:
        """Tokenizing the text from the PDF document.

        The line-oriented text is broken down into qualified
        tokens with the means of SpaCy.

        Args:
            full_name_in (str):
                    The directory name and file name of the input file.
            full_name_out (str):
                    The directory name and file name of the output file.
            pipeline_name (str):
                    The loaded SpaCy pipeline.
            document_id (int, optional):
                    The identification number of the document.
                    Defaults to -1.
            full_name_orig (str, optional):
                    The file name of the originating document. Defaults to "".
            no_lines_footer (int, optional):
                    Total number of footer lines.
                    Defaults to -1.
            no_lines_header (int, optional):
                    Total number of header lines.
                    Defaults to -1.
            no_lines_toc (int, optional):
                    Total number of TOC lines.
                    Defaults to -1.

        Returns:
            tuple[str, str]:
                    ("ok", "") if the processing has been completed successfully,
                               otherwise a corresponding error code and error message.
        """
        try:
            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)
        except AttributeError:
            dcr_core.core_glob.initialise_logger()
            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

        dcr_core.core_glob.logger.debug("param document_id    =%i", document_id)
        dcr_core.core_glob.logger.debug("param full_name_in   =%s", full_name_in)
        dcr_core.core_glob.logger.debug("param full_name_orig =%s", full_name_orig)
        dcr_core.core_glob.logger.debug("param full_name_out  =%s", full_name_out)
        dcr_core.core_glob.logger.debug("param no_lines_footer=%i", no_lines_footer)
        dcr_core.core_glob.logger.debug("param no_lines_header=%i", no_lines_header)
        dcr_core.core_glob.logger.debug("param no_lines_toc   =%i", no_lines_toc)
        dcr_core.core_glob.logger.debug("param pipeline_name  =%s", pipeline_name)

        try:
            dcr_core.core_glob.text_parser = dcr_core.cls_text_parser.TextParser.from_files(
                file_encoding=dcr_core.core_glob.FILE_ENCODING_DEFAULT, full_name_line=full_name_in
            )

            dcr_core.core_glob.tokenizer_spacy.process_document(
                document_id=document_id,
                file_name_next=full_name_out,
                file_name_orig=full_name_orig,
                no_lines_footer=no_lines_footer,
                no_lines_header=no_lines_header,
                no_lines_toc=no_lines_toc,
                pipeline_name=pipeline_name,
            )

        except FileNotFoundError:
            error_msg = Process.ERROR_71_901.replace("{full_name}", full_name_in)
            dcr_core.core_glob.logger.debug("return               =%s", (error_msg[:6], error_msg))
            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)
            return error_msg[:6], error_msg

        dcr_core.core_glob.logger.debug("return               =%s", dcr_core.core_glob.RETURN_OK)
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

        return dcr_core.core_glob.RETURN_OK
