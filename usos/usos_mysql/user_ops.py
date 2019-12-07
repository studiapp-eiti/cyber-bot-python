from db.db_connector import DbConnector, db_operation
from usos.objects.points import Points
from usos.objects.user import User
from usos.usos_api_calls import get_user_points
from usos.usos_mysql.update_tables import update_usos_points
from messenger import Notifier


@db_operation
def get_usos_users(user_ids: list = None) -> list:
    """Get all users from DB and convert to User objects

    :param user_ids: List of user_ids to get from DB. Omit this parameter if you want to get all users
    :returns: List of User objects
    """
    connection = DbConnector.get_connection()

    # Column names
    columns = [
        'id', 'fb_first_name', 'fb_last_name', 'nickname', 'gender',
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
            user_data['id_'] = user_data['id']
            del user_data['id']
            users.append(User(**user_data))

    cursor.close()

    return users


def check_for_new_points(user: User):
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

    if len(new_points) != 0:
        update_usos_points(new_points)

    if len(modified_points) != 0:
        update_points_query = 'update usos_points set points = %s, comment = %s, last_changed = %s ' \
                              'where node_id = %s and student_id = %s;'
        for p in modified_points:
            cursor.execute(update_points_query, (
                p.points, p.comment, p.last_changed,
                p.node_id, p.student_id
            ))

    # TODO: Send notification to user
    print('New points:')
    for n in new_points:
        print(n.course_id, n.name, n.points, n.comment)

    notifier = Notifier([user.id])
    notifier.message_new_points([n for n in new_points])

    print('Modified points:')
    for m in modified_points:
        print(m.course_id, m.name, m.points, m.comment)

    cursor.close()
