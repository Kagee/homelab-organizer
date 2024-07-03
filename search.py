# ruff: noqa: T201,F401
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
    ParseException,
    ParseResults,
    QuotedString,
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


def main():
    orig_tests = {
        "ASCII": [],
        "BMP": [],
        "UNICODE": [],
    }

    def dappend(
        search_str: str,
        expected_out_list: list,
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

    dappend("wood AND blue OR red", [["wood", "AND", "blue"], "OR", "red"])
    dappend(
        "wood AND blå OR RØD",
        [["wood", "AND", "blå"], "OR", "RØD"],
        "ASCII",
    )
    dappend("wood OR blue OR red", ["wood", "OR", "blue", "OR", "red"])
    dappend("wood AND(blue OR red)", ["wood", "AND", ["blue", "OR", "red"]])
    dappend(
        '(steel OR iron)AND "lime green"',
        [["steel", "OR", "iron"], "AND", "lime green"],
    )
    dappend(
        "NOT steel OR iron AND 'lime green'",
        [["NOT", "steel"], "OR", ["iron", "AND", "lime green"]],
    )
    dappend(
        "NOT(steelAND OR ORiron) AND 'lime greenNOT'",
        [["NOT", ["steelAND", "OR", "ORiron"]], "AND", "lime greenNOT"],
    )

    for name, parser in (
        ("ASCII", make_parser(printables)),
        # ("UNICODE", make_parser(pyparsing_unicode.printables)),
        ("BMP", make_parser(pyparsing_unicode.BMP.printables)),
    ):
        print(f"{Fore.blue}#####", name, f"#####{Style.reset}")
        tests = iter(orig_tests[name])
        num_tests = 0
        num_passed_tests = 0
        for t in tests:
            num_tests += 1
            print(t.strip())
            u = next(tests)
            parsed = parser.parseString(t)[0]
            # can't compare lists directly using ==
            if str(parsed) == str(u):
                print(f"{Fore.green}True{Style.reset}")
                num_passed_tests += 1
            else:
                print("False", parsed)
                print(f"{Fore.red}     ", str(u), Style.reset)
            sys.stdout.flush()

        s = Fore.green if num_tests == num_passed_tests else Fore.red
        print(f"{s}{num_tests} of {num_passed_tests} passed{Style.reset}")
        sys.stdout.flush()


main()
