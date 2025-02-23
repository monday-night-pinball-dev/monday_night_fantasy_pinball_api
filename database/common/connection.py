import psycopg2

from common.types import ForeignKeyMetadata, TableMetadata

class PGConnection :

    connection : psycopg2.extensions.connection
    cursor : psycopg2.extensions.cursor
    
    def create_connection(self, host: str, port: str, database: str, username: str, password: str):
    
        self.connection = psycopg2.connect(
            database = database,
            user = username,
            password = password,
            host = host,
            port = port
        )

        self.cursor = self.connection.cursor()

    def execute_command(self, sqlstring: str): 
      
        self.cursor.execute(sqlstring)  
        self.connection.commit()
  
    def execute_command_with_results(self, sqlstring: str): 
      
        self.cursor.execute(sqlstring)  
        self.connection.commit()
 
        records = self.cursor.fetchall()

        return records

    def select(self, tablename: str): 
        sqlstring = (
            f"SELECT * "
            f"FROM {tablename};"
        )

        self.cursor.execute(sqlstring)

        records = self.cursor.fetchall()

        print(f"Selected {records.count} rows from {tablename}")

        return records

    def select_all_tables(self):
        sqlstring: str = (
            f"SELECT * FROM"
            f"\nINFORMATION_SCHEMA.TABLES"
            f"\nWHERE"
            f"\n\tTABLE_SCHEMA='public' and"
            f"\n\tTABLE_TYPE = 'BASE TABLE'"
        )

        records = self.execute_command_with_results(sqlstring)

        tables:list[TableMetadata] = []

        for record in records:
            table: TableMetadata = TableMetadata()
            
            table.table_catalog = record[0]
            table.table_schema = record[1]
            table.table_name = record[2]
            table.table_type = record[3] 

            tables.append(table)

        return tables

        
    def select_all_foreign_keys_for_table(self, table_name: str):
        sqlstring: str = (
            f"SELECT * FROM"
            f"\ninformation_schema.table_constraints"
            f"\nWHERE" 
            f"\n\tconstraint_schema = 'public'"
            f"\n\tAND constraint_type = 'FOREIGN KEY'"
            f"\n\tAND table_name = '{table_name}'"
        )

        records = self.execute_command_with_results(sqlstring)

        fks:list[ForeignKeyMetadata] = []

        for record in records:
            fk = ForeignKeyMetadata() 
            fk.fk_name = record[2]

            fks.append(fk)
             
        return fks
    
    def delete_foreign_key(self, table_name: str, fk_name: str):
        sqlstring: str = (
            f"ALTER TABLE {table_name} DROP CONSTRAINT {fk_name}"
        )

        records = self.execute_command(sqlstring)

        return records
    
    def delete_all_rows_from_table(self, table_name: str):
        sqlstring: str = (
            f"DELETE FROM {table_name}"
        )

        records = self.execute_command(sqlstring)

        return records

    def delete_table(self, table_name: str):
        sqlstring: str = (
            f"DROP TABLE {table_name}"
        )

        records = self.execute_command(sqlstring)

        return records
            
    def disable_foreign_keys_on_table(self, table_name: str):
        sqlstring: str = (
            f"ALTER TABLE {table_name} DISABLE TRIGGER ALL;"
        )

        records = self.execute_command(sqlstring)

        return records
    
    def enable_foreign_keys_on_table(self, table_name: str):
        sqlstring: str = (
            f"ALTER TABLE {table_name} ENABLE TRIGGER ALL;"
        )

        records = self.execute_command(sqlstring)

        return records
            
    
