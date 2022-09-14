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


# pylint: disable=too-many-instance-attributes
class LineTypeListNumber:
    """Determine list of numbered lines."""

    Entry = dict[str, int | str]
    Entries = list[Entry]

    List = dict[str, Entries | float | int | object | str]
    Lists = list[List]

    RuleExtern = tuple[str, str, collections.abc.Callable[[str, str], bool], list[str]]
    RuleIntern = tuple[str, re.Pattern[str], collections.abc.Callable[[str, str], bool], list[str], str]

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
            is_line_type_header_footer=True,
            is_line_type_list_bullet=True,
            is_line_type_table=True,
            is_line_type_toc=True,
            is_nlp_core=True,
            is_setup=True,
            is_text_parser=True,
        )

        self._file_name_curr = file_name_curr

        self._environment_variant = ""

        core_utils.check_exists_object(
            is_text_parser=True,
        )

        core_utils.progress_msg(core_glob.setup.is_verbose_lt_list_number, "LineTypeListNumber")
        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_list_number,
            f"LineTypeListNumber: Start create instance                ={self._file_name_curr}",
        )

        self._RULE_NAME_SIZE: int = 20

        self._anti_patterns: list[tuple[str, re.Pattern[str]]] = self._init_anti_patterns()

        # page_idx, para_no, line_lines_idx_from, line_lines_idx_till, target_value
        self._entries: list[list[int | str]] = []

        self._line_idx = -1
        self._lines_json: list[nlp_core.LineJSON] = []
        self._lists: LineTypeListNumber.Lists = []
        self._llx_lower_limit = 0.0
        self._llx_upper_limit = 0.0

        self._max_line_no = 0

        self._no_entries = 0

        self._page_idx = -1
        self._page_idx_prev = -1
        self._para_no = 0
        self._para_no_prev = 0

        self._rule: LineTypeListNumber.RuleIntern = ()  # type: ignore
        self._rules: list[LineTypeListNumber.RuleExtern] = self._init_rules()

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
        self._rules_collection: list[LineTypeListNumber.RuleIntern] = []

        for (rule_name, regexp_str, function_is_asc, start_values) in self._rules:
            self._rules_collection.append(
                (
                    rule_name.ljust(self._RULE_NAME_SIZE),
                    re.compile(regexp_str),
                    function_is_asc,
                    start_values,
                    regexp_str,
                )
            )

        self.no_lists = 0

        self._exist = True

        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_list_number,
            f"LineTypeListNumber: End   create instance                ={self._file_name_curr}",
        )

        core_glob.logger.debug(core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Finish a list.
    # ------------------------------------------------------------------
    def _finish_list(self) -> None:
        """Finish a list."""
        if self._no_entries == 0:
            return

        if self._no_entries < core_glob.setup.lt_list_number_min_entries:
            core_utils.progress_msg(
                core_glob.setup.is_verbose_lt_list_number,
                f"LineTypeListNumber: Not enough list entries    found only={self._no_entries} - "
                + f"number='{self._rule[0]}' - entries={self._entries}",
            )
            self._reset_list()
            return

        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_list_number,
            f"LineTypeListNumber: List entries                    found={self._no_entries} - "
            + f"number='{self._rule[0]}' - entries={self._entries}",
        )

        self.no_lists += 1

        entries: LineTypeListNumber.Entries = []

        for [page_idx, para_no, line_lines_idx_from, line_lines_idx_till, _] in self._entries:
            line_lines: nlp_core.NLPCore.ParserLineLines = core_glob.nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_PAGES][page_idx][
                nlp_core.NLPCore.JSON_NAME_LINES
            ]

            text = []

            for idx in range(int(line_lines_idx_from), int(line_lines_idx_till) + 1):
                line_lines[idx][nlp_core.NLPCore.JSON_NAME_LINE_TYPE] = nlp_core.NLPCore.LINE_TYPE_LIST_NUMBER

                if core_glob.setup.is_create_extra_file_list_number:
                    text.append(line_lines[idx][nlp_core.NLPCore.JSON_NAME_TEXT])

            if core_glob.setup.is_create_extra_file_list_number:
                entries.append(
                    {
                        nlp_core.NLPCore.JSON_NAME_ENTRY_NO: len(entries) + 1,
                        nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE_FROM: int(line_lines_idx_from) + 1,
                        nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE_TILL: int(line_lines_idx_till) + 1,
                        nlp_core.NLPCore.JSON_NAME_PAGE_NO: int(page_idx) + 1,
                        nlp_core.NLPCore.JSON_NAME_PARA_NO: para_no,
                        nlp_core.NLPCore.JSON_NAME_TEXT: " ".join(text),
                    }
                )

            core_glob.nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_PAGES][page_idx][nlp_core.NLPCore.JSON_NAME_LINES] = line_lines

        if core_glob.setup.is_create_extra_file_list_number:
            entry = {
                nlp_core.NLPCore.JSON_NAME_NUMBER: self._rule[0].rstrip(),
                nlp_core.NLPCore.JSON_NAME_LIST_NO: self.no_lists,
                nlp_core.NLPCore.JSON_NAME_NO_ENTRIES: len(entries),
                nlp_core.NLPCore.JSON_NAME_PAGE_NO_FROM: int(self._entries[0][0]) + 1,
                nlp_core.NLPCore.JSON_NAME_PAGE_NO_TILL: int(self._entries[-1][0]) + 1,
            }

            if core_glob.setup.is_lt_list_number_file_incl_regexp:
                entry[nlp_core.NLPCore.JSON_NAME_REGEXP] = self._rule[-1]

            entry[nlp_core.NLPCore.JSON_NAME_ENTRIES] = entries

            self._lists.append(entry)

        self._reset_list()

        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_list_number,
            f"LineTypeListNumber: End   list                    on page={self._page_idx+1}",
        )

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
        if core_glob.setup.lt_list_number_rule_file and core_glob.setup.lt_list_number_rule_file.lower() != "none":
            lt_list_number_rule_file_path = core_utils.get_os_independent_name(core_glob.setup.lt_list_number_rule_file)
            if os.path.isfile(lt_list_number_rule_file_path):
                return self._load_anti_patterns_from_json(pathlib.Path(lt_list_number_rule_file_path))

            core_utils.terminate_fatal(
                f"File with numbered list anti-patterns is missing - " f"file name '{core_glob.setup.lt_list_number_rule_file}'"
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
    def _init_rules(self) -> list[LineTypeListNumber.RuleExtern]:
        """Initialise the numbered list rules.

        Returns:
            list[tuple[str, str, collections.abc.Callable[[str, str], bool], list[str]]]: The
                valid numbered list rules.
        """
        if core_glob.setup.lt_list_number_rule_file and core_glob.setup.lt_list_number_rule_file.lower() != "none":
            lt_list_number_rule_file_path = core_utils.get_os_independent_name(core_glob.setup.lt_list_number_rule_file)
            if os.path.isfile(lt_list_number_rule_file_path):
                return self._load_rules_from_json(pathlib.Path(lt_list_number_rule_file_path))

            core_utils.terminate_fatal(
                f"File with numbered list rules is missing - " f"file name '{core_glob.setup.lt_list_number_rule_file}'"
            )

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
            core_glob.setup.is_verbose_lt_list_number,
            "The numbered list anti-patterns were successfully loaded " + f"from the file {core_glob.setup.lt_list_number_rule_file}",
        )

        return anti_patterns

    # ------------------------------------------------------------------
    # Load numbered list rules from a JSON file.
    # ------------------------------------------------------------------
    @staticmethod
    def _load_rules_from_json(
        lt_list_number_rule_file: pathlib.Path,
    ) -> list[LineTypeListNumber.RuleExtern]:
        """Load numbered list rules from a JSON file.

        Args:
            lt_list_number_rule_file (Path): JSON file.

        Returns:
            list[tuple[str, str, collections.abc.Callable[[str, str], bool], list[str]]]: The valid
                numbered list rules from the JSON file,
        """
        rules: list[LineTypeListNumber.RuleExtern] = []

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
            core_glob.setup.is_verbose_lt_list_number,
            "The list_number rules were successfully loaded from the " + f"file {core_glob.setup.lt_list_number_rule_file}",
        )

        return rules

    # ------------------------------------------------------------------
    # Process the line-related data.
    # ------------------------------------------------------------------
    def _process_line(self, line_json: nlp_core.LineJSON) -> None:  # noqa: C901
        """Process the line-related data.

        Args:
            line_json (nlp_core.LineJSON):
                The line to be processed.
        """
        text = str(line_json[nlp_core.NLPCore.JSON_NAME_TEXT])

        for (rule_name, pattern) in self._anti_patterns:
            if pattern.match(text):
                core_utils.progress_msg(
                    core_glob.setup.is_verbose_lt_list_number,
                    f"LineTypeListNumber: Anti pattern                         ={rule_name} - text={text}",
                )
                return

        para_no = int(line_json[nlp_core.NLPCore.JSON_NAME_PARA_NO])
        target_value = text.split()[0]

        if self._rule:
            if self._rule[1].match(target_value):
                if self._llx_lower_limit <= float(line_json[nlp_core.NLPCore.JSON_NAME_COORD_LLX]) <= self._llx_upper_limit and self._rule[
                    2
                ](str(self._entries[-1][4]), target_value):
                    self._entries.append([self._page_idx, para_no, self._line_idx, self._line_idx, target_value])
                    self._no_entries += 1
                    self._para_no_prev = para_no
                    return

                self._finish_list()

        rule: LineTypeListNumber.RuleIntern = ()  # type: ignore

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
                self._finish_list()
        else:
            if self._rule:
                if self._page_idx == self._page_idx_prev and para_no == self._para_no_prev:
                    # Paragraph already in progress.
                    self._entries[-1][-2] = self._line_idx
                else:
                    self._finish_list()

            self._para_no_prev = para_no
            return

        self._rule = rule

        if not self._entries:
            # New numbered paragraph.
            self._line_lines_idx_from = self._line_idx
            self._line_lines_idx_till = self._line_idx
            self._llx_lower_limit = round(
                (coord_llx := float(line_json[nlp_core.NLPCore.JSON_NAME_COORD_LLX]))
                * (100 - core_glob.setup.lt_list_number_tolerance_llx)
                / 100,
                2,
            )
            self._llx_upper_limit = round(coord_llx * (100 + core_glob.setup.lt_list_number_tolerance_llx) / 100, 2)

        self._entries.append([self._page_idx, para_no, self._line_idx, self._line_idx, target_value])

        self._no_entries += 1

        self._para_no_prev = para_no

    # ------------------------------------------------------------------
    # Process the page-related data.
    # ------------------------------------------------------------------
    def _process_page(self) -> None:
        """Process the page-related data."""
        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_list_number,
            f"LineTypeListNumber: Start page                           ={self._page_idx + 1}",
        )

        for line_idx, line_json in enumerate(self._lines_json):
            self._line_idx = line_idx

            if line_json[nlp_core.NLPCore.JSON_NAME_LINE_TYPE] == nlp_core.NLPCore.LINE_TYPE_BODY:
                self._process_line(line_json)
                self._page_idx_prev = self._page_idx

        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_list_number,
            f"LineTypeListNumber: End   page                           ={self._page_idx + 1}",
        )

    # ------------------------------------------------------------------
    # Reset the document memory.
    # ------------------------------------------------------------------
    def _reset_document(self) -> None:
        """Reset the document memory."""
        self._max_page = core_glob.inst_parser.parse_result_no_pages_in_doc

        self._lists = []

        core_utils.progress_msg(core_glob.setup.is_verbose_lt_list_number, "LineTypeListNumber: Reset the document memory")

        self._reset_list()

    # ------------------------------------------------------------------
    # Reset the list memory.
    # ------------------------------------------------------------------
    def _reset_list(self) -> None:
        """Reset the list memory."""
        self._rule = ()  # type: ignore

        self._entries = []

        self._llx_lower_limit = 0.0
        self._llx_upper_limit = 0.0

        self._no_entries = 0

        self._page_idx_prev = -1
        self._para_no_prev = 0

        self._predecessor = ""

        self._rule = ()  # type: ignore

        core_utils.progress_msg(core_glob.setup.is_verbose_lt_list_number, "LineTypeListNumber: Reset the list memory")

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
            is_line_type_header_footer=True,
            is_line_type_list_bullet=True,
            is_line_type_table=True,
            is_line_type_toc=True,
            is_nlp_core=True,
            is_setup=True,
            is_text_parser=True,
        )

        self._file_name_curr = file_name_curr
        self._environment_variant = environment_variant

        core_utils.progress_msg(core_glob.setup.is_verbose_lt_list_number, "LineTypeListNumber")
        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_list_number,
            f"LineTypeListNumber: Start document                       ={self._file_name_curr}",
        )

        self._reset_document()

        for page_idx, page_json in enumerate(core_glob.nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_PAGES]):
            self._page_idx = page_idx
            self._max_line_no = page_json[nlp_core.NLPCore.JSON_NAME_LINE_NO]
            self._lines_json = page_json[nlp_core.NLPCore.JSON_NAME_LINES]
            self._process_page()

        self._finish_list()

        if core_glob.setup.is_create_extra_file_list_number and self._lists:
            full_name = core_utils.get_full_name_from_components(
                directory_name,
                core_utils.get_stem_name(str(file_name_curr)) + ".list_number." + core_glob.FILE_TYPE_JSON,
            )
            with open(full_name, "w", encoding=core_glob.FILE_ENCODING_DEFAULT) as file_handle:
                json.dump(
                    {
                        nlp_core.NLPCore.JSON_NAME_DOC_ID: document_id,
                        nlp_core.NLPCore.JSON_NAME_DOC_FILE_NAME: file_name_orig,
                        nlp_core.NLPCore.JSON_NAME_NO_LISTS_NUMBER_IN_DOC: self.no_lists,
                        nlp_core.NLPCore.JSON_NAME_LISTS_NUMBER: self._lists,
                    },
                    file_handle,
                    indent=core_glob.setup.json_indent,
                    sort_keys=core_glob.setup.is_json_sort_keys,
                )

        if self.no_lists > 0:
            core_utils.progress_msg(
                core_glob.setup.is_verbose_lt_list_number,
                f"LineTypeListNumber:                 number numbered lists={self.no_lists}",
            )

        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_list_number,
            f"LineTypeListNumber: End   document                       ={self._file_name_curr}",
        )

        core_glob.logger.debug(core_glob.LOGGER_END)
