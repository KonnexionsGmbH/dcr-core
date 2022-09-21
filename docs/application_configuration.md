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

| Parameter                        | Default                              | Description                                                                                                          |
|----------------------------------|--------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| delete_auxiliary_files           | false                                | Delete the auxiliary files after a successful <br>processing step.                                                   |
| directory_inbox                  | data/inbox_prod                      | Directory for the new documents received.                                                                            |
| json_incl_config                 | true                                 | Include the configuration data in the **`JSON`** file.                                                               |
| json_incl_fonts                  | true                                 | Include the font data in the **`JSON`** file.                                                                        |
| json_incl_heading                | true                                 | Include the heading data in the **`JSON`** file.                                                                     |
| json_incl_list_bullet            | true                                 | Include the bulleted list data in the **`JSON`** file.                                                               |
| json_incl_list_number            | true                                 | Include the numbered list data in the **`JSON`** file.                                                               |
| json_incl_params                 | true                                 | Include the parameters in the **`JSON`** file.                                                                       |
| json_incl_table                  | true                                 | Include the table data in the **`JSON`** file.                                                                       |
| json_indent                      | 4                                    | Improves the readability of the **`JSON`** file.                                                                     |
| json_sort_keys                   | true                                 | If it is set to **`true`**, the keys are set <br/>in ascending order else, they appear as <br/>in the Python object. |
| lt_export_rule_file_heading      | data/lt_export_rule_heading.json     | File name for the export of the heading rules.                                                                       |
| lt_export_rule_file_list_bullet  | data/lt_export_rule_list_bullet.json | File name for the export of the bulleted list rules.                                                                 |
| lt_export_rule_file_list_number  | data/lt_export_rule_list_number.json | File name for the export of the numbered list rules.                                                                 |
| lt_footer_max_distance           | 3                                    | Maximum Levenshtein distance for a footer line.                                                                      |
| lt_footer_max_lines              | 3                                    | Maximum number of footers.                                                                                           |
| lt_header_max_distance           | 3                                    | Maximum Levenshtein distance for a header line.                                                                      |
| lt_header_max_lines              | 3                                    | Maximum number of headers.                                                                                           |
| lt_heading_file_incl_no_ctx      | 1                                    | The number of lines following the heading to be included as context into the **`JSON`** file.                        |
| lt_heading_file_incl_regexp      | true                                 | If it is set to **`true`**, the regular expression for the heading is included in the **`JSON`** file.               |
| lt_heading_max_level             | 3                                    | Maximum level of the heading structure.                                                                              |
| lt_heading_min_pages             | 2                                    | Minimum number of pages to determine the headings.                                                                   |
| lt_heading_required              | true                                 | If it is set to **`true`**, the determination of the heading lines is performed.                                     |
| lt_heading_rule_file             | none                                 | File with rules to determine the headings.                                                                           |
| lt_heading_tolerance_llx         | 10                                   | Tolerance of vertical indentation in percent.                                                                        |
| lt_list_bullet_min_entries       | 2                                    | Minimum number of entries to determine a bulleted list.                                                              |
| lt_list_bullet_required          | true                                 | If it is set to **`true`**, the determination of the bulleted lists lines is performed.                              |
| lt_list_bullet_rule_file         | none                                 | File with rules to determine the bulleted lists.                                                                     |
| lt_list_bullet_tolerance_llx     | 10                                   | Tolerance of vertical indentation in percent.                                                                        |
| lt_list_number_file_incl_regexp  | true                                 | If it is set to **`true`**, the regular expression for the numbered list is included in the **`JSON`** file.         |
| lt_list_number_min_entries       | 2                                    | Minimum number of entries to determine a numbered list.                                                              |
| lt_list_number_required          | true                                 | If it is set to **`true`**, the determination of the numbered lists lines is performed.                              |
| lt_list_number_rule_file         | none                                 | File with rules to determine the numbered lists.                                                                     |
| lt_list_number_tolerance_llx     | 10                                   | Tolerance of vertical indentation in percent.                                                                        |
| lt_toc_last_page                 | 5                                    | Maximum number of pages for the search of the TOC (from the beginning).                                              |
| lt_toc_min_entries               | 5                                    | Minimum number of TOC entries.                                                                                       |
| lt_toc_required                  | true                                 | If it is set to **`true`**, the determination of the TOC lines is performed.                                         |
| pdfimage_type                    | jpeg                                 | Format of the image files for the scanned <br/>`pdf` document: **`jpeg`** or **`pdf`**.                              |
| tesseract_timeout                | 30                                   | Terminate the tesseract job after a <br>period of time (seconds).                                                    |
| tokenize_2_database              | true                                 | Store the tokens in the database table **`token`**.                                                                  |
| tokenize_2_jsonfile              | true                                 | Store the tokens in a **`JSON`** flat file.                                                                          |
| verbose                          | true                                 | Display progress messages for processing.                                                                            |
| verbose_lt_headers_footers       | false                                | Display progress messages for headers & footers line type determination.                                             |
| verbose_lt_heading               | false                                | Display progress messages for heading line type determination.                                                       |
| verbose_lt_list_bullet           | false                                | Display progress messages for line type determination of a bulleted list.                                            |
| verbose_lt_list_number           | false                                | Display progress messages for line type determination of a numbered list.                                            |
| verbose_lt_toc                   | false                                | Display progress messages for table of content line type determination.                                              |
| verbose_parser                   | false                                | Display progress messages for parsing **`xml`** (TETML) : <br>**`all`**, **`none`** or **`text`**.                   |

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
    
| Parameter                          | Default   | Description                                                                                                   |
|------------------------------------|-----------|---------------------------------------------------------------------------------------------------------------|
 | spacy_ignore_bracket               | false     | Ignore the tokens which are brackets ?                                                                        |
 | spacy_ignore_left_punct            | false     | Ignore the tokens which are left punctuation marks, e.g. "(" ?                                                |
 | spacy_ignore_line_type_footer      | false     | Ignore the tokens from line type footer ?                                                                     |
 | spacy_ignore_line_type_header      | false     | Ignore the tokens from line type header ?                                                                     |
 | spacy_ignore_line_type_heading     | false     | Ignore the tokens from line type heading ?                                                                    |
 | spacy_ignore_line_type_list_bullet | false     | Ignore the tokens from line type bulleted list ?                                                              |
 | spacy_ignore_line_type_list_number | false     | Ignore the tokens from line type numbered list ?                                                              |
 | spacy_ignore_line_type_table       | false     | Ignore the tokens from line type table ?                                                                      |
 | spacy_ignore_line_type_toc         | false     | Ignore the tokens from line type TOC ?                                                                        |
 | spacy_ignore_punct                 | false     | Ignore the tokens which are punctuations ?                                                                    |
 | spacy_ignore_quote                 | false     | Ignore the tokens which are quotation marks ?                                                                 |
 | spacy_ignore_right_punct           | false     | Ignore the tokens which are right punctuation marks, e.g. ")" ?                                               |
 | spacy_ignore_space                 | false     | Ignore the tokens which consist of whitespace characters ?                                                    |
 | spacy_ignore_stop                  | false     | Ignore the tokens which are part of a “stop list” ?                                                           |
 |                                    |           |                                                                                                               |                                                                                                               |
 | spacy_tkn_attr_cluster             | true      | Brown cluster ID.                                                                                             |
 | spacy_tkn_attr_dep_                | true      | Syntactic dependency relation.                                                                                |
 | spacy_tkn_attr_doc                 | true      | The parent document.                                                                                          |
 | spacy_tkn_attr_ent_iob_            | true      | IOB code of named entity tag.                                                                                 |
 | spacy_tkn_attr_ent_kb_id_          | true      | Knowledge base ID that refers to the named entity <br>this token is a part of, if any.                        |
 | spacy_tkn_attr_ent_type_           | true      | Named entity type.                                                                                            |
 | spacy_tkn_attr_head                | true      | The syntactic parent, or “governor”, of this token.                                                           |
 | spacy_tkn_attr_i                   | true      | The index of the token within the parent document.                                                            |
 | spacy_tkn_attr_idx                 | true      | The character offset of the token within the parent document.                                                 |
 | spacy_tkn_attr_is_alpha            | true      | Does the token consist of alphabetic characters?                                                              |
 | spacy_tkn_attr_is_ascii            | true      | Does the token consist of ASCII characters? <br>Equivalent to all (ord(c) < 128 for c in token.text).         |
 | spacy_tkn_attr_is_bracket          | true      | Is the token a bracket?                                                                                       |
 | spacy_tkn_attr_is_currency         | true      | Is the token a currency symbol?                                                                               |
 | spacy_tkn_attr_is_digit            | true      | Does the token consist of digits?                                                                             |
 | spacy_tkn_attr_is_left_punct       | true      | Is the token a left punctuation mark, e.g. "(" ?                                                              |
 | spacy_tkn_attr_is_lower            | true      | Is the token in lowercase? Equivalent to token.text.islower().                                                |
 | spacy_tkn_attr_is_oov              | true      | Is the token out-of-vocabulary?                                                                               |
 | spacy_tkn_attr_is_punct            | true      | Is the token punctuation?                                                                                     |
 | spacy_tkn_attr_is_quote            | true      | Is the token a quotation mark?                                                                                |
 | spacy_tkn_attr_is_right_punct      | true      | Is the token a right punctuation mark, e.g. ")" ?                                                             |
 | spacy_tkn_attr_is_sent_end         | true      | Does the token end a sentence?                                                                                |
 | spacy_tkn_attr_is_sent_start       | true      | Does the token start a sentence?                                                                              |
 | spacy_tkn_attr_is_space            | true      | Does the token consist of whitespace characters? <br>Equivalent to token.text.isspace().                      |
 | spacy_tkn_attr_is_stop             | true      | Is the token part of a “stop list”?                                                                           |
 | spacy_tkn_attr_is_title            | true      | Is the token in titlecase?                                                                                    |
 | spacy_tkn_attr_is_upper            | true      | Is the token in uppercase? Equivalent to token.text.isupper().                                                |
 | spacy_tkn_attr_lang_               | true      | Language of the parent document’s vocabulary.                                                                 |
 | spacy_tkn_attr_left_edge           | true      | The leftmost token of this token’s syntactic descendants.                                                     |
 | spacy_tkn_attr_lemma_              | true      | Base form of the token, with no inflectional suffixes.                                                        |
 | spacy_tkn_attr_lex                 | true      | The underlying lexeme.                                                                                        |
 | spacy_tkn_attr_lex_id              | true      | Sequential ID of the token’s lexical type, used to index into tables, e.g. for word vectors.                  |
 | spacy_tkn_attr_like_email          | true      | Does the token resemble an email address?                                                                     |
 | spacy_tkn_attr_like_num            | true      | Does the token represent a number?                                                                            |
 | spacy_tkn_attr_like_url            | true      | Does the token resemble a URL?                                                                                |
 | spacy_tkn_attr_lower_              | true      | Lowercase form of the token text. Equivalent to Token.text.lower().                                           |
 | spacy_tkn_attr_morph               | true      | Morphological analysis.                                                                                       |
 | spacy_tkn_attr_norm_               | true      | The token’s norm, i.e. a normalized form of the token text.                                                   |
 | spacy_tkn_attr_orth_               | true      | Verbatim text content (identical to Token.text). <br>Exists mostly for consistency with the other attributes. |
 | spacy_tkn_attr_pos_                | true      | Coarse-grained part-of-speech from the Universal POS tag set.                                                 |
 | spacy_tkn_attr_prefix_             | true      | A length-N substring from the start of the token. <br>Defaults to N=1.                                        |
 | spacy_tkn_attr_prob                | true      | Smoothed log probability estimate of token’s word type <br>(context-independent entry in the vocabulary).     |
 | spacy_tkn_attr_rank                | true      | Sequential ID of the token’s lexical type, used to index <br>into tables, e.g. for word vectors.              |
 | spacy_tkn_attr_right_edge          | true      | The rightmost token of this token’s syntactic descendants.                                                    |
 | spacy_tkn_attr_sent                | true      | The sentence span that this token is a part of.                                                               |
 | spacy_tkn_attr_sentiment           | true      | A scalar value indicating the positivity or negativity of the token.                                          |
 | spacy_tkn_attr_shape_              | true      | Transform of the token’s string to show orthographic features.                                                |
 | spacy_tkn_attr_suffix_             | true      | Length-N substring from the end of the token. Defaults to N=3.                                                |
 | spacy_tkn_attr_tag_                | true      | Fine-grained part-of-speech.                                                                                  |
 | spacy_tkn_attr_tensor              | true      | The token’s slice of the parent Doc’s tensor.                                                                 |
 | spacy_tkn_attr_text                | true      | Verbatim text content.                                                                                        |
 | spacy_tkn_attr_text_with_ws        | true      | Text content, with trailing space character if present.                                                       |
 | spacy_tkn_attr_vocab               | true      | The vocab object of the parent Doc.                                                                           |
 | spacy_tkn_attr_whitespace_         | true      | Trailing space character if present.                                                                          |

More information about the [spaCy](https://spacy.io){:target="_blank"} token attributes can be found [here](https://spacy.io/api/token#attributes){:target="_blank"}.
**`DCR-CORE`** currently supports only a subset of the possible attributes, but this can easily be extended if required.

Detailed information about the universal POS tags can be found [here](https://universaldependencies.org/u/pos/){:target="_blank"}.