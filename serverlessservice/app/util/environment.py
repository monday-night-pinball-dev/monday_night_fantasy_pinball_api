from pprint import pprint
from util.configuration import Configuration, set_global_configuration


class Environment:
    configuration = Configuration()

    def setup_environment(self, configuration_path: str | None = None):
        # Configuration Init
        self.configuration.populate_configuration(configuration_path)

        pprint(f"Configuration Loaded: {vars(self.configuration)}")

        # Database Connection

        self.configuration.setup_pg_connection_pool()

        set_global_configuration(self.configuration)
