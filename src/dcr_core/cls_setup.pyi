from __future__ import annotations

from typing import ClassVar

class Setup:
    DCR_VERSION: ClassVar[str]
    ENVIRONMENT_TYPE_DEV: ClassVar[str]
    ENVIRONMENT_TYPE_PROD: ClassVar[str]
    ENVIRONMENT_TYPE_TEST: ClassVar[str]
    PDF2IMAGE_TYPE_JPEG: ClassVar[str]
    PDF2IMAGE_TYPE_PNG: ClassVar[str]

    is_create_extra_file_heading: bool
    is_create_extra_file_list_bullet: bool
    is_create_extra_file_list_number: bool
    is_create_extra_file_table: bool
    json_indent: int
    is_json_sort_keys: bool
    lt_footer_max_distance: int
    lt_footer_max_lines: int
    lt_header_max_distance: int
    lt_header_max_lines: int
    lt_heading_file_incl_no_ctx: int
    is_lt_heading_file_incl_regexp: bool
    lt_export_rule_file_heading: str
    lt_export_rule_file_list_bullet: str
    lt_export_rule_file_list_number: str
    lt_heading_max_level: int
    lt_heading_min_pages: int
    lt_heading_rule_file: str
    lt_heading_tolerance_llx: int
    lt_list_bullet_min_entries: int
    lt_list_bullet_rule_file: str
    lt_list_bullet_tolerance_llx: int
    is_lt_list_number_file_incl_regexp: bool
    lt_list_number_min_entries: int
    lt_list_number_rule_file: str
    lt_list_number_tolerance_llx: int
    is_lt_table_file_incl_empty_columns: bool
    lt_toc_last_page: int
    lt_toc_min_entries: int
    is_parsing_line: bool
    is_parsing_page: bool
    is_parsing_word: bool
    pdf2image_type: ClassVar[str]
    tesseract_timeout: int
    is_tetml_page: bool
    is_tetml_word: bool
    is_tokenize_2_database: bool
    is_tokenize_2_jsonfile: bool
    is_verbose: bool
    is_verbose_lt_headers_footers: bool
    is_verbose_lt_heading: bool
    is_verbose_lt_list_bullet: bool
    is_verbose_lt_list_number: bool
    is_verbose_lt_table: bool
    is_verbose_lt_toc: bool
    verbose_parser: str

    is_spacy_ignore_bracket: bool
    is_spacy_ignore_left_punct: bool
    is_spacy_ignore_line_type_footer: bool
    is_spacy_ignore_line_type_header: bool
    is_spacy_ignore_line_type_heading: bool
    is_spacy_ignore_line_type_list_bullet: bool
    is_spacy_ignore_line_type_list_number: bool
    is_spacy_ignore_line_type_table: bool
    is_spacy_ignore_line_type_toc: bool
    is_spacy_ignore_punct: bool
    is_spacy_ignore_quote: bool
    is_spacy_ignore_right_punct: bool
    is_spacy_ignore_space: bool
    is_spacy_ignore_stop: bool
    is_spacy_tkn_attr_cluster: bool
    is_spacy_tkn_attr_dep_: bool
    is_spacy_tkn_attr_doc: bool
    is_spacy_tkn_attr_ent_iob_: bool
    is_spacy_tkn_attr_ent_kb_id_: bool
    is_spacy_tkn_attr_ent_type_: bool
    is_spacy_tkn_attr_head: bool
    is_spacy_tkn_attr_i: bool
    is_spacy_tkn_attr_idx: bool
    is_spacy_tkn_attr_is_alpha: bool
    is_spacy_tkn_attr_is_ascii: bool
    is_spacy_tkn_attr_is_bracket: bool
    is_spacy_tkn_attr_is_currency: bool
    is_spacy_tkn_attr_is_digit: bool
    is_spacy_tkn_attr_is_left_punct: bool
    is_spacy_tkn_attr_is_lower: bool
    is_spacy_tkn_attr_is_oov: bool
    is_spacy_tkn_attr_is_punct: bool
    is_spacy_tkn_attr_is_quote: bool
    is_spacy_tkn_attr_is_right_punct: bool
    is_spacy_tkn_attr_is_sent_end: bool
    is_spacy_tkn_attr_is_sent_start: bool
    is_spacy_tkn_attr_is_space: bool
    is_spacy_tkn_attr_is_stop: bool
    is_spacy_tkn_attr_is_title: bool
    is_spacy_tkn_attr_is_upper: bool
    is_spacy_tkn_attr_lang_: bool
    is_spacy_tkn_attr_left_edge: bool
    is_spacy_tkn_attr_lemma_: bool
    is_spacy_tkn_attr_lex: bool
    is_spacy_tkn_attr_lex_id: bool
    is_spacy_tkn_attr_like_email: bool
    is_spacy_tkn_attr_like_num: bool
    is_spacy_tkn_attr_like_url: bool
    is_spacy_tkn_attr_lower_: bool
    is_spacy_tkn_attr_morph: bool
    is_spacy_tkn_attr_norm_: bool
    is_spacy_tkn_attr_orth_: bool
    is_spacy_tkn_attr_pos_: bool
    is_spacy_tkn_attr_prefix_: bool
    is_spacy_tkn_attr_prob: bool
    is_spacy_tkn_attr_rank: bool
    is_spacy_tkn_attr_right_edge: bool
    is_spacy_tkn_attr_sent: bool
    is_spacy_tkn_attr_sentiment: bool
    is_spacy_tkn_attr_shape_: bool
    is_spacy_tkn_attr_suffix_: bool
    is_spacy_tkn_attr_tag_: bool
    is_spacy_tkn_attr_tensor: bool
    is_spacy_tkn_attr_text: bool
    is_spacy_tkn_attr_text_with_ws: bool
    is_spacy_tkn_attr_vocab: bool
    is_spacy_tkn_attr_whitespace_: bool

    def __init__(self) -> None:
        self.is_irregular_footer = None
        ...
    def exists(self) -> bool: ...
