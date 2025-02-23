# api-stack/src/api.py

from mangum import Mangum
from fastapi import FastAPI


def set_utility_routes(app: FastAPI):

    @app.get("/hello")
    def list_items():
        """
        Return a hello hello 
        """
        return {
            'message': 'Hello HELLO hello!'
        }

