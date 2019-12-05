from db import db_connector
from studia3.studia3_mysql.queries import Queries
from dotenv import load_dotenv


def init():
    load_dotenv()


def get_supported_subjects():
    db = db_connector.DBConnector()
    q = Queries()
    result = q.carry_transaction(q.get_accessible_subject)
    supported_subjects = dict()
    for line in result:
        supported_subjects[line["cookie"]] = line["usos_courses"].split(";")
    return supported_subjects


def check_if_subject_supported(subjects, subject_id):
    return next((k for k, v in subjects.items() if subject_id in v), False)


if __name__ == "__main__":
    init()
    supported_subjects = get_supported_subjects()
    supported = check_if_subject_supported(supported_subjects, "34")
    print(supported)
    if supported:
        print("This sub is supported")
