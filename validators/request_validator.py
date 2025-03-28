import globals.request_globals as request_globals
import logger.error_handlers as error_handlers
import logger.logger as log
import datetime


# Validators
def validate_event_request(app, request_json):
    log.log_info_validation(
        app,
        "Validate event request start",
        request_json
    )
    if not request_json or not isinstance(request_json, dict):
        log.log_info_validation(
            app,
            "Event Validation Invalid Payload",
            request_json)
        return error_handlers.error_response_builder(
            'Invalid Payload',
            400,
            'No JSON Payload Provided',
            datetime.datetime.now().isoformat()
            )
    fields_exist_result = fields_exist(
        request_json, request_globals.Event_POST_Payload)
    if fields_exist_result is not True:
        return error_handlers.error_response_builder(
            'Missing Fields',
            400,
            'Missing field "{}"'.format(
                fields_exist_result),
            datetime.datetime.now().isoformat()
        )
    if not field_accepted_entries_check(
        request_json,
        'type',
        request_globals.Accepted_Transaction_Types
    ):
        return error_handlers.error_response_builder(
            'Invalid Transaction Type',
            400,
            'Transaction Type must be {}'.format(
                request_globals.Accepted_Transaction_Types),
            datetime.datetime.now().isoformat()
        )
    log.log_info_validation(
        app,
        "Validate event request end",
        request_json
    )
    return None


# Generic validation helper functions
def fields_exist(request_json, fields):
    for field in fields:
        if field not in request_json:
            return field
    return True


def field_accepted_entries_check(request_json, field, accepted_entries):
    if request_json[field] not in accepted_entries:
        return False
    return True
