# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Determines the headers and footers of a parsed PDF document.

Typical usage example:

    my_instance = LineTypeHeaderFooters()

    if my_instance.exists():

    my_instance.process_document(parse_line_pages_json = my_pages)
"""
import jellyfish

import dcr_core.cls_nlp_core


# pylint: disable=too-many-instance-attributes
class LineTypeHeaderFooters:
    """Determines the headers and footers of a parsed PDF document.

    Attributes:
        line_pages_json (dcr_core.cls_nlp_core.NLPCore.ParserLinePages):
            A list of the lines provided with line types per page.
        no_lines_footer (int):
            The number of footers found.
        no_lines_header (int):
            The number of headers found.
    """

    Candidate = tuple[int, int]
    Candidates = list[Candidate]

    # line index, line text
    LineDataCell = tuple[int, str]
    LineDataRow = tuple[LineDataCell, LineDataCell]
    LineData = list[LineDataRow]

    # line index current page, line index previous page, Levenshtein distance
    LSDDataCell = tuple[int, int, int]
    LSDDataRow = list[LSDDataCell]
    LSDData = list[LSDDataRow]

    # page_index, line index
    ResultKey = tuple[int, int]
    ResultData = dict[ResultKey, str]

    # ------------------------------------------------------------------
    # Initialise the instance.
    # ------------------------------------------------------------------
    def __init__(
        self,
        file_name_curr: str = "",
    ) -> None:
        """Initialise an instance.

        Args:
            file_name_curr (str, optional):
                    File name of the PDF document to be processed - only
                    For documentation purposes. Defaults to "".
        """
        dcr_core.core_utils.check_exists_object(
            is_setup=True,
            is_text_parser=True,
        )

        self._file_name_curr = file_name_curr

        dcr_core.core_utils.progress_msg(dcr_core.core_glob.setup.is_verbose_lt_headers_footers, "LineTypeHeaderFooters")
        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers,
            f"LineTypeHeaderFooters: Start create instance                ={self._file_name_curr}",
        )

        self._irregular_footer_cand: LineTypeHeaderFooters.Candidate
        self._irregular_footer_cand_fp: LineTypeHeaderFooters.Candidates = []
        self._irregular_footer_cands: LineTypeHeaderFooters.Candidates = []

        self._irregular_header_cand: LineTypeHeaderFooters.Candidate
        self._irregular_header_cand_fp: LineTypeHeaderFooters.Candidates = []
        self._irregular_header_cands: LineTypeHeaderFooters.Candidates = []

        self._is_irregular_footer = True
        self._is_irregular_header = True

        self._line_data: LineTypeHeaderFooters.LineData = []
        self._line_data_max = 0

        self._lsd_data: LineTypeHeaderFooters.LSDData = []

        self._no_irregular_footer = 0
        self._no_irregular_header = 0

        self._page_ind = -1
        self._page_max = 0

        self._parser_line_lines_json: dcr_core.cls_nlp_core.NLPCore.ParserLineLines = []

        self._result_data: LineTypeHeaderFooters.ResultData = {}

        self.line_pages_json: dcr_core.cls_nlp_core.NLPCore.ParserLinePages = []

        self.no_lines_footer = 0
        self.no_lines_header = 0

        self._exist = True

        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers,
            f"LineTypeHeaderFooters: End   create instance                ={self._file_name_curr}",
        )

    # ------------------------------------------------------------------
    # Calculate the Levenshtein distances.
    # ------------------------------------------------------------------
    def _calc_levenshtein(self) -> None:
        dcr_core.core_utils.progress_msg(dcr_core.core_glob.setup.is_verbose_lt_headers_footers, "LineTypeHeaderFooters")
        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers, "LineTypeHeaderFooters: Start Levenshtein distance"
        )
        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers,
            f"LineTypeHeaderFooters: Value of line_data                   ={self._line_data}",
        )

        for ind in range(self._line_data_max):
            ((curr_line_ind, curr_line), (prev_line_ind, prev_line)) = self._line_data[ind]
            if curr_line_ind != -1:
                if prev_line_ind != -1:
                    distance = jellyfish.levenshtein_distance(
                        prev_line,
                        curr_line,
                    )

                    lsd_row = self._lsd_data[ind]
                    lsd_row[self._page_ind] = (curr_line_ind, prev_line_ind, distance)
                    self._lsd_data[ind] = lsd_row

        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers,
            f"LineTypeHeaderFooters: Value of lsd_data                    ={self._lsd_data}",
        )
        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers, "LineTypeHeaderFooters: End   Levenshtein distance"
        )

    # ------------------------------------------------------------------
    # Try to determine an ascending page number in the footers.
    # ------------------------------------------------------------------
    def _check_irregular_footer(self, line_ind: int, text: str) -> None:
        try:
            if text.strip() == "":
                return

            page_no_cand = int(text.split()[-1])

            if self._page_ind == 0:
                self._irregular_footer_cand_fp.append((line_ind, page_no_cand))
                return

            if self._page_ind == 1:
                for line, page_no_prev in self._irregular_footer_cand_fp:
                    if page_no_cand == int(page_no_prev) + 1:
                        self._irregular_footer_cands.append((line, page_no_prev))
                        self._irregular_footer_cand = (line_ind, page_no_cand)
                        return
                return

            if page_no_cand == self._irregular_footer_cands[-1][1] + 1:
                self._irregular_footer_cand = (line_ind, page_no_cand)
        except ValueError:
            return

    # ------------------------------------------------------------------
    # Try to determine an ascending page number in the headers.
    # ------------------------------------------------------------------
    def _check_irregular_header(self, line_ind: int, text: str) -> None:
        try:
            if text.strip() == "":
                return

            page_no_cand = int(text.split()[-1])

            if self._page_ind == 0:
                self._irregular_header_cand_fp.append((line_ind, page_no_cand))
                return

            if self._page_ind == 1:
                for line, page_no_prev in self._irregular_header_cand_fp:
                    if page_no_cand == int(page_no_prev) + 1:
                        self._irregular_header_cands.append((line, page_no_prev))
                        self._irregular_header_cand = (line_ind, page_no_cand)
                        return
                return

            if page_no_cand == self._irregular_header_cands[-1][1] + 1:
                # not testable
                self._irregular_header_cand = (line_ind, page_no_cand)
        except ValueError:
            return

    # ------------------------------------------------------------------
    # Determine the candidates.
    # ------------------------------------------------------------------
    def _determine_candidate(self, distance_max: int, line_ind: int) -> bool:
        is_empty_line = True
        is_special_line = True

        for page_ind in range(self._page_max):
            (_, _, distance) = self._lsd_data[line_ind][page_ind]

            # no line existing
            if distance == -1:
                if page_ind <= 1 or page_ind == self._page_max - 1:
                    continue

                is_special_line = False
                break

            is_empty_line = False

            # processing a header line
            if distance <= distance_max:
                continue

            if page_ind == 1 or page_ind >= self._page_max - 1:
                if self._page_max > 2:
                    continue

            is_special_line = False
            break

        if is_empty_line:
            return False

        return is_special_line

    # ------------------------------------------------------------------
    # Process the page-related data.
    # ------------------------------------------------------------------
    def _process_page(self) -> None:  # noqa: C901
        self._page_ind += 1

        dcr_core.core_utils.progress_msg(dcr_core.core_glob.setup.is_verbose_lt_headers_footers, "LineTypeHeaderFooters")
        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers,
            f"LineTypeHeaderFooters: Start page                           ={self._page_ind + 1}",
        )

        if self._is_irregular_footer:
            self._irregular_footer_cand = LineTypeHeaderFooters.Candidate()

        if self._is_irregular_header:
            self._irregular_header_cand = LineTypeHeaderFooters.Candidate()

        if dcr_core.core_glob.setup.lt_header_max_lines > 0:
            self._store_line_data_header()

        if dcr_core.core_glob.setup.lt_footer_max_lines > 0:
            self._store_line_data_footer()

        if self._is_irregular_footer:
            if self._page_ind == 0:
                if not self._irregular_footer_cand_fp:
                    self._is_irregular_footer = False
            elif self._irregular_footer_cand:
                self._irregular_footer_cands.append(self._irregular_footer_cand)
            else:
                self._is_irregular_footer = False

        if self._is_irregular_header:
            if self._page_ind == 0:
                if not self._irregular_header_cand_fp:
                    self._is_irregular_header = False
            elif self._irregular_header_cand:
                self._irregular_header_cands.append(self._irregular_header_cand)
            else:
                self._is_irregular_header = False

        if self._page_ind > 0:
            self._calc_levenshtein()

        self._swap_current_previous()

        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers,
            f"LineTypeHeaderFooters: End   page                           ={self._page_ind + 1}",
        )

    # ------------------------------------------------------------------
    # Store the irregular footers and headers.
    # ------------------------------------------------------------------
    def _store_irregulars(self) -> None:
        if self._is_irregular_footer:
            self._no_irregular_footer = 1
            dcr_core.core_utils.progress_msg(
                dcr_core.core_glob.setup.is_verbose_lt_headers_footers,
                f"LineTypeHeaderFooters: Value of irregular footers           ={self._irregular_footer_cands}",
            )

        if self._is_irregular_header:
            self._no_irregular_header = 1
            dcr_core.core_utils.progress_msg(
                dcr_core.core_glob.setup.is_verbose_lt_headers_footers,
                f"LineTypeHeaderFooters: Value of irregular headers           ={self._irregular_header_cands}",
            )

        for page_ind, page in enumerate(self.line_pages_json):
            lines = page[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINES]

            is_changed = False

            if self._is_irregular_footer and self._irregular_footer_cands:
                if (
                    lines[self._irregular_footer_cands[page_ind][0]][dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE]
                    == dcr_core.cls_nlp_core.NLPCore.LINE_TYPE_BODY
                ):
                    lines[self._irregular_footer_cands[page_ind][0]][
                        dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE
                    ] = dcr_core.cls_nlp_core.NLPCore.LINE_TYPE_FOOTER
                    is_changed = True
                else:
                    self._no_irregular_footer = 0

            if self._is_irregular_header and self._irregular_header_cands:
                if (
                    lines[self._irregular_header_cands[page_ind][0]][dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE]
                    == dcr_core.cls_nlp_core.NLPCore.LINE_TYPE_BODY
                ):
                    lines[self._irregular_header_cands[page_ind][0]][
                        dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE
                    ] = dcr_core.cls_nlp_core.NLPCore.LINE_TYPE_HEADER
                    is_changed = True
                else:
                    self._no_irregular_header = 0

            if is_changed:
                self.line_pages_json[page_ind] = page

    # ------------------------------------------------------------------
    # Store the footers of the current page.
    # ------------------------------------------------------------------
    def _store_line_data_footer(self) -> None:
        dcr_core.core_utils.progress_msg(dcr_core.core_glob.setup.is_verbose_lt_headers_footers, "LineTypeHeaderFooters")
        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers, "LineTypeHeaderFooters: Start store footers"
        )
        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers,
            f"LineTypeHeaderFooters: Value of line_data                   ={self._line_data}",
        )

        if len(self._parser_line_lines_json) == 0:
            return

        line_lines_ind = len(self._parser_line_lines_json) - 1

        for ind in range(self._line_data_max - 1, dcr_core.core_glob.setup.lt_header_max_lines - 1, -1):
            (_, prev) = self._line_data[ind]

            page_line: dict[str, int | str] = self._parser_line_lines_json[line_lines_ind]

            text = str(page_line[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_TEXT])

            if self._is_irregular_footer:
                self._check_irregular_footer(line_lines_ind, text)

            self._line_data[ind] = (
                (
                    int(page_line[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE]) - 1,
                    text,
                ),
                prev,
            )

            if line_lines_ind == 0:
                break

            line_lines_ind -= 1

        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers,
            f"LineTypeHeaderFooters: Value of line_data                   ={self._line_data}",
        )
        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers, "LineTypeHeaderFooters: End   store footers"
        )

    # ------------------------------------------------------------------
    # Store the headers of the current page.
    # ------------------------------------------------------------------
    def _store_line_data_header(self) -> None:
        dcr_core.core_utils.progress_msg(dcr_core.core_glob.setup.is_verbose_lt_headers_footers, "LineTypeHeaderFooters")
        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers, "LineTypeHeaderFooters: Start store headers"
        )
        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers,
            f"LineTypeHeaderFooters: Value of line_data                   ={self._line_data}",
        )

        if (line_lines_max := len(self._parser_line_lines_json)) == 0:
            return

        for ind in range(dcr_core.core_glob.setup.lt_header_max_lines):
            if ind >= line_lines_max:
                break

            (_, prev) = self._line_data[ind]

            page_line: dict[str, int | str] = self._parser_line_lines_json[ind]

            text = str(page_line[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_TEXT])

            if self._is_irregular_header:
                self._check_irregular_header(ind, text)

            self._line_data[ind] = (
                (
                    int(page_line[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE]) - 1,
                    text,
                ),
                prev,
            )

        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers,
            f"LineTypeHeaderFooters: Value of line_data                   ={self._line_data}",
        )
        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers, "LineTypeHeaderFooters: End   store headers"
        )

    # ------------------------------------------------------------------
    # Store the found line types in parser result.
    # ------------------------------------------------------------------
    def _store_results(self) -> None:
        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers, "LineTypeHeaderFooters: Start store result"
        )

        self.no_lines_footer = 0
        self.no_lines_header = 0

        for page in self.line_pages_json:
            page_no = page[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO]

            for line_line in page[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINES]:
                line_index_page = int(line_line[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE]) - 1
                if (page_no, line_index_page) in self._result_data:
                    line_line[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] = self._result_data[(page_no, line_index_page)]
                    if page_no == 2:
                        if self._result_data[(page_no, line_index_page)] == dcr_core.cls_nlp_core.NLPCore.LINE_TYPE_FOOTER:
                            self.no_lines_footer += 1
                        elif self._result_data[(page_no, line_index_page)] == dcr_core.cls_nlp_core.NLPCore.LINE_TYPE_HEADER:
                            self.no_lines_header += 1

        if self.no_lines_header > 0:
            dcr_core.core_utils.progress_msg(
                dcr_core.core_glob.setup.is_verbose_lt_headers_footers,
                f"LineTypeHeaderFooters: End   store result             header={self.no_lines_header}",
            )
        if self.no_lines_footer > 0:
            dcr_core.core_utils.progress_msg(
                dcr_core.core_glob.setup.is_verbose_lt_headers_footers,
                f"LineTypeHeaderFooters: End   store result             footer={self.no_lines_footer}",
            )
        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers, "LineTypeHeaderFooters: End   store result"
        )

    # ------------------------------------------------------------------
    # Swap the current and previous data.
    # ------------------------------------------------------------------
    def _swap_current_previous(self) -> None:
        dcr_core.core_utils.progress_msg(dcr_core.core_glob.setup.is_verbose_lt_headers_footers, "LineTypeHeaderFooters")
        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers,
            "LineTypeHeaderFooters: Start swap current & previous",
        )
        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers,
            f"LineTypeHeaderFooters: Value of line_data                   ={self._line_data}",
        )

        for ind in range(self._line_data_max):
            (curr, _) = self._line_data[ind]
            self._line_data[ind] = ((-1, ""), curr)

        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers,
            f"LineTypeHeaderFooters: Value of line_data                   ={self._line_data}",
        )
        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers,
            "LineTypeHeaderFooters: End   swap current & previous",
        )

    # ------------------------------------------------------------------
    # Check the object existence.
    # ------------------------------------------------------------------
    def exists(self) -> bool:
        """Check the existence of the instance.

        Returns:
            bool:   Always true
        """
        return self._exist

    # ------------------------------------------------------------------
    # Process the document related data.
    # ------------------------------------------------------------------
    def process_document(
        self,
        line_pages_json: dcr_core.cls_nlp_core.NLPCore.ParserLinePages,
        file_name_curr: str = "",
    ) -> None:
        """Process the document related data.

        Args:
            line_pages_json
                (dcr_core.cls_nlp_core.NLPCore.ParserLinePages):
                The document pages formatted in the parser.
            file_name_curr (str, optional):
                File name of the PDF document to be processed - only
                For documentation purposes. Defaults to "".
        """
        dcr_core.core_utils.check_exists_object(
            is_setup=True,
            is_text_parser=True,
        )

        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers,
            f"LineTypeHeaderFooters: lt_header_max_lines={dcr_core.core_glob.setup.lt_header_max_lines} "
            + f"- lt_footer_max_lines={dcr_core.core_glob.setup.lt_footer_max_lines}",
        )

        # Neither the identification of headers nor footers is desired.
        if dcr_core.core_glob.setup.lt_footer_max_lines == 0 and dcr_core.core_glob.setup.lt_header_max_lines == 0:
            return

        self._file_name_curr = file_name_curr
        self.line_pages_json = line_pages_json
        self._page_max = len(self.line_pages_json)

        dcr_core.core_utils.progress_msg(dcr_core.core_glob.setup.is_verbose_lt_headers_footers, "LineTypeHeaderFooters")
        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers,
            f"LineTypeHeaderFooters: Start document                       ={self._file_name_curr}",
        )
        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers,
            f"LineTypeHeaderFooters: Value of lsd_data                    ={self._lsd_data}",
        )

        self._line_data_max = dcr_core.core_glob.setup.lt_header_max_lines + dcr_core.core_glob.setup.lt_footer_max_lines

        self._line_data = [((-1, ""), (-1, "")) for _ in range(self._line_data_max)]
        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers,
            f"LineTypeHeaderFooters: Value of line_data                   ={self._line_data}",
        )

        self._lsd_data = [[(-1, -1, -1) for _ in range(self._page_max)] for _ in range(self._line_data_max)]
        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers,
            f"LineTypeHeaderFooters: Value of lsd_data                    ={self._lsd_data}",
        )

        for page_json in self.line_pages_json:
            self._parser_line_lines_json = page_json[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINES]
            self._process_page()

        for line_ind in range(self._line_data_max):
            if line_ind < dcr_core.core_glob.setup.lt_header_max_lines:
                distance_max = dcr_core.core_glob.setup.lt_header_max_distance
                line_type = dcr_core.cls_nlp_core.NLPCore.LINE_TYPE_HEADER
            else:
                distance_max = dcr_core.core_glob.setup.lt_footer_max_distance
                line_type = dcr_core.cls_nlp_core.NLPCore.LINE_TYPE_FOOTER

            if self._determine_candidate(distance_max, line_ind):
                for page_ind in range(self._page_max):
                    (line_no_curr, line_no_prev, distance) = self._lsd_data[line_ind][page_ind]
                    if 0 <= distance <= distance_max:
                        self._result_data[(page_ind, line_no_prev)] = line_type
                        self._result_data[(page_ind + 1, line_no_curr)] = line_type

        if len(self._result_data) > 0:
            dcr_core.core_utils.progress_msg(
                dcr_core.core_glob.setup.is_verbose_lt_headers_footers,
                f"LineTypeHeaderFooters: Value of result_data                 ={self._result_data}",
            )
            self._store_results()

        if (
            dcr_core.core_glob.setup.lt_footer_max_distance > 0
            and self._is_irregular_footer
            or dcr_core.core_glob.setup.lt_header_max_distance > 0
            and self._is_irregular_header
        ):
            self._store_irregulars()
            self.no_lines_footer += self._no_irregular_footer
            self.no_lines_header += self._no_irregular_header

        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_headers_footers,
            f"LineTypeHeaderFooters: End document                         ={self._file_name_curr}",
        )
