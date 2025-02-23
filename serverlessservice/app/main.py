# api-stack/src/api.py

import os
from mangum import Mangum
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routes.sales_intake_job_routes import set_sales_intake_job_routes
from routes.sales_intake_batch_job_routes import set_sales_intake_batch_job_routes
from routes.inventory_intake_job_routes import set_inventory_intake_job_routes
from routes.inventory_intake_batch_job_routes import set_inventory_intake_batch_job_routes
from routes.inventory_product_snapshot_routes import set_inventory_product_snapshot_routes
from routes.pos_integration_call_routes import set_pos_integration_call_routes
from routes.pos_simulator_response_routes import set_pos_simulator_response_routes
from routes.product_routes import set_product_routes
from routes.user_routes import set_user_routes
from routes.utility_routes import set_utility_routes
from routes.pos_integration_routes import set_pos_integration_routes
from routes.vendor_routes import set_vendor_routes
from routes.retailer_routes import set_retailer_routes
from routes.retailer_location_routes import set_retailer_location_routes
from routes.historical_sale_routes import set_historical_sale_routes
from routes.historical_sale_item_routes import set_historical_sale_item_routes

from util.environment import Environment
 
enviroment: Environment = Environment() 
 
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../.env')

enviroment.setup_environment(env_path)

app = FastAPI(
    title="Samson Core Api",
    description="Core Data Service for the Samson ICS.",
    version="0.0.1",
    docs_url='/docs',
    openapi_url='/openapi.json', 
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if(enviroment.configuration.STAGE != 'local'):
    app.root_path = "/prod"
 
set_utility_routes(app)
set_retailer_routes(app)
set_retailer_location_routes(app)
set_user_routes(app)
set_vendor_routes(app)
set_pos_integration_routes(app)
set_pos_integration_call_routes(app)    
set_pos_simulator_response_routes(app)

set_product_routes(app)
set_inventory_intake_job_routes(app)
set_inventory_intake_batch_job_routes(app)
set_sales_intake_job_routes(app)
set_sales_intake_batch_job_routes(app)
set_inventory_product_snapshot_routes(app)
set_historical_sale_routes(app)
set_historical_sale_item_routes(app)


if __name__ == '__main__' and enviroment.configuration.STAGE == 'local':
    uvicorn.run(app, host='0.0.0.0', port=8001)
    
else:
    handler = Mangum(app, lifespan="off")