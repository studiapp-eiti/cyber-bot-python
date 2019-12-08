import requests
from dotenv import load_dotenv
from usos.usos_api_calls import *
from usos.objects.user import User
from usos.usos_mysql.update_tables import update_usos_courses, update_usos_programs, update_new_usos_points
from usos.usos_mysql.user_ops import get_usos_users

if __name__ == '__main__':
    load_dotenv()

    User.get_usos_api_key()
    users = get_usos_users()

    courses = set()
    programs = set()
    points = set()
    for u in users:
        try:
            programs.update(get_user_programs(u))
            courses.update(get_user_courses(u))
            points.update(get_user_points(u))
        except requests.exceptions.ConnectionError as err:
            print(err)

    print('User programs:')
    for i in sorted(programs, key=lambda x: x.program_name_pl):
        i: Program
        print(i.program_id, i.program_name_pl, sep=' - ')

    print('\nUser courses:')
    for i in sorted(courses, key=lambda x: x.course_name_pl):
        i: Course
        print(i.course_id, i.course_name_pl, sep=' - ')

    print('\nUser points:')
    for i in sorted(points, key=lambda x: x.name):
        i: Points
        print(i.course_id, i.name, i.points, sep=' - ')

    print('\nUpdating user_programs table...')
    update_usos_programs(programs)
    print('Done.')

    print('\nUpdating user_courses table...')
    update_usos_courses(courses,)
    print('Done.')

    print('\nUpdating user_points table...')
    update_new_usos_points(points)
    print('Done.')
