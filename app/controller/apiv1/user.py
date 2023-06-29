from bson import ObjectId

from app.config import Config
from app.models.database import MongoStorage
from app.schema.apiv1 import CreateUserRequest, UpdateUserRequest
from app.schema.apiv1 import UserIdResponse
from app.schema.apiv1 import UserResponse
from app.utils.jsonify import jsonify


class UserController:
    collection_name = Config.COLLECTION_NAME
    collection = MongoStorage(collection_name)

    @staticmethod
    def create_user(platform: str, user: CreateUserRequest) -> dict:
        existing_user = UserController.is_existing_user(platform, user)

        if existing_user:
            if existing_user.get('Error'):
                return jsonify(code=102, status=500, metadata=existing_user)
            return jsonify(code=117, status=409)

        # check fields exist
        if (not user.user_id or user.user_id is None) and (not user.user_name or user.user_name is None) \
                and (not user.link or user.link is None):
            return jsonify(code=105, status=422)
        if not user.country or user.country is None:
            return jsonify(code=105, status=422)
        if not user.sub_platform or user.sub_platform is None:
            return jsonify(code=105, status=422)

        user_data = {
            "country": user.country.strip(),
            "platform": platform,
            "sub_platform": user.sub_platform.strip(),
            "user_id": user.user_id.strip(),
            "user_name": user.user_name.strip(),
            "link": user.link.strip() if user.link else user.link,
            "bio": None,
            "member_count": None,
            "follower_count": None,
            "following_count": None,
            "fetch_ts": None,
            "create_time": None,
            "priority": user.priority,
            "status": "pending",
            "error_message": None,
        }
        result = UserController.collection.insert(user_data)

        if isinstance(result, dict) and result.get('Error'):
            return jsonify(code=102, status=500, metadata=result)

        return jsonify({
            "source_id": str(result.inserted_id)
        })

    @staticmethod
    def get_user_by_id(platform: str, user: UserIdResponse):
        try:
            result = UserController.get_user({"_id": ObjectId(user.user_id), "platform": platform})

            if result is None:
                return jsonify(code=104, status=422)

            result['create_time'] = result.get('_id').generation_time.replace(tzinfo=None).isoformat()
            response = UserResponse(**result) if result else None

            if response is None:
                return jsonify(code=104, status=422)

        except Exception as e:
            return jsonify(code=102, status=500, metadata={"Error": str(e)})
        return jsonify(response.dict())

    @staticmethod
    def get_users_by_platform(platform: str):
        try:
            result = UserController.get_platform({"platform": platform})

            list_users = []
            for user in result:
                user['create_time'] = user.get('_id').generation_time.replace(tzinfo=None).isoformat()
                user["_id"] = str(user.get('_id'))
                list_users.append(user)

            if not list_users:
                return jsonify(code=104, status=422)

        except Exception as e:
            return jsonify(code=102, status=500, metadata={"Error": str(e)})
        return list_users, 200

    @staticmethod
    def inactive_user(platform: str, user: UserIdResponse):
        try:
            result = UserController.get_user({"_id": ObjectId(user.user_id), "platform": platform})
        except Exception as e:
            return jsonify(code=102, status=500, metadata={"Error": str(e)})
        if result:
            try:
                UserController.collection.delete_one({"_id": ObjectId(user.user_id)})
                MongoStorage("inactive_users").insert(result)
            except Exception as e:
                return jsonify(code=102, status=500, metadata={"Error": str(e)})
            return jsonify(metadata={"status": "success inactive user"})

    @staticmethod
    def update_user_fields(platform: str, user_id: UserIdResponse, request: UpdateUserRequest):
        try:
            user = UserController.get_user({"_id": ObjectId(user_id.user_id), "platform": platform})
        except Exception as e:
            return jsonify(code=102, status=500, metadata={"Error": str(e)})
        if not user:
            return jsonify(code=111, status=404, metadata={"message": "User not found"})

        user["country"] = request.country if request.country is not None else user.get('country')
        user["sub_platform"] = request.sub_platform if request.sub_platform is not None else user.get('sub_platform')
        user["user_id"] = request.user_id if request.user_id is not None else user.get('user_id')
        user["user_name"] = request.user_name if request.user_name is not None else user.get('user_name')

        try:
            UserController.collection.update({"_id": ObjectId(user_id.user_id)}, user)
        except Exception as e:
            return jsonify(code=102, status=500, metadata={"Error": str(e)})

        return jsonify(metadata={"message": "User fields updated"})

    @staticmethod
    def is_existing_user(platform, user):
        if user.user_id:
            query = {"user_id": user.user_id.strip(), "platform": platform}
        elif user.user_name:
            query = {"user_name": user.user_name.strip(), "platform": platform}
        else:
            query = {"link": user.link.strip(), "platform": platform}

        return UserController.get_user(query)

    @staticmethod
    def get_user(query):
        return UserController.collection.find_one(query)

    @staticmethod
    def get_platform(query):
        return UserController.collection.find_all(query)
