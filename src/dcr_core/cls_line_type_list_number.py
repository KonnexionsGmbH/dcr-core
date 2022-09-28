# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Determine list of numbered lines.

Typical usage example:

    my_instance = LineTypeListNumber()

    if my_instance.exists():

    my_instance.process_document(directory_name = my_directory,
                                 document_id = my_document_id,
                                 environment_variant = my_environment_variant,
                                 file_name_curr = my_file_name_curr,
                                 file_name_orig = my_file_name_orig,
                                 line_pages_json = my_line_pages_json)
"""
from __future__ import annotations

import collections
import json
import os
import pathlib
import re

import dcr_core.cls_nlp_core as nlp_core
from dcr_core import core_glob
from dcr_core import core_utils


# pylint: disable=duplicate-code
# pylint: disable=too-many-instance-attributes
class LineTypeListNumber:
    """Determine list of numbered lines."""

    _Entry = dict[str, int | str]
    _Entries = list[_Entry]

    _List = dict[str, _Entries | float | int | object | str]
    _Lists = list[_List]

    _RULE_NAME_SIZE = 20

    _RuleExtern = tuple[str, str, collections.abc.Callable[[str, str], bool], list[str]]
    _RuleIntern = tuple[str, re.Pattern[str], collections.abc.Callable[[str, str], bool], list[str], str]

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

        self._file_name_curr = file_name_curr

        self._environment_variant = ""

        self._anti_patterns: list[tuple[str, re.Pattern[str]]] = self._init_anti_patterns()

        # page_idx, para_no, line_idx_first, line_idx_last, target_value
        self._entries: list[list[int | str]] = []

        self._line_idx = -1
        self._lists: list[nlp_core.NLPCore.ListJSON] = []
        self._llx_lower_limit = 0.0
        self._llx_subsequent: tuple[float, float] = (0.0, 0.0)
        self._llx_upper_limit = 0.0

        self._no_lines_line_type = 0

        self._rule: LineTypeListNumber._RuleIntern = ()  # type: ignore
        self._rules: list[LineTypeListNumber._RuleExtern] = self._init_rules()

        # ------------------------------------------------------------------
        # Number rules collection.
        # ------------------------------------------------------------------
        # 1: rule_name
        # 2: regexp_compiled:
        #           compiled regular expression
        # 3: function_is_asc:
        #           compares predecessor and successor
        # 4: start_values:
        #           list of strings
        # 5: regexp_str:
        #           regular expression
        # ------------------------------------------------------------------
        self._rules_collection: list[LineTypeListNumber._RuleIntern] = []

        for (rule_name, regexp_str, function_is_asc, start_values) in self._rules:
            self._rules_collection.append(
                (
                    rule_name.ljust(LineTypeListNumber._RULE_NAME_SIZE),
                    re.compile(regexp_str),
                    function_is_asc,
                    start_values,
                    regexp_str,
                )
            )

        self._exist = True

        core_glob.logger.debug(core_glob.LOGGER_END)

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
            core_glob.inst_setup.is_verbose_lt_list_number,
            "LineTypeListNumber: " + msg,
        )

    # ------------------------------------------------------------------
    # Finish a list.
    # ------------------------------------------------------------------
    def _finish_list(self, page_idx: int) -> None:
        """Finish a list."""
        if (no_entries := len(self._entries)) == 0:
            return

        self._debug_lt("=" * 80)
        self._debug_lt(f"Start list on page                   ={page_idx + 1} candidates={no_entries}")

        if no_entries < core_glob.inst_setup.lt_list_number_min_entries:
            self._debug_lt(
                f"Not enough list entries              ={page_idx + 1} found only={no_entries} - "
                + f"number='{self._rule[0]}' - entries={self._entries}"
            )
            self._reset_list()
            self._debug_lt(f"End   list on page                   ={page_idx + 1}")
            self._debug_lt("-" * 80)
            return

        self._debug_lt(
            f"List entries                         ={page_idx + 1} verified  ={no_entries} - "
            + f"number='{self._rule[0]}' - entries={self._entries}"
        )

        entries: LineTypeListNumber._Entries = []

        for [page_idx_list, para_no, line_idx_first, line_idx_last, _] in self._entries:
            lines_json: list[nlp_core.NLPCore.LineJSON] = core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES][
                page_idx_list
            ][nlp_core.NLPCore.JSON_NAME_CONTAINER_LINES]

            text = []

            for idx in range(line_idx_first, line_idx_last + 1):
                lines_json[idx][nlp_core.NLPCore.JSON_NAME_TYPE] = nlp_core.NLPCore.LINE_TYPE_LIST_NUMBER
                self._no_lines_line_type += 1

                para_no_page = lines_json[idx][nlp_core.NLPCore.JSON_NAME_PARA_NO_PAGE]

                for word in core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES][page_idx_list][
                    nlp_core.NLPCore.JSON_NAME_CONTAINER_PARAS
                ][para_no_page - 1][nlp_core.NLPCore.JSON_NAME_CONTAINER_WORDS]:
                    word_line_no_page = word[nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE]
                    if word_line_no_page > line_idx_last + 1:
                        break
                    if word_line_no_page < line_idx_first + 1:
                        continue
                    word[nlp_core.NLPCore.JSON_NAME_TYPE] = nlp_core.NLPCore.LINE_TYPE_LIST_NUMBER

                text.append(lines_json[idx][nlp_core.NLPCore.JSON_NAME_TEXT])

            entries.append(
                {
                    nlp_core.NLPCore.JSON_NAME_ENTRY_NO: len(entries) + 1,
                    nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE_FIRST: line_idx_first + 1,
                    nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE_LAST: line_idx_last + 1,
                    nlp_core.NLPCore.JSON_NAME_PAGE_NO: page_idx_list + 1,
                    nlp_core.NLPCore.JSON_NAME_PARA_NO: para_no,
                    nlp_core.NLPCore.JSON_NAME_TEXT: "\n".join(text),
                }
            )

            core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES][page_idx_list][
                nlp_core.NLPCore.JSON_NAME_CONTAINER_LINES
            ] = lines_json

        self._lists.append(
            {
                nlp_core.NLPCore.JSON_NAME_FORMAT: self._rule[0].rstrip(),
                nlp_core.NLPCore.JSON_NAME_LIST_NO: len(self._lists) + 1,
                nlp_core.NLPCore.JSON_NAME_NO_ENTRIES: len(entries),
                nlp_core.NLPCore.JSON_NAME_PAGE_NO_FIRST: self._entries[0][0] + 1,
                nlp_core.NLPCore.JSON_NAME_PAGE_NO_LAST: self._entries[-1][0] + 1,
                nlp_core.NLPCore.JSON_NAME_ENTRIES: entries,
            }
        )

        self._reset_list()

        self._debug_lt(f"End   list                           ={page_idx + 1}")
        self._debug_lt("-" * 80)

    # ------------------------------------------------------------------
    # Determine the lower left x-position of a possible following line
    # of the current numbered point.
    # ------------------------------------------------------------------
    def _get_llx_subsequent(self, page_idx: int, para_idx_page, line_no_page) -> tuple[float, float]:
        llx_center = 0.0

        for word in core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES][page_idx][
            nlp_core.NLPCore.JSON_NAME_CONTAINER_PARAS
        ][para_idx_page][nlp_core.NLPCore.JSON_NAME_CONTAINER_WORDS]:
            line_no_page_word = word[nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE]
            if line_no_page_word < line_no_page:
                continue

            if line_no_page_word == line_no_page:
                if word[nlp_core.NLPCore.JSON_NAME_WORD_NO_LINE] == 1:
                    continue

                llx_center = word[nlp_core.NLPCore.JSON_NAME_LLX]
                return (
                    round(llx_center * (100 - core_glob.inst_setup.lt_list_number_tolerance_llx) / 100, 2),
                    round(llx_center * (100 + core_glob.inst_setup.lt_list_number_tolerance_llx) / 100, 2),
                )

            break

        return (0.0, 0.0)

    # ------------------------------------------------------------------
    # Initialise the numbered list anti-patterns.
    # ------------------------------------------------------------------
    # 1: name:  pattern name
    # 2: regexp regular expression
    # ------------------------------------------------------------------
    def _init_anti_patterns(self) -> list[tuple[str, re.Pattern[str]]]:
        """Initialise the numbered list anti-patterns.

        Returns:
            list[tuple[str, re.Pattern[str]]]: The valid numbered list anti-patterns.
        """
        if core_glob.inst_setup.lt_list_number_rule_file and core_glob.inst_setup.lt_list_number_rule_file.lower() != "none":
            lt_list_number_rule_file_path = core_utils.get_os_independent_name(core_glob.inst_setup.lt_list_number_rule_file)
            if os.path.isfile(lt_list_number_rule_file_path):
                return self._load_anti_patterns_from_json(pathlib.Path(lt_list_number_rule_file_path))

            core_utils.terminate_fatal(
                f"File with numbered list anti-patterns is missing - " f"file name '{core_glob.inst_setup.lt_list_number_rule_file}'"
            )

        anti_patterns = []

        for name, regexp in nlp_core.NLPCore.get_lt_anti_patterns_default_list_number(environment_variant=self._environment_variant):
            anti_patterns.append((name, re.compile(regexp)))

        return anti_patterns

    # ------------------------------------------------------------------
    # Initialise the numbered list rules.
    # ------------------------------------------------------------------
    # 1: rule_name
    # 2: regexp_str:
    #           regular expression
    # 3: function_is_asc:
    #           compares predecessor and successor
    # 4: start_values:
    #           list of strings
    # ------------------------------------------------------------------
    def _init_rules(self) -> list[LineTypeListNumber._RuleExtern]:
        """Initialise the numbered list rules.

        Returns:
            list[LineTypeListNumber.RuleExtern]: The valid numbered list rules.
        """
        self._debug_lt("=" * 80)
        self._debug_lt("Start initialise rules")
        self._debug_lt("-" * 80)

        if core_glob.inst_setup.lt_list_number_rule_file and core_glob.inst_setup.lt_list_number_rule_file.lower() != "none":
            lt_list_number_rule_file_path = core_utils.get_os_independent_name(core_glob.inst_setup.lt_list_number_rule_file)
            if os.path.isfile(lt_list_number_rule_file_path):
                return self._load_rules_from_json(pathlib.Path(lt_list_number_rule_file_path))

            core_utils.terminate_fatal(
                f"File with numbered list rules is missing - " f"file name '{core_glob.inst_setup.lt_list_number_rule_file}'"
            )

        self._debug_lt("-" * 80)
        self._debug_lt("End   initialise rules")

        return nlp_core.NLPCore.get_lt_rules_default_list_number()

    # ------------------------------------------------------------------
    # Load the valid numbered list anti-patterns from a JSON file.
    # ------------------------------------------------------------------
    @staticmethod
    def _load_anti_patterns_from_json(
        lt_list_number_rule_file: pathlib.Path,
    ) -> list[tuple[str, re.Pattern[str]]]:
        """Load the valid numbered list anti-patterns from a JSON file.

        Args:
            lt_list_number_rule_file (Path): JSON file.

        Returns:
            list[tuple[str, re.Pattern[str]]]: The valid numbered list
                anti-patterns from the JSON file,
        """
        anti_patterns = []

        with open(lt_list_number_rule_file, "r", encoding=core_glob.FILE_ENCODING_DEFAULT) as file_handle:
            json_data = json.load(file_handle)

            for rule in json_data[nlp_core.NLPCore.JSON_NAME_LINE_TYPE_ANTI_PATTERNS]:
                anti_patterns.append(
                    (
                        rule[nlp_core.NLPCore.JSON_NAME_NAME],
                        re.compile(rule[nlp_core.NLPCore.JSON_NAME_REGEXP]),
                    )
                )

        core_utils.progress_msg(
            core_glob.inst_setup.is_verbose_lt_list_number,
            "The numbered list anti-patterns were successfully loaded " + f"from the file {core_glob.inst_setup.lt_list_number_rule_file}",
        )

        return anti_patterns

    # ------------------------------------------------------------------
    # Load numbered list rules from a JSON file.
    # ------------------------------------------------------------------
    @staticmethod
    def _load_rules_from_json(
        lt_list_number_rule_file: pathlib.Path,
    ) -> list[LineTypeListNumber._RuleExtern]:
        """Load numbered list rules from a JSON file.

        Args:
            lt_list_number_rule_file (Path): JSON file.

        Returns:
            list[tuple[str, str, collections.abc.Callable[[str, str], bool], list[str]]]: The valid
                numbered list rules from the JSON file,
        """
        rules: list[LineTypeListNumber._RuleExtern] = []

        with open(lt_list_number_rule_file, "r", encoding=core_glob.FILE_ENCODING_DEFAULT) as file_handle:
            json_data = json.load(file_handle)

            for rule in json_data[nlp_core.NLPCore.JSON_NAME_LINE_TYPE_RULES]:
                rules.append(
                    (
                        rule[nlp_core.NLPCore.JSON_NAME_NAME],
                        rule[nlp_core.NLPCore.JSON_NAME_REGEXP],
                        getattr(
                            nlp_core.NLPCore,
                            "is_asc_" + rule[nlp_core.NLPCore.JSON_NAME_FUNCTION_IS_ASC],
                        ),
                        rule[nlp_core.NLPCore.JSON_NAME_START_VALUES],
                    )
                )

        core_utils.progress_msg(
            core_glob.inst_setup.is_verbose_lt_list_number,
            "The list_number rules were successfully loaded from the " + f"file {core_glob.inst_setup.lt_list_number_rule_file}",
        )

        return rules

    # ------------------------------------------------------------------
    # Process the line-related data.
    # ------------------------------------------------------------------
    def _process_line(self, page_idx: int, line_idx: int, line_json: nlp_core.NLPCore.LineJSON) -> None:  # noqa: C901
        """Process the line-related data.

        Args:
            page_idx (int):
                The current page index.
            line_idx (int):
                The current line index on the page.
            line_json (nlp_core.NLPCore.LineJSON):
                The line to be processed.
        """
        text = str(line_json[nlp_core.NLPCore.JSON_NAME_TEXT])

        for (rule_name, pattern) in self._anti_patterns:
            if pattern.match(text):
                self._debug_lt(f"Anti pattern                         ={rule_name} - text={text}")
                return

        para_no = int(line_json[nlp_core.NLPCore.JSON_NAME_PARA_NO])

        target_value = text.split()[0]

        if self._rule:
            if self._rule[1].match(target_value):
                if self._llx_lower_limit <= float(line_json[nlp_core.NLPCore.JSON_NAME_LLX]) <= self._llx_upper_limit and self._rule[2](
                    str(self._entries[-1][4]), target_value
                ):
                    self._entries.append([page_idx, para_no, self._line_idx, self._line_idx, target_value])
                    self._debug_lt(f"Candidate                            =number='{self._rule[0]}' - text='{text[:51]}'")
                    return

                self._finish_list(page_idx)

        rule: LineTypeListNumber._RuleIntern = ()  # type: ignore

        # rule_name, regexp_compiled, function_is_asc, start_values, regexp_str,
        for elem in self._rules_collection:
            if not elem[1].match(target_value):
                continue

            if elem[3]:
                if target_value not in elem[3]:
                    continue

            rule = elem
            break

        if rule:
            if self._rule:
                self._finish_list(page_idx)
        else:
            if self._rule:
                llx = line_json[nlp_core.NLPCore.JSON_NAME_LLX]
                if self._llx_subsequent[0] <= llx <= self._llx_subsequent[1]:
                    # Paragraph already in progress.
                    self._entries[-1][-2] = line_idx
                    self._debug_lt(f"Candidate                            =number='{self._rule[0]}' - text='{text[:51]}'")
                    return

                self._finish_list(page_idx)

            return

        self._rule = rule
        self._llx_subsequent = self._get_llx_subsequent(page_idx, line_json[nlp_core.NLPCore.JSON_NAME_PARA_NO_PAGE] - 1, line_idx + 1)

        if not self._entries:
            # New numbered paragraph.
            self._line_idx_first = self._line_idx
            self._line_idx_last = self._line_idx
            self._llx_lower_limit = round(
                (coord_llx := float(line_json[nlp_core.NLPCore.JSON_NAME_LLX]))
                * (100 - core_glob.inst_setup.lt_list_number_tolerance_llx)
                / 100,
                2,
            )
            self._llx_upper_limit = round(coord_llx * (100 + core_glob.inst_setup.lt_list_number_tolerance_llx) / 100, 2)

        self._entries.append([page_idx, para_no, self._line_idx, self._line_idx, target_value])

        self._debug_lt(f"Candidate                            =number='{self._rule[0]}' - text='{text[:51]}'")

    # ------------------------------------------------------------------
    # Process the page-related data.
    # ------------------------------------------------------------------
    def _process_page(self, page_idx: int, lines_json: list[nlp_core.NLPCore.LineJSON]) -> None:
        """Process the page-related data."""
        self._debug_lt("=" * 80)
        self._debug_lt(f"Start page                           ={page_idx + 1}")
        self._debug_lt("-" * 80)

        for line_idx, line_json in enumerate(lines_json):
            self._line_idx = line_idx

            if line_json[nlp_core.NLPCore.JSON_NAME_TYPE] == nlp_core.NLPCore.LINE_TYPE_BODY:
                self._process_line(page_idx, line_idx, line_json)

        self._debug_lt("-" * 80)
        self._debug_lt(f"End   page                           ={page_idx + 1}")

    # ------------------------------------------------------------------
    # Reset the list memory.
    # ------------------------------------------------------------------
    def _reset_list(self) -> None:
        """Reset the list memory."""
        self._rule = ()  # type: ignore

        self._entries = []

        self._llx_lower_limit = 0.0
        self._llx_subsequent = (0.0, 0.0)
        self._llx_upper_limit = 0.0

        self._debug_lt("Reset the list memory")

    # ------------------------------------------------------------------
    # Check the object existence.
    # ------------------------------------------------------------------
    def exists(self) -> bool:
        """Check the object existence.

        Returns:
            bool: Always true.
        """
        return self._exist

    # ------------------------------------------------------------------
    # Process the document related data.
    # ------------------------------------------------------------------
    def process_document(
        self,
        directory_name: str,
        document_id: int,
        environment_variant: str,
        file_name_curr: str,
        file_name_orig: str,
    ) -> None:
        """Process the document related data.

        Args:
            directory_name (str):
                Directory name of the output file.
            document_id (int):
                Identification of the document.
            environment_variant (str):
                Environment variant: dev, prod or test.
            file_name_curr (str):
                File name of the file to be processed.
            file_name_orig (in):
                File name of the document file.
        """
        core_glob.logger.debug(core_glob.LOGGER_START)
        core_glob.logger.debug("param directory_name     =%s", directory_name)
        core_glob.logger.debug("param document_id        =%i", document_id)
        core_glob.logger.debug("param environment_variant=%s", environment_variant)
        core_glob.logger.debug("param file_name_curr     =%s", file_name_curr)
        core_glob.logger.debug("param file_name_orig     =%s", file_name_orig)

        core_utils.check_exists_object(
            is_nlp_core=True,
            is_setup=True,
            is_text_parser=True,
        )

        self._debug_lt("=" * 80)
        self._debug_lt(f"Start document                       ={self._file_name_curr}")
        self._debug_lt("-" * 37)
        self._debug_lt(f"lt_list_number_file_incl_regexp={core_glob.inst_setup.is_lt_list_number_file_incl_regexp}")
        self._debug_lt(f"lt_list_number_min_entries     ={core_glob.inst_setup.lt_list_number_min_entries}")
        self._debug_lt(f"lt_list_number_rule_file       ={core_glob.inst_setup.lt_list_number_rule_file}")
        self._debug_lt(f"lt_list_number_tolerance_llx   ={core_glob.inst_setup.lt_list_number_tolerance_llx}")

        if self._anti_patterns:
            self._debug_lt("-" * 37)
            for (rule_name, pattern) in self._anti_patterns:
                self._debug_lt(f"Anti pattern                         =rule={rule_name} - pattern={pattern}")

        if self._rules:
            self._debug_lt("-" * 37)
            for [rule_name, regexp_str, _, _] in self._rules:
                self._debug_lt(
                    "Rule                                 ="
                    + f"rule={rule_name.ljust(LineTypeListNumber._RULE_NAME_SIZE)} - regexp={regexp_str}"
                )

        self._file_name_curr = file_name_curr
        self._environment_variant = environment_variant
        self._lists = []
        self._no_lines_line_type = 0

        page_idx_last = 0

        for page_idx, page_json in enumerate(core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES]):
            page_idx_last = page_idx
            self._process_page(page_idx, page_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_LINES])

        self._finish_list(page_idx_last)

        core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_LINES_LIST_NUMBER] = self._no_lines_line_type
        core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_LISTS_NUMBER] = len(self._lists)
        core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_LISTS_NUMBER] = self._lists

        self._debug_lt("-" * 80)
        self._debug_lt(f"End   document                       ={self._file_name_curr}")
        self._debug_lt("=" * 80)

        core_glob.logger.debug(core_glob.LOGGER_END)
