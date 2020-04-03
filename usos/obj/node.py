class Node:
    """Class providing convenient interface to interact with USOS API course test node tree"""

    def __init__(self, node_id: str, parent_node, name: str, node_type: str):
        """Constructs new Node object

        :type parent_node: Node, NoneType
        """
        self.node_id = node_id
        self.parent_node = parent_node
        self.name = name
        self.type = node_type
        self.subnodes = []

    @classmethod
    def from_json(cls, json_data: dict, parent_node):
        """Creates new Node tree from supplied JSON data

        Performs recursive lookup into the tree and creates a Node object for every
        subnode in all nodes that have them.

        :param json_data: Data returned from `services/crstests/node`
        It should contain root node as its first element
        :param parent_node: Parent node (should be `None` for root node)
        :type parent_node: Node, NoneType
        :returns: Node tree with root node on top
        """
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
        """Shows node tree in human readable format

        :param node: Top level node
        :type node: Node
        :param indent: How many tabs
        """
        if node.type == 'root':
            print('{}{}'.format('\t' * indent, str(node)))
        for subn in node.subnodes:
            print('{}{}'.format('\t' * indent, str(subn)))
            if len(subn.subnodes) != 0:
                Node.show_node_tree(subn, indent+1)

    @staticmethod
    def get_node_by_id(root_node, node_id: int):
        """Finds given node ID and returns corresponding Node object

        :param root_node: Search starting point node
        :type root_node: Node
        :param node_id: Node ID that we want to search in the tree
        :returns: Node that matches given node ID or `None` if search has failed
        """
        for n in Node.traverse_tree(root_node):
            if n.node_id == node_id:
                return n
        return None

    @staticmethod
    def traverse_tree(node):
        """Generator that yields every node in the tree

        :param node: Point which we want to start traversing with
        :type node: Node
        """
        yield node
        for subn in node.subnodes:
            yield from Node.traverse_tree(subn)

    @staticmethod
    def search_tree(node, criterion, extract):
        """Function that searches for nodes matching given criteria and yields their specified attributes

        :param node: Search starting point node
        :type node: Node
        :param criterion: Function with node as its only parameter which performs a test on that parameter
        For example (we want to search for nodes of type 'fld'): `lambda n: n.type == 'fld'`
        :type criterion: function
        :param extract: Function with node as its only parameter which returns certain attribute of that parameter
        For example (we want to return node_id attribute of found nodes): `lambda n: n.node_id`
        :type extract: function
        """
        if criterion(node):
            yield extract(node)
        for n in Node.traverse_tree(node):
            if criterion(n):
                yield extract(n)
