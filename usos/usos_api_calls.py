import rauth
from usos.user import User

from usos.tests import Node

BASE_URL = 'https://apps.usos.pw.edu.pl/'
TEST_PARTICIPANT_URL = 'services/crstests/participant'
STUDENT_POINT_URL = 'services/crstests/student_point'
NODE_URL = 'services/crstests/node'
TIMETABLE_URL = 'services/tt/student'


def get_timetable_for_tommorow(session: rauth.OAuth1Session):
    r = session.post(BASE_URL + TIMETABLE_URL, data={'days': 4})
    return r.json()


def get_points(user: User):
    r = user.session.get(BASE_URL + TEST_PARTICIPANT_URL)

    if 'tests' not in r.json():
        return

    for n in r.json()['tests']['2019Z']:
        fields = [
            'node_id', 'root_id', 'parent_id',
            'name', 'type', 'subnodes'
        ]
        r = user.session.post(BASE_URL + NODE_URL, data={
            'node_id': n,
            'recursive': 'true',
            'fields': '|'.join(fields)
        })

        root_node = Node.from_json(r.json(), None)
        # print('\nTree structure for ' + root_node.name)
        # Node.show_node_tree(root_node, 0)
        root_node.get_points(user)

        return
