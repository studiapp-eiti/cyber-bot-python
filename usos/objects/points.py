class Points:
    """Class for holding information about points scored by user in a certain test"""

    def __init__(self, name, points, last_changed, comment, grader_id, node_id, student_id, course_id):
        self.name = name
        self.points = points
        self.last_changed = last_changed
        self.comment = comment
        self.grader_id = grader_id
        self.node_id = node_id
        self.student_id = student_id
        self.course_id = course_id

    @classmethod
    def from_json(cls, json_data: dict):
        """Construct Points object from given JSON data

        :param json_data: Dictionary obtained from calling `services/crstests/user_points`
        :returns: New Points object
        """
        return cls(
            json_data['name'], json_data['points'], json_data['last_changed'], json_data['comment'],
            json_data['grader_id'], json_data['node_id'], json_data['student_id'], json_data['course_id']
        )

    def __hash__(self):
        return hash((self.node_id, self.student_id))

    def __eq__(self, other):
        return self.node_id == other.node_id and self.student_id == other.student_id
