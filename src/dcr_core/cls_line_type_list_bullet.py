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
import json
import os
import pathlib
import re

import dcr_core.cls_nlp_core as nlp_core
from dcr_core import core_glob
from dcr_core import core_utils


# pylint: disable=too-many-instance-attributes
class LineTypeListBullet:
    """Determine list of bulleted lines."""

    Entry = dict[str, int | str]
    Entries = list[Entry]

    List = dict[str, Entries | float | int | str]
    Lists = list[List]

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
            is_line_type_table=True,
            is_line_type_toc=True,
            is_nlp_core=True,
            is_setup=True,
            is_text_parser=True,
        )

        self._file_name_curr = file_name_curr

        self._environment_variant = ""

        core_utils.progress_msg(core_glob.setup.is_verbose_lt_list_bullet, "LineTypeListBullet")
        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_list_bullet,
            f"LineTypeListBullet: Start create instance                ={self._file_name_curr}",
        )

        self._anti_patterns: list[tuple[str, re.Pattern[str]]] = self._init_anti_patterns()

        self._bullet = ""

        # page_idx, para_no, line_lines_idx_from, line_lines_idx_till
        self._entries: list[list[int]] = []

        self._line_idx = -1
        self._lines_json: list[nlp_core.LineJSON] = []
        self._lists: LineTypeListBullet.Lists = []
        self._llx_lower_limit = 0.0
        self._llx_upper_limit = 0.0

        self._max_line_no = 0

        self._no_entries = 0

        self._page_idx = -1
        self._page_idx_prev = -1
        self._para_no = 0
        self._para_no_prev = 0

        self._rules = self._init_rules()
        for key in self._rules:
            self._rules[key] = len(key)

        self.no_lists = 0

        self._exist = True

        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_list_bullet,
            f"LineTypeListBullet: End   create instance                ={self._file_name_curr}",
        )

        core_glob.logger.debug(core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Finish a list.
    # ------------------------------------------------------------------
    def _finish_list(self) -> None:
        """Finish a list."""
        if self._no_entries == 0:
            return

        if self._no_entries < core_glob.setup.lt_list_bullet_min_entries:
            core_utils.progress_msg(
                core_glob.setup.is_verbose_lt_list_bullet,
                f"LineTypeListBullet: Not enough list entries    found only={self._no_entries} - "
                + f"bullet='{self._bullet}' - entries={self._entries}",
            )
            self._reset_list()
            return

        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_list_bullet,
            f"LineTypeListBullet: List entries                    found={self._no_entries} - "
            + f"bullet='{self._bullet}' - entries={self._entries}",
        )

        self.no_lists += 1

        entries: LineTypeListBullet.Entries = []

        for [page_idx, para_no, line_lines_idx_from, line_lines_idx_till] in self._entries:
            lines_json: list[nlp_core.LineJSON] = core_glob.text_parser.parse_result_line_pages[page_idx][nlp_core.NLPCore.JSON_NAME_LINES]

            text = []

            for idx in range(line_lines_idx_from, line_lines_idx_till + 1):
                lines_json[idx][nlp_core.NLPCore.JSON_NAME_LINE_TYPE] = nlp_core.NLPCore.LINE_TYPE_LIST_BULLET

                if core_glob.setup.is_create_extra_file_list_bullet:
                    text.append(lines_json[idx][nlp_core.NLPCore.JSON_NAME_TEXT])

            if core_glob.setup.is_create_extra_file_list_bullet:
                entries.append(
                    {
                        nlp_core.NLPCore.JSON_NAME_ENTRY_NO: len(entries) + 1,
                        nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE_FROM: line_lines_idx_from + 1,
                        nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE_TILL: line_lines_idx_till + 1,
                        nlp_core.NLPCore.JSON_NAME_PAGE_NO: page_idx + 1,
                        nlp_core.NLPCore.JSON_NAME_PARA_NO: para_no,
                        nlp_core.NLPCore.JSON_NAME_TEXT: " ".join(text),
                    }
                )

            core_glob.text_parser.parse_result_line_pages[page_idx][nlp_core.NLPCore.JSON_NAME_LINES] = lines_json

        if core_glob.setup.is_create_extra_file_list_bullet:
            self._lists.append(
                {
                    nlp_core.NLPCore.JSON_NAME_BULLET: self._bullet.rstrip(),
                    nlp_core.NLPCore.JSON_NAME_LIST_NO: self.no_lists,
                    nlp_core.NLPCore.JSON_NAME_NO_ENTRIES: len(entries),
                    nlp_core.NLPCore.JSON_NAME_PAGE_NO_FROM: self._entries[0][0] + 1,
                    nlp_core.NLPCore.JSON_NAME_PAGE_NO_TILL: self._entries[-1][0] + 1,
                    nlp_core.NLPCore.JSON_NAME_ENTRIES: entries,
                }
            )

        self._reset_list()

        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_list_bullet,
            f"LineTypeListBullet: End   list                    on page={self._page_idx+1}",
        )

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
        if core_glob.setup.lt_list_bullet_rule_file and core_glob.setup.lt_list_bullet_rule_file.lower() != "none":
            lt_list_bullet_rule_file_path = core_utils.get_os_independent_name(core_glob.setup.lt_list_bullet_rule_file)
            if os.path.isfile(lt_list_bullet_rule_file_path):
                return self._load_anti_patterns_from_json(pathlib.Path(lt_list_bullet_rule_file_path))

            core_utils.terminate_fatal(
                f"File with bulleted list anti-patterns is missing - " f"file name '{core_glob.setup.lt_list_bullet_rule_file}'"
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
        """Initialise the valid bullets.

        Returns:
            dict[str, int]: All valid bullets.
        """
        if core_glob.setup.lt_list_bullet_rule_file and core_glob.setup.lt_list_bullet_rule_file.lower() != "none":
            lt_list_bullet_rule_file_path = core_utils.get_os_independent_name(core_glob.setup.lt_list_bullet_rule_file)

            if os.path.isfile(lt_list_bullet_rule_file_path):
                return self._load_rules_from_json(pathlib.Path(lt_list_bullet_rule_file_path))

            core_utils.terminate_fatal(f"File with valid bullets is missing - " f"file name '{core_glob.setup.lt_list_bullet_rule_file}'")

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
            core_glob.setup.is_verbose_lt_list_bullet,
            "The bulleted list anti-patterns were successfully loaded " + f"from the file {core_glob.setup.lt_list_bullet_rule_file}",
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
            core_glob.setup.is_verbose_lt_list_bullet,
            "The list_bullet rules were successfully loaded from the " + f"file {core_glob.setup.lt_list_bullet_rule_file}",
        )

        return list_bullet_rules

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
                    core_glob.setup.is_verbose_lt_list_bullet,
                    f"LineTypeListBullet: Anti pattern                         ={rule_name} - text={text}",
                )
                return

        para_no = int(line_json[nlp_core.NLPCore.JSON_NAME_PARA_NO])

        bullet = ""

        for key, value in self._rules.items():
            if text[0:value] == key:
                bullet = key
                break

        if not bullet:
            if self._page_idx == self._page_idx_prev and para_no == self._para_no_prev:
                # Paragraph already in progress.
                self._entries[-1][-1] = self._line_idx
                return

            self._finish_list()
            return

        if (
            bullet != self._bullet
            or self._llx_upper_limit <= float(line_json[nlp_core.NLPCore.JSON_NAME_COORD_LLX]) <= self._llx_lower_limit
        ):
            self._finish_list()

        self._bullet = bullet

        if not self._entries:
            # New bulleted paragraph.
            self._line_lines_idx_from = self._line_idx
            self._line_lines_idx_till = self._line_idx
            self._llx_lower_limit = round(
                (coord_llx := float(line_json[nlp_core.NLPCore.JSON_NAME_COORD_LLX]))
                * (100 - core_glob.setup.lt_list_bullet_tolerance_llx)
                / 100,
                2,
            )
            self._llx_upper_limit = round(coord_llx * (100 + core_glob.setup.lt_list_bullet_tolerance_llx) / 100, 2)

        self._entries.append([self._page_idx, para_no, self._line_idx, self._line_idx])

        self._no_entries += 1

        self._para_no_prev = para_no

    # ------------------------------------------------------------------
    # Process the page-related data.
    # ------------------------------------------------------------------
    def _process_page(self) -> None:
        """Process the page-related data."""
        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_list_bullet,
            f"LineTypeListBullet: Start page                           ={self._page_idx + 1}",
        )

        for line_idx, line_json in enumerate(self._lines_json):
            self._line_idx = line_idx

            if line_json[nlp_core.NLPCore.JSON_NAME_LINE_TYPE] == nlp_core.NLPCore.LINE_TYPE_BODY:
                self._process_line(line_json)
                self._page_idx_prev = self._page_idx

        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_list_bullet,
            f"LineTypeListBullet: End   page                           ={self._page_idx + 1}",
        )

    # ------------------------------------------------------------------
    # Reset the document memory.
    # ------------------------------------------------------------------
    def _reset_document(self) -> None:
        """Reset the document memory."""
        core_utils.progress_msg(core_glob.setup.is_verbose_lt_list_bullet, "LineTypeListBullet: Reset the document memory")

        self.no_lists = 0

        if core_glob.setup.is_create_extra_file_list_bullet:
            self._lists = []

        self._reset_list()

    # ------------------------------------------------------------------
    # Reset the list memory.
    # ------------------------------------------------------------------
    def _reset_list(self) -> None:
        """Reset the list memory."""
        self._bullet = ""

        self._entries = []

        self._llx_lower_limit = 0.0
        self._llx_upper_limit = 0.0

        self._no_entries = 0

        self._page_idx_prev = -1
        self._para_no_prev = 0

        core_utils.progress_msg(core_glob.setup.is_verbose_lt_list_bullet, "LineTypeListBullet: Reset the list memory")

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
            directory_name (str): Directory name of the output file.
            document_id (int): Identification of the document.
            environment_variant (str): Environment variant: dev, prod or test.
            file_name_curr (str): File name of the file to be processed.
            file_name_orig (in): File name of the document file.
        """
        core_glob.logger.debug(core_glob.LOGGER_START)
        core_glob.logger.debug("param directory_name     =%s", directory_name)
        core_glob.logger.debug("param document_id        =%i", document_id)
        core_glob.logger.debug("param environment_variant=%s", environment_variant)
        core_glob.logger.debug("param file_name_curr     =%s", file_name_curr)
        core_glob.logger.debug("param file_name_orig     =%s", file_name_orig)

        core_utils.check_exists_object(
            is_line_type_header_footer=True,
            is_line_type_table=True,
            is_line_type_toc=True,
            is_setup=True,
            is_nlp_core=True,
            is_text_parser=True,
        )

        self._file_name_curr = file_name_curr
        self._environment_variant = environment_variant

        core_utils.progress_msg(core_glob.setup.is_verbose_lt_list_bullet, "LineTypeListBullet")
        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_list_bullet,
            f"LineTypeListBullet: Start document                       ={self._file_name_curr}",
        )

        self._reset_document()

        for page_idx, page_json in enumerate(core_glob.nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_PAGES]):
            self._page_idx = page_idx
            self._max_line_no = page_json[nlp_core.NLPCore.JSON_NAME_LINE_NO]
            self._lines_json = page_json[nlp_core.NLPCore.JSON_NAME_LINES]
            self._process_page()

        self._finish_list()

        if core_glob.setup.is_create_extra_file_list_bullet and self._lists:
            full_name = core_utils.get_full_name_from_components(
                directory_name,
                core_utils.get_stem_name(str(file_name_curr)) + ".list_bullet." + core_glob.FILE_TYPE_JSON,
            )
            with open(full_name, "w", encoding=core_glob.FILE_ENCODING_DEFAULT) as file_handle:
                json.dump(
                    {
                        nlp_core.NLPCore.JSON_NAME_DOC_ID: document_id,
                        nlp_core.NLPCore.JSON_NAME_DOC_FILE_NAME: file_name_orig,
                        nlp_core.NLPCore.JSON_NAME_NO_LISTS_BULLET_IN_DOC: self.no_lists,
                        nlp_core.NLPCore.JSON_NAME_LISTS_BULLET: self._lists,
                    },
                    file_handle,
                    indent=core_glob.setup.json_indent,
                    sort_keys=core_glob.setup.is_json_sort_keys,
                )

        if self.no_lists > 0:
            core_utils.progress_msg(
                core_glob.setup.is_verbose_lt_list_bullet,
                f"LineTypeListBullet:                 number bulleted lists={self.no_lists}",
            )

        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_list_bullet,
            f"LineTypeListBullet: End   document                       ={self._file_name_curr}",
        )

        core_glob.logger.debug(core_glob.LOGGER_END)
