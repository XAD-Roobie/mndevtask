from flask import Flask, request
from logging.config import dictConfig
import validators.request_validator as request_validator
from api_handlers import event_handler, event_alerts_handler
import logger.logger as log
import logger.response_handler as response_handler
import logger.error_handlers as error_handlers
from uuid import uuid4
import datetime


app = Flask(__name__)


# Logging Configuration
# Ugly but works, I would prefer to have this defined elsewhere
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
    }},
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'DEBUG',
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': 'flask.log',
            'level': 'DEBUG',
        }
    },
    'loggers': {
        'console': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False
        },
        'file': {
            'level': 'DEBUG',
            'handlers': ['file'],
            'propagate': False
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file']
    }
})


@app.route('/event', methods=['POST'])
def event():
    try:
        # Generate a UUID for the request
        uuid = str(uuid4())
        app.uuid = uuid

        data = request.get_json()

        # Payload validation block
        try:
            validated = request_validator.validate_event_request(app, data)
            if validated is not None:
                log.log_warning_post(
                    app, 'Event Request Validation Failed', data)
                return validated
            log.log_info_post(
                app, 'Event Request Validation Successful', "")
        except Exception as e:
            log.log_error_post(app, 'Request validation failed', e)
            return error_handlers.error_response_builder(
                'Internal Server Error',
                500,
                'Internal Server Error',
                datetime.datetime.now().isoformat()
            )
        # Event publish block
        try:
            publish_event = event_handler.post_event_handler(
                app, data)
            if publish_event is not None:
                return publish_event
        except Exception as e:
            log.log_error_post(app, 'Event Publish Failed', e)
            return error_handlers.error_response_builder(
                'Internal Server Error',
                500,
                'Internal Server Error',
                datetime.datetime.now().isoformat()
                )
        # Action code block
        alerts = []
        try:
            alerts = event_alerts_handler.check_for_alerts(
                app, data['user_id'])
            log.log_info_post(app, 'Alert Check Successful', alerts)
        except Exception as e:
            log.log_error_post(app, 'Alert Check Failed', e)
            return error_handlers.error_response_builder(
                'Internal Server Error',
                500,
                'Internal Server Error',
                datetime.datetime.now().isoformat()
                )
        log.log_info_post(app, 'Request end ', 200)
        return response_handler.response_builder(data['user_id'], alerts), 200
    except Exception as e:
        log.log_critical_post(app, 'Unhandled Exception', e)
        return error_handlers.error_response_builder(
            'Internal Server Error',
            500,
            'Internal Server Error',
            datetime.datetime.now().isoformat()
            )
