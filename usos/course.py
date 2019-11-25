class Course:
    def __init__(self, course_id, course_name_pl, course_name_en, class_type_pl, class_type_en, term_id, class_type_id):
        self.course_id = course_id
        self.course_name_pl = course_name_pl
        self.course_name_en = course_name_en
        self.class_type_pl = class_type_pl
        self.class_type_en = class_type_en
        self.term_id = term_id
        self.class_type_id = class_type_id

    @classmethod
    def from_json(cls, json_data: dict):
        return cls(
            json_data['course_id'], json_data['course_name']['pl'], json_data['course_name']['en'],
            json_data['class_type']['pl'], json_data['class_type']['en'],
            json_data['term_id'], json_data['class_type_id']
        )
