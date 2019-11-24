class Node:
    def __init__(self, node_id, parent_node, name, node_type):
        self.node_id = node_id
        self.parent_node = parent_node
        self.name = name
        self.type = node_type
        self.subnodes = []

    @classmethod
    def from_json(cls, json_data: dict, parent_node):
        if parent_node is not None and parent_node.node_id != json_data['parent_id']:
            return None

        new_node = cls(
            json_data['node_id'],
            parent_node,
            json_data['name']['pl'],
            json_data['type'],
        )

        subnodes = []
        for subn in json_data['subnodes']:
            subnodes.append(cls.from_json(subn, new_node))
        new_node.subnodes = subnodes

        return new_node

    def __str__(self):
        return '{self.name} [{self.node_id}] --- {self.type}'.format(self=self)

    @staticmethod
    def show_node_tree(node, indent: int):
        if node.type == 'root':
            print('{}{}'.format('\t' * indent, str(node)))
        for subn in node.subnodes:
            print('{}{}'.format('\t' * indent, str(subn)))
            if len(subn.subnodes) != 0:
                Node.show_node_tree(subn, indent+1)

    @staticmethod
    def get_node_by_id(root_node, node_id: int):
        for n in Node.traverse_tree(root_node):
            if n.node_id == node_id:
                return n
        return None

    @staticmethod
    def traverse_tree(node):
        yield node
        for subn in node.subnodes:
            yield from Node.traverse_tree(subn)

    @staticmethod
    def search_tree(node, criterion, extract):
        if criterion(node):
            yield extract(node)
        for n in Node.traverse_tree(node):
            if criterion(n):
                yield extract(n)
