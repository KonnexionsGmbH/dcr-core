# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Determines the headers and footers of a parsed PDF document.

Typical usage example:

    my_instance = LineTypeHeaderFooter()

    if my_instance.exists():

    my_instance.process_document(parse_line_pages_json = my_pages)
"""
from __future__ import annotations

import jellyfish

import dcr_core.cls_nlp_core as nlp_core
from dcr_core import core_glob
from dcr_core import core_utils


# pylint: disable=too-many-instance-attributes
class LineTypeHeaderFooter:
    """Determines the headers and footers of a parsed PDF document."""

    # --------------------------------------------------------------------------
    # Tuple content:
    #       (line_no_page - 1,
    #        text)
    # --------------------------------------------------------------------------
    _CandLinesPage = list[tuple[int, str]]
    _CandLinesPages = list[_CandLinesPage]

    _PATTERN_NAME_LEVENSHTEIN_DISTANCE = "Levenshtein distance"

    # --------------------------------------------------------------------------
    # Tuple content:
    #       (is line header or footer,
    #        pattern name,
    #        number of affected pages)
    # --------------------------------------------------------------------------
    _ResultDoc = list[tuple[bool, str, int]]
    _ResultPages = list[list[bool]]

    _VARIANT_FOOTER = "Footer"
    _VARIANT_HEADER = "Header"

    # ------------------------------------------------------------------
    # Initialise the instance.
    # ------------------------------------------------------------------
    def __init__(
        self,
        file_name_curr: str = "",
    ) -> None:
        """Initialise an instance.

        Args:
            file_name_curr (str, optional): File name of the PDF document to be processed -
                only for documentation purposes. Defaults to "".
        """
        try:
            core_glob.logger.debug(core_glob.LOGGER_START)
        except AttributeError:
            core_glob.initialise_logger()
            core_glob.logger.debug(core_glob.LOGGER_START)

        core_glob.logger.debug("param file_name_curr=%s", file_name_curr)

        core_utils.check_exists_object(
            is_nlp_core=True,
            is_setup=True,
            is_text_parser=True,
        )

        self._cand_lines_footer_pages: LineTypeHeaderFooter._CandLinesPages = []
        self._cand_lines_footer_template: LineTypeHeaderFooter._CandLinesPage = []
        self._cand_lines_header_pages: LineTypeHeaderFooter._CandLinesPages = []
        self._cand_lines_header_template: LineTypeHeaderFooter._CandLinesPage = []
        self._current_pattern_name = ""

        self._file_name_curr = file_name_curr

        self._is_complete_footer = False
        self._is_complete_header = False
        self._is_required_footer = False
        self._is_required_header = False
        self._is_result_footer = False
        self._is_result_header = False

        self._no_footers = 0
        self._no_headers = 0
        self._no_lines_line_type_footer = 0
        self._no_lines_line_type_header = 0
        self._no_pages = 0

        self._result_doc_footer: LineTypeHeaderFooter._ResultDoc = []
        self._result_doc_header: LineTypeHeaderFooter._ResultDoc = []
        self._result_pages_footer: LineTypeHeaderFooter._ResultPages = []
        self._result_pages_header: LineTypeHeaderFooter._ResultPages = []

        self._exist = True

        core_glob.logger.debug(core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Apply the test patterns.
    # ------------------------------------------------------------------
    def _apply_patterns(self) -> None:
        """Apply the test patterns."""
        self._debug_lt("Apply the different test patterns - Start")
        self._debug_lt("-" * 80)

        self._current_pattern_name = LineTypeHeaderFooter._PATTERN_NAME_LEVENSHTEIN_DISTANCE
        self._pattern_levenshtein()
        if self._is_complete_header and self._is_complete_footer:
            self._debug_lt("-" * 80)
            self._debug_lt("Apply the different test patterns - End with pattern Levenshtein distance")
            self._debug_lt("=" * 80)
            return

        self._debug_lt("-" * 80)
        self._debug_lt("Apply the different test patterns - End")
        self._debug_lt("=" * 80)

    # ------------------------------------------------------------------
    # Determine the candidate lines from a page.
    # ------------------------------------------------------------------
    def _create_cand_from_page(self, lines_json: list[nlp_core.NLPCore.LineJSON]) -> None:
        """Determine the candidate lines from a page."""
        if self._is_required_header:
            self._create_cand_from_page_header(lines_json)

        if self._is_required_footer:
            self._create_cand_from_page_footer(lines_json)

    # ------------------------------------------------------------------
    # Determine the candidate lines from a page - footer.
    # ------------------------------------------------------------------
    def _create_cand_from_page_footer(self, lines_json: list[nlp_core.NLPCore.LineJSON]) -> None:
        """Determine the candidate lines from a page - footer."""
        page = self._create_cand_template_page(core_glob.inst_setup.lt_footer_max_lines)

        if lines_json:
            idx_line_page = len(lines_json) - 1
            for idx_cand in range(core_glob.inst_setup.lt_footer_max_lines - 1, -1, -1):
                page[idx_cand] = (
                    idx_line_page,
                    lines_json[idx_line_page][nlp_core.NLPCore.JSON_NAME_TEXT],
                )

                idx_line_page -= 1
                if idx_line_page < 0:
                    break

        self._cand_lines_footer_pages.append(page)

        if core_glob.inst_setup.is_verbose_lt_header_footer:
            self._debug_lt(LineTypeHeaderFooter._VARIANT_FOOTER + " candidates:")
            for idx, text in page:
                self._debug_lt(f"Line no. page={idx} - text={text[:50] + ' ...'}")

    # ------------------------------------------------------------------
    # Determine the candidate lines from a page - header.
    # ------------------------------------------------------------------
    def _create_cand_from_page_header(self, lines_json: list[nlp_core.NLPCore.LineJSON]) -> None:
        """Determine the candidate lines from a page - header."""
        page = self._create_cand_template_page(core_glob.inst_setup.lt_header_max_lines)

        if lines_json:
            for idx_cand in range(core_glob.inst_setup.lt_header_max_lines):
                if idx_cand < len(lines_json):
                    page[idx_cand] = (
                        idx_cand,
                        lines_json[idx_cand][nlp_core.NLPCore.JSON_NAME_TEXT],
                    )
                else:
                    break

        self._cand_lines_header_pages.append(page)

        if core_glob.inst_setup.is_verbose_lt_header_footer:
            self._debug_lt(LineTypeHeaderFooter._VARIANT_HEADER + " candidates:")
            for idx, text in page:
                self._debug_lt(f"Line no. page={idx} - text={text[:50] + ' ...'}")

    # ------------------------------------------------------------------
    # Create the candidate template page.
    # ------------------------------------------------------------------
    @staticmethod
    def _create_cand_template_page(lt_max_lines: int) -> LineTypeHeaderFooter._CandLinesPage:
        """Create the candidate template page.

        Args:
            lt_max_lines (int):
                The maximum number of expected candidate lines.

        Returns:
            LineTypeHeaderFooter.CandLinesPage:
                An initialised line container.
        """
        line = (-1, "")
        page = []

        for _ in range(lt_max_lines):
            page.append(line)

        return page

    # ------------------------------------------------------------------
    # Create the result array template.
    # ------------------------------------------------------------------
    @staticmethod
    def _create_result_template(lt_max_lines: int) -> LineTypeHeaderFooter._ResultDoc:
        """Create the result array template.

        Args:
            lt_max_lines (int):
                The maximum number of expected candidate lines.

        Returns:
            LineTypeHeaderFooter.ResultDoc:
                An initialised result container.
        """
        page: list[tuple[bool, str, int]] = []

        for _ in range(lt_max_lines):
            page.append((False, "", 0))

        return page

    # ------------------------------------------------------------------
    # Debug line type processing.
    # ------------------------------------------------------------------
    @staticmethod
    def _debug_lt(msg: str) -> None:
        """Debug line type processing.

        Args:
            msg (str): Debug message.
        """
        core_utils.progress_msg(
            core_glob.inst_setup.is_verbose_lt_header_footer,
            "LineTypeHeaderFooter: " + msg,
        )

    # ------------------------------------------------------------------
    # Initialize the candidate data structures.
    # ------------------------------------------------------------------
    def _init_cand(self) -> None:
        """Initialize the candidate data structures."""
        self._debug_lt("Create line candidates - Start")

        self._cand_lines_header_template = self._create_cand_template_page(core_glob.inst_setup.lt_header_max_lines)

        for page_idx, page_json in enumerate(core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES]):
            self._debug_lt("-" * 80)
            self._debug_lt(f"Page {page_idx+1}")
            self._debug_lt("-" * 80)
            self._create_cand_from_page(page_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_LINES])

        self._debug_lt("-" * 80)
        self._debug_lt("Create line candidates - End")
        self._debug_lt("=" * 80)

    # ------------------------------------------------------------------
    # Initialize the result array for the whole document.
    # ------------------------------------------------------------------
    def _init_result_doc(self) -> None:
        """Initialize the result array for the whole document."""
        self._result_doc_header = self._create_result_template(core_glob.inst_setup.lt_header_max_lines)
        self._result_pages_header = []

        self._result_doc_footer = self._create_result_template(core_glob.inst_setup.lt_footer_max_lines)
        self._result_pages_footer = []

        for _ in range(self._no_pages):
            self._result_pages_header.append([False for _ in range(core_glob.inst_setup.lt_header_max_lines)])
            self._result_pages_footer.append([False for _ in range(core_glob.inst_setup.lt_footer_max_lines)])

    # ------------------------------------------------------------------
    # Pattern: Levenshtein distance.
    # ------------------------------------------------------------------
    def _pattern_levenshtein(
        self,
    ) -> None:
        """Pattern: Levenshtein distance."""
        self._debug_lt("Pattern Levenshtein distance - Start")
        self._debug_lt("-" * 80)

        if self._is_required_header:
            self._result_doc_header, self._result_pages_header = self._pattern_levenshtein_distance(
                LineTypeHeaderFooter._VARIANT_HEADER,
                core_glob.inst_setup.lt_header_max_distance,
                self._cand_lines_header_pages,
                self._result_doc_header,
                self._result_pages_header,
            )
            self._is_complete_header = all(value_doc for value_doc in self._result_doc_header)

        if self._is_required_footer:
            self._result_doc_footer, self._result_pages_footer = self._pattern_levenshtein_distance(
                LineTypeHeaderFooter._VARIANT_FOOTER,
                core_glob.inst_setup.lt_footer_max_distance,
                self._cand_lines_footer_pages,
                self._result_doc_footer,
                self._result_pages_footer,
            )
            self._is_complete_footer = all(value_doc for value_doc in self._result_doc_footer)

        self._debug_lt("-" * 80)
        self._debug_lt("Pattern Levenshtein distance - End")
        self._debug_lt("=" * 80)

    # ------------------------------------------------------------------
    # Pattern: Levenshtein distance.
    # ------------------------------------------------------------------
    def _pattern_levenshtein_distance(
        self,
        variant: str,
        lt_max_distance: int,
        cand_lines_pages: LineTypeHeaderFooter._CandLinesPages,
        result_doc: LineTypeHeaderFooter._ResultDoc,
        result_pages: LineTypeHeaderFooter._ResultPages,
    ) -> tuple[LineTypeHeaderFooter._ResultDoc, LineTypeHeaderFooter._ResultPages]:
        """Pattern: Levenshtein distance.

        Args:
            variant (str):
                variant is 'header' or 'footer'.
            lt_max_distance (int):
                Maximum Levenshtein distance for two consecutive lines.
            cand_lines_pages (LineTypeHeaderFooter.CandLinesPages):
                All the candidate lines.
            result_doc (LineTypeHeaderFooter.ResultDoc):
                Document-related result.
            result_pages (LineTypeHeaderFooter.ResultPages):
                Page-related results.

        Returns:
            tuple(LineTypeHeaderFooter.ResultDoc, LineTypeHeaderFooter.ResultPages):
                The modified results.
        """
        core_glob.logger.debug(core_glob.LOGGER_START)
        core_glob.logger.debug("param variant                   =%s", variant)
        core_glob.logger.debug("param lt_max_distance           =%i", lt_max_distance)
        core_glob.logger.debug("param cand_lines_pages          =%s", str(cand_lines_pages)[:100])
        core_glob.logger.debug("param result_doc                =%s", str(result_doc))
        core_glob.logger.debug("param result_pages              =%s", str(result_pages)[:100])

        result_pages = self._reset_result_pages(result_doc, result_pages)

        for idx_line, (value_doc, _, _) in enumerate(result_doc):
            if value_doc:
                continue

            for idx_page in range(self._no_pages - 1):
                if cand_lines_pages[idx_page][idx_line][0] == -1 or cand_lines_pages[idx_page + 1][idx_line][0] == -1:
                    continue

                if (
                    jellyfish.levenshtein_distance(
                        cand_lines_pages[idx_page][idx_line][1],
                        cand_lines_pages[idx_page + 1][idx_line][1],
                    )
                    <= lt_max_distance
                ):
                    result_pages[idx_page][idx_line] = True
                    result_pages[idx_page + 1][idx_line] = True

        result_doc = self._update_result_doc(result_doc, result_pages)

        if core_glob.inst_setup.is_verbose_lt_header_footer:
            self._debug_lt(variant + " results")

            for idx_line, (value_doc, _, _) in enumerate(result_doc):
                self._debug_lt(f"Line no={idx_line} - value={value_doc}")

        core_glob.logger.debug(core_glob.LOGGER_END)

        return result_doc, result_pages

    # ------------------------------------------------------------------
    # Reset the result pages.
    # ------------------------------------------------------------------
    @staticmethod
    def _reset_result_pages(
        result_doc: LineTypeHeaderFooter._ResultDoc,
        result_pages: LineTypeHeaderFooter._ResultPages,
    ) -> LineTypeHeaderFooter._ResultPages:
        """Reset the result pages.

        Args:
            result_doc (LineTypeHeaderFooter.ResultDoc):
                Document-related result.
            result_pages (LineTypeHeaderFooter.ResultPages):
                Page-related results.
        """
        for idx_line, (value_doc, _, _) in enumerate(result_doc):
            if not value_doc:
                for idx_page, value_line in enumerate(result_pages):
                    if value_line:
                        result_pages[idx_page][idx_line] = False

        return result_pages

    # ------------------------------------------------------------------
    # Pattern: Levenshtein distance.
    # ------------------------------------------------------------------
    def _store_results_variant(
        self,
        variant: str,
        line_type: str,
        cand_lines_pages: LineTypeHeaderFooter._CandLinesPages,
        result_doc: LineTypeHeaderFooter._ResultDoc,
        result_pages: LineTypeHeaderFooter._ResultPages,
    ) -> None:
        """Pattern: Levenshtein distance.

        Args:
            variant (str):
                variant is 'header' or 'footer'.
            line_type (str):
                Maximum Levenshtein distance for two consecutive lines.
            cand_lines_pages (LineTypeHeaderFooter.CandLinesPages):
                All the candidate lines.
            result_doc (LineTypeHeaderFooter.ResultDoc):
                Document-related result.
            result_pages (LineTypeHeaderFooter.ResultPages):
                Page-related results.
        """
        core_glob.logger.debug(core_glob.LOGGER_START)
        core_glob.logger.debug("param variant                   =%s", variant)
        core_glob.logger.debug("param line_type                 =%s", line_type)
        core_glob.logger.debug("param cand_lines_pages          =%s", str(cand_lines_pages)[:100])
        core_glob.logger.debug("param result_doc                =%s", str(result_doc))
        core_glob.logger.debug("param result_pages              =%s", str(result_pages)[:100])

        self._debug_lt(variant + f" results - line_type={line_type}")

        for idx_line, (value_doc, pattern_name, no_pages) in enumerate(result_doc):
            if not value_doc:
                continue

            if line_type == nlp_core.NLPCore.LINE_TYPE_HEADER:
                self._no_headers += 1
            else:
                self._no_footers += 1

            for idx_page in range(self._no_pages):
                if not result_pages[idx_page][idx_line]:
                    continue

                core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES][idx_page][
                    nlp_core.NLPCore.JSON_NAME_CONTAINER_LINES
                ][cand_lines_pages[idx_page][idx_line][0]][nlp_core.NLPCore.JSON_NAME_TYPE]: str = line_type

                if line_type == nlp_core.NLPCore.LINE_TYPE_HEADER:
                    self._no_lines_line_type_header += 1
                else:
                    self._no_lines_line_type_footer += 1

                line_no: int = core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES][idx_page][
                    nlp_core.NLPCore.JSON_NAME_CONTAINER_LINES
                ][cand_lines_pages[idx_page][idx_line][0]][nlp_core.NLPCore.JSON_NAME_LINE_NO]

                para_no_page: int = core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES][idx_page][
                    nlp_core.NLPCore.JSON_NAME_CONTAINER_LINES
                ][cand_lines_pages[idx_page][idx_line][0]][nlp_core.NLPCore.JSON_NAME_PARA_NO_PAGE]

                for word in core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES][idx_page][
                    nlp_core.NLPCore.JSON_NAME_CONTAINER_PARAS
                ][para_no_page - 1][nlp_core.NLPCore.JSON_NAME_CONTAINER_WORDS]:
                    if word[nlp_core.NLPCore.JSON_NAME_LINE_NO] == line_no - 1:
                        word[nlp_core.NLPCore.JSON_NAME_TYPE] = line_type

            self._debug_lt(f"Relative line number={idx_line+1:2d} Affected pages={no_pages:3d} Pattern={pattern_name}")

        core_glob.logger.debug(core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Store the results in the JSON document.
    # ------------------------------------------------------------------
    def _store_results(self) -> None:
        """Store the results in the JSON document."""
        self._debug_lt("Store the results obtained - Start")
        self._debug_lt("-" * 80)
        self._debug_lt(f"Pages {self._no_pages}")

        if self._is_required_header:
            if any(value_doc for value_doc in self._result_doc_header):
                self._store_results_variant(
                    LineTypeHeaderFooter._VARIANT_HEADER,
                    nlp_core.NLPCore.LINE_TYPE_HEADER,
                    self._cand_lines_header_pages,
                    self._result_doc_header,
                    self._result_pages_header,
                )
            core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_HEADERS] = self._no_headers
            core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_LINES_HEADER] = self._no_lines_line_type_header

        if self._is_required_footer:
            if any(value_doc for value_doc in self._result_doc_footer):
                self._store_results_variant(
                    LineTypeHeaderFooter._VARIANT_FOOTER,
                    nlp_core.NLPCore.LINE_TYPE_FOOTER,
                    self._cand_lines_footer_pages,
                    self._result_doc_footer,
                    self._result_pages_footer,
                )
            core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_FOOTERS] = self._no_footers
            core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_LINES_FOOTER] = self._no_lines_line_type_footer

        self._debug_lt("-" * 80)
        self._debug_lt("Store the results obtained - End")
        self._debug_lt("=" * 80)

    # ------------------------------------------------------------------
    # Update the document related results.
    # ------------------------------------------------------------------
    def _update_result_doc(  # noqa: C901
        self,
        result_doc: LineTypeHeaderFooter._ResultDoc,
        result_pages: LineTypeHeaderFooter._ResultPages,
    ) -> LineTypeHeaderFooter._ResultDoc:
        """Update the document related results.

        Args:
            result_doc (LineTypeHeaderFooter.ResultDoc):
                Document-related result.
            result_pages (LineTypeHeaderFooter.ResultPages):
                Page-related results.

        Returns:
            LineTypeHeaderFooter.ResultDoc:
                The updated document-related results.
        """
        for idx_line, (value_doc, _, _) in enumerate(result_doc):
            if value_doc:
                continue

            is_first = False
            is_last = False
            is_rest = True
            no_lines = 0

            for idx_page in range(self._no_pages):
                if result_pages[idx_page][idx_line]:
                    no_lines += 1

                if idx_page == 0:
                    is_first = result_pages[idx_page][idx_line]
                elif idx_page == self._no_pages - 1:
                    is_last = result_pages[idx_page][idx_line]
                elif not result_pages[idx_page][idx_line]:
                    is_rest = False

            if self._no_pages == 2:
                if is_first and is_last:
                    result_doc[idx_line] = (True, self._current_pattern_name, no_lines)
            elif is_rest:
                result_doc[idx_line] = (True, self._current_pattern_name, no_lines)

        return result_doc

    # ------------------------------------------------------------------
    # Check the object existence.
    # ------------------------------------------------------------------
    def exists(self) -> bool:
        """Check the existence of the instance.

        Returns:
            bool: Always true.
        """
        return self._exist

    # ------------------------------------------------------------------
    # Process the document related data.
    # ------------------------------------------------------------------
    def process_document(
        self,
        file_name_curr: str = "",
    ) -> None:
        """Process the document related data.

        Args:
            file_name_curr (str, optional): File name of the PDF document to be processed -
                only for documentation purposes. Defaults to "".
        """
        core_glob.logger.debug(core_glob.LOGGER_START)
        core_glob.logger.debug("param file_name_curr =%s", file_name_curr)

        self._debug_lt("=" * 80)
        self._debug_lt(f"Start document                       ={self._file_name_curr}")
        self._debug_lt("-" * 37)
        self._debug_lt(f"lt_footer_max_distance={core_glob.inst_setup.lt_footer_max_distance}")
        self._debug_lt(f"lt_footer_max_lines   ={core_glob.inst_setup.lt_footer_max_lines}")
        self._debug_lt(f"lt_header_max_distance={core_glob.inst_setup.lt_header_max_distance}")
        self._debug_lt(f"lt_header_max_lines   ={core_glob.inst_setup.lt_header_max_lines}")
        self._debug_lt("-" * 80)

        core_utils.check_exists_object(
            is_nlp_core=True,
            is_setup=True,
            is_text_parser=True,
        )

        self._no_footers = 0
        self._no_headers = 0
        self._no_lines_footer = 0
        self._no_lines_header = 0

        # Neither the identification of headers nor footers is desired.
        if core_glob.inst_setup.lt_footer_max_lines == 0 and core_glob.inst_setup.lt_header_max_lines == 0:
            self._debug_lt("End (not required)")
            self._debug_lt("=" * 80)
            return

        self._file_name_curr = file_name_curr

        self._no_pages = core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_PAGES]

        self._is_complete_footer = False
        self._is_complete_header = False

        self._is_required_header = core_glob.inst_setup.lt_header_max_lines != 0
        self._is_required_footer = core_glob.inst_setup.lt_footer_max_lines != 0

        if self._no_pages == 1:
            self._debug_lt("End (document size only one page)")
            self._debug_lt("=" * 80)
            return

        # ------------------------------------------------------------------
        # Initialise the candidate data structures.
        # ------------------------------------------------------------------
        self._init_cand()

        self._init_result_doc()

        self._apply_patterns()

        self._store_results()

        self._debug_lt(f"End   document                       ={self._file_name_curr}")
        self._debug_lt("=" * 80)

        core_glob.logger.debug(core_glob.LOGGER_END)
