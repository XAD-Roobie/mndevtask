import database_functions.database_get_functions as db_get
import sqlite3
import logger.logger as log
import logger.error_handlers as error_handlers
from globals import request_globals
import datetime

# Alert config variables
# Withdrawal threshold amount to fire an alert
max_withdrawal_threshold = 100

# Number of withdrawals to fire an alert
max_consecutive_withdrawals = 3

# Number of consecutive increasing deposits
max_consecutive_increasing_deposits = 3

# Accumulative deposits checks
max_accumulative_deposit_amount = 200
max_accumulative_deposit_duration = 30

# Cutoff point to avoid checking the entire events list
max_db_entry_checks = 15


def check_for_alerts(app, user_id):
    alerts = []
    try:
        conn = sqlite3.connect('database.db')
        log.log_info_post(app, 'Connection to db established ', __name__)
        cursor = conn.cursor()
        events = db_get.get_events(cursor, user_id)
        alerts = []
        alerts.append(withdraw_threshold_check(events[-1]))
        alerts.append(consecutive_withdrawal_check(events))
        alerts.append(consecutive_increasing_deposits(events))
        alerts.append(accumulative_deposit_amount_check(events))
        alerts = list(filter(None, alerts))
        if alerts:
            log.log_info_post(
                app,
                "Detected {} alerts for user {}".format(len(alerts), user_id),
                __name__)
        conn.close()
    except Exception as e:
        log.log_error_post(app, "Unhandled Exception", e.with_traceback)
        return error_handlers.error_response_builder(
            'Internal Server Error',
            500,
            'Internal Server Error',
            datetime.datetime.now().isoformat()
            )
    return alerts


def withdraw_threshold_check(event):
    return_code = None
    if (
        event[1] == request_globals.Accepted_Transaction_Types[1]
        and event[2] > max_withdrawal_threshold
    ):
        return_code = 1100
    return return_code


def consecutive_withdrawal_check(events):
    count = 0
    return_code = None
    for event in events[-3:]:
        if event[1] == request_globals.Accepted_Transaction_Types[1]:
            count += 1
            if count == 3:
                return_code = 30
        else:
            count = 0
    return return_code


def consecutive_increasing_deposits(events):
    count = 0
    current_deposit = 0
    return_code = None
    for event in events[-3:]:
        if event[1] == request_globals.Accepted_Transaction_Types[0]:
            if event[2] > current_deposit:
                count += 1
            if count == 3:
                return_code = 300
                break
            current_deposit = event[2]
        else:
            break
    return return_code


def accumulative_deposit_amount_check(events):
    deposit_total = 0
    deposit_start_time = events[-1][4]
    return_code = None
    for event in reversed(events):
        if event[1] != request_globals.Accepted_Transaction_Types[0]:
            continue
        if deposit_start_time - event[4] > max_accumulative_deposit_duration:
            break
        deposit_total += event[2]
        if deposit_total > max_accumulative_deposit_amount:
            return_code = 123
            break
    return return_code
