# ruff: noqa: N806,COM812,N802,ARG002,T201,ERA001,UP035,F401,TRY003,EM101,EM102,E501,RET504,B904,S101
import operator
from functools import reduce

from django.db.models import (
    Q,
)
from iommi.query import Filter, Query, QueryException, StringValue
from iommi.struct import Struct
from pyparsing import (
    Forward,
    Group,
    Keyword,
    ParseException,
    ParseResults,
    QuotedString,
    Word,
    ZeroOrMore,
    alphanums,
    alphas,
    quotedString,
)

from hlo.models import OrderItem

PRECEDENCE = {
    "AND": 3,  # pragma: no mutate
    "OR": 2,  # pragma: no mutate
}
assert PRECEDENCE["AND"] > PRECEDENCE["OR"]  # pragma: no mutate


class SingleFieldQuery(Query):
    model = OrderItem

    def __init__(self, *args, field=None, **kwargs):
        if not field:
            msg = "Field can not be none"
            raise ValueError(msg)
        self.field_ = field
        super().__init__(*args, **kwargs)

    def parse_query_string(self, query_string: str) -> Q:
        query_string = query_string.strip()
        if not query_string:
            return Q()
        parser = self._create_grammar()
        try:
            tokens = parser.parseString(query_string, parse_all=True)
        except ParseException:
            raise QueryException("Invalid syntax for query")
        return self._compile(tokens)

    def _create_grammar(self):
        and_ = Keyword("AND", caseless=False)
        or_ = Keyword("OR", caseless=False)
        not_ = Keyword("NOT", caseless=False)
        quoted_string_excluding_quotes = QuotedString(
            '"', escChar="\\"
        ).setParseAction(lambda token: StringValue(token[0]))
        value = Word(printables)
        # define query tokens
        # identifier = Word(alphas, alphanums + "_$-.").setName("identifier")
        # raw_value_chars = alphanums + "_$-+/$%*;?@[]\\^`{}|~."
        # raw_value = Word(raw_value_chars, raw_value_chars).setName("raw_value")
        # value_string = quoted_string_excluding_quotes | raw_value

        # Define a where expression
        where_expression = Forward()
        free_text_statement = quotedString.copy().setParseAction(
            self._freetext_to_q
        )
        operator_statement = free_text_statement
        where_condition = Group(
            operator_statement | ("(" + where_expression + ")")
        )
        where_expression << Group(
            where_condition + ZeroOrMore((and_ | or_) + where_expression),
        )

        # define the full grammar
        query_statement = Forward()
        query_statement << Group(where_expression).setResultsName("where")
        return query_statement

    def _freetext_to_q(self, token):
        if len(token) != 1:
            raise QueryException("freetext_to_q got more than one token")
        token = token[0].strip('"')

        return Q(**{self.field_ + "__" + "icontains": token})

    def _compile(self, tokens) -> Q:
        items = []
        for token in tokens:
            if isinstance(token, ParseResults):
                items.append(self._compile(token))
            elif isinstance(token, Q) or token in ("AND", "OR", "NOT"):
                items.append(token)
        return self._rpn_to_q(self._tokens_to_rpn(items))

    @staticmethod
    def _rpn_to_q(tokens):
        stack = []
        unused_not = False
        for each in tokens:
            if isinstance(each, Q):
                # if unused_not:
                #    unused_not = False
                #    stack.append(~each)
                #    continue
                stack.append(each)
            elif each == "NOT":
                unused_not = True
                stack.append(~stack.pop())
                continue
            else:
                op = each
                # infix right hand operator is on the top of the stack
                right, left = stack.pop(), stack.pop()
                stack.append(left & right if op == "AND" else left | right)
        assert len(stack) == 1
        return stack[0]

    @staticmethod
    def _tokens_to_rpn(tokens):
        # Convert a infix sequence of Q objects and 'and/or' operators using
        # dijkstra shunting yard algorithm into RPN
        if len(tokens) == 1:
            return tokens
        result_q, stack = [], []
        for token in tokens:
            assert token is not None
            if isinstance(token, Q):
                result_q.append(token)
            elif token in PRECEDENCE:
                p1 = PRECEDENCE[token]
                while stack:
                    t2, p2 = stack[-1]
                    if p1 <= p2:
                        stack.pop()
                        result_q.append(t2)
                    else:  # pragma: no cover
                        break  # pragma: no mutate
                stack.append((token, PRECEDENCE[token]))
        while stack:
            result_q.append(stack.pop()[0])
        return result_q
