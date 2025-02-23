import json
import os
from typing import cast
from dotenv import load_dotenv

from root import ROOT_DIR 

env_path = os.path.join(ROOT_DIR, '.env')

print(f"Loading environment from {env_path}")

class ConfigurationIssue :
   property: str
   message: str

   def generate_missing_required_property_message(self, property: str):
       return f"Required property {property} is missing."


class Configuration :

    API_URL: str 

    def populate_configuration(self, config_path: str = env_path) -> None:


        if os.path.isfile(config_path):
            print(f"Loading configuration from file at {config_path}")
            load_dotenv(config_path)
            # Debug: print environment variables
            print(f"API_URL={os.getenv('API_URL')}")
 
        else:
            print(f"No configuration file found at {config_path}, using existing environment for config values.")

        # Validate
        issues : list[ConfigurationIssue] = []

        required_list = [
            'API_URL' 
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

            print(f"Encountered issues loading the configuration: {issues}")
            raise Exception("Terminated due to invalid configuration.")

        # Load

        self.API_URL = os.getenv('API_URL') or '' 
 
def get_global_configuration():
    return cast(Configuration,globals()['configuration'])

def set_global_configuration(configuration: Configuration):
     globals()['configuration'] = configuration


def populate_configuration_if_not_exists(config_path: str = env_path):
  
    if('configuration' not in globals().keys()):
        config: Configuration = Configuration()

        config.populate_configuration(config_path)

        set_global_configuration(config)