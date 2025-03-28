def log_info_post(app, message, data):
    app.logger.info('{}: POST Event: {} {}'
                    .format(app.uuid, message, data))


def log_error_post(app, message, data):
    app.logger.error('{}: POST Event Failed: {} {}'
                     .format(app.uuid, message, data))


def log_warning_post(app, message, data):
    app.logger.warning('{}: POST Event: {} {}'
                       .format(app.uuid, message, data))


def log_critical_post(app, message, data):
    app.logger.critical('{}: POST Event: {} {}'
                        .format(app.uuid, message, data))


def log_info_validation(app, message, data):
    app.logger.info('{}: POST Event: {} {}'
                    .format(app.uuid, message, data))
