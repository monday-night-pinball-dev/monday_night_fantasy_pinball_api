import os
from typing import cast
from dotenv import load_dotenv

class ConfigurationIssue :
   property: str
   message: str

   def generate_missing_required_property_message(self, property: str):
       return f"Required property {property} is missing."


class Configuration :

    MIGRATOR_POSTGRES_HOST: str
    MIGRATOR_POSTGRES_PORT:  str
    MIGRATOR_POSTGRES_USER:  str
    MIGRATOR_POSTGRES_PASSWORD: str
    MIGRATOR_POSTGRES_DB: str

    def populate_configuration(self, config_path: str = ".env") -> None:

        if os.path.isfile(config_path):
            print(f"Loading configuration from file at {config_path}")
            load_dotenv(config_path)
        else:
            print("No configuration file found at {config_path}, using existing environment for config values.")

            for name, value in os.environ.items():
                print("{0}: {1}".format(name, value))

        # Validate
        issues : list[ConfigurationIssue] = []

        required_list = [
            'MIGRATOR_POSTGRES_HOST',
            'MIGRATOR_POSTGRES_PORT',
            'MIGRATOR_POSTGRES_USER',
            'MIGRATOR_POSTGRES_PASSWORD',
            'MIGRATOR_POSTGRES_DB'
        ]

        for item in required_list:
            property = item
            value = os.getenv(property)

            if(value is None):
                issue = ConfigurationIssue()
                issue.property = 'property'
                issue.message = issue.generate_missing_required_property_message(property)
                issues.append(issue)


        if(len(issues) > 0):
            
            print(f"Encountered issues loading the configuration")
            
            for i,issue in enumerate(issues):
                
                print(f"{i} - Property: {issue.property}, Message: {issue.message}")
                
            raise Exception("Terminated due to invalid configuration.")

        # Load

        self.MIGRATOR_POSTGRES_HOST = os.getenv('MIGRATOR_POSTGRES_HOST') or ''
        self.MIGRATOR_POSTGRES_PORT = os.getenv('MIGRATOR_POSTGRES_PORT')  or ''
        self.MIGRATOR_POSTGRES_USER = os.getenv('MIGRATOR_POSTGRES_USER')  or ''
        self.MIGRATOR_POSTGRES_PASSWORD = os.getenv('MIGRATOR_POSTGRES_PASSWORD')  or ''
        self.MIGRATOR_POSTGRES_DB = os.getenv('MIGRATOR_POSTGRES_DB')  or ''

def get_global_configuration():
    return cast(Configuration,globals()['configuration'])

def set_global_configuration(configuration: Configuration):
     globals()['configuration'] = configuration
