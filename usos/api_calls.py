from datetime import date, timedelta

from usos.obj.course import Course
from usos.obj.points import Points
from usos.obj.program import Program
from usos.obj.timetable import Timetable
from usos.obj.user import User
from usos.obj.node import Node

from usos.api import UsosApi as api

# URLs for USOS API methods
BASE_URL = 'https://apps.usos.pw.edu.pl/'
TEST_PARTICIPANT_URL = 'services/crstests/participant'
STUDENT_POINT_URL = 'services/crstests/student_point'
NODE_URL = 'services/crstests/node'
TIMETABLE_URL = 'services/tt/student'
TERM_SEARCH = 'services/terms/search'
USER_PROGRAMS_URL = 'services/progs/student'
USER_COURSES_URL = 'services/courses/user'
USER_COURSES_PARTICIPANT_URL = 'services/groups/participant'
USER_POINTS_URL = 'services/crstests/user_points'
USER_URL = 'services/users/user'


def get_user_terms_ids(user: User) -> list:
    """Gets term IDs in which the user took part

    :param user: User that has an active session
    :returns: A list of term IDs
    """
    r = api.user_post(user, BASE_URL + USER_COURSES_URL, data={
        'fields': 'terms',
        'active_terms_only': 'false'
    })

    return [term['id'] for term in r.json()['terms']]


def get_global_term_id() -> str:
    """Gets global semester ID (independent of each user)"""
    r = api.anon_get(BASE_URL + TERM_SEARCH, params={
        'min_finish_date': date.today().strftime('%Y-%m-%d')
    })
    return r.json()[0]['id']


def get_user_programs(user: User) -> set:
    """Get all user programs

    :param user: User that has an active session
    :returns: Set of unique Program objects representing user programs
    """
    r = api.user_get(user, BASE_URL + USER_PROGRAMS_URL)

    programs = set()
    for program in r.json():
        programs.add(Program.from_json(program['programme']))

    return programs


def get_user_courses(user: User) -> set:
    """Get all user courses

    :param user: User that has an active session
    :returns: Set of unique Course objects representing user courses
    """
    fields = [
        'course_id', 'course_name', 'term_id'
    ]
    r = api.user_post(user, BASE_URL + USER_COURSES_PARTICIPANT_URL, data={
        'fields': '|'.join(fields),
        'active_terms': 'true'
    })

    courses = set()
    for term in get_user_terms_ids(user):
        for course in r.json()['groups'][term]:
            courses.add(Course.from_json(course))

    return courses


def get_user_points(user: User, current_term_only: bool = True) -> set:
    """Get all points that user has scored in all courses

    :param user: User that has an active session
    :param current_term_only: Get points only scored during current semester
    :returns: Set of all points scored by user
    """
    r = api.user_get(user, BASE_URL + TEST_PARTICIPANT_URL)
    user_points = set()

    terms = []
    if current_term_only:
        terms.append(get_global_term_id())
    else:
        terms.extend(get_user_terms_ids(user))

    terms_from_api = r.json()['tests']

    for term in terms:
        if term not in terms_from_api:
            continue

        for root_id, root_content in r.json()['tests'][term].items():
            fields = [
                'node_id', 'root_id', 'parent_id',
                'name', 'type', 'subnodes'
            ]
            r = api.user_post(user, BASE_URL + NODE_URL, data={
                'node_id': root_id,
                'recursive': 'true',
                'fields': '|'.join(fields)
            })

            root_node = Node.from_json(r.json(), None)
            pkt_node_ids = [str(i) for i in Node.search_tree(root_node, lambda x: x.type == 'pkt', lambda x: x.node_id)]

            r = api.user_post(user, BASE_URL + USER_POINTS_URL, data={
                'node_ids': '|'.join(pkt_node_ids)
            })

            course_id = root_content['course_edition']['course_id']
            for point in r.json():
                # We need to add 'name' and 'course_id' attributes to point because API doesn't return them
                point['name'] = Node.get_node_by_id(root_node, point['node_id']).name
                point['course_id'] = course_id

                user_points.add(Points.from_json(point))

    return user_points


def get_timetable_for_tomorrow(user: User):
    """Get timetable for tomorrow for specified user

    :param user: User that has an active session
    :returns: User's timetable for tomorrow
    """
    tomorrow = date.today() + timedelta(days=1)
    fields = [
        'start_time', 'end_time', 'room_number',
        'course_name', 'classtype_name', 'course_id'
    ]

    # Note: fields 'course_id', 'room_number', 'course_name' and 'classtype_name' might cause the program to break
    # because USOS API throws HTTP 500 error when the fields don't match the 'type' specific fields

    r = api.user_post(user, BASE_URL + TIMETABLE_URL, data={
        'start': tomorrow.strftime('%Y-%m-%d'),
        'days': 1,
        'fields': '|'.join(fields)
    })

    return Timetable(r.json())


def get_user_usos_id_and_name(user: User) -> dict:
    """Get user usos_id, first_name and last_name

    :param user: User that has an active session
    :returns: Dict that contains usos_id, first_name and last_name
    """
    fields = [
        'id', 'first_name', 'last_name'
    ]
    r = api.user_post(user, BASE_URL + USER_URL, data={
        'fields': '|'.join(fields)
    })
    return r.json()
