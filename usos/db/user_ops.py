from db.db_connector import DbConnector, db_operation_usos
from usos.obj.points import Points
from usos.obj.user import User
from usos.api_calls import get_user_points


@db_operation_usos
def get_usos_users(user_ids: list = None) -> list:
    """Get all users from DB and convert to User objects

    :param user_ids: List of user_ids to get from DB. Omit this parameter if you want to get all users
    :returns: List of User objects
    """
    connection = DbConnector.get_connection()

    # Column names
    columns = [
        'id', 'fb_first_name', 'fb_last_name', 'nickname', 'gender', 'subscriptions',
        'usos_first_name', 'usos_last_name', 'usos_id', 'usos_courses',
        'usos_token', 'usos_token_secret', 'locale', 'is_registered'
    ]

    users = []
    cursor = connection.cursor(dictionary=True)

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


@db_operation_usos
def get_new_and_modified_points(user: User) -> tuple:
    """Get all points scored by given user and return new and modified ones

    Compare points fetched from API and those that are in the DB and look for differences

    :param user: User that has an active session
    :returns: Tuple in format (new_points, modified_points)
    :rtype: (set[Points], set[Points])
    """
    connection = DbConnector.get_connection()

    columns = [
        'name', 'points', 'comment', 'grader_id', 'node_id',
        'student_id', 'last_changed', 'course_id'
    ]
    get_points_query = 'select {} from usos_points ' \
                       'where student_id = %s;'.format(', '.join(columns))
    cursor = connection.cursor(dictionary=True)
    cursor.execute(get_points_query, (user.usos_id,))

    points_from_db = {Points(**i) for i in cursor}
    points_from_api = get_user_points(user)

    modified_points = set()
    new_points = set()
    for p_api in points_from_api:
        p_db = [x for x in points_from_db if x == p_api]
        if len(p_db) == 0:  # If there's no equivalent of p_api in DB
            new_points.add(p_api)
        elif p_db[0].last_changed != p_api.last_changed:
            modified_points.add(p_api)

    cursor.close()

    return new_points, modified_points
