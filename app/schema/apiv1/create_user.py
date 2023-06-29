from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, Field, validator


class CreateUserRequest(BaseModel):
    country: str = Field(..., min_length=1)
    sub_platform: str = Field(..., min_length=1)
    priority: int = Field(..., ge=1, le=5)
    user_id: Optional[str]
    user_name: Optional[str]
    link: Optional[str]

    @validator('country')
    def check_country_whitespace(cls, value):
        if value.strip() == '':
            raise HTTPException(status_code=400, detail="Country must not be only whitespace")
        return value

    @validator('sub_platform')
    def check_sub_platform_whitespace(cls, value):
        if value.strip() == '':
            raise HTTPException(status_code=400, detail="sub platform must not be only whitespace")
        return value

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validate_user_fields(**kwargs)

    @staticmethod
    def validate_user_fields(**kwargs):
        if not any([kwargs.get('user_id'), kwargs.get('user_name'), kwargs.get('link')]):
            raise HTTPException(status_code=400,
                                detail="At least one of 'user_id', 'user_name', 'link' fields must have data")
        elif kwargs.get('user_id').strip() == '' and\
                kwargs.get('user_name').strip() == '' and \
                kwargs.get('link').strip() == '':
            raise HTTPException(status_code=400, detail="must not be only whitespace")
