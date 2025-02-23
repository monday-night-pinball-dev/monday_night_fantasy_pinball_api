import os
from typing import cast
from dotenv import load_dotenv

from util.db_connection import PGConnection

class ConfigurationIssue:
    property: str
    message: str

    def generate_missing_required_property_message(self, property: str):
        return f'Required property {property} is missing.'


class Configuration:

    pg_connection = PGConnection()

    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    
    BASE_URL: str
    
    STAGE: str

    def populate_configuration(self, config_path: str | None = None) -> None:

        if os.path.isfile(config_path):
            print(f'Loading configuration from file at {config_path}')
            load_dotenv(config_path)
            # Debug: print environment variables
            print(f"DATABASE_HOST={os.getenv('DATABASE_HOST')}")
            print(f"DATABASE_PORT={os.getenv('DATABASE_PORT')}")
            print(f"DATABASE_USERNAME={os.getenv('DATABASE_USERNAME')}")
            print(f"DATABASE_PASSWORD={os.getenv('DATABASE_PASSWORD')}")
            print(f"DATABASE_NAME={os.getenv('DATABASE_NAME')}")
            print(f"BASE_URL={os.getenv('BASE_URL')}")
             
            print(f"STAGE={os.getenv('STAGE')}")
        else:
            print(
                f'No configuration file found at {config_path}, using existing environment for config values. Values found:'
            )
            
            for name, value in os.environ.items():
                print("{0}: {1}".format(name, value))

        # Validate
        issues: list[ConfigurationIssue] = []

        required_list = [
            'DATABASE_HOST',
            'DATABASE_PORT',
            'DATABASE_USERNAME',
            'DATABASE_PASSWORD',
            'DATABASE_NAME',
            'BASE_URL',
            'STAGE',
        ]

        for item in required_list:
            property = item
            value = os.getenv(property)

            if value is None:
                issue = ConfigurationIssue()
                issue.property = property
                issue.message = (issue.generate_missing_required_property_message(property))
                issues.append(issue)

        if len(issues) > 0:

            print(f'Encountered issues loading the configuration:')
            
            for i,issue in enumerate(issues):
                
                print(f"{i} - Property: {issue.property}, Message: {issue.message}")
                
            raise Exception("Terminated due to invalid configuration.")
        
        # Load

        self.DATABASE_HOST = os.getenv('DATABASE_HOST') or ''
        self.BASE_URL = os.getenv('BASE_URL') or ''
        self.DATABASE_PORT = os.getenv('DATABASE_PORT') or ''
        self.DATABASE_USERNAME = os.getenv('DATABASE_USERNAME') or ''
        self.DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD') or ''
        self.DATABASE_NAME = os.getenv('DATABASE_NAME') or ''
        self.STAGE = os.getenv('STAGE') or ''

    def setup_pg_connection(self):
        self.pg_connection.create_connection(
            host=self.DATABASE_HOST,
            port=self.DATABASE_PORT,
            database=self.DATABASE_NAME,
            username=self.DATABASE_USERNAME,
            password=self.DATABASE_PASSWORD,
        )


def get_global_configuration():
    return cast(Configuration, globals()['configuration'])


def set_global_configuration(configuration: Configuration):
    globals()['configuration'] = configuration
