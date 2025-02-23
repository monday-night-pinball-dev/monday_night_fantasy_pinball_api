from managers.managers import Manager
from models.retailer_model import RetailerCreateModel, RetailerModel
from util.common import RequestOperators

def insert(
    self,
    model: RetailerCreateModel,
    request_operators: RequestOperators | None = None
)   -> RetailerModel | None:
    
    
    
    print("This is the insert method")
    return None

def test_build_insert_query_handles_all_types():
    manager = Manager()
    
    manager.retailer_accessor.insert = insert
    
    result = manager.create_retailer(RetailerCreateModel(
        account_status="RegisteredActive",
        contact_email="test@example.com",
        hq_city="test",
        hq_country="test",
        hq_state="test",
        name="test", 
    ))
    
    assert result is None
    
 