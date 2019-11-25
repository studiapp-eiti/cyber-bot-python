from usos.course import Course
from usos.points import Points
from usos.program import Program
from usos.user import User
from usos.node import Node

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


def get_active_term_id(user: User) -> str:
    """Gets active term ID

    :param user: User that has an active session
    :returns: A string representing term ID
    """
    r = user.session.post(BASE_URL + USER_COURSES_URL, data={
        'fields': 'terms',
        'active_terms_only': 'true'
    })

    return r.json()['terms'][0]['id']


def get_user_programs(user: User) -> list:
    """Get all user programs

    :param user: User that has an active session
    :returns: List of Program objects representing user programs
    """
    r = user.session.get(BASE_URL + USER_PROGRAMS_URL)

    programs = []
    for program in r.json():
        programs.append(Program.from_json(program['programme']))

    return programs


def get_user_courses(user: User) -> list:
    """Get all user courses

    :param user: User that has an active session
    :returns: List of Course objects representing user courses
    """
    fields = [
        'course_id', 'class_type', 'course_name', 'term_id', 'class_type_id'
    ]
    r = user.session.post(BASE_URL + USER_COURSES_PARTICIPANT_URL, data={
        'fields': '|'.join(fields),
        'active_terms': 'true'
    })

    courses = []
    for course in r.json()['groups'][get_active_term_id(user)]:
        courses.append(Course.from_json(course))

    return courses


def get_user_points(user: User) -> dict:
    """Get all points that user has scored in all courses

    :param user: User that has an active session
    :returns: Dictionary in format `{'course_id': Point}` that represents user points in all courses
    """
    r = user.session.get(BASE_URL + TEST_PARTICIPANT_URL)
    user_points = {}

    for root_id, root_content in r.json()['tests'][get_active_term_id(user)].items():
        fields = [
            'node_id', 'root_id', 'parent_id',
            'name', 'type', 'subnodes'
        ]
        r = user.session.post(BASE_URL + NODE_URL, data={
            'node_id': root_id,
            'recursive': 'true',
            'fields': '|'.join(fields)
        })

        root_node = Node.from_json(r.json(), None)
        pkt_node_ids = [str(i) for i in Node.search_tree(root_node, lambda x: x.type == 'pkt', lambda x: x.node_id)]

        r = user.session.post(BASE_URL + USER_POINTS_URL, data={
            'node_ids': '|'.join(pkt_node_ids)
        })

        course_id = root_content['course_edition']['course_id']
        user_points[course_id] = []
        for point in r.json():
            # We need to add 'name' attribute to point because API doesn't return it
            point['name'] = Node.get_node_by_id(root_node, point['node_id']).name
            user_points[course_id].append(Points.from_json(point))

    return user_points


def get_timetable_for_tommorow(user: User):
    """Get timetable for tommorow for specified user

    :param user: User that has an active session
    :returns: User's timetable for tommorow
    """
    # TODO: Make timetable class and return it
    r = user.session.post(BASE_URL + TIMETABLE_URL, data={'days': 4})
    return r.json()
