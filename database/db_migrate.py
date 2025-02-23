import os 

from common.migrator import Migrator
from environment import Environment

enviroment: Environment = Environment()

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')

enviroment.setup_environment(env_path)

migrator = Migrator()

migrator.migrate(enviroment)

