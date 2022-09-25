# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Determine table of content lines.

Typical usage example:

    my_instance = LineTypeToc()

    if my_instance.exists():

    my_instance.process_document(file_name_curr = my_file_name_curr,
                                 line_pages_json = my_line_pages_json)
"""
from __future__ import annotations

import dcr_core.cls_nlp_core as nlp_core
from dcr_core import core_glob
from dcr_core import core_utils


class LineTypeToc:
    """Determine table of content lines."""

    # ------------------------------------------------------------------
    # Initialise the instance.
    # ------------------------------------------------------------------
    def __init__(
        self,
        file_name_curr: str = "",
    ) -> None:
        """Initialise the instance.

        Args:
            file_name_curr (str, optional): File name of the PDF document to be processed -
                                            only for documentation purposes.
                                            Defaults to "".
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

        self._file_name_curr = file_name_curr

        self._is_toc_existing = False

        self._lines_json: list[nlp_core.NLPCore.LineJSON] = []

        self._page_no = 0

        self._strategy = ""

        # page_no_toc, page_no, para_no_page, line_no_page or row_no
        self._toc_candidates: list[list[int]] = []

        self.no_lines_toc = 0

        self._exist = True

        core_glob.logger.debug(core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Check a TOC candidate.
    # ------------------------------------------------------------------
    def _check_toc_candidate(self) -> None:  # noqa: C901
        if not self._toc_candidates:
            return

        self._debug_lt("=" * 80)
        self._debug_lt(f"Start check TOC candidate            ={len(self._toc_candidates)}")
        self._debug_lt("-" * 80)

        row_no = 0
        page_no_max = core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_PAGES]
        page_no_toc_last = -1
        idx_last = 0

        for idx, [page_no_toc, page_no, _, line_no_page] in enumerate(self._toc_candidates):
            row_no += 1

            if page_no_toc == -1:
                continue

            text_original = core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES][page_no - 1][
                nlp_core.NLPCore.JSON_NAME_CONTAINER_LINES
            ][line_no_page - 1][nlp_core.NLPCore.JSON_NAME_TEXT]

            if page_no_toc == -2:
                if row_no != 1:
                    self._init_toc_candidate()
                    self._debug_lt("End   check TOC candidate (!=)       " + f"={text_original}")
                    return
                continue

            # Page numbers not ascending
            if page_no_toc < page_no_toc_last:
                self._toc_candidates[idx][0] = -1
                self._debug_lt("Break: page numbers not ascending    " + f"={text_original}")
                break

            # Not a page number
            if page_no_toc > page_no_max:
                self._toc_candidates[idx][0] = -1
                self._debug_lt("Break: not a page number             " + f"={text_original}")
                break

            page_no_toc_last = page_no_toc
            idx_last = idx

        # Delete unnecessary entries at the end of the list
        for idx, _ in reversed(list(enumerate(self._toc_candidates))):
            if idx_last < idx:
                del self._toc_candidates[idx]
            else:
                break

        if len(self._toc_candidates) <= 1:
            self._toc_candidates = []
        else:
            # Correction of page numbers: page_no_toc
            page_no_toc_last = 0

            for idx, [page_no_toc, page_no, _, line_no_page] in enumerate(self._toc_candidates):
                self._debug_lt("TOC text                             " + f"={text_original}")
                if page_no_toc == -1:
                    self._toc_candidates[idx][0] = page_no_toc_last
                else:
                    page_no_toc_last = page_no_toc

            self._is_toc_existing = True

        self._debug_lt("-" * 80)
        self._debug_lt("End   check TOC candidate            " + f"={self._is_toc_existing}")

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
            core_glob.inst_setup.is_verbose_lt_toc,
            "LineTypeToc: " + msg,
        )

    # ------------------------------------------------------------------
    # Initialise the TOC candidate variables.
    # ------------------------------------------------------------------
    def _init_toc_candidate(self) -> None:
        self._toc_candidates = []

    # ------------------------------------------------------------------
    # Process the page-related data - line version.
    # ------------------------------------------------------------------
    def _process_page_lines(self) -> None:
        """Process the page-related data - line version."""
        if self._is_toc_existing or self._page_no >= core_glob.inst_setup.lt_toc_last_page:
            return

        self._page_no += 1

        self._debug_lt("=" * 80)
        self._debug_lt(f"Start page (lines)                   ={self._page_no}")
        self._debug_lt("-" * 80)

        gap = -1
        is_started = False

        for line_json in self._lines_json:
            if (
                line_json[nlp_core.NLPCore.JSON_NAME_TYPE] == nlp_core.NLPCore.LINE_TYPE_BODY
                or line_json[nlp_core.NLPCore.JSON_NAME_TYPE] == nlp_core.NLPCore.LINE_TYPE_TABLE
            ):
                if (text := line_json[nlp_core.NLPCore.JSON_NAME_TEXT]) != "":
                    line_tokens = text[:-1].split() if text[-1] == "." else text.split()
                    try:
                        self._process_toc_candidate_line_line(line_json, int(line_tokens[-1]))
                        gap = 0
                        is_started = True
                        self._debug_lt(f"Candidate                            ={text}")
                    except ValueError:
                        if not is_started:
                            continue
                        if 0 <= gap <= 3:
                            self._process_toc_candidate_line_line(line_json, -1)
                            gap += 1
                            self._debug_lt(f"Candidate                            ={text}")
                            continue
                        self._check_toc_candidate()
                        if self._is_toc_existing:
                            break
                        is_started = False

        self._debug_lt("-" * 80)
        self._debug_lt(f"End   page (lines)                   ={self._page_no}")

    # ------------------------------------------------------------------
    # Process the page-related data - table version.
    # ------------------------------------------------------------------
    def _process_page_table(self) -> None:
        """Process the page-related data - table version."""
        if self._is_toc_existing or self._page_no >= core_glob.inst_setup.lt_toc_last_page:
            return

        self._page_no += 1

        self._debug_lt("=" * 80)
        self._debug_lt(f"Start page (table)                   ={self._page_no}")
        self._debug_lt("-" * 80)

        for line_json in self._lines_json:
            if line_json[nlp_core.NLPCore.JSON_NAME_TYPE] == nlp_core.NLPCore.LINE_TYPE_TABLE:
                self._debug_lt(f"Candidate                            ={line_json[nlp_core.NLPCore.JSON_NAME_TEXT]}")
                if line_json[nlp_core.NLPCore.JSON_NAME_TABLE_ROW_NO] > 0:
                    self._process_toc_candidate_table_line(line_json)
                else:
                    self._check_toc_candidate()
                    if self._is_toc_existing:
                        break

        self._debug_lt("-" * 80)
        self._debug_lt(f"End   page (table)                   ={self._page_no}")

    # ------------------------------------------------------------------
    # Add a TOC line candidate element.
    # ------------------------------------------------------------------
    def _process_toc_candidate_line_line(self, line_json: nlp_core.NLPCore.LineJSON, page_no_toc: int) -> None:
        """Add a TOC line candidate element.

        Args:
            line_json (nlp_core.NLPCore.LineLine): Document line.
            page_no_toc (int): Page number in the table of contents.
        """
        line_no_page = line_json[nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE]

        para_no_page = line_json[nlp_core.NLPCore.JSON_NAME_PARA_NO_PAGE]

        self._toc_candidates.append([page_no_toc, self._page_no, para_no_page, line_no_page])

    # ------------------------------------------------------------------
    # Add a TOC table candidate element.
    # ------------------------------------------------------------------
    def _process_toc_candidate_table_line(self, line_json: nlp_core.NLPCore.LineJSON) -> None:
        """Add a TOC table candidate element.

        Args:
            line_json (nlp_core.NLPCore.LineJSON): Document line.
        """
        row_no = line_json[nlp_core.NLPCore.JSON_NAME_TABLE_ROW_NO]

        para_no_page = line_json[nlp_core.NLPCore.JSON_NAME_PARA_NO_PAGE]

        if not self._toc_candidates or self._page_no != self._toc_candidates[-1][1] or row_no != self._toc_candidates[-1][3]:
            self._toc_candidates.append([-1, self._page_no, para_no_page, row_no])

        try:
            self._toc_candidates[-1][0] = int(line_json[nlp_core.NLPCore.JSON_NAME_TEXT])
            self._toc_candidates[-1][2] = para_no_page
        except ValueError:
            self._toc_candidates[-1][0] = -2

    # ------------------------------------------------------------------
    # Store the found TOC entries in parser result - strategy lines.
    # ------------------------------------------------------------------
    def _store_results_lines(self) -> None:  # noqa: C901
        """Store the found TOC entries in parser result."""
        self.no_lines_toc = len(self._toc_candidates)

        self._debug_lt("=" * 80)
        self._debug_lt(f"Start store result - strategy lines  ={self.no_lines_toc}")
        self._debug_lt("-" * 80)

        for [_, page_no, para_no_page, line_no_page] in self._toc_candidates:
            self._debug_lt(
                f"Line                                 ={core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES][page_no - 1][nlp_core.NLPCore.JSON_NAME_CONTAINER_LINES][line_no_page - 1][nlp_core.NLPCore.JSON_NAME_TEXT]}"  # noqa: E501 W505
            )
            core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES][page_no - 1][
                nlp_core.NLPCore.JSON_NAME_CONTAINER_LINES
            ][line_no_page - 1][nlp_core.NLPCore.JSON_NAME_TYPE] = nlp_core.NLPCore.LINE_TYPE_TOC
            for word in core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES][page_no - 1][
                nlp_core.NLPCore.JSON_NAME_CONTAINER_PARAS
            ][para_no_page - 1][nlp_core.NLPCore.JSON_NAME_CONTAINER_WORDS]:
                word_line_no_page = word[nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE]
                if word_line_no_page > line_no_page:
                    break
                if word_line_no_page < line_no_page:
                    continue
                self._debug_lt(f".... Word                            ={word[nlp_core.NLPCore.JSON_NAME_TEXT]}")
                word[nlp_core.NLPCore.JSON_NAME_TYPE] = nlp_core.NLPCore.LINE_TYPE_TOC

        self._debug_lt("-" * 80)
        self._debug_lt(f"End   store result - strategy lines  ={self.no_lines_toc}")

    # ------------------------------------------------------------------
    # Store the found TOC entries in parser result - strategy table.
    # ------------------------------------------------------------------
    def _store_results_table(self) -> None:  # noqa: C901
        """Store the found TOC entries in parser result."""
        self.no_lines_toc = len(self._toc_candidates)

        self._debug_lt("=" * 80)
        self._debug_lt(f"Start store result - strategy table  ={self.no_lines_toc}")
        self._debug_lt("-" * 80)

        if len(self._toc_candidates) < core_glob.inst_setup.lt_toc_min_entries:
            self._debug_lt("-" * 80)
            self._debug_lt(f"End   store result (min. entries)    ={self.no_lines_toc}")
            self.no_lines_toc = 0
            core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_LINES_TOC] = self.no_lines_toc
            return

        core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_LINES_TOC] = self.no_lines_toc

        page_no_from = self._toc_candidates[0][1]
        page_no_till = self._toc_candidates[-1][1]
        para_no_page_from = self._toc_candidates[0][2]
        para_no_page_till = self._toc_candidates[-1][2]

        for page_idx, page_json in enumerate(core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES]):
            page_no = page_json[nlp_core.NLPCore.JSON_NAME_PAGE_NO]

            if page_no < page_no_from:
                continue
            if page_no > page_no_till:
                break

            for line_json in page_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_LINES]:
                para_no_page = line_json[nlp_core.NLPCore.JSON_NAME_PARA_NO_PAGE]

                if page_no == page_no_from and para_no_page < para_no_page_from:
                    continue
                if page_no == page_no_till and para_no_page > para_no_page_till:
                    break

                if self._strategy == nlp_core.NLPCore.SEARCH_STRATEGY_LINES:
                    for [_, cand_page_no, cand_para_no_page, cand_line_no_page] in self._toc_candidates:
                        if (
                            page_no == cand_page_no
                            and para_no_page == cand_para_no_page
                            and line_json[nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE] == cand_line_no_page
                        ):
                            line_json[nlp_core.NLPCore.JSON_NAME_TYPE] = nlp_core.NLPCore.LINE_TYPE_TOC
                elif self._strategy == nlp_core.NLPCore.SEARCH_STRATEGY_TABLE:
                    if nlp_core.NLPCore.JSON_NAME_TABLE_ROW_NO in line_json:
                        if (
                            line_json[nlp_core.NLPCore.JSON_NAME_TYPE] == nlp_core.NLPCore.LINE_TYPE_BODY
                            or line_json[nlp_core.NLPCore.JSON_NAME_TYPE] == nlp_core.NLPCore.LINE_TYPE_TABLE
                        ):
                            line_json[nlp_core.NLPCore.JSON_NAME_TYPE] = nlp_core.NLPCore.LINE_TYPE_TOC

                core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES][page_idx][
                    nlp_core.NLPCore.JSON_NAME_CONTAINER_LINES
                ] = self._lines_json

        self._debug_lt("-" * 80)
        self._debug_lt(f"End   store result - strategy table  ={self.no_lines_toc}")

    # ------------------------------------------------------------------
    # Check the object existence.
    # ------------------------------------------------------------------
    def exists(self) -> bool:
        """Check the object existence.

        Returns: bool: Always true.
        """
        return self._exist

    # ------------------------------------------------------------------
    # Process the document related data.
    # ------------------------------------------------------------------
    def process_document(  # noqa: C)01
        self,
        file_name_curr: str,
    ) -> None:
        """Process the document related data.

        Args:
            file_name_curr (str, optional): File name of the file to be processed.
        """
        core_glob.logger.debug(core_glob.LOGGER_START)
        core_glob.logger.debug("param file_name_curr =%s", file_name_curr)

        core_utils.check_exists_object(
            is_nlp_core=True,
            is_setup=True,
            is_text_parser=True,
        )

        self._debug_lt("=" * 80)
        self._debug_lt(f"Start document                       ={self._file_name_curr}")
        self._debug_lt("-" * 37)
        self._debug_lt(f"lt_toc_last_page  ={core_glob.inst_setup.lt_toc_last_page}")
        self._debug_lt(f"lt_toc_min_entries={core_glob.inst_setup.lt_toc_min_entries}")

        # Neither the identification of headers nor footers is desired.
        if core_glob.inst_setup.lt_toc_last_page == 0:
            self._debug_lt("End (not required)")
            self._debug_lt("=" * 80)
            return

        self._file_name_curr = file_name_curr

        # -------------------------------------------------------------------------
        # Examine the table version.
        # -------------------------------------------------------------------------
        self._strategy = nlp_core.NLPCore.SEARCH_STRATEGY_TABLE

        for page_json in core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES]:
            self._lines_json = page_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_LINES]
            self._process_page_table()
            if self._is_toc_existing:
                break

        if not self._is_toc_existing:
            self._check_toc_candidate()

        # -------------------------------------------------------------------------
        # Examine the lines version.
        # -------------------------------------------------------------------------
        if not self._is_toc_existing:
            self._strategy = nlp_core.NLPCore.SEARCH_STRATEGY_LINES
            self._page_no = 0
            self._init_toc_candidate()
            for page_json in core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES]:
                self._lines_json = page_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_LINES]
                self._process_page_lines()
                if self._is_toc_existing:
                    break

            if not self._is_toc_existing:
                self._check_toc_candidate()

        # -------------------------------------------------------------------------
        # Store the results.
        # -------------------------------------------------------------------------
        if self._is_toc_existing:
            if self._strategy == nlp_core.NLPCore.SEARCH_STRATEGY_LINES:
                self._store_results_lines()
            elif self._strategy == nlp_core.NLPCore.SEARCH_STRATEGY_TABLE:
                self._store_results_table()

        self._debug_lt("-" * 80)
        self._debug_lt(f"End   document                       ={self._file_name_curr}")
        self._debug_lt("=" * 80)

        core_glob.logger.debug(core_glob.LOGGER_END)
