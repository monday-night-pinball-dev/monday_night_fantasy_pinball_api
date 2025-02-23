from genericpath import isfile
import os
from typing import Any, cast
import psycopg2

from environment import Environment 

class BigHammer :

    def hammer(self, environment: Environment):

        print("Retrieving All Tables")

        all_tables = environment.pg_connection.select_all_tables()
    
        print(f"Retrieved {len(all_tables)} tables: \n[\n\t{([t.table_name for t in all_tables])}\n]")

        for table in all_tables:
            print(f"Getting all foreign keys on table {table.table_name}...")

            all_foreign_keys = environment.pg_connection.select_all_foreign_keys_for_table(table.table_name) 
 
            print(f"Retrieved {len(all_foreign_keys)} foreign keys on table {table.table_name}: \n[\n\t{([t.fk_name for t in all_foreign_keys])}]\n")

            for fk in all_foreign_keys: 
                print(f"Deleting Foreign Key {fk.fk_name}...")

                environment.pg_connection.delete_foreign_key(table.table_name, fk.fk_name)

                print(f"Deleted Foreign Key {fk.fk_name}")

        for table in all_tables:

            print(f"Deleting all rows from table {table.table_name}...")

            environment.pg_connection.delete_all_rows_from_table(table.table_name) 
            
            print(f"Deleted all rows from table {table.table_name}")

            print(f"Dropping table {table.table_name}...")

            environment.pg_connection.delete_table(table.table_name) 
            
            print(f"Dropped table {table.table_name}")
            
    
