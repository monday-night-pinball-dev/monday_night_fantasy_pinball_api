from typing import Any

from database import (
    ExactMatchSearchTerm,
    InListSearchTerm,
    LikeComparatorModes,
    LikeSearchTerm,
    PagingModel,
    RangeSearchTerm,
    SearchTerm,
)
from db_connection import PGConnection


def test_build_insert_query_handles_all_types():
    connection = PGConnection()

    parameters: dict[str, Any] = {
        'string_test': 'string_theory',
        'int_test': 1234,
        'bool_test': True,
        'timestamp_test': '2000-10-31T01:30:00.000-05:00',
    }

    expected_sqlstr = (f'INSERT INTO test_table\n'
                       f'(\n'
                       f'\tstring_test,\n'
                       f'\tint_test,\n'
                       f'\tbool_test,\n'
                       f'\ttimestamp_test\n'
                       f')\n'
                       f'VALUES\n'
                       f'(\n'
                       f"\t'string_theory',\n"
                       f"\t'1234',\n"
                       f"\t'True',\n"
                       f"\t'2000-10-31T01:30:00.000-05:00'\n"
                       f')\n'
                       f'RETURNING *;')

    sqlstr = connection.build_insert_query('test_table', parameters)

    assert sqlstr == expected_sqlstr


def test_build_select_by_id_query():
    connection = PGConnection()

    id = '123abc'

    expected_sqlstr: str = (f'SELECT * FROM test_table\n'
                            f"WHERE id = '123abc';")

    sqlstr = connection.build_select_by_id_query('test_table', id)

    assert sqlstr == expected_sqlstr


def test_build_select_query():
    connection = PGConnection()

    search_terms: list[SearchTerm] = []

    exact_match_search_term = ExactMatchSearchTerm('test_col_exact', 1234)

    like_match_search_term = LikeSearchTerm('test_col_like', 'likesearch',
                                            LikeComparatorModes.Like)

    in_list_match_search_term = InListSearchTerm('test_col_list',
                                                 ['abc', 'def', 'ghi'], False)

    range_match_search_term = RangeSearchTerm('test_col_range', 111, 222,
                                              False)

    search_terms.append(exact_match_search_term)
    search_terms.append(like_match_search_term)
    search_terms.append(in_list_match_search_term)
    search_terms.append(range_match_search_term)

    expected_sqlstr: str = (
        f'SELECT * FROM test_table\n'
        f'WHERE\n'
        f'(\n'
        f"\t(test_col_exact = '1234')\n"
        f'\tAND\n'
        f"\t(test_col_like LIKE '%likesearch%')\n"
        f'\tAND\n'
        f'\t(test_col_list IN (\n'
        f"\t'abc',\n"
        f"\t'def',\n"
        f"\t'ghi'\n"
        f'))\n'
        f'\tAND\n'
        f"\t(test_col_range >= '111' AND test_col_range <= '222')\n"
        f')\n'
        f'ORDER BY created_at\n'
        f'OFFSET 0 LIMIT 25;')

    sqlstr = connection.build_select_query('test_table', search_terms)

    assert sqlstr == expected_sqlstr


def test_build_select_query_with_uninitialized_paging_fields():
    connection = PGConnection()

    search_terms: list[SearchTerm] = []

    exact_match_search_term = ExactMatchSearchTerm('test_col_exact', 1234)

    paging = PagingModel()

    like_match_search_term = LikeSearchTerm('test_col_like', 'likesearch',
                                            LikeComparatorModes.Like)

    in_list_match_search_term = InListSearchTerm('test_col_list',
                                                 ['abc', 'def', 'ghi'], False)

    range_match_search_term = RangeSearchTerm('test_col_range', 111, 222,
                                              False)

    search_terms.append(exact_match_search_term)
    search_terms.append(like_match_search_term)
    search_terms.append(in_list_match_search_term)
    search_terms.append(range_match_search_term)

    expected_sqlstr: str = (
        f'SELECT * FROM test_table\n'
        f'WHERE\n'
        f'(\n'
        f"\t(test_col_exact = '1234')\n"
        f'\tAND\n'
        f"\t(test_col_like LIKE '%likesearch%')\n"
        f'\tAND\n'
        f'\t(test_col_list IN (\n'
        f"\t'abc',\n"
        f"\t'def',\n"
        f"\t'ghi'\n"
        f'))\n'
        f'\tAND\n'
        f"\t(test_col_range >= '111' AND test_col_range <= '222')\n"
        f')\n'
        f'ORDER BY created_at\n'
        f'OFFSET 0 LIMIT 25;')

    sqlstr = connection.build_select_query('test_table', search_terms, paging)

    assert sqlstr == expected_sqlstr


def test_build_select_query_with_set_paging_fields():
    connection = PGConnection()

    search_terms: list[SearchTerm] = []

    exact_match_search_term = ExactMatchSearchTerm('test_col_exact', 1234)

    paging = PagingModel(
        is_sort_descending=True,
        page=12,
        page_length=5,
        sort_by='sortablecolumn',
    )

    like_match_search_term = LikeSearchTerm('test_col_like', 'likesearch',
                                            LikeComparatorModes.Like)

    in_list_match_search_term = InListSearchTerm('test_col_list',
                                                 ['abc', 'def', 'ghi'], False)

    range_match_search_term = RangeSearchTerm('test_col_range', 111, 222,
                                              False)

    search_terms.append(exact_match_search_term)
    search_terms.append(like_match_search_term)
    search_terms.append(in_list_match_search_term)
    search_terms.append(range_match_search_term)

    expected_sqlstr: str = (
        f'SELECT * FROM test_table\n'
        f'WHERE\n'
        f'(\n'
        f"\t(test_col_exact = '1234')\n"
        f'\tAND\n'
        f"\t(test_col_like LIKE '%likesearch%')\n"
        f'\tAND\n'
        f'\t(test_col_list IN (\n'
        f"\t'abc',\n"
        f"\t'def',\n"
        f"\t'ghi'\n"
        f'))\n'
        f'\tAND\n'
        f"\t(test_col_range >= '111' AND test_col_range <= '222')\n"
        f')\n'
        f'ORDER BY sortablecolumn DESC\n'
        f'OFFSET 55 LIMIT 5;')

    sqlstr = connection.build_select_query('test_table', search_terms, paging)

    assert sqlstr == expected_sqlstr


def test_build_select_query_with_bad_paging_fields():
    connection = PGConnection()

    search_terms: list[SearchTerm] = []

    exact_match_search_term = ExactMatchSearchTerm('test_col_exact', 1234)

    paging = PagingModel(
        is_sort_descending=True,
        page=-1,
        page_length=1005,
        sort_by='sortablecolumn',
    )

    like_match_search_term = LikeSearchTerm('test_col_like', 'likesearch',
                                            LikeComparatorModes.Like)

    in_list_match_search_term = InListSearchTerm('test_col_list',
                                                 ['abc', 'def', 'ghi'], False)

    range_match_search_term = RangeSearchTerm('test_col_range', 111, 222,
                                              False)

    search_terms.append(exact_match_search_term)
    search_terms.append(like_match_search_term)
    search_terms.append(in_list_match_search_term)
    search_terms.append(range_match_search_term)

    expected_sqlstr: str = (
        f'SELECT * FROM test_table\n'
        f'WHERE\n'
        f'(\n'
        f"\t(test_col_exact = '1234')\n"
        f'\tAND\n'
        f"\t(test_col_like LIKE '%likesearch%')\n"
        f'\tAND\n'
        f'\t(test_col_list IN (\n'
        f"\t'abc',\n"
        f"\t'def',\n"
        f"\t'ghi'\n"
        f'))\n'
        f'\tAND\n'
        f"\t(test_col_range >= '111' AND test_col_range <= '222')\n"
        f')\n'
        f'ORDER BY sortablecolumn DESC\n'
        f'OFFSET 0 LIMIT 1000;')

    sqlstr = connection.build_select_query('test_table', search_terms, paging)

    assert sqlstr == expected_sqlstr


def test_build_update_query():
    connection = PGConnection()

    id = '123abc'

    parameters: dict[str, Any] = {
        'string_test': 'string_theory',
        'int_test': 1234,
        'bool_test': True,
        'timestamp_test': '2000-10-31T01:30:00.000-05:00',
    }

    expected_sqlstr = (f'UPDATE test_table\n'
                       f'SET\n'
                       f"\tstring_test = 'string_theory',\n"
                       f"\tint_test = '1234',\n"
                       f"\tbool_test = 'True',\n"
                       f"\ttimestamp_test = '2000-10-31T01:30:00.000-05:00'\n"
                       f"WHERE id = '123abc'\n"
                       f'RETURNING *;')

    sqlstr = connection.build_update_query('test_table', id, parameters)

    assert sqlstr == expected_sqlstr


def test_build_delete_query():
    connection = PGConnection()

    id = '123abc'

    expected_sqlstr: str = (f'DELETE FROM test_table\n'
                            f"WHERE id = '123abc'\n"
                            f'RETURNING *;')

    sqlstr = connection.build_delete_query('test_table', id)

    assert sqlstr == expected_sqlstr
