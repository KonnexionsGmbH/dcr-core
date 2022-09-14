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

import dcr_core.cls_nlp_core as nlp_core
import dcr_core.cls_setup as setup
import dcr_core.cls_text_parser as parser
import dcr_core.cls_tokenizer_spacy as tokenizer
from dcr_core import core_glob
from dcr_core import core_utils

# noinspection PyUnresolvedReferences
from dcr_core.PDFlib import TET


# pylint: disable=too-many-instance-attributes
class Process:
    """Process utility class."""

    # ------------------------------------------------------------------
    # Class variables.
    # ------------------------------------------------------------------
    ERROR_01_901: ClassVar[str] = "01.901 Issue (p_i): Document rejected because of unknown file extension='{extension}'."
    ERROR_01_903: ClassVar[str] = (
        "01.903 Issue (p_i): Error with fitz.open() processing of file '{file_name}' " + "- RuntimeError - error: '{error_msg}'"
    )

    ERROR_21_901: ClassVar[str] = (
        "21.901 Issue (p_2_i): Processing file '{full_name}' with pdf2image failed - PDFPageCountError - "
        + "error type: '{error_type}' - error: '{error_msg}'"
    )
    ERROR_31_902: ClassVar[str] = (
        "31.902 Issue (n_2_p): The file '{full_name}' cannot be converted to an " + "'PDF' document - FileNotFoundError"
    )
    ERROR_31_903: ClassVar[str] = (
        "31.903 Issue (n_2_p): The file '{full_name}' cannot be converted to an " + "'PDF' document - RuntimeError - error: '{error_msg}'"
    )
    ERROR_31_911: ClassVar[str] = "31.911 Issue (n_2_p): The pdf document {full_name} for PDFlib TET is an empty file"
    ERROR_41_901: ClassVar[str] = (
        "41.901 Issue (ocr): Converting the file '{full_name}' with Tesseract OCR failed - " + "RuntimeError - error: '{error_msg}'"
    )
    ERROR_41_911: ClassVar[str] = "41.911 Issue (ocr): Tesseract OCR has created an empty pdf file from the file {full_name}"
    ERROR_51_901: ClassVar[str] = (
        "51.901 Issue (tet): Opening document '{full_name}' - " + "error no: '{error_no}' - api: '{api_name}' - error: '{error_msg}'"
    )
    ERROR_61_901: ClassVar[str] = "61.901 Issue (s_p_j): Parsing the file '{full_name}' failed - FileNotFoundError"
    ERROR_61_902: ClassVar[str] = "61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'"
    ERROR_61_903: ClassVar[str] = "61.903 Issue (s_p_j): The number of unknown XML nodes is {no_errors} - details can be found in the log"
    ERROR_71_901: ClassVar[str] = "71.901 Issue (tkn): Tokenizing the file '{full_name}' failed - FileNotFoundError"

    PANDOC_PDF_ENGINE_LULATEX: ClassVar[str] = "lulatex"
    PANDOC_PDF_ENGINE_XELATEX: ClassVar[str] = "xelatex"

    # ------------------------------------------------------------------
    # Initialise the instance.
    # ------------------------------------------------------------------
    def __init__(self) -> None:
        """Initialise the instance."""
        try:
            core_glob.logger.debug(core_glob.LOGGER_START)
        except AttributeError:
            core_glob.initialise_logger()
            core_glob.logger.debug(core_glob.LOGGER_START)

        self._document_id: int = 0

        self._full_name_in = ""
        self._full_name_in_directory = ""
        self._full_name_in_extension = ""
        self._full_name_in_extension_int = ""
        self._full_name_in_next_step = ""
        self._full_name_in_pandoc = ""
        self._full_name_in_parser = ""
        self._full_name_in_pdf2image = ""
        self._full_name_in_pdflib = ""
        self._full_name_in_stem_name = ""
        self._full_name_in_tesseract = ""
        self._full_name_in_tokenizer = ""
        self._full_name_orig = ""

        self._is_delete_auxiliary_files = False
        self._is_lt_footer_required = False
        self._is_lt_header_required = False
        self._is_lt_heading_required = False
        self._is_lt_list_bullet_required = False
        self._is_lt_list_number_required = False
        self._is_lt_table_required = False
        self._is_lt_toc_required = False
        self._is_pandoc = False
        self._is_pdf2image = False
        self._is_tesseract = False
        self._is_verbose = False

        self._language_pandoc: str = ""
        self._language_spacy: str = ""
        self._language_tesseract: str = ""

        self._no_lines_footer: int = 0
        self._no_lines_header: int = 0
        self._no_lines_toc: int = 0
        self._no_pdf_pages: int = 0

        self._exist = True

        core_glob.logger.debug(core_glob.LOGGER_END)

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
        core_glob.logger.debug(core_glob.LOGGER_START)

        if self._full_name_in_extension_int == core_glob.FILE_TYPE_PDF:
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
        elif self._full_name_in_extension_int in core_glob.FILE_TYPE_PANDOC:
            self._is_pandoc = True
            self._full_name_in_pandoc = self._full_name_in
        elif self._full_name_in_extension_int in core_glob.FILE_TYPE_TESSERACT:
            self._is_tesseract = True
            self._full_name_in_tesseract = self._full_name_in
        else:
            raise RuntimeError(Process.ERROR_01_901.replace("{extension}", self._full_name_in_extension_int))

        core_glob.logger.debug(core_glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Delete the given auxiliary file.
    # -----------------------------------------------------------------------------
    def _document_delete_auxiliary_file(self, full_name: str) -> None:
        """Delete the given auxiliary file.

        Args:
            full_name (str): File name.
        """
        if not self._is_delete_auxiliary_files:
            return

        # Don't remove the base document !!!
        if full_name == self._full_name_in:
            return

        if os.path.isfile(full_name):
            os.remove(full_name)
            core_utils.progress_msg(self._is_verbose, f"Auxiliary file '{full_name}' deleted")

    # ------------------------------------------------------------------
    # Initialize the document recognition process.
    # ------------------------------------------------------------------
    def _document_init(self) -> None:
        """Initialize the document recognition process."""
        core_glob.logger.debug(core_glob.LOGGER_START)

        self._document_id: int = 0

        self._full_name_in: str = ""
        self._full_name_in_directory: str = ""
        self._full_name_in_extension: str = ""
        self._full_name_in_extension_int: str = ""
        self._full_name_in_next_step: str = ""
        self._full_name_in_pandoc: str = ""
        self._full_name_in_parser: str = ""
        self._full_name_in_pdf2image: str = ""
        self._full_name_in_pdflib: str = ""
        self._full_name_in_stem_name: str = ""
        self._full_name_in_tesseract: str = ""
        self._full_name_in_tokenizer: str = ""
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

        core_glob.logger.debug(core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Convert the document to PDF format using Pandoc.
    # ------------------------------------------------------------------
    def _document_pandoc(self):
        """Convert the document to PDF format using Pandoc.

        Raises:
            RuntimeError: Any Pandoc issue.
        """
        if self._is_pandoc:
            core_glob.logger.debug(core_glob.LOGGER_START)

            core_utils.progress_msg(self._is_verbose, f"Start processing Pandoc        {self._full_name_in_pandoc}")

            self._full_name_in_pdflib = core_utils.get_full_name_from_components(
                self._full_name_in_directory, self._full_name_in_stem_name, core_glob.FILE_TYPE_PDF
            )

            return_code, error_msg = Process.pandoc(
                self._full_name_in_pandoc,
                self._full_name_in_pdflib,
                self._language_pandoc,
            )
            if return_code != "ok":
                raise RuntimeError(error_msg)

            self._document_delete_auxiliary_file(self._full_name_in_pandoc)

            core_utils.progress_msg(self._is_verbose, f"End   processing Pandoc        {self._full_name_in_pdflib}")

            core_glob.logger.debug(core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Extract the text for all granularities from the PDF document.
    # ------------------------------------------------------------------
    def _document_parser(self):
        """Extract the text for all granularities from the PDF document."""
        core_glob.logger.debug(core_glob.LOGGER_START)

        self._full_name_in_tokenizer = core_utils.get_full_name_from_components(
            self._full_name_in_directory,
            self._full_name_in_stem_name + "." + core_glob.FILE_TYPE_JSON,
        )

        return_code, error_msg = Process.parser(
            document_id=self._document_id,
            full_name_in=self._full_name_in_parser,
            full_name_orig=self._full_name_orig,
            full_name_out=self._full_name_in_tokenizer,
            is_lt_footer_required=self._is_lt_footer_required,
            is_lt_header_required=self._is_lt_header_required,
            is_lt_heading_required=self._is_lt_heading_required,
            is_lt_list_bullet_required=self._is_lt_list_bullet_required,
            is_lt_list_number_required=self._is_lt_list_number_required,
            is_lt_table_required=self._is_lt_table_required,
            is_lt_toc_required=self._is_lt_toc_required,
            no_pdf_pages=self._no_pdf_pages,
        )
        if return_code != "ok":
            raise RuntimeError(error_msg)

        self._document_delete_auxiliary_file(self._full_name_in_parser)

        if self._is_lt_footer_required or self._is_lt_header_required:
            self._no_lines_footer = core_glob.inst_lt_hf.no_lines_footer
            self._no_lines_header = core_glob.inst_lt_hf.no_lines_header

        if self._is_lt_toc_required:
            self._no_lines_toc = core_glob.inst_lt_toc.no_lines_toc

        core_glob.logger.debug(core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Convert the PDF document to an image file using pdf2image.
    # ------------------------------------------------------------------
    def _document_pdf2image(self):
        """Convert the PDF document to an image file using pdf2image.

        Raises:
            RuntimeError: Any pdf2image issue.
        """
        if self._is_pdf2image:
            core_glob.logger.debug(core_glob.LOGGER_START)

            core_utils.progress_msg(self._is_verbose, f"Start processing pdf2image     {self._full_name_in_pdf2image}")

            self._full_name_in_tesseract = core_utils.get_full_name_from_components(
                self._full_name_in_directory,
                self._full_name_in_stem_name
                + "_[0-9]*."
                + (
                    core_glob.FILE_TYPE_PNG
                    if core_glob.setup.pdf2image_type == setup.Setup.PDF2IMAGE_TYPE_PNG
                    else core_glob.FILE_TYPE_JPEG
                ),
            )

            return_code, error_msg, _ = Process.pdf2image(
                self._full_name_in_pdf2image,
            )
            if return_code != "ok":
                raise RuntimeError(error_msg)

            self._document_delete_auxiliary_file(self._full_name_in_pdf2image)

            core_utils.progress_msg(self._is_verbose, f"End   processing pdf2image     {self._full_name_in_tesseract}")

            core_glob.logger.debug(core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Extract the text and metadata from a PDF document to an XML file.
    # ------------------------------------------------------------------
    def _document_pdflib(self):
        """Extract the text and metadata from a PDF document to an XML file.

        Raises:
            RuntimeError: Any PDFlib TET issue.
        """
        core_glob.logger.debug(core_glob.LOGGER_START)

        core_utils.progress_msg(self._is_verbose, f"Start processing PDFlib TET    {self._full_name_in_pdflib}")

        # noinspection PyUnresolvedReferences
        self._no_pdf_pages = len(PyPDF2.PdfReader(self._full_name_in_pdflib).pages)
        if self._no_pdf_pages == 0:
            raise RuntimeError(f"The number of pages of the PDF document {self._full_name_in_pdflib} cannot be determined")

        self._full_name_in_parser = core_utils.get_full_name_from_components(
            self._full_name_in_directory,
            self._full_name_in_stem_name + "." + core_glob.FILE_TYPE_XML,
        )

        return_code, error_msg = Process.pdflib(
            full_name_in=self._full_name_in_pdflib,
            full_name_out=self._full_name_in_parser,
            document_opt_list=nlp_core.NLPCore.TET_DOCUMENT_OPT_LIST,
            page_opt_list=nlp_core.NLPCore.TET_PAGE_OPT_LIST,
        )
        if return_code != "ok":
            raise RuntimeError(error_msg)

        core_utils.progress_msg(self._is_verbose, f"End   processing PDFlib TET    {self._full_name_in_parser}")

        self._document_delete_auxiliary_file(self._full_name_in_pdflib)

        core_glob.logger.debug(core_glob.LOGGER_END)

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
            core_glob.logger.debug(core_glob.LOGGER_START)

            core_utils.progress_msg(self._is_verbose, f"Start processing Tesseract OCR {self._full_name_in_tesseract}")

            if self._is_pdf2image:
                self._full_name_in_stem_name += "_0"

            self._full_name_in_pdflib = core_utils.get_full_name_from_components(
                self._full_name_in_directory, self._full_name_in_stem_name, core_glob.FILE_TYPE_PDF
            )

            return_code, error_msg, children = Process.tesseract(
                self._full_name_in_tesseract,
                self._full_name_in_pdflib,
                self._language_tesseract,
            )
            if return_code != "ok":
                raise RuntimeError(error_msg)

            # noinspection PyUnresolvedReferences
            self._no_pdf_pages = len(PyPDF2.PdfReader(self._full_name_in_pdflib).pages)
            if self._no_pdf_pages == 0:
                raise RuntimeError(f"The number of pages of the PDF document {self._full_name_in_pdflib} cannot be determined")

            for child in children:
                self._document_delete_auxiliary_file(child)

            core_utils.progress_msg(self._is_verbose, f"End   processing Tesseract OCR {self._full_name_in_pdflib}")

            core_glob.logger.debug(core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Convert the PDF document to an image file using pdf2image.
    # ------------------------------------------------------------------
    def _document_tokenizer(self) -> None:
        """Tokenize the document with spaCy.

        Raises:
            RuntimeError: Any spaCy issue.
        """
        core_glob.logger.debug(core_glob.LOGGER_START)

        core_utils.progress_msg(self._is_verbose, f"Start processing spaCy         {self._full_name_in_tokenizer}")

        try:
            core_glob.tokenizer_spacy.exists()
        except AttributeError:
            core_glob.tokenizer_spacy = tokenizer.TokenizerSpacy()

        self._full_name_in_next_step = core_utils.get_full_name_from_components(
            self._full_name_in_directory,
            self._full_name_in_stem_name + ".token." + core_glob.FILE_TYPE_JSON,
        )

        return_code, error_msg = Process.tokenizer(
            full_name_in=self._full_name_in_tokenizer,
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

        self._document_delete_auxiliary_file(self._full_name_in_tokenizer)

        core_utils.progress_msg(self._is_verbose, f"End   processing spaCy         {self._full_name_in_next_step}")

        core_glob.logger.debug(core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Document content recognition for a specific file.
    # ------------------------------------------------------------------
    def document(  # pylint: disable=too-many-arguments
        self,
        full_name_in: str,
        document_id: int = None,
        full_name_orig: str = None,
        is_delete_auxiliary_files: bool = None,
        is_lt_footer_required: bool = None,
        is_lt_header_required: bool = None,
        is_lt_heading_required: bool = None,
        is_lt_list_bullet_required: bool = None,
        is_lt_list_number_required: bool = None,
        is_lt_table_required: bool = None,
        is_lt_toc_required: bool = None,
        is_verbose: bool = None,
        language_pandoc: str = None,
        language_spacy: str = None,
        language_tesseract: str = None,
        output_directory: str = None,
    ) -> None:
        """Document content recognition for a specific file.

        This method extracts the document content structure from a
        given document and stores it in JSON format. For this purpose,
        all non-pdf documents and all scanned pdf documents are first
        converted into a searchable pdf format. Depending on the file
        format, the tools Pandoc, pdf2image or Tesseract OCR are used
        for this purpose. PDFlib TET then extracts the text and metadata
        from the searchable pdf file and makes them available in XML format.
        spaCY generates qualified tokens from the document text, and these
        token data are then made available together with the metadata in a
        JSON format.

        Args:
            full_name_in (str):
                Full file name of the document file.
            document_id (int, optional):
                Document identification.
                Defaults to -1 i.e. no document identification.
            full_name_orig (str, optional):
                Original full file name.
                Defaults to the full file name of the document file.
            is_delete_auxiliary_files (bool, optional):
                Delete the auxiliary files after a successful processing step.
                Defaults to parameter `delete_auxiliary_files` in `setup.cfg`.
            is_lt_footer_required (bool, optional):
                If it is set to **`true`**, the determination of the footer lines is performed.
                Defaults to parameter `lt_footer_required` in `setup.cfg`.
            is_lt_header_required (bool, optional):
                If it is set to **`true`**, the determination of the header lines is performed.
                Defaults to parameter `lt_header_required` in `setup.cfg`.
            is_lt_heading_required (bool, optional):
                If it is set to **`true`**, the determination of the heading lines is performed.
                Defaults to parameter `lt_heading_required` in `setup.cfg`.
            is_lt_list_bullet_required (bool, optional):
                If it is set to **`true`**, the determination of the bulleted lists is performed.
                Defaults to parameter `lt_list_bullet_required` in `setup.cfg`.
            is_lt_list_number_required (bool, optional):
                If it is set to **`true`**, the determination of the numbered lists is performed.
                Defaults to parameter `lt_list_number_required` in `setup.cfg`.
            is_lt_table_required (bool, optional):
                If it is set to **`true`**, the determination of the table lines is performed.
                Defaults to parameter `lt_table_required` in `setup.cfg`.
            is_lt_toc_required (bool, optional):
                If it is set to **`true`**, the determination of the TOC lines is performed.
                Defaults to parameter `lt_toc_required` in `setup.cfg`.
            is_verbose (bool, optional):
                Display progress messages for processing.
                Defaults to parameter `verbose` in `setup.cfg`.
            language_pandoc (str, optional):
                Pandoc language code.
                Defaults to English.
            language_spacy (str, optional):
                spaCy language code.
                Defaults to English transformer pipeline (roberta-base)..
            language_tesseract (str, optional):
                Tesseract OCR language code.
                Defaults to English.
            output_directory (str, optional):
                Directory for the flat files to be created.
                Defaults to the directory of the document file.

        Raises:
            RuntimeError: Any issue from Pandoc, pdf2image, PDFlib TET, spaCy, or Tesseract OCR.
        """
        # Initialise the logging functionality.
        core_glob.initialise_logger()

        core_glob.logger.debug(core_glob.LOGGER_START)

        core_glob.logger.debug("param full_name_in              =%s", full_name_in)
        if document_id:
            core_glob.logger.debug("param document_id               =%i", document_id)

        self._document_init()

        self._document_id = document_id if document_id else -1
        self._full_name_in = full_name_in
        self._full_name_orig = full_name_orig if full_name_orig else full_name_in

        # Load the configuration parameters.
        core_glob.setup = setup.Setup()

        self._is_delete_auxiliary_files = (
            is_delete_auxiliary_files if is_delete_auxiliary_files is not None else core_glob.setup.is_delete_auxiliary_files
        )
        self._is_lt_footer_required = is_lt_footer_required if is_lt_footer_required is not None else core_glob.setup.is_lt_footer_required
        self._is_lt_header_required = is_lt_header_required if is_lt_header_required is not None else core_glob.setup.is_lt_header_required
        self._is_lt_heading_required = (
            is_lt_heading_required if is_lt_heading_required is not None else core_glob.setup.is_lt_heading_required
        )
        self._is_lt_list_bullet_required = (
            is_lt_list_bullet_required if is_lt_list_bullet_required is not None else core_glob.setup.is_lt_list_bullet_required
        )
        self._is_lt_list_number_required = (
            is_lt_list_number_required if is_lt_list_number_required is not None else core_glob.setup.is_lt_list_number_required
        )
        self._is_lt_table_required = is_lt_table_required if is_lt_table_required is not None else core_glob.setup.is_lt_table_required
        self._is_lt_toc_required = is_lt_toc_required if is_lt_toc_required is not None else core_glob.setup.is_lt_toc_required
        self._is_verbose = is_verbose if is_verbose is not None else core_glob.setup.is_verbose
        self._language_pandoc = language_pandoc if language_pandoc else nlp_core.NLPCore.LANGUAGE_PANDOC_DEFAULT
        self._language_spacy = language_spacy if language_spacy else nlp_core.NLPCore.LANGUAGE_SPACY_DEFAULT
        self._language_tesseract = language_tesseract if language_tesseract else nlp_core.NLPCore.LANGUAGE_TESSERACT_DEFAULT

        core_glob.logger.debug("param is_lt_footer_required     =%s", self._is_lt_footer_required)
        core_glob.logger.debug("param is_lt_header_required     =%s", self._is_lt_header_required)
        core_glob.logger.debug("param is_lt_heading_required    =%s", self._is_lt_heading_required)
        core_glob.logger.debug("param is_lt_list_bullet_required=%s", self._is_lt_list_bullet_required)
        core_glob.logger.debug("param is_lt_list_number_required=%s", self._is_lt_list_number_required)
        core_glob.logger.debug("param is_lt_table_required      =%s", self._is_lt_table_required)
        core_glob.logger.debug("param is_lt_toc_required        =%s", self._is_lt_toc_required)
        core_glob.logger.debug("param full_name_orig            =%s", self._full_name_orig)
        core_glob.logger.debug("param language_pandoc           =%s", self._language_pandoc)
        core_glob.logger.debug("param language_spacy            =%s", self._language_spacy)
        core_glob.logger.debug("param language_tesseract        =%s", self._language_tesseract)

        core_utils.progress_msg(self._is_verbose, f"Start processing document file {self._full_name_orig}")
        core_utils.progress_msg(self._is_verbose, f"Language key Pandoc            {self._language_pandoc}")
        core_utils.progress_msg(self._is_verbose, f"Language key spaCy             {self._language_spacy}")
        core_utils.progress_msg(self._is_verbose, f"Language key Tesseract OCR     {self._language_tesseract}")

        (
            full_name_in_directory,
            self._full_name_in_stem_name,
            self._full_name_in_extension,
        ) = core_utils.get_components_from_full_name(self._full_name_in)

        self._full_name_in_directory = output_directory if output_directory is not None else full_name_in_directory

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

        core_utils.progress_msg(self._is_verbose, f"End   processing document file {self._full_name_orig}")

        core_glob.logger.debug(core_glob.LOGGER_END)

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
            core_glob.logger.debug(core_glob.LOGGER_START)
        except AttributeError:
            core_glob.initialise_logger()
            core_glob.logger.debug(core_glob.LOGGER_START)

        core_glob.logger.debug("param full_name_in   =%s", full_name_in)
        core_glob.logger.debug("param full_name_out  =%s", full_name_out)
        core_glob.logger.debug("param language_pandoc=%s", language_pandoc)

        # Convert the document
        extra_args = [
            f"--pdf-engine={Process.PANDOC_PDF_ENGINE_XELATEX}",
            "-V",
            f"lang:{language_pandoc}",
        ]

        try:
            pypandoc.convert_file(
                full_name_in,
                core_glob.FILE_TYPE_PDF,
                extra_args=extra_args,
                outputfile=full_name_out,
            )

            if len(PyPDF2.PdfReader(full_name_out).pages) == 0:
                error_msg = Process.ERROR_31_911.replace("{full_name}", full_name_out)
                core_glob.logger.debug("return               =%s", (error_msg[:6], error_msg))
                core_glob.logger.debug(core_glob.LOGGER_END)
                return error_msg[:6], error_msg

        except FileNotFoundError:
            error_msg = Process.ERROR_31_902.replace("{full_name}", full_name_in)
            core_glob.logger.debug("return               =%s", (error_msg[:6], error_msg))
            core_glob.logger.debug(core_glob.LOGGER_END)
            return error_msg[:6], error_msg
        except RuntimeError as err:
            error_msg = Process.ERROR_31_903.replace("{full_name}", full_name_in).replace("{error_msg}", str(err))
            core_glob.logger.debug("return               =%s", (error_msg[:6], error_msg))
            core_glob.logger.debug(core_glob.LOGGER_END)
            return error_msg[:6], error_msg

        core_glob.logger.debug("return               =%s", core_glob.RETURN_OK)
        core_glob.logger.debug(core_glob.LOGGER_END)

        return core_glob.RETURN_OK

    # ------------------------------------------------------------------
    # Extracting the text from the PDF document.
    # ------------------------------------------------------------------
    @classmethod
    def parser(  # pylint: disable=too-many-arguments
        cls,
        full_name_in: str,
        full_name_out: str,
        no_pdf_pages: int,
        document_id: int = -1,
        full_name_orig: str = None,
        is_lt_footer_required: bool = False,
        is_lt_header_required: bool = False,
        is_lt_heading_required: bool = False,
        is_lt_list_bullet_required: bool = False,
        is_lt_list_number_required: bool = False,
        is_lt_table_required: bool = False,
        is_lt_toc_required: bool = False,
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
                Defaults to None.
            full_name_orig (str, optional):
                The file name of the originating document.
                Defaults to None.
            is_lt_footer_required (bool, optional):
                If it is set to **`true`**, the determination of the footer lines is performed.
                Defaults to False.
            is_lt_header_required (bool, optional):
                If it is set to **`true`**, the determination of the header lines is performed.
                Defaults to False.
            is_lt_heading_required (bool, optional):
                If it is set to **`true`**, the determination of the heading lines is performed.
                Defaults to False.
            is_lt_list_bullet_required (bool, optional):
                If it is set to **`true`**, the determination of the bulleted lists is performed.
                Defaults to False.
            is_lt_list_number_required (bool, optional):
                If it is set to **`true`**, the determination of the numbered lists is performed.
                Defaults to False.
            is_lt_table_required (bool, optional):
                If it is set to **`true`**, the determination of the table lines is performed.
                Defaults to False.
            is_lt_toc_required (bool, optional):
                If it is set to **`true`**, the determination of the TOC lines is performed.
                Defaults to False.

        Returns:
            tuple[str, str]:
                    ("ok", "") if the processing has been completed successfully,
                               otherwise a corresponding error code and error message.
        """
        try:
            core_glob.logger.debug(core_glob.LOGGER_START)
        except AttributeError:
            core_glob.initialise_logger()
            core_glob.logger.debug(core_glob.LOGGER_START)

        if document_id:
            core_glob.logger.debug("param document_id               =%i", document_id)
        core_glob.logger.debug("param full_name_in              =%s", full_name_in)
        if full_name_orig:
            core_glob.logger.debug("param full_name_orig            =%s", full_name_orig)
        core_glob.logger.debug("param full_name_out             =%s", full_name_out)
        core_glob.logger.debug("param is_lt_footer_required     =%s", is_lt_footer_required)
        core_glob.logger.debug("param is_lt_header_required     =%s", is_lt_header_required)
        core_glob.logger.debug("param is_lt_heading_required    =%s", is_lt_heading_required)
        core_glob.logger.debug("param is_lt_list_bullet_required=%s", is_lt_list_bullet_required)
        core_glob.logger.debug("param is_lt_list_number_required=%s", is_lt_list_number_required)
        core_glob.logger.debug("param is_lt_table_required      =%s", is_lt_table_required)
        core_glob.logger.debug("param is_lt_toc_required        =%s", is_lt_toc_required)
        core_glob.logger.debug("param no_pdf_pages              =%i", no_pdf_pages)

        try:
            # Create the Element tree object
            tree = defusedxml.ElementTree.parse(full_name_in)

            # Get the root Element
            root = tree.getroot()

            core_glob.text_parser = parser.TextParser()

            core_glob.text_parser.no_errors = 0

            for child in root:
                child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
                match child_tag:
                    case nlp_core.NLPCore.PARSE_ELEM_DOCUMENT:
                        core_glob.text_parser.parse_tag_document(
                            directory_name=os.path.dirname(full_name_in),
                            document_id=document_id,
                            environment_variant=core_glob.setup.environment_variant,
                            file_name_curr=os.path.basename(full_name_in),
                            file_name_next=full_name_out,
                            file_name_orig=full_name_orig,
                            is_lt_footer_required=is_lt_footer_required,
                            is_lt_header_required=is_lt_header_required,
                            is_lt_heading_required=is_lt_heading_required,
                            is_lt_list_bullet_required=is_lt_list_bullet_required,
                            is_lt_list_number_required=is_lt_list_number_required,
                            is_lt_table_required=is_lt_table_required,
                            is_lt_toc_required=is_lt_toc_required,
                            no_pdf_pages=no_pdf_pages,
                            parent=child,
                            parent_tag=child_tag,
                        )
                    case nlp_core.NLPCore.PARSE_ELEM_CREATION:
                        pass
                    case other:
                        core_utils.progress_msg_core(Process.ERROR_61_902.replace("{parent_tag}", "XML root").replace("{child_tag", other))
                        core_glob.text_parser.no_errors += 1

            if core_glob.text_parser.no_errors != 0:
                error_msg = Process.ERROR_61_903.replace("{no_errors}", str(core_glob.text_parser.no_errors))
                core_glob.logger.debug("return              =%s", (error_msg[:6], error_msg))
                core_glob.logger.debug(core_glob.LOGGER_END)
                return error_msg[:6], error_msg

        except FileNotFoundError:
            error_msg = Process.ERROR_61_901.replace("{full_name}", full_name_in)
            core_glob.logger.debug("return              =%s", (error_msg[:6], error_msg))
            core_glob.logger.debug(core_glob.LOGGER_END)
            return error_msg[:6], error_msg

        core_glob.logger.debug("return              =%s", core_glob.RETURN_OK)
        core_glob.logger.debug(core_glob.LOGGER_END)

        return core_glob.RETURN_OK

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
            core_glob.logger.debug(core_glob.LOGGER_START)
        except AttributeError:
            core_glob.initialise_logger()
            core_glob.logger.debug(core_glob.LOGGER_START)

        core_glob.logger.debug("param full_name_in=%s", full_name_in)

        try:
            images = pdf2image.convert_from_path(full_name_in)

            children: list[tuple[str, str]] = []
            no_children = 0

            directory_name = os.path.dirname(full_name_in)
            stem_name = os.path.splitext(os.path.basename(full_name_in))[0]

            try:
                os.remove(
                    core_utils.get_full_name_from_components(
                        directory_name,
                        stem_name
                        + "_*."
                        + (
                            core_glob.FILE_TYPE_PNG
                            if core_glob.setup.pdf2image_type == setup.Setup.PDF2IMAGE_TYPE_PNG
                            else core_glob.FILE_TYPE_JPEG
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
                        core_glob.FILE_TYPE_PNG
                        if core_glob.setup.pdf2image_type == setup.Setup.PDF2IMAGE_TYPE_PNG
                        else core_glob.FILE_TYPE_JPEG
                    )
                )

                full_name_next = core_utils.get_full_name_from_components(
                    directory_name,
                    file_name_next,
                )

                img.save(
                    full_name_next,
                    core_glob.setup.pdf2image_type,
                )

                children.append((file_name_next, full_name_next))
        except PDFPageCountError as err:
            error_msg = (
                Process.ERROR_21_901.replace("{full_name}", full_name_in)
                .replace("{error_type}", str(type(err)))
                .replace("{error_msg}", str(err))
            )
            core_glob.logger.debug("return            =%s", (error_msg[:6], error_msg, []))
            core_glob.logger.debug(core_glob.LOGGER_END)
            return error_msg[:6], error_msg, []

        core_glob.logger.debug("return            =%s", (core_glob.RETURN_OK[0], core_glob.RETURN_OK[1], children))
        core_glob.logger.debug(core_glob.LOGGER_END)

        return core_glob.RETURN_OK[0], core_glob.RETURN_OK[1], children

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
                Page level options.

        Returns:
            tuple[str, str]:
                ("ok", "") if the processing has been completed successfully,
                           otherwise a corresponding error code and error message.
        """
        try:
            core_glob.logger.debug(core_glob.LOGGER_START)
        except AttributeError:
            core_glob.initialise_logger()
            core_glob.logger.debug(core_glob.LOGGER_START)

        core_glob.logger.debug("param full_name_in     =%s", full_name_in)
        core_glob.logger.debug("param full_name_out    =%s", full_name_out)
        core_glob.logger.debug("param document_opt_list=%s", document_opt_list)
        core_glob.logger.debug("param page_opt_list    =%s", page_opt_list)

        tet = TET.TET()

        doc_opt_list = f"tetml={{filename={{{full_name_out}}}}} {document_opt_list}"

        if (file_curr := tet.open_document(full_name_in, doc_opt_list)) == -1:
            error_msg = (
                Process.ERROR_51_901.replace("{full_name}", full_name_in)
                .replace("{error_no}", str(tet.get_errnum()))
                .replace("{api_name}", tet.get_apiname() + "()")
                .replace("{error_msg}", tet.get_errmsg())
            )
            core_glob.logger.debug("return                 =%s", (error_msg[:6], error_msg))
            core_glob.logger.debug(core_glob.LOGGER_END)
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

        core_glob.logger.debug("return                 =%s", core_glob.LOGGER_END)
        core_glob.logger.debug(core_glob.LOGGER_END)

        return core_glob.RETURN_OK

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
            core_glob.logger.debug(core_glob.LOGGER_START)
        except AttributeError:
            core_glob.initialise_logger()
            core_glob.logger.debug(core_glob.LOGGER_START)

        core_glob.logger.debug("param full_name_in      =%s", full_name_in)
        core_glob.logger.debug("param full_name_out     =%s", full_name_out)
        core_glob.logger.debug("param language_tesseract=%s", language_tesseract)

        children: list[str] = []

        pdf_writer = PyPDF2.PdfWriter()

        for full_name in sorted(glob.glob(full_name_in)):
            try:
                pdf = pytesseract.image_to_pdf_or_hocr(
                    extension="pdf",
                    image=full_name,
                    lang=language_tesseract,
                    timeout=core_glob.setup.tesseract_timeout,
                )

                with open(full_name_out, "w+b") as file_handle:
                    # PDF type is bytes by default
                    file_handle.write(pdf)

                if len(PyPDF2.PdfReader(full_name_out).pages) == 0:
                    error_msg = Process.ERROR_41_911.replace("{full_name_out}", full_name_out)
                    core_glob.logger.debug("return                  =%s", (error_msg[:6], error_msg, []))
                    core_glob.logger.debug(core_glob.LOGGER_END)
                    return error_msg[:6], error_msg, []

                pdf_reader = PyPDF2.PdfReader(full_name_out)

                for page in pdf_reader.pages:
                    # Add each page to the writer object
                    pdf_writer.add_page(page)

                children.append(full_name)

            except RuntimeError as err:
                error_msg = Process.ERROR_41_901.replace("{full_name}", full_name_in).replace("{error_msg}", str(err))
                core_glob.logger.debug("return                  =%s", (error_msg[:6], error_msg, []))
                core_glob.logger.debug(core_glob.LOGGER_END)
                return error_msg[:6], error_msg, []

        # Write out the merged PDF
        with open(full_name_out, "wb") as file_handle:
            pdf_writer.write(file_handle)

        core_glob.logger.debug("return                  =%s", (core_glob.RETURN_OK[0], core_glob.RETURN_OK[1], children))
        core_glob.logger.debug(core_glob.LOGGER_END)

        return core_glob.RETURN_OK[0], core_glob.RETURN_OK[1], children

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
            core_glob.logger.debug(core_glob.LOGGER_START)
        except AttributeError:
            core_glob.initialise_logger()
            core_glob.logger.debug(core_glob.LOGGER_START)

        core_glob.logger.debug("param document_id    =%i", document_id)
        core_glob.logger.debug("param full_name_in   =%s", full_name_in)
        core_glob.logger.debug("param full_name_orig =%s", full_name_orig)
        core_glob.logger.debug("param full_name_out  =%s", full_name_out)
        core_glob.logger.debug("param no_lines_footer=%i", no_lines_footer)
        core_glob.logger.debug("param no_lines_header=%i", no_lines_header)
        core_glob.logger.debug("param no_lines_toc   =%i", no_lines_toc)
        core_glob.logger.debug("param pipeline_name  =%s", pipeline_name)

        try:
            core_glob.tokenizer_spacy.process_document(
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
            core_glob.logger.debug("return               =%s", (error_msg[:6], error_msg))
            core_glob.logger.debug(core_glob.LOGGER_END)
            return error_msg[:6], error_msg

        core_glob.logger.debug("return               =%s", core_glob.RETURN_OK)
        core_glob.logger.debug(core_glob.LOGGER_END)

        return core_glob.RETURN_OK
