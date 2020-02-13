from datetime import datetime


class Timetable:
    MINIMUM_GAP_DURATION = 60

    def __init__(self, activities_json: list):
        self.activities = []
        self.gaps = []
        for act_no, act in enumerate(activities_json):
            next_act = ClassActivity.from_json(act)
            if act_no != 0:
                gap = Gap(self.activities[-1].end, next_act.start)
                if gap.duration > Timetable.MINIMUM_GAP_DURATION:
                    self.gaps.append(gap)
            self.activities.append(next_act)

        if len(self.activities) != 0:
            self.day_start = self.activities[0].start
            self.day_end = self.activities[-1].end

    def is_day_off(self) -> bool:
        return len(self.activities) == 0


class ClassActivity:
    def __init__(self, name_pl, name_en, type_pl, type_en, room, start, end):
        self.name_pl = name_pl
        self.name_en = name_en
        self.type_pl = type_pl
        self.type_en = type_en
        self.room = room
        self.start = datetime.fromisoformat(start)
        self.end = datetime.fromisoformat(end)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            data['course_name']['pl'],
            data['course_name']['en'],
            data['classtype_name']['pl'],
            data['classtype_name']['en'],
            data['room_number'],
            data['start_time'],
            data['end_time']
        )


class Gap:
    def __init__(self, start: datetime, end: datetime):
        self.start = start
        self.end = end
        self.duration = (end - start).total_seconds() / 60
