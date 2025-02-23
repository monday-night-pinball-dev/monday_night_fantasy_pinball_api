from typing import Generic, TypeVar


class TestContext:
    def __init__(self, 
                 api_url: str) -> None:
        
        self.api_url = api_url

class RequestOperators:
    def __init__(
        self, 
        hydration_properties: list[str] | None = None,
        added_headers: dict[str,str] | None = None, 
        token: str | None = None
    ) -> None:
    
        self.hydration_properties = hydration_properties or []
        self.added_headers = added_headers or {}
        self.token = token or []

T = TypeVar("T")

class PagingRequestModel:
    def __init__(self,
                 page: int | None = None,
                 page_length: int | None = None,
                 is_sort_descending: bool | None = None,
                 sort_by: str | None = None) -> None:
        
        self.page: int | None = page
        self.page_length: int | None = page_length
        self.is_sort_descending: bool | None = is_sort_descending
        self.sort_by: str | None = sort_by 

class PagingResponseModel:
    def __init__(self,
                 page: int,
                 page_length: int,
                 is_sort_descending: bool,
                 sort_by: str | None = None,
                 total_record_count: int | None = None) -> None:
        self.page: int = page
        self.page_length: int = page_length
        self.is_sort_descending: bool = is_sort_descending
        self.sort_by: str | None = sort_by
        self.total_record_count: int | None = total_record_count
         
class PagedResponseItemList(Generic[T]):
    def __init__(self,
                items: list[T],  
                paging: PagingResponseModel) -> None:
        self.items: list[T] = items
        self.paging: PagingResponseModel = paging

