from urllib.parse import urlencode
import requests
from typing import Any, Type, TypeVar

from tests.qdk.types import RequestOperators
from tests.qdk.utils import transform_operators_to_headers

def qa_post(
   url: str,
   body: object, 
   request_operators: RequestOperators | None = None,
):
   request_body: dict[str, Any]

   if(not isinstance(body, dict)):
      request_body = body.__dict__
   else:
      request_body = body
 
   response: requests.Response

   if(request_operators is not None):
      headers: dict[str, str] = transform_operators_to_headers(request_operators)
      response = requests.post(url = url, json = request_body, headers = headers)
   else:
      response = requests.post(url = url, json = request_body)

   return response

def qa_patch(url: str, body: object, request_operators: RequestOperators | None = None):
   request_body: dict[str, Any]

   if(not isinstance(body, dict)):
      request_body = body.__dict__
   else:
      request_body = body
 
   response: requests.Response

   if(request_operators is not None):
      headers: dict[str, str] = transform_operators_to_headers(request_operators)
      response = requests.patch(url = url, json = request_body, headers = headers)
   else:
      response = requests.patch(url = url, json = request_body)

   return response

def qa_get(url: str, query_params: object | None = None, request_operators: RequestOperators | None = None):
   
   query_params = query_params or {}

   params_dict: dict[str, Any] = {}
   
   if(not isinstance(query_params, dict)):
      params_dict.update( (k,v) for k,v in query_params.__dict__.items() if v is not None)
   else:
      params_dict.update((k,v) for k,v in query_params.items() if v is not None)
 
   param_string = urlencode(params_dict)
   
   full_url = url + f"?{param_string}" if len(param_string) > 0 else url

   response: requests.Response

   if(request_operators is not None):
      headers: dict[str, str] = transform_operators_to_headers(request_operators)
      response = requests.get(url = full_url, headers = headers)
   else:
      response = requests.get(url = full_url)

   return response