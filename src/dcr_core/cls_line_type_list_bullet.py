# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Determine list of bulleted lines.

Typical usage example:

    my_instance = LineTypeListBullet()

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
class LineTypeListBullet:
    """Determine list of bulleted lines."""

    _RuleExtern = tuple[str, str, collections.abc.Callable[[str, str], bool], list[str]]

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

        self._bullet = ""

        # page_idx, para_no, line_idx_first, line_idx_last
        self._entries: list[list[int]] = []

        self._line_idx = -1
        self._lists: list[nlp_core.NLPCore.ListJSON] = []
        self._llx_lower_limit = 0.0
        self._llx_upper_limit = 0.0

        self._page_idx_prev = -1
        self._para_no_prev = 0

        self._rules = self._init_rules()
        for key in self._rules:
            self._rules[key] = len(key)

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
            core_glob.inst_setup.is_verbose_lt_list_bullet,
            "LineTypeListBullet: " + msg,
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

        if no_entries < core_glob.inst_setup.lt_list_bullet_min_entries:
            self._debug_lt(
                f"Not enough list entries              ={page_idx + 1} found only={no_entries} - "
                + f"bullet='{self._bullet}' - entries={self._entries}"
            )
            self._reset_list()
            self._debug_lt(f"End   list on page                   ={page_idx + 1}")
            self._debug_lt("-" * 80)
            return

        self._debug_lt(
            f"List entries                         ={page_idx + 1} verified  ={no_entries} - "
            + f"bullet='{self._bullet}' - entries={self._entries}"
        )

        entries: LineTypeListBullet.Entries = []

        for [page_idx_list, para_no, line_idx_first, line_idx_last] in self._entries:
            lines_json: list[nlp_core.NLPCore.LineJSON] = core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES][
                page_idx_list
            ][nlp_core.NLPCore.JSON_NAME_CONTAINER_LINES]

            text = []

            for idx in range(line_idx_first, line_idx_last + 1):
                lines_json[idx][nlp_core.NLPCore.JSON_NAME_TYPE] = nlp_core.NLPCore.LINE_TYPE_LIST_BULLET

                para_no_page = lines_json[idx][nlp_core.NLPCore.JSON_NAME_PARA_NO_PAGE]

                for word in core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES][page_idx_list][
                    nlp_core.NLPCore.JSON_NAME_CONTAINER_PARAS
                ][para_no_page - 1][nlp_core.NLPCore.JSON_NAME_CONTAINER_WORDS]:
                    word_line_no_page = word[nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE]
                    if word_line_no_page > line_idx_last + 1:
                        break
                    if word_line_no_page < line_idx_first + 1:
                        continue
                    word[nlp_core.NLPCore.JSON_NAME_TYPE] = nlp_core.NLPCore.LINE_TYPE_LIST_BULLET

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
                nlp_core.NLPCore.JSON_NAME_FORMAT: self._bullet.rstrip(),
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
    # Initialise the bulleted list anti-patterns.
    # ------------------------------------------------------------------
    # 1: name:  pattern name
    # 2: regexp regular expression
    # ------------------------------------------------------------------
    def _init_anti_patterns(self) -> list[tuple[str, re.Pattern[str]]]:
        """Initialise the bulleted list anti-patterns.

        Returns:
            list[tuple[str, re.Pattern[str]]]: The valid bulleted list anti-patterns.
        """
        if core_glob.inst_setup.lt_list_bullet_rule_file and core_glob.inst_setup.lt_list_bullet_rule_file.lower() != "none":
            lt_list_bullet_rule_file_path = core_utils.get_os_independent_name(core_glob.inst_setup.lt_list_bullet_rule_file)
            if os.path.isfile(lt_list_bullet_rule_file_path):
                return self._load_anti_patterns_from_json(pathlib.Path(lt_list_bullet_rule_file_path))

            core_utils.terminate_fatal(
                f"File with bulleted list anti-patterns is missing - " f"file name '{core_glob.inst_setup.lt_list_bullet_rule_file}'"
            )

        anti_patterns = []

        for name, regexp in nlp_core.NLPCore.get_lt_anti_patterns_default_list_bullet(environment_variant=self._environment_variant):
            anti_patterns.append((name, re.compile(regexp)))

        return anti_patterns

    # ------------------------------------------------------------------
    # Initialise the valid bullets.
    # ------------------------------------------------------------------
    # 1: bullet character(s)
    # ------------------------------------------------------------------
    def _init_rules(self) -> dict[str, int]:
        """Initialise the bulleted list rules.

        Returns:
            dict[str, int]: The valid bulleted list rules.
        """
        self._debug_lt("=" * 80)
        self._debug_lt("Start initialise rules")
        self._debug_lt("-" * 80)

        if core_glob.inst_setup.lt_list_bullet_rule_file and core_glob.inst_setup.lt_list_bullet_rule_file.lower() != "none":
            lt_list_bullet_rule_file_path = core_utils.get_os_independent_name(core_glob.inst_setup.lt_list_bullet_rule_file)

            if os.path.isfile(lt_list_bullet_rule_file_path):
                return self._load_rules_from_json(pathlib.Path(lt_list_bullet_rule_file_path))

            core_utils.terminate_fatal(
                f"File with valid bullets is missing - " f"file name '{core_glob.inst_setup.lt_list_bullet_rule_file}'"
            )

        self._debug_lt("-" * 80)
        self._debug_lt("End   initialise rules")

        return nlp_core.NLPCore.get_lt_rules_default_list_bullet()

    # ------------------------------------------------------------------
    # Load the valid bulleted list anti-patterns from a JSON file.
    # ------------------------------------------------------------------
    @staticmethod
    def _load_anti_patterns_from_json(
        lt_list_bullet_rule_file: pathlib.Path,
    ) -> list[tuple[str, re.Pattern[str]]]:
        """Load the valid bulleted list anti-patterns from a JSON file.

        Args:
            lt_list_bullet_rule_file (Path): JSON file.

        Returns:
            list[tuple[str, re.Pattern[str]]]: The valid
                bulleted list anti-patterns from the JSON file,
        """
        anti_patterns = []

        with open(lt_list_bullet_rule_file, "r", encoding=core_glob.FILE_ENCODING_DEFAULT) as file_handle:
            json_data = json.load(file_handle)

            for rule in json_data[nlp_core.NLPCore.JSON_NAME_LINE_TYPE_ANTI_PATTERNS]:
                anti_patterns.append(
                    (
                        rule[nlp_core.NLPCore.JSON_NAME_NAME],
                        re.compile(rule[nlp_core.NLPCore.JSON_NAME_REGEXP]),
                    )
                )

        core_utils.progress_msg(
            core_glob.inst_setup.is_verbose_lt_list_bullet,
            "The bulleted list anti-patterns were successfully loaded " + f"from the file {core_glob.inst_setup.lt_list_bullet_rule_file}",
        )

        return anti_patterns

    # ------------------------------------------------------------------
    # Load the valid bullets from a JSON file.
    # ------------------------------------------------------------------
    @staticmethod
    def _load_rules_from_json(
        lt_list_bullet_rule_file: pathlib.Path,
    ) -> dict[str, int]:
        """Load the valid bullets from a JSON file.

        Args:
            lt_list_bullet_rule_file (Path): JSON file name including directory path.

        Returns:
            dict[str, int]: The valid bullets from the JSON file,
        """
        list_bullet_rules = {}

        with open(lt_list_bullet_rule_file, "r", encoding=core_glob.FILE_ENCODING_DEFAULT) as file_handle:
            json_data = json.load(file_handle)

            for bullet in json_data[nlp_core.NLPCore.JSON_NAME_LINE_TYPE_RULES]:
                list_bullet_rules[bullet] = 0

        core_utils.progress_msg(
            core_glob.inst_setup.is_verbose_lt_list_bullet,
            "The list_bullet rules were successfully loaded from the " + f"file {core_glob.inst_setup.lt_list_bullet_rule_file}",
        )

        return list_bullet_rules

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

        bullet = ""

        for key, value in self._rules.items():
            if text[0:value] == key:
                bullet = key
                break

        if not bullet:
            if page_idx == self._page_idx_prev and para_no == self._para_no_prev:
                # Paragraph already in progress.
                self._entries[-1][-1] = line_idx
                return

            self._finish_list(page_idx)
            return

        if bullet != self._bullet or self._llx_upper_limit <= float(line_json[nlp_core.NLPCore.JSON_NAME_LLX]) <= self._llx_lower_limit:
            self._finish_list(page_idx)

        self._bullet = bullet

        if not self._entries:
            # New bulleted paragraph.
            self._line_idx_first = self._line_idx
            self._line_idx_last = self._line_idx
            self._llx_lower_limit = round(
                (coord_llx := float(line_json[nlp_core.NLPCore.JSON_NAME_LLX]))
                * (100 - core_glob.inst_setup.lt_list_bullet_tolerance_llx)
                / 100,
                2,
            )
            self._llx_upper_limit = round(coord_llx * (100 + core_glob.inst_setup.lt_list_bullet_tolerance_llx) / 100, 2)

        self._entries.append([page_idx, para_no, self._line_idx, self._line_idx])

        self._debug_lt(f"Candidate                            =bullet='{self._bullet}' - text='{text[:51]}'")

        self._para_no_prev = para_no

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
                self._page_idx_prev = page_idx

        self._debug_lt("-" * 80)
        self._debug_lt(f"End   page                           ={page_idx + 1}")

    # ------------------------------------------------------------------
    # Reset the list memory.
    # ------------------------------------------------------------------
    def _reset_list(self) -> None:
        """Reset the list memory."""
        self._bullet = ""

        self._entries = []

        self._llx_lower_limit = 0.0
        self._llx_upper_limit = 0.0

        self._page_idx_prev = -1
        self._para_no_prev = 0

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
        self._debug_lt(f"lt_list_bullet_min_entries  ={core_glob.inst_setup.lt_list_bullet_min_entries}")
        self._debug_lt(f"lt_list_bullet_rule_file    ={core_glob.inst_setup.lt_list_bullet_rule_file}")
        self._debug_lt(f"lt_list_bullet_tolerance_llx={core_glob.inst_setup.lt_list_bullet_tolerance_llx}")

        if self._anti_patterns:
            self._debug_lt("-" * 37)
            for (rule_name, pattern) in self._anti_patterns:
                self._debug_lt(f"Anti pattern                         =rule={rule_name} - pattern={pattern}")

        if self._rules:
            self._debug_lt("-" * 37)
            for key, value in self._rules.items():
                self._debug_lt(f"Rule                                 =key={key} - value={value}")

        self._file_name_curr = file_name_curr
        self._environment_variant = environment_variant

        self._lists = []

        page_idx_last = 0

        for page_idx, page_json in enumerate(core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_PAGES]):
            page_idx_last = page_idx
            self._process_page(page_idx, page_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_LINES])

        self._finish_list(page_idx_last)

        core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_NO_LISTS_BULLET] = len(self._lists)
        core_glob.inst_nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_CONTAINER_LISTS_BULLET] = self._lists

        self._debug_lt("-" * 80)
        self._debug_lt(f"End   document                       ={self._file_name_curr}")
        self._debug_lt("=" * 80)

        core_glob.logger.debug(core_glob.LOGGER_END)
