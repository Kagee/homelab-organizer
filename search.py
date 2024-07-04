# ruff: noqa: T201,F401,ERA001,RET504,C901,PLR0915
import sys

from attr.validators import instance_of
from colored import Fore, Style
from django.db.models import (
    Q,
)
from pyparsing import (
    CaselessLiteral,
    Forward,
    Group,
    Keyword,
    Literal,
    Optional,
    ParseException,
    ParseResults,
    QuotedString,
    Suppress,
    Word,
    ZeroOrMore,
    alphanums,
    alphas,
    infix_notation,
    opAssoc,
    printables,
    pyparsing_unicode,
    quoted_string,
    remove_quotes,
)
from pyparsing.core import OneOrMore
from pyparsing.exceptions import ParseException

LPAREN = Literal("(").suppress()
RPAREN = Literal(")").suppress()

# (
#    "ASCII",
#    make_parser(printables),
# ),
# (
#    "Unicode",  # ALL or unicode, SLOW!!
#    make_parser(pyparsing_unicode.printables),
# ),
# (
#    "BasicMultilingualPlane",
#    make_parser(pyparsing_unicode.BasicMultilingualPlane.printables),
# ),


def make_parser(p=printables):
    and_ = Literal("AND")
    or_ = Literal("OR")
    not_ = Literal("NOT")
    search_term = Forward()
    search_term << (
        Word(p, exclude_chars=['"', "'", "(", ")"])
        | quoted_string.setParseAction(remove_quotes)
    )
    search_expr = infix_notation(
        search_term,
        [
            (not_, 1, opAssoc.RIGHT),
            (and_, 2, opAssoc.LEFT),
            (or_, 2, opAssoc.LEFT),
        ],
    )
    return search_expr


def make_parser2(p=printables):
    and_ = Literal("AND")
    or_ = Literal("OR")
    not_ = Literal("NOT")

    # complete_search_expr = Forward()
    # single_search_term = Forward()
    # single_search_term = Word(
    #    p, exclude_chars=['"', "'", "(", ")"]
    # ) | quoted_string.setParseAction(remove_quotes)

    single_word = Word(p, exclude_chars=['"', "'", "(", ")"])

    # d_quoted_word = (Literal('"') + single_word + Literal('"')).setParseAction(
    #    remove_quotes,
    # )
    d_quoted_word = QuotedString('"', unquoteResults=False)
    s_quoted_word = QuotedString("'", unquoteResults=False)
    # single_search_term = Word(p, exclude_chars=['"', "'", "(", ")"]) | Word(
    #    p, exclude_chars=["(", ")"]
    # ).setParseAction(remove_quotes)
    single_search_term = single_word | s_quoted_word | d_quoted_word
    not_term = Group(not_ + single_search_term)
    # not_term = Optional(not_) + (single_search_term)

    multiple_search_term = Forward()
    multiple_search_term = (
        multiple_search_term
        |
        # Group(
        OneOrMore(not_term | single_search_term)
        # )
    )
    # not_term = Group(Optional(not_) + single_search_term)
    search = Group(OneOrMore(not_term | multiple_search_term))

    where_expression = Forward()
    where_expression << ((search + (and_ | or_) + search) | search)

    return where_expression
    # and_term = not_term | Group(not_term + and_ + not_term)
    # and_term = Forward()
    # and_term << Group(
    #    not_term + ZeroOrMore((and_ | or_) + and_term),
    # )

    # Group()
    # + ZeroOrMore(single_search_term)
    # )
    # search_term = Optional(not_) + (
    #    Word(alphas)
    #    | quoted_string.setParseAction(remove_quotes)
    #    | Group(LPAREN + complete_search_expr + RPAREN)
    # )
    # search_and = Group(search_term + ZeroOrMore(and_ + search_term))
    # complete_search_expr << Group(search_and + ZeroOrMore(or_ + search_and))
    # search_expr = infix_notation(
    #    single_search_term,
    #    [
    #        (not_, 1, opAssoc.RIGHT),
    #        (and_, 2, opAssoc.LEFT),
    #        (or_, 2, opAssoc.LEFT),
    #    ],
    # )


def main():
    parsers = [
        (
            "BasicMultilingualPlane2",
            make_parser2(
                # any non-whitespace character
                pyparsing_unicode.BasicMultilingualPlane.printables,
            ),
        ),
    ]

    orig_tests = {}

    for name, _ in parsers:
        orig_tests[name] = []

    def test(
        search_str: str,
        expected_out_list: list | None = None,
        skip: str | list[str] | None = None,
    ) -> None:
        if not skip:
            skip = []
        elif isinstance(skip, str):
            skip = [skip]

        for key in orig_tests:
            if key in skip:
                continue
            orig_tests[key].append(search_str)
            orig_tests[key].append(expected_out_list)

    test("wood", ["wood"])
    test("""'woody legs'""", ["'woody legs'"])
    test("""'woody "" legs'""", ["'woody \"\" legs'"])
    test('''"woody legs"''', ['"woody legs"'])
    test('''"woody legs"''', ['"woody legs"'])
    test('"wooひd næils"', ['"wooひd næils"'])
    test("'wood\"", "invalid")
    test("\"wood'", "invalid")
    test("'wood", "invalid")
    test('"wood', "invalid")
    test("wood iron", ["wood", "iron"])
    test("wood iron steel", ["wood", "iron", "steel"])
    test("NOT wood iron steel", [["NOT", "wood"], "iron", "steel"])
    test("wood NOT iron steel", ["wood", ["NOT", "iron"], "steel"])
    test("wood NOT iron NOT steel", ["wood", ["NOT", "iron"], ["NOT", "steel"]])
    test(
        "wood NOT 'iron' NOT \"steel foundries\"",
        ["wood", ["NOT", "'iron'"], ["NOT", '"steel foundries"']],
    )
    test("wood AND iron", ["wood", "AND", "iron"])
    test("NOT wood AND NOT iron", [["NOT", "wood"], "AND", ["NOT", "iron"]])
    test("NOT wood NOT iron", [["NOT", "wood"], ["NOT", "iron"]])
    test("wood AND iron AND steel", [["wood", "AND", "iron"], "AND", "steel"])
    # test("wood AND blue OR red", [["wood", "AND", "blue"], "OR", "red"])
    # test(
    #    "wood AND blå OR RØD",
    #    [["wood", "AND", "blå"], "OR", "RØD"],
    #    "ASCII",
    # )
    # test("wood OR blue OR red", ["wood", "OR", "blue", "OR", "red"])
    # test("wood AND(blue OR red)", ["wood", "AND", ["blue", "OR", "red"]])
    # test(
    #    '(steel OR iron)AND "lime green"',
    #    [["steel", "OR", "iron"], "AND", "lime green"],
    # )
    # test(
    #    "NOT steel OR iron AND 'lime green'",
    #    [["NOT", "steel"], "OR", ["iron", "AND", "lime green"]],
    # )
    # test(
    #    "NOT(steelAND OR ORiron) AND 'lime greenNOT'",
    #    [["NOT", ["steelAND", "OR", "ORiron"]], "AND", "lime greenNOT"],
    # )

    for name, parser in parsers:
        print(f"{Fore.blue}#####", name, f"#####{Style.reset}")
        tests = iter(orig_tests[name])
        num_tests = 0
        num_passed_tests = 0
        for t in tests:
            num_tests += 1
            print(Fore.blue, t.strip(), "", end=Style.reset)
            expected = str(next(tests))

            try:
                parsed = parser.parseString(t)[0]
            except ParseException:
                s = Fore.red
                if expected == "invalid":
                    s = Fore.green
                    num_passed_tests += 1
                print(f"{s}\nInvalid search: {t}{Style.reset}")
                continue
            if isinstance(parsed, str):
                parsed = [parsed]

            if False:
                expected = "[" + expected + "]"
            # can't compare lists directly using ==
            if str(parsed) == str(expected):
                print(f"{Fore.green}\n{parsed}{Style.reset}")
                num_passed_tests += 1
            else:
                print(f"{Fore.red}")
                # print("  EXPECTED:", )
                print(
                    f"{Style.reset}       GOT:",
                    parsed,
                    "EXP: ",
                    expected,
                    Style.reset,
                )

        _s = Fore.green if num_tests == num_passed_tests else Fore.red
        print(f"{num_passed_tests} of {num_tests}")


main()
