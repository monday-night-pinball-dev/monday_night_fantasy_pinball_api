from datetime import datetime
from typing import Any, cast
from uuid import UUID
import psycopg2
import psycopg2.pool

from util.common import RequestOperators
from util.database import PagingModel, ResultantPagingModel, SearchTerm


class SqlStringAndParameters:
    def __init__(self, sql_string: str, parameters: dict[str, Any]) -> None:
        self.sql_string = sql_string
        self.parameters = parameters or {}


class BuildSelectQueryResults:
    def __init__(
        self,
        sql_string_and_parameters: SqlStringAndParameters,
        paging: ResultantPagingModel,
    ) -> None:
        self.sql_string_and_parameters = sql_string_and_parameters
        self.paging = paging


class SelectQueryResults:
    def __init__(
        self,
        paging: ResultantPagingModel,
        items: list[dict[str, Any]] | None = None,
    ) -> None:
        self.paging = paging
        self.items = items or []


class PGConnection:
    pool: psycopg2.pool.SimpleConnectionPool

    def create_connection_pool(
        self, host: str, port: str, database: str, username: str, password: str
    ) -> None:
        self.pool = psycopg2.pool.SimpleConnectionPool(
            minconn=2,
            maxconn=50,
            user=username,
            password=password,
            host=host,
            port=port,
            database=database,
        )

    def map_result_columns_to_values(
        self, column_names: list[str], record: tuple[Any, ...]
    ) -> dict[str, Any]:
        returndict: dict[str, Any] = {}

        for i, column_name in enumerate(column_names):
            returndict[column_name] = record[i]

        return returndict

    def execute_command(self, sqlstring: str) -> None:
        conn = self.pool.getconn()
        cursor = conn.cursor()

        try:
            cursor.execute(sqlstring)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            self.pool.putconn(conn)

    def execute_command_with_results(self, sqlstring: str) -> list[tuple[Any, ...]]:
        conn = self.pool.getconn()
        cursor = conn.cursor()

        try:
            cursor.execute(sqlstring)

            conn.commit()

            records = cursor.fetchall()

            return records
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            self.pool.putconn(conn)

    def insert(
        self,
        table_name: str,
        model: dict[str, Any],
        request_operators: RequestOperators | None = None,
    ) -> dict[str, Any]:
        conn = self.pool.getconn()
        cursor = conn.cursor()

        try:
            sql_string_and_parameters = self.build_insert_query(
                table_name=table_name, model=model, request_operators=request_operators
            )

            cursor.execute(
                sql_string_and_parameters.sql_string,
                sql_string_and_parameters.parameters,
            )

            conn.commit()

            rows = cursor.fetchall()

            columns = cursor.description

            if columns is None or rows is None or len(rows) != 1:
                raise

            colnames: list[str] = [desc[0] for desc in columns]

            returndict = self.map_result_columns_to_values(colnames, rows[0])

            return returndict

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            conn.close()
            self.pool.putconn(conn)

    def select_by_id(
        self,
        table_name: str,
        id: UUID,
        request_operators: RequestOperators | None = None,
    ) -> dict[str, Any] | None:
        conn = self.pool.getconn()
        cursor = conn.cursor()

        try:
            sqlstring = self.build_select_by_id_query(
                table_name=table_name, id=id, request_operators=request_operators
            )

            cursor.execute(sqlstring)

            rows = cursor.fetchall()

            columns = cursor.description

            if columns is None:
                raise

            if len(rows) == 0:
                return None

            colnames: list[str] = [desc[0] for desc in columns]

            returndict = self.map_result_columns_to_values(colnames, rows[0])

            return returndict

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            conn.close()
            self.pool.putconn(conn)

    def select(
        self,
        table_name: str,
        search_terms: list[SearchTerm],
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None,
    ):
        conn = self.pool.getconn()
        cursor = conn.cursor()

        try:
            build_query_results = self.build_select_query(
                table_name=table_name,
                search_terms=search_terms,
                paging_model=paging_model,
                request_operators=request_operators,
            )

            print(
                f"Executing SQL: {build_query_results.sql_string_and_parameters.sql_string}"
            )

            cursor.execute(
                build_query_results.sql_string_and_parameters.sql_string,
                build_query_results.sql_string_and_parameters.parameters,
            )

            rows = cursor.fetchall()

            columns = cursor.description

            if columns is None:
                raise

            colnames: list[str] = [desc[0] for desc in columns]

            print(f"Column names for {table_name}: {colnames}")

            total_count_index = colnames.index("_count_")

            returnitemlist: SelectQueryResults = SelectQueryResults(
                build_query_results.paging
            )

            if rows is None or len(rows) == 0:
                returnitemlist.paging.total_record_count = 0
            else:
                returnitemlist.paging.total_record_count = rows[0][total_count_index]

            for row in rows:
                returnitemlist.items.append(
                    self.map_result_columns_to_values(colnames, row)
                )

            return returnitemlist
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            self.pool.putconn(conn)

    def update(
        self,
        table_name: str,
        id: UUID,
        model: dict[str, Any],
        request_operators: RequestOperators | None = None,
    ) -> dict[str, Any] | None:
        # Eliminate nulls

        conn = self.pool.getconn()
        cursor = conn.cursor()

        try:
            refined_model = dict[str, Any]()

            for x in model.keys():
                if model[x] is not None:
                    refined_model[x] = model[x]

            # if nothing to update, just select by id
            if len(refined_model) == 0:
                returndict = self.select_by_id(table_name, id)
                return returndict

            else:
                refined_model["updated_at"] = datetime.utcnow()

            results = self.build_update_query(
                table_name=table_name,
                id=id,
                model=refined_model,
                request_operators=request_operators,
            )

            cursor.execute(results.sql_string, results.parameters)

            conn.commit()

            rows = cursor.fetchall()

            columns = cursor.description

            if columns is None:
                raise

            if len(rows) == 0:
                return None

            colnames: list[str] = [desc[0] for desc in columns]

            returndict = self.map_result_columns_to_values(colnames, rows[0])

            return returndict

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            self.pool.putconn(conn)

    def delete(
        self,
        table_name: str,
        id: UUID,
        request_operators: RequestOperators | None = None,
    ) -> dict[str, Any] | None:
        conn = self.pool.getconn()
        cursor = conn.cursor()

        try:
            sqlstring = self.build_delete_query(
                table_name=table_name, id=id, request_operators=request_operators
            )

            cursor.execute(sqlstring)

            conn.commit()

            rows = cursor.fetchall()

            columns = cursor.description

            if columns is None:
                raise

            if len(rows) == 0:
                return None

            colnames: list[str] = [desc[0] for desc in columns]

            returndict = self.map_result_columns_to_values(colnames, rows[0])

            return returndict

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            self.pool.putconn(conn)

    def build_insert_query(
        self,
        table_name: str,
        model: dict[str, Any],
        request_operators: RequestOperators | None = None,
    ) -> SqlStringAndParameters:
        sqlstring: str = f"INSERT INTO {table_name}\n(\n"

        keys = [key for key in model.keys() if model[key] is not None]

        # Columns

        for i, key in enumerate(keys):
            sqlstring += f"\t{key}"

            if i < len(keys) - 1:
                sqlstring += ","

            sqlstring += f"\n"

        sqlstring += f")\n"
        sqlstring += f"VALUES\n"
        sqlstring += f"(\n"

        # Values

        for i, key in enumerate(keys):
            sqlstring += f"\t%({key})s"

            if i < len(keys) - 1:
                sqlstring += ","

            sqlstring += f"\n"

        sqlstring += f")\nRETURNING *;"

        # Parameters
        parameters: dict[str, any] = {}

        for i, key in enumerate(keys):
            parameters[key] = model[key]

        result = SqlStringAndParameters(sql_string=sqlstring, parameters=parameters)

        return result

    def build_select_query(
        self,
        table_name: str,
        search_terms: list[SearchTerm],
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None,
    ) -> BuildSelectQueryResults:
        skip_paging: bool = (
            request_operators.skip_paging if request_operators is not None else False
        )

        parameters: dict[str, Any] = {}

        if paging_model is None:
            paging_model = PagingModel(
                is_sort_descending=False,
                page=1,
                page_length=25,
                sort_by="created_at",
            )

        page = (
            1
            if paging_model.page is None or paging_model.page < 1
            else paging_model.page
        )

        page_length = 25
        if paging_model.page_length is None:
            page_length = 25
        elif paging_model.page_length < 0:
            page_length = 1
        elif paging_model.page_length > 1000:
            page_length = 1000
        else:
            page_length = paging_model.page_length

        offset = page_length * (page - 1)

        sort_by = paging_model.sort_by or "created_at"
        is_sort_descending = True if paging_model.is_sort_descending == True else False

        resultant_paging_model = ResultantPagingModel(
            page=page,
            page_length=page_length,
            sort_by=sort_by,
            is_sort_descending=is_sort_descending,
        )

        sqlstring: str = f"SELECT *, count(*) over() as _count_ FROM {table_name}\n"

        if len(search_terms) > 0:
            sqlstring += f"WHERE\n(\n"

            for i, search_term in enumerate(search_terms):
                sqlstring += f"\t({search_term.generate_sql(parameters)})\n"
                sqlstring += "\tAND\n" if (i < len(search_terms) - 1) else ""

            sqlstring += f")\n"

        sqlstring += f"ORDER BY {sort_by}"

        if is_sort_descending:
            sqlstring += " DESC"

        if not skip_paging:
            sqlstring += f"\nOFFSET {offset} LIMIT {page_length}"

        sqlstring += ";"

        return_object = BuildSelectQueryResults(
            SqlStringAndParameters(sql_string=sqlstring, parameters=parameters),
            paging=resultant_paging_model,
        )

        return return_object

    def build_select_by_id_query(
        self,
        table_name: str,
        id: UUID,
        request_operators: RequestOperators | None = None,
    ) -> str:
        sqlstring: str = f"SELECT * FROM {table_name}\nWHERE id = '{id}';"

        return sqlstring

    def build_update_query(
        self,
        table_name: str,
        id: UUID,
        model: dict[str, Any],
        request_operators: RequestOperators | None = None,
    ) -> SqlStringAndParameters:
        sqlstring: str = f"UPDATE {table_name}\nSET\n"
        keys = model.keys()

        for i, key in enumerate(keys):
            sqlstring += f"\t{key} = %({key})s"
            if i < len(keys) - 1:
                sqlstring += ","
            sqlstring += "\n"

        sqlstring += f"WHERE id = '{id}'\nRETURNING *;"

        # Parameters
        parameters: dict[str, Any] = {}

        for i, key in enumerate(keys):
            parameters[key] = model[key]

        results = SqlStringAndParameters(sql_string=sqlstring, parameters=parameters)

        return results

    def build_delete_query(
        self,
        table_name: str,
        id: UUID,
        request_operators: RequestOperators | None = None,
    ) -> str:
        sqlstring: str = f"DELETE FROM {table_name}\nWHERE id = '{id}'\nRETURNING *;"

        return sqlstring
