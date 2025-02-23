from abc import abstractmethod
from datetime import datetime
from enum import Enum
import secrets
import string
from typing import Any, Generic, TypeVar
from uuid import UUID
import uuid


class RequestOperators:
    
    def __init__(
        self, 
        hydration: list[str] | None = None,
        skip_paging: bool = False,
    ) -> None:
        
        self.hydration = hydration
        self.skip_paging = skip_paging
    

T_in = TypeVar('T_in')
T_out = TypeVar('T_out')
TRangeSearchable = TypeVar('TRangeSearchable', str, int, float, datetime)
TListSearchable = TypeVar('TListSearchable', str, int, float)


class CommonUtilities:

    def convert_comma_delimited_ids_to_uuid_list(self, value: str | list[str]):
       
        returnlist: list[UUID] = []
        
        str_list: list[str] = []
        
        if isinstance(value, str):
            str_list = value.split(',')
        elif isinstance(value, list):
            str_list = value
      
        for x in str_list:
            returnlist.append(uuid.UUID(x))

        return returnlist

    def validate_comma_delimited_ids(self, ids_string: str | list[str] | None):

        if ids_string is None:
            return None

        errors: dict[int, str] = {}

        ids : list[str] = []
        
        if isinstance(ids_string, str):
            ids = ids_string.split(',')
        elif isinstance(ids_string, list):
            ids = ids_string
        else:
            errors[0] = f'Property must be a valid list of v4 uuids. Could not parse comma delimited ids or list.'
            return errors

        for index, x in enumerate(ids):
            try:
                UUID(x, version=4)
            except ValueError:
                errors[index] = x

        if len(errors.keys()) > 0:
            return errors
        else:
            return None

    def generate_invalid_comma_delimited_ids_message(self, errors):
        message = f'Property must be a valid list of v4 uuids. Invalid values received: ['

        for i, key in enumerate(errors.keys()):

            message += f'\n\t{key}: {errors[key]}'

            if i != len(errors.keys()) - 1:
                message += f','

        message += '\n].'

        return message

    def convert_uuid_list_to_string_list(self, uuids: list[UUID]):
        resultlist = [str(x) for x in uuids]
        return resultlist
    
        
    def generate_random_string(
        self,
        len: int = 12, 
        charset: str | None = None
    ) -> str:
        charset = charset or string.ascii_letters + string.digits

        result = ''.join(secrets.choice(charset) for i in range(len))

        return result