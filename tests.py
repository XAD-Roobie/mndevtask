import sqlite3
import requests
from database_functions.database_post_functions import create_user
from database_functions.database_get_functions import check_user_exists

# Contains tests to check for baseline functionality
# Not a subsitute for Unittests

endpoint = "0.0.0.0:1337"
test_user_id = 1337


# Initialisation
def create_user_test():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if check_user_exists(cursor, test_user_id):
        delete_user()
    assert create_user(cursor, test_user_id)
    assert check_user_exists(cursor, test_user_id)


def delete_events_for_user():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM events WHERE user_id = ?', (test_user_id,))
    conn.commit()
    conn.close()


def check_test_user_exists():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    return check_user_exists(cursor, test_user_id)


def delete_user():
    delete_events_for_user()
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE user_id = ?', (test_user_id,))
    conn.commit()
    conn.close()


def validate_latest_event(amount):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events WHERE user_id = ?', (test_user_id,))
    events = cursor.fetchall()
    assert events[-1][2] == amount
    conn.close()


# Flow tests
def test_deposit_event():
    amount = 1
    response = requests.post(
        f"http://{endpoint}/event",
        json={
            "type": "deposit",
            "amount": amount,
            "user_id": test_user_id,
            "t": 0},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert not response_json["alert"]
    assert not response_json["alert_codes"]
    assert response_json["user_id"] == test_user_id

    validate_latest_event(amount)
    delete_events_for_user()


def test_withdraw_event():
    amount = 1
    response = requests.post(
        f"http://{endpoint}/event",
        json={
            "type": "withdraw",
            "amount": amount,
            "user_id": test_user_id,
            "t": 0},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert not response_json["alert"]
    assert not response_json["alert_codes"]
    assert response_json["user_id"] == test_user_id

    validate_latest_event(amount)
    delete_events_for_user()


def test_code_1100():
    amount = 101
    response = requests.post(
        f"http://{endpoint}/event",
        json={
            "type": "withdraw",
            "amount": amount,
            "user_id": test_user_id,
            "t": 0},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["alert"]
    assert response_json["alert_codes"] == [1100]
    assert response_json["user_id"] == test_user_id

    validate_latest_event(amount)
    delete_events_for_user()


def test_code_30():
    max_range = 3
    for i in range(max_range-1):
        amount = 1
        response = requests.post(
            f"http://{endpoint}/event",
            json={
                "type": "withdraw",
                "amount": amount,
                "user_id": test_user_id,
                "t": i},
        )
        assert response.status_code == 200
        response_json = response.json()
        assert not response_json["alert"]
        assert not response_json["alert_codes"]
        assert response_json["user_id"] == test_user_id

        validate_latest_event(amount)

    amount = 1
    response = requests.post(
        f"http://{endpoint}/event",
        json={
            "type": "withdraw",
            "amount": amount,
            "user_id": test_user_id,
            "t": max_range},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["alert"]
    assert response_json["alert_codes"] == [30]
    assert response_json["user_id"] == test_user_id

    validate_latest_event(amount)
    delete_events_for_user()


def test_code_300():
    max_range = 3
    amount = 1
    for i in range(max_range-1):
        response = requests.post(
            f"http://{endpoint}/event",
            json={
                "type": "deposit",
                "amount": amount,
                "user_id": test_user_id,
                "t": i},
        )
        assert response.status_code == 200
        response_json = response.json()
        assert not response_json["alert"]
        assert not response_json["alert_codes"]
        assert response_json["user_id"] == test_user_id

        validate_latest_event(amount)

        amount += 1
    response = requests.post(
        f"http://{endpoint}/event",
        json={
            "type": "deposit",
            "amount": amount,
            "user_id": test_user_id,
            "t": max_range},
        )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["alert"]
    assert response_json["alert_codes"] == [300]
    assert response_json["user_id"] == test_user_id

    validate_latest_event(amount)
    delete_events_for_user()


def test_code_123():
    max_range = 2
    for i in range(max_range):
        amount = i*150
        response = requests.post(
            f"http://{endpoint}/event",
            json={
                "type": "deposit",
                "amount": amount,
                "user_id": test_user_id,
                "t": i},
        )
        assert response.status_code == 200
        response_json = response.json()
        if amount >= 200:
            assert response_json["alert"]
            assert response_json["alert_codes"] == [123]
        validate_latest_event(amount)
    delete_events_for_user()


create_user_test()
test_deposit_event()
test_withdraw_event()
test_code_1100()
test_code_30()
test_code_300()
test_code_123()

delete_user()

print("Test User exists: \n\t{}".format(check_test_user_exists()))

print("Happy tests")
