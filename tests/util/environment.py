import json
from pprint import pprint 
from util.configuration import Configuration, set_global_configuration
import builtins
 

class Environment:
 
    configuration = Configuration()

    def setup_environment(self, configuration_path: str = "/.env"):
        # Configuration Init
        self.configuration.populate_configuration(configuration_path) 
 
        pprint(f"Configuration Loaded: {vars(self.configuration)}")

        # Database Connection
 
        set_global_configuration(self.configuration)




    
