from typing import Optional

from pydantic import BaseModel


class UpdateUserRequest(BaseModel):
    country: Optional[str]
    sub_platform: Optional[str]
    user_name: Optional[str]
    user_id: Optional[str]
    priority: Optional[int]
