# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module stub file."""
import configparser
from typing import ClassVar

class Setup:
    _CONFIG_PARAM_NO: ClassVar[int]
    _DCR_CFG_DELETE_AUXILIARY_FILES: ClassVar[str]
    _DCR_CFG_DIRECTORY_INBOX: ClassVar[str]
    _DCR_CFG_FILE: ClassVar[str]
    _DCR_CFG_JSON_INCL_CONFIG: ClassVar[str]
    _DCR_CFG_JSON_INCL_FONTS: ClassVar[str]
    _DCR_CFG_JSON_INCL_HEADING: ClassVar[str]
    _DCR_CFG_JSON_INCL_LIST_BULLET: ClassVar[str]
    _DCR_CFG_JSON_INCL_LIST_NUMBER: ClassVar[str]
    _DCR_CFG_JSON_INCL_PARAMS: ClassVar[str]
    _DCR_CFG_JSON_INDENT: ClassVar[str]
    _DCR_CFG_JSON_SORT_KEYS: ClassVar[str]
    _DCR_CFG_LT_FOOTER_MAX_DISTANCE: ClassVar[str]
    _DCR_CFG_LT_FOOTER_MAX_LINES: ClassVar[str]
    _DCR_CFG_LT_FOOTER_REQUIRED: ClassVar[str]
    _DCR_CFG_LT_HEADER_MAX_DISTANCE: ClassVar[str]
    _DCR_CFG_LT_HEADER_MAX_LINES: ClassVar[str]
    _DCR_CFG_LT_HEADER_REQUIRED: ClassVar[str]
    _DCR_CFG_LT_HEADING_FILE_INCL_NO_CTX: ClassVar[str]
    _DCR_CFG_LT_HEADING_FILE_INCL_REGEXP: ClassVar[str]
    _DCR_CFG_LT_HEADING_MAX_LEVEL: ClassVar[str]
    _DCR_CFG_LT_HEADING_MIN_PAGES: ClassVar[str]
    _DCR_CFG_LT_HEADING_REQUIRED: ClassVar[str]
    _DCR_CFG_LT_HEADING_RULE_FILE: ClassVar[str]
    _DCR_CFG_LT_HEADING_TOLERANCE_LLX: ClassVar[str]
    _DCR_CFG_LT_LIST_BULLET_MIN_ENTRIES: ClassVar[str]
    _DCR_CFG_LT_LIST_BULLET_REQUIRED: ClassVar[str]
    _DCR_CFG_LT_LIST_BULLET_RULE_FILE: ClassVar[str]
    _DCR_CFG_LT_LIST_BULLET_TOLERANCE_LLX: ClassVar[str]
    _DCR_CFG_LT_LIST_NUMBER_FILE_INCL_REGEXP: ClassVar[str]
    _DCR_CFG_LT_LIST_NUMBER_MIN_ENTRIES: ClassVar[str]
    _DCR_CFG_LT_LIST_NUMBER_REQUIRED: ClassVar[str]
    _DCR_CFG_LT_LIST_NUMBER_RULE_FILE: ClassVar[str]
    _DCR_CFG_LT_LIST_NUMBER_TOLERANCE_LLX: ClassVar[str]
    _DCR_CFG_LT_TOC_LAST_PAGE: ClassVar[str]
    _DCR_CFG_LT_TOC_MIN_ENTRIES: ClassVar[str]
    _DCR_CFG_LT_TOC_REQUIRED: ClassVar[str]
    _DCR_CFG_PDF2IMAGE_TYPE: ClassVar[str]
    _DCR_CFG_SECTION_CORE: ClassVar[str]
    _DCR_CFG_SECTION_CORE_ENV_TEST: ClassVar[str]
    _DCR_CFG_SECTION_CORE_SPACY: ClassVar[str]
    _DCR_CFG_SPACY_IGNORE_BRACKET: ClassVar[str]
    _DCR_CFG_SPACY_IGNORE_LEFT_PUNCT: ClassVar[str]
    _DCR_CFG_SPACY_IGNORE_LINE_TYPE_FOOTER: ClassVar[str]
    _DCR_CFG_SPACY_IGNORE_LINE_TYPE_HEADER: ClassVar[str]
    _DCR_CFG_SPACY_IGNORE_LINE_TYPE_HEADING: ClassVar[str]
    _DCR_CFG_SPACY_IGNORE_LINE_TYPE_LIST_BULLET: ClassVar[str]
    _DCR_CFG_SPACY_IGNORE_LINE_TYPE_LIST_NUMBER: ClassVar[str]
    _DCR_CFG_SPACY_IGNORE_LINE_TYPE_TABLE: ClassVar[str]
    _DCR_CFG_SPACY_IGNORE_LINE_TYPE_TOC: ClassVar[str]
    _DCR_CFG_SPACY_IGNORE_PUNCT: ClassVar[str]
    _DCR_CFG_SPACY_IGNORE_QUOTE: ClassVar[str]
    _DCR_CFG_SPACY_IGNORE_RIGHT_PUNCT: ClassVar[str]
    _DCR_CFG_SPACY_IGNORE_SPACE: ClassVar[str]
    _DCR_CFG_SPACY_IGNORE_STOP: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_CLUSTER: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_DEP_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_DOC: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_ENT_IOB_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_ENT_KB_ID_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_ENT_TYPE_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_HEAD: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_I: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IDX: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_ALPHA: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_ASCII: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_BRACKET: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_CURRENCY: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_DIGIT: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_LEFT_PUNCT: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_LOWER: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_OOV: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_PUNCT: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_QUOTE: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_RIGHT_PUNCT: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_SENT_END: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_SENT_START: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_SPACE: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_STOP: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_TITLE: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_UPPER: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_LANG_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_LEFT_EDGE: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_LEMMA_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_LEX: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_LEX_ID: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_LIKE_EMAIL: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_LIKE_NUM: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_LIKE_URL: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_LOWER_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_MORPH: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_NORM_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_ORTH_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_POS_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_PREFIX_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_PROB: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_RANK: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_RIGHT_EDGE: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_SENT: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_SENTIMENT: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_SHAPE_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_SUFFIX_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_TAG_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_TENSOR: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_TEXT: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_TEXT_WITH_WS: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_VOCAB: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_WHITESPACE_: ClassVar[str]
    _DCR_CFG_TESSERACT_TIMEOUT: ClassVar[str]
    _DCR_CFG_TOKENIZE_2_JSONFILE: ClassVar[str]
    _DCR_CFG_TOKENIZE_2_XMLFILE: ClassVar[str]
    _DCR_CFG_VERBOSE: ClassVar[str]
    _DCR_CFG_VERBOSE_LT_HEADER_FOOTER: ClassVar[str]
    _DCR_CFG_VERBOSE_LT_HEADING: ClassVar[str]
    _DCR_CFG_VERBOSE_LT_LIST_BULLET: ClassVar[str]
    _DCR_CFG_VERBOSE_LT_LIST_NUMBER: ClassVar[str]
    _DCR_CFG_VERBOSE_LT_TOC: ClassVar[str]
    _DCR_CFG_VERBOSE_PARSER: ClassVar[str]
    _DCR_CORE_ENVIRONMENT_TYPE: ClassVar[str]

    DCR_VERSION: ClassVar[str]
    ENVIRONMENT_TYPE_DEV: ClassVar[str]
    ENVIRONMENT_TYPE_PROD: ClassVar[str]
    ENVIRONMENT_TYPE_TEST: ClassVar[str]
    PDF2IMAGE_TYPE_JPEG: ClassVar[str]
    PDF2IMAGE_TYPE_PNG: ClassVar[str]

    def __init__(self) -> None:
        self._config: dict[str, str] = {}
        self._config_parser: configparser.ConfigParser = configparser.ConfigParser()
        self.directory_inbox = ""
        self.is_delete_auxiliary_files = False
        self.is_json_incl_config = False
        self.is_json_incl_fonts = False
        self.is_json_incl_heading = False
        self.is_json_incl_list_bullet = False
        self.is_json_incl_list_number = False
        self.is_json_incl_params = False
        self.is_json_sort_keys = False
        self.is_lt_footer_required = False
        self.is_lt_header_required = False
        self.is_lt_heading_file_incl_regexp = False
        self.is_lt_heading_required = False
        self.is_lt_list_bullet_required = False
        self.is_lt_list_number_file_incl_regexp = False
        self.is_lt_list_number_required = False
        self.is_lt_toc_required = False
        self.is_spacy_ignore_bracket = False
        self.is_spacy_ignore_left_punct = False
        self.is_spacy_ignore_line_type_footer = False
        self.is_spacy_ignore_line_type_header = False
        self.is_spacy_ignore_line_type_heading = False
        self.is_spacy_ignore_line_type_list_bullet = False
        self.is_spacy_ignore_line_type_list_number = False
        self.is_spacy_ignore_line_type_table = False
        self.is_spacy_ignore_line_type_toc = False
        self.is_spacy_ignore_punct = False
        self.is_spacy_ignore_quote = False
        self.is_spacy_ignore_right_punct = False
        self.is_spacy_ignore_space = False
        self.is_spacy_ignore_stop = False
        self.is_spacy_tkn_attr_cluster = False
        self.is_spacy_tkn_attr_dep_ = False
        self.is_spacy_tkn_attr_doc = False
        self.is_spacy_tkn_attr_ent_iob_ = False
        self.is_spacy_tkn_attr_ent_kb_id_ = False
        self.is_spacy_tkn_attr_ent_type_ = False
        self.is_spacy_tkn_attr_head = False
        self.is_spacy_tkn_attr_i = False
        self.is_spacy_tkn_attr_idx = False
        self.is_spacy_tkn_attr_is_alpha = False
        self.is_spacy_tkn_attr_is_ascii = False
        self.is_spacy_tkn_attr_is_bracket = False
        self.is_spacy_tkn_attr_is_currency = False
        self.is_spacy_tkn_attr_is_digit = False
        self.is_spacy_tkn_attr_is_left_punct = False
        self.is_spacy_tkn_attr_is_lower = False
        self.is_spacy_tkn_attr_is_oov = False
        self.is_spacy_tkn_attr_is_punct = False
        self.is_spacy_tkn_attr_is_quote = False
        self.is_spacy_tkn_attr_is_right_punct = False
        self.is_spacy_tkn_attr_is_sent_end = False
        self.is_spacy_tkn_attr_is_sent_start = False
        self.is_spacy_tkn_attr_is_space = False
        self.is_spacy_tkn_attr_is_stop = False
        self.is_spacy_tkn_attr_is_title = False
        self.is_spacy_tkn_attr_is_upper = False
        self.is_spacy_tkn_attr_lang_ = False
        self.is_spacy_tkn_attr_left_edge = False
        self.is_spacy_tkn_attr_lemma_ = False
        self.is_spacy_tkn_attr_lex = False
        self.is_spacy_tkn_attr_lex_id = False
        self.is_spacy_tkn_attr_like_email = False
        self.is_spacy_tkn_attr_like_num = False
        self.is_spacy_tkn_attr_like_url = False
        self.is_spacy_tkn_attr_lower_ = False
        self.is_spacy_tkn_attr_morph = False
        self.is_spacy_tkn_attr_norm_ = False
        self.is_spacy_tkn_attr_orth_ = False
        self.is_spacy_tkn_attr_pos_ = False
        self.is_spacy_tkn_attr_prefix_ = False
        self.is_spacy_tkn_attr_prob = False
        self.is_spacy_tkn_attr_rank = False
        self.is_spacy_tkn_attr_right_edge = False
        self.is_spacy_tkn_attr_sent = False
        self.is_spacy_tkn_attr_sentiment = False
        self.is_spacy_tkn_attr_shape_ = False
        self.is_spacy_tkn_attr_suffix_ = False
        self.is_spacy_tkn_attr_tag_ = False
        self.is_spacy_tkn_attr_tensor = False
        self.is_spacy_tkn_attr_text = False
        self.is_spacy_tkn_attr_text_with_ws = False
        self.is_spacy_tkn_attr_vocab = False
        self.is_spacy_tkn_attr_whitespace_ = False
        self.is_tokenize_2_jsonfile = False
        self.is_tokenize_2_xmlfile = False
        self.is_verbose = False
        self.is_verbose_lt_header_footer = False
        self.is_verbose_lt_heading = False
        self.is_verbose_lt_list_bullet = False
        self.is_verbose_lt_list_number = False
        self.is_verbose_lt_toc = False
        self.json_indent = 0
        self.lt_footer_max_distance = 0
        self.lt_footer_max_lines = 0
        self.lt_header_max_distance = 0
        self.lt_header_max_lines = 0
        self.lt_heading_file_incl_no_ctx = 0
        self.lt_heading_max_level = 0
        self.lt_heading_min_pages = 0
        self.lt_heading_rule_file = ""
        self.lt_heading_tolerance_llx = 0
        self.lt_list_bullet_min_entries = 0
        self.lt_list_bullet_rule_file = ""
        self.lt_list_bullet_tolerance_llx = 0
        self.lt_list_number_min_entries = 0
        self.lt_list_number_rule_file = ""
        self.lt_list_number_tolerance_llx = 0
        self.lt_toc_last_page = 0
        self.lt_toc_min_entries = 0
        self.pdf2image_type = ""
        self.tesseract_timeout = 0
        self.verbose_parser = ""
        self._exist = False
    def _check_config(self) -> None: ...
    def _check_config_directory_inbox(self) -> None: ...
    def _check_config_pdf2image_type(self) -> None: ...
    def _check_config_verbose_parser(self) -> None: ...
    def _determine_config_param_boolean(
        self,
        param: str,
        var: bool,
    ) -> bool: ...
    def _determine_config_param_integer(
        self,
        param: str,
        var: int,
    ) -> int: ...
    def _determine_config_spacy_tkn(self) -> None: ...
    def _determine_config_spacy_tkn_ignore(self) -> None: ...
    def _get_environment_variant(self) -> None: ...
    def _load_config(self) -> None: ...
    def exists(self) -> bool: ...
