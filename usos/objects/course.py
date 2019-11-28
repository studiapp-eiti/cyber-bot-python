class Course:
    """Class representing student course"""

    def __init__(self, course_id, course_name_pl, course_name_en, term_id):
        """Constructs a new Course object"""
        self.course_id = course_id
        self.course_name_pl = course_name_pl
        self.course_name_en = course_name_en
        self.term_id = term_id

    @classmethod
    def from_json(cls, json_data: dict):
        """Constructs a new Course object from given JSON data

        :param json_data: Data obtained from calling `services/groups/participant`
        """
        return cls(
            json_data['course_id'], json_data['course_name']['pl'],
            json_data['course_name']['en'], json_data['term_id']
        )

    def __hash__(self):
        return hash(self.course_id)

    def __eq__(self, other):
        return self.course_id == other.course_id
