import sys
import logging

from dotenv import load_dotenv
from pathlib import Path
from argparse import ArgumentParser

from usos.objects.user import User
from usos.usos_api_calls import get_user_programs, get_user_courses, get_user_points
from usos.usos_mysql.update_tables import update_usos_programs, update_usos_courses, update_new_usos_points
from usos.usos_mysql.user_ops import get_usos_users

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler('./initialize_new_usos_user.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(file_formatter)

stream_formatter = logging.Formatter('[%(levelname)s] %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(stream_formatter)

logger.addHandler(file_handler)

if __name__ == '__main__':
    argparser = ArgumentParser(
        description='Get user programs, courses and points and store them in the DB'
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

    dotenv_path = Path(__file__).parents[1] / '.env'
    load_dotenv(dotenv_path=dotenv_path)

    User.get_usos_api_key()
    users = get_usos_users(args.user_ids)

    if len(users) != len(args.user_ids):
        logger.error('Attempt to update user that doesn\'t exist')
        sys.exit(-1)

    logger.debug('Initializing following users:')
    for user in users:
        logger.debug('User %s %s [%s]:', user.fb_first_name, user.fb_last_name, user.id)

        logger.debug('Fetching programs...')
        programs = get_user_programs(user)
        logger.debug('Updating DB...')
        update_usos_programs(programs)

        logger.debug('Fetching courses...')
        courses = get_user_courses(user)
        logger.debug('Updating DB...')
        update_usos_courses(courses)

        logger.debug('Fetching points...')
        points = get_user_points(user)
        logger.debug('Updating DB...')
        update_new_usos_points(points)

        logger.info('Initialized user %s %s [%s]', user.fb_first_name, user.fb_last_name, user.id)
