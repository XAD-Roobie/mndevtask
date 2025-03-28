import error_handlers
import datetime


def test_error_response_builder():
    timestamp = datetime.datetime.now().isoformat()
    assert error_handlers.error_response_builder(
        'Internal Server Error', 500, 'Internal Server Error', timestamp) == {
            'timestamp': timestamp,
            'error': 'Internal Server Error',
            'code': 500,
            'additional_info': 'Internal Server Error'
        }
