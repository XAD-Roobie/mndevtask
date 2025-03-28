import event_post_handler
from flask import Flask

app = Flask(__name__)
app.uuid = "test"


def test_event_post_handler():
    data = {
        "user_id": 1337,
        "type": "deposit",
        "amount": 1000,
        "t": 0
    }
    assert event_post_handler.event_post_handler(app, data) is None


def test_event_post_handler_new_user_error():
    data = {
        "user_id": "test",
        "type": "deposit",
        "amount": 1000,
        "t": 0
    }
    assert event_post_handler.event_post_handler(app, data) is not None