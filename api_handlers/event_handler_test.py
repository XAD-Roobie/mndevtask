import event_handler
from flask import Flask

app = Flask(__name__)
app.uuid = "test"


def test_post_event_handler_happy():
    request = {
        "user_id": 1337,
        "type": "deposit",
        "amount": 1000,
        "t": 0
    }
    assert event_handler.post_event_handler(app, request) is None
    request = {
        "user_id": 1337,
        "type": "withdraw",
        "amount": 1000,
        "t": 0
    }
    assert event_handler.post_event_handler(app, request) is None


def test_post_event_handler_error():
    request = {}
    assert event_handler.post_event_handler(app, request) is not None
