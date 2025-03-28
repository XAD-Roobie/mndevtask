import response_handler


def response_builder_test():
    assert response_handler.response_builder('user_id', None) == {
        'alert': False,
        'alert_codes': None,
        'user_id': 'user_id'
    }
    assert response_handler.response_builder('user_id', [1100]) == {
        'alert': True,
        'alert_codes': [1100],
        'user_id': 'user_id'
    }
    assert response_handler.response_builder('user_id', [1100, 300]) == {
        'alert': True,
        'alert_codes': [1100, 300],
        'user_id': 'user_id'
    }
