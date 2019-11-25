class Program:
    def __init__(self, program_id, program_name_pl, program_name_en):
        self.program_id = program_id
        self.program_name_pl = program_name_pl
        self.program_name_en = program_name_en

    @classmethod
    def from_json(cls, json_data: dict):
        return cls(
            json_data['id'], json_data['description']['pl'], json_data['description']['en']
        )
