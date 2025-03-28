import sqlite3
import logger.logger as log
from database_functions.database_post_functions import (
    create_event, create_user
)
from database_functions.database_get_functions import check_user_exists
import logger.logger
import datetime


def event_post_handler(app, data):
    try:
        conn = sqlite3.connect('database.db')
        log.log_info_post(app, 'Connection to db established ', __name__)
        cursor = conn.cursor()
        if not check_user_exists(cursor, data['user_id']):
            log.log_warning_post(
                app, 'User Not Found', data['user_id'])
            create_user(cursor, data['user_id'])
            log.log_info_post(
                app, 'User Created', data['user_id'])
        create_event(cursor, data['user_id'], data)
        conn.commit()
        conn.close()
        log.log_info_post(app, 'Event Created', data['user_id'])
    except Exception as e:
        log.log_error_post(app, "Unhandled Exception", e)
        return logger.error_handlers.error_response_builder(
            'Internal Server Error',
            500,
            'Internal Server Error',
            datetime.datetime.now().isoformat()
        )
    log.log_info_post(app, "Event post handler complete", None)
