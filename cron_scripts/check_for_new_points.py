from dotenv import load_dotenv
from pathlib import Path

from messenger import Notifier
from usos.db.update_tables import update_new_usos_points, update_modified_usos_points
from usos.db.user_ops import get_usos_users, get_new_and_modified_points

from usos.log import UsosLogger as logger

if __name__ == '__main__':
    dotenv_path = Path(__file__).parents[1] / '.env'
    load_dotenv(dotenv_path=dotenv_path)

    logger.gen().info('Started check for new points script.')

    users = get_usos_users()

    logger.gen().debug('Checking for new and modified points for following users:')
    for u in users:
        logger.gen().info('User %s %s [%s]:', u.fb_first_name, u.fb_last_name, u.id)
        new_points, mod_points = get_new_and_modified_points(u)
        if len(new_points) != 0:
            logger.gen().info('%s new points:', len(new_points))
            for p in new_points:
                logger.gen().debug('--> [%s] %s: %s -- %s', p.course_id, p.name, p.points, p.comment)
            logger.gen().debug('Updating DB...')
            update_new_usos_points(new_points)
            if 'new_points' in u.subscriptions:
                logger.gen().debug('Sending notification...')
                notifier = Notifier([u.id])
                notifier.message_updated_points(new_points, True)
            else:
                logger.gen().warning('User doesn\'t have `new_points` in subscriptions '
                                     'so no notification will be sent.')
        else:
            logger.gen().info('No new points.')

        if len(mod_points) != 0:
            logger.gen().info('%s modified points:', len(mod_points))
            for p in mod_points:
                logger.gen().info('--> [%s] %s: %s -- %s', p.course_id, p.name, p.points, p.comment)
            logger.gen().debug('Updating DB...')
            update_modified_usos_points(mod_points, u)
            if 'mod_points' in u.subscriptions:
                logger.gen().debug('Sending notification...')
                notifier = Notifier([u.id])
                notifier.message_updated_points(mod_points, False)
            else:
                logger.gen().warning('User doesn\'t have `mod_points` in subscriptions '
                                     'so no notification will be sent.')
        else:
            logger.gen().info('No modified points.')
