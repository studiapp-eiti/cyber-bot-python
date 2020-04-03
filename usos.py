from dotenv import load_dotenv
from usos.api_calls import *
from usos.db.user_ops import get_usos_users

if __name__ == '__main__':
    load_dotenv()

    users = get_usos_users()
    timetables = []

    for user in users:
        print('\nTimetable for user: {} {}'.format(user.fb_first_name, user.fb_last_name))
        tt = get_timetable_for_tomorrow(user)
        if tt.is_day_off():
            print('Day off')
        else:
            print('Day start: {}\nDay end: {}'.format(tt.start_activity.start_str, tt.end_activity.end_str))
            print('Gaps:')
            for g in tt.gaps:
                print('-> from {} to {} [{}]'.format(g.start_str, g.end_str, g.duration_str))

            print('Activities:')
            for a in tt.activities:
                print('-> from {} to {} - {} [{}] in {}'.format(a.start_str, a.end_str, a.short_course_id, a.type_pl, a.room))