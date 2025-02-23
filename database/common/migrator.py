from genericpath import isfile
import os
from typing import Any 

from environment import Environment 

class Migrator :

    def migrate(self, environment: Environment):

        file_list: list[str] = os.listdir("./schema")
        

        print(f"Retrieved {len(file_list)} items in ./schema.")
        
        file_list.sort()

        for filehandle in file_list:
            if(isfile(f"./schema/{filehandle}")):
                
                print(f"Executing {filehandle}") 
            
                with open(f"./schema/{filehandle}", 'r') as file:
                    file_content: str = file.read()
                     
                    environment.pg_connection.execute_command(file_content)
 
                        
    
