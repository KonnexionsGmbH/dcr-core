# DCR-CORE - Application - Configuration

![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr-core?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr-core)

## 1. **`logging_cfg.yaml`**

This file controls the logging behaviour of the application. 

**Default content**:

    version: 1
    
    formatters:
      simple:
        format: "%(asctime)s [%(module)s.py  ] %(levelname)-5s %(funcName)s:%(lineno)d %(message)s"
      extended:
        format: "%(asctime)s [%(module)s.py  ] %(levelname)-5s %(funcName)s:%(lineno)d \n%(message)s"
    
    handlers:
      console:
        class: logging.StreamHandler
        level: INFO
        formatter: simple
    
      file_handler:
        class: logging.FileHandler
        level: INFO
        filename: logging_dcr_core.log
        formatter: extended
    
    loggers:
      dcr_core:
        handlers: [ console ]
    root:
      handlers: [ file_handler ]

## 2. **`setup.cfg`**

This file controls the behaviour of the **`DCR-CORE`** application. 

The customisable entries are:

    [dcr_core]
    create_extra_file_heading = true
    create_extra_file_list_bullet = true
    create_extra_file_list_number = true
    create_extra_file_table = true
    delete_auxiliary_files = true
    directory_inbox = data/inbox_prod
    json_indent = 4
    json_sort_keys = false
    lt_export_rule_file_heading = data/lt_export_rule_heading.json
    lt_export_rule_file_list_bullet = data/lt_export_rule_list_bullet.json
    lt_export_rule_file_list_number = data/lt_export_rule_list_number.json
    lt_footer_max_distance = 3
    lt_footer_max_lines = 3
    lt_footer_required = true
    lt_header_max_distance = 3
    lt_header_max_lines = 3
    lt_header_required = true
    lt_heading_file_incl_no_ctx = 1
    lt_heading_file_incl_regexp = false
    lt_heading_max_level = 3
    lt_heading_min_pages = 2
    lt_heading_required = true
    lt_heading_rule_file = none
    lt_heading_tolerance_llx = 10
    lt_list_bullet_min_entries = 2
    lt_list_bullet_required = true
    lt_list_bullet_rule_file = none
    lt_list_bullet_tolerance_llx = 10
    lt_list_number_file_incl_regexp = false
    lt_list_number_min_entries = 2
    lt_list_number_required = true
    lt_list_number_rule_file = none
    lt_list_number_tolerance_llx = 10
    lt_table_file_incl_empty_columns = true
    lt_table_required = true
    lt_toc_last_page = 5
    lt_toc_min_entries = 5
    lt_toc_required = true
    pdf2image_type = jpeg
    tesseract_timeout = 30
    tokenize_2_database = true
    tokenize_2_jsonfile = true
    verbose = true
    verbose_lt_header_footer = false
    verbose_lt_heading = false
    verbose_lt_list_bullet = false
    verbose_lt_list_number = false
    verbose_lt_table = false
    verbose_lt_toc = false
    verbose_parser = none

| Parameter                        | Description                                                                                                          |
|----------------------------------|----------------------------------------------------------------------------------------------------------------------|
| create_extra_file_heading        | Create a separate **`JSON`** file with the table of contents.                                                        |
| create_extra_file_list_bullet    | Create a separate **`JSON`** file with the bulleted lists.                                                           |
| create_extra_file_list_number    | Create a separate **`JSON`** file with the numbered lists.                                                           |
| create_extra_file_table          | Create a separate **`JSON`** file with the tables.                                                                   |
| delete_auxiliary_files           | Delete the auxiliary files after a successful <br>processing step.                                                   |
| directory_inbox                  | Directory for the new documents received.                                                                            |
| json_indent                      | Improves the readability of the **`JSON`** file.                                                                     |
| json_sort_keys                   | If it is set to **`true`**, the keys are set <br/>in ascending order else, they appear as <br/>in the Python object. |
| lt_export_rule_file_heading      | File name for the export of the heading rules.                                                                       |
| lt_export_rule_file_list_bullet  | File name for the export of the bulleted list rules.                                                                 |
| lt_export_rule_file_list_number  | File name for the export of the numbered list rules.                                                                 |
| lt_footer_max_distance           | Maximum Levenshtein distance for a footer line.                                                                      |
| lt_footer_max_lines              | Maximum number of footers.                                                                                           |
| lt_footer_required               | If it is set to **`true`**, the determination of the footer lines is performed.                                      |
| lt_header_max_distance           | Maximum Levenshtein distance for a header line.                                                                      |
| lt_header_max_lines              | Maximum number of headers.                                                                                           |
| lt_header_required               | If it is set to **`true`**, the determination of the header lines is performed.                                      |
| lt_heading_file_incl_no_ctx      | The number of lines following the heading to be included as context into the **`JSON`** file.                        |
| lt_heading_file_incl_regexp      | If it is set to **`true`**, the regular expression for the heading is included in the **`JSON`** file.               |
| lt_heading_max_level             | Maximum level of the heading structure.                                                                              |
| lt_heading_min_pages             | Minimum number of pages to determine the headings.                                                                   |
| lt_heading_required              | If it is set to **`true`**, the determination of the heading lines is performed.                                     |
| lt_heading_rule_file             | File with rules to determine the headings.                                                                           |
| lt_heading_tolerance_llx         | Tolerance of vertical indentation in percent.                                                                        |
| lt_list_bullet_min_entries       | Minimum number of entries to determine a bulleted list.                                                              |
| lt_list_bullet_required          | If it is set to **`true`**, the determination of the bulleted lists lines is performed.                               |
| lt_list_bullet_rule_file         | File with rules to determine the bulleted lists.                                                                     |
| lt_list_bullet_tolerance_llx     | Tolerance of vertical indentation in percent.                                                                        |
| lt_list_number_file_incl_regexp  | If it is set to **`true`**, the regular expression for the numbered list is included in the **`JSON`** file.         |
| lt_list_number_min_entries       | Minimum number of entries to determine a numbered list.                                                              |
| lt_list_number_required          | If it is set to **`true`**, the determination of the numbered lists lines is performed.                               |
| lt_list_number_rule_file         | File with rules to determine the numbered lists.                                                                     |
| lt_list_number_tolerance_llx     | Tolerance of vertical indentation in percent.                                                                        |
| lt_table_file_incl_empty_columns | If it is set to **`true`**, the empty <br/>cells are included in the separate <br/>**`JSON`** file with the tables.  |
| lt_table_required                | If it is set to **`true`**, the determination of the table lines is performed.                                       |
| lt_toc_last_page                 | Maximum number of pages for the search of the TOC (from the beginning).                                              |
| lt_toc_min_entries               | Minimum number of TOC entries.                                                                                       |
| lt_toc_required                  | If it is set to **`true`**, the determination of the TOC lines is performed.                                         |
| pdfimage_type                    | Format of the image files for the scanned <br/>`pdf` document: **`jpeg`** or **`pdf`**.                              |
| tesseract_timeout                | Terminate the tesseract job after a <br>period of time (seconds).                                                    |
| tokenize_2_database              | Store the tokens in the database table **`token`**.                                                                  |
| tokenize_2_jsonfile              | Store the tokens in a **`JSON`** flat file.                                                                          |
| verbose                          | Display progress messages for processing.                                                                            |
| verbose_lt_headers_footers       | Display progress messages for headers & footers line type determination.                                             |
| verbose_lt_heading               | Display progress messages for heading line type determination.                                                       |
| verbose_lt_list_bullet           | Display progress messages for line type determination of a bulleted list.                                            |
| verbose_lt_list_number           | Display progress messages for line type determination of a numbered list.                                            |
| verbose_lt_table                 | Display progress messages for table line type determination.                                                         |
| verbose_lt_toc                   | Display progress messages for table of content line type determination.                                              |
| verbose_parser                   | Display progress messages for parsing **`xml`** (TETML) : <br>**`all`**, **`none`** or **`text`**.                   |

The configuration parameters can be set differently for the individual environments (`dev`, `prod` and `test`).

**Examples**:
      
    [dcr_core.env.dev]
    delete_auxiliary_files = false
    directory_inbox = data/inbox_dev
    lt_footer_max_lines = 3
    lt_header_max_lines = 3
    lt_heading_file_incl_no_ctx = 3
    lt_heading_file_incl_regexp = true
    lt_heading_tolerance_llx = 5
    lt_list_bullet_tolerance_llx = 5
    lt_list_number_file_incl_regexp = true
    lt_list_number_tolerance_llx = 5
    lt_table_file_incl_empty_columns = false
    ...
    
## 4. **`setup.cfg`** - [spaCy](https://spacy.io){:target="_blank"} Token Attributes

The tokens derived from the documents can be qualified via various attributes. 
The available options are described below.

    [dcr_core.spacy]
    spacy_ignore_bracket = false
    spacy_ignore_left_punct = false
    spacy_ignore_line_type_footer = false
    spacy_ignore_line_type_header = false
    spacy_ignore_line_type_heading = false
    spacy_ignore_line_type_list_bullet = false
    spacy_ignore_line_type_list_number = false
    spacy_ignore_line_type_table = false
    spacy_ignore_line_type_toc = false
    spacy_ignore_punct = false
    spacy_ignore_quote = false
    spacy_ignore_right_punct = false
    spacy_ignore_space = false
    spacy_ignore_stop = false
    spacy_tkn_attr_cluster = true
    spacy_tkn_attr_dep_ = true
    spacy_tkn_attr_doc = true
    spacy_tkn_attr_ent_iob_ = true
    spacy_tkn_attr_ent_kb_id_ = true
    spacy_tkn_attr_ent_type_ = true
    spacy_tkn_attr_head = true
    spacy_tkn_attr_i = true
    spacy_tkn_attr_idx = true
    spacy_tkn_attr_is_alpha = true
    spacy_tkn_attr_is_ascii = true
    spacy_tkn_attr_is_bracket = true
    spacy_tkn_attr_is_currency = true
    spacy_tkn_attr_is_digit = true
    spacy_tkn_attr_is_left_punct = true
    spacy_tkn_attr_is_lower = true
    spacy_tkn_attr_is_oov = true
    spacy_tkn_attr_is_punct = true
    spacy_tkn_attr_is_quote = true
    spacy_tkn_attr_is_right_punct = true
    spacy_tkn_attr_is_sent_end = true
    spacy_tkn_attr_is_sent_start = true
    spacy_tkn_attr_is_space = true
    spacy_tkn_attr_is_stop = true
    spacy_tkn_attr_is_title = true
    spacy_tkn_attr_is_upper = true
    spacy_tkn_attr_lang_ = true
    spacy_tkn_attr_left_edge = true
    spacy_tkn_attr_lemma_ = true
    spacy_tkn_attr_lex = true
    spacy_tkn_attr_lex_id = true
    spacy_tkn_attr_like_email = true
    spacy_tkn_attr_like_num = true
    spacy_tkn_attr_like_url = true
    spacy_tkn_attr_lower_ = true
    spacy_tkn_attr_morph = true
    spacy_tkn_attr_norm_ = true
    spacy_tkn_attr_orth_ = true
    spacy_tkn_attr_pos_ = true
    spacy_tkn_attr_prefix_ = true
    spacy_tkn_attr_prob = true
    spacy_tkn_attr_rank = true
    spacy_tkn_attr_right_edge = true
    spacy_tkn_attr_sent = true
    spacy_tkn_attr_sentiment = true
    spacy_tkn_attr_shape_ = true
    spacy_tkn_attr_suffix_ = true
    spacy_tkn_attr_tag_ = true
    spacy_tkn_attr_tensor = true
    spacy_tkn_attr_text = true
    spacy_tkn_attr_text_with_ws = true
    spacy_tkn_attr_vocab = true
    spacy_tkn_attr_whitespace_ = true
    
| Parameter                          | Description                                                                                                   |
|------------------------------------|---------------------------------------------------------------------------------------------------------------|
 | spacy_ignore_bracket               | Ignore the tokens which are brackets ?                                                                        |
 | spacy_ignore_left_punct            | Ignore the tokens which are left punctuation marks, e.g. "(" ?                                                |
 | spacy_ignore_line_type_footer      | Ignore the tokens from line type footer ?                                                                     |
 | spacy_ignore_line_type_header      | Ignore the tokens from line type header ?                                                                     |
 | spacy_ignore_line_type_heading     | Ignore the tokens from line type heading ?                                                                    |
 | spacy_ignore_line_type_list_bullet | Ignore the tokens from line type bulleted list ?                                                              |
 | spacy_ignore_line_type_list_number | Ignore the tokens from line type numbered list ?                                                              |
 | spacy_ignore_line_type_table       | Ignore the tokens from line type table ?                                                                      |
 | spacy_ignore_line_type_toc         | Ignore the tokens from line type TOC ?                                                                        |
 | spacy_ignore_punct                 | Ignore the tokens which are punctuations ?                                                                    |
 | spacy_ignore_quote                 | Ignore the tokens which are quotation marks ?                                                                 |
 | spacy_ignore_right_punct           | Ignore the tokens which are right punctuation marks, e.g. ")" ?                                               |
 | spacy_ignore_space                 | Ignore the tokens which consist of whitespace characters ?                                                    |
 | spacy_ignore_stop                  | Ignore the tokens which are part of a “stop list” ?                                                           |
 |                                    |                                                                                                               |                                                                                                               |
 | spacy_tkn_attr_cluster             | Brown cluster ID.                                                                                             |
 | spacy_tkn_attr_dep_                | Syntactic dependency relation.                                                                                |
 | spacy_tkn_attr_doc                 | The parent document.                                                                                          |
 | spacy_tkn_attr_ent_iob_            | IOB code of named entity tag.                                                                                 |
 | spacy_tkn_attr_ent_kb_id_          | Knowledge base ID that refers to the named entity <br>this token is a part of, if any.                        |
 | spacy_tkn_attr_ent_type_           | Named entity type.                                                                                            |
 | spacy_tkn_attr_head                | The syntactic parent, or “governor”, of this token.                                                           |
 | spacy_tkn_attr_i                   | The index of the token within the parent document.                                                            |
 | spacy_tkn_attr_idx                 | The character offset of the token within the parent document.                                                 |
 | spacy_tkn_attr_is_alpha            | Does the token consist of alphabetic characters?                                                              |
 | spacy_tkn_attr_is_ascii            | Does the token consist of ASCII characters? <br>Equivalent to all (ord(c) < 128 for c in token.text).         |
 | spacy_tkn_attr_is_bracket          | Is the token a bracket?                                                                                       |
 | spacy_tkn_attr_is_currency         | Is the token a currency symbol?                                                                               |
 | spacy_tkn_attr_is_digit            | Does the token consist of digits?                                                                             |
 | spacy_tkn_attr_is_left_punct       | Is the token a left punctuation mark, e.g. "(" ?                                                              |
 | spacy_tkn_attr_is_lower            | Is the token in lowercase? Equivalent to token.text.islower().                                                |
 | spacy_tkn_attr_is_oov              | Is the token out-of-vocabulary?                                                                               |
 | spacy_tkn_attr_is_punct            | Is the token punctuation?                                                                                     |
 | spacy_tkn_attr_is_quote            | Is the token a quotation mark?                                                                                |
 | spacy_tkn_attr_is_right_punct      | Is the token a right punctuation mark, e.g. ")" ?                                                             |
 | spacy_tkn_attr_is_sent_end         | Does the token end a sentence?                                                                                |
 | spacy_tkn_attr_is_sent_start       | Does the token start a sentence?                                                                              |
 | spacy_tkn_attr_is_space            | Does the token consist of whitespace characters? <br>Equivalent to token.text.isspace().                      |
 | spacy_tkn_attr_is_stop             | Is the token part of a “stop list”?                                                                           |
 | spacy_tkn_attr_is_title            | Is the token in titlecase?                                                                                    |
 | spacy_tkn_attr_is_upper            | Is the token in uppercase? Equivalent to token.text.isupper().                                                |
 | spacy_tkn_attr_lang_               | Language of the parent document’s vocabulary.                                                                 |
 | spacy_tkn_attr_left_edge           | The leftmost token of this token’s syntactic descendants.                                                     |
 | spacy_tkn_attr_lemma_              | Base form of the token, with no inflectional suffixes.                                                        |
 | spacy_tkn_attr_lex                 | The underlying lexeme.                                                                                        |
 | spacy_tkn_attr_lex_id              | Sequential ID of the token’s lexical type, used to index into tables, e.g. for word vectors.                  |
 | spacy_tkn_attr_like_email          | Does the token resemble an email address?                                                                     |
 | spacy_tkn_attr_like_num            | Does the token represent a number?                                                                            |
 | spacy_tkn_attr_like_url            | Does the token resemble a URL?                                                                                |
 | spacy_tkn_attr_lower_              | Lowercase form of the token text. Equivalent to Token.text.lower().                                           |
 | spacy_tkn_attr_morph               | Morphological analysis.                                                                                       |
 | spacy_tkn_attr_norm_               | The token’s norm, i.e. a normalized form of the token text.                                                   |
 | spacy_tkn_attr_orth_               | Verbatim text content (identical to Token.text). <br>Exists mostly for consistency with the other attributes. |
 | spacy_tkn_attr_pos_                | Coarse-grained part-of-speech from the Universal POS tag set.                                                 |
 | spacy_tkn_attr_prefix_             | A length-N substring from the start of the token. <br>Defaults to N=1.                                        |
 | spacy_tkn_attr_prob                | Smoothed log probability estimate of token’s word type <br>(context-independent entry in the vocabulary).     |
 | spacy_tkn_attr_rank                | Sequential ID of the token’s lexical type, used to index <br>into tables, e.g. for word vectors.              |
 | spacy_tkn_attr_right_edge          | The rightmost token of this token’s syntactic descendants.                                                    |
 | spacy_tkn_attr_sent                | The sentence span that this token is a part of.                                                               |
 | spacy_tkn_attr_sentiment           | A scalar value indicating the positivity or negativity of the token.                                          |
 | spacy_tkn_attr_shape_              | Transform of the token’s string to show orthographic features.                                                |
 | spacy_tkn_attr_suffix_             | Length-N substring from the end of the token. Defaults to N=3.                                                |
 | spacy_tkn_attr_tag_                | Fine-grained part-of-speech.                                                                                  |
 | spacy_tkn_attr_tensor              | The token’s slice of the parent Doc’s tensor.                                                                 |
 | spacy_tkn_attr_text                | Verbatim text content.                                                                                        |
 | spacy_tkn_attr_text_with_ws        | Text content, with trailing space character if present.                                                       |
 | spacy_tkn_attr_vocab               | The vocab object of the parent Doc.                                                                           |
 | spacy_tkn_attr_whitespace_         | Trailing space character if present.                                                                          |

More information about the [spaCy](https://spacy.io){:target="_blank"} token attributes can be found [here](https://spacy.io/api/token#attributes){:target="_blank"}.
**`DCR-CORE`** currently supports only a subset of the possible attributes, but this can easily be extended if required.

Detailed information about the universal POS tags can be found [here](https://universaldependencies.org/u/pos/){:target="_blank"}.