# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Extract text and metadata from PDFlib TET.

Typical usage example:

    my_instance = TextParser()

    my_instance.process_document(parse_line_pages_json = my_pages,
                                 file_name_curr = my_file)
"""
from __future__ import annotations

import collections.abc
import json
from datetime import datetime

import dcr_core.cls_line_type_header_footer as lt_hf
import dcr_core.cls_line_type_heading as lt_h
import dcr_core.cls_line_type_list_bullet as lt_lb
import dcr_core.cls_line_type_list_number as lt_ln
import dcr_core.cls_line_type_toc as lt_toc
import dcr_core.cls_nlp_core as nlp_core
from dcr_core import core_glob
from dcr_core import core_utils


# pylint: disable=too-many-instance-attributes
class TextParser:
    """Extract text and metadata from PDFlib TET."""

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

        core_utils.check_exists_object(
            is_setup=True,
        )

        self._directory_name = ""
        self._document_id = 0
        self._environment_variant = ""
        self._file_name_curr = ""
        self._file_name_orig = ""
        self._full_name = ""
        self._is_line_processing = False
        self._is_lt_footer_required = False
        self._is_lt_header_required = False
        self._is_lt_heading_required = False
        self._is_lt_list_bullet_required = False
        self._is_lt_list_number_required = False
        self._is_lt_toc_required = False
        self._is_word_processing = False
        self._no_pdf_pages = 0

        self._parse_result_container_fonts: list[nlp_core.NLPCore.FontJSON] = []
        self._parse_result_container_lines: list[nlp_core.NLPCore.LineJSON] = []
        self._parse_result_container_pages: list[nlp_core.NLPCore.PageJSON] = []
        self._parse_result_container_paras: list[nlp_core.NLPCore.ParaJSON] = []
        self._parse_result_container_words: list[nlp_core.NLPCore.WordJSON] = []
        self._parse_result_font = ""
        self._parse_result_glyph_is_empty = False
        self._parse_result_index_page = 0
        self._parse_result_line_idx = 0
        self._parse_result_line_word_no_first = 0
        self._parse_result_line_word_no_last = 0
        self._parse_result_llx: float = 0.0
        self._parse_result_no_cells_row = 0
        self._parse_result_no_fonts = 0
        self._parse_result_no_lines_line = 0
        self._parse_result_no_lines_page = 0
        self._parse_result_no_lines_para = 0
        self._parse_result_no_lines_word = 0
        self._parse_result_no_paras = 0
        self._parse_result_no_rows_table = 0
        self._parse_result_no_paras_page = 0
        self._parse_result_no_tables = 0
        self._parse_result_no_titles = 0
        self._parse_result_no_words = 0
        self._parse_result_no_words_line = 0
        self._parse_result_no_words_page = 0
        self._parse_result_no_words_para = 0
        self._parse_result_page_idx = 0
        self._parse_result_page_line_no_first = 0
        self._parse_result_page_line_no_last = 0
        self._parse_result_page_para_no_first = 0
        self._parse_result_page_para_no_last = 0
        self._parse_result_page_word_no_first = 0
        self._parse_result_page_word_no_last = 0
        self._parse_result_para_line_no_first = 0
        self._parse_result_para_line_no_last = 0
        self._parse_result_para_word_no_first = 0
        self._parse_result_para_word_no_last = 0
        self._parse_result_size = 0.00
        self._parse_result_table = False
        self._parse_result_table_cell_is_empty = False
        self._parse_result_table_cell_span = 0
        self._parse_result_table_cell_span_prev = 0
        self._parse_result_text = ""
        self._parse_result_urx = 0.0

        self.no_errors = 0

        self.parse_result_no_pages = 0

        core_glob.inst_nlp_core = nlp_core.NLPCore()

        self._exist = True

        core_glob.logger.debug(core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Create the container 'params'.
    # ------------------------------------------------------------------
    def _create_params(self) -> nlp_core.ParamsJSON:
        """Create the container 'params'.

        Returns:
            nlp_core.ParamsJSON:
                Container 'params'.
        """
        params = {
            nlp_core.NLPCore.JSON_NAME_DIRECTORY_NAME: self._directory_name,
        }

        if self._document_id > 0:
            params[nlp_core.NLPCore.JSON_NAME_DOCUMENT_ID] = self._document_id

        params[nlp_core.NLPCore.JSON_NAME_ENVIRONMENT_VARIANT] = self._environment_variant
        params[nlp_core.NLPCore.JSON_NAME_FILE_NAME_CURR] = self._file_name_curr
        params[nlp_core.NLPCore.JSON_NAME_FILE_NAME_NEXT] = self._full_name
        params[nlp_core.NLPCore.JSON_NAME_FILE_NAME_ORIG] = self._file_name_orig
        params[nlp_core.NLPCore.JSON_NAME_LINE_TYPE_FOOTER_REQUIRED] = self._is_lt_footer_required
        params[nlp_core.NLPCore.JSON_NAME_LINE_TYPE_HEADER_REQUIRED] = self._is_lt_header_required
        params[nlp_core.NLPCore.JSON_NAME_LINE_TYPE_HEADING_REQUIRED] = self._is_lt_heading_required
        params[nlp_core.NLPCore.JSON_NAME_LINE_TYPE_LIST_BULLET_REQUIRED] = self._is_lt_list_bullet_required
        params[nlp_core.NLPCore.JSON_NAME_LINE_TYPE_LIST_NUMBER_REQUIRED] = self._is_lt_list_number_required
        params[nlp_core.NLPCore.JSON_NAME_LINE_TYPE_TOC_REQUIRED] = self._is_lt_toc_required

        return params

    # ------------------------------------------------------------------
    # Debug an XML element detailed.
    # ------------------------------------------------------------------
    @staticmethod
    def _debug_xml_element_all(event: str, parent_tag: str, attrib: dict[str, str], text: collections.abc.Iterable[str | None]) -> None:
        """Debug an XML element detailed.

        Args:
            event (str): Event: 'start' or 'end'.
            parent_tag (str): Parent tag.
            attrib (dict[str,str]): Attributes.
            text (collections.abc.Iterable[str|None]): XML element.
        """
        if core_glob.inst_setup.verbose_parser == "all":
            print(f"{event} tag   ={parent_tag}")

            if attrib != {}:
                print(f"      attrib={attrib}")

            if text is not None and str(text).strip() > "":
                print(f"      text  ='{text}'")

    # ------------------------------------------------------------------
    # Debug an XML element only 'text'.
    # ------------------------------------------------------------------
    def _debug_xml_element_text(self) -> None:
        """Debug an XML element only 'text - variant word."""
        if core_glob.inst_setup.verbose_parser == "text":
            print(
                f"document: pages={self.parse_result_no_pages:2d} "
                f"paras={self._parse_result_no_paras:2d} "
                f"lines={self._parse_result_no_lines_word:2d} "
                f"words={self._parse_result_no_words:2d} "
                f"page: paras={self._parse_result_no_paras_page:2d} "
                f"lines={self._parse_result_no_lines_page:2d} "
                f"words={self._parse_result_no_words_page:2d} "
                f"para: lines={self._parse_result_no_lines_para:2d} "
                f"words={self._parse_result_no_words_para:2d} "
                f"line: words={self._parse_result_no_words_line:2d} "
                f"text='{self._parse_result_text}'"
            )

    # ------------------------------------------------------------------
    # Determine the line types.
    # ------------------------------------------------------------------
    def _determine_line_types(self) -> None:
        """Determine the line types."""
        # ------------------------------------------------------------------
        # Line types footer and header.
        # ------------------------------------------------------------------
        if self._is_lt_footer_required or self._is_lt_header_required:
            core_glob.inst_lt_hf = lt_hf.LineTypeHeaderFooter(
                file_name_curr=self._file_name_curr,
            )
            core_glob.inst_lt_hf.process_document(
                file_name_curr=self._file_name_curr,
            )
            if self._is_lt_footer_required:
                core_glob.nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_LINES_FOOTER] = core_glob.inst_lt_hf.no_lines_footer
            if self._is_lt_header_required:
                core_glob.nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_LINES_HEADER] = core_glob.inst_lt_hf.no_lines_header

        # ------------------------------------------------------------------
        # Line type toc.
        # ------------------------------------------------------------------
        if self._is_lt_toc_required:
            core_glob.inst_lt_toc = lt_toc.LineTypeToc(
                file_name_curr=self._file_name_curr,
            )
            core_glob.inst_lt_toc.process_document(
                file_name_curr=self._file_name_curr,
            )
            core_glob.nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_LINES_TOC] = core_glob.inst_lt_toc.no_lines_toc

        # ------------------------------------------------------------------
        # Line type bulleted list.
        # ------------------------------------------------------------------
        if self._is_lt_list_bullet_required:
            core_glob.inst_lt_lb = lt_lb.LineTypeListBullet(
                file_name_curr=self._file_name_curr,
            )
            core_glob.inst_lt_lb.process_document(
                directory_name=self._directory_name,
                document_id=self._document_id,
                environment_variant=self._environment_variant,
                file_name_curr=self._file_name_curr,
                file_name_orig=self._file_name_orig,
            )
            core_glob.nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_LISTS_BULLET] = core_glob.inst_lt_lb.no_lists

        # ------------------------------------------------------------------
        # Line type numbered list.
        # ------------------------------------------------------------------
        if self._is_lt_list_number_required:
            core_glob.inst_lt_ln = lt_ln.LineTypeListNumber(
                file_name_curr=self._file_name_curr,
            )
            core_glob.inst_lt_ln.process_document(
                directory_name=self._directory_name,
                document_id=self._document_id,
                environment_variant=self._environment_variant,
                file_name_curr=self._file_name_curr,
                file_name_orig=self._file_name_orig,
            )
            core_glob.nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_LISTS_NUMBER] = core_glob.inst_lt_ln.no_lists

        # ------------------------------------------------------------------
        # Line type heading.
        # ------------------------------------------------------------------
        if self._is_lt_heading_required:
            core_glob.inst_lt_h = lt_h.LineTypeHeading(
                file_name_curr=self._file_name_curr,
            )
            core_glob.inst_lt_h.process_document(
                directory_name=self._directory_name,
                document_id=self._document_id,
                file_name_curr=self._file_name_curr,
                file_name_orig=self._file_name_orig,
            )

    # ------------------------------------------------------------------
    # Processing tag Bookmark.
    # ------------------------------------------------------------------
    def _parse_tag_bookmark(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Bookmark'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case (nlp_core.NLPCore.PARSE_ELEM_ACTION | nlp_core.NLPCore.PARSE_ELEM_TITLE):
                    pass
                case nlp_core.NLPCore.PARSE_ELEM_BOOKMARK:
                    self._parse_tag_bookmark(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_BOOKMARK).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag Bookmarks.
    # ------------------------------------------------------------------
    def _parse_tag_bookmarks(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Bookmarks'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case nlp_core.NLPCore.PARSE_ELEM_BOOKMARK:
                    self._parse_tag_bookmark(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_BOOKMARKS).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag Box with granularity 'line'.
    # ------------------------------------------------------------------
    def _parse_tag_box_line(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Box' with granularity 'line'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case (nlp_core.NLPCore.PARSE_ELEM_A | nlp_core.NLPCore.PARSE_ELEM_GLYPH | nlp_core.NLPCore.PARSE_ELEM_PLACED_IMAGE):
                    self._parse_tag_glyph(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_LINE:
                    self._parse_tag_line_line(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_PARA:
                    self._parse_tag_para_line(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_TABLE:
                    if self._is_word_processing:
                        self._parse_tag_table_word(child_tag, child)
                    else:
                        self._parse_tag_table_line(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_BOX).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag Box with granularity 'word'.
    # ------------------------------------------------------------------
    def _parse_tag_box_word(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Box' with granularity 'word'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case (nlp_core.NLPCore.PARSE_ELEM_A | nlp_core.NLPCore.PARSE_ELEM_PLACED_IMAGE):
                    pass
                case nlp_core.NLPCore.PARSE_ELEM_GLYPH:
                    self._parse_tag_glyph(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_LINE:
                    self._parse_tag_line_word(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_PARA:
                    self._parse_tag_para_word(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_TABLE:
                    if self._is_word_processing:
                        self._parse_tag_table_word(child_tag, child)
                    else:
                        self._parse_tag_table_line(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_TEXT:
                    self._parse_tag_text(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_WORD:
                    self._parse_tag_word(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_BOX).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag Cell.
    # ------------------------------------------------------------------
    def _parse_tag_cell_line(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Cell'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case nlp_core.NLPCore.PARSE_ELEM_PARA:
                    self._parse_tag_para_line(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_CELL).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag Cell.
    # ------------------------------------------------------------------
    def _parse_tag_cell_word(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Cell'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._parse_result_no_cells_row += self._parse_result_table_cell_span_prev

        self._parse_result_table_cell_span = parent.attrib.get(nlp_core.NLPCore.PARSE_ATTR_COL_SPAN)

        if self._parse_result_table_cell_span:
            self._parse_result_table_cell_span_prev = int(self._parse_result_table_cell_span)
        else:
            self._parse_result_table_cell_span = 1
            self._parse_result_no_cells_row += 1

        self._parse_result_table_cell_is_empty = True

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case nlp_core.NLPCore.PARSE_ELEM_PARA:
                    self._parse_tag_para_word(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_CELL).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag 'Content'.
    # ------------------------------------------------------------------
    def _parse_tag_content(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Content'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case nlp_core.NLPCore.PARSE_ELEM_PARA:
                    if self._is_word_processing:
                        self._parse_tag_para_word(child_tag, child)
                    else:
                        self._parse_tag_para_line(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_TABLE:
                    if self._is_word_processing:
                        self._parse_tag_table_word(child_tag, child)
                    else:
                        self._parse_tag_table_line(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_CONTENT).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag 'DocInfo'.
    # ------------------------------------------------------------------
    def _parse_tag_doc_info(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'DocInfo'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case (
                    nlp_core.NLPCore.PARSE_ELEM_AUTHOR
                    | nlp_core.NLPCore.PARSE_ELEM_CREATION_DATE
                    | nlp_core.NLPCore.PARSE_ELEM_CREATOR
                    | nlp_core.NLPCore.PARSE_ELEM_CUSTOM
                    | nlp_core.NLPCore.PARSE_ELEM_CUSTOM_BINARY
                    | nlp_core.NLPCore.PARSE_ELEM_GTS_PDFX_CONFORMANCE
                    | nlp_core.NLPCore.PARSE_ELEM_GTS_PDFX_VERSION
                    | nlp_core.NLPCore.PARSE_ELEM_GTS_PPMLVDX_CONFORMANCE
                    | nlp_core.NLPCore.PARSE_ELEM_GTS_PPMLVDX_VERSION
                    | nlp_core.NLPCore.PARSE_ELEM_ISO_PDFE_VERSION
                    | nlp_core.NLPCore.PARSE_ELEM_KEYWORDS
                    | nlp_core.NLPCore.PARSE_ELEM_MOD_DATE
                    | nlp_core.NLPCore.PARSE_ELEM_PRODUCER
                    | nlp_core.NLPCore.PARSE_ELEM_SUBJECT
                    | nlp_core.NLPCore.PARSE_ELEM_TITLE
                    | nlp_core.NLPCore.PARSE_ELEM_TRAPPED
                ):
                    pass
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_DOC_INFO).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag Font.
    # ------------------------------------------------------------------
    def _parse_tag_font(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Font'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._parse_result_no_fonts += 1

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_FONT).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        if core_glob.inst_setup.is_json_incl_fonts:
            self._parse_result_container_fonts.append(
                {
                    nlp_core.NLPCore.JSON_NAME_EMBEDDED: bool(parent.attrib.get(nlp_core.NLPCore.PARSE_ATTR_EMBEDDED)),
                    nlp_core.NLPCore.JSON_NAME_FONT_NO: self._parse_result_no_fonts,
                    nlp_core.NLPCore.JSON_NAME_FULL_NAME: parent.attrib.get(nlp_core.NLPCore.PARSE_ATTR_FULL_NAME),
                    nlp_core.NLPCore.JSON_NAME_ID: parent.attrib.get(nlp_core.NLPCore.PARSE_ATTR_ID),
                    nlp_core.NLPCore.JSON_NAME_ITALIC_ANGLE: float(parent.attrib.get(nlp_core.NLPCore.PARSE_ATTR_ITALIC_ANGLE)),
                    nlp_core.NLPCore.JSON_NAME_NAME: parent.attrib.get(nlp_core.NLPCore.PARSE_ATTR_NAME),
                    nlp_core.NLPCore.JSON_NAME_TYPE: parent.attrib.get(nlp_core.NLPCore.PARSE_ATTR_TYPE),
                    nlp_core.NLPCore.JSON_NAME_WEIGHT: float(parent.attrib.get(nlp_core.NLPCore.PARSE_ATTR_WEIGHT)),
                }
            )

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag Fonts.
    # ------------------------------------------------------------------
    def _parse_tag_fonts(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Fonts'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case nlp_core.NLPCore.PARSE_ELEM_FONT:
                    self._parse_tag_font(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_FONTS).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag Glyph.
    # ------------------------------------------------------------------
    def _parse_tag_glyph(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Glyph'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_GLYPH).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        if self._parse_result_glyph_is_empty:
            self._parse_result_glyph_is_empty = False
            self._parse_result_font = parent.attrib.get(nlp_core.NLPCore.PARSE_ATTR_GLYPH_FONT)
            self._parse_result_size = float(parent.attrib.get(nlp_core.NLPCore.PARSE_ATTR_GLYPH_SIZE))

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag Line with granularity 'line'.
    # ------------------------------------------------------------------
    def _parse_tag_line_line(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Line' with granularity 'line'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case nlp_core.NLPCore.PARSE_ELEM_A:
                    pass
                case nlp_core.NLPCore.PARSE_ELEM_TEXT:
                    self._parse_tag_text(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_LINE).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        if self._parse_result_line_idx == self._parse_result_no_lines_word:
            core_utils.progress_msg_core(core_utils.ERROR_61_905.replace("{word", str(self._parse_result_no_lines_word)))
            self.no_errors += 1

        core_glob.nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_PAGES][self._parse_result_page_idx][nlp_core.NLPCore.JSON_NAME_LINES][
            self._parse_result_line_idx
        ][nlp_core.NLPCore.JSON_NAME_TEXT] = self._parse_result_text

        self._parse_result_no_lines_line += 1
        self._parse_result_line_idx += 1

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag Line with granularity 'word'.
    # ------------------------------------------------------------------
    def _parse_tag_line_word(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Line' with granularity 'word'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._parse_result_no_words_line = 0

        self._parse_result_line_word_no_first = 0
        self._parse_result_line_word_no_last = 0

        self._parse_result_no_lines_word += 1
        self._parse_result_no_lines_page += 1
        self._parse_result_no_lines_para += 1

        if self._parse_result_para_line_no_first == 0:
            self._parse_result_para_line_no_first = self._parse_result_no_lines_word
        self._parse_result_para_line_no_last = self._parse_result_no_lines_word

        if self._parse_result_page_line_no_first == 0:
            self._parse_result_page_line_no_first = self._parse_result_no_lines_word
        self._parse_result_page_line_no_last = self._parse_result_no_lines_word

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case nlp_core.NLPCore.PARSE_ELEM_A:
                    pass
                case nlp_core.NLPCore.PARSE_ELEM_WORD:
                    self._parse_tag_word(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_LINE).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        if self._parse_result_table:
            no_tables = self._parse_result_no_tables
            no_rows_table = self._parse_result_no_rows_table
            no_cells_row = self._parse_result_no_cells_row
            line_type = nlp_core.NLPCore.LINE_TYPE_TABLE
        else:
            no_tables = 0
            no_rows_table = 0
            no_cells_row = 0
            line_type = nlp_core.NLPCore.LINE_TYPE_BODY

        self._parse_result_container_lines.append(
            {
                nlp_core.NLPCore.JSON_NAME_CONTAINER_WORDS: self._parse_result_container_words,
                nlp_core.NLPCore.JSON_NAME_LINE_NO: self._parse_result_no_lines_word,
                nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE: self._parse_result_page_line_no_first,
                nlp_core.NLPCore.JSON_NAME_LINE_NO_PARA: self._parse_result_para_line_no_first,
                nlp_core.NLPCore.JSON_NAME_LLX: float(parent.attrib.get(nlp_core.NLPCore.PARSE_ATTR_LLX)),
                nlp_core.NLPCore.JSON_NAME_PAGE_NO: self.parse_result_no_pages,
                nlp_core.NLPCore.JSON_NAME_TABLE_CELL_SPAN: self._parse_result_table_cell_span,
                nlp_core.NLPCore.JSON_NAME_TABLE_NO: no_tables,
                nlp_core.NLPCore.JSON_NAME_TABLE_NO_CELL: no_cells_row,
                nlp_core.NLPCore.JSON_NAME_TABLE_NO_ROW: no_rows_table,
                nlp_core.NLPCore.JSON_NAME_TYPE: line_type,
                nlp_core.NLPCore.JSON_NAME_URX: float(parent.attrib.get(nlp_core.NLPCore.PARSE_ATTR_URX)),
                nlp_core.NLPCore.JSON_NAME_WORD_NO_FIRST: self._parse_result_line_word_no_first,
                nlp_core.NLPCore.JSON_NAME_WORD_NO_LAST: self._parse_result_line_word_no_last,
            }
        )

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag 'Page' with granularity 'line'.
    # ------------------------------------------------------------------
    # noinspection PyArgumentList
    def _parse_tag_page_line(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Page' with granularity 'line'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._parse_result_line_idx = 0

        # Process the page related tags.
        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case (
                    nlp_core.NLPCore.PARSE_ELEM_ACTION
                    | nlp_core.NLPCore.PARSE_ELEM_ANNOTATIONS
                    | nlp_core.NLPCore.PARSE_ELEM_EXCEPTION
                    | nlp_core.NLPCore.PARSE_ELEM_FIELDS
                    | nlp_core.NLPCore.PARSE_ELEM_OPTIONS
                    | nlp_core.NLPCore.PARSE_ELEM_OUTPUT_INTENTS
                ):
                    pass
                case nlp_core.NLPCore.PARSE_ELEM_CONTENT:
                    self._parse_tag_content(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_PAGE).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        self._parse_result_page_idx += 1

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag 'Page' with granularity 'word'.
    # ------------------------------------------------------------------
    # noinspection PyArgumentList
    def _parse_tag_page_word(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Page' with granularity 'word'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._parse_result_container_lines = []
        self._parse_result_container_paras = []

        self._parse_result_no_paras_page = 0
        self._parse_result_no_lines_page = 0
        self._parse_result_no_words_page = 0

        self._parse_result_page_line_no_first = 0
        self._parse_result_page_line_no_last = 0
        self._parse_result_page_para_no_first = 0
        self._parse_result_page_para_no_last = 0
        self._parse_result_page_word_no_first = 0
        self._parse_result_page_word_no_last = 0

        self.parse_result_no_pages += 1

        # Process the page related tags.
        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case (
                    nlp_core.NLPCore.PARSE_ELEM_ACTION
                    | nlp_core.NLPCore.PARSE_ELEM_ANNOTATIONS
                    | nlp_core.NLPCore.PARSE_ELEM_EXCEPTION
                    | nlp_core.NLPCore.PARSE_ELEM_FIELDS
                    | nlp_core.NLPCore.PARSE_ELEM_OPTIONS
                    | nlp_core.NLPCore.PARSE_ELEM_OUTPUT_INTENTS
                ):
                    pass
                case nlp_core.NLPCore.PARSE_ELEM_CONTENT:
                    self._parse_tag_content(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_PAGE).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        self._parse_result_container_pages.append(
            {
                nlp_core.NLPCore.JSON_NAME_LINE_NO_FIRST: self._parse_result_page_line_no_first,
                nlp_core.NLPCore.JSON_NAME_LINE_NO_LAST: self._parse_result_page_line_no_last,
                nlp_core.NLPCore.JSON_NAME_PAGE_NO: self.parse_result_no_pages,
                nlp_core.NLPCore.JSON_NAME_PARA_NO_FIRST: self._parse_result_page_para_no_first,
                nlp_core.NLPCore.JSON_NAME_PARA_NO_LAST: self._parse_result_page_para_no_last,
                nlp_core.NLPCore.JSON_NAME_WORD_NO_FIRST: self._parse_result_page_word_no_first,
                nlp_core.NLPCore.JSON_NAME_WORD_NO_LAST: self._parse_result_page_word_no_last,
                nlp_core.NLPCore.JSON_NAME_CONTAINER_LINES: self._parse_result_container_lines,
                nlp_core.NLPCore.JSON_NAME_CONTAINER_PARAS: self._parse_result_container_paras,
            }
        )

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag 'Pages' with granularity 'line'.
    # ------------------------------------------------------------------
    # noinspection PyArgumentList
    def _parse_tag_pages_line(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:  # noqa: C901
        """Process tag 'Pages' with granularity 'line'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._parse_result_no_lines_line = 0
        self._parse_result_page_idx = 0

        # Process the tags of all document pages.
        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case nlp_core.NLPCore.PARSE_ELEM_GRAPHICS | nlp_core.NLPCore.PARSE_ELEM_RESOURCES:
                    pass
                case nlp_core.NLPCore.PARSE_ELEM_PAGE:
                    self._parse_tag_page_line(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_PAGES).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        if self._parse_result_no_lines_line != self._parse_result_no_lines_word:
            core_utils.progress_msg_core(
                core_utils.ERROR_61_904.replace("{line}", str(self._parse_result_no_lines_line)).replace(
                    "{word", str(self._parse_result_no_lines_word)
                )
            )
            self.no_errors += 1

        self._determine_line_types()

        with open(self._full_name, "w", encoding=core_glob.FILE_ENCODING_DEFAULT) as file_handle:
            json.dump(
                core_glob.nlp_core.document_json,
                file_handle,
                indent=core_glob.inst_setup.json_indent,
                sort_keys=core_glob.inst_setup.is_json_sort_keys,
            )

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag 'Pages' with granularity 'word'.
    # ------------------------------------------------------------------
    # noinspection PyArgumentList
    def _parse_tag_pages_word(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:  # noqa: C901
        """Process tag 'Pages' with granularity 'word'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._parse_result_container_fonts = []
        self._parse_result_container_pages = []

        self._parse_result_no_fonts = 0
        self._parse_result_no_lines_word = 0
        self.parse_result_no_pages = 0
        self._parse_result_no_paras = 0
        self.parse_result_no_tables = 0
        self._parse_result_no_words = 0

        # Process the tags of all document pages.
        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case nlp_core.NLPCore.PARSE_ELEM_GRAPHICS:
                    pass
                case nlp_core.NLPCore.PARSE_ELEM_PAGE:
                    self._parse_tag_page_word(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_RESOURCES:
                    self._parse_tag_resources(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_PAGES).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        core_glob.nlp_core.document_json = {
            nlp_core.NLPCore.JSON_NAME_CREATED_AT: datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            nlp_core.NLPCore.JSON_NAME_CREATED_BY: __name__,
            nlp_core.NLPCore.JSON_NAME_NO_LINES: self._parse_result_no_lines_word,
            nlp_core.NLPCore.JSON_NAME_NO_PAGES: self.parse_result_no_pages,
            nlp_core.NLPCore.JSON_NAME_NO_PARAS: self._parse_result_no_paras,
            nlp_core.NLPCore.JSON_NAME_NO_TABLES: self._parse_result_no_tables,
            nlp_core.NLPCore.JSON_NAME_NO_WORDS: self._parse_result_no_words,
            nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES: self._parse_result_container_pages,
        }

        if core_glob.inst_setup.is_json_incl_config:
            core_glob.nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONFIG] = {
                nlp_core.NLPCore.JSON_NAME_PARSER: core_utils.create_config()
            }

        if core_glob.inst_setup.is_json_incl_fonts:
            core_glob.nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_FONTS] = self._parse_result_container_fonts
            core_glob.nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_FONTS] = self._parse_result_no_fonts

        if core_glob.inst_setup.is_json_incl_params:
            core_glob.nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_PARAMS] = {nlp_core.NLPCore.JSON_NAME_PARSER: self._create_params()}

        with open(self._full_name, "w", encoding=core_glob.FILE_ENCODING_DEFAULT) as file_handle:
            json.dump(
                core_glob.nlp_core.document_json,
                file_handle,
                indent=core_glob.inst_setup.json_indent,
                sort_keys=core_glob.inst_setup.is_json_sort_keys,
            )

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag Para with granularity 'line'.
    # ------------------------------------------------------------------
    def _parse_tag_para_line(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Para' with granularity 'line'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case nlp_core.NLPCore.PARSE_ELEM_A:
                    pass
                case nlp_core.NLPCore.PARSE_ELEM_BOX:
                    self._parse_tag_box_line(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_PARA:
                    self._parse_tag_para_line(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_PARA).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag Para with granularity 'word'.
    # ------------------------------------------------------------------
    def _parse_tag_para_word(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Para' with granularity 'word'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._parse_result_container_words = []

        self._parse_result_no_lines_para = 0
        self._parse_result_no_words_para = 0

        self._parse_result_para_line_no_first = 0
        self._parse_result_para_line_no_last = 0
        self._parse_result_para_word_no_first = 0
        self._parse_result_para_word_no_last = 0

        self._parse_result_no_paras += 1
        self._parse_result_no_paras_page += 1

        if self._parse_result_page_para_no_first == 0:
            self._parse_result_page_para_no_first = self._parse_result_no_paras
        self._parse_result_page_para_no_last = self._parse_result_no_paras

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case nlp_core.NLPCore.PARSE_ELEM_A:
                    pass
                case nlp_core.NLPCore.PARSE_ELEM_BOX:
                    self._parse_tag_box_word(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_PARA:
                    self._parse_tag_para_word(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_PARA).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        if self._parse_result_table:
            no_tables = self._parse_result_no_tables
            no_rows_table = self._parse_result_no_rows_table
            no_cells_row = self._parse_result_no_cells_row
        else:
            no_tables = 0
            no_rows_table = 0
            no_cells_row = 0

        self._parse_result_container_paras.append(
            {
                nlp_core.NLPCore.JSON_NAME_LINE_NO_FIRST: self._parse_result_para_line_no_first,
                nlp_core.NLPCore.JSON_NAME_LINE_NO_LAST: self._parse_result_para_line_no_last,
                nlp_core.NLPCore.JSON_NAME_PAGE_NO: self.parse_result_no_pages,
                nlp_core.NLPCore.JSON_NAME_PARA_NO: self._parse_result_no_paras,
                nlp_core.NLPCore.JSON_NAME_PARA_NO_PAGE: self._parse_result_page_para_no_first,
                nlp_core.NLPCore.JSON_NAME_TABLE_CELL_SPAN: self._parse_result_table_cell_span,
                nlp_core.NLPCore.JSON_NAME_TABLE_NO: no_tables,
                nlp_core.NLPCore.JSON_NAME_TABLE_NO_CELL: no_cells_row,
                nlp_core.NLPCore.JSON_NAME_TABLE_NO_ROW: no_rows_table,
                nlp_core.NLPCore.JSON_NAME_WORD_NO_FIRST: self._parse_result_para_word_no_first,
                nlp_core.NLPCore.JSON_NAME_WORD_NO_LAST: self._parse_result_para_word_no_last,
                nlp_core.NLPCore.JSON_NAME_CONTAINER_WORDS: self._parse_result_container_words,
            }
        )

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag Resources.
    # ------------------------------------------------------------------
    def _parse_tag_resources(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Resources'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case nlp_core.NLPCore.PARSE_ELEM_FONTS:
                    self._parse_tag_fonts(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_COLOR_SPACES:
                    pass
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_RESOURCES).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag Row.
    # ------------------------------------------------------------------
    def _parse_tag_row_line(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Row'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case nlp_core.NLPCore.PARSE_ELEM_CELL:
                    self._parse_tag_cell_line(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_ROW).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag Row.
    # ------------------------------------------------------------------
    def _parse_tag_row_word(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Row'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._parse_result_no_cells_row = 0

        self._parse_result_no_rows_table += 1

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case nlp_core.NLPCore.PARSE_ELEM_CELL:
                    self._parse_tag_cell_word(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_ROW).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag Table.
    # ------------------------------------------------------------------
    def _parse_tag_table_line(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Table'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._parse_result_table = True

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case nlp_core.NLPCore.PARSE_ELEM_ROW:
                    self._parse_tag_row_line(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_TABLE).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        self._parse_result_table = False

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag Table.
    # ------------------------------------------------------------------
    def _parse_tag_table_word(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Table'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._parse_result_table = True
        self._parse_result_no_rows_table = 0

        self._parse_result_no_tables += 1

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case nlp_core.NLPCore.PARSE_ELEM_ROW:
                    self._parse_tag_row_word(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_TABLE).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        self._parse_result_table = False

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag Text.
    # ------------------------------------------------------------------
    def _parse_tag_text(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Text'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_WORD).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        self._parse_result_text = parent.text

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag Word.
    # ------------------------------------------------------------------
    def _parse_tag_word(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Word'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._parse_result_no_words += 1
        self._parse_result_no_words_line += 1
        self._parse_result_no_words_page += 1
        self._parse_result_no_words_para += 1

        if self._parse_result_line_word_no_first == 0:
            self._parse_result_line_word_no_first = self._parse_result_no_words
        self._parse_result_line_word_no_last = self._parse_result_no_words

        if self._parse_result_para_word_no_first == 0:
            self._parse_result_para_word_no_first = self._parse_result_no_words
        self._parse_result_para_word_no_last = self._parse_result_no_words

        if self._parse_result_page_word_no_first == 0:
            self._parse_result_page_word_no_first = self._parse_result_no_words
        self._parse_result_page_word_no_last = self._parse_result_no_words

        self._parse_result_glyph_is_empty = True

        self._parse_result_font = ""
        self._parse_result_size = 0.0

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case nlp_core.NLPCore.PARSE_ELEM_BOX:
                    self._parse_tag_box_word(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_TEXT:
                    self._parse_tag_text(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_WORD).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        if self._parse_result_table:
            no_tables = self._parse_result_no_tables
            no_rows_table = self._parse_result_no_rows_table
            no_cells_row = self._parse_result_no_cells_row
            line_type = nlp_core.NLPCore.LINE_TYPE_TABLE
        else:
            no_tables = 0
            no_rows_table = 0
            no_cells_row = 0
            line_type = nlp_core.NLPCore.LINE_TYPE_BODY

        container_word = {
            nlp_core.NLPCore.JSON_NAME_LINE_NO: self._parse_result_no_lines_word,
            nlp_core.NLPCore.JSON_NAME_PAGE_NO: self.parse_result_no_pages,
            nlp_core.NLPCore.JSON_NAME_PARA_NO: self._parse_result_no_paras,
            nlp_core.NLPCore.JSON_NAME_TABLE_CELL_SPAN: self._parse_result_table_cell_span,
            nlp_core.NLPCore.JSON_NAME_TABLE_NO: no_tables,
            nlp_core.NLPCore.JSON_NAME_TABLE_NO_CELL: no_cells_row,
            nlp_core.NLPCore.JSON_NAME_TABLE_NO_ROW: no_rows_table,
            nlp_core.NLPCore.JSON_NAME_TEXT: self._parse_result_text,
            nlp_core.NLPCore.JSON_NAME_TYPE: line_type,
            nlp_core.NLPCore.JSON_NAME_WORD_NO: self._parse_result_no_words,
            nlp_core.NLPCore.JSON_NAME_WORD_NO_LINE: self._parse_result_line_word_no_first,
            nlp_core.NLPCore.JSON_NAME_WORD_NO_PAGE: self._parse_result_page_word_no_first,
            nlp_core.NLPCore.JSON_NAME_WORD_NO_PARA: self._parse_result_para_word_no_first,
        }

        if core_glob.inst_setup.is_json_incl_fonts:
            container_word[nlp_core.NLPCore.JSON_NAME_FONT] = self._parse_result_font
            container_word[nlp_core.NLPCore.JSON_NAME_SIZE] = self._parse_result_size

        self._parse_result_container_words.append(container_word)

        self._debug_xml_element_text()

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Check the object existence.
    # ------------------------------------------------------------------
    def exists(self) -> bool:
        """Check the object existence.

        Returns:
            bool: Always true
        """
        return self._exist

    # ------------------------------------------------------------------
    # Initialise from the JSON file.
    # ------------------------------------------------------------------
    @classmethod
    def from_file(
        cls,
        file_encoding: str,
        full_name: str,
    ) -> None:
        """Initialise from JSON file.

        Args:
            file_encoding (str):
                The encoding of the output file.
            full_name (str):
                Name of the file with the JSON data.
        """
        core_glob.logger.debug(core_glob.LOGGER_START)
        core_glob.logger.debug("param file_encoding=%s", file_encoding)
        core_glob.logger.debug("param full_name    =%s", full_name)

        try:
            core_glob.nlp_core.exists()
        except AttributeError:
            core_glob.nlp_core = nlp_core.NLPCore()

        with open(full_name, "r", encoding=file_encoding) as file_handle:
            core_glob.nlp_core.document_json = json.load(file_handle)

        core_glob.logger.debug(core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Processing tag 'Document' with granularity 'line'.
    # ------------------------------------------------------------------
    def parse_tag_document_line(
        self,
        parent: collections.abc.Iterable[str],
        parent_tag: str,
    ) -> None:
        """Process tag 'Document' with granularity 'line'.

        Args:
            parent (collections.abc.Iterable[str]):
                Parent data structure.
            parent_tag (str):
                Parent tag.
        """
        core_glob.logger.debug(core_glob.LOGGER_START)
        core_glob.logger.debug("param parent                    =%s", parent)
        core_glob.logger.debug("param parent_tag                =%s", parent_tag)

        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._is_line_processing = True
        self._is_word_processing = False

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case (
                    nlp_core.NLPCore.PARSE_ELEM_ACTION
                    | nlp_core.NLPCore.PARSE_ELEM_ATTACHMENTS
                    | nlp_core.NLPCore.PARSE_ELEM_DESTINATIONS
                    | nlp_core.NLPCore.PARSE_ELEM_DOC_INFO
                    | nlp_core.NLPCore.PARSE_ELEM_BOOKMARKS
                    | nlp_core.NLPCore.PARSE_ELEM_ENCRYPTION
                    | nlp_core.NLPCore.PARSE_ELEM_EXCEPTION
                    | nlp_core.NLPCore.PARSE_ELEM_JAVA_SCRIPTS
                    | nlp_core.NLPCore.PARSE_ELEM_METADATA
                    | nlp_core.NLPCore.PARSE_ELEM_OPTIONS
                    | nlp_core.NLPCore.PARSE_ELEM_OUTPUT_INTENTS
                    | nlp_core.NLPCore.PARSE_ELEM_SIGNATURE_FIELDS
                    | nlp_core.NLPCore.PARSE_ELEM_XFA
                ):
                    pass
                case nlp_core.NLPCore.PARSE_ELEM_PAGES:
                    self._parse_tag_pages_line(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_DOCUMENT).replace("{child_tag", other)
                    )
                    self.no_errors += 1

            self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

        core_glob.logger.debug(core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Processing tag 'Document' with granularity 'word'.
    # ------------------------------------------------------------------
    def parse_tag_document_word(  # pylint: disable=too-many-arguments
        self,
        directory_name: str,
        document_id: int,
        environment_variant: str,
        file_name_curr: str,
        file_name_next: str,
        file_name_orig: str,
        is_lt_footer_required: bool,
        is_lt_header_required: bool,
        is_lt_heading_required: bool,
        is_lt_list_bullet_required: bool,
        is_lt_list_number_required: bool,
        is_lt_toc_required: bool,
        no_pdf_pages: int,
        parent: collections.abc.Iterable[str],
        parent_tag: str,
    ) -> None:
        """Process tag 'Document' with granularity 'word'.

        Args:
            directory_name (str):
                Directory name of the output file.
            document_id (int):
                Identification of the document.
            environment_variant (str):
                Environment variant: dev, prod or test.
            file_name_curr (str):
                File name of the current file.
            file_name_next (str):
                File name of the output file.
            file_name_orig (in):
                File name of the document file.
            is_lt_footer_required (bool):
                If it is set to **`true`**, the determination of the footer lines is performed.
            is_lt_header_required (bool):
                If it is set to **`true`**, the determination of the header lines is performed.
            is_lt_heading_required (bool):
                If it is set to **`true`**, the determination of the heading lines is performed.
            is_lt_list_bullet_required (bool):
                If it is set to **`true`**, the determination of the bulleted lists is performed.
            is_lt_list_number_required (bool):
                If it is set to **`true`**, the determination of the numbered lists is performed.
            is_lt_toc_required (bool):
                If it is set to **`true`**, the determination of the TOC lines is performed.
            no_pdf_pages (int):
                Number ODF pages.
            parent (collections.abc.Iterable[str]):
                Parent data structure.
            parent_tag (str):
                Parent tag.
        """
        core_glob.logger.debug(core_glob.LOGGER_START)
        core_glob.logger.debug("param directory_name            =%s", directory_name)
        core_glob.logger.debug("param document_id               =%i", document_id)
        core_glob.logger.debug("param environment_variant       =%s", environment_variant)
        core_glob.logger.debug("param file_name_curr            =%s", file_name_curr)
        core_glob.logger.debug("param file_name_next            =%s", file_name_next)
        core_glob.logger.debug("param file_name_orig            =%s", file_name_orig)
        core_glob.logger.debug("param is_lt_footer_required     =%s", is_lt_footer_required)
        core_glob.logger.debug("param is_lt_header_required     =%s", is_lt_header_required)
        core_glob.logger.debug("param is_lt_heading_required    =%s", is_lt_heading_required)
        core_glob.logger.debug("param is_lt_list_bullet_required=%s", is_lt_list_bullet_required)
        core_glob.logger.debug("param is_lt_list_number_required=%s", is_lt_list_number_required)
        core_glob.logger.debug("param is_lt_toc_required        =%s", is_lt_toc_required)
        core_glob.logger.debug("param no_pdf_pages              =%i", no_pdf_pages)
        core_glob.logger.debug("param parent                    =%s", parent)
        core_glob.logger.debug("param parent_tag                =%s", parent_tag)

        core_utils.check_exists_object(
            is_setup=True,
        )

        self._directory_name = directory_name
        self._document_id = document_id
        self._environment_variant = environment_variant
        self._file_name_curr = file_name_curr
        self._file_name_orig = file_name_orig
        self._full_name = file_name_next
        self._is_lt_footer_required = is_lt_footer_required
        self._is_lt_header_required = is_lt_header_required
        self._is_lt_heading_required = is_lt_heading_required
        self._is_lt_list_bullet_required = is_lt_list_bullet_required
        self._is_lt_list_number_required = is_lt_list_number_required
        self._is_lt_toc_required = is_lt_toc_required
        self._no_pdf_pages = no_pdf_pages

        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        core_glob.nlp_core.document_json = {}

        self.no_errors = 0

        self._is_line_processing = False
        self._is_word_processing = True

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case (
                    nlp_core.NLPCore.PARSE_ELEM_ACTION
                    | nlp_core.NLPCore.PARSE_ELEM_ATTACHMENTS
                    | nlp_core.NLPCore.PARSE_ELEM_DESTINATIONS
                    | nlp_core.NLPCore.PARSE_ELEM_ENCRYPTION
                    | nlp_core.NLPCore.PARSE_ELEM_EXCEPTION
                    | nlp_core.NLPCore.PARSE_ELEM_JAVA_SCRIPTS
                    | nlp_core.NLPCore.PARSE_ELEM_METADATA
                    | nlp_core.NLPCore.PARSE_ELEM_OPTIONS
                    | nlp_core.NLPCore.PARSE_ELEM_OUTPUT_INTENTS
                    | nlp_core.NLPCore.PARSE_ELEM_SIGNATURE_FIELDS
                    | nlp_core.NLPCore.PARSE_ELEM_XFA
                ):
                    pass
                case nlp_core.NLPCore.PARSE_ELEM_BOOKMARKS:
                    self._parse_tag_bookmarks(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_DOC_INFO:
                    self._parse_tag_doc_info(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_PAGES:
                    self._parse_tag_pages_word(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_DOCUMENT).replace("{child_tag", other)
                    )
                    self.no_errors += 1

            self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

        core_glob.logger.debug(core_glob.LOGGER_END)
