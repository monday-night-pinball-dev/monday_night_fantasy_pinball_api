from pprint import pprint
from common.configuration import Configuration 

from common.connection import PGConnection

class Environment:

    pg_connection = PGConnection()
    configuration = Configuration()

    def setup_environment(self, configuration_path: str):

        self.configuration.populate_configuration(configuration_path)

        pprint(f"Configuration Loaded: {vars(self.configuration)}")

        # Database Connection

        self.pg_connection.create_connection(
            host = self.configuration.MIGRATOR_POSTGRES_HOST,
            port = self.configuration.MIGRATOR_POSTGRES_PORT,
            database = self.configuration.MIGRATOR_POSTGRES_DB,
            username = self.configuration.MIGRATOR_POSTGRES_USER,
            password = self.configuration.MIGRATOR_POSTGRES_PASSWORD
        )

        print(f"Database Connection Created: { self.pg_connection.connection.get_dsn_parameters()['port'] }")
