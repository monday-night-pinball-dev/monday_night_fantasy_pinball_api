from typing import Any, LiteralString
from util.database import (
    ExactMatchSearchTerm,
    InListSearchTerm,
    LikeComparatorModes,
    LikeSearchTerm,
    RangeSearchTerm,
)
from util.db_connection import PGConnection


def test_exact_match_search_term_generates_sql_with_string():
    search_term = ExactMatchSearchTerm('test_column', 'a string')

    expected_sqlstring = "test_column = 'a string'"

    result_sqlstring = search_term.generate_sql()

    assert expected_sqlstring == result_sqlstring


def test_exact_match_search_term_generates_sql_with_boolean():
    search_term = ExactMatchSearchTerm('test_column', True)

    expected_sqlstring = "test_column = 'True'"

    result_sqlstring = search_term.generate_sql()

    assert expected_sqlstring == result_sqlstring


def test_exact_match_search_term_generates_sql_ignore_case():
    search_term = ExactMatchSearchTerm('test_column', 'A String', True)

    expected_sqlstring = "LOWER(test_column) = LOWER('A String')"

    result_sqlstring = search_term.generate_sql()

    assert expected_sqlstring == result_sqlstring


def test_like_search_term_generates_sql_as_like():
    search_term = LikeSearchTerm('test_column', 'A String')

    expected_sqlstring = "test_column LIKE '%A String%'"

    result_sqlstring = search_term.generate_sql()

    assert expected_sqlstring == result_sqlstring


def test_like_search_term_generates_sql_as_starts_with():
    search_term = LikeSearchTerm('test_column', 'A String',
                                 LikeComparatorModes.StartsWith)

    expected_sqlstring = "test_column LIKE 'A String%'"

    result_sqlstring = search_term.generate_sql()

    assert expected_sqlstring == result_sqlstring


def test_like_search_term_generates_sql_as_ends_with():
    search_term = LikeSearchTerm('test_column', 'A String',
                                 LikeComparatorModes.EndsWith)

    expected_sqlstring = "test_column LIKE '%A String'"

    result_sqlstring = search_term.generate_sql()

    assert expected_sqlstring == result_sqlstring


def test_like_search_term_generates_sql_as_like_ignore_case():
    search_term = LikeSearchTerm('test_column', 'A String',
                                 LikeComparatorModes.Like, True)

    expected_sqlstring = "test_column ILIKE '%A String%'"

    result_sqlstring = search_term.generate_sql()

    assert expected_sqlstring == result_sqlstring


def test_in_list_search_term_generates_sql():
    search_term = InListSearchTerm('test_column',
                                   ['string 1', 'string 2', 'string 3'])

    expected_sqlstring = (f'test_column IN (\n'
                          f"\t'string 1',\n"
                          f"\t'string 2',\n"
                          f"\t'string 3'\n"
                          f')')

    result_sqlstring = search_term.generate_sql()

    assert expected_sqlstring == result_sqlstring


def test_in_list_search_term_generates_sql_ignore_case():
    search_term = InListSearchTerm('test_column',
                                   ['string 1', 'string 2', 'string 3'], True)

    expected_sqlstring = (f'LOWER(test_column) IN (\n'
                          f"\tLOWER('string 1'),\n"
                          f"\tLOWER('string 2'),\n"
                          f"\tLOWER('string 3')\n"
                          f')')

    result_sqlstring = search_term.generate_sql()

    assert expected_sqlstring == result_sqlstring


def test_range_search_term_generates_sql_no_min_max():
    search_term = RangeSearchTerm('test_column')

    search_term.column_name = 'test_column'

    expected_sqlstring: str = (
        f'test_column = test_column OR test_column IS NULL')

    result_sqlstring = search_term.generate_sql()

    assert expected_sqlstring == result_sqlstring


def test_range_search_term_generates_sql_both_min_max():
    search_term = RangeSearchTerm('test_column', 222, 444)

    expected_sqlstring: str = f"test_column >= '222' AND test_column <= '444'"

    result_sqlstring = search_term.generate_sql()

    assert expected_sqlstring == result_sqlstring


def test_range_search_term_generates_sql_only_min():
    search_term = RangeSearchTerm('test_column', 222)

    expected_sqlstring: str = f"test_column >= '222'"

    result_sqlstring = search_term.generate_sql()

    assert expected_sqlstring == result_sqlstring


def test_range_search_term_generates_sql_only_max():
    search_term = RangeSearchTerm('test_column', None, 444)

    expected_sqlstring: str = f"test_column <= '444'"

    result_sqlstring = search_term.generate_sql()

    assert expected_sqlstring == result_sqlstring


def test_range_search_term_generates_sql_both_min_max_ignore_case():
    search_term = RangeSearchTerm('test_column', 222, 444, True)

    search_term.column_name = 'test_column'
    search_term.value_min = 222
    search_term.value_max = 444
    search_term.ignore_case = True

    expected_sqlstring: str = f"LOWER(test_column) >= LOWER('222') AND LOWER(test_column) <= LOWER('444')"

    result_sqlstring = search_term.generate_sql()

    assert expected_sqlstring == result_sqlstring
