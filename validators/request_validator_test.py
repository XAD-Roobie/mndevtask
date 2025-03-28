from validators import request_validator as v
from flask import Flask

app = Flask(__name__)
app.uuid = "test"


def test_validator_event_request_happy():
    request = {
        "user_id": "test",
        "type": "deposit",
        "amount": 1000,
        "t": 0
    }
    assert v.validate_event_request(app, request) is None
    request = {
        "user_id": "test",
        "type": "withdraw",
        "amount": 1000,
        "t": 0
    }
    assert v.validate_event_request(app, request) is None


def test_validator_event_request_no_data():
    request = {}
    assert v.validate_event_request(app, request) is not None


def test_validator_event_request_missing_field():
    request = {
        "type": "deposit",
        "amount": 1000,
        "t": 0
    }
    assert v.validate_event_request(app, request) is not None
    request = {
        "user_id": "test",
        "amount": 1000,
        "t": 0
    }
    assert v.validate_event_request(app, request) is not None
    request = {
        "user_id": "test",
        "type": "deposit",
        "t": 0
    }
    assert v.validate_event_request(app, request) is not None
    request = {
        "user_id": "test",
        "type": "deposit",
        "amount": 1000
    }
    assert v.validate_event_request(app, request) is not None


def test_validator_event_request_invalid_type():
    request = {
        "user_id": "test",
        "type": "invalid",
        "amount": 1000,
        "t": 0
    }
    assert v.validate_event_request(app, request) is not None