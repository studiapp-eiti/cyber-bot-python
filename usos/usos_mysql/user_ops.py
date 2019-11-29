from db.db_connector import DBConnector
from usos.objects.user import User


def get_usos_users(connector: DBConnector) -> list:
    """Get all users from DB and convert to User objects

    :param connector: MySQL DB connector
    :returns: List of User objects
    """

    # Column names
    col_usos_token = 'usos_token'
    col_usos_token_secret = 'usos_token_secret'
    col_usos_locale = 'locale'

    query = 'select {}, {}, {} from users;'.format(
        col_usos_token, col_usos_token_secret, col_usos_locale
    )

    users = []

    cursor = connector.connection.cursor()
    cursor.execute(query)
    for (usos_token, usos_token_secret, locale) in cursor:
        users.append(User(usos_token, usos_token_secret, locale))
    cursor.close()

    return users
