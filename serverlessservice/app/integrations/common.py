from datetime import datetime, timedelta
 
import json
from uuid import UUID

import requests
    
from managers.managers import Manager
 
class ServiceCaller:
    def __init__(
        self,
        pos_simulator_response_manager : Manager | None = Manager()
    ) -> None:
    
        self.manager = pos_simulator_response_manager
    
    def get(
        self,  
        url: str,
        headers: dict[str, str],
        simulator_response_id : UUID | None = None,
    ) -> requests.Response:
        
        if simulator_response_id is not None: 
            
            response = self.manager.get_pos_simulator_response_by_id(simulator_response_id)

            if(response is None):
                raise Exception(f"Pos Simulator Response with id {simulator_response_id} not found.")
    
            return_response = requests.Response()
            
            return_response.status_code = response.response_status_code
            return_response._content = json.dumps(response.response_body).encode('utf-8')
            
            return return_response
        else:
            
            response = requests.get(url, headers=headers) 
             
            return response
    
    def post(
        self,  
        url: str,
        headers: dict[str, str],
        body: dict[str, str],
        simulator_response_id : UUID | None = None,
    ) -> requests.Response:
        
        requests.post(url, headers=headers, json=body)
        
    def patch(
        self,  
        url: str,
        headers: dict[str, str],
        body: dict[str, str],
        simulator_response_id : UUID | None = None,
    ) -> requests.Response:
        
        requests.patch(url, headers=headers, json=body)
        
    def put(
        self,  
        url: str,
        headers: dict[str, str],
        body: dict[str, str],
        simulator_response_id : UUID | None = None,
    ) -> requests.Response:
        
        requests.put(url, headers=headers, json=body)
    
    def delete(
        self,  
        url: str,
        headers: dict[str, str],
        body: dict[str, str],
        simulator_response_id : UUID | None = None,
    ) -> requests.Response:
        
        requests.delete(url, headers=headers, json=body)
    