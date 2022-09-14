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

import dcr_core.cls_line_type_header_footer as lt_hf
import dcr_core.cls_line_type_heading as lt_h
import dcr_core.cls_line_type_list_bullet as lt_lb
import dcr_core.cls_line_type_list_number as lt_ln
import dcr_core.cls_line_type_table as lt_tab
import dcr_core.cls_line_type_toc as lt_toc
import dcr_core.cls_nlp_core as nlp_core
import dcr_core.cls_process as process
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

        self._directory_name: str = ""
        self._document_id: int = 0
        self._environment_variant: str = ""
        self._file_name_curr: str = ""
        self._file_name_orig: str = ""
        self._full_name: str = ""
        self._is_lt_footer_required = False
        self._is_lt_header_required = False
        self._is_lt_heading_required = False
        self._is_lt_list_bullet_required = False
        self._is_lt_list_number_required = False
        self._is_lt_table_required = False
        self._is_lt_toc_required = False
        self._no_pdf_pages: int = 0

        self._parse_result_container_fonts: list[nlp_core.FontJSON] = []
        self._parse_result_container_lines: list[nlp_core.LineJSON] = []
        self._parse_result_container_pages: list[nlp_core.PageJSON] = []
        self._parse_result_container_paras: list[nlp_core.ParaJSON] = []
        self._parse_result_container_words: list[nlp_core.WordJSON] = []
        self._parse_result_container_words_line: list[str] = []
        self._parse_result_container_words_para: list[str] = []
        self._parse_result_font = ""
        self._parse_result_glyph_is_empty: bool = False
        self._parse_result_index_page: int = 0
        self._parse_result_llx: float = 0.0
        self._parse_result_no_fonts: int = 0
        self._parse_result_no_lines: int = 0
        self._parse_result_no_lines_in_page: int = 0
        self._parse_result_no_lines_in_para: int = 0
        self._parse_result_no_paras: int = 0
        self._parse_result_no_paras_in_page: int = 0
        self._parse_result_no_titles: int = 0
        self._parse_result_no_words: int = 0
        self._parse_result_no_words_in_line: int = 0
        self._parse_result_no_words_in_page: int = 0
        self._parse_result_no_words_in_para: int = 0
        self._parse_result_size = 0.00
        self._parse_result_table: bool = False
        self._parse_result_table_cell: int = 0
        self._parse_result_table_cell_is_empty: bool = False
        self._parse_result_table_col_span: int = 0
        self._parse_result_table_col_span_prev: int = 0
        self._parse_result_table_row: int = 0
        self._parse_result_text: str = ""
        self._parse_result_urx: float = 0.0
        self.no_errors: int = 0

        self.parse_result_no_pages = 0
        self.parse_result_titles: list[str] = []

        core_glob.cls_nlp_core = nlp_core.NLPCore()

        self._exist = True

        core_glob.logger.debug(core_glob.LOGGER_END)

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
        if core_glob.setup.verbose_parser == "all":
            print(f"{event} tag   ={parent_tag}")

            if attrib != {}:
                print(f"      attrib={attrib}")

            if text is not None and str(text).strip() > "":
                print(f"      text  ='{text}'")

    # ------------------------------------------------------------------
    # Debug an XML element only 'text' - variant line.
    # ------------------------------------------------------------------
    def _debug_xml_element_text_line(self) -> None:
        """Debug an XML element only 'text - variant line."""
        if core_glob.setup.verbose_parser == "text":
            print(
                f"pages_i_doc={self.parse_result_no_pages:2d} "
                f"paras_i_page={self._parse_result_no_paras_in_page:2d} "
                f"lines_i_page={self._parse_result_no_lines_in_page:2d} "
                f"lines_i_para={self._parse_result_no_lines_in_para:2d} "
                f"text='{self._parse_result_text}'"
            )

    # ------------------------------------------------------------------
    # Debug an XML element only 'text' - variant page.
    # ------------------------------------------------------------------
    def _debug_xml_element_text_page(self) -> None:
        """Debug an XML element only 'text - variant page."""
        if core_glob.setup.verbose_parser == "text":
            print(
                f"pages_i_doc={self.parse_result_no_pages:2d} "
                f"paras_i_page={self._parse_result_no_paras_in_page:2d} "
                f"lines_i_page={self._parse_result_no_lines_in_page:2d} "
                f"lines_i_para={self._parse_result_no_lines_in_para:2d} "
                f"text='{self._parse_result_text}'"
            )

    # ------------------------------------------------------------------
    # Debug an XML element only 'text' - variant word.
    # ------------------------------------------------------------------
    def _debug_xml_element_text_word(self) -> None:
        """Debug an XML element only 'text - variant word."""
        if core_glob.setup.verbose_parser == "text":
            print(
                f"pages_i_doc={self.parse_result_no_pages:2d} "
                f"paras_i_page={self._parse_result_no_paras_in_page:2d} "
                f"lines_i_page={self._parse_result_no_lines_in_page:2d} "
                f"lines_i_para={self._parse_result_no_lines_in_para:2d} "
                f"words_i_page={self._parse_result_no_words_in_page:2d} "
                f"words_i_para={self._parse_result_no_words_in_para:2d} "
                f"words_i_line={self._parse_result_no_words_in_line:2d} "
                f"text='{self._parse_result_text}'"
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
                case nlp_core.NLPCore.PARSE_ELEM_ACTION:
                    pass
                case nlp_core.NLPCore.PARSE_ELEM_BOOKMARK:
                    self._parse_tag_bookmark(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_TITLE:
                    self._parse_tag_title(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        process.Process.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_BOOKMARK).replace(
                            "{child_tag", other
                        )
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
                # wwe
                # case nlp_core.NLPCore.PARSE_ELEM_TEXT:
                #     self._parse_tag_text(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        process.Process.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_BOOKMARKS).replace(
                            "{child_tag", other
                        )
                    )
                    self.no_errors += 1

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag Box.
    # ------------------------------------------------------------------
    def _parse_tag_box(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Box'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case nlp_core.NLPCore.PARSE_ELEM_GLYPH:
                    self._parse_tag_glyph(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_LINE:
                    self._parse_tag_line(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_PARA:
                    self._parse_tag_para(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_PLACED_IMAGE:
                    pass
                case nlp_core.NLPCore.PARSE_ELEM_TABLE:
                    self._parse_tag_table(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_TEXT:
                    self._parse_tag_text(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_WORD:
                    self._parse_tag_word(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        process.Process.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_BOX).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag Cell.
    # ------------------------------------------------------------------
    def _parse_tag_cell(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Cell'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._parse_result_table_cell_is_empty = True

        self._parse_result_table_cell += self._parse_result_table_col_span_prev

        self._parse_result_table_col_span = parent.attrib.get(nlp_core.NLPCore.PARSE_ATTR_COL_SPAN)

        if self._parse_result_table_col_span:
            self._parse_result_table_col_span_prev = int(self._parse_result_table_col_span)
        else:
            self._parse_result_table_col_span_prev = 1

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case other:
                    core_utils.progress_msg_core(
                        process.Process.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_CELL).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        if self._parse_result_table_cell_is_empty:
            self._parse_result_llx = float(parent.attrib.get(nlp_core.NLPCore.PARSE_ATTR_LLX))
            self._parse_result_urx = float(parent.attrib.get(nlp_core.NLPCore.PARSE_ATTR_URX))
            new_entry = {
                nlp_core.NLPCore.JSON_NAME_COLUMN_NO: self._parse_result_table_cell,
                nlp_core.NLPCore.JSON_NAME_COORD_LLX: self._parse_result_llx,
                nlp_core.NLPCore.JSON_NAME_COORD_URX: self._parse_result_urx,
                nlp_core.NLPCore.JSON_NAME_LINE_NO: self._parse_result_no_lines_in_para,
                nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE: self._parse_result_index_page + 1,
                nlp_core.NLPCore.JSON_NAME_LINE_TYPE: nlp_core.NLPCore.LINE_TYPE_BODY,
                nlp_core.NLPCore.JSON_NAME_PARA_NO: self._parse_result_no_paras_in_page,
                nlp_core.NLPCore.JSON_NAME_ROW_NO: self._parse_result_table_row,
                nlp_core.NLPCore.JSON_NAME_TEXT: "",
            }

            if self._parse_result_table_col_span:
                # not testable
                new_entry[nlp_core.NLPCore.JSON_NAME_COLUMN_SPAN] = int(self._parse_result_table_col_span)

            self._parse_result_container_lines.append(new_entry)

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
                    self._parse_tag_para(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        process.Process.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_CONTENT).replace(
                            "{child_tag", other
                        )
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
                        process.Process.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_DOC_INFO).replace(
                            "{child_tag", other
                        )
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

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case other:
                    core_utils.progress_msg_core(
                        process.Process.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_FONT).replace("{child_tag", other)
                    )
                    self.no_errors += 1

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
                # wwe
                # case nlp_core.NLPCore.PARSE_ELEM_TEXT:
                #     self._parse_tag_text(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        process.Process.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_FONTS).replace("{child_tag", other)
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
                        process.Process.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_GLYPH).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        if self._parse_result_glyph_is_empty:
            self._parse_result_font = parent.attrib.get(nlp_core.NLPCore.PARSE_ATTR_GLYPH_FONT)
            self._parse_result_size = float(parent.attrib.get(nlp_core.NLPCore.PARSE_ATTR_GLYPH_SIZE))

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag Line.
    # ------------------------------------------------------------------
    def _parse_tag_line(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Line'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._parse_result_container_words = []

        self._parse_result_no_words_in_line = 0

        self._parse_result_no_lines += 1
        self._parse_result_no_lines_in_page += 1
        self._parse_result_no_lines_in_para += 1

        self._parse_result_container_words_line = []

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                # wwe
                # case nlp_core.NLPCore.PARSE_ELEM_TEXT:
                #     self._parse_tag_text(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_WORD:
                    self._parse_tag_word(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        process.Process.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_LINE).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        self._parse_result_container_lines.append(
            {
                nlp_core.NLPCore.JSON_NAME_LINE_NO: self._parse_result_no_lines,
                nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE: self._parse_result_no_lines_in_page,
                nlp_core.NLPCore.JSON_NAME_LINE_NO_PARA: self._parse_result_no_lines_in_para,
                nlp_core.NLPCore.JSON_NAME_LLX: float(parent.attrib.get(nlp_core.NLPCore.PARSE_ATTR_LLX)),
                nlp_core.NLPCore.JSON_NAME_NO_WORDS_IN_LINE: self._parse_result_no_words_in_line,
                nlp_core.NLPCore.JSON_NAME_TEXT: " ".join(self._parse_result_container_words_line),
                nlp_core.NLPCore.JSON_NAME_TYPE: nlp_core.NLPCore.LINE_TYPE_BODY,
                nlp_core.NLPCore.JSON_NAME_URX: float(parent.attrib.get(nlp_core.NLPCore.PARSE_ATTR_URX)),
                nlp_core.NLPCore.JSON_NAME_CONTAINER_WORDS: self._parse_result_container_words,
            }
        )

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag 'Page'.
    # ------------------------------------------------------------------
    # noinspection PyArgumentList
    def _parse_tag_page(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Page'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._parse_result_container_paras = []
        self.parse_result_line_lines = []

        self._parse_result_no_lines_in_page = 0
        self._parse_result_no_paras_in_page = 0
        self._parse_result_no_words_in_page = 0

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
                        process.Process.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_PAGE).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        self._parse_result_container_pages.append(
            {
                nlp_core.NLPCore.JSON_NAME_NO_LINES_IN_PAGE: self._parse_result_no_lines_in_page,
                nlp_core.NLPCore.JSON_NAME_NO_PARAS_IN_PAGE: self._parse_result_no_paras_in_page,
                nlp_core.NLPCore.JSON_NAME_NO_WORDS_IN_PAGE: self._parse_result_no_words_in_page,
                nlp_core.NLPCore.JSON_NAME_PAGE_NO: self.parse_result_no_pages,
                nlp_core.NLPCore.JSON_NAME_CONTAINER_PARAS: self._parse_result_container_paras,
            }
        )

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag 'Pages'.
    # ------------------------------------------------------------------
    # noinspection PyArgumentList
    def _parse_tag_pages(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:  # noqa: C901
        """Process tag 'Pages'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        core_glob.cls_nlp_core.document_json = {nlp_core.NLPCore.JSON_NAME_FILE_NAME: self._file_name_orig}

        if self._document_id > 0:
            core_glob.cls_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_ID] = self._document_id

        self._parse_result_container_fonts = []
        self._parse_result_container_pages = []
        self._parse_result_container_titles = []
        self.parse_result_line_pages = []

        self._parse_result_no_fonts = 0
        self._parse_result_no_lines = 0
        self.parse_result_no_pages = 0
        self._parse_result_no_paras = 0
        # wwe
        # self._parse_result_no_titles = 0
        self._parse_result_no_words = 0

        if self._is_lt_footer_required or self._is_lt_header_required:
            core_glob.line_type_header_footer = lt_hf.LineTypeHeaderFooter(
                file_name_curr=self._file_name_curr,
            )

        if self._is_lt_toc_required:
            core_glob.line_type_toc = lt_toc.LineTypeToc(
                file_name_curr=self._file_name_curr,
            )

        if self._is_lt_table_required:
            core_glob.line_type_table = lt_tab.LineTypeTable(
                file_name_curr=self._file_name_curr,
            )

        if self._is_lt_list_bullet_required:
            core_glob.line_type_list_bullet = lt_lb.LineTypeListBullet(
                file_name_curr=self._file_name_curr,
            )

        if self._is_lt_list_number_required:
            core_glob.line_type_list_number = lt_ln.LineTypeListNumber(
                file_name_curr=self._file_name_curr,
            )

        if self._is_lt_heading_required:
            core_glob.line_type_heading = lt_h.LineTypeHeading(
                file_name_curr=self._file_name_curr,
            )

        # Process the tags of all document pages.
        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case nlp_core.NLPCore.PARSE_ELEM_GRAPHICS:
                    pass
                case nlp_core.NLPCore.PARSE_ELEM_PAGE:
                    self._parse_tag_page(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_RESOURCES:
                    self._parse_tag_resources(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        process.Process.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_PAGES).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        core_glob.cls_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_FONTS] = self._parse_result_no_fonts
        core_glob.cls_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_LINES] = self._parse_result_no_lines

        if self._is_lt_footer_required:
            core_glob.cls_nlp_core.document_json[
                nlp_core.NLPCore.JSON_NAME_NO_LINES_FOOTER
            ] = core_glob.line_type_header_footer.no_lines_footer

        if self._is_lt_header_required:
            core_glob.cls_nlp_core.document_json[
                nlp_core.NLPCore.JSON_NAME_NO_LINES_HEADER
            ] = core_glob.line_type_header_footer.no_lines_header

        if self._is_lt_toc_required:
            core_glob.cls_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_LINES_TOC] = core_glob.line_type_toc.no_lines_toc

        if self._is_lt_list_bullet_required:
            core_glob.cls_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_LISTS_BULLET] = core_glob.line_type_list_bullet.no_lists

        if self._is_lt_list_number_required:
            core_glob.cls_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_LISTS_NUMBER] = core_glob.line_type_list_number.no_lists

        core_glob.cls_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_PAGES] = self.parse_result_no_pages
        core_glob.cls_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_PARAS] = self._parse_result_no_paras

        if self._is_lt_table_required:
            core_glob.cls_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_TABLES] = core_glob.line_type_table.no_tables

        # wwe
        # if self.parse_result_titles:
        #     self._parse_result_document[nlp_core.NLPCore.JSON_NAME_NO_TITLES] = self._parse_result_no_titles

        core_glob.cls_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_WORDS] = self._parse_result_no_words

        core_glob.cls_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_FONTS] = self._parse_result_container_fonts
        core_glob.cls_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES] = self._parse_result_container_pages

        if self._is_lt_footer_required or self._is_lt_header_required:
            core_glob.line_type_header_footer.process_document(
                file_name_curr=self._file_name_curr,
            )

        if self._is_lt_toc_required:
            core_glob.line_type_toc.process_document(
                file_name_curr=self._file_name_curr,
            )

        if self._is_lt_table_required:
            core_glob.line_type_table.process_document(
                file_name_curr=self._file_name_curr,
                directory_name=self._directory_name,
                document_id=self._document_id,
                file_name_orig=self._file_name_orig,
            )

        if self._is_lt_list_bullet_required:
            core_glob.line_type_list_bullet.process_document(
                directory_name=self._directory_name,
                document_id=self._document_id,
                environment_variant=self._environment_variant,
                file_name_curr=self._file_name_curr,
                file_name_orig=self._file_name_orig,
            )

        if self._is_lt_list_number_required:
            core_glob.line_type_list_number.process_document(
                directory_name=self._directory_name,
                document_id=self._document_id,
                environment_variant=self._environment_variant,
                file_name_curr=self._file_name_curr,
                file_name_orig=self._file_name_orig,
            )

        if self._is_lt_heading_required:
            core_glob.line_type_heading.process_document(
                directory_name=self._directory_name,
                document_id=self._document_id,
                file_name_curr=self._file_name_curr,
                file_name_orig=self._file_name_orig,
            )

        with open(self._full_name, "w", encoding=core_glob.FILE_ENCODING_DEFAULT) as file_handle:
            json.dump(
                core_glob.cls_nlp_core.document_json,
                file_handle,
                indent=core_glob.setup.json_indent,
                sort_keys=core_glob.setup.is_json_sort_keys,
            )

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag Para.
    # ------------------------------------------------------------------
    def _parse_tag_para(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Para'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._parse_result_container_lines = []

        self._parse_result_no_lines_in_para = 0
        self._parse_result_no_words_in_para = 0

        self._parse_result_no_paras += 1
        self._parse_result_no_paras_in_page += 1

        self._parse_result_container_words_para = []

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case nlp_core.NLPCore.PARSE_ELEM_A:
                    pass
                case nlp_core.NLPCore.PARSE_ELEM_BOX:
                    self._parse_tag_box(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_PARA:
                    self._parse_tag_para(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        process.Process.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_PARA).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        self._parse_result_container_paras.append(
            {
                nlp_core.NLPCore.JSON_NAME_NO_LINES_IN_PARA: self._parse_result_no_lines_in_para,
                nlp_core.NLPCore.JSON_NAME_NO_WORDS_IN_PARA: self._parse_result_no_words_in_para,
                nlp_core.NLPCore.JSON_NAME_PARA_NO: self._parse_result_no_paras,
                nlp_core.NLPCore.JSON_NAME_PARA_NO_PAGE: self._parse_result_no_paras_in_page,
                nlp_core.NLPCore.JSON_NAME_TEXT: " ".join(self._parse_result_container_words_para),
                nlp_core.NLPCore.JSON_NAME_CONTAINER_LINES: self._parse_result_container_lines,
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
                # wwe
                # case nlp_core.NLPCore.PARSE_ELEM_TEXT:
                #     self._parse_tag_text(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_COLOR_SPACES:
                    pass
                case other:
                    core_utils.progress_msg_core(
                        process.Process.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_RESOURCES).replace(
                            "{child_tag", other
                        )
                    )
                    self.no_errors += 1

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag Row.
    # ------------------------------------------------------------------
    def _parse_tag_row(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Row'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._parse_result_table_row += 1
        self._parse_result_table_cell = 0
        self._parse_result_table_col_span_prev = 1

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case nlp_core.NLPCore.PARSE_ELEM_CELL:
                    self._parse_tag_cell(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        process.Process.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_ROW).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag Table.
    # ------------------------------------------------------------------
    def _parse_tag_table(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Table'.

        Args:
            parent_tag (str): Parent tag.
            parent (collections.abc.Iterable[str]): Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._parse_result_table = True
        self._parse_result_table_row = 0

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case nlp_core.NLPCore.PARSE_ELEM_ROW:
                    self._parse_tag_row(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        process.Process.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_TABLE).replace("{child_tag", other)
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
                # wwe
                # case nlp_core.NLPCore.PARSE_ELEM_BOX:
                #     self._parse_tag_box(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        process.Process.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_WORD).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        self._parse_result_text = parent.text

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # ------------------------------------------------------------------
    # Processing tag Title.
    # ------------------------------------------------------------------
    def _parse_tag_title(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Process tag 'Title'.

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
                        process.Process.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_TITLE).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        self.parse_result_titles.append(parent.text)

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
        self._parse_result_no_words_in_line += 1
        self._parse_result_no_words_in_page += 1
        self._parse_result_no_words_in_para += 1

        for child in parent:
            child_tag = child.tag[nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case nlp_core.NLPCore.PARSE_ELEM_BOX:
                    self._parse_tag_box(child_tag, child)
                case nlp_core.NLPCore.PARSE_ELEM_TEXT:
                    self._parse_tag_text(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        process.Process.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_WORD).replace("{child_tag", other)
                    )
                    self.no_errors += 1

        self._parse_result_container_words.append(
            {
                nlp_core.NLPCore.JSON_NAME_FONT: self._parse_result_font,
                nlp_core.NLPCore.JSON_NAME_SIZE: self._parse_result_size,
                nlp_core.NLPCore.JSON_NAME_TEXT: self._parse_result_text,
                nlp_core.NLPCore.JSON_NAME_WORD_NO: self._parse_result_no_words,
                nlp_core.NLPCore.JSON_NAME_WORD_NO_LINE: self._parse_result_no_words_in_line,
                nlp_core.NLPCore.JSON_NAME_WORD_NO_PAGE: self._parse_result_no_words_in_page,
                nlp_core.NLPCore.JSON_NAME_WORD_NO_PARA: self._parse_result_no_words_in_para,
            }
        )

        self._parse_result_container_words_line.append(self._parse_result_text)
        self._parse_result_container_words_para.append(self._parse_result_text)

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
            core_glob.cls_nlp_core.exists()
        except AttributeError:
            core_glob.cls_nlp_core = nlp_core.NLPCore()

        with open(full_name, "r", encoding=file_encoding) as file_handle:
            core_glob.cls_nlp_core.document_json = json.load(file_handle)

        core_glob.logger.debug(core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Processing tag 'Document'.
    # ------------------------------------------------------------------
    def parse_tag_document(  # pylint: disable=too-many-arguments
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
        is_lt_table_required: bool,
        is_lt_toc_required: bool,
        no_pdf_pages: int,
        parent: collections.abc.Iterable[str],
        parent_tag: str,
    ) -> None:
        """Process tag 'Document'.

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
            is_lt_table_required (bool):
                If it is set to **`true`**, the determination of the table lines is performed.
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
        core_glob.logger.debug("param is_lt_table_required      =%s", is_lt_table_required)
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
        self._is_lt_table_required = is_lt_table_required
        self._is_lt_toc_required = is_lt_toc_required
        self._no_pdf_pages = no_pdf_pages

        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        core_glob.cls_nlp_core.document_json = {}

        self.no_errors = 0

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
                    self._parse_tag_pages(child_tag, child)
                case other:
                    core_utils.progress_msg_core(
                        process.Process.ERROR_61_902.replace("{parent_tag}", nlp_core.NLPCore.PARSE_ELEM_DOCUMENT).replace(
                            "{child_tag", other
                        )
                    )
                    self.no_errors += 1

            self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

        core_glob.logger.debug(core_glob.LOGGER_END)
