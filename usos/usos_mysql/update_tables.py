from usos_mysql.usos_mysql_connector import USOSMySQLConnector


def update_usos_courses(courses: set, connector: USOSMySQLConnector):
    """Update `usos_courses` table

    Gets all courses from DB and compares results with `courses` list.
    If it finds a course that is not present in DB it inserts it.

    :param courses: Set of usos courses
    :param connector: MySQL DB connector
    """
    cursor = connector.connector.cursor()

    get_courses_query = 'select course_id from usos_courses;'
    cursor.execute(get_courses_query)

    db_course_ids = [i for (i,) in cursor]
    insert_data = []
    for c in courses:
        if c.course_id not in db_course_ids:
            insert_data.append((
                c.course_id, c.course_name_pl, c.course_name_en,
                c.class_type_pl, c.class_type_en, c.class_type_id, c.term_id
            ))

    if len(insert_data) == 0:
        return

    insert_new_courses = 'insert into usos_courses (' \
                         'course_id, course_name_pl, course_name_en, ' \
                         'class_type_pl, class_type_en, class_type_id, ' \
                         'term_id) values (%s, %s, %s, %s, %s, %s, %s);'

    cursor.executemany(insert_new_courses, insert_data)
    connector.connector.commit()
    cursor.close()


def update_usos_programs(programs: set, connector: USOSMySQLConnector):
    """Updates `usos_programs` table

    Gets all programs from DB and compares results with `programs` list.
    If it finds a program that is not present in DB it inserts it.

    :param programs: Set of usos programs
    :param connector: MySQL DB connector
    """
    cursor = connector.connector.cursor()

    get_programs_query = 'select program_id from usos_programs;'
    cursor.execute(get_programs_query)

    db_program_ids = [i for (i,) in cursor]
    insert_data = []
    for p in programs:
        if p.program_id not in db_program_ids:
            insert_data.append((
                p.program_id, p.program_name_pl, p.program_name_en
            ))

    if len(insert_data) == 0:
        return

    insert_new_programs = 'insert into usos_programs (' \
                          'program_id, program_name_pl, program_name_en) ' \
                          'values (%s, %s, %s);'

    cursor.executemany(insert_new_programs, insert_data)
    connector.connector.commit()
    cursor.close()
