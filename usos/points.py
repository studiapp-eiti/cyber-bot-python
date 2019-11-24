class Points:
    def __init__(self, name, points, last_changed, comment, grader_id, node_id, student_id):
        self.name = name
        self.points = points
        self.last_changed = last_changed
        self.comment = comment
        self.grader_id = grader_id
        self.node_id = node_id
        self.student_id = student_id

    @classmethod
    def from_json(cls, json_data):
        return cls(
            json_data['name'], json_data['points'], json_data['last_changed'], json_data['comment'],
            json_data['grader_id'], json_data['node_id'], json_data['student_id']
        )
