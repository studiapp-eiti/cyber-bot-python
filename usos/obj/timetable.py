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
            self.start_activity = self.activities[0]
            self.end_activity = self.activities[-1]

    def is_day_off(self) -> bool:
        return len(self.activities) == 0


class ClassActivity:
    def __init__(self, course_id: str, type_pl: str, type_en: str, room: str, start: str, end: str):
        self.course_id = course_id
        self.type_pl = type_pl
        self.type_en = type_en
        self.room = room
        self.start = datetime.fromisoformat(start)
        self.end = datetime.fromisoformat(end)

    @property
    def short_course_id(self):
        return self.course_id.split('-')[-1]

    @property
    def start_str(self):
        return self.start.strftime('%H:%M')

    @property
    def end_str(self):
        return self.end.strftime('%H:%M')

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            data['course_id'],
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
        self.duration = (end - start).total_seconds() // 60

    @property
    def start_str(self):
        return self.start.strftime('%H:%M')

    @property
    def end_str(self):
        return self.end.strftime('%H:%M')

    @property
    def duration_str(self):
        hours = ''
        minutes = ''
        if self.duration >= 60:
            hours = '{}h'.format(int(self.duration // 60))
        if self.duration % 60 != 0:
            minutes = '{}min'.format(int(self.duration % 60))

        separator = ' ' if len(hours) != 0 and len(minutes) != 0 else ''

        return hours + separator + minutes
