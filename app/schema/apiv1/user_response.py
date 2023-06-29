from typing import List, Union, Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class UserIdResponse(BaseModel):
    user_id: str = Field(..., min_length=1)


class UserResponse(BaseModel):
    _id: ObjectId
    country: str
    platform: str
    sub_platform: Union[str, List[str]]
    user_id: Union[str, None]
    user_name: Union[str, None]
    link: Union[str, None]
    bio: Union[str, None]
    member_count: Union[int, None]
    follower_count: Union[int, None]
    following_count: Union[int, None]
    fetch_ts: Union[int, None]
    create_time: Union[str, None]
    priority: int = Field(..., ge=1, le=5)
    status: str
    error_message: Union[str, None]
