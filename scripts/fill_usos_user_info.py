import sys
import pathlib
import logging
from dotenv import load_dotenv
from db.db_connector import DbConnector
from argparse import ArgumentParser
from usos.objects.user import User
from usos.usos_api_calls import get_user_courses, get_user_usos_id_and_name
from usos.usos_mysql.user_ops import get_usos_users

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler('./fill_usos_user_info.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(file_formatter)

stream_formatter = logging.Formatter('[DEBUG] %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(stream_formatter)

logger.addHandler(file_handler)

if __name__ == '__main__':
    # Parse args
    argparser = ArgumentParser(
        description='Get user USOS ID, first and last name from USOS and fill `users` table in DB'
    )
    argparser.add_argument(
        '-d', '--debug', help='Turn on debug messages', action='store_true'
    )
    argparser.add_argument(
        'user_ids', type=int, metavar='UIDs', nargs='+',
        help='User IDs from `users` table'
    )
    args = argparser.parse_args()

    if args.debug:
        logger.addHandler(stream_handler)

    logger.info('Started script with UIDs: %s', ', '.join([str(x) for x in args.user_ids]))

    # Load .env
    env_path = pathlib.Path(__file__).parents[1] / '.env'
    load_dotenv(dotenv_path=env_path)

    # Get users from DB
    User.get_usos_api_key()
    users = get_usos_users(args.user_ids)
    if len(users) != len(args.user_ids):
        logger.error('Attempt to update user that doesn\'t exist')
        sys.exit(-1)

    connection = DbConnector().get_connection()
    cursor = connection.cursor()

    query_course_ids = 'select course_id, id from usos_courses;'
    cursor.execute(query_course_ids)

    course_ids = {course_id: str(tbl_id) for (course_id, tbl_id) in cursor}

    logger.debug('Filling USOS information for following users:')
    for user in users:
        logger.debug('User %s %s [%s]:', user.fb_first_name, user.fb_last_name, user.id)
        logger.debug('Courses:')
        courses = get_user_courses(user)
        for c in courses:
            logger.debug('--> %s', c.course_id)
        usos_info = get_user_usos_id_and_name(user)
        logger.debug('USOS info:')
        logger.debug('--> USOS ID: %s', usos_info['id'])
        logger.debug('--> First name: %s', usos_info['first_name'])
        logger.debug('--> Last name: %s', usos_info['last_name'])

        query_course_ids = 'select id from usos_courses'

        insert_usos_info = 'update users ' \
                           'set usos_id = %s, usos_first_name = %s, usos_last_name = %s, usos_courses = %s ' \
                           'where id = %s;'

        logger.debug('Updating user\'s record in database...')
        cursor.execute(insert_usos_info, (
            usos_info['id'], usos_info['first_name'], usos_info['last_name'],
            ';'.join(sorted([course_ids[c.course_id] for c in courses])), user.id
        ))
        connection.commit()
        logger.info('Updated user %s %s [%s]', user.fb_first_name, user.fb_last_name, user.id)

    cursor.close()
