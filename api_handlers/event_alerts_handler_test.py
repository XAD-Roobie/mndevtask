import event_alerts_handler
from flask import Flask

app = Flask(__name__)
app.uuid = "test"


def test_check_for_alerts_happy():
    assert event_alerts_handler.check_for_alerts(app, 1337) is not None


def test_check_for_alerts_error():
    assert event_alerts_handler.check_for_alerts(app, "test") is not None


def test_withdraw_threshold_check():
    event = ["test", "withdraw", 100]
    assert event_alerts_handler.withdraw_threshold_check(event) is None
    event = ["test", "withdraw", 101]
    assert event_alerts_handler.withdraw_threshold_check(event) == 1100


def test_consecutive_withdrawal_check():
    events = [
        ["test", "withdraw", 1000],
        ["test", "withdraw", 1000],
        ["test", "withdraw", 1000],
        ["test", "deposit", 1000],
    ]
    assert event_alerts_handler.consecutive_withdrawal_check(
        events) is None
    events = [
        ["test", "withdraw", 1000],
        ["test", "withdraw", 1000],
        ["test", "withdraw", 1000],
    ]
    assert event_alerts_handler.consecutive_withdrawal_check(events) == 30


def test_consecutive_increasing_deposits():
    events = [
        ["test", "deposit", 1000],
        ["test", "deposit", 1001],
        ["test", "deposit", 1002],
        ["test", "withdraw", 1000],
    ]
    assert event_alerts_handler.consecutive_increasing_deposits(
        events) is None
    events = [
        ["test", "deposit", 998],
        ["test", "deposit", 999],
        ["test", "deposit", 1000],
    ]
    assert event_alerts_handler.consecutive_increasing_deposits(events) == 300
    events = [
        ["test", "deposit", 1000],
        ["test", "deposit", 1000],
    ]
    assert event_alerts_handler.consecutive_increasing_deposits(events) is None


def test_accumulative_deposit_amount_check():
    events = [
        ["test", "deposit", 99, 0, 0],
        ["test", "deposit", 10, 0, 30],
        ["test", "deposit", 10, 0, 60],
    ]
    assert event_alerts_handler.accumulative_deposit_amount_check(
        events) is None
    events = [
        ["test", "deposit", 50, 0, 1],
        ["test", "deposit", 50, 0, 2],
        ["test", "deposit", 50, 0, 3],
        ["test", "deposit", 50, 0, 4],
        ["test", "deposit", 50, 0, 5],
    ]
    assert event_alerts_handler.accumulative_deposit_amount_check(
        events) == 123
    events = [
        ["test", "deposit", 100, 0, 0],
        ["test", "deposit", 101, 0, 29],
    ]
    assert event_alerts_handler.accumulative_deposit_amount_check(
        events) == 123
