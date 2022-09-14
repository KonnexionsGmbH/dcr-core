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
            is_line_type_header_footer=True,
            is_nlp_core=True,
            is_setup=True,
            is_text_parser=True,
        )

        self._file_name_curr = file_name_curr

        core_utils.progress_msg(core_glob.setup.is_verbose_lt_toc, "LineTypeToc")
        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_toc,
            f"LineTypeToc: Start create instance                ={self._file_name_curr}",
        )

        self._is_toc_existing = False

        self._lines_json: list[nlp_core.LineJSON] = []

        self._page_no = 0

        self._strategy = ""

        # page_no_toc, page_no, paragraph_no, row_no
        self._toc_candidates: list[list[int]] = []

        self.no_lines_toc = 0

        self._exist = True

        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_toc,
            f"LineTypeToc: End   create instance                ={self._file_name_curr}",
        )

        core_glob.logger.debug(core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Check a TOC candidate.
    # ------------------------------------------------------------------
    def _check_toc_candidate(self) -> None:
        if not self._toc_candidates:
            return

        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_toc,
            f"LineTypeToc: Start check TOC candidate            ={len(self._toc_candidates)}",
        )

        row_no = 0
        page_no_max = core_glob.nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_PAGES]
        page_no_toc_last = -1

        for [page_no_toc, _, _, _] in self._toc_candidates:
            row_no += 1

            if page_no_toc == -1:
                if row_no != 1:
                    self._init_toc_candidate()
                    core_utils.progress_msg(
                        core_glob.setup.is_verbose_lt_toc,
                        "LineTypeToc: End   check TOC candidate (!=)       " + f"={self._is_toc_existing}: {page_no_toc}",
                    )
                    return

                continue

            if page_no_toc < page_no_toc_last or page_no_toc > page_no_max:
                self._init_toc_candidate()
                core_utils.progress_msg(
                    core_glob.setup.is_verbose_lt_toc,
                    "LineTypeToc: End   check TOC candidate (<>)       " + f"={self._is_toc_existing}: {page_no_toc}",
                )
                return

            page_no_toc_last = page_no_toc

        self._is_toc_existing = True

        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_toc,
            "LineTypeToc: End   check TOC candidate            " + f"={self._is_toc_existing}",
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
        if self._is_toc_existing or self._page_no >= core_glob.setup.lt_toc_last_page:
            return

        self._page_no += 1

        core_utils.progress_msg(core_glob.setup.is_verbose_lt_toc, "LineTypeToc")
        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_toc,
            f"LineTypeToc: Start page (lines)                   ={self._page_no}",
        )

        for line_json in self._lines_json:
            if line_json[nlp_core.NLPCore.JSON_NAME_LINE_TYPE] == nlp_core.NLPCore.LINE_TYPE_BODY:
                if (text := line_json[nlp_core.NLPCore.JSON_NAME_TEXT]) != "":
                    line_tokens = text.split()
                    try:
                        self._process_toc_candidate_line_line(line_json, int(line_tokens[-1]))
                    except ValueError:
                        self._check_toc_candidate()
                        if self._is_toc_existing:
                            break

        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_toc,
            f"LineTypeToc: End   page (lines)                   ={self._page_no}",
        )

    # ------------------------------------------------------------------
    # Process the page-related data - table version.
    # ------------------------------------------------------------------
    def _process_page_table(self) -> None:
        """Process the page-related data - table version."""
        if self._is_toc_existing or self._page_no >= core_glob.setup.lt_toc_last_page:
            return

        self._page_no += 1

        core_utils.progress_msg(core_glob.setup.is_verbose_lt_toc, "LineTypeToc")
        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_toc,
            f"LineTypeToc: Start page (table)                   ={self._page_no}",
        )

        for line_json in self._lines_json:
            if line_json[nlp_core.NLPCore.JSON_NAME_LINE_TYPE] == nlp_core.NLPCore.LINE_TYPE_BODY:
                if nlp_core.NLPCore.JSON_NAME_ROW_NO in line_json:
                    self._process_toc_candidate_table_line(line_json)
                else:
                    self._check_toc_candidate()
                    if self._is_toc_existing:
                        break

        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_toc,
            f"LineTypeToc: End   page (table)                   ={self._page_no}",
        )

    # ------------------------------------------------------------------
    # Add a TOC line candidate element.
    # ------------------------------------------------------------------
    def _process_toc_candidate_line_line(self, line_json: nlp_core.LineJSON, page_no_toc: int) -> None:
        """Add a TOC line candidate element.

        Args:
            line_json (nlp_core.NLPCore.LineLine): Document line.
            page_no_toc (int): Page number in the table of contents.
        """
        line_no = line_json[nlp_core.NLPCore.JSON_NAME_LINE_NO]

        para_no = line_json[nlp_core.NLPCore.JSON_NAME_PARA_NO]

        self._toc_candidates.append([page_no_toc, self._page_no, para_no, line_no])

    # ------------------------------------------------------------------
    # Add a TOC table candidate element.
    # ------------------------------------------------------------------
    def _process_toc_candidate_table_line(self, line_json: nlp_core.LineJSON) -> None:
        """Add a TOC table candidate element.

        Args:
            line_json (nlp_core.LineJSON): Document line.
        """
        row_no = line_json[nlp_core.NLPCore.JSON_NAME_ROW_NO]

        para_no = line_json[nlp_core.NLPCore.JSON_NAME_PARA_NO]

        if not self._toc_candidates or self._page_no != self._toc_candidates[-1][1] or row_no != self._toc_candidates[-1][3]:
            self._toc_candidates.append([-1, self._page_no, para_no, row_no])

        try:
            self._toc_candidates[-1][0] = int(line_json[nlp_core.NLPCore.JSON_NAME_TEXT])
            self._toc_candidates[-1][2] = para_no
        except ValueError:
            self._toc_candidates[-1][0] = -1

    # ------------------------------------------------------------------
    # Store the found TOC entries in parser result.
    # ------------------------------------------------------------------
    def _store_results(self) -> None:  # noqa: C901
        """Store the found TOC entries in parser result."""
        self.no_lines_toc = len(self._toc_candidates)

        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_toc,
            f"LineTypeToc: Start store result                   ={self.no_lines_toc}",
        )

        if len(self._toc_candidates) < core_glob.setup.lt_toc_min_entries:
            core_utils.progress_msg(
                core_glob.setup.is_verbose_lt_toc,
                f"LineTypeToc: End   store result (min. entries)    ={self.no_lines_toc}",
            )
            self.no_lines_toc = 0
            return

        page_no_from = self._toc_candidates[0][1]
        page_no_till = self._toc_candidates[-1][1]
        para_no_from = self._toc_candidates[0][2]
        para_no_till = self._toc_candidates[-1][2]

        for page in core_glob.nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_PAGES]:
            page_no = page[nlp_core.NLPCore.JSON_NAME_PAGE_NO]

            if page_no < page_no_from:
                continue
            if page_no > page_no_till:
                break

            for line_json in page[nlp_core.NLPCore.JSON_NAME_LINES]:
                para_no = line_json[nlp_core.NLPCore.JSON_NAME_PARA_NO]

                if page_no == page_no_from and para_no < para_no_from:
                    continue
                if page_no == page_no_till and para_no > para_no_till:
                    break

                if self._strategy == nlp_core.NLPCore.SEARCH_STRATEGY_LINES:
                    for [_, cand_page_no, cand_para_no, cand_line_no] in self._toc_candidates:
                        if (
                            page_no == cand_page_no
                            and para_no == cand_para_no
                            and line_json[nlp_core.NLPCore.JSON_NAME_LINE_NO] == cand_line_no
                        ):
                            line_json[nlp_core.NLPCore.JSON_NAME_LINE_TYPE] = nlp_core.NLPCore.LINE_TYPE_TOC
                elif self._strategy == nlp_core.NLPCore.SEARCH_STRATEGY_TABLE:
                    if nlp_core.NLPCore.JSON_NAME_ROW_NO in line_json:
                        if line_json[nlp_core.NLPCore.JSON_NAME_LINE_TYPE] == nlp_core.NLPCore.LINE_TYPE_BODY:
                            line_json[nlp_core.NLPCore.JSON_NAME_LINE_TYPE] = nlp_core.NLPCore.LINE_TYPE_TOC

        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_toc,
            f"LineTypeToc: End   store result                   ={self.no_lines_toc}",
        )

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
    def process_document(
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
            is_line_type_header_footer=True,
            is_nlp_core=True,
            is_setup=True,
            is_text_parser=True,
        )

        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_toc,
            f"LineTypeToc: lt_toc_last_page={core_glob.setup.lt_toc_last_page}",
        )

        if core_glob.setup.lt_toc_last_page == 0:
            return

        self._file_name_curr = file_name_curr

        core_utils.progress_msg(core_glob.setup.is_verbose_lt_toc, "LineTypeToc")
        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_toc,
            f"LineTypeToc: Start document                       ={self._file_name_curr}",
        )

        # -------------------------------------------------------------------------
        # Examine the table version.
        # -------------------------------------------------------------------------
        self._strategy = nlp_core.NLPCore.SEARCH_STRATEGY_TABLE

        for page_json in core_glob.nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_PAGES]:
            self._lines_json = page_json[nlp_core.NLPCore.JSON_NAME_LINES]
            self._process_page_table()

        if not self._is_toc_existing:
            self._check_toc_candidate()

        # -------------------------------------------------------------------------
        # Examine the lines version.
        # -------------------------------------------------------------------------
        if not self._is_toc_existing:
            self._strategy = nlp_core.NLPCore.SEARCH_STRATEGY_LINES
            self._page_no = 0
            self._init_toc_candidate()
            for page_json in core_glob.nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_PAGES]:
                self._lines_json = page_json[nlp_core.NLPCore.JSON_NAME_LINES]
                self._process_page_lines()

            if not self._is_toc_existing:
                self._check_toc_candidate()

        # -------------------------------------------------------------------------
        # Store the results.
        # -------------------------------------------------------------------------
        if self._is_toc_existing:
            self._store_results()

        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_toc,
            f"LineTypeToc: End   document                       ={self._file_name_curr}",
        )

        core_glob.logger.debug(core_glob.LOGGER_END)
