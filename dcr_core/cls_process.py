# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Main processing."""

import glob
import os.path

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
import PDFlib.TET


# pylint: disable=too-many-instance-attributes
class Process:
    """Process utility class.

    Returns:
        _type_: Process instance.
    """

    # ------------------------------------------------------------------
    # Class variables.
    # ------------------------------------------------------------------
    ERROR_01_901 = "01.901 Issue (p_i): Document rejected because of unknown file extension='{extension}'."
    ERROR_01_903 = "01.903 Issue (p_i): Runtime error with fitz.open() processing of file '{file_name}' " + "- error: '{error_msg}'."

    ERROR_21_901 = (
        "21.901 Issue (p_2_i): Processing file '{full_name}' with pdf2image failed - " + "error type: '{error_type}' - error: '{error}'."
    )
    ERROR_31_902 = (
        "31.902 Issue (n_2_p): The file '{full_name}' cannot be converted to an "
        + "'pdf' document - "
        + "error type: '{error_type}' - error: '{error_msg}'."
    )
    ERROR_41_901 = (
        "41.901 Issue (ocr): Converting the file '{full_name}' with Tesseract OCR failed - "
        + "error type: '{error_type}' - error: '{error}'."
    )
    ERROR_51_901 = (
        "51.901 Issue (tet): Opening document '{full_name}' - " + "error no: '{error_no}' - api: '{api_name}' - error: '{error}'."
    )
    ERROR_61_901 = "61.901 Issue (s_p_j): Parsing the file '{full_name}' failed - " + "error type: '{error_type}' - error: '{error}'."
    ERROR_71_901 = "71.901 Issue (tkn): Tokenizing the file '{full_name}' failed - " + "error type: '{error_type}' - error: '{error}'."

    PANDOC_PDF_ENGINE_LULATEX = "lulatex"
    PANDOC_PDF_ENGINE_XELATEX = "xelatex"

    # ------------------------------------------------------------------
    # Initialise the instance.
    # ------------------------------------------------------------------
    def __init__(self) -> None:
        """Initialise the instance."""
        self._full_name_in: str = ""
        self._full_name_in_directory: str = ""
        self._full_name_in_extension: str = ""
        self._full_name_in_extension_int: str = ""
        self._full_name_in_parser_line: str = ""
        self._full_name_in_parser_page: str = ""
        self._full_name_in_parser_word: str = ""
        self._full_name_in_pdf2image: str = ""
        self._full_name_in_pdflib: str = ""
        self._full_name_in_stem_name: str = ""
        self._full_names_in_tesseract: list[str] = []

        self._is_process_pandoc: bool = False
        self._is_process_pdf2image: bool = False
        self._is_process_tesseract: bool = False

        self._language_pandoc: str = ""
        self._language_tesseract: str = ""

        self._exist = True

    def _file_process_check_extension(self):
        if self._full_name_in_extension_int == dcr_core.core_glob.FILE_TYPE_PDF:
            try:
                if bool("".join([page.get_text() for page in fitz.open(self._full_name_in)])):
                    self._full_name_in_pdflib = self._full_name_in
                else:
                    self._is_process_pdf2image = True
                    self._full_name_in_pdf2image = self._full_name_in
            except RuntimeError as exc:
                raise RuntimeError(
                    Process.ERROR_01_903.replace("{file_name}", self._full_name_in).replace("{error_msg}", str(exc)),
                ) from exc
        elif self._full_name_in_extension_int in dcr_core.core_glob.FILE_TYPE_PANDOC:
            self._is_process_pandoc = True
            self._full_name_in_pandoc = self._full_name_in
        elif self._full_name_in_extension_int in dcr_core.core_glob.FILE_TYPE_TESSERACT:
            self._is_process_tesseract = True
            self._full_names_in_tesseract.append(self._full_name_in)
        else:
            raise RuntimeError(Process.ERROR_01_901.replace("{extension}", self._full_name_in_extension_int))

    # ------------------------------------------------------------------
    # Initialize the document recognition process.
    # ------------------------------------------------------------------
    def _file_process_init(self) -> None:
        """Initialize the document recognition process."""
        self._full_name_in: str = ""
        self._full_name_in_directory: str = ""
        self._full_name_in_extension: str = ""
        self._full_name_in_extension_int: str = ""
        self._full_name_in_parser_line: str = ""
        self._full_name_in_parser_page: str = ""
        self._full_name_in_parser_word: str = ""
        self._full_name_in_pdf2image: str = ""
        self._full_name_in_pdflib: str = ""
        self._full_name_in_stem_name: str = ""
        self._full_names_in_tesseract: list[str] = []

        self._is_process_pandoc: bool = False
        self._is_process_pdf2image: bool = False
        self._is_process_tesseract: bool = False

        self._language_pandoc: str = ""
        self._language_tesseract: str = ""

    # ------------------------------------------------------------------
    # Convert the document to pdf format using Pandoc.
    # ------------------------------------------------------------------
    def _file_process_pandoc(self):
        """Convert the document to pdf format using Pandoc."""
        if self._is_process_pandoc:
            self._full_name_in_pdflib = dcr_core.core_utils.get_full_name_from_components(
                self._full_name_in_directory, self._full_name_in_stem_name, dcr_core.core_glob.FILE_TYPE_PDF
            )
            return_code, error_msg = Process.pandoc_process(
                self._full_name_in_pandoc,
                self._full_name_in_pdflib,
                self._language_pandoc,
            )
            if return_code != "ok":
                raise RuntimeError(error_msg)

    # ------------------------------------------------------------------
    # Convert the pdf document to an image file using pdf2image.
    # ------------------------------------------------------------------
    def _file_process_parser(self):
        self._full_name_in_tokenizer_line = dcr_core.core_utils.get_full_name_from_components(
            self._full_name_in_directory, self._full_name_in_stem_name + "_line", dcr_core.core_glob.FILE_TYPE_JSON
        )
        return_code, error_msg = Process.parser_process(
            self._full_name_in_parser_line,
            self._full_name_in_tokenizer_line,
            self._language_tesseract,
        )
        if return_code != "ok":
            raise RuntimeError(error_msg)

    # ------------------------------------------------------------------
    # Convert the pdf document to an image file using pdf2image.
    # ------------------------------------------------------------------
    def _file_process_pdf2image(self):
        """Convert the pdf document to an image file using pdf2image."""
        if self._is_process_pdf2image:
            return_code, error_msg, self._full_names_out_pdf2image = Process.pdf2image_process(
                self._full_name_in_pdf2image,
            )
            if return_code != "ok":
                raise RuntimeError(error_msg)

    # ------------------------------------------------------------------
    # Convert the pdf document to an image file using pdf2image.
    # ------------------------------------------------------------------
    def _file_process_pdflib(self):
        self._full_name_in_parser_line = dcr_core.core_utils.get_full_name_from_components(
            self._full_name_in_directory,
            self._full_name_in_stem_name + "_" + dcr_core.cls_nlp_core.NLPCore.LINE_XML_VARIATION + dcr_core.core_glob.FILE_TYPE_XML,
        )
        return_code, error_msg = Process.pdflib_process(
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
                self._full_name_in_stem_name + "_" + dcr_core.cls_nlp_core.NLPCore.PAGE_XML_VARIATION + dcr_core.core_glob.FILE_TYPE_XML,
            )
            return_code, error_msg = Process.pdflib_process(
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
                self._full_name_in_stem_name + "_" + dcr_core.cls_nlp_core.NLPCore.WORD_XML_VARIATION + dcr_core.core_glob.FILE_TYPE_XML,
            )
            return_code, error_msg = Process.pdflib_process(
                full_name_in=self._full_name_in_pdflib,
                full_name_out=self._full_name_in_parser_word,
                document_opt_list=dcr_core.cls_nlp_core.NLPCore.WORD_TET_DOCUMENT_OPT_LIST,
                page_opt_list=dcr_core.cls_nlp_core.NLPCore.WORD_TET_PAGE_OPT_LIST,
            )
            if return_code != "ok":
                raise RuntimeError(error_msg)

    # ------------------------------------------------------------------
    # Convert the image file to a pdf file using Tesseract OCR.
    # ------------------------------------------------------------------
    def _file_process_tesseract(self):
        """Convert the image file to a pdf file using Tesseract OCR."""
        if self._is_process_tesseract:
            self._full_name_in_pdflib = dcr_core.core_utils.get_full_name_from_components(
                self._full_name_in_directory, self._full_name_in_stem_name, dcr_core.core_glob.FILE_TYPE_PDF
            )
            return_code, error_msg, _children = Process.tesseract_process(
                self._full_names_in_tesseract,
                self._full_name_in_pdflib,
                self._language_tesseract,
            )
            if return_code != "ok":
                raise RuntimeError(error_msg)

    # ------------------------------------------------------------------
    # Convert the pdf document to an image file using pdf2image.
    # ------------------------------------------------------------------
    def _file_process_tokenizer(self):
        self._full_name_in_next_step = dcr_core.core_utils.get_full_name_from_components(
            self._full_name_in_directory, self._full_name_in_stem_name, dcr_core.core_glob.FILE_TYPE_PDF
        )
        return_code, error_msg = Process.tokenizer_process(
            self._full_name_in_tokenizer_line,
            self._full_name_in_next_step,
            self._language_tesseract,
        )
        if return_code != "ok":
            raise RuntimeError(error_msg)

    # ------------------------------------------------------------------
    # Document content recognition for a specific file.
    # ------------------------------------------------------------------
    def document_process(
        self,
        full_name_in: str,
        language_pandoc: str = "",
        language_tesseract: str = "",
    ) -> None:
        """Document content recognition for a specific file.

        Args:
            full_name_in (str):
                Full file name of the document file.
            language_pandoc (str, optional):
                Pandoc language code. Defaults to "".
            language_tesseract (str, optional):
                Tesseract OCR language code. Defaults to "".

        Raises:
            RuntimeError: _description_
        """
        # Initialise the logging functionality.
        dcr_core.core_glob.initialise_logger()

        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)
        dcr_core.core_glob.logger.debug("param full_name_in      =%s", full_name_in)
        dcr_core.core_glob.logger.debug("param language_pandoc   =%s", language_pandoc)
        dcr_core.core_glob.logger.debug("param language_tesseract=%s", language_tesseract)

        self._file_process_init()

        self._full_name_in = full_name_in
        self._language_pandoc = language_pandoc
        self._language_tesseract = language_tesseract

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

        self._file_process_check_extension()

        self._file_process_pandoc()

        self._file_process_pdf2image()

        self._file_process_tesseract()

        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Converting a Non-PDF file to a PDF file.
    # ------------------------------------------------------------------
    @classmethod
    def pandoc_process(
        cls,
        full_name_in: str,
        full_name_out: str,
        language_pandoc: str,
    ) -> tuple[str, str]:
        """Convert a Non-PDF file to a PDF file.

        The following file formats are converted into
        PDF format here with the help of Pandoc:

        - csv  comma-separated values
        - docx Office Open XML
        - epub e-book file format
        - html HyperText Markup Language
        - odt  Open Document Format for Office Applications
        - rst  reStructuredText (RST
        - rtf  Rich Text Format

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

        except (FileNotFoundError, RuntimeError) as err:
            error_msg = (
                Process.ERROR_31_902.replace("{full_name}", full_name_in)
                .replace("{error_type}", str(type(err)))
                .replace("{error}", str(err))
            )
            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)
            return error_msg[:6], error_msg

        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

        return dcr_core.core_glob.RETURN_OK

    # ------------------------------------------------------------------
    # Extracting the text from the PDF document.
    # ------------------------------------------------------------------
    @classmethod
    def parser_process(
        cls,
        full_name_in: str,
        full_name_out: str,
        no_pdf_pages: int,
        document_id: int = -1,
        file_name_orig: str = dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE,
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
            file_name_orig (str, optional):
                    The file name of the originating document.
                    Defaults to dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE.

        Returns:
            tuple[str, str]:
                    ("ok", "") if the processing has been completed successfully,
                               otherwise a corresponding error code and error message.
        """
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)
        dcr_core.core_glob.logger.debug("param document_id   =%i", document_id)
        dcr_core.core_glob.logger.debug("param file_name_orig=%s", file_name_orig)
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
                            file_name_orig=file_name_orig,
                            no_pdf_pages=no_pdf_pages,
                            parent=child,
                            parent_tag=child_tag,
                        )
                    case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_CREATION:
                        pass
        except FileNotFoundError as err:
            error_msg = (
                Process.ERROR_61_901.replace("{full_name}", full_name_in)
                .replace("{error_type}", str(type(err)))
                .replace("{error}", str(err))
            )
            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)
            return error_msg[:6], error_msg

        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

        return dcr_core.core_glob.RETURN_OK

    # ------------------------------------------------------------------
    # Converting a scanned PDF file to a set of image files.
    # ------------------------------------------------------------------
    @classmethod
    def pdf2image_process(
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
                .replace("{error}", str(err))
            )
            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)
            return error_msg[:6], error_msg, []

        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

        return dcr_core.core_glob.RETURN_OK[0], dcr_core.core_glob.RETURN_OK[1], children

    # ------------------------------------------------------------------
    # Processing a PDF file with PDFlib TET.
    # ------------------------------------------------------------------
    @classmethod
    def pdflib_process(
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
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)
        dcr_core.core_glob.logger.debug("param full_name_in     =%s", full_name_in)
        dcr_core.core_glob.logger.debug("param full_name_out    =%s", full_name_out)
        dcr_core.core_glob.logger.debug("param document_opt_list=%s", document_opt_list)
        dcr_core.core_glob.logger.debug("param page_opt_list    =%s", page_opt_list)

        tet = PDFlib.TET.TET()

        doc_opt_list = f"tetml={{filename={{{full_name_out}}}}} {document_opt_list}"

        if (file_curr := tet.open_document(full_name_in, doc_opt_list)) == -1:
            error_msg = (
                Process.ERROR_51_901.replace("{full_name}", full_name_in)
                .replace("{error_no}", str(tet.get_errnum()))
                .replace("{api_name}", tet.get_apiname() + "()")
                .replace("{error}", tet.get_errmsg())
            )
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

        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

        return dcr_core.core_glob.RETURN_OK

    # ------------------------------------------------------------------
    # Converting image files to PDF files via OCR.
    # ------------------------------------------------------------------
    @classmethod
    def tesseract_process(
        cls,
        full_name_in: str,
        full_name_out: str,
        language_tesseract: str,
    ) -> tuple[str, str, list[str]]:
        """Convert image files to PDF files via OCR.

        The documents of the following document types are converted
        to the pdf format using Tesseract OCR:

        - bmp  - bitmap image file
        - gif  - Graphics Interchange Format
        - jp2  - JPEG 2000
        - jpeg - Joint Photographic Experts Group
        - png  - Portable Network Graphics
        - pnm  - portable any-map format
        - tif  - Tag Image File Format
        - tiff - Tag Image File Format
        - webp - Image file format with lossless and lossy compression

        After processing with Tesseract OCR, the files split previously
        into multiple image files are combined into a single pdf document.

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
                    # pdf type is bytes by default
                    file_handle.write(pdf)

                pdf_reader = PyPDF2.PdfReader(full_name_out)

                for page in pdf_reader.pages:
                    # Add each page to the writer object
                    pdf_writer.add_page(page)

                children.append(full_name)

            except RuntimeError as err:
                error_msg = (
                    Process.ERROR_41_901.replace("{full_name}", full_name_in)
                    .replace("{error_type}", str(type(err)))
                    .replace("{error}", str(err))
                )
                dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)
                return error_msg[:6], error_msg, []

        # Write out the merged PDF
        with open(full_name_out, "wb") as file_handle:
            pdf_writer.write(file_handle)

        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

        return dcr_core.core_glob.RETURN_OK[0], dcr_core.core_glob.RETURN_OK[1], children

    # ------------------------------------------------------------------
    # Tokenizing the text from the PDF document.
    # ------------------------------------------------------------------
    @classmethod
    def tokenizer_process(
        cls,
        full_name_in: str,
        full_name_out: str,
        pipeline_name: str,
        document_id: int = -1,
        file_name_orig: str = dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE,
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
            file_name_orig (str, optional):
                    The file name of the originating document.
                    Defaults to dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE.
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
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)
        dcr_core.core_glob.logger.debug("param document_id    =%i", document_id)
        dcr_core.core_glob.logger.debug("param file_name_orig =%s", file_name_orig)
        dcr_core.core_glob.logger.debug("param full_name_in   =%s", full_name_in)
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
                file_name_orig=file_name_orig,
                no_lines_footer=no_lines_footer,
                no_lines_header=no_lines_header,
                no_lines_toc=no_lines_toc,
                pipeline_name=pipeline_name,
            )

        except FileNotFoundError as err:
            error_msg = (
                Process.ERROR_71_901.replace("{full_name}", full_name_in)
                .replace("{error_type}", str(type(err)))
                .replace("{error}", str(err))
            )
            dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)
            return error_msg[:6], error_msg

        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

        return dcr_core.core_glob.RETURN_OK