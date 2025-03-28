def error_response_builder(error, code, additional_info, timestamp):
    return {
        'timestamp': timestamp,
        'error': error,
        'code': code,
        'additional_info': additional_info
    }
