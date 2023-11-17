import json
import re
from datetime import date
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, EmailStr, ValidationError, validator

from model import *

db_model = FormModel()


class FormData(BaseModel):
    """
    Class to validate data
    """
    form_name: Optional[str]
    order_date: Optional[date]
    phone_number: Optional[str]
    lead_email: Optional[EmailStr]
    text_message: Optional[str]

    @validator("phone_number")
    def validate_phone_number(cls, value) -> str:
        '''
        Validate phone number format.
        '''
        clear_value = re.sub(r'\s', '', str(value))
        if re.match(r'^\+7\d{10}$', clear_value):
            return clear_value
        else:
            raise ValueError("Invalid number format, must be +7 xxx xxx xx xx")


def validate_data(data: Dict[str, Union[str, date, EmailStr]]) -> Union[Dict[str, str], ValidationError]:
    """
    Validate form data.
    """
    try:
        result = FormData(**data)
        return result.model_dump()
    except ValidationError as e:
        return e


def insert_in_db(data: Dict[str, Union[str, date, EmailStr]]) -> str:
    '''
    Insert form data into the database.
    '''
    resp = db_model.insert_new_form(data)
    if resp is not None:
        return 'success'
    else:
        return 'error'


def filtering_incoming_data(data: Dict[str, str]) -> Dict[str, Union[str, date, EmailStr]]:
    '''
    Filter incoming data based on the model.
    '''
    info_model = FormData.__annotations__
    need_data = {key: value for key, value in data.items() if key in info_model}
    return need_data


def search_form(result_filter: Dict[str, str]) -> List[Dict[str, Union[str, date, EmailStr]]]:
    '''
    Search for forms in the database.
    '''
    resp = db_model.search_form(result_filter)
    return resp


def need_views(result_validate: ValidationError) -> Dict[str, str]:
    '''
    Format validation errors.
    '''
    json_data = json.loads(result_validate.json())
    formatted_errors = {error["loc"][0]: error["type"] for error in json_data if error.get("loc")}
    return formatted_errors