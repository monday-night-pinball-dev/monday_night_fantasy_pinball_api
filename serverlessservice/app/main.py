# api-stack/src/api.py

import os
from mangum import Mangum
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routes.fantasy_team_routes import set_fantasy_team_routes
from routes.fantasy_team_season_link_routes import (
    set_fantasy_team_season_link_routes,
)
from routes.league_player_routes import set_league_player_routes
from routes.fantasy_league_routes import set_fantasy_league_routes
from routes.league_team_routes import set_league_team_routes
from routes.venue_routes import set_venue_routes
from routes.season_routes import set_season_routes
from routes.user_routes import set_user_routes
from routes.utility_routes import set_utility_routes

from util.environment import Environment

enviroment: Environment = Environment()

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.env")

enviroment.setup_environment(env_path)

app = FastAPI(
    title="Mnfp Core Data Service",
    description="Core Data Service for the Monday Night Fantasy Pinball application.",
    version="0.0.1",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if enviroment.configuration.STAGE != "local":
    app.root_path = "/prod"


set_league_player_routes(app)
set_league_team_routes(app)
set_utility_routes(app)
set_user_routes(app)
set_venue_routes(app)
set_season_routes(app)
set_fantasy_league_routes(app)
set_fantasy_team_routes(app)
set_fantasy_team_season_link_routes(app)

if __name__ == "__main__" and enviroment.configuration.STAGE == "local":
    uvicorn.run(app, host="0.0.0.0", port=8001)

else:
    handler = Mangum(app, lifespan="off")
