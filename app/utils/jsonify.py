from app.config import Config

DEBUG_MSG_CODES = {
    "100": "OK",
    "101": "Unsupported Media Type",
    "102": "Database Error",
    "103": "Resource Not Found",
    "104": "Request Validation Failed",
    "105": "Empty Data supplied",
    "106": "Resource Conflict",
    "107": "Not Implemented",
    "108": "Resource Expired",
    "109": "Bad Desired Status",
    "110": "Token Encryption Error",
    "111": "Resource Not Matched",
    "112": "Header Not Specified",
    "113": "Token Validation Error",
    "114": "Invalid Token Data",
    "115": "Controller Allowed Roles Not Found",
    "116": "Resource Access Denied",
    "117": "User Already Exists",
}


def jsonify(state=None, metadata=None, status=200, code=100):
    if metadata is None:
        metadata = {}
    if state is None:
        state = {}
    data = state
    data.update(metadata)
    if Config.DEBUG:
        data["message"] = DEBUG_MSG_CODES[str(code)]
    data["code"] = code
    return data, status
