# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""NLP utility class.

Typical usage example:

    my_instance = NLPCore()

    if my_instance.exists():
"""
from __future__ import annotations

import collections
import json
import re
from typing import ClassVar

from dcr_core import core_glob
from dcr_core import core_utils


class NLPCore:
    """NLP utility class."""

    # ------------------------------------------------------------------
    # Global type aliases.
    # ------------------------------------------------------------------
    FontJSON = dict[str, bool | float | int | str]
    WordJSON = dict[str, bool | float | int | str]
    LineJSON = dict[str, float | int | list[WordJSON] | str]
    ParaJSON = dict[str, int | list[LineJSON] | str]
    PageJSON = dict[str, int | list[ParaJSON]]
    ConfigJSON = dict[str, bool | str]
    DocumentJSON = dict[str, bool | int | list[PageJSON] | str]
    ParamsJSON = dict[str, bool | int | str]

    # ------------------------------------------------------------------
    # Class variables.
    # ------------------------------------------------------------------
    ENVIRONMENT_TYPE_DEV: ClassVar[str] = "dev"
    ENVIRONMENT_TYPE_PROD: ClassVar[str] = "prod"
    ENVIRONMENT_TYPE_TEST: ClassVar[str] = "test"

    JSON_NAME_CONFIG: ClassVar[str] = "config"
    JSON_NAME_CONTAINER_FONTS: ClassVar[str] = "fonts"
    JSON_NAME_CONTAINER_LINES: ClassVar[str] = "lines"
    JSON_NAME_CONTAINER_PAGES: ClassVar[str] = "pages"
    JSON_NAME_CONTAINER_PARAS: ClassVar[str] = "paras"
    JSON_NAME_CONTAINER_WORDS: ClassVar[str] = "words"
    JSON_NAME_CREATED_AT: ClassVar[str] = "createdAt"
    JSON_NAME_CREATED_BY: ClassVar[str] = "createdBy"

    JSON_NAME_DIRECTORY_NAME: ClassVar[str] = "directoryName"
    JSON_NAME_DOCUMENT_ID: ClassVar[str] = "documentId"

    JSON_NAME_EMBEDDED: ClassVar[str] = "embedded"
    JSON_NAME_ENVIRONMENT_VARIANT: ClassVar[str] = "environmentVariant"

    JSON_NAME_FILE_NAME_CURR: ClassVar[str] = "fileNameCurr"
    JSON_NAME_FILE_NAME_NEXT: ClassVar[str] = "fileNameNext"
    JSON_NAME_FILE_NAME_ORIG: ClassVar[str] = "fileNameOrig"
    JSON_NAME_FONT: ClassVar[str] = "font"
    JSON_NAME_FONT_NO: ClassVar[str] = "fontNo"
    JSON_NAME_FULL_NAME: ClassVar[str] = "fullName"

    JSON_NAME_ID: ClassVar[str] = "id"
    JSON_NAME_ITALIC_ANGLE: ClassVar[str] = "italicAngle"

    JSON_NAME_JSON_INDENT: ClassVar[str] = "jsonIndent"
    JSON_NAME_JSON_SORT_KEYS: ClassVar[str] = "jsonSortKeys"

    JSON_NAME_LINE_NO: ClassVar[str] = "lineNo"
    JSON_NAME_LINE_NO_FIRST: ClassVar[str] = "lineNoFirst"
    JSON_NAME_LINE_NO_LAST: ClassVar[str] = "lineNoLast"
    JSON_NAME_LINE_NO_PAGE: ClassVar[str] = "lineNoPage"
    JSON_NAME_LINE_NO_PARA: ClassVar[str] = "lineNoPara"
    JSON_NAME_LINE_TYPE_FOOTER_REQUIRED: ClassVar[str] = "ltFooterRequired"
    JSON_NAME_LINE_TYPE_HEADER_REQUIRED: ClassVar[str] = "ltHeaderRequired"
    JSON_NAME_LINE_TYPE_HEADING_REQUIRED: ClassVar[str] = "ltHeadingRequired"
    JSON_NAME_LINE_TYPE_LIST_BULLET_REQUIRED: ClassVar[str] = "ltListBulletRequired"
    JSON_NAME_LINE_TYPE_LIST_NUMBER_REQUIRED: ClassVar[str] = "ltListNumberRequired"
    JSON_NAME_LINE_TYPE_TABLE_REQUIRED: ClassVar[str] = "ltTableRequired"
    JSON_NAME_LINE_TYPE_TOC_REQUIRED: ClassVar[str] = "ltTocRequired"
    JSON_NAME_LLX: ClassVar[str] = "llx"
    JSON_NAME_LT_FOOTER_MAX_DISTANCE: ClassVar[str] = "ltFooterMaxDistance"
    JSON_NAME_LT_FOOTER_MAX_LINES: ClassVar[str] = "ltFooterMaxLines"
    JSON_NAME_LT_HEADER_MAX_DISTANCE: ClassVar[str] = "ltHeaderMaxDistance"
    JSON_NAME_LT_HEADER_MAX_LINES: ClassVar[str] = "ltHeaderMaxLines"
    JSON_NAME_LT_HEADING_FILE_INCL_NO_CTX: ClassVar[str] = "ltHeadingFileInclNoCtx"
    JSON_NAME_LT_HEADING_FILE_INCL_REGEXP: ClassVar[str] = "ltHeadingFileInclRegexp"
    JSON_NAME_LT_HEADING_MAX_LEVEL: ClassVar[str] = "ltHeadingMaxLevel"
    JSON_NAME_LT_HEADING_MIN_PAGES: ClassVar[str] = "ltHeadingMinPages"
    JSON_NAME_LT_HEADING_RULE_FILE: ClassVar[str] = "ltHeadingRuleFile"
    JSON_NAME_LT_HEADING_TOLERANCE_LLX: ClassVar[str] = "ltHeadingToleranceLlx"
    JSON_NAME_LT_LIST_BULLET_MIN_ENTRIES: ClassVar[str] = "ltListBulletMinEntries"
    JSON_NAME_LT_LIST_BULLET_RULE_FILE: ClassVar[str] = "ltListBulletRuleFile"
    JSON_NAME_LT_LIST_BULLET_TOLERANCE_LLX: ClassVar[str] = "ltListBulletToleranceLlx"
    JSON_NAME_LT_LIST_NUMBER_MIN_ENTRIES: ClassVar[str] = "ltListNumberMinEntries"
    JSON_NAME_LT_LIST_NUMBER_RULE_FILE: ClassVar[str] = "ltListNumberRuleFile"
    JSON_NAME_LT_LIST_NUMBER_TOLERANCE_LLX: ClassVar[str] = "ltListNumberToleranceLlx"
    JSON_NAME_LT_TABLE_FILE_INCL_EMPTY_COLUMNS: ClassVar[str] = "ltTableFileInclEmptyColumns"
    JSON_NAME_LT_TOC_LAST_PAGE: ClassVar[str] = "ltTocLastPage"
    JSON_NAME_LT_TOC_MIN_ENTRIES: ClassVar[str] = "ltTocMinEntries"

    JSON_NAME_NAME: ClassVar[str] = "name"
    JSON_NAME_NO_FONTS: ClassVar[str] = "noFonts"
    JSON_NAME_NO_LINES: ClassVar[str] = "noLines"
    JSON_NAME_NO_LINES_FOOTER: ClassVar[str] = "noLinesFooter"
    JSON_NAME_NO_LINES_HEADER: ClassVar[str] = "noLinesHeader"
    JSON_NAME_NO_LINES_TOC: ClassVar[str] = "noLinesToc"
    JSON_NAME_NO_LISTS_BULLET: ClassVar[str] = "noListsBullet"
    JSON_NAME_NO_LISTS_NUMBER: ClassVar[str] = "noListsNumber"
    JSON_NAME_NO_PAGES: ClassVar[str] = "noPages"
    JSON_NAME_NO_PARAS: ClassVar[str] = "noParas"
    JSON_NAME_NO_PDF_PAGES: ClassVar[str] = "noPDFPages"
    JSON_NAME_NO_TABLES: ClassVar[str] = "noTables"
    JSON_NAME_NO_WORDS: ClassVar[str] = "noWords"

    JSON_NAME_PAGE_NO: ClassVar[str] = "pageNo"
    JSON_NAME_PARAMS: ClassVar[str] = "params"
    JSON_NAME_PARA_NO: ClassVar[str] = "paraNo"
    JSON_NAME_PARA_NO_FIRST: ClassVar[str] = "paraNoFirst"
    JSON_NAME_PARA_NO_LAST: ClassVar[str] = "paraNoLast"
    JSON_NAME_PARA_NO_PAGE: ClassVar[str] = "paraNoPage"
    JSON_NAME_PARSER: ClassVar[str] = "parser"

    JSON_NAME_SIZE: ClassVar[str] = "size"

    JSON_NAME_SPACY_IGNORE_BRACKET: ClassVar[str] = "spacyIgnoreBracket"
    JSON_NAME_SPACY_IGNORE_LEFT_PUNCT: ClassVar[str] = "spacyIgnoreLeftPunct"
    JSON_NAME_SPACY_IGNORE_LINE_TYPE_FOOTER: ClassVar[str] = "spacyIgnoreLineTypeFooter"
    JSON_NAME_SPACY_IGNORE_LINE_TYPE_HEADER: ClassVar[str] = "spacyIgnoreLineTypeHeader"
    JSON_NAME_SPACY_IGNORE_LINE_TYPE_HEADING: ClassVar[str] = "spacyIgnoreLineTypeHeading"
    JSON_NAME_SPACY_IGNORE_LINE_TYPE_LIST_BULLET: ClassVar[str] = "spacyIgnoreLineTypeListBullet"
    JSON_NAME_SPACY_IGNORE_LINE_TYPE_LIST_NUMBER: ClassVar[str] = "spacyIgnoreLineTypeListNumber"
    JSON_NAME_SPACY_IGNORE_LINE_TYPE_TABLE: ClassVar[str] = "spacyIgnoreLineTypeTable"
    JSON_NAME_SPACY_IGNORE_LINE_TYPE_TOC: ClassVar[str] = "spacyIgnoreLineTypeToc"
    JSON_NAME_SPACY_IGNORE_PUNCT: ClassVar[str] = "spacyIgnorePunct"
    JSON_NAME_SPACY_IGNORE_QUOTE: ClassVar[str] = "spacyIgnoreQuote"
    JSON_NAME_SPACY_IGNORE_RIGHT_PUNCT: ClassVar[str] = "spacyIgnoreRightPunct"
    JSON_NAME_SPACY_IGNORE_SPACE: ClassVar[str] = "spacyIgnoreSpace"
    JSON_NAME_SPACY_IGNORE_STOP: ClassVar[str] = "spacyIgnoreStop"

    JSON_NAME_SPACY_TKN_CLUSTER: ClassVar[str] = "spacyTknCluster"
    JSON_NAME_SPACY_TKN_DEP_: ClassVar[str] = "spacyTknDep_"
    JSON_NAME_SPACY_TKN_DOC: ClassVar[str] = "spacyTknDoc"
    JSON_NAME_SPACY_TKN_ENT_IOB_: ClassVar[str] = "spacyTknEntIob_"
    JSON_NAME_SPACY_TKN_ENT_KB_ID_: ClassVar[str] = "spacyTknEntKbId_"
    JSON_NAME_SPACY_TKN_ENT_TYPE_: ClassVar[str] = "spacyTknEntType_"
    JSON_NAME_SPACY_TKN_HEAD: ClassVar[str] = "spacyTknHead"
    JSON_NAME_SPACY_TKN_I: ClassVar[str] = "spacyTknI"
    JSON_NAME_SPACY_TKN_IDX: ClassVar[str] = "spacyTknIdx"
    JSON_NAME_SPACY_TKN_IS_ALPHA: ClassVar[str] = "spacyTknIsAlpha"
    JSON_NAME_SPACY_TKN_IS_ASCII: ClassVar[str] = "spacyTknIsAscii"
    JSON_NAME_SPACY_TKN_IS_BRACKET: ClassVar[str] = "spacyTknIsBracket"
    JSON_NAME_SPACY_TKN_IS_CURRENCY: ClassVar[str] = "spacyTknIsCurrency"
    JSON_NAME_SPACY_TKN_IS_DIGIT: ClassVar[str] = "spacyTknIsDigit"
    JSON_NAME_SPACY_TKN_IS_LEFT_PUNCT: ClassVar[str] = "spacyTknIsLeftPunct"
    JSON_NAME_SPACY_TKN_IS_LOWER: ClassVar[str] = "spacyTknIsLower"
    JSON_NAME_SPACY_TKN_IS_OOV: ClassVar[str] = "spacyTknIsOov"
    JSON_NAME_SPACY_TKN_IS_PUNCT: ClassVar[str] = "spacyTknIsPunct"
    JSON_NAME_SPACY_TKN_IS_QUOTE: ClassVar[str] = "spacyTknIsQuot"
    JSON_NAME_SPACY_TKN_IS_RIGHT_PUNCT: ClassVar[str] = "spacyTknIsRightPunct"
    JSON_NAME_SPACY_TKN_IS_SENT_END: ClassVar[str] = "spacyTknIsSentEnd"
    JSON_NAME_SPACY_TKN_IS_SENT_START: ClassVar[str] = "spacyTknIsSentStart"
    JSON_NAME_SPACY_TKN_IS_SPACE: ClassVar[str] = "spacyTknIsSpace"
    JSON_NAME_SPACY_TKN_IS_STOP: ClassVar[str] = "spacyTknStop"
    JSON_NAME_SPACY_TKN_IS_TITLE: ClassVar[str] = "spacyTknIsTitle"
    JSON_NAME_SPACY_TKN_IS_UPPER: ClassVar[str] = "spacyTknIsUpper"
    JSON_NAME_SPACY_TKN_LANG_: ClassVar[str] = "spacyTknLang_"
    JSON_NAME_SPACY_TKN_LEFT_EDGE: ClassVar[str] = "spacyTknLeftEdge"
    JSON_NAME_SPACY_TKN_LEMMA_: ClassVar[str] = "spacyTknLemma_"
    JSON_NAME_SPACY_TKN_LEX: ClassVar[str] = "spacyTknLex"
    JSON_NAME_SPACY_TKN_LEX_ID: ClassVar[str] = "spacyTknLexId"
    JSON_NAME_SPACY_TKN_LIKE_EMAIL: ClassVar[str] = "spacyTknLikeEmail"
    JSON_NAME_SPACY_TKN_LIKE_NUM: ClassVar[str] = "spacyTknLikeNum"
    JSON_NAME_SPACY_TKN_LIKE_URL: ClassVar[str] = "spacyTknLikeUrl"
    JSON_NAME_SPACY_TKN_LOWER_: ClassVar[str] = "spacyTknLower_"
    JSON_NAME_SPACY_TKN_MORPH: ClassVar[str] = "spacyTknMorph"
    JSON_NAME_SPACY_TKN_NORM_: ClassVar[str] = "spacyTknNorm_"
    JSON_NAME_SPACY_TKN_ORTH_: ClassVar[str] = "spacyTknOrth_"
    JSON_NAME_SPACY_TKN_POS_: ClassVar[str] = "spacyTknPos_"
    JSON_NAME_SPACY_TKN_PREFIX_: ClassVar[str] = "spacyTknPrefix_"
    JSON_NAME_SPACY_TKN_PROB: ClassVar[str] = "spacyTknProb"
    JSON_NAME_SPACY_TKN_RANK: ClassVar[str] = "spacyTknRank"
    JSON_NAME_SPACY_TKN_RIGHT_EDGE: ClassVar[str] = "spacyTknRightEdge"
    JSON_NAME_SPACY_TKN_SENT: ClassVar[str] = "spacyTknSent"
    JSON_NAME_SPACY_TKN_SENTIMENT: ClassVar[str] = "spacyTknSentiment"
    JSON_NAME_SPACY_TKN_SHAPE_: ClassVar[str] = "spacyTknShape_"
    JSON_NAME_SPACY_TKN_SUFFIX_: ClassVar[str] = "spacyTknSuffix_"
    JSON_NAME_SPACY_TKN_TAG_: ClassVar[str] = "spacyTknTag_"
    JSON_NAME_SPACY_TKN_TENSOR: ClassVar[str] = "spacyTknTensor"
    JSON_NAME_SPACY_TKN_TEXT: ClassVar[str] = "spacyTknText"
    JSON_NAME_SPACY_TKN_TEXT_WITH_WS: ClassVar[str] = "spacyTknTextWithWs"
    JSON_NAME_SPACY_TKN_VOCAB: ClassVar[str] = "spacyTknVocab"
    JSON_NAME_SPACY_TKN_WHITESPACE_: ClassVar[str] = "spacyTknWhitespace_"

    JSON_NAME_TEXT: ClassVar[str] = "text"
    JSON_NAME_TOKENIZER: ClassVar[str] = "tokenizer"
    JSON_NAME_TYPE: ClassVar[str] = "type"

    JSON_NAME_URX: ClassVar[str] = "urx"

    JSON_NAME_WEIGHT: ClassVar[str] = "weight"
    JSON_NAME_WORD_NO: ClassVar[str] = "wordNo"
    JSON_NAME_WORD_NO_FIRST: ClassVar[str] = "wordNoFirst"
    JSON_NAME_WORD_NO_LAST: ClassVar[str] = "wordNoLast"
    JSON_NAME_WORD_NO_LINE: ClassVar[str] = "wordNoLine"
    JSON_NAME_WORD_NO_PAGE: ClassVar[str] = "wordNoPage"
    JSON_NAME_WORD_NO_PARA: ClassVar[str] = "wordNoPara"

    # wwe ======================= wwe #

    JSON_NAME_COLUMN: ClassVar[str] = "column"
    JSON_NAME_COLUMN_NO: ClassVar[str] = "columnNo"
    JSON_NAME_CONTAINER_COLUMNS: ClassVar[str] = "columns"
    JSON_NAME_CONTAINER_ENTRIES: ClassVar[str] = "entries"
    JSON_NAME_CONTAINER_LISTS: ClassVar[str] = "lists"
    JSON_NAME_CONTAINER_ROWS: ClassVar[str] = "rows"
    JSON_NAME_CONTAINER_SENTENCES: ClassVar[str] = "sentences"
    JSON_NAME_CONTAINER_TABLES: ClassVar[str] = "tables"
    JSON_NAME_CONTAINER_TITLES: ClassVar[str] = "titles"
    JSON_NAME_CTX_LINE_1: ClassVar[str] = "ctxLine1"
    JSON_NAME_CTX_LINE_2: ClassVar[str] = "ctxLine2"
    JSON_NAME_CTX_LINE_3: ClassVar[str] = "ctxLine3"
    JSON_NAME_DOCUMENT: ClassVar[str] = "document"
    JSON_NAME_ENTRY: ClassVar[str] = "entry"
    JSON_NAME_ENTRY_NO: ClassVar[str] = "entryNo"
    JSON_NAME_FORMAT: ClassVar[str] = "format"
    JSON_NAME_LEVEL: ClassVar[str] = "level"
    JSON_NAME_LINE: ClassVar[str] = "line"
    JSON_NAME_LINE_NO_PAGEFIRST: ClassVar[str] = "lineNoPageFirst"
    JSON_NAME_LINE_NO_PAGELAST: ClassVar[str] = "lineNoPageLast"
    JSON_NAME_LIST: ClassVar[str] = "list"
    JSON_NAME_LIST_NO: ClassVar[str] = "listNo"
    JSON_NAME_LISTS_BULLET: ClassVar[str] = "listsBullet"
    JSON_NAME_LISTS_NUMBER: ClassVar[str] = "listsNumber"
    JSON_NAME_LLX_FIRST_COLUMN: ClassVar[str] = "llxFirstColumn"
    JSON_NAME_LLX_FIRST_ROW: ClassVar[str] = "llxFirstRow"
    JSON_NAME_NO_COLUMNS: ClassVar[str] = "noColumns"
    JSON_NAME_NO_ENTRIES: ClassVar[str] = "noEntries"
    JSON_NAME_NO_ROWS: ClassVar[str] = "noRows"
    JSON_NAME_NO_SENTENCES: ClassVar[str] = "noSentences"
    JSON_NAME_NO_TITLES: ClassVar[str] = "noTitles"
    JSON_NAME_PAGE: ClassVar[str] = "page"
    JSON_NAME_PAGE_NO_FIRST: ClassVar[str] = "pageNoFirst"
    JSON_NAME_PAGE_NO_LAST: ClassVar[str] = "pageNoLast"
    JSON_NAME_PARA: ClassVar[str] = "para"
    JSON_NAME_REGEXP: ClassVar[str] = "regexp"
    JSON_NAME_ROW: ClassVar[str] = "row"
    JSON_NAME_ROW_NO: ClassVar[str] = "rowNo"
    JSON_NAME_SENTENCES: ClassVar[str] = "sentences"
    JSON_NAME_TABLE: ClassVar[str] = "table"
    JSON_NAME_TABLE_NO: ClassVar[str] = "tableNo"
    JSON_NAME_TABLES: ClassVar[str] = "tables"
    # wwe
    # JSON_NAME_TOKEN_CLUSTER: ClassVar[str] = "tknCluster"
    # JSON_NAME_TOKEN_DEP_: ClassVar[str] = "tknDep_"
    # JSON_NAME_TOKEN_DOC: ClassVar[str] = "tknDoc"
    # JSON_NAME_TOKEN_ENT_IOB_: ClassVar[str] = "tknEntIob_"
    # JSON_NAME_TOKEN_HEAD: ClassVar[str] = "tknHead"
    # JSON_NAME_TOKEN_I: ClassVar[str] = "tknI"
    # JSON_NAME_TOKEN__IDX: ClassVar[str] = "tknIdx"
    # JSON_NAME_TOKEN_IS_ALPHA: ClassVar[str] = "tknIsAlpha"
    # JSON_NAME_TOKEN_IS_ASCII: ClassVar[str] = "tknIsAscii"
    # JSON_NAME_TOKEN_IS_OOV: ClassVar[str] = "tknIsOov"
    # JSON_NAME_TOKEN_IS_SENT_START: ClassVar[str] = "tknIsSentStart"
    # JSON_NAME_TOKEN_IS_TITLE: ClassVar[str] = "tknIsTitle"
    # JSON_NAME_TOKEN_LANG_: ClassVar[str] = "tknLang_"
    # JSON_NAME_TOKEN_LEFT_EDGE: ClassVar[str] = "tknLeftEdge"
    # JSON_NAME_TOKEN_LEMMA_: ClassVar[str] = "tknLemma_"
    # JSON_NAME_TOKEN_LEX: ClassVar[str] = "tknLex"
    # JSON_NAME_TOKEN_LEX_ID: ClassVar[str] = "tknLexId"
    # JSON_NAME_TOKEN_LOWER_: ClassVar[str] = "tknLower_"
    # JSON_NAME_TOKEN_MORPH: ClassVar[str] = "tknMorph"
    # JSON_NAME_TOKEN__NORM_: ClassVar[str] = "tknNorm_"
    # JSON_NAME_TOKEN_ORTH_: ClassVar[str] = "tknOrth_"
    # JSON_NAME_TOKEN_POS_: ClassVar[str] = "tknPos_"
    # JSON_NAME_TOKEN_PREFIX_: ClassVar[str] = "tknPrefix_"
    # JSON_NAME_TOKEN_PROB: ClassVar[str] = "tknProb"
    # JSON_NAME_TOKEN_RANK: ClassVar[str] = "tknRank"
    # JSON_NAME_TOKEN_RIGHTEDGE: ClassVar[str] = "tknRightEdge"
    # JSON_NAME_TOKEN_SENT: ClassVar[str] = "tknSent"
    # JSON_NAME_TOKEN_SENTIMENT: ClassVar[str] = "tknSentiment"
    # JSON_NAME_TOKEN_SHAPE_: ClassVar[str] = "tknShape_"
    # JSON_NAME_TOKEN_SUFFIX_: ClassVar[str] = "tknSuffix_"
    # JSON_NAME_TOKEN_TAG_: ClassVar[str] = "tknTag_"
    # JSON_NAME_TOKEN_TEXT: ClassVar[str] = "tknText"
    # JSON_NAME_TOKEN_TEXTWITHWS: ClassVar[str] = "tknTextWithWs"
    # JSON_NAME_TOKEN_VOCAB: ClassVar[str] = "tknVocab"
    # JSON_NAME_TOKEN_WHITESPACE_: ClassVar[str] = "tknWhitespace_"
    JSON_NAME_TOC: ClassVar[str] = "toc"
    JSON_NAME_URX_FIRST_COLUMN: ClassVar[str] = "urxFirstColumn"
    JSON_NAME_URX_FIRST_ROW: ClassVar[str] = "urxFirstRow"
    JSON_NAME_WORD: ClassVar[str] = "word"

    JSON_NAME_BULLET: ClassVar[str] = "bullet"

    JSON_NAME_COLUMNS: ClassVar[str] = "columns"
    JSON_NAME_COLUMN_SPAN: ClassVar[str] = "columnSpan"
    JSON_NAME_COORD_LLX: ClassVar[str] = "coordLLX"
    JSON_NAME_COORD_URX: ClassVar[str] = "coordURX"

    JSON_NAME_ENTRIES: ClassVar[str] = "entries"

    JSON_NAME_FIRST_COLUMN_LLX: ClassVar[str] = "firstColumnLLX"
    JSON_NAME_FIRST_ENTRY_LLX: ClassVar[str] = "firstEntryLLX"
    JSON_NAME_FIRST_ROW_LLX: ClassVar[str] = "firstRowLLX"
    JSON_NAME_FIRST_ROW_URX: ClassVar[str] = "firstRowURX"
    JSON_NAME_FUNCTION_IS_ASC: ClassVar[str] = "functionIsAsc"

    JSON_NAME_GLYPH_FONT: ClassVar[str] = "font"
    JSON_NAME_GLYPH_FONT_SIZE: ClassVar[str] = "fontSize"

    JSON_NAME_HEADING_CTX_LINE: ClassVar[str] = "headingCtxLine"
    JSON_NAME_HEADING_LEVEL: ClassVar[str] = "headingLevel"
    JSON_NAME_HEADING_TEXT: ClassVar[str] = "headingText"

    JSON_NAME_IS_FIRST_TOKEN: ClassVar[str] = "isFirstToken"

    JSON_NAME_LAST_COLUMN_URX: ClassVar[str] = "lastColumnURX"
    JSON_NAME_LINES: ClassVar[str] = "lines"
    JSON_NAME_LINE_NO_PAGE_FROM: ClassVar[str] = "lineNoPageFrom"
    JSON_NAME_LINE_NO_PAGE_TILL: ClassVar[str] = "lineNoPageTill"
    JSON_NAME_LINE_TYPE: ClassVar[str] = "lineType"
    JSON_NAME_LINE_TYPE_ANTI_PATTERNS: ClassVar[str] = "lineTypeAntiPatterns"
    JSON_NAME_LINE_TYPE_RULES: ClassVar[str] = "lineTypeRules"

    JSON_NAME_NO_LINES_IN_DOC: ClassVar[str] = "noLinesInDocument"
    JSON_NAME_NO_LINES_IN_PAGE: ClassVar[str] = "noLinesInPage"
    JSON_NAME_NO_LINES_IN_PARA: ClassVar[str] = "noLinesInParagraph"
    JSON_NAME_NO_LISTS_BULLET_IN_DOC: ClassVar[str] = "noListsBulletInDocument"
    JSON_NAME_NO_LISTS_NUMBER_IN_DOC: ClassVar[str] = "noListsNumberInDocument"
    JSON_NAME_NO_PAGES_IN_DOC: ClassVar[str] = "noPagesInDocument"
    JSON_NAME_NO_PARAS_IN_DOC: ClassVar[str] = "noParagraphsInDocument"
    JSON_NAME_NO_PARAS_IN_PAGE: ClassVar[str] = "noParagraphsInPage"
    JSON_NAME_NO_SENTS_IN_DOC: ClassVar[str] = "noSentencesInDocument"
    JSON_NAME_NO_SENTS_IN_PAGE: ClassVar[str] = "noSentencesInPage"
    JSON_NAME_NO_SENTS_IN_PARA: ClassVar[str] = "noSentencesInParagraph"
    JSON_NAME_NO_TABLES_IN_DOC: ClassVar[str] = "noTablesInDocument"
    JSON_NAME_NO_TITLES_IN_DOC: ClassVar[str] = "noTitlesInDocument"
    JSON_NAME_NO_TOKENS_IN_DOC: ClassVar[str] = "noTokensInDocument"
    JSON_NAME_NO_TOKENS_IN_PAGE: ClassVar[str] = "noTokensInPage"
    JSON_NAME_NO_TOKENS_IN_PARA: ClassVar[str] = "noTokensInParagraph"
    JSON_NAME_NO_TOKENS_IN_SENT: ClassVar[str] = "noTokensInSentence"
    JSON_NAME_NO_WORDS_IN_DOC: ClassVar[str] = "noWordsInDocument"
    JSON_NAME_NO_WORDS_IN_LINE: ClassVar[str] = "noWordsInLine"
    JSON_NAME_NO_WORDS_IN_PAGE: ClassVar[str] = "noWordsInPage"
    JSON_NAME_NO_WORDS_IN_PARA: ClassVar[str] = "noWordsInParagraph"
    JSON_NAME_NUMBER: ClassVar[str] = "number"

    JSON_NAME_PAGES: ClassVar[str] = "pages"
    JSON_NAME_PAGE_NO_FROM: ClassVar[str] = "pageNoFrom"
    JSON_NAME_PAGE_NO_TILL: ClassVar[str] = "pageNoTill"
    JSON_NAME_PARAS: ClassVar[str] = "paragraphs"

    JSON_NAME_ROWS: ClassVar[str] = "rows"

    JSON_NAME_SENTS: ClassVar[str] = "sentences"
    JSON_NAME_SENT_NO: ClassVar[str] = "sentenceNo"
    JSON_NAME_START_VALUES: ClassVar[str] = "startValues"

    JSON_NAME_TITLES: ClassVar[str] = "titles"
    JSON_NAME_TOKENS: ClassVar[str] = "tokens"

    JSON_NAME_TOKEN_ENT_KB_ID_: ClassVar[str] = "tknEntKbId_"
    JSON_NAME_TOKEN_ENT_TYPE_: ClassVar[str] = "tknEntType_"
    JSON_NAME_TOKEN_IDX: ClassVar[str] = "tknIdx"
    JSON_NAME_TOKEN_IS_BRACKET: ClassVar[str] = "tknIsBracket"
    JSON_NAME_TOKEN_IS_CURRENCY: ClassVar[str] = "tknIsCurrency"
    JSON_NAME_TOKEN_IS_DIGIT: ClassVar[str] = "tknIsDigit"
    JSON_NAME_TOKEN_IS_LEFT_PUNCT: ClassVar[str] = "tknIsLeftPunct"
    JSON_NAME_TOKEN_IS_LOWER: ClassVar[str] = "tknIsLower"
    JSON_NAME_TOKEN_IS_PUNCT: ClassVar[str] = "tknIsPunct"
    JSON_NAME_TOKEN_IS_QUOTE: ClassVar[str] = "tknIsQuote"
    JSON_NAME_TOKEN_IS_RIGHT_PUNCT: ClassVar[str] = "tknIsRightPunct"
    JSON_NAME_TOKEN_IS_SENT_END: ClassVar[str] = "tknIsSentEnd"
    JSON_NAME_TOKEN_IS_SPACE: ClassVar[str] = "tknIsSpace"
    JSON_NAME_TOKEN_IS_STOP: ClassVar[str] = "tknIsStop"
    JSON_NAME_TOKEN_IS_UPPER: ClassVar[str] = "tknIsUpper"
    JSON_NAME_TOKEN_LIKE_EMAIL: ClassVar[str] = "tknLikeEmail"
    JSON_NAME_TOKEN_LIKE_NUM: ClassVar[str] = "tknLikeNum"
    JSON_NAME_TOKEN_LIKE_URL: ClassVar[str] = "tknLikeUrl"
    JSON_NAME_TOKEN_NORM_: ClassVar[str] = "tknNorm_"
    JSON_NAME_TOKEN_RIGHT_EDGE: ClassVar[str] = "tknRightEdge"
    JSON_NAME_TOKEN_TENSOR: ClassVar[str] = "tknTensor"
    JSON_NAME_TOKEN_TEXT_WITH_WS: ClassVar[str] = "tknTextWithWs"

    JSON_NAME_UPPER_RIGHT_X: ClassVar[str] = "upperRightX"

    JSON_NAME_WORDS: ClassVar[str] = "words"

    LANGUAGE_PANDOC_DEFAULT: ClassVar[str] = "en"
    LANGUAGE_SPACY_DEFAULT: ClassVar[str] = "en_core_web_trf"
    LANGUAGE_TESSERACT_DEFAULT: ClassVar[str] = "eng"

    LINE_TET_DOCUMENT_OPT_LIST: ClassVar[str] = "engines={noannotation noimage text notextcolor novector}"
    LINE_TET_PAGE_OPT_LIST: ClassVar[str] = "granularity=line"
    LINE_XML_VARIATION: ClassVar[str] = "line."

    LINE_TYPE_BODY: ClassVar[str] = "b"
    LINE_TYPE_FOOTER: ClassVar[str] = "f"
    LINE_TYPE_HEADER: ClassVar[str] = "h"
    LINE_TYPE_HEADING: ClassVar[str] = "h_"
    LINE_TYPE_LIST_BULLET: ClassVar[str] = "lb"
    LINE_TYPE_LIST_NUMBER: ClassVar[str] = "ln"
    LINE_TYPE_TABLE: ClassVar[str] = "tab"
    LINE_TYPE_TOC: ClassVar[str] = "toc"

    LOGGER_PROGRESS_UPDATE: ClassVar[str] = "Progress update "

    PARSE_ATTR_COL_SPAN: ClassVar[str] = "colSpan"
    PARSE_ATTR_EMBEDDED: ClassVar[str] = "embedded"
    PARSE_ATTR_FULL_NAME: ClassVar[str] = "fullname"
    PARSE_ATTR_ID: ClassVar[str] = "id"
    PARSE_ATTR_ITALIC_ANGLE: ClassVar[str] = "italicangle"
    PARSE_ATTR_LLX: ClassVar[str] = "llx"
    PARSE_ATTR_NAME: ClassVar[str] = "name"
    PARSE_ATTR_TYPE: ClassVar[str] = "type"
    PARSE_ATTR_URX: ClassVar[str] = "urx"
    PARSE_ATTR_WEIGHT: ClassVar[str] = "weight"
    PARSE_ATTR_GLYPH_FONT: ClassVar[str] = "font"
    PARSE_ATTR_GLYPH_SIZE: ClassVar[str] = "size"

    PARSE_NAME_SPACE: ClassVar[str] = "{http://www.pdflib.com/XML/TET5/TET-5.0}"

    PARSE_ELEM_A: ClassVar[str] = "A"
    PARSE_ELEM_ACTION: ClassVar[str] = "Action"
    PARSE_ELEM_ANNOTATIONS: ClassVar[str] = "Annotations"
    PARSE_ELEM_ATTACHMENTS: ClassVar[str] = "Attachments"
    PARSE_ELEM_AUTHOR: ClassVar[str] = "Author"
    PARSE_ELEM_BOOKMARK: ClassVar[str] = "Bookmark"
    PARSE_ELEM_BOOKMARKS: ClassVar[str] = "Bookmarks"
    PARSE_ELEM_BOX: ClassVar[str] = "Box"
    PARSE_ELEM_CELL: ClassVar[str] = "Cell"
    PARSE_ELEM_COLOR_SPACES: ClassVar[str] = "ColorSpaces"
    PARSE_ELEM_CONTENT: ClassVar[str] = "Content"
    PARSE_ELEM_CREATION: ClassVar[str] = "Creation"
    PARSE_ELEM_CREATION_DATE: ClassVar[str] = "CreationDate"
    PARSE_ELEM_CREATOR: ClassVar[str] = "Creator"
    PARSE_ELEM_CUSTOM: ClassVar[str] = "Custom"
    PARSE_ELEM_CUSTOM_BINARY: ClassVar[str] = "CustomBinary"
    PARSE_ELEM_DESTINATIONS: ClassVar[str] = "Destinations"
    PARSE_ELEM_DOC_INFO: ClassVar[str] = "DocInfo"
    PARSE_ELEM_DOCUMENT: ClassVar[str] = "Document"
    PARSE_ELEM_ENCRYPTION: ClassVar[str] = "Encryption"
    PARSE_ELEM_EXCEPTION: ClassVar[str] = "Exception"
    PARSE_ELEM_FIELDS: ClassVar[str] = "Fields"
    PARSE_ELEM_FONT: ClassVar[str] = "Font"
    PARSE_ELEM_FONTS: ClassVar[str] = "Fonts"
    PARSE_ELEM_FROM: ClassVar[int] = len(PARSE_NAME_SPACE)
    PARSE_ELEM_GLYPH: ClassVar[str] = "Glyph"
    PARSE_ELEM_GRAPHICS: ClassVar[str] = "Graphics"
    PARSE_ELEM_GTS_PDFX_CONFORMANCE: ClassVar[str] = "GTS_PDFXConformance"
    PARSE_ELEM_GTS_PDFX_VERSION: ClassVar[str] = "GTS_PDFXVersion"
    PARSE_ELEM_GTS_PPMLVDX_CONFORMANCE: ClassVar[str] = "GTS_PPMLVDXConformance"
    PARSE_ELEM_GTS_PPMLVDX_VERSION: ClassVar[str] = "GTS_PPMLVDXVersion"
    PARSE_ELEM_ISO_PDFE_VERSION: ClassVar[str] = "ISO_PDFEVersion"
    PARSE_ELEM_JAVA_SCRIPTS: ClassVar[str] = "JavaScripts"
    PARSE_ELEM_KEYWORDS: ClassVar[str] = "Keywords"
    PARSE_ELEM_LINE: ClassVar[str] = "Line"
    PARSE_ELEM_METADATA: ClassVar[str] = "Metadata"
    PARSE_ELEM_MOD_DATE: ClassVar[str] = "ModDate"
    PARSE_ELEM_OPTIONS: ClassVar[str] = "Options"
    PARSE_ELEM_OUTPUT_INTENTS: ClassVar[str] = "OutputIntents"
    PARSE_ELEM_PAGE: ClassVar[str] = "Page"
    PARSE_ELEM_PAGES: ClassVar[str] = "Pages"
    PARSE_ELEM_PARA: ClassVar[str] = "Para"
    PARSE_ELEM_PLACED_IMAGE: ClassVar[str] = "PlacedImage"
    PARSE_ELEM_PRODUCER: ClassVar[str] = "Producer"
    PARSE_ELEM_RESOURCES: ClassVar[str] = "Resources"
    PARSE_ELEM_ROW: ClassVar[str] = "Row"
    PARSE_ELEM_SIGNATURE_FIELDS: ClassVar[str] = "SignatureFields"
    PARSE_ELEM_SUBJECT: ClassVar[str] = "Subject"
    PARSE_ELEM_TABLE: ClassVar[str] = "Table"
    PARSE_ELEM_TEXT: ClassVar[str] = "Text"
    PARSE_ELEM_TITLE: ClassVar[str] = "Title"
    PARSE_ELEM_TRAPPED: ClassVar[str] = "Trapped"
    PARSE_ELEM_WORD: ClassVar[str] = "Word"
    PARSE_ELEM_XFA: ClassVar[str] = "XFA"

    SEARCH_STRATEGY_LINES: ClassVar[str] = "lines"
    SEARCH_STRATEGY_TABLE: ClassVar[str] = "table"

    TETML_TYPE_LINE: ClassVar[str] = "line"
    TETML_TYPE_PAGE: ClassVar[str] = "page"
    TETML_TYPE_WORD: ClassVar[str] = "word"

    WORD_TET_DOCUMENT_OPT_LIST: ClassVar[str] = "engines={noannotation noimage text notextcolor novector}"
    WORD_TET_PAGE_OPT_LIST: ClassVar[str] = "granularity=word tetml={glyphdetails={all} elements={line}}"
    WORD_XML_VARIATION: ClassVar[str] = "word."

    # ------------------------------------------------------------------
    # Initialise the instance.
    # ------------------------------------------------------------------
    def __init__(self) -> None:
        """Initialise the instance."""
        try:
            core_glob.logger.debug(core_glob.LOGGER_START)
        except AttributeError:
            core_glob.initialise_logger()
            core_glob.logger.debug(core_glob.LOGGER_START)

        self._exist = True

        self.document_json: dict[str, bool | int | list[NLPCore.PageJSON] | str] = {}

        core_glob.logger.debug(core_glob.LOGGER_END)

    # ------------------------------------------------------------------
    # Convert a roman numeral to integer.
    # ------------------------------------------------------------------
    @classmethod
    def _convert_roman_2_int(cls, roman: str) -> int:
        """Convert a roman numeral to integer.

        Args:
            roman (str): The roman numeral.

        Returns:
            int: The corresponding integer.
        """
        roman_int = re.match(  # type: ignore
            "(m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3}))" + "|(M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))",
            roman,
        ).group(0)

        tallies = {
            "i": 1,
            "v": 5,
            "x": 10,
            "l": 50,
            "c": 100,
            "d": 500,
            "m": 1000,
            # specify more numerals if you wish
        }

        integer: int = 0

        for i in range(len(roman_int) - 1):
            left = roman_int[i]
            right = roman_int[i + 1]
            if tallies[left] < tallies[right]:
                integer -= tallies[left]
            else:
                integer += tallies[left]

        integer += tallies[roman_int[-1]]

        return integer

    # ------------------------------------------------------------------
    # Get the default heading line type anti-patterns.
    # ------------------------------------------------------------------
    # 1: rule_name
    # 2: regexp_str:
    #           regular expression
    # ------------------------------------------------------------------
    @staticmethod
    def _get_lt_anti_patterns_default_heading() -> list[tuple[str, str]]:
        """Get the default heading line type anti-patterns.

        Returns:
            list[tuple[str, str]]: The heading line type anti-patterns.
        """
        return [
            ("9 AAA aaa", r"^\d+[ ][A-Z]+ [A-Z][a-z]+"),
            ("A A ", r"^[A-Z] [A-Z] "),
            ("A AAA Aaa", r"^[A-Z][ ]+[A-Z]+ [A-Z]*[a-z]+"),
            ("a) * a)", r"^[a-z]{1}\) [a-z A-Z0-9\.!\?]* [a-z]{1}\)"),
        ]

    # ------------------------------------------------------------------
    # Get the default bulleted list line type anti-patterns.
    # ------------------------------------------------------------------
    # 1: rule_name
    # 2: regexp_str:
    #           regular expression
    # ------------------------------------------------------------------
    @staticmethod
    def _get_lt_anti_patterns_default_list_bullet(environment_variant: str) -> list[tuple[str, str]]:
        """Get the default bulleted list line type anti-patterns.

        Returns:
            list[tuple[str, str]]: The bulleted list line type anti-patterns.
        """
        if environment_variant == NLPCore.ENVIRONMENT_TYPE_TEST:
            return [
                ("n/a", r"^_n/a_$"),
            ]

        return []

    # ------------------------------------------------------------------
    # Get the default numbered list line type anti-patterns.
    # ------------------------------------------------------------------
    # 1: rule_name
    # 2: regexp_str:
    #           regular expression
    # ------------------------------------------------------------------
    @staticmethod
    def _get_lt_anti_patterns_default_list_number(environment_variant: str) -> list[tuple[str, str]]:
        """Get the default numbered list line type anti-patterns.

        Args:
            environment_variant (str): Environment variant: dev, prod or test.

        Returns:
            list[tuple[str, str]]: The numbered list line type anti-patterns.
        """
        if environment_variant == NLPCore.ENVIRONMENT_TYPE_TEST:
            return [
                ("n/a", r"^_n/a_$"),
            ]

        return []

    # ------------------------------------------------------------------
    # Get the default heading & numbered list line type rules.
    # ------------------------------------------------------------------
    # 1: rule_name
    # 2: is_first_token:
    #           True:  apply rule to first token (split)
    #           False: apply rule to beginning of line
    # 3: regexp_str:
    #           regular expression
    # 4: function_is_asc:
    #           compares predecessor and successor
    # 5: start_values:
    #           list of strings
    # ------------------------------------------------------------------
    @staticmethod
    def _get_lt_rules_default_heading_list_number() -> list[tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str]]]:
        """Get the default heading & numbered list line type rules.

        Returns:
            list[tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str]]]: The
                heading & numbered list line type rules.
        """
        return [
            (
                "(999)",
                True,
                r"\(\d+\)$",
                NLPCore.is_asc_string_integers,
                ["(1)"],
            ),
            (
                "(A)",
                True,
                r"\([A-Z]\)$",
                NLPCore.is_asc_uppercase_letters,
                ["(A)"],
            ),
            (
                "(ROM)",
                True,
                r"\(M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\)$",
                NLPCore.is_asc_romans,
                ["(I)"],
            ),
            (
                "(a)",
                True,
                r"\([a-z]\)$",
                NLPCore.is_asc_lowercase_letters,
                ["(a)"],
            ),
            (
                "(rom)",
                True,
                r"\(m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})\)$",
                NLPCore.is_asc_romans,
                ["(i)"],
            ),
            (
                "[999]",
                True,
                r"\[\d+\]$",
                NLPCore.is_asc_string_integers,
                ["[1]"],
            ),
            (
                "[A]",
                True,
                r"\[[A-Z]\]$",
                NLPCore.is_asc_uppercase_letters,
                ["[A]"],
            ),
            (
                "[ROM]",
                True,
                r"\[M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\]$",
                NLPCore.is_asc_romans,
                ["[I]"],
            ),
            (
                "[a]",
                True,
                r"\[[a-z]\]$",
                NLPCore.is_asc_lowercase_letters,
                ["[a]"],
            ),
            (
                "[rom]",
                True,
                r"\[m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})\]$",
                NLPCore.is_asc_romans,
                ["[i]"],
            ),
            (
                "999)",
                True,
                r"\d+\)$",
                NLPCore.is_asc_string_integers,
                ["1)"],
            ),
            (
                "999.",
                False,
                r"\d+\.",
                NLPCore.is_asc_string_integers,
                ["1."],
            ),
            (
                "999.999",
                True,
                r"\d+\.\d{1,3}$",
                NLPCore.is_asc_string_floats,
                ["0.0", "0.1", "0.01", "0.001"],
            ),
            (
                "A)",
                True,
                r"[A-Z]\)$",
                NLPCore.is_asc_uppercase_letters,
                ["A)"],
            ),
            (
                "A.",
                False,
                r"[A-Z]\.",
                NLPCore.is_asc_uppercase_letters,
                ["A."],
            ),
            (
                "ROM)",
                True,
                r"M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\)$",
                NLPCore.is_asc_romans,
                ["I)"],
            ),
            (
                "ROM.",
                False,
                r"M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\.",
                NLPCore.is_asc_romans,
                ["I."],
            ),
            (
                "a)",
                True,
                r"[a-z]\)$",
                NLPCore.is_asc_lowercase_letters,
                ["a)"],
            ),
            (
                "a.",
                False,
                r"[a-z]\.",
                NLPCore.is_asc_lowercase_letters,
                ["a."],
            ),
            (
                "rom)",
                True,
                r"m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})\)$",
                NLPCore.is_asc_romans,
                ["i)"],
            ),
            (
                "rom.",
                False,
                r"m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})\.",
                NLPCore.is_asc_romans,
                ["i."],
            ),
            (
                "999",
                False,
                r"\d+[ ]+[A-Z][a-zA-Z]+",
                NLPCore.is_asc_string_integers_token,
                ["1 "],
            ),
            (
                "A",
                False,
                r"[A-Z][ ]+[A-Z][a-zA-Z]+",
                NLPCore.is_asc_uppercase_letters_token,
                ["A "],
            ),
            (
                "ROM",
                False,
                r"M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})[ ]+[A-Z][a-zA-Z]+",
                NLPCore.is_asc_romans_token,
                ["I "],
            ),
            (
                "a",
                False,
                r"[a-z][ ]+[A-Z][a-zA-Z]+",
                NLPCore.is_asc_lowercase_letters_token,
                ["a "],
            ),
            (
                "rom",
                False,
                r"m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})[ ]+[A-Z][a-zA-Z]+",
                NLPCore.is_asc_romans_token,
                ["i "],
            ),
        ]

    # ------------------------------------------------------------------
    # Get the default bulleted list line type rules.
    # ------------------------------------------------------------------
    # 1: bullet character(s)
    # ------------------------------------------------------------------
    @staticmethod
    def _get_lt_rules_default_list_bullet() -> dict[str, int]:
        """Get the default bulleted list line type rules.

        Returns:
            dict[str, int]: The bulleted list line type rules.
        """
        return {
            "\u002D": 0,
            "\u002E": 0,
            "\u006F": 0,
            "\u00B0": 0,
            "\u00B7": 0,
            "\u00BA": 0,
            "\u2022": 0,
            "\u2023": 0,
            "\u2043": 0,
            "\u204C": 0,
            "\u204D": 0,
            "\u2218": 0,
            "\u2219": 0,
            "\u22C4": 0,
            "\u22C5": 0,
            "\u22C6": 0,
            "\u25CB": 0,
            "\u25CF": 0,
            "\u25D8": 0,
            "\u25E6": 0,
            "\u2605": 0,
            "\u2606": 0,
            "\u2609": 0,
            "\u2619": 0,
            "\u2662": 0,
            "\u2666": 0,
            "\u26AC": 0,
            "\u26B9": 0,
            "\u2765": 0,
            "\u2767": 0,
            "\u29BE": 0,
            "\u29BF": 0,
        }

    # ------------------------------------------------------------------
    # Check the object existence.
    # ------------------------------------------------------------------
    def exists(self) -> bool:
        """Check the object existence.

        Returns: bool: Always true.
        """
        return self._exist

    # ------------------------------------------------------------------
    # Export the default heading line type rules.
    # ------------------------------------------------------------------
    @staticmethod
    def export_rule_file_heading(is_verbose: bool, file_name: str, file_encoding: str, json_indent: int, is_json_sort_keys: bool) -> None:
        """Export the default heading line type rules.

        Args:
            is_verbose (bool): If true, processing results are reported.
            file_name (str): File name of the output file.
            file_encoding (str): The encoding of the output file.
            json_indent (int): Indent level for pretty-printing the JSON output.
            is_json_sort_keys (bool): If true,
                the output of the JSON dictionaries will be sorted by key.
        """
        anti_patterns = []

        for name, regexp in NLPCore.get_lt_anti_patterns_default_heading():
            anti_patterns.append(
                {
                    NLPCore.JSON_NAME_NAME: name,
                    NLPCore.JSON_NAME_REGEXP: regexp,
                }
            )

        rules = []

        for name, is_first_token, regexp, function_is_asc, start_values in NLPCore.get_lt_rules_default_heading():
            rules.append(
                {
                    NLPCore.JSON_NAME_NAME: name,
                    NLPCore.JSON_NAME_IS_FIRST_TOKEN: is_first_token,
                    NLPCore.JSON_NAME_REGEXP: regexp,
                    NLPCore.JSON_NAME_FUNCTION_IS_ASC: function_is_asc.__qualname__[15:],
                    NLPCore.JSON_NAME_START_VALUES: start_values,
                }
            )

        with open(file_name, "w", encoding=file_encoding) as file_handle:
            json.dump(
                {
                    NLPCore.JSON_NAME_LINE_TYPE_ANTI_PATTERNS: anti_patterns,
                    NLPCore.JSON_NAME_LINE_TYPE_RULES: rules,
                },
                file_handle,
                indent=int(json_indent),
                sort_keys=is_json_sort_keys,
            )

        if len(anti_patterns) > 0:
            core_utils.progress_msg(is_verbose, f"{len(anti_patterns):3d} heading       line type anti-pattern(s) exported")
        if len(rules) > 0:
            core_utils.progress_msg(is_verbose, f"{len(rules):3d} heading       line type rule(s)         exported")

    # ------------------------------------------------------------------
    # Export the default bulleted list line type rules.
    # ------------------------------------------------------------------
    @staticmethod
    def export_rule_file_list_bullet(
        is_verbose: bool,
        file_name: str,
        file_encoding: str,
        json_indent: str,
        is_json_sort_keys: bool,
        environment_variant: str,
    ) -> None:
        """Export the default bulleted list line type rules.

        Args:
            is_verbose (bool): If true, processing results are reported.
            file_name (str): File name of the output file.
            file_encoding (str): The encoding of the output file.
            json_indent (str): Indent level for pretty-printing the JSON output.
            is_json_sort_keys (bool): If true,
                the output of the JSON dictionaries will be sorted by key.
            environment_variant (str): Environment variant: dev, prod or test.
        """
        anti_patterns = []

        for name, regexp in NLPCore.get_lt_anti_patterns_default_list_bullet(environment_variant):
            anti_patterns.append(
                {
                    NLPCore.JSON_NAME_NAME: name,
                    NLPCore.JSON_NAME_REGEXP: regexp,
                }
            )

        rules = []

        for rule in NLPCore.get_lt_rules_default_list_bullet():
            rules.append(rule)

        with open(file_name, "w", encoding=file_encoding) as file_handle:
            json.dump(
                {
                    NLPCore.JSON_NAME_LINE_TYPE_ANTI_PATTERNS: anti_patterns,
                    NLPCore.JSON_NAME_LINE_TYPE_RULES: rules,
                },
                file_handle,
                indent=int(json_indent),
                sort_keys=is_json_sort_keys,
            )

        if len(anti_patterns) > 0:
            core_utils.progress_msg(is_verbose, f"{len(anti_patterns):3d} bulleted list line type anti-pattern(s) exported")
        if len(rules) > 0:
            core_utils.progress_msg(is_verbose, f"{len(rules):3d} bulleted list line type rule(s)         exported")

    # ------------------------------------------------------------------
    # Export the default numbered list line type rules.
    # ------------------------------------------------------------------
    @staticmethod
    def export_rule_file_list_number(
        is_verbose: bool,
        file_name: str,
        file_encoding: str,
        json_indent: str,
        is_json_sort_keys: bool,
        environment_variant: str,
    ) -> None:
        """Export the default numbered list line type rules.

        Args:
            is_verbose (bool): If true, processing results are reported.
            file_name (str, optional): File name of the output file.
            file_encoding (str): The encoding of the output file.
            json_indent (str): Indent level for pretty-printing the JSON output.
            is_json_sort_keys (bool): If true,
                the output of the JSON dictionaries will be sorted by key.
            environment_variant (str): Environment variant: dev, prod or test.
        """
        anti_patterns = []

        for name, regexp in NLPCore.get_lt_anti_patterns_default_list_number(environment_variant):
            anti_patterns.append(
                {
                    NLPCore.JSON_NAME_NAME: name,
                    NLPCore.JSON_NAME_REGEXP: regexp,
                }
            )

        rules = []

        for name, regexp, function_is_asc, start_values in NLPCore.get_lt_rules_default_list_number():
            rules.append(
                {
                    NLPCore.JSON_NAME_NAME: name,
                    NLPCore.JSON_NAME_REGEXP: regexp,
                    NLPCore.JSON_NAME_FUNCTION_IS_ASC: function_is_asc.__qualname__[15:],
                    NLPCore.JSON_NAME_START_VALUES: start_values,
                }
            )

        with open(file_name, "w", encoding=file_encoding) as file_handle:
            json.dump(
                {
                    NLPCore.JSON_NAME_LINE_TYPE_ANTI_PATTERNS: anti_patterns,
                    NLPCore.JSON_NAME_LINE_TYPE_RULES: rules,
                },
                file_handle,
                indent=int(json_indent),
                sort_keys=is_json_sort_keys,
            )

        if len(anti_patterns) > 0:
            core_utils.progress_msg(is_verbose, f"{len(anti_patterns):3d} numbered list line type anti-pattern(s) exported")
        if len(rules) > 0:
            core_utils.progress_msg(is_verbose, f"{len(rules):3d} numbered list line type rule(s)         exported")

    # ------------------------------------------------------------------
    # Get the default heading line type anti-patterns.
    # ------------------------------------------------------------------
    @staticmethod
    def get_lt_anti_patterns_default_heading() -> list[
        tuple[
            str,
            str,
        ]
    ]:
        """Get the default heading line type anti-patterns.

        Returns:
            list[tuple[str, str,]]: The heading line type anti-patterns.
        """
        return NLPCore._get_lt_anti_patterns_default_heading()

    # ------------------------------------------------------------------
    # Get the default bulleted list line type anti-patterns.
    # ------------------------------------------------------------------
    @staticmethod
    def get_lt_anti_patterns_default_list_bullet(
        environment_variant: str,
    ) -> list[tuple[str, str]]:
        """Get the default bulleted list line type anti-patterns.

        Args:
            environment_variant (str): Environment variant: dev, prod or test.

        Returns:
            list[tuple[str, str]]: The bulleted list line type anti-patterns.
        """
        return NLPCore._get_lt_anti_patterns_default_list_bullet(environment_variant)

    # ------------------------------------------------------------------
    # Get the default numbered list line type anti-patterns.
    # ------------------------------------------------------------------
    @staticmethod
    def get_lt_anti_patterns_default_list_number(environment_variant: str) -> list[tuple[str, str]]:
        """Get the default numbered list line type anti-patterns.

        Args:
            environment_variant (str): Environment variant: dev, prod or test.

        Returns:
            list[tuple[str, str]]: The numbered list line type anti-patterns.
        """
        return NLPCore._get_lt_anti_patterns_default_list_number(environment_variant)

    # ------------------------------------------------------------------
    # Get the default heading line type rules.
    # ------------------------------------------------------------------
    @staticmethod
    def get_lt_rules_default_heading() -> list[tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str]]]:
        """Get the default heading line type rules.

        Returns:
            list[tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str]]]: The heading line type rules.
        """
        return NLPCore._get_lt_rules_default_heading_list_number()

    # ------------------------------------------------------------------
    # Get the default bulleted list line type rules.
    # ------------------------------------------------------------------
    @staticmethod
    def get_lt_rules_default_list_bullet() -> dict[str, int]:
        """Get the default bulleted list line type rules.

        Returns:
            dict[str, int]: The bulleted list line type rules.
        """
        return NLPCore._get_lt_rules_default_list_bullet()

    # ------------------------------------------------------------------
    # Get the default numbered list line type rules.
    # ------------------------------------------------------------------
    @staticmethod
    def get_lt_rules_default_list_number() -> list[tuple[str, str, collections.abc.Callable[[str, str], bool], list[str]]]:
        """Get the default numbered list line type rules.

        Returns:
            list[tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str]]]: The numbered list line type rules.
        """
        rules: list[tuple[str, str, collections.abc.Callable[[str, str], bool], list[str]]] = []

        for (
            rule_name,
            _,
            regexp_str,
            function_is_asc,
            start_values,
        ) in NLPCore._get_lt_rules_default_heading_list_number():
            rules.append((rule_name, regexp_str, function_is_asc, start_values))

        return rules

    # ------------------------------------------------------------------
    # Ignore the comparison.
    # ------------------------------------------------------------------
    @classmethod
    def is_asc_ignore(cls, _predecessor: str, _successor: str) -> bool:
        """Ignore the comparison.

        Returns:
            bool: True.
        """
        return True

    # ------------------------------------------------------------------
    # Compare two lowercase letters on difference ascending 1.
    # ------------------------------------------------------------------
    @classmethod
    def is_asc_lowercase_letters(cls, predecessor: str, successor: str) -> bool:
        """Compare two lowercase_letters on ascending.

        Args:
            predecessor (str): The previous string.
            successor (str): The current string.

        Returns:
            bool: True, if the successor - predecessor is equal to 1,
                False else.
        """
        if (predecessor_ints := re.findall(r"[a-z]", predecessor.lower())) and (successor_ints := re.findall(r"[a-z]", successor.lower())):
            if ord(successor_ints[0]) - ord(predecessor_ints[0]) == 1:
                return True

        return False

    # ------------------------------------------------------------------
    # Compare two lowercase letters on difference ascending 1 - only first token.
    # ------------------------------------------------------------------
    @classmethod
    def is_asc_lowercase_letters_token(cls, predecessor: str, successor: str) -> bool:
        """Compare two lowercase_letters on ascending - only first token.

        Args:
            predecessor (str): The previous string.
            successor (str): The current string.

        Returns:
            bool: True, if the successor - predecessor is equal to 1,
                False else.
        """
        return cls.is_asc_lowercase_letters(predecessor.split()[0], successor.split()[0])

    # ------------------------------------------------------------------
    # Compare two roman numerals on ascending.
    # ------------------------------------------------------------------
    @classmethod
    def is_asc_romans(cls, predecessor: str, successor: str) -> bool:
        """Compare two roman numerals on ascending.

        Args:
            predecessor (str): The previous roman numeral.
            successor (str): The current roman numeral.

        Returns:
            bool: False, if the predecessor is greater than the current value,
                  True else.
        """
        # TBD depending on different regexp patterns
        # if predecessor[0] == "(":
        #     predecessor_net = predecessor[1:-1]
        #     successor_net = successor[1:-1]
        # else:
        #     predecessor_net = predecessor
        #     successor_net = successor

        if predecessor[0:1] == "(":
            predecessor_net = predecessor[1:]
        else:
            predecessor_net = predecessor
        if predecessor_net[-1] in {")", "."}:
            predecessor_net = predecessor_net[:-1]

        if successor[0:1] == "(":
            successor_net = successor[1:]
        else:
            successor_net = successor
        if successor_net[-1] in {")", "."}:
            successor_net = successor_net[:-1]

        if NLPCore._convert_roman_2_int(successor_net.lower()) - NLPCore._convert_roman_2_int(predecessor_net.lower()) == 1:
            return True

        return False

    # ------------------------------------------------------------------
    # Compare two roman numerals on ascending - only first token.
    # ------------------------------------------------------------------
    @classmethod
    def is_asc_romans_token(cls, predecessor: str, successor: str) -> bool:
        """Compare two roman numerals on ascending - only first token.

        Args:
            predecessor (str): The previous roman numeral.
            successor (str): The current roman numeral.

        Returns:
            bool:False, if the predecessor is greater than the current value,
                 True else.
        """
        # TBD depending on different regexp patterns
        # if predecessor[0] == "(":
        #     predecessor_net = predecessor[1:-1]
        #     successor_net = successor[1:-1]
        # else:
        #     predecessor_net = predecessor
        #     successor_net = successor
        return cls.is_asc_romans(predecessor.split()[0], successor.split()[0])

    # ------------------------------------------------------------------
    # Compare two strings on ascending.
    # ------------------------------------------------------------------
    @classmethod
    def is_asc_strings(cls, predecessor: str, successor: str) -> bool:
        """Compare two strings on ascending.

        Args:
            predecessor (str): The previous string.
            successor (str): The current string.

        Returns:
            bool: False, if the predecessor is greater than the current value,
                  True else.
        """
        if predecessor > successor:
            return False

        return True

    # ------------------------------------------------------------------
    # Compare two string floats on ascending.
    # ------------------------------------------------------------------
    @classmethod
    def is_asc_string_floats(cls, predecessor: str, successor: str) -> bool:
        """Compare two string float numbers on ascending.

        Args:
            predecessor (str): The previous string float number.
            successor (str): The current string float number.

        Returns:
            bool: False, if the predecessor is greater than the current value,
                  True else.
        """
        if (predecessor_floats := re.findall(r"\d+\.\d+", predecessor)) and (successor_floats := re.findall(r"\d+\.\d+", successor)):
            if 0 < float(successor_floats[0]) - float(predecessor_floats[0]) <= 1:
                return True

        return False

    # ------------------------------------------------------------------
    # Compare two string floats on ascending - only first token.
    # ------------------------------------------------------------------
    @classmethod
    def is_asc_string_floats_token(cls, predecessor: str, successor: str) -> bool:
        """Compare two string float numbers on ascending - only first token.

        Args:
            predecessor (str): The previous string float number.
            successor (str): The current string float number.

        Returns:
            bool: False, if the predecessor is greater than the current value,
                  True else.
        """
        return cls.is_asc_string_floats(predecessor.split()[0], successor.split()[0])

    # ------------------------------------------------------------------
    # Compare two string integers on difference ascending 1.
    # ------------------------------------------------------------------
    @classmethod
    def is_asc_string_integers(cls, predecessor: str, successor: str) -> bool:
        """Compare two string integers on ascending.

        Args:
            predecessor (str): The previous string integer.
            successor (str): The current string integer.

        Returns:
            bool: True, if the successor - predecessor is equal to 1,
                False else.
        """
        if (predecessor_ints := re.findall(r"\d+", predecessor)) and (successor_ints := re.findall(r"\d+", successor)):
            if int(successor_ints[0]) - int(predecessor_ints[0]) == 1:
                return True

        return False

    # ------------------------------------------------------------------
    # Compare two string integers on difference ascending 1 - only first token.
    # ------------------------------------------------------------------
    @classmethod
    def is_asc_string_integers_token(cls, predecessor: str, successor: str) -> bool:
        """Compare two string integers on ascending - only first token.

        Args:
            predecessor (str): The previous string integer.
            successor (str): The current string integer.

        Returns:
            bool: True, if the successor - predecessor is equal to 1,
                False else.
        """
        return cls.is_asc_string_integers(predecessor.split()[0], successor.split()[0])

    # ------------------------------------------------------------------
    # Compare two uppercase letters on difference ascending 1.
    # ------------------------------------------------------------------
    @classmethod
    def is_asc_uppercase_letters(cls, predecessor: str, successor: str) -> bool:
        """Compare two uppercase_letters on ascending.

        Args:
            predecessor (str): The previous string.
            successor (str): The current string.

        Returns:
            bool: True, if the successor - predecessor is equal to 1,
                False else.
        """
        if (predecessor_ints := re.findall(r"[A-Z]", predecessor.upper())) and (successor_ints := re.findall(r"[A-Z]", successor.upper())):
            if ord(successor_ints[0]) - ord(predecessor_ints[0]) == 1:
                return True

        return False

    # ------------------------------------------------------------------
    # Compare two uppercase letters on difference ascending 1 - only first token.
    # ------------------------------------------------------------------
    @classmethod
    def is_asc_uppercase_letters_token(cls, predecessor: str, successor: str) -> bool:
        """Compare two uppercase_letters on ascending - only first token.

        Args:
            predecessor (str): The previous string.
            successor (str): The current string.

        Returns:
            bool: True, if the successor - predecessor is equal to 1,
                False else.
        """
        return cls.is_asc_uppercase_letters(predecessor.split()[0], successor.split()[0])
