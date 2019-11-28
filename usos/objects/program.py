class Program:
    """Class representing user program (or programme if you speak british english)"""

    def __init__(self, program_id, program_name_pl, program_name_en):
        """Constructs a new Program object"""
        self.program_id = program_id
        self.program_name_pl = program_name_pl
        self.program_name_en = program_name_en

    @property
    def short_program_name_pl(self):
        return self.program_name_pl.split(',')[0]

    @property
    def short_program_name_en(self):
        return self.program_name_en.split(',')[0]

    @classmethod
    def from_json(cls, json_data: dict):
        """Constructs a new Program object from given JSON data

        :param json_data: Data obtained form calling `services/progs/student`
        """
        return cls(
            json_data['id'], json_data['description']['pl'], json_data['description']['en']
        )

    def __hash__(self):
        return hash(self.program_id)

    def __eq__(self, other):
        return self.program_id == other.program_id
