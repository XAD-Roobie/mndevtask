def response_builder(user_id, alert_codes):
    alert = False
    if alert_codes:
        alert = True
    return {
        'alert': alert,
        'alert_codes': alert_codes,
        'user_id': user_id
    }
