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
        self._is_lt_heading_required = False
        self._is_lt_list_bullet_required = False
        self._is_lt_list_number_required = False
        self._is_lt_toc_required = False
        self._is_word_processing = False

        self._no_lines_line_type_table = 0
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
        self._parse_result_line_word_no_para_first = 0
        self._parse_result_llx: float = 0.0
        self._parse_result_no_cells_row = 0
        self._parse_result_no_fonts = 0
        self._parse_result_no_lines_line = 0
        self._parse_result_no_lines_page = 0
        self._parse_result_no_lines_para = 0
        self._parse_result_no_lines_word = 0
        self._parse_result_no_pages = 0
        self._parse_result_no_paras = 0
        self._parse_result_no_paras_page = 0
        self._parse_result_no_rows_table = 0
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
                f"document: pages={self._parse_result_no_pages:2d} "
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
        core_glob.inst_lt_hf = lt_hf.LineTypeHeaderFooter()
        core_glob.inst_lt_hf.process_document(
            file_name_curr=self._file_name_curr,
        )

        # ------------------------------------------------------------------
        # Line type toc.
        # ------------------------------------------------------------------
        if self._is_lt_toc_required:
            core_glob.inst_lt_toc = lt_toc.LineTypeToc()
            core_glob.inst_lt_toc.process_document(
                file_name_curr=self._file_name_curr,
            )

        # ------------------------------------------------------------------
        # Line type bulleted list.
        # ------------------------------------------------------------------
        if self._is_lt_list_bullet_required:
            core_glob.inst_lt_lb = lt_lb.LineTypeListBullet()
            core_glob.inst_lt_lb.process_document(
                directory_name=self._directory_name,
                document_id=self._document_id,
                environment_variant=self._environment_variant,
                file_name_curr=self._file_name_curr,
                file_name_orig=self._file_name_orig,
            )

        # ------------------------------------------------------------------
        # Line type numbered list.
        # ------------------------------------------------------------------
        if self._is_lt_list_number_required:
            core_glob.inst_lt_ln = lt_ln.LineTypeListNumber()
            core_glob.inst_lt_ln.process_document(
                directory_name=self._directory_name,
                document_id=self._document_id,
                environment_variant=self._environment_variant,
                file_name_curr=self._file_name_curr,
                file_name_orig=self._file_name_orig,
            )

        # ------------------------------------------------------------------
        # Line type heading.
        # ------------------------------------------------------------------
        if self._is_lt_heading_required:
            core_glob.inst_lt_h = lt_h.LineTypeHeading()
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
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_BOOKMARK).replace("{child_tag}", other)
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
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_BOOKMARKS).replace("{child_tag}", other)
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
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_BOX).replace("{child_tag}", other)
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
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_BOX).replace("{child_tag}", other)
                    )
                    self.no_errors += 1

        self._parse_result_llx = float(parent.attrib.get(nlp_core.NLPCore.PARSE_ATTR_LLX))
        self._parse_result_urx = float(parent.attrib.get(nlp_core.NLPCore.PARSE_ATTR_URX))

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
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_CELL).replace("{child_tag}", other)
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
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_CELL).replace("{child_tag}", other)
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
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_CONTENT).replace("{child_tag}", other)
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
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_DOC_INFO).replace("{child_tag}", other)
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
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_FONT).replace("{child_tag}", other)
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
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_FONTS).replace("{child_tag}", other)
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
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_GLYPH).replace("{child_tag}", other)
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
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_LINE).replace("{child_tag}", other)
                    )
                    self.no_errors += 1
                    return

        # 61.905 Issue (s_p_j): Too many lines at granularity 'line' - expected {no_lines_word} (text='{text}')
        if self._parse_result_line_idx >= self._parse_result_no_lines_word:
            core_utils.progress_msg_core(
                core_utils.ERROR_61_905.replace("{no_lines_word}", str(self._parse_result_no_lines_word)).replace(
                    "{text}", self._parse_result_text
                )
            )
            self.no_errors += 1
            return

        # 61.907 Issue (s_p_j): Not enough lines at granularity 'word' - found only {no_lines_word} (text='{text}')
        no_lines_page = core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES][self._parse_result_page_idx][
            nlp_core.NLPCore.JSON_NAME_NO_LINES_PAGE
        ]
        if self._parse_result_line_idx >= no_lines_page:
            core_utils.progress_msg_core(
                core_utils.ERROR_61_907.replace(
                    "{no_lines_word}",
                    str(no_lines_page),
                ).replace("{text}", self._parse_result_text)
            )
            self.no_errors += 1
            return

        # Try to check whether the line determined at the granularity 'Word' corresponds to the current line
        para_idx_page = (
            core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES][self._parse_result_page_idx][
                nlp_core.NLPCore.JSON_NAME_CONTAINER_LINES
            ][self._parse_result_line_idx][nlp_core.NLPCore.JSON_NAME_PARA_NO_PAGE]
            - 1
        )

        word_idx_para_first = (
            core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES][self._parse_result_page_idx][
                nlp_core.NLPCore.JSON_NAME_CONTAINER_LINES
            ][self._parse_result_line_idx][nlp_core.NLPCore.JSON_NAME_WORD_NO_PARA_FIRST]
            - 1
        )

        first_word_text = core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES][self._parse_result_page_idx][
            nlp_core.NLPCore.JSON_NAME_CONTAINER_PARAS
        ][para_idx_page][nlp_core.NLPCore.JSON_NAME_CONTAINER_WORDS][word_idx_para_first][nlp_core.NLPCore.JSON_NAME_TEXT]

        if not self._parse_result_text.startswith(first_word_text):
            # 61.906 Issue (s_p_j): Line number {line_no}: the line text '{line_text}' should start with '{word_text}'
            core_utils.progress_msg_core(
                core_utils.ERROR_61_906.replace("{line_no}", str(self._parse_result_line_idx + 1))
                .replace("{line_text}", str(self._parse_result_text))
                .replace("{word_text}", first_word_text)
            )
            self.no_errors += 1

        # Store the line text in the JSON document
        core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES][self._parse_result_page_idx][
            nlp_core.NLPCore.JSON_NAME_CONTAINER_LINES
        ][self._parse_result_line_idx][nlp_core.NLPCore.JSON_NAME_TEXT] = self._parse_result_text

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
        self._parse_result_line_word_no_para_first = 0

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
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_LINE).replace("{child_tag}", other)
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
                nlp_core.NLPCore.JSON_NAME_LINE_NO: self._parse_result_no_lines_word,
                nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE: self._parse_result_no_lines_page,
                nlp_core.NLPCore.JSON_NAME_LINE_NO_PARA: self._parse_result_no_lines_para,
                nlp_core.NLPCore.JSON_NAME_LLX: float(parent.attrib.get(nlp_core.NLPCore.PARSE_ATTR_LLX)),
                nlp_core.NLPCore.JSON_NAME_NO_WORDS_LINE: self._parse_result_no_words_line,
                nlp_core.NLPCore.JSON_NAME_PAGE_NO: self._parse_result_no_pages,
                nlp_core.NLPCore.JSON_NAME_PARA_NO: self._parse_result_no_paras,
                nlp_core.NLPCore.JSON_NAME_PARA_NO_PAGE: self._parse_result_no_paras_page,
                nlp_core.NLPCore.JSON_NAME_TABLE_CELL_NO: no_cells_row,
                nlp_core.NLPCore.JSON_NAME_TABLE_CELL_SPAN: self._parse_result_table_cell_span,
                nlp_core.NLPCore.JSON_NAME_TABLE_NO: no_tables,
                nlp_core.NLPCore.JSON_NAME_TABLE_ROW_NO: no_rows_table,
                nlp_core.NLPCore.JSON_NAME_TEXT: "",
                nlp_core.NLPCore.JSON_NAME_TYPE: line_type,
                nlp_core.NLPCore.JSON_NAME_URX: float(parent.attrib.get(nlp_core.NLPCore.PARSE_ATTR_URX)),
                nlp_core.NLPCore.JSON_NAME_WORD_NO_FIRST: self._parse_result_line_word_no_first,
                nlp_core.NLPCore.JSON_NAME_WORD_NO_LAST: self._parse_result_line_word_no_last,
                nlp_core.NLPCore.JSON_NAME_WORD_NO_PARA_FIRST: self._parse_result_line_word_no_para_first,
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
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_PAGE).replace("{child_tag}", other)
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

        self._parse_result_no_pages += 1

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
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_PAGE).replace("{child_tag}", other)
                    )
                    self.no_errors += 1

        self._parse_result_container_pages.append(
            {
                nlp_core.NLPCore.JSON_NAME_LINE_NO_FIRST: self._parse_result_page_line_no_first,
                nlp_core.NLPCore.JSON_NAME_LINE_NO_LAST: self._parse_result_page_line_no_last,
                nlp_core.NLPCore.JSON_NAME_NO_LINES_PAGE: self._parse_result_no_lines_page,
                nlp_core.NLPCore.JSON_NAME_NO_PARAS_PAGE: self._parse_result_no_paras_page,
                nlp_core.NLPCore.JSON_NAME_NO_WORDS_PAGE: self._parse_result_no_words_page,
                nlp_core.NLPCore.JSON_NAME_PAGE_NO: self._parse_result_no_pages,
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
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_PAGES).replace("{child_tag}", other)
                    )
                    self.no_errors += 1

        if self._parse_result_no_lines_line != self._parse_result_no_lines_word:
            # 61.904 Issue (s_p_j): Too few lines at granularity 'line' - {line} instead of {word}
            core_utils.progress_msg_core(
                core_utils.ERROR_61_904.replace("{line}", str(self._parse_result_no_lines_line)).replace(
                    "{word}", str(self._parse_result_no_lines_word)
                )
            )
            self.no_errors += 1

        if self.no_errors == 0:
            self._determine_line_types()

        with open(self._full_name, "w", encoding=core_glob.FILE_ENCODING_DEFAULT) as file_handle:
            json.dump(
                core_glob.inst_nlp_core.document_json,
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
        self._parse_result_no_pages = 0
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
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_PAGES).replace("{child_tag}", other)
                    )
                    self.no_errors += 1

        core_glob.inst_nlp_core.document_json = {
            nlp_core.NLPCore.JSON_NAME_CREATED_AT: datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            nlp_core.NLPCore.JSON_NAME_CREATED_BY: __name__,
            nlp_core.NLPCore.JSON_NAME_MODIFIED_AT: "",
            nlp_core.NLPCore.JSON_NAME_MODIFIED_BY: "",
        }

        if core_glob.inst_setup.is_json_incl_fonts:
            core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_FONTS] = self._parse_result_no_fonts

        core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_FOOTERS] = 0
        core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_HEADERS] = 0
        core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_LINES] = self._parse_result_no_lines_word
        core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_LINES_FOOTER] = 0
        core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_LINES_HEADER] = 0

        if self._is_lt_heading_required:
            core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_LINES_HEADING] = 0

        if self._is_lt_list_bullet_required:
            core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_LINES_LIST_BULLET] = 0

        if self._is_lt_list_number_required:
            core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_LINES_LIST_NUMBER] = 0

        core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_LINES_TABLE] = self._no_lines_line_type_table

        if self._is_lt_toc_required:
            core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_LINES_TOC] = 0

        if self._is_lt_list_bullet_required:
            core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_LISTS_BULLET] = 0

        if self._is_lt_list_number_required:
            core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_LISTS_NUMBER] = 0

        core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_PAGES] = self._parse_result_no_pages
        core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_PARAS] = self._parse_result_no_paras

        if core_glob.inst_setup.is_json_incl_sentences:
            core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_SENTENCES] = 0

        core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_TABLES] = self._parse_result_no_tables
        core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_WORDS] = self._parse_result_no_words

        if core_glob.inst_setup.is_json_incl_config:
            core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONFIG] = {
                nlp_core.NLPCore.JSON_NAME_PARSER: core_utils.create_config()
            }

        if core_glob.inst_setup.is_json_incl_fonts:
            core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_FONTS] = self._parse_result_container_fonts

        if self._is_lt_heading_required:
            core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_HEADING] = "TBD"

        if self._is_lt_list_bullet_required:
            core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_LISTS_BULLET] = "TBD"

        if self._is_lt_list_number_required:
            core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_LISTS_NUMBER] = "TBD"

        core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES] = self._parse_result_container_pages

        if core_glob.inst_setup.is_json_incl_params:
            core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_PARAMS] = {
                nlp_core.NLPCore.JSON_NAME_PARSER: self._create_params()
            }

        if core_glob.inst_setup.is_json_incl_sentences:
            core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_SENTENCES] = "TBD"

        with open(self._full_name, "w", encoding=core_glob.FILE_ENCODING_DEFAULT) as file_handle:
            json.dump(
                core_glob.inst_nlp_core.document_json,
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
                case nlp_core.NLPCore.PARSE_ELEM_LINE:
                    self._parse_tag_para_line(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_TEXT:
                    self._parse_tag_text(child_tag, child)
                case other:
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_PARA).replace("{child_tag}", other)
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
                case nlp_core.NLPCore.PARSE_ELEM_WORD:
                    self._parse_tag_para_word(child_tag, child)
                case other:
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_PARA).replace("{child_tag}", other)
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
                nlp_core.NLPCore.JSON_NAME_NO_LINES_PARA: self._parse_result_no_lines_para,
                nlp_core.NLPCore.JSON_NAME_NO_SENTENCES_PARA: 0,
                nlp_core.NLPCore.JSON_NAME_NO_WORDS_PARA: self._parse_result_no_words_para,
                nlp_core.NLPCore.JSON_NAME_PAGE_NO: self._parse_result_no_pages,
                nlp_core.NLPCore.JSON_NAME_PARA_NO: self._parse_result_no_paras,
                nlp_core.NLPCore.JSON_NAME_PARA_NO_PAGE: self._parse_result_page_para_no_first,
                nlp_core.NLPCore.JSON_NAME_TABLE_CELL_NO: no_cells_row,
                nlp_core.NLPCore.JSON_NAME_TABLE_CELL_SPAN: self._parse_result_table_cell_span,
                nlp_core.NLPCore.JSON_NAME_TABLE_NO: no_tables,
                nlp_core.NLPCore.JSON_NAME_TABLE_ROW_NO: no_rows_table,
                nlp_core.NLPCore.JSON_NAME_TEXT: "",
                nlp_core.NLPCore.JSON_NAME_WORD_NO_FIRST: self._parse_result_para_word_no_first,
                nlp_core.NLPCore.JSON_NAME_WORD_NO_LAST: self._parse_result_para_word_no_last,
                nlp_core.NLPCore.JSON_NAME_CONTAINER_SENTENCES: "TBD",
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
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_RESOURCES).replace("{child_tag}", other)
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
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_ROW).replace("{child_tag}", other)
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
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_ROW).replace("{child_tag}", other)
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
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_TABLE).replace("{child_tag}", other)
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
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_TABLE).replace("{child_tag}", other)
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
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_WORD).replace("{child_tag}", other)
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

        if self._parse_result_line_word_no_para_first == 0:
            self._parse_result_line_word_no_para_first = self._parse_result_no_words_para

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
        self._parse_result_llx = 0.0
        self._parse_result_size = 0.0
        self._parse_result_urx = 0.0

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case nlp_core.NLPCore.PARSE_ELEM_BOX:
                    self._parse_tag_box_word(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_TEXT:
                    self._parse_tag_text(child_tag, child)
                case other:
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_WORD).replace("{child_tag}", other)
                    )
                    self.no_errors += 1

        if self._parse_result_table:
            no_tables = self._parse_result_no_tables
            no_rows_table = self._parse_result_no_rows_table
            no_cells_row = self._parse_result_no_cells_row
            line_type = nlp_core.NLPCore.LINE_TYPE_TABLE
            self._no_lines_line_type_table += 1
        else:
            no_tables = 0
            no_rows_table = 0
            no_cells_row = 0
            line_type = nlp_core.NLPCore.LINE_TYPE_BODY

        container_word = {}

        if core_glob.inst_setup.is_json_incl_fonts:
            container_word[nlp_core.NLPCore.JSON_NAME_FONT] = self._parse_result_font

        container_word[nlp_core.NLPCore.JSON_NAME_LINE_NO] = self._parse_result_no_lines_word
        container_word[nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE] = self._parse_result_no_lines_page
        container_word[nlp_core.NLPCore.JSON_NAME_LLX] = self._parse_result_llx
        container_word[nlp_core.NLPCore.JSON_NAME_PAGE_NO] = self._parse_result_no_pages
        container_word[nlp_core.NLPCore.JSON_NAME_PARA_NO] = self._parse_result_no_paras

        if core_glob.inst_setup.is_json_incl_fonts:
            container_word[nlp_core.NLPCore.JSON_NAME_SIZE] = self._parse_result_size

        container_word[nlp_core.NLPCore.JSON_NAME_TABLE_CELL_NO] = no_cells_row
        container_word[nlp_core.NLPCore.JSON_NAME_TABLE_CELL_SPAN] = self._parse_result_table_cell_span
        container_word[nlp_core.NLPCore.JSON_NAME_TABLE_NO] = no_tables
        container_word[nlp_core.NLPCore.JSON_NAME_TABLE_ROW_NO] = no_rows_table
        container_word[nlp_core.NLPCore.JSON_NAME_TEXT] = self._parse_result_text
        container_word[nlp_core.NLPCore.JSON_NAME_TYPE] = line_type
        container_word[nlp_core.NLPCore.JSON_NAME_URX] = self._parse_result_urx
        container_word[nlp_core.NLPCore.JSON_NAME_WORD_NO] = self._parse_result_no_words
        container_word[nlp_core.NLPCore.JSON_NAME_WORD_NO_LINE] = self._parse_result_no_words_line
        container_word[nlp_core.NLPCore.JSON_NAME_WORD_NO_PAGE] = self._parse_result_no_words_page
        container_word[nlp_core.NLPCore.JSON_NAME_WORD_NO_PARA] = self._parse_result_no_words_para

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
            core_glob.inst_nlp_core.exists()
        except AttributeError:
            core_glob.nlp_core = nlp_core.NLPCore()

        with open(full_name, "r", encoding=file_encoding) as file_handle:
            core_glob.inst_nlp_core.document_json = json.load(file_handle)

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

        self.no_errors = 0

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
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_DOCUMENT).replace("{child_tag}", other)
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
        self._is_lt_heading_required = is_lt_heading_required
        self._is_lt_list_bullet_required = is_lt_list_bullet_required
        self._is_lt_list_number_required = is_lt_list_number_required
        self._is_lt_toc_required = is_lt_toc_required
        self._no_pdf_pages = no_pdf_pages

        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self.no_errors = 0

        core_glob.inst_nlp_core.document_json = {}

        self._is_line_processing = False
        self._is_word_processing = True
        self._no_lines_line_table = 0

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
                    # 61.902 Issue (s_p_j): Parent node '{parent_tag}' has unknown child node '{child_tag}'
                    core_utils.progress_msg_core(
                        core_utils.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_DOCUMENT).replace("{child_tag}", other)
                    )
                    self.no_errors += 1

            self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

        core_glob.logger.debug(core_glob.LOGGER_END)
