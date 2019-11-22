import json
from usos.user import User


class Node:
    def __init__(self, node_id, parent_node, name, node_type):
        self.node_id = node_id
        self.parent_node = parent_node
        self.name = name
        self.type = node_type
        self.subnodes = []

    @classmethod
    def from_json(cls, json_data, parent_node):
        if parent_node is not None and parent_node.node_id != json_data['parent_id']:
            return None

        new_node = cls(
            json_data['node_id'],
            parent_node,
            json_data['name']['pl'],
            json_data['type'],
        )

        subnodes = []
        for sn in json_data['subnodes']:
            subnodes.append(cls.from_json(sn, new_node))
        new_node.subnodes = subnodes

        return new_node

    def __str__(self):
        return '{self.name} [{self.node_id}] --- {self.type}'.format(self=self)

    @staticmethod
    def show_node_tree(node, indent: int):
        if node.type == 'root':
            print('{}{}'.format('\t' * indent, str(node)))
        for subn in node.subnodes:
            print('{}{}'.format('\t' * indent, str(node)))
            if len(subn.subnodes) != 0:
                Node.show_node_tree(subn, indent+1)

    def get_pkt_node_ids(self, user: User):
        for subn in self.subnodes:
            if subn.type == 'pkt':
                user.pkt_node_ids.append(subn.node_id)

            if len(subn.subnodes) != 0:
                subn.get_pkt_node_ids(user)

    def get_points(self, user: User):
        self.get_pkt_node_ids(user)

        r = user.session.post('https://apps.usos.pw.edu.pl/services/crstests/user_points', data={
            'node_ids': '|'.join([str(i) for i in user.pkt_node_ids])
        })

        print(json.dumps(r.json(), ensure_ascii=False, indent=2))
