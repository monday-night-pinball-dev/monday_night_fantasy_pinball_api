import os
from pprint import pprint
from common.bighammer import BigHammer

from db_environment import Environment

environment: Environment = Environment()

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

environment.setup_environment(env_path)

big_hammer = BigHammer()

big_hammer.hammer(environment)
