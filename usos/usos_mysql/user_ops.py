from db.db_connector import DBConnector
from usos.objects.user import User


def get_usos_users(connector: DBConnector, user_ids: list = None) -> list:
    """Get all users from DB and convert to User objects

    :param connector: MySQL DB connector
    :param user_ids: List of user_ids to get from DB. Omit this parameter if you want to get all users
    :returns: List of User objects
    """

    # Column names
    columns = [
        'fb_first_name', 'fb_last_name', 'nickname', 'gender',
        'usos_first_name', 'usos_last_name', 'usos_id', 'usos_courses',
        'usos_token', 'usos_token_secret', 'locale', 'is_registered'
    ]

    users = []
    cursor = connector.connection.cursor(dictionary=True)

    if user_ids is None:
        query = 'select {} from users;'.format(', '.join(columns))
        cursor.execute(query)
    else:
        query = 'select {} from users where id in ({});'.format(
            ', '.join(columns), ', '.join(['%s' for i in range(len(user_ids))])
        )
        cursor.execute(query, user_ids)

    for user_data in cursor:
        if user_data['is_registered']:
            users.append(User(**user_data))

    cursor.close()

    return users
