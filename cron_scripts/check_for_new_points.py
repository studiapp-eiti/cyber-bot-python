from dotenv import load_dotenv
from pathlib import Path
import logging
from argparse import ArgumentParser

from messenger import Notifier
from usos.objects.user import User
from usos.usos_mysql.update_tables import update_new_usos_points, update_modified_usos_points
from usos.usos_mysql.user_ops import get_usos_users, get_new_and_modified_points


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler('./check_for_new_points.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(file_formatter)

stream_formatter = logging.Formatter('[%(levelname)s] %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(stream_formatter)

if __name__ == '__main__':
    argparser = ArgumentParser(
        description='Check for new points for users that enabled `` option'
    )
    argparser.add_argument(
        '-d', '--debug', help='Turn on debug messages', action='store_true'
    )
    args = argparser.parse_args()

    if args.debug:
        logger.addHandler(stream_handler)

    logger.info('Started script')

    dotenv_path = Path(__file__).parents[1] / '.env'
    load_dotenv(dotenv_path=dotenv_path)

    User.get_usos_api_key()
    users = get_usos_users()

    logger.debug('Checking for new and modified points for following users:')
    for u in users:
        logger.debug('User %s %s [%s]:', u.fb_first_name, u.fb_last_name, u.id)
        new_points, mod_points = get_new_and_modified_points(u)
        if len(new_points) != 0:
            logger.debug('New points:')
            for p in new_points:
                logger.debug('--> [%s] %s: %s -- %s', p.course_id, p.name, p.points, p.comment)
            logger.debug('Updating DB...')
            update_new_usos_points(new_points)
            if 'points_notifications' in u.subscriptions:
                logger.debug('Sending notification...')
                notifier = Notifier([u.id])
                notifier.message_new_points(new_points)
            else:
                logger.debug('User doesn\'t have `points_notifications` in subscriptions '
                             'so no notification will be sent.')
        else:
            logger.debug('No new points.')

        if len(mod_points) != 0:
            logger.debug('Modified points:')
            for p in mod_points:
                logger.debug('--> [%s] %s: %s -- %s', p.course_id, p.name, p.points, p.comment)
            logger.debug('Updating DB...')
            update_modified_usos_points(mod_points, u)
            # TODO: Notify user about modified points
        else:
            logger.debug('No modified points.')
