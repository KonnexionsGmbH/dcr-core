# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.


"""Determine table of content lines.

Typical usage example:

    my_instance = LineTypeHeading()

    if my_instance.exists():

    my_instance.process_document(directory_name = my_directory,
                                 document_id = my_document_id,
                                 file_name_curr = my_file_name_curr,
                                 file_name_orig = my_file_name_orig,
                                 line_pages_json = my_line_pages_json)
"""
from __future__ import annotations

import collections
import decimal
import json
import math
import os
import pathlib
import re

import dcr_core.cls_nlp_core as nlp_core
from dcr_core import core_glob
from dcr_core import core_utils

# ------------------------------------------------------------------
# Global type aliases.
# ------------------------------------------------------------------


# pylint: disable=too-many-instance-attributes
class LineTypeHeading:
    """Determine table of content lines."""

    # ------------------------------------------------------------------
    # 0: rule_name
    # 1: is_first_token:
    #           True:  apply rule to first token (split)
    #           False: apply rule to beginning of line
    # 2: regexp_compiled:
    #           compiled regular expression
    # 3: function_is_asc:
    #           compares predecessor and successor
    # 4: start_values:
    #           list of strings
    # 5: level:
    #           hierarchical level of the current heading
    # 6: llx:
    #           lower left x-coordinate of the beginning of the possible heading
    # 7: predecessor:
    #           predecessor value
    # 8: regexp_str:
    #           regular expression
    # 9: tolerance_llx:
    #           tolerated deviation on the x-axis
    # ------------------------------------------------------------------
    _RuleHierarchyTuple = tuple[
        str,
        bool,
        re.Pattern[str],
        collections.abc.Callable[[str, str], bool],
        list[str],
        int,
        str,
        str,
        str,
        float,
    ]

    _RULE_NAME_SIZE: int = 20

    # ------------------------------------------------------------------
    # Initialise the instance.
    # ------------------------------------------------------------------
    def __init__(
        self,
        file_name_curr: str = "",
    ) -> None:
        """Initialise the instance.

        Args:
            file_name_curr (str, optional):
                File name of the PDF document to be processed -
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

        self._anti_patterns: list[nlp_core.NLPCore.AntiPatternTuple] = self._init_anti_patterns()

        self._file_name_curr = file_name_curr

        self._heading: list[dict[str, int | object | str]] = []

        self._level_prev = 0
        self._line_idx = 0
        self._line_no_max = 0

        self._no_lines_line_type = 0

        self._page_idx = 0
        self._page_no_max = 0

        self._rules: list[nlp_core.NLPCore.RuleTuple] = self._init_rules()

        self._rules_collection: list[nlp_core.NLPCore.RuleTuple] = []

        for (rule_name, is_first_token, regexp_str, function_is_asc, start_values, tolerance_llx) in self._rules:
            self._rules_collection.append(
                (
                    rule_name.ljust(LineTypeHeading._RULE_NAME_SIZE),
                    is_first_token,
                    re.compile(regexp_str),
                    function_is_asc,
                    start_values,
                    regexp_str,
                    tolerance_llx,
                )
            )

        self._rules_hierarchy: list[LineTypeHeading._RuleHierarchyTuple] = []

        self._exist = True

        core_glob.logger.debug(core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Check whether a valid start value is present.
    # ------------------------------------------------------------------
    @staticmethod
    def _check_valid_start_value(target_value: str, is_first_token: bool, start_values: list[str]) -> bool:  # noqa: C901
        """Check whether a valid start value is present.

        Args:
            target_value (str):
                Value to be checked.
            is_first_token (bool):
                Restrict the check to the first token.
            start_values (list[str]):
                Valid start values.

        Returns:
            bool: True if a valid start value is present, false else.
        """
        if is_first_token:
            try:
                float(target_value)
                target_value_decimal = decimal.Decimal(target_value)
                target_fraction = target_value_decimal - math.floor(target_value_decimal)

                for start_value in start_values:
                    try:
                        start_value_decimal = decimal.Decimal(start_value)
                        start_fraction = start_value_decimal - math.floor(start_value_decimal)

                        if target_fraction == start_fraction:
                            return True
                    except ValueError:
                        pass

                return False
            except ValueError:
                if target_value in start_values:
                    return True
                return False

        for start_value in start_values:
            start_value_len = len(start_value)

            if len(target_value) < start_value_len:
                continue

            if start_value == target_value[0:start_value_len]:
                return True

        return False

    # ------------------------------------------------------------------
    # Create a table of content entry.
    # ------------------------------------------------------------------
    def _create_toc_entry(self, level: int, page_idx: int, line_json: nlp_core.NLPCore.LineJSON) -> None:
        """Create a table of content entry.

        Args:
            level (int):
                Heading level.
            page_idx (int):
                Index of current page.
            line_json (nlp_core.NLPCore.LineJSON):
                Current JSON line.
        """
        heading_entry = {}

        if core_glob.inst_setup.lt_heading_file_incl_no_ctx > 0:
            page_idx_local = page_idx
            line_lines: list[nlp_core.NLPCore.LineJSON] = core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES][
                page_idx_local
            ][nlp_core.NLPCore.JSON_NAME_CONTAINER_LINES]
            line_idx = self._line_idx + 1

            for idx in range(core_glob.inst_setup.lt_heading_file_incl_no_ctx):
                (text, new_page_idx, new_line_lines, new_line_idx) = self._get_next_body_line(page_idx_local, line_lines, line_idx)

                heading_entry[nlp_core.NLPCore.JSON_NAME_CTX_LINE_ + str(idx + 1)] = text

                line_lines = new_line_lines
                line_idx = new_line_idx
                page_idx_local = new_page_idx

        heading_entry[nlp_core.NLPCore.JSON_NAME_LEVEL] = level
        heading_entry[nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE] = line_json[nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE]
        heading_entry[nlp_core.NLPCore.JSON_NAME_LINE_NO_PARA] = line_json[nlp_core.NLPCore.JSON_NAME_LINE_NO_PARA]
        heading_entry[nlp_core.NLPCore.JSON_NAME_PAGE_NO] = page_idx + 1
        heading_entry[nlp_core.NLPCore.JSON_NAME_PARA_NO_PAGE] = line_json[nlp_core.NLPCore.JSON_NAME_PARA_NO_PAGE]

        if core_glob.inst_setup.is_lt_heading_file_incl_regexp:
            heading_entry[nlp_core.NLPCore.JSON_NAME_REGEXP] = self._rules_hierarchy[level - 1][8]

        heading_entry[nlp_core.NLPCore.JSON_NAME_TEXT] = line_json[nlp_core.NLPCore.JSON_NAME_TEXT]

        self._heading.append(heading_entry)

    # ------------------------------------------------------------------
    # Debug line type processing.
    # ------------------------------------------------------------------
    @staticmethod
    def _debug_lt(msg: str) -> None:
        """Debug line type processing.

        Args:
            msg (str):
                Debug message.
        """
        core_utils.progress_msg(
            core_glob.inst_setup.is_verbose_lt_heading,
            "LineTypeHeading: " + msg,
        )

    # ------------------------------------------------------------------
    # Get the next body line.
    # ------------------------------------------------------------------
    def _get_next_body_line(
        self, page_idx: int, lines_json: list[nlp_core.NLPCore.LineJSON], line_idx: int
    ) -> tuple[str, int, list[nlp_core.NLPCore.LineJSON], int]:
        """Get the next body line.

        Args:
            page_idx (int):
                Start with this page number.
            lines_json (LineLines):
                The lines of the start page.
            line_idx (int):
                Start with this line number.

        Returns:
            tuple[str, int, LineLines, int]: Found line or empty,
                last page searched, lines of this page, last checked line.
        """
        for idx in range(line_idx + 1, len(lines_json)):
            line_json: nlp_core.NLPCore.LineJSON = lines_json[idx]

            if line_json[nlp_core.NLPCore.JSON_NAME_TYPE] != nlp_core.NLPCore.LINE_TYPE_BODY:
                continue

            return line_json[nlp_core.NLPCore.JSON_NAME_TEXT], page_idx, lines_json, idx

        if (page_idx + 1) < self._page_no_max:
            page_idx_local = page_idx + 1
            lines_json_local: list[nlp_core.NLPCore.LineJSON] = core_glob.inst_nlp_core.document_json[
                nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES
            ][page_idx_local][nlp_core.NLPCore.JSON_NAME_CONTAINER_LINES]

            for idx, line_json in enumerate(lines_json_local):
                if line_json[nlp_core.NLPCore.JSON_NAME_TYPE] != nlp_core.NLPCore.LINE_TYPE_BODY:
                    continue

                return (
                    line_json[nlp_core.NLPCore.JSON_NAME_TEXT],
                    page_idx_local,
                    lines_json_local,
                    idx + 1,
                )

        # not testable
        return "", page_idx, lines_json, line_idx

    # ------------------------------------------------------------------
    # Initialise the heading anti-patterns.
    # ------------------------------------------------------------------
    def _init_anti_patterns(self) -> list[nlp_core.NLPCore.AntiPatternTuple]:
        """Initialise the heading anti-patterns.

        Returns:
            list[_AntiPatternTuple]:
                The valid heading anti-patterns.
        """
        if core_glob.inst_setup.lt_heading_rule_file and core_glob.inst_setup.lt_heading_rule_file.lower() != "none":
            lt_heading_rule_file_path = core_utils.get_os_independent_name(core_glob.inst_setup.lt_heading_rule_file)
            if os.path.isfile(lt_heading_rule_file_path):
                return self._load_anti_patterns_from_json(pathlib.Path(lt_heading_rule_file_path))

            core_utils.terminate_fatal(
                f"File with heading anti-patterns is missing - " f"file name '{core_glob.inst_setup.lt_heading_rule_file}'"
            )

        anti_patterns = []

        for name, regexp in nlp_core.NLPCore.get_lt_anti_patterns_default_heading():
            anti_patterns.append((name, re.compile(regexp)))

        return anti_patterns

    # ------------------------------------------------------------------
    # Initialise the heading rules.
    # ------------------------------------------------------------------
    def _init_rules(self) -> list[nlp_core.NLPCore.RuleTuple]:
        """Initialise the heading rules.

        Returns:
            list[tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str], float]]:
                The valid heading rules.
        """
        if core_glob.inst_setup.lt_heading_rule_file and core_glob.inst_setup.lt_heading_rule_file.lower() != "none":
            lt_heading_rule_file_path = core_utils.get_os_independent_name(core_glob.inst_setup.lt_heading_rule_file)
            if os.path.isfile(lt_heading_rule_file_path):
                return self._load_rules_from_json(pathlib.Path(lt_heading_rule_file_path))

            core_utils.terminate_fatal(f"File with heading rules is missing - " f"file name '{core_glob.inst_setup.lt_heading_rule_file}'")

        return nlp_core.NLPCore.get_lt_rules_default_heading()

    # ------------------------------------------------------------------
    # Load the valid heading anti-patterns from a JSON file.
    # ------------------------------------------------------------------
    @staticmethod
    def _load_anti_patterns_from_json(
        lt_heading_rule_file: pathlib.Path,
    ) -> list[tuple[str, re.Pattern[str]]]:
        """Load the valid heading anti-patterns from a JSON file.

        Args:
            lt_heading_rule_file (Path):
                JSON file.

        Returns:
            list[tuple[str, re.Pattern[str]]]:
                The valid heading anti-patterns from the JSON file,
        """
        anti_patterns = []

        with open(lt_heading_rule_file, "r", encoding=core_glob.FILE_ENCODING_DEFAULT) as file_handle:
            json_data = json.load(file_handle)

            for rule in json_data[nlp_core.NLPCore.JSON_NAME_LINE_TYPE_ANTI_PATTERNS]:
                anti_patterns.append(
                    (
                        rule[nlp_core.NLPCore.JSON_NAME_NAME],
                        re.compile(rule[nlp_core.NLPCore.JSON_NAME_REGEXP]),
                    )
                )

        core_utils.progress_msg(
            core_glob.inst_setup.is_verbose_lt_heading,
            "The heading anti-patterns were successfully loaded from the " + f"file {core_glob.inst_setup.lt_heading_rule_file}",
        )

        return anti_patterns

    # ------------------------------------------------------------------
    # Load the valid heading rules from a JSON file.
    # ------------------------------------------------------------------
    @staticmethod
    def _load_rules_from_json(
        lt_heading_rule_file: pathlib.Path,
    ) -> list[nlp_core.NLPCore.RuleTuple]:
        """Load the valid heading rules from a JSON file.

        Args:
            lt_heading_rule_file (Path):
                JSON file.

        Returns:
            list[_RuleTuple]:
                The valid heading rules from the JSON file,
        """
        rules = []

        with open(lt_heading_rule_file, "r", encoding=core_glob.FILE_ENCODING_DEFAULT) as file_handle:
            json_data = json.load(file_handle)

            for rule in json_data[nlp_core.NLPCore.JSON_NAME_LINE_TYPE_RULES]:
                rules.append(
                    (
                        rule[nlp_core.NLPCore.JSON_NAME_NAME],
                        rule[nlp_core.NLPCore.JSON_NAME_IS_FIRST_TOKEN],
                        rule[nlp_core.NLPCore.JSON_NAME_REGEXP],
                        getattr(
                            nlp_core.NLPCore,
                            "is_asc_" + rule[nlp_core.NLPCore.JSON_NAME_FUNCTION_IS_ASC],
                        ),
                        rule[nlp_core.NLPCore.JSON_NAME_START_VALUES],
                        rule[nlp_core.NLPCore.JSON_NAME_TOLERANCE_LLX]
                        if nlp_core.NLPCore.JSON_NAME_TOLERANCE_LLX in rule
                        else core_glob.inst_setup.lt_heading_tolerance_llx,
                    )
                )

        core_utils.progress_msg(
            core_glob.inst_setup.is_verbose_lt_heading,
            f"The heading rules were successfully loaded from the file {core_glob.inst_setup.lt_heading_rule_file}",
        )

        return rules

    # ------------------------------------------------------------------
    # Process the line-related data.
    # ------------------------------------------------------------------
    def _process_line(self, page_idx: int, line_json: nlp_core.NLPCore.LineJSON, first_token: str) -> int:  # noqa: C901
        """Process the line-related data.

        Args:
            page_idx (int):
                The index of the current page.
            line_json (nlp_core.NLPCore.LineJSON):
                The line to be processed.
            first_token (str): The first token of the text.

        Returns:
            int: The heading level or zero.
        """
        text = line_json[nlp_core.NLPCore.JSON_NAME_TEXT]

        for (rule_name, pattern) in self._anti_patterns:
            if pattern.match(text):
                self._debug_lt(f"Anti pattern                         ={rule_name} - text={text}")
                return 0

        llx_curr = line_json[nlp_core.NLPCore.JSON_NAME_LLX]

        for ph_idx in reversed(range(ph_size := len(self._rules_hierarchy))):
            (
                rule_name,
                is_first_token,
                regexp_compiled,
                function_is_asc,
                start_values,
                level,
                llx,
                predecessor,
                regexp_str,
            ) = self._rules_hierarchy[ph_idx]

            target_value = first_token if is_first_token else text

            if regexp_compiled.match(target_value):
                if not function_is_asc(predecessor, target_value):
                    if self._check_valid_start_value(target_value, is_first_token, start_values):
                        break
                    continue

                llx_curr_float = float(llx_curr)
                llx_float = float(llx)

                if (
                    llx_curr_float < llx_float * (100 - core_glob.inst_setup.lt_heading_tolerance_llx) / 100
                    or llx_curr_float > llx_float * (100 + core_glob.inst_setup.lt_heading_tolerance_llx) / 100
                ):
                    return 0

                self._rules_hierarchy[ph_idx] = (
                    rule_name,
                    is_first_token,
                    regexp_compiled,
                    function_is_asc,
                    start_values,
                    level,
                    llx,
                    target_value,
                    regexp_str,
                )

                self._level_prev = level

                self._create_toc_entry(level, page_idx, line_json)

                self._debug_lt(
                    f"Match                                ={rule_name} " + f"- level={level} - heading={text}",
                )

                # Delete levels that are no longer needed
                if ph_size > level:
                    for i in range(ph_size - 1, level - 1, -1):
                        del self._rules_hierarchy[i]

                return level

        for (
            rule_name,
            is_first_token,
            regexp_compiled,
            function_is_asc,
            start_values,
            regexp_str,
        ) in self._rules_collection:
            target_value = first_token if is_first_token else text
            if regexp_compiled.match(target_value):
                if not self._check_valid_start_value(target_value, is_first_token, start_values):
                    continue

                level = self._level_prev + 1

                self._rules_hierarchy.append(
                    (
                        rule_name,
                        is_first_token,
                        regexp_compiled,
                        function_is_asc,
                        start_values,
                        level,
                        llx_curr,
                        target_value,
                        regexp_str,
                    )
                )

                self._level_prev = level

                self._create_toc_entry(level, page_idx, line_json)

                self._debug_lt(f"Match new level                      ={rule_name} " + f"- level={level} - heading={text}")

                return level

        return 0

    # ------------------------------------------------------------------
    # Process the page-related data.
    # ------------------------------------------------------------------
    def _process_page(self, page_idx: int, lines_json: list[nlp_core.NLPCore.LinesJSON]) -> None:
        """Process the page-related data.

        Args:
            page_idx (int):
                The index of the current page.
            lines_json (nlp_core.NLPCore.LineJSON):
                The lines to be processed.
        """
        self._debug_lt("=" * 80)
        self._debug_lt(f"Start page                           ={page_idx + 1}")
        self._debug_lt("-" * 80)

        self._line_no_max = len(lines_json)

        for line_idx, line_json in enumerate(lines_json):
            self._line_idx = line_idx

            if line_json[nlp_core.NLPCore.JSON_NAME_TYPE] != nlp_core.NLPCore.LINE_TYPE_BODY:
                continue

            if (text := line_json[nlp_core.NLPCore.JSON_NAME_TEXT]) == "":
                # not testable
                continue

            if (first_token := text.split()[0]) == text:
                continue

            if (level := self._process_line(page_idx, line_json, first_token)) > 0:
                line_json[nlp_core.NLPCore.JSON_NAME_TYPE] = nlp_core.NLPCore.LINE_TYPE_HEADER + "_" + str(level)
                lines_json[self._line_idx] = line_json
                self._no_lines_line_type += 1

        self._debug_lt("-" * 80)
        self._debug_lt(f"End   page                           ={page_idx + 1}")

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
        file_name_curr: str,
        file_name_orig: str,
    ) -> None:
        """Process the document related data.

        Args:
            directory_name (str):
                Directory name of the output file.
            document_id (int):
                Identification of the document.
            file_name_curr (str):
                File name of the file to be processed.
            file_name_orig (in):
                File name of the document file.
        """
        core_glob.logger.debug(core_glob.LOGGER_START)
        core_glob.logger.debug("param directory_name =%s", directory_name)
        core_glob.logger.debug("param document_id    =%i", document_id)
        core_glob.logger.debug("param file_name_curr =%s", file_name_curr)
        core_glob.logger.debug("param file_name_orig =%s", file_name_orig)

        core_utils.check_exists_object(
            is_nlp_core=True,
            is_setup=True,
            is_text_parser=True,
        )

        self._file_name_curr = file_name_curr

        self._debug_lt("=" * 80)
        self._debug_lt(f"Start document                       ={self._file_name_curr}")
        self._debug_lt("-" * 37)
        self._debug_lt(f"lt_heading_file_incl_no_ctx={core_glob.inst_setup.lt_heading_file_incl_no_ctx}")
        self._debug_lt(f"lt_heading_file_incl_regexp={core_glob.inst_setup.is_lt_heading_file_incl_regexp}")
        self._debug_lt(f"lt_heading_max_level       ={core_glob.inst_setup.lt_heading_max_level}")
        self._debug_lt(f"lt_heading_min_pages       ={core_glob.inst_setup.lt_heading_min_pages}")
        self._debug_lt(f"lt_heading_rule_file       ={core_glob.inst_setup.lt_heading_rule_file}")
        self._debug_lt(f"lt_heading_tolerance_llx   ={core_glob.inst_setup.lt_heading_tolerance_llx}")

        if self._anti_patterns:
            self._debug_lt("-" * 37)
            for (rule_name, pattern) in self._anti_patterns:
                self._debug_lt(f"Anti pattern                         =rule={rule_name} - pattern={pattern}")

        if self._rules:
            for [rule_name, _, _, _, regexp_str, _] in self._rules:
                self._debug_lt(
                    "Rule                                 ="
                    + f"rule={rule_name.ljust(LineTypeHeading._RULE_NAME_SIZE)} - regexp={regexp_str}"
                )

        if (
            core_glob.inst_setup.lt_heading_max_level == 0
            or core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_PAGES] < core_glob.inst_setup.lt_heading_min_pages
        ):
            core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_HEADING] = []
            self._debug_lt("End (not required)")
            self._debug_lt("=" * 80)
            return

        self._heading = []
        self._no_lines_line_type = 0
        self._page_no_max = core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_PAGES]

        for page_idx, page_json in enumerate(core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES]):
            self._process_page(page_idx, page_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_LINES])

        core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_LINES_HEADING] = self._no_lines_line_type
        core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_HEADING] = self._heading

        self._debug_lt("-" * 80)
        self._debug_lt(f"End   document                       ={self._file_name_curr}")
        self._debug_lt("=" * 80)

        core_glob.logger.debug(core_glob.LOGGER_END)
