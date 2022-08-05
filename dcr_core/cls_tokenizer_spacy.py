import json

import spacy
import spacy.tokens

from dcr_core import cls_nlp_core
from dcr_core import core_glob
from dcr_core import core_utils


# pylint: disable=too-many-branches
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-statements
class TokenizerSpacy:
    """Determine footer and header lines.

    Returns:
        _type_: TokenizeSpacy instance.
    """

    TokenToken = dict[str, bool | float | int | str]
    TokenTokens = list[TokenToken]

    TokenSent = dict[str, float | int | None | str | TokenTokens]
    TokenSents = list[TokenSent]

    TokenPara = dict[str, int | TokenSents]
    TokenParas = list[TokenPara]

    TokenPage = dict[str, int | TokenParas]
    TokenPages = list[TokenPage]

    TokenDocument = dict[str, int | TokenPages | str]

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(self) -> None:
        """Initialise the instance."""
        core_utils.check_exists_object(
            is_setup=True,
        )

        self._document_id: int = 0
        self._file_name_next = ""
        self._file_name_orig: str = ""
        self._no_lines_footer: int = 0
        self._no_lines_header: int = 0
        self._no_lines_toc: int = 0
        self._pipeline_name = cls_nlp_core.NLPCore.CODE_SPACY_DEFAULT
        self._nlp: spacy.Language = spacy.load(self._pipeline_name)

        self._column_no: int = 0
        self._column_span: int = 0
        self._coord_llx = 0.0
        self._coord_urx = 0.0

        self._line_type = ""

        self._no_lines_in_doc = 0
        self._no_lines_in_page = 0
        self._no_lines_in_para = 0
        self._no_pages_in_doc = 0
        self._no_paras_in_doc = 0
        self._no_paras_in_page = 0
        self._no_sents_in_doc = 0
        self._no_sents_in_page = 0
        self._no_tokens_in_doc = 0
        self._no_tokens_in_page = 0
        self._no_tokens_in_para = 0
        self._no_tokens_in_sent = 0

        self._page_no = 0
        self._para_lines: list[str] = []
        self._para_no = 0
        self._para_no_prev = 0
        self._para_text = ""
        self._processing_ok = False

        self._row_no: int = 0

        self._sent_no = 0
        self._sentence = ""

        self._token_paras: TokenizerSpacy.TokenParas = []
        self._token_sents: TokenizerSpacy.TokenSents = []
        self._token_tokens: TokenizerSpacy.TokenTokens = []

        self.token_pages: TokenizerSpacy.TokenPages = []

        self._exist = True

    # -----------------------------------------------------------------------------
    # Finish current document.
    # -----------------------------------------------------------------------------
    # {
    #     "documentId": 99,
    #     "documentFileName": "xxx",
    #     "noLinesFooter": 99,
    #     "noLinesHeader": 99,
    #     "noLinesInDocument": 99,
    #     "noLinesToc": 99,
    #     "noListsBulletInDocument": 99,
    #     "noListsNumberInDocument": 99,
    #     "noPagesInDocument": 99,
    #     "noParagraphsInDocument": 99,
    #     "noSentencesInDocument": 99,
    #     "noTablesInDocument": 99,
    #     "noTokensInDocument": 99,
    #     "pages": [
    #     ]
    # }
    # -----------------------------------------------------------------------------
    def _finish_document(self) -> None:
        """Finish current ent."""
        core_utils.check_exists_object(
            is_text_parser=True,
        )

        json_data = {
            cls_nlp_core.NLPCore.JSON_NAME_DOC_ID: self._document_id,
            cls_nlp_core.NLPCore.JSON_NAME_DOC_FILE_NAME: self._file_name_orig,
            cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_FOOTER: self._no_lines_footer,
            cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_HEADER: self._no_lines_header,
            cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_IN_DOC: self._no_lines_in_doc,
            cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_TOC: self._no_lines_toc,
            cls_nlp_core.NLPCore.JSON_NAME_NO_LISTS_BULLET_IN_DOC: core_glob.text_parser.parse_result_line_document[
                cls_nlp_core.NLPCore.JSON_NAME_NO_LISTS_BULLET_IN_DOC
            ],
            cls_nlp_core.NLPCore.JSON_NAME_NO_LISTS_NUMBER_IN_DOC: core_glob.text_parser.parse_result_line_document[
                cls_nlp_core.NLPCore.JSON_NAME_NO_LISTS_NUMBER_IN_DOC
            ],
            cls_nlp_core.NLPCore.JSON_NAME_NO_PAGES_IN_DOC: self._no_pages_in_doc,
            cls_nlp_core.NLPCore.JSON_NAME_NO_PARAS_IN_DOC: self._no_paras_in_doc,
            cls_nlp_core.NLPCore.JSON_NAME_NO_SENTS_IN_DOC: self._no_sents_in_doc,
            cls_nlp_core.NLPCore.JSON_NAME_NO_TABLES_IN_DOC: core_glob.text_parser.parse_result_line_document[
                cls_nlp_core.NLPCore.JSON_NAME_NO_TABLES_IN_DOC
            ],
            cls_nlp_core.NLPCore.JSON_NAME_NO_TOKENS_IN_DOC: self._no_tokens_in_doc,
            cls_nlp_core.NLPCore.JSON_NAME_PAGES: self.token_pages,
        }

        if core_glob.setup.is_tokenize_2_jsonfile:
            with open(self._file_name_next, "w", encoding=core_glob.FILE_ENCODING_DEFAULT) as file_handle:
                json.dump(
                    json_data,
                    file_handle,
                    indent=core_glob.setup.json_indent,
                    sort_keys=core_glob.setup.is_json_sort_keys,
                )

    # -----------------------------------------------------------------------------
    # Finish current page.
    # -----------------------------------------------------------------------------
    # {
    #     "pageNo": 99,
    #     "noLinesInPage": 99,
    #     "noParagraphsInPage": 99,
    #     "noSentencesInPage": 99,
    #     "noTokensInPage": 99,
    #     "paragraphs": [
    #     ]
    # }
    # -----------------------------------------------------------------------------
    def _finish_page(self) -> None:
        """Finish current page."""
        self._no_pages_in_doc += 1

        self.token_pages.append(
            {
                cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO: self._page_no,
                cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_IN_PAGE: self._no_lines_in_page,
                cls_nlp_core.NLPCore.JSON_NAME_NO_PARAS_IN_PAGE: self._no_paras_in_page,
                cls_nlp_core.NLPCore.JSON_NAME_NO_SENTS_IN_PAGE: self._no_sents_in_page,
                cls_nlp_core.NLPCore.JSON_NAME_NO_TOKENS_IN_PAGE: self._no_tokens_in_page,
                cls_nlp_core.NLPCore.JSON_NAME_PARAS: self._token_paras,
            }
        )

    # -----------------------------------------------------------------------------
    # Finish current paragraph.
    # -----------------------------------------------------------------------------
    # {
    #     "paragraphNo": 99,
    #     "noLinesInParagraph": 99,
    #     "noSentencesInParagraph": 99,
    #     "noTokensInParagraph": 99,
    #     "sentences": [
    #     ]
    # }
    # -----------------------------------------------------------------------------
    def _finish_para(self) -> None:
        """Finish current paragraph."""
        self._para_text = " ".join(self._para_lines)

        self._no_paras_in_doc += 1
        self._no_paras_in_page += 1

        self._process_sents()

        self._token_paras.append(
            {
                cls_nlp_core.NLPCore.JSON_NAME_PARA_NO: self._para_no_prev,
                cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_IN_PARA: self._no_lines_in_para,
                cls_nlp_core.NLPCore.JSON_NAME_NO_SENTS_IN_PARA: self._sent_no,
                cls_nlp_core.NLPCore.JSON_NAME_NO_TOKENS_IN_PARA: self._no_tokens_in_para,
                cls_nlp_core.NLPCore.JSON_NAME_SENTS: self._token_sents,
            }
        )

    # -----------------------------------------------------------------------------
    # Finish current sentence.
    # -----------------------------------------------------------------------------
    # {
    #     "sentenceNo": 99,
    #     "columnNo": 99,
    #     "coordLLX": 99.99,
    #     "coordURX": 99.99,
    #     "lineType": "xxx",
    #     "noTokensInSentence": 99,
    #     "rowNo": 99,
    #     "text": "xxx",
    #     "tokens": [
    #     ]
    # }
    # -----------------------------------------------------------------------------
    def _finish_sent(self) -> None:
        """Finish current sentence."""
        self._no_sents_in_doc += 1
        self._no_sents_in_page += 1

        self._sent_no += 1

        if self._line_type[:2] == cls_nlp_core.NLPCore.LINE_TYPE_HEADING and self._sent_no > 1:
            line_type = cls_nlp_core.NLPCore.LINE_TYPE_BODY
        else:
            line_type = self._line_type

        if self._column_no > 0:
            if self._column_span > 0:
                self._token_sents.append(
                    {
                        cls_nlp_core.NLPCore.JSON_NAME_SENT_NO: self._sent_no,
                        cls_nlp_core.NLPCore.JSON_NAME_COLUMN_NO: self._column_no,
                        cls_nlp_core.NLPCore.JSON_NAME_COLUMN_SPAN: self._column_span,
                        cls_nlp_core.NLPCore.JSON_NAME_COORD_LLX: self._coord_llx,
                        cls_nlp_core.NLPCore.JSON_NAME_COORD_URX: self._coord_urx,
                        cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE: line_type,
                        cls_nlp_core.NLPCore.JSON_NAME_NO_TOKENS_IN_SENT: self._no_tokens_in_sent,
                        cls_nlp_core.NLPCore.JSON_NAME_ROW_NO: self._row_no,
                        cls_nlp_core.NLPCore.JSON_NAME_TEXT: self._sentence,
                        cls_nlp_core.NLPCore.JSON_NAME_TOKENS: self._token_tokens,
                    }
                )
            else:
                self._token_sents.append(
                    {
                        cls_nlp_core.NLPCore.JSON_NAME_SENT_NO: self._sent_no,
                        cls_nlp_core.NLPCore.JSON_NAME_COLUMN_NO: self._column_no,
                        cls_nlp_core.NLPCore.JSON_NAME_COORD_LLX: self._coord_llx,
                        cls_nlp_core.NLPCore.JSON_NAME_COORD_URX: self._coord_urx,
                        cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE: line_type,
                        cls_nlp_core.NLPCore.JSON_NAME_NO_TOKENS_IN_SENT: self._no_tokens_in_sent,
                        cls_nlp_core.NLPCore.JSON_NAME_ROW_NO: self._row_no,
                        cls_nlp_core.NLPCore.JSON_NAME_TEXT: self._sentence,
                        cls_nlp_core.NLPCore.JSON_NAME_TOKENS: self._token_tokens,
                    }
                )
        else:
            self._token_sents.append(
                {
                    cls_nlp_core.NLPCore.JSON_NAME_SENT_NO: self._sent_no,
                    cls_nlp_core.NLPCore.JSON_NAME_COORD_LLX: self._coord_llx,
                    cls_nlp_core.NLPCore.JSON_NAME_COORD_URX: self._coord_urx,
                    cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE: line_type,
                    cls_nlp_core.NLPCore.JSON_NAME_NO_TOKENS_IN_SENT: self._no_tokens_in_sent,
                    cls_nlp_core.NLPCore.JSON_NAME_TEXT: self._sentence,
                    cls_nlp_core.NLPCore.JSON_NAME_TOKENS: self._token_tokens,
                }
            )

    # -----------------------------------------------------------------------------
    # Determine the requested token attributes.
    # -----------------------------------------------------------------------------
    @staticmethod
    def _get_token_attributes(token: spacy.tokens.Token) -> TokenToken:  # type: ignore # noqa: C901
        """Determine the requested token attributes.

        Args:
            token (spacy.tokens.Token):
                spaCy tokens.

        Returns:
            Token:
                Requested token attributes.
        """
        token_attr: dict[str, bool | float | int | str] = {}

        if (
            token.is_bracket  # pylint: disable=too-many-boolean-expressions
            and core_glob.setup.is_spacy_ignore_bracket
            or token.is_left_punct
            and core_glob.setup.is_spacy_ignore_left_punct
            or token.is_punct
            and core_glob.setup.is_spacy_ignore_punct
            or token.is_quote
            and core_glob.setup.is_spacy_ignore_quote
            or token.is_right_punct
            and core_glob.setup.is_spacy_ignore_right_punct
            or token.is_space
            and core_glob.setup.is_spacy_ignore_space
            or token.is_stop
            and core_glob.setup.is_spacy_ignore_stop
        ):
            return token_attr

        if core_glob.setup.is_spacy_tkn_attr_cluster:
            if token.cluster != "":
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_CLUSTER] = token.cluster

        if core_glob.setup.is_spacy_tkn_attr_dep_:
            if token.dep_ != "":
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_DEP_] = token.dep_

        if core_glob.setup.is_spacy_tkn_attr_doc:
            if token.doc is not None:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_DOC] = token.doc.text

        if core_glob.setup.is_spacy_tkn_attr_ent_iob_:
            if token.ent_iob_ != "":
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_ENT_IOB_] = token.ent_iob_

        if core_glob.setup.is_spacy_tkn_attr_ent_kb_id_:
            # not testable
            if token.ent_kb_id_ != "":
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_ENT_KB_ID_] = token.ent_kb_id_

        if core_glob.setup.is_spacy_tkn_attr_ent_type_:
            if token.ent_type_ != "":
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_ENT_TYPE_] = token.ent_type_

        if core_glob.setup.is_spacy_tkn_attr_head:
            if token.head is not None:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_HEAD] = token.head.i

        if core_glob.setup.is_spacy_tkn_attr_i:
            token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_I] = token.i

        if core_glob.setup.is_spacy_tkn_attr_idx:
            if token.idx != "":
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IDX] = token.idx

        if core_glob.setup.is_spacy_tkn_attr_is_alpha:
            if token.is_alpha:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_ALPHA] = token.is_alpha

        if core_glob.setup.is_spacy_tkn_attr_is_ascii:
            if token.is_ascii:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_ASCII] = token.is_ascii

        if core_glob.setup.is_spacy_tkn_attr_is_bracket:
            if token.is_bracket:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_BRACKET] = token.is_bracket

        if core_glob.setup.is_spacy_tkn_attr_is_currency:
            if token.is_currency:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_CURRENCY] = token.is_currency

        if core_glob.setup.is_spacy_tkn_attr_is_digit:
            if token.is_digit:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_DIGIT] = token.is_digit

        if core_glob.setup.is_spacy_tkn_attr_is_left_punct:
            if token.is_left_punct:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_LEFT_PUNCT] = token.is_left_punct

        if core_glob.setup.is_spacy_tkn_attr_is_lower:
            if token.is_lower:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_LOWER] = token.is_lower

        if core_glob.setup.is_spacy_tkn_attr_is_oov:
            if token.is_oov:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_OOV] = token.is_oov

        if core_glob.setup.is_spacy_tkn_attr_is_punct:
            if token.is_punct:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_PUNCT] = token.is_punct

        if core_glob.setup.is_spacy_tkn_attr_is_quote:
            if token.is_quote:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_QUOTE] = token.is_quote

        if core_glob.setup.is_spacy_tkn_attr_is_right_punct:
            if token.is_right_punct:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_RIGHT_PUNCT] = token.is_right_punct

        if core_glob.setup.is_spacy_tkn_attr_is_sent_end:
            if token.is_sent_end:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_SENT_END] = token.is_sent_end

        if core_glob.setup.is_spacy_tkn_attr_is_sent_start:
            if token.is_sent_start:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_SENT_START] = token.is_sent_start

        if core_glob.setup.is_spacy_tkn_attr_is_space:
            if token.is_space:
                # not testable
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_SPACE] = token.is_space

        if core_glob.setup.is_spacy_tkn_attr_is_stop:
            if token.is_stop:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_STOP] = token.is_stop

        if core_glob.setup.is_spacy_tkn_attr_is_title:
            if token.is_title:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_TITLE] = token.is_title

        if core_glob.setup.is_spacy_tkn_attr_is_upper:
            if token.is_upper:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_UPPER] = token.is_upper

        if core_glob.setup.is_spacy_tkn_attr_lang_:
            if token.lang_ != "":
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_LANG_] = token.lang_

        if core_glob.setup.is_spacy_tkn_attr_left_edge:
            if token.left_edge.text is not None:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_LEFT_EDGE] = token.left_edge.i

        if core_glob.setup.is_spacy_tkn_attr_lemma_:
            if token.lemma_ != "":
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_LEMMA_] = token.lemma_

        if core_glob.setup.is_spacy_tkn_attr_lex:
            if token.lex is not None:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_LEX] = token.lex.text

        if core_glob.setup.is_spacy_tkn_attr_lex_id:
            if token.lex_id != "":
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_LEX_ID] = token.lex_id

        if core_glob.setup.is_spacy_tkn_attr_like_email:
            if token.like_email:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_LIKE_EMAIL] = token.like_email

        if core_glob.setup.is_spacy_tkn_attr_like_num:
            if token.like_num:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_LIKE_NUM] = token.like_num

        if core_glob.setup.is_spacy_tkn_attr_like_url:
            if token.like_url:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_LIKE_URL] = token.like_url

        if core_glob.setup.is_spacy_tkn_attr_lower_:
            if token.lower_ != "":
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_LOWER_] = token.lower_

        if core_glob.setup.is_spacy_tkn_attr_morph:
            if token.morph is not None:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_MORPH] = str(token.morph)

        if core_glob.setup.is_spacy_tkn_attr_norm_:
            if token.norm_ != "":
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_NORM_] = token.norm_

        if core_glob.setup.is_spacy_tkn_attr_orth_:
            if token.orth_ != "":
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_ORTH_] = token.orth_

        if core_glob.setup.is_spacy_tkn_attr_pos_:
            if token.pos_ != "":
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_POS_] = token.pos_

        if core_glob.setup.is_spacy_tkn_attr_prefix_:
            if token.prefix_ != "":
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_PREFIX_] = token.prefix_

        if core_glob.setup.is_spacy_tkn_attr_prob:
            if token.prob != "":
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_PROB] = token.prob

        if core_glob.setup.is_spacy_tkn_attr_rank:
            if token.rank != "":
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_RANK] = token.rank

        if core_glob.setup.is_spacy_tkn_attr_right_edge:
            if token.right_edge is not None:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_RIGHT_EDGE] = token.right_edge.i

        if core_glob.setup.is_spacy_tkn_attr_sent:
            if token.sent is not None:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_SENT] = token.sent.text

        if core_glob.setup.is_spacy_tkn_attr_sentiment:
            if token.sentiment != "":
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_SENTIMENT] = token.sentiment

        if core_glob.setup.is_spacy_tkn_attr_shape_:
            if token.shape_ != "":
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_SHAPE_] = token.shape_

        if core_glob.setup.is_spacy_tkn_attr_suffix_:
            if token.suffix_ != "":
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_SUFFIX_] = token.suffix_

        if core_glob.setup.is_spacy_tkn_attr_tag_:
            if token.tag_ != "":
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_TAG_] = token.tag_

        if core_glob.setup.is_spacy_tkn_attr_tensor:
            try:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_TENSOR] = str(token.tensor)
            except IndexError:
                pass

        if core_glob.setup.is_spacy_tkn_attr_text:
            if token.text != "":
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_TEXT] = token.text

        if core_glob.setup.is_spacy_tkn_attr_text_with_ws:
            if token.text_with_ws != "":
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_TEXT_WITH_WS] = token.text_with_ws

        if core_glob.setup.is_spacy_tkn_attr_vocab:
            if token.vocab is not None:
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_RANK] = str(token.vocab)

        if core_glob.setup.is_spacy_tkn_attr_whitespace_:
            if token.whitespace_ != "":
                token_attr[cls_nlp_core.NLPCore.JSON_NAME_TOKEN_WHITESPACE_] = token.whitespace_

        return token_attr

    # -----------------------------------------------------------------------------
    # Initialise a new document.
    # -----------------------------------------------------------------------------
    def _init_document(self) -> None:
        """Initialize a new document."""
        self._no_lines_in_doc = 0
        self._no_pages_in_doc = 0
        self._no_paras_in_doc = 0
        self._no_sents_in_doc = 0
        self._no_tokens_in_doc = 0

        self.token_pages = []

    # -----------------------------------------------------------------------------
    # Initialise a new page.
    # -----------------------------------------------------------------------------
    def _init_page(self) -> None:
        """Initialize a new page."""
        self._no_lines_in_page = 0
        self._no_paras_in_page = 0
        self._no_sents_in_page = 0
        self._no_tokens_in_page = 0

        self._token_paras = []

    # -----------------------------------------------------------------------------
    # Initialise a new paragraph.
    # -----------------------------------------------------------------------------
    def _init_para(self) -> None:
        """Initialize a new paragraph."""
        core_utils.check_exists_object(
            is_text_parser=True,
        )

        if cls_nlp_core.NLPCore.JSON_NAME_COLUMN_NO in core_glob.text_parser.parse_result_line_line:
            self._column_no = core_glob.text_parser.parse_result_line_line[cls_nlp_core.NLPCore.JSON_NAME_COLUMN_NO]
            self._row_no = core_glob.text_parser.parse_result_line_line[cls_nlp_core.NLPCore.JSON_NAME_ROW_NO]
            if cls_nlp_core.NLPCore.JSON_NAME_COLUMN_SPAN in core_glob.text_parser.parse_result_line_line:
                self._column_span = core_glob.text_parser.parse_result_line_line[cls_nlp_core.NLPCore.JSON_NAME_COLUMN_SPAN]
            else:
                self._column_span = 0
        else:
            self._column_no = 0
            self._column_span = 0
            self._row_no = 0

        self._coord_llx = core_glob.text_parser.parse_result_line_line[cls_nlp_core.NLPCore.JSON_NAME_COORD_LLX]
        self._coord_urx = core_glob.text_parser.parse_result_line_line[cls_nlp_core.NLPCore.JSON_NAME_COORD_URX]

        self._no_lines_in_para = 0
        self._no_tokens_in_para = 0

        self._para_lines = []

        self._token_sents = []

        self._para_no_prev = self._para_no

    # -----------------------------------------------------------------------------
    # Initialise a new sentence.
    # -----------------------------------------------------------------------------
    def _init_sent(self) -> None:
        """Initialize a new sentence."""
        self._no_tokens_in_sent = 0

        self._token_tokens = []

    # -----------------------------------------------------------------------------
    # Process a whole new page.
    # -----------------------------------------------------------------------------
    def _process_page(self) -> None:
        """Process a whole new page."""
        core_utils.check_exists_object(
            is_text_parser=True,
        )

        self._para_no_prev = 0

        # {
        #    "columnNo": 99,
        #    "columnSpan": 99,
        #    "lineNo": 99,
        #    "lineIndexPage": 99,
        #    "lineIndexParagraph": 99,
        #    "lineType": "b",
        #    "lowerLeftX": 99.99,
        #    "paragraphNo": 99,
        #    "rowNo": 99,
        #    "text": "..."
        # },
        for core_glob.text_parser.parse_result_line_line in core_glob.text_parser.parse_result_line_page[
            cls_nlp_core.NLPCore.JSON_NAME_LINES
        ]:
            line_type = core_glob.text_parser.parse_result_line_line[cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE]

            if (
                line_type == cls_nlp_core.NLPCore.LINE_TYPE_FOOTER  # pylint: disable=too-many-boolean-expressions
                and core_glob.setup.is_spacy_ignore_line_type_footer
                or line_type == cls_nlp_core.NLPCore.LINE_TYPE_HEADER
                and core_glob.setup.is_spacy_ignore_line_type_header
                or line_type == cls_nlp_core.NLPCore.LINE_TYPE_HEADING
                and core_glob.setup.is_spacy_ignore_line_type_heading
                or line_type == cls_nlp_core.NLPCore.LINE_TYPE_LIST_BULLET
                and core_glob.setup.is_spacy_ignore_line_type_list_bullet
                or line_type == cls_nlp_core.NLPCore.LINE_TYPE_LIST_NUMBER
                and core_glob.setup.is_spacy_ignore_line_type_list_number
                or line_type == cls_nlp_core.NLPCore.LINE_TYPE_TABLE
                and core_glob.setup.is_spacy_ignore_line_type_table
                or line_type == cls_nlp_core.NLPCore.LINE_TYPE_TOC
                and core_glob.setup.is_spacy_ignore_line_type_toc
            ):
                continue

            self._para_no = core_glob.text_parser.parse_result_line_line[cls_nlp_core.NLPCore.JSON_NAME_PARA_NO]

            if self._para_no_prev == 0:
                self._init_para()
            elif self._para_no != self._para_no_prev:
                self._finish_para()
                self._init_para()

            self._process_para()

        if self._para_no_prev > 0:
            self._finish_para()

    # -----------------------------------------------------------------------------
    # Process a whole new paragraph.
    # -----------------------------------------------------------------------------
    def _process_para(self) -> None:
        """Process a whole new paragraph."""
        core_utils.check_exists_object(
            is_text_parser=True,
        )

        self._no_lines_in_doc += 1
        self._no_lines_in_page += 1
        self._no_lines_in_para += 1

        if not self._para_lines:
            self._line_type = core_glob.text_parser.parse_result_line_line[cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE]

        self._para_lines.append(core_glob.text_parser.parse_result_line_line[cls_nlp_core.NLPCore.JSON_NAME_TEXT])

    # -----------------------------------------------------------------------------
    # Process all sentences of a paragraph.
    # -----------------------------------------------------------------------------
    def _process_sents(self) -> None:
        """Process all sentences of a paragraph."""
        self._sent_no = 0

        paragraph = self._nlp(self._para_text)

        for sent in paragraph.sents:
            self._sentence = sent.text

            self._init_sent()

            self._process_tokens()

            self._finish_sent()

    # -----------------------------------------------------------------------------
    # Process all tokens of a sentence.
    # -----------------------------------------------------------------------------
    # {
    #     "tknI": 99,
    #     "tknIsOov": boolean,
    #     "tknIsTitle": boolean,
    #     "tknLemma_": "xxx",
    #     "tknNorm_": "xxx",
    #     "tknPos_": "xxx",
    #     "tknTag_": "xxx",
    #     "tknText": "xxx",
    #     "tknWhitespace_": "xxx"
    # }
    # -----------------------------------------------------------------------------
    def _process_tokens(self) -> None:
        """Process all tokens of a sentence."""
        self._token_no = 0

        sentence = self._nlp(self._sentence)

        for token in sentence:
            if (token_token := self._get_token_attributes(token)) != {}:
                self._no_tokens_in_doc += 1
                self._no_tokens_in_page += 1
                self._no_tokens_in_para += 1
                self._no_tokens_in_sent += 1
                self._token_tokens.append(token_token)

    # -----------------------------------------------------------------------------
    # Check the object existence.
    # -----------------------------------------------------------------------------
    def exists(self) -> bool:
        """Check the object existence.

        Returns:
            bool:   Always true
        """
        return self._exist

    # -----------------------------------------------------------------------------
    # Process a whole new document.
    # -----------------------------------------------------------------------------
    def process_document(
        self,
        document_id: int,
        file_name_next: str,
        file_name_orig: str,
        no_lines_footer: int,
        no_lines_header: int,
        no_lines_toc: int,
        pipeline_name: str,
    ) -> None:
        """Process a whole new document.

        Args:
            document_id (int):
                    Identification of the document.
            file_name_next (str):
                    File name of the output file.
            file_name_orig (in):
                    File name of the document file.
            no_lines_footer (int):
                    Number footer lines.
            no_lines_header (int):
                    Number header lines.
            no_lines_toc (int):
                    Nummer TOC lines.
            pipeline_name (str):
                    SpaCy pipeline name.
        """
        core_utils.check_exists_object(
            is_setup=True,
            is_text_parser=True,
        )

        self._document_id = document_id
        self._file_name_next = file_name_next
        self._file_name_orig = file_name_orig
        self._no_lines_footer = no_lines_footer
        self._no_lines_header = no_lines_header
        self._no_lines_toc = no_lines_toc

        if pipeline_name != self._pipeline_name:
            self._nlp = spacy.load(pipeline_name)
            self._pipeline_name = pipeline_name

        self._processing_ok = False

        self._init_document()

        # {
        #   "pageNo": 99,
        #   "noParagraphsInPage": 99,
        #   "noLinesInPage": 99,
        #   "lines": [...]
        # }
        for core_glob.text_parser.parse_result_line_page in core_glob.text_parser.parse_result_line_document[
            cls_nlp_core.NLPCore.JSON_NAME_PAGES
        ]:
            self._page_no = core_glob.text_parser.parse_result_line_page[cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO]

            self._init_page()
            self._process_page()
            self._finish_page()

        self._finish_document()

        self._processing_ok = True

    # -----------------------------------------------------------------------------
    # Check the processing result.
    # -----------------------------------------------------------------------------
    def processing_ok(self) -> bool:
        """Check the processing result.

        Returns:
            bool:   True if processing has been completed without errors.
        """
        return self._processing_ok