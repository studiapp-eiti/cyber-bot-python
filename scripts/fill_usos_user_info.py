import sys
import pathlib
from dotenv import load_dotenv
from db.db_connector import DbConnector
from argparse import ArgumentParser
from usos.objects.user import User
from usos.usos_api_calls import get_user_courses, get_user_usos_id_and_name
from usos.usos_mysql.user_ops import get_usos_users

if __name__ == '__main__':
    # Parse args
    argparser = ArgumentParser(
        description='Get user USOS ID, first and last name from USOS and fill `users` table in DB'
    )
    argparser.add_argument(
        'user_ids', type=int, metavar='UIDs', nargs='+',
        help='User IDs from `users` table'
    )
    args = argparser.parse_args()

    # Load .env
    env_path = pathlib.Path(__file__).parents[1] / '.env'
    load_dotenv(dotenv_path=env_path)

    # Get users from DB
    User.get_usos_api_key()
    users = get_usos_users(args.user_ids)
    if len(users) != len(args.user_ids):
        print('Attempt to update user that doesn\'t exist!')
        sys.exit(-1)

    connection = DbConnector().get_connection()
    cursor = connection.cursor()

    query_course_ids = 'select course_id, id from usos_courses;'
    cursor.execute(query_course_ids)

    course_ids = {course_id: str(tbl_id) for (course_id, tbl_id) in cursor}

    for uid, user in zip(args.user_ids, users):
        courses = get_user_courses(user)
        usos_info = get_user_usos_id_and_name(user)

        query_course_ids = 'select id from usos_courses'

        insert_usos_info = 'update users ' \
                           'set usos_id = %s, usos_first_name = %s, usos_last_name = %s, usos_courses = %s ' \
                           'where id = %s;'
        cursor.execute(insert_usos_info, (
            usos_info['id'], usos_info['first_name'], usos_info['last_name'],
            ';'.join(sorted([course_ids[c.course_id] for c in courses])), uid
        ))

    cursor.close()
