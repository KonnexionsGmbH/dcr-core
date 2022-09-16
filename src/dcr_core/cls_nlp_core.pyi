# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module stub file."""
import collections
from typing import ClassVar

class NLPCore:
    FontJSON = dict[str, bool | float | int | str]
    WordJSON = dict[str, bool | float | int | str]
    LineJSON = dict[str, float | int | list[WordJSON] | str]
    ParaJSON = dict[str, int | list[LineJSON] | str]
    PageJSON = dict[str, int | list[ParaJSON]]
    ConfigJSON = dict[str, bool | str]
    DocumentJSON = dict[str, bool | int | list[PageJSON] | str]
    ParamsJSON = dict[str, bool | int | str]

    ENVIRONMENT_TYPE_DEV: ClassVar[str]
    ENVIRONMENT_TYPE_PROD: ClassVar[str]
    ENVIRONMENT_TYPE_TEST: ClassVar[str]

    JSON_NAME_CONFIG: ClassVar[str]
    JSON_NAME_CONTAINER_FONTS: ClassVar[str]
    JSON_NAME_CONTAINER_LINES: ClassVar[str]
    JSON_NAME_CONTAINER_PAGES: ClassVar[str]
    JSON_NAME_CONTAINER_PARAS: ClassVar[str]
    JSON_NAME_CONTAINER_WORDS: ClassVar[str]
    JSON_NAME_CREATED_AT: ClassVar[str]
    JSON_NAME_CREATED_BY: ClassVar[str]

    JSON_NAME_DIRECTORY_NAME: ClassVar[str]
    JSON_NAME_DOCUMENT_ID: ClassVar[str]

    JSON_NAME_EMBEDDED: ClassVar[str]
    JSON_NAME_ENVIRONMENT_VARIANT: ClassVar[str]

    JSON_NAME_FILE_NAME_CURR: ClassVar[str]
    JSON_NAME_FILE_NAME_NEXT: ClassVar[str]
    JSON_NAME_FILE_NAME_ORIG: ClassVar[str]
    JSON_NAME_FONT: ClassVar[str]
    JSON_NAME_FONT_NO: ClassVar[str]
    JSON_NAME_FULL_NAME: ClassVar[str]

    JSON_NAME_ID: ClassVar[str]
    JSON_NAME_ITALIC_ANGLE: ClassVar[str]

    JSON_NAME_JSON_INDENT: ClassVar[str]
    JSON_NAME_JSON_SORT_KEYS: ClassVar[str]

    JSON_NAME_LINE_NO: ClassVar[str]
    JSON_NAME_LINE_NO_FIRST: ClassVar[str]
    JSON_NAME_LINE_NO_LAST: ClassVar[str]
    JSON_NAME_LINE_NO_PAGE: ClassVar[str]
    JSON_NAME_LINE_NO_PARA: ClassVar[str]
    JSON_NAME_LINE_TYPE_FOOTER_REQUIRED: ClassVar[str]
    JSON_NAME_LINE_TYPE_HEADER_REQUIRED: ClassVar[str]
    JSON_NAME_LINE_TYPE_HEADING_REQUIRED: ClassVar[str]
    JSON_NAME_LINE_TYPE_LIST_BULLET_REQUIRED: ClassVar[str]
    JSON_NAME_LINE_TYPE_LIST_NUMBER_REQUIRED: ClassVar[str]
    JSON_NAME_LINE_TYPE_TABLE_REQUIRED: ClassVar[str]
    JSON_NAME_LINE_TYPE_TOC_REQUIRED: ClassVar[str]
    JSON_NAME_LLX: ClassVar[str]
    JSON_NAME_LT_FOOTER_MAX_DISTANCE: ClassVar[str]
    JSON_NAME_LT_FOOTER_MAX_LINES: ClassVar[str]
    JSON_NAME_LT_HEADER_MAX_DISTANCE: ClassVar[str]
    JSON_NAME_LT_HEADER_MAX_LINES: ClassVar[str]
    JSON_NAME_LT_HEADING_FILE_INCL_NO_CTX: ClassVar[str]
    JSON_NAME_LT_HEADING_FILE_INCL_REGEXP: ClassVar[str]
    JSON_NAME_LT_HEADING_MAX_LEVEL: ClassVar[str]
    JSON_NAME_LT_HEADING_MIN_PAGES: ClassVar[str]
    JSON_NAME_LT_HEADING_RULE_FILE: ClassVar[str]
    JSON_NAME_LT_HEADING_TOLERANCE_LLX: ClassVar[str]
    JSON_NAME_LT_LIST_BULLET_MIN_ENTRIES: ClassVar[str]
    JSON_NAME_LT_LIST_BULLET_RULE_FILE: ClassVar[str]
    JSON_NAME_LT_LIST_BULLET_TOLERANCE_LLX: ClassVar[str]
    JSON_NAME_LT_LIST_NUMBER_MIN_ENTRIES: ClassVar[str]
    JSON_NAME_LT_LIST_NUMBER_RULE_FILE: ClassVar[str]
    JSON_NAME_LT_LIST_NUMBER_TOLERANCE_LLX: ClassVar[str]
    JSON_NAME_LT_TABLE_FILE_INCL_EMPTY_COLUMNS: ClassVar[str]
    JSON_NAME_LT_TOC_LAST_PAGE: ClassVar[str]
    JSON_NAME_LT_TOC_MIN_ENTRIES: ClassVar[str]

    JSON_NAME_NAME: ClassVar[str]
    JSON_NAME_NO_FONTS: ClassVar[str]
    JSON_NAME_NO_LINES: ClassVar[str]
    JSON_NAME_NO_LINES_FOOTER: ClassVar[str]
    JSON_NAME_NO_LINES_HEADER: ClassVar[str]
    JSON_NAME_NO_LINES_TOC: ClassVar[str]
    JSON_NAME_NO_LISTS_BULLET: ClassVar[str]
    JSON_NAME_NO_LISTS_NUMBER: ClassVar[str]
    JSON_NAME_NO_PAGES: ClassVar[str]
    JSON_NAME_NO_PARAS: ClassVar[str]
    JSON_NAME_NO_PDF_PAGES: ClassVar[str]
    JSON_NAME_NO_TABLES: ClassVar[str]
    JSON_NAME_NO_WORDS: ClassVar[str]

    JSON_NAME_PAGE_NO: ClassVar[str]
    JSON_NAME_PARAMS: ClassVar[str]
    JSON_NAME_PARA_NO: ClassVar[str]
    JSON_NAME_PARA_NO_FIRST: ClassVar[str]
    JSON_NAME_PARA_NO_LAST: ClassVar[str]
    JSON_NAME_PARA_NO_PAGE: ClassVar[str]

    JSON_NAME_SIZE: ClassVar[str]

    JSON_NAME_SPACY_IGNORE_BRACKET: ClassVar[str]
    JSON_NAME_SPACY_IGNORE_LEFT_PUNCT: ClassVar[str]
    JSON_NAME_SPACY_IGNORE_LINE_TYPE_FOOTER: ClassVar[str]
    JSON_NAME_SPACY_IGNORE_LINE_TYPE_HEADER: ClassVar[str]
    JSON_NAME_SPACY_IGNORE_LINE_TYPE_HEADING: ClassVar[str]
    JSON_NAME_SPACY_IGNORE_LINE_TYPE_LIST_BULLET: ClassVar[str]
    JSON_NAME_SPACY_IGNORE_LINE_TYPE_LIST_NUMBER: ClassVar[str]
    JSON_NAME_SPACY_IGNORE_LINE_TYPE_TABLE: ClassVar[str]
    JSON_NAME_SPACY_IGNORE_LINE_TYPE_TOC: ClassVar[str]
    JSON_NAME_SPACY_IGNORE_PUNCT: ClassVar[str]
    JSON_NAME_SPACY_IGNORE_QUOTE: ClassVar[str]
    JSON_NAME_SPACY_IGNORE_RIGHT_PUNCT: ClassVar[str]
    JSON_NAME_SPACY_IGNORE_SPACE: ClassVar[str]
    JSON_NAME_SPACY_IGNORE_STOP: ClassVar[str]

    JSON_NAME_SPACY_TKN_CLUSTER: ClassVar[str]
    JSON_NAME_SPACY_TKN_DEP_: ClassVar[str]
    JSON_NAME_SPACY_TKN_DOC: ClassVar[str]
    JSON_NAME_SPACY_TKN_ENT_KB_ID_: ClassVar[str]
    JSON_NAME_SPACY_TKN_ENT_IOB_: ClassVar[str]
    JSON_NAME_SPACY_TKN_ENT_TYPE_: ClassVar[str]
    JSON_NAME_SPACY_TKN_HEAD: ClassVar[str]
    JSON_NAME_SPACY_TKN_I: ClassVar[str]
    JSON_NAME_SPACY_TKN_IDX: ClassVar[str]
    JSON_NAME_SPACY_TKN_IS_ALPHA: ClassVar[str]
    JSON_NAME_SPACY_TKN_IS_ASCII: ClassVar[str]
    JSON_NAME_SPACY_TKN_IS_BRACKET: ClassVar[str]
    JSON_NAME_SPACY_TKN_IS_CURRENCY: ClassVar[str]
    JSON_NAME_SPACY_TKN_IS_DIGIT: ClassVar[str]
    JSON_NAME_SPACY_TKN_IS_LEFT_PUNCT: ClassVar[str]
    JSON_NAME_SPACY_TKN_IS_LOWER: ClassVar[str]
    JSON_NAME_SPACY_TKN_IS_OOV: ClassVar[str]
    JSON_NAME_SPACY_TKN_IS_PUNCT: ClassVar[str]
    JSON_NAME_SPACY_TKN_IS_QUOTE: ClassVar[str]
    JSON_NAME_SPACY_TKN_IS_RIGHT_PUNCT: ClassVar[str]
    JSON_NAME_SPACY_TKN_IS_SENT_END: ClassVar[str]
    JSON_NAME_SPACY_TKN_IS_SENT_START: ClassVar[str]
    JSON_NAME_SPACY_TKN_IS_SPACE: ClassVar[str]
    JSON_NAME_SPACY_TKN_IS_STOP: ClassVar[str]
    JSON_NAME_SPACY_TKN_IS_TITLE: ClassVar[str]
    JSON_NAME_SPACY_TKN_IS_UPPER: ClassVar[str]
    JSON_NAME_SPACY_TKN_LANG_: ClassVar[str]
    JSON_NAME_SPACY_TKN_LEFT_EDGE: ClassVar[str]
    JSON_NAME_SPACY_TKN_LEMMA_: ClassVar[str]
    JSON_NAME_SPACY_TKN_LEX: ClassVar[str]
    JSON_NAME_SPACY_TKN_LEX_ID: ClassVar[str]
    JSON_NAME_SPACY_TKN_LIKE_EMAIL: ClassVar[str]
    JSON_NAME_SPACY_TKN_LIKE_NUM: ClassVar[str]
    JSON_NAME_SPACY_TKN_LIKE_URL: ClassVar[str]
    JSON_NAME_SPACY_TKN_LOWER_: ClassVar[str]
    JSON_NAME_SPACY_TKN_MORPH: ClassVar[str]
    JSON_NAME_SPACY_TKN_NORM_: ClassVar[str]
    JSON_NAME_SPACY_TKN_ORTH_: ClassVar[str]
    JSON_NAME_SPACY_TKN_POS_: ClassVar[str]
    JSON_NAME_SPACY_TKN_PREFIX_: ClassVar[str]
    JSON_NAME_SPACY_TKN_PROB: ClassVar[str]
    JSON_NAME_SPACY_TKN_RANK: ClassVar[str]
    JSON_NAME_SPACY_TKN_RIGHT_EDGE: ClassVar[str]
    JSON_NAME_SPACY_TKN_SENT: ClassVar[str]
    JSON_NAME_SPACY_TKN_SENTIMENT: ClassVar[str]
    JSON_NAME_SPACY_TKN_SHAPE_: ClassVar[str]
    JSON_NAME_SPACY_TKN_SUFFIX_: ClassVar[str]
    JSON_NAME_SPACY_TKN_TAG_: ClassVar[str]
    JSON_NAME_SPACY_TKN_TENSOR: ClassVar[str]
    JSON_NAME_SPACY_TKN_TEXT: ClassVar[str]
    JSON_NAME_SPACY_TKN_TEXT_WITH_WS: ClassVar[str]
    JSON_NAME_SPACY_TKN_VOCAB: ClassVar[str]
    JSON_NAME_SPACY_TKN_WHITESPACE_: ClassVar[str]

    JSON_NAME_TEXT: ClassVar[str]
    JSON_NAME_TYPE: ClassVar[str]

    JSON_NAME_URX: ClassVar[str]

    JSON_NAME_WEIGHT: ClassVar[str]
    JSON_NAME_WORD_NO: ClassVar[str]
    JSON_NAME_WORD_NO_FIRST: ClassVar[str]
    JSON_NAME_WORD_NO_LAST: ClassVar[str]
    JSON_NAME_WORD_NO_LINE: ClassVar[str]
    JSON_NAME_WORD_NO_PAGE: ClassVar[str]
    JSON_NAME_WORD_NO_PARA: ClassVar[str]

    # wwe =================================== wwe #

    JSON_NAME_COLUMN: ClassVar[str]
    JSON_NAME_COLUMN_NO: ClassVar[str]
    JSON_NAME_CONTAINER_COLUMNS: ClassVar[str]
    JSON_NAME_CONTAINER_ENTRIES: ClassVar[str]
    JSON_NAME_CONTAINER_LISTS: ClassVar[str]
    JSON_NAME_CONTAINER_ROWS: ClassVar[str]
    JSON_NAME_CONTAINER_SENTENCES: ClassVar[str]
    JSON_NAME_CONTAINER_TABLES: ClassVar[str]
    JSON_NAME_CONTAINER_TITLES: ClassVar[str]
    JSON_NAME_CTX_LINE_1: ClassVar[str]
    JSON_NAME_CTX_LINE_2: ClassVar[str]
    JSON_NAME_CTX_LINE_3: ClassVar[str]
    JSON_NAME_DOCUMENT: ClassVar[str]
    JSON_NAME_ENTRY: ClassVar[str]
    JSON_NAME_ENTRY_NO: ClassVar[str]
    JSON_NAME_FORMAT: ClassVar[str]
    JSON_NAME_LEVEL: ClassVar[str]
    JSON_NAME_LINE: ClassVar[str]
    JSON_NAME_LINE_NO_PAGEFIRST: ClassVar[str]
    JSON_NAME_LINE_NO_PAGELAST: ClassVar[str]
    JSON_NAME_LIST: ClassVar[str]
    JSON_NAME_LIST_NO: ClassVar[str]
    JSON_NAME_LISTS_BULLET: ClassVar[str]
    JSON_NAME_LISTS_NUMBER: ClassVar[str]
    JSON_NAME_LLX_FIRST_COLUMN: ClassVar[str]
    JSON_NAME_LLX_FIRST_ROW: ClassVar[str]
    JSON_NAME_NO_COLUMNS: ClassVar[str]
    JSON_NAME_NO_ENTRIES: ClassVar[str]
    JSON_NAME_NO_ROWS: ClassVar[str]
    JSON_NAME_NO_SENTENCES: ClassVar[str]
    JSON_NAME_NO_TITLES: ClassVar[str]
    JSON_NAME_PAGE: ClassVar[str]
    JSON_NAME_PAGE_NO_FIRST: ClassVar[str]
    JSON_NAME_PAGE_NO_LAST: ClassVar[str]
    JSON_NAME_PARA: ClassVar[str]
    JSON_NAME_REGEXP: ClassVar[str]
    JSON_NAME_ROW: ClassVar[str]
    JSON_NAME_ROW_NO: ClassVar[str]
    JSON_NAME_SENTENCES: ClassVar[str]
    JSON_NAME_TABLE: ClassVar[str]
    JSON_NAME_TABLE_NO: ClassVar[str]
    JSON_NAME_TABLES: ClassVar[str]
    # wwe
    # JSON_NAME_TOKEN_CLUSTER: ClassVar[str]
    # JSON_NAME_TOKEN_DEP_: ClassVar[str]
    # JSON_NAME_TOKEN_DOC: ClassVar[str]
    # JSON_NAME_TOKEN_ENT_IOB_: ClassVar[str]
    # JSON_NAME_TOKEN_HEAD: ClassVar[str]
    # JSON_NAME_TOKEN_I: ClassVar[str]
    # JSON_NAME_TOKEN__IDX: ClassVar[str]
    # JSON_NAME_TOKEN_IS_ALPHA: ClassVar[str]
    # JSON_NAME_TOKEN_IS_ASCII: ClassVar[str]
    # JSON_NAME_TOKEN_IS_OOV: ClassVar[str]
    # JSON_NAME_TOKEN_IS_SENT_START: ClassVar[str]
    # JSON_NAME_TOKEN_IS_TITLE: ClassVar[str]
    # JSON_NAME_TOKEN_LANG_: ClassVar[str]
    # JSON_NAME_TOKEN_LEFT_EDGE: ClassVar[str]
    # JSON_NAME_TOKEN_LEMMA_: ClassVar[str]
    # JSON_NAME_TOKEN_LEX: ClassVar[str]
    # JSON_NAME_TOKEN_LEX_ID: ClassVar[str]
    # JSON_NAME_TOKEN_LOWER_: ClassVar[str]
    # JSON_NAME_TOKEN_MORPH: ClassVar[str]
    # JSON_NAME_TOKEN__NORM_: ClassVar[str]
    # JSON_NAME_TOKEN_ORTH_: ClassVar[str]
    # JSON_NAME_TOKEN_POS_: ClassVar[str]
    # JSON_NAME_TOKEN_PREFIX_: ClassVar[str]
    # JSON_NAME_TOKEN_PROB: ClassVar[str]
    # JSON_NAME_TOKEN_RANK: ClassVar[str]
    # JSON_NAME_TOKEN_RIGHTEDGE: ClassVar[str]
    # JSON_NAME_TOKEN_SENT: ClassVar[str]
    # JSON_NAME_TOKEN_SENTIMENT: ClassVar[str]
    # JSON_NAME_TOKEN_SHAPE_: ClassVar[str]
    # JSON_NAME_TOKEN_SUFFIX_: ClassVar[str]
    # JSON_NAME_TOKEN_TAG_: ClassVar[str]
    # JSON_NAME_TOKEN_TEXT: ClassVar[str]
    # JSON_NAME_TOKEN_TEXTWITHWS: ClassVar[str]
    # JSON_NAME_TOKEN_VOCAB: ClassVar[str]
    # JSON_NAME_TOKEN_WHITESPACE_: ClassVar[str]
    JSON_NAME_TOC: ClassVar[str]
    JSON_NAME_URX_FIRST_COLUMN: ClassVar[str]
    JSON_NAME_URX_FIRST_ROW: ClassVar[str]
    JSON_NAME_WORD: ClassVar[str]
    LANGUAGE_PANDOC_DEFAULT: ClassVar[str]
    LANGUAGE_SPACY_DEFAULT: ClassVar[str]
    LANGUAGE_TESSERACT_DEFAULT: ClassVar[str]
    LINE_TYPE_BODY: ClassVar[str]
    LINE_TYPE_FOOTER: ClassVar[str]
    LINE_TYPE_HEADER: ClassVar[str]
    LINE_TYPE_HEADING: ClassVar[str]
    LINE_TYPE_LIST_BULLET: ClassVar[str]
    LINE_TYPE_LIST_NUMBER: ClassVar[str]
    LINE_TYPE_TABLE: ClassVar[str]
    LINE_TYPE_TOC: ClassVar[str]
    LOGGER_PROGRESS_UPDATE: ClassVar[str]

    PARSE_NAME_SPACE: ClassVar[str]
    PARSE_ELEM_A: ClassVar[str]
    PARSE_ELEM_ACTION: ClassVar[str]
    PARSE_ELEM_ANNOTATIONS: ClassVar[str]
    PARSE_ELEM_ATTACHMENTS: ClassVar[str]
    PARSE_ELEM_AUTHOR: ClassVar[str]
    PARSE_ELEM_BOOKMARK: ClassVar[str]
    PARSE_ELEM_BOOKMARKS: ClassVar[str]
    PARSE_ELEM_BOX: ClassVar[str]
    PARSE_ELEM_CELL: ClassVar[str]
    PARSE_ELEM_COLOR_SPACES: ClassVar[str]
    PARSE_ELEM_CONTENT: ClassVar[str]
    PARSE_ELEM_CREATION: ClassVar[str]
    PARSE_ELEM_CREATION_DATE: ClassVar[str]
    PARSE_ELEM_CREATOR: ClassVar[str]
    PARSE_ELEM_CUSTOM: ClassVar[str]
    PARSE_ELEM_CUSTOM_BINARY: ClassVar[str]
    PARSE_ELEM_DESTINATIONS: ClassVar[str]
    PARSE_ELEM_DOC_INFO: ClassVar[str]
    PARSE_ELEM_DOCUMENT: ClassVar[str]
    PARSE_ELEM_ENCRYPTION: ClassVar[str]
    PARSE_ELEM_EXCEPTION: ClassVar[str]
    PARSE_ELEM_FIELDS: ClassVar[str]
    PARSE_ELEM_FONT: ClassVar[str]
    PARSE_ELEM_FONTS: ClassVar[str]
    PARSE_ELEM_FROM: ClassVar[int] = len(PARSE_NAME_SPACE)
    PARSE_ELEM_GLYPH: ClassVar[str]
    PARSE_ELEM_GRAPHICS: ClassVar[str]
    PARSE_ELEM_GTS_PDFX_CONFORMANCE: ClassVar[str]
    PARSE_ELEM_GTS_PDFX_VERSION: ClassVar[str]
    PARSE_ELEM_GTS_PPMLVDX_CONFORMANCE: ClassVar[str]
    PARSE_ELEM_GTS_PPMLVDX_VERSION: ClassVar[str]
    PARSE_ELEM_ISO_PDFE_VERSION: ClassVar[str]
    PARSE_ELEM_JAVA_SCRIPTS: ClassVar[str]
    PARSE_ELEM_KEYWORDS: ClassVar[str]
    PARSE_ELEM_LINE: ClassVar[str]
    PARSE_ELEM_METADATA: ClassVar[str]
    PARSE_ELEM_MOD_DATE: ClassVar[str]
    PARSE_ELEM_OPTIONS: ClassVar[str]
    PARSE_ELEM_OUTPUT_INTENTS: ClassVar[str]
    PARSE_ELEM_PAGE: ClassVar[str]
    PARSE_ELEM_PAGES: ClassVar[str]
    PARSE_ELEM_PARA: ClassVar[str]
    PARSE_ELEM_PLACED_IMAGE: ClassVar[str]
    PARSE_ELEM_PRODUCER: ClassVar[str]
    PARSE_ELEM_RESOURCES: ClassVar[str]
    PARSE_ELEM_ROW: ClassVar[str]
    PARSE_ELEM_SIGNATURE_FIELDS: ClassVar[str]
    PARSE_ELEM_SUBJECT: ClassVar[str]
    PARSE_ELEM_TABLE: ClassVar[str]
    PARSE_ELEM_TEXT: ClassVar[str]
    PARSE_ELEM_TITLE: ClassVar[str]
    PARSE_ELEM_TRAPPED: ClassVar[str]
    PARSE_ELEM_WORD: ClassVar[str]
    PARSE_ELEM_XFA: ClassVar[str]
    SEARCH_STRATEGY_LINES: ClassVar[str]
    SEARCH_STRATEGY_TABLE: ClassVar[str]
    TET_DOCUMENT_OPT_LIST: ClassVar[str]
    TET_PAGE_OPT_LIST: ClassVar[str]

    def __init__(self) -> None:
        self.document_json: dict[str, bool | int | list[NLPCore.PageJSON] | str] = {}
        self._exist = None
    @classmethod
    def _convert_roman_2_int(cls, roman: str) -> int: ...
    @staticmethod
    def _get_lt_anti_patterns_default_heading() -> list[tuple[str, str]]: ...
    @staticmethod
    def _get_lt_anti_patterns_default_list_bullet(environment_variant: str) -> list[tuple[str, str]]: ...
    @staticmethod
    def _get_lt_anti_patterns_default_list_number(environment_variant: str) -> list[tuple[str, str]]: ...
    @staticmethod
    def _get_lt_rules_default_heading_list_number() -> list[
        tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str]]
    ]: ...
    @staticmethod
    def _get_lt_rules_default_list_bullet() -> dict[str, int]: ...
    def exists(self) -> bool: ...
    @staticmethod
    def export_rule_file_heading(
        is_verbose: bool, file_name: str, file_encoding: str, json_indent: str, is_json_sort_keys: bool
    ) -> None: ...
    @staticmethod
    def export_rule_file_list_bullet(
        is_verbose: bool,
        file_name: str,
        file_encoding: str,
        json_indent: str,
        is_json_sort_keys: bool,
        environment_variant: str,
    ) -> None: ...
    @staticmethod
    def export_rule_file_list_number(
        is_verbose: bool,
        file_name: str,
        file_encoding: str,
        json_indent: str,
        is_json_sort_keys: bool,
        environment_variant: str,
    ) -> None: ...
    @staticmethod
    def get_lt_anti_patterns_default_heading() -> list[
        tuple[
            str,
            str,
        ]
    ]: ...
    @staticmethod
    def get_lt_anti_patterns_default_list_bullet(
        environment_variant: str,
    ) -> list[tuple[str, str]]: ...
    @staticmethod
    def get_lt_anti_patterns_default_list_number(environment_variant: str) -> list[tuple[str, str]]: ...
    @staticmethod
    def get_lt_rules_default_heading() -> list[tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str]]]: ...
    @staticmethod
    def get_lt_rules_default_list_bullet() -> dict[str, int]: ...
    @staticmethod
    def get_lt_rules_default_list_number() -> list[tuple[str, str, collections.abc.Callable[[str, str], bool], list[str]]]: ...
    @classmethod
    def is_asc_ignore(cls, _predecessor: str, _successor: str) -> bool: ...
    @classmethod
    def is_asc_lowercase_letters(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_lowercase_letters_token(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_romans(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_romans_token(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_strings(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_string_floats(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_string_floats_token(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_string_integers(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_string_integers_token(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_uppercase_letters(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_uppercase_letters_token(cls, predecessor: str, successor: str) -> bool: ...
