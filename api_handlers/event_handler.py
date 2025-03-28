from database_functions import event_post_handler


def post_event_handler(app, data):
    datastore = event_post_handler.event_post_handler(app, data)
    if datastore is not None:
        return datastore

    return None
