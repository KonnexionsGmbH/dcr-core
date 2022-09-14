# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Determine table of content lines.

Typical usage example:

    my_instance = LineTypeTable()

    if my_instance.exists():

    my_instance.process_document(directory_name = my_directory,
                                 document_id = my_document_id,
                                 file_name_curr = my_file_name_curr,
                                 file_name_orig = my_file_name_orig,
                                 line_pages_json = my_line_pages_json)
"""

import json

import dcr_core.cls_nlp_core as nlp_core
from dcr_core import core_glob
from dcr_core import core_utils


# pylint: disable=too-many-instance-attributes
class LineTypeTable:
    """Determine table of content lines."""

    Column = dict[str, float | int | object | str]
    Columns = list[Column]

    Row = dict[str, Columns | float | int | str]
    Rows = list[Row]

    Table = dict[str, float | int | Rows]
    Tables = list[Table]

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
            is_line_type_toc=True,
            is_nlp_core=True,
            is_setup=True,
            is_text_parser=True,
        )

        self._file_name_curr = file_name_curr

        core_utils.progress_msg(core_glob.setup.is_verbose_lt_table, "LineTypeTable")
        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_table,
            f"LineTypeTable: Start create instance                ={self._file_name_curr}",
        )

        self._column_no = 0
        self._column_no_prev = 0
        self._columns: LineTypeTable.Columns = []

        self._first_column_llx = 0.0
        self._first_row_llx = 0.0
        self._first_row_urx = 0.0

        self._is_table_open = False

        self._last_column_urx = 0.0
        self._lines_json: list[nlp_core.LineJSON] = []

        self._max_line_no = 0

        self._no_columns_table = 0
        self._no_rows = 0

        self._page_idx = 0
        self._page_no_from = 0
        self._page_no_till = 0

        self._row_no = 0
        self._row_no_prev = 0
        self._rows: LineTypeTable.Rows = []

        self._tables: LineTypeTable.Tables = []

        self.no_tables = 0

        self._exist = True

        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_table,
            f"LineTypeTable: End   create instance                ={self._file_name_curr}",
        )

        core_glob.logger.debug(core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Finish a row.
    # ------------------------------------------------------------------
    def _finish_row(self) -> None:
        """Finish a row."""
        if (no_columns := len(self._columns)) == 0:
            return

        self._no_columns_table += no_columns
        row_no = len(self._rows) + 1

        self._rows.append(
            {
                nlp_core.NLPCore.JSON_NAME_FIRST_COLUMN_LLX: self._first_column_llx,
                nlp_core.NLPCore.JSON_NAME_LAST_COLUMN_URX: self._last_column_urx,
                nlp_core.NLPCore.JSON_NAME_NO_COLUMNS: no_columns,
                nlp_core.NLPCore.JSON_NAME_ROW_NO: row_no,
                nlp_core.NLPCore.JSON_NAME_COLUMNS: self._columns,
            }
        )

        self._reset_row()

        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_table,
            f"LineTypeTable: End   row                            ={row_no}",
        )

    # ------------------------------------------------------------------
    # Finish a table.
    # ------------------------------------------------------------------
    def _finish_table(self) -> None:
        """Finish a table."""
        if not self._is_table_open:
            return

        self._finish_row()

        self.no_tables += 1
        self._page_no_till = self._page_idx + 1

        self._tables.append(
            {
                nlp_core.NLPCore.JSON_NAME_FIRST_ROW_LLX: self._first_row_llx,
                nlp_core.NLPCore.JSON_NAME_FIRST_ROW_URX: self._first_row_urx,
                nlp_core.NLPCore.JSON_NAME_NO_COLUMNS: self._no_columns_table,
                nlp_core.NLPCore.JSON_NAME_NO_ROWS: len(self._rows),
                nlp_core.NLPCore.JSON_NAME_PAGE_NO_FROM: self._page_no_from,
                nlp_core.NLPCore.JSON_NAME_PAGE_NO_TILL: self._page_no_till,
                nlp_core.NLPCore.JSON_NAME_TABLE_NO: self.no_tables,
                nlp_core.NLPCore.JSON_NAME_ROWS: self._rows,
            }
        )

        self._reset_table()

        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_table,
            f"LineTypeTable: End   table                   on page={self._page_idx+1}",
        )

    # ------------------------------------------------------------------
    # Process the line-related data.
    # ------------------------------------------------------------------
    def _process_line(self, line_json: nlp_core.LineJSON) -> str:  # noqa: C901
        """Process the line-related data.

        Args:
            line_json (nlp_core.LineJSON): The line to be processed.

        Returns:
            str: The new or the old line type.
        """
        if nlp_core.NLPCore.JSON_NAME_ROW_NO not in line_json:
            return nlp_core.NLPCore.LINE_TYPE_BODY

        self._column_no = int(line_json[nlp_core.NLPCore.JSON_NAME_COLUMN_NO])
        self._row_no = int(line_json[nlp_core.NLPCore.JSON_NAME_ROW_NO])

        if not self._is_table_open:
            self._reset_table()
        elif self._row_no < self._row_no_prev:
            self._finish_table()
        elif self._row_no != self._row_no_prev:
            self._finish_row()

        text = line_json[nlp_core.NLPCore.JSON_NAME_TEXT]

        if text == "" and not core_glob.setup.is_lt_table_file_incl_empty_columns:
            return nlp_core.NLPCore.LINE_TYPE_TABLE

        coord_llx = float(line_json[nlp_core.NLPCore.JSON_NAME_COORD_LLX])
        coord_urx = float(line_json[nlp_core.NLPCore.JSON_NAME_COORD_URX])

        if self._page_no_from == 0:
            self._page_no_from = self._page_idx + 1

        if self._row_no == 1:
            if self._column_no_prev == 0:
                self._first_row_llx = coord_llx
            self._first_row_urx = coord_urx

        if self._column_no_prev == 0:
            self._first_column_llx = coord_llx
        self._last_column_urx = coord_urx

        new_entry = {
            nlp_core.NLPCore.JSON_NAME_COLUMN_NO: line_json[nlp_core.NLPCore.JSON_NAME_COLUMN_NO],
            nlp_core.NLPCore.JSON_NAME_COORD_LLX: coord_llx,
            nlp_core.NLPCore.JSON_NAME_COORD_URX: coord_urx,
            nlp_core.NLPCore.JSON_NAME_LINE_NO: line_json[nlp_core.NLPCore.JSON_NAME_LINE_NO],
            nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE: line_json[nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE],
            nlp_core.NLPCore.JSON_NAME_PARA_NO: line_json[nlp_core.NLPCore.JSON_NAME_PARA_NO],
            nlp_core.NLPCore.JSON_NAME_TEXT: text,
        }

        if nlp_core.NLPCore.JSON_NAME_COLUMN_SPAN in line_json:
            new_entry[nlp_core.NLPCore.JSON_NAME_COLUMN_SPAN] = line_json[nlp_core.NLPCore.JSON_NAME_COLUMN_SPAN]

        self._columns.append(new_entry)

        self._is_table_open = True
        self._column_no_prev = self._column_no
        self._row_no_prev = self._row_no

        return nlp_core.NLPCore.LINE_TYPE_TABLE

    # ------------------------------------------------------------------
    # Process the page-related data.
    # ------------------------------------------------------------------
    def _process_page(self) -> None:
        """Process the page-related data."""
        for line_idx, line_json in enumerate(self._lines_json):
            if line_json[nlp_core.NLPCore.JSON_NAME_LINE_TYPE] != nlp_core.NLPCore.LINE_TYPE_BODY:
                continue

            if self._process_line(line_json) == nlp_core.NLPCore.LINE_TYPE_TABLE:
                line_json[nlp_core.NLPCore.JSON_NAME_LINE_TYPE] = nlp_core.NLPCore.LINE_TYPE_TABLE
                self._lines_json[line_idx] = line_json
            else:
                self._finish_table()

    # ------------------------------------------------------------------
    # Reset the document memory.
    # ------------------------------------------------------------------
    def _reset_document(self) -> None:
        """Reset the document memory."""
        self.no_tables = 0

        self._tables = []

        self.table_no = 0

        core_utils.progress_msg(core_glob.setup.is_verbose_lt_table, "LineTypeTable: Reset the document memory")

        self._reset_table()

    # ------------------------------------------------------------------
    # Reset the row memory.
    # ------------------------------------------------------------------
    def _reset_row(self) -> None:
        """Reset the row memory."""
        self._column_no_prev = 0
        self._columns = []

        self._first_column_llx = 0.0
        self._last_column_urx = 0.0

        core_utils.progress_msg(core_glob.setup.is_verbose_lt_table, "LineTypeTable: Reset the row memory")

    # ------------------------------------------------------------------
    # Reset the table memory.
    # ------------------------------------------------------------------
    def _reset_table(self) -> None:
        """Reset the table memory."""
        self._first_row_llx = 0.0
        self._first_row_urx = 0.0

        self._is_table_open = False

        self._no_columns_table = 0

        self._page_no_from = 0
        self._page_no_till = 0

        self._row_no_prev = 0
        self._rows = []

        self.table_no = 0

        core_utils.progress_msg(core_glob.setup.is_verbose_lt_table, "LineTypeTable: Reset the table memory")

        self._reset_row()

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
        directory_name: str,
        document_id: int,
        file_name_curr: str,
        file_name_orig: str,
    ) -> None:
        """Process the document related data.

        Args:
            directory_name (str): Directory name of the output file.
            document_id (int): Identification of the document.
            file_name_curr (str): File name of the file to be processed.
            file_name_orig (in): File name of the original document file.
        """
        core_glob.logger.debug(core_glob.LOGGER_START)
        core_glob.logger.debug("param directory_name =%s", directory_name)
        core_glob.logger.debug("param document_id    =%i", document_id)
        core_glob.logger.debug("param file_name_curr =%s", file_name_curr)
        core_glob.logger.debug("param file_name_orig =%s", file_name_orig)

        core_utils.check_exists_object(
            is_line_type_header_footer=True,
            is_line_type_toc=True,
            is_nlp_core=True,
            is_setup=True,
            is_text_parser=True,
        )

        self._file_name_curr = file_name_curr

        core_utils.progress_msg(core_glob.setup.is_verbose_lt_table, "LineTypeTable")
        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_table,
            f"LineTypeTable: Start document                       ={self._file_name_curr}",
        )

        self._reset_document()

        for page_idx, page_json in enumerate(core_glob.nlp_core.document_json[nlp_core.NLPCore.JSON_NAME_PAGES]):
            self._page_idx = page_idx
            self._max_line_no = page_json[nlp_core.NLPCore.JSON_NAME_LINE_NO]
            self._lines_json = page_json[nlp_core.NLPCore.JSON_NAME_LINES]
            self._process_page()

        if core_glob.setup.is_create_extra_file_table and self._tables:
            full_name = core_utils.get_full_name_from_components(
                directory_name,
                core_utils.get_stem_name(str(file_name_curr)) + ".table." + core_glob.FILE_TYPE_JSON,
            )
            with open(full_name, "w", encoding=core_glob.FILE_ENCODING_DEFAULT) as file_handle:
                json.dump(
                    {
                        nlp_core.NLPCore.JSON_NAME_DOC_ID: document_id,
                        nlp_core.NLPCore.JSON_NAME_DOC_FILE_NAME: file_name_orig,
                        nlp_core.NLPCore.JSON_NAME_NO_TABLES_IN_DOC: self.no_tables,
                        nlp_core.NLPCore.JSON_NAME_TABLES: self._tables,
                    },
                    file_handle,
                    indent=core_glob.setup.json_indent,
                    sort_keys=core_glob.setup.is_json_sort_keys,
                )

        if self.no_tables > 0:
            core_utils.progress_msg(
                core_glob.setup.is_verbose_lt_table,
                f"LineTypeTable:                         number tables={self.no_tables}",
            )

        core_utils.progress_msg(
            core_glob.setup.is_verbose_lt_table,
            f"LineTypeTable: End   document                       ={self._file_name_curr}",
        )

        core_glob.logger.debug(core_glob.LOGGER_END)
