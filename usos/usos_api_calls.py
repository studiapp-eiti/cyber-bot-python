from datetime import date, datetime, timedelta

from usos.objects.course import Course
from usos.objects.points import Points
from usos.objects.program import Program
from usos.objects.user import User
from usos.objects.node import Node

# URLs for USOS API methods
BASE_URL = 'https://apps.usos.pw.edu.pl/'
TEST_PARTICIPANT_URL = 'services/crstests/participant'
STUDENT_POINT_URL = 'services/crstests/student_point'
NODE_URL = 'services/crstests/node'
TIMETABLE_URL = 'services/tt/student'
USER_PROGRAMS_URL = 'services/progs/student'
USER_COURSES_URL = 'services/courses/user'
USER_COURSES_PARTICIPANT_URL = 'services/groups/participant'
USER_POINTS_URL = 'services/crstests/user_points'
USER_URL = 'services/users/user'


def get_active_terms_ids(user: User) -> list:
    """Gets active term ID

    :param user: User that has an active session
    :returns: A list with active term IDs
    """
    r = user.api_post(BASE_URL + USER_COURSES_URL, data={
        'fields': 'terms',
        'active_terms_only': 'true'
    })

    return [term['id'] for term in r.json()['terms']]


def get_user_programs(user: User) -> set:
    """Get all user programs

    :param user: User that has an active session
    :returns: Set of unique Program objects representing user programs
    """
    r = user.api_get(BASE_URL + USER_PROGRAMS_URL)

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
    r = user.api_post(BASE_URL + USER_COURSES_PARTICIPANT_URL, data={
        'fields': '|'.join(fields),
        'active_terms': 'true'
    })

    courses = set()
    for term in get_active_terms_ids(user):
        for course in r.json()['groups'][term]:
            courses.add(Course.from_json(course))

    return courses


def get_user_points(user: User) -> set:
    """Get all points that user has scored in all courses

    :param user: User that has an active session
    :returns: Set of all points scored by user
    """
    r = user.api_get(BASE_URL + TEST_PARTICIPANT_URL)
    user_points = set()

    for term in get_active_terms_ids(user):
        if term not in r.json()['tests']:
            continue

        for root_id, root_content in r.json()['tests'][term].items():
            fields = [
                'node_id', 'root_id', 'parent_id',
                'name', 'type', 'subnodes'
            ]
            r = user.api_post(BASE_URL + NODE_URL, data={
                'node_id': root_id,
                'recursive': 'true',
                'fields': '|'.join(fields)
            })

            root_node = Node.from_json(r.json(), None)
            pkt_node_ids = [str(i) for i in Node.search_tree(root_node, lambda x: x.type == 'pkt', lambda x: x.node_id)]

            r = user.api_post(BASE_URL + USER_POINTS_URL, data={
                'node_ids': '|'.join(pkt_node_ids)
            })

            course_id = root_content['course_edition']['course_id']
            for point in r.json():
                # We need to add 'name' and 'course_id' attributes to point because API doesn't return them
                point['name'] = Node.get_node_by_id(root_node, point['node_id']).name
                point['course_id'] = course_id

                user_points.add(Points.from_json(point))

    return user_points


def get_timetable_for_tommorow(user: User):
    """Get timetable for tommorow for specified user

    :param user: User that has an active session
    :returns: User's timetable for tommorow
    """
    tomorrow = date.today() + timedelta(days=1)

    r = user.api_post(BASE_URL + TIMETABLE_URL, data={
        'start': tomorrow.strftime('%Y-%m-%d'),
        'days': 1
    })

    for course in r.json():
        t = datetime.fromisoformat(course['start_time'])
        print('{}: {}'.format(t.strftime('%H:%M'), course['name'][user.locale]))


def get_user_usos_id_and_name(user: User) -> dict:
    """Get user usos_id, first_name and last_name

    :param user: User that has an active session
    :returns: Dict that contains usos_id, first_name and last_name
    """
    fields = [
        'id', 'first_name', 'last_name'
    ]
    r = user.api_post(BASE_URL + USER_URL, data={
        'fields': '|'.join(fields)
    })
    return r.json()
