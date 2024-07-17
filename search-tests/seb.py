# ruff: noqa: N806,COM812,N802,ARG002,T201,ERA001
import logging

from pyparsing import (
    # Combine,
    Forward,
    Group,
    Keyword,
    OneOrMore,
    Suppress,
    Word,
    alphanums,
    oneOf,
)

logging.basicConfig(
    level=logging.DEBUG,
    style="{",
    format="{asctime} [{levelname}] {message} ({name}:{module})",
    handlers=[logging.StreamHandler()],
    # stream=sys.stderr # replaces handlers above
)
logger = logging.getLogger(__name__)


class SearchQueryParser:
    def __init__(self):
        self._methods = {
            "AND": self.evaluateAnd,
            "OR": self.evaluateOr,
            "NOT": self.evaluateNot,
            "parenthesis": self.evaluateParenthesis,
            "quotes": self.evaluateQuotes,
            "word": self.evaluateWord,
        }
        self._parser = self.parser()

    def parser(self):
        """
        This function returns a parser.
        The grammar should be like most full text search
        engines (Google, Tsearch, Lucene).

        Grammar:
        - a query consists of alphanumeric words
        - a sequence of words between quotes is a literal string
        - words can be used together by using operators ('AND' or 'OR')
        - words with operators can be grouped with parenthesis
        - a word or group of words can be preceded by a 'NOT' operator
        - the 'AND' operator precedes an 'or' operator
        - if an operator is missing, use an 'AND' operator
        """
        operatorOr = Forward()

        operatorWord = Group(Word(alphanums)).setResultsName("word")

        operatorQuotesContent = Forward()
        operatorQuotesContent << (
            (operatorWord + operatorQuotesContent) | operatorWord
        )

        operatorQuotes = (
            Group(
                Suppress('"') + operatorQuotesContent + Suppress('"')
            ).setResultsName("quotes")
            | operatorWord
        )

        operatorParenthesis = (
            Group(Suppress("(") + operatorOr + Suppress(")")).setResultsName(
                "parenthesis"
            )
            | operatorQuotes
        )

        operatorNot = Forward()
        operatorNot << (
            Group(
                Suppress(Keyword("NOT", caseless=True)) + operatorNot
            ).setResultsName("NOT")
            | operatorParenthesis
        )

        operatorAnd = Forward()
        operatorAnd << (
            Group(
                operatorNot
                + Suppress(Keyword("AND", caseless=True))
                + operatorAnd
            ).setResultsName("AND")
            | Group(
                operatorNot + OneOrMore(~oneOf("AND OR") + operatorAnd)
            ).setResultsName("AND")
            | operatorNot
        )

        operatorOr << (
            Group(
                operatorAnd
                + Suppress(Keyword("OR", caseless=True))
                + operatorOr
            ).setResultsName("OR")
            | operatorAnd
        )

        return operatorOr.parseString

    def evaluateAnd(self, argument):
        return self.evaluate(argument[0]).intersection(
            self.evaluate(argument[1])
        )

    def evaluateOr(self, argument):
        return self.evaluate(argument[0]).union(self.evaluate(argument[1]))

    def evaluateNot(self, argument):
        return self.GetNot(self.evaluate(argument[0]))

    def evaluateParenthesis(self, argument):
        return self.evaluate(argument[0])

    def evaluateQuotes(self, argument):
        """Evaluate quoted strings

        First is does an 'AND' on the indidual search terms, then it asks the
        function GetQuoted to only return the subset of ID's that contain the
        literal string.
        """
        r = set()
        search_terms = []
        for item in argument:
            search_terms.append(item[0])
            if len(r) == 0:
                r = self.evaluate(item)
            else:
                r = r.intersection(self.evaluate(item))
        return self.GetQuotes(" ".join(search_terms), r)

    def evaluateWord(self, argument):
        return self.GetWord(argument[0])

    def evaluate(self, argument):
        return self._methods[argument.getName()](argument)

    def Parse(self, query):
        # print self._parser(query)[0]
        return self.evaluate(self._parser(query)[0])

    def GetWord(self, word):
        return set()

    def GetQuotes(self, search_string, tmp_result):
        return set()

    def GetNot(self, not_set):
        return set().difference(not_set)


class SimpleSearcher(SearchQueryParser):
    def GetWord(self, word):
        logger.debug("GetWord: %s", word)
        return set([word])

    def GetQuotes(self, search_string, tmp_result):
        logger.debug("GetQuotes ss: %s", search_string)
        logger.debug("GetQuotes ts: %s", tmp_result)
        result = set()
        return result

    def GetNot(self, not_set):
        logger.debug("GetNot: %s", not_set)
        return set()

    def Do(self, item: str):
        logger.debug()
        logger.debug("Query: ", item)
        r = self.Parse(item)
        logger.debug("Result: %s", r)


if __name__ == "__main__":
    SimpleSearcher().Do("hello AND world")
    SimpleSearcher().Do("hello NOT world")
    SimpleSearcher().Do("hello not world")
    SimpleSearcher().Do("hello not 'ursa primor'")
