# Contains all the database getters
def check_user_exists(cursor, user_id):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    if cursor.fetchone():
        return True
    return False


# Get all events for a user
def get_events(cursor, user_id):
    cursor.execute('SELECT * FROM events WHERE user_id = ?', (user_id,))
    return cursor.fetchall()
