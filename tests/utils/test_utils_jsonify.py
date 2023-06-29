from app.config import Config
from app.utils import jsonify


def test_jsonify_with_state_and_metadata():
    state = {"key1": "value1", "key2": "value2"}
    metadata = {"meta_key": "meta_value"}
    status = 200
    code = 100
    result = jsonify(state, metadata, status, code)

    expected_data = {
        "key1": "value1",
        "key2": "value2",
        "meta_key": "meta_value",
        "code": 100,
    }
    expected_status = 200

    assert result == (expected_data, expected_status)


def test_jsonify_without_state_and_metadata():
    status = 200
    code = 100
    result = jsonify(status=status, code=code)

    expected_data = {
        "code": 100,
    }
    expected_status = 200

    assert result == (expected_data, expected_status)


def test_jsonify_with_debug_mode_enabled():
    Config.DEBUG = True
    state = {"key1": "value1"}
    status = 200
    code = 101
    result = jsonify(state, status=status, code=code)

    expected_data = {
        "key1": "value1",
        "message": "Unsupported Media Type",
        "code": 101,
    }
    expected_status = 200

    assert result == (expected_data, expected_status)
    Config.DEBUG = False


def test_jsonify_with_debug_mode_disable():
    state = {"key1": "value1"}
    status = 200
    code = 101
    result = jsonify(state, status=status, code=code)

    expected_data = {
        "key1": "value1",
        "message": "Unsupported Media Type",
        "code": 101,
    }
    expected_status = 200

    assert result != (expected_data, expected_status)
