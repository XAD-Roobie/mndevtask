# Contains all the database setters

# This would probably be done when a new user is created and not this far in-
# the product, but for now we'll just create a new user if they don't exist
def create_user(cursor, user_id):
    # Insert into users if not exists
    cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
    return True


# Create new event for a user
def create_event(cursor, user_id, event):
    cursor.execute(
        'INSERT INTO events (type, amount, user_id, t) VALUES (?, ?, ?, ?)',
        (event['type'], event['amount'], user_id, event['t'])
    )
    return True
