import json
from dotenv import load_dotenv
from usos.usos_api_calls import *
from usos.objects.user import User
from usos.usos_mysql.user_ops import get_usos_users

if __name__ == '__main__':
    load_dotenv()

    User.get_usos_api_key()
    users = get_usos_users()

    for user in users:
        print('\nTimetable for user: {} {}'.format(user.fb_first_name, user.fb_last_name))
        tt = get_timetable_for_tommorow(user)
        # print(json.dumps(tt, indent=2, ensure_ascii=False))
