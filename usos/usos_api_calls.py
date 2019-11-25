from usos.course import Course
from usos.points import Points
from usos.user import User
from usos.node import Node

BASE_URL = 'https://apps.usos.pw.edu.pl/'
TEST_PARTICIPANT_URL = 'services/crstests/participant'
STUDENT_POINT_URL = 'services/crstests/student_point'
NODE_URL = 'services/crstests/node'
TIMETABLE_URL = 'services/tt/student'
USER_COURSES_URL = 'services/courses/user'
USER_COURSES_PARTICIPANT_URL = 'services/groups/participant'
USER_POINTS_URL = 'services/crstests/user_points'


def get_active_term_id(user: User):
    r = user.session.post(BASE_URL + USER_COURSES_URL, data={
        'fields': 'terms',
        'active_terms_only': 'true'
    })

    return r.json()['terms'][0]['id']


def get_user_courses(user: User):
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


def get_timetable_for_tommorow(user: User):
    r = user.session.post(BASE_URL + TIMETABLE_URL, data={'days': 4})
    return r.json()


def get_user_points(user: User):
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
            point['name'] = Node.get_node_by_id(root_node, point['node_id']).name
            user_points[course_id].append(Points.from_json(point))

    return user_points
