from dotenv import load_dotenv
from pathlib import Path

from messenger import Notifier
from usos.objects.user import User
from usos.usos_mysql.update_tables import update_new_usos_points, update_modified_usos_points
from usos.usos_mysql.user_ops import get_usos_users, get_new_and_modified_points

if __name__ == '__main__':
    dotenv_path = Path(__file__).parents[1] / '.env'
    load_dotenv(dotenv_path=dotenv_path)

    User.get_usos_api_key()
    users = get_usos_users()
    for u in users:
        new_points, mod_points = get_new_and_modified_points(u)
        if len(new_points) != 0:
            print('Adding new points for user {} {}:'.format(u.fb_first_name, u.fb_last_name))
            for p in new_points:
                print('-->', p.course_id, p.name, p.points, p.comment)
            update_new_usos_points(new_points)
            # notifier = Notifier([u.id])
            # notifier.message_new_points(new_points)

        if len(mod_points) != 0:
            print('Updating modified points for user {} {}:'.format(u.fb_first_name, u.fb_last_name))
            for p in mod_points:
                print('-->', p.course_id, p.name, p.points, p.comment)
            update_modified_usos_points(mod_points, u)
            # TODO: Notify user about modified points
