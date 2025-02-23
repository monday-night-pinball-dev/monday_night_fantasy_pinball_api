from typing import Any
from uuid import UUID
from util.common import RequestOperators
from util.database import PagingModel

class Hydrator:
    def reduce_hydration_tokens(
        self, 
        string: str,
        target: str
    ) -> str:
        if(string==target):
            return ""
        else:
            tokens = string.split(".")
            reduced_tokens = [x for i, x in enumerate(tokens) if i > 0]
            reduced_string = ".".join(reduced_tokens)
            return reduced_string
        
    def seek_hydration_and_reduce(self, target: str, hydration: list[str]):
         
        list_of_reduced_strings = [self.reduce_hydration_tokens(x,target) for x in hydration if x.startswith(f"{target}.") or x == target]
        
        return list_of_reduced_strings
      
    def hydrate_target(
        self, 
        target_name: str, 
        parent_models: list[Any],
        search_model: Any,
        search_function: callable,
        hydration: list[str]
    ) -> None:
        if(hydration is None):
            return
        
        sub_hydration_list = self.seek_hydration_and_reduce(target_name, hydration)
            
        if(len(sub_hydration_list) > 0):
            
            sub_hydration_list_with_root_removed = [x for x in sub_hydration_list if x != target_name]
            
            sub_operators : RequestOperators = RequestOperators(skip_paging=True)
            
            if(len(sub_hydration_list_with_root_removed) > 0): 
                sub_operators.hydration = [x for x in sub_hydration_list_with_root_removed]
             
            target_ids = [parent_model.__dict__[f"{target_name}_id"] for parent_model in parent_models if parent_model.__dict__[f"{target_name}_id"] is not None]
            
            search_model.ids = target_ids
            
            existing_children = search_function(search_model, None, sub_operators)
            
            existing_children_dict : dict[UUID, Any]= {child.id : child for child in existing_children.items}
            
            for parent_model in parent_models: 
                existing_child = existing_children_dict[parent_model.__dict__[f"{target_name}_id"]] if parent_model.__dict__[f"{target_name}_id"] is not None else None 
                parent_model.__dict__[target_name] = existing_child