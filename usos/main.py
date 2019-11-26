import os
from dotenv import load_dotenv
from usos_mysql.usos_mysql_connector import USOSMySQLConnector
from usos_api_calls import *
from objects.user import User
from usos_mysql.update_tables import update_usos_courses

if __name__ == '__main__':
    load_dotenv()

    User.get_usos_api_key()
    usos_mysql_connector = USOSMySQLConnector()
    users = usos_mysql_connector.get_usos_users()

    test_user = User(os.getenv('TEST_USER_TOKEN'), os.getenv('TEST_USER_SECRET'), 'pl')

    print('User programs:')
    user_programs = get_user_programs(test_user)
    for p in user_programs:
        print(p.program_id, p.program_name_pl)

    print('\nUser courses:')
    user_courses = get_user_courses(test_user)
    for c in user_courses:
        print(c.course_id, c.course_name_pl, c.class_type_pl)

    update_usos_courses(user_courses, usos_mysql_connector)

    # print('\nUser points:')
    # user_points = get_user_points(test_user)
    # for course, points in user_points.items():
    #     print(course)
    #     for point in points:
    #         print('\t{} - Score: {} points [{}]'.format(point.name, point.points, point.comment))
    #
    # print('\nUser timetable for tomorrow:')
    # tt = get_timetable_for_tommorow(test_user)
    # print(tt)
