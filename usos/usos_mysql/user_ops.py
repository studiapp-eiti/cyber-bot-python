from db.db_connector import DBConnector
from usos.objects.user import User


def get_usos_users(connector: DBConnector) -> list:
    """Get all users from DB and convert to User objects

    :param connector: MySQL DB connector
    :returns: List of User objects
    """

    # Column names
    columns = [
        'first_name', 'last_name', 'nickname', 'gender',
        'usos_id', 'usos_courses', 'usos_token', 'usos_token_secret',
        'locale', 'is_registered'
    ]
    query = 'select {} from users;'.format(', '.join(columns))

    users = []

    cursor = connector.connection.cursor(dictionary=True)
    cursor.execute(query)
    for user_data in cursor:
        if user_data['is_registered']:
            users.append(User(**user_data))

    cursor.close()

    return users
