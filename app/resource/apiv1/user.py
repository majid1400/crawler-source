from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from app.controller.apiv1 import UserController
from app.schema.apiv1 import CreateUserRequest, Platform, UserIdResponse, UpdateUserRequest

router = APIRouter()


@router.post("/{platform}/sources")
async def post(user: CreateUserRequest, platform: Platform):
    user_id = UserController.create_user(platform.value, user)
    return JSONResponse(content=user_id[0], status_code=user_id[1])


@router.get("/{platform}/sources/{source_id}")
async def get(source_id: str, platform: Platform):
    user = UserIdResponse(user_id=source_id)
    result = UserController.get_user_by_id(platform.value, user)
    return JSONResponse(content=result[0], status_code=result[1])


@router.get("/{platform}/sources")
async def get_platform(platform: Platform):
    result = UserController.get_users_by_platform(platform.value)
    return JSONResponse(content=result[0], status_code=result[1])


@router.delete("/{platform}/sources/{source_id}")
async def delete(source_id: str, platform: Platform):
    user = UserIdResponse(user_id=source_id)
    result = UserController.inactive_user(platform.value, user)
    return JSONResponse(content=result[0], status_code=result[1])


@router.put("/{platform}/sources/{source_id}")
async def put(source_id: str, platform: Platform, request: UpdateUserRequest):
    user = UserIdResponse(user_id=source_id)
    result = UserController.update_user_fields(platform, user, request)
    return JSONResponse(content=result[0], status_code=result[1])
