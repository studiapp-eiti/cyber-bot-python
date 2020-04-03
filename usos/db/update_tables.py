from db.db_connector import DbConnector, db_safe_transaction
from usos.obj.user import User


def update_usos_courses(courses: set):
    """Update `usos_courses` table

    :param courses: Set of usos courses
    """
    columns = [
        'course_id', 'course_name_pl',
        'course_name_en', 'term_id'
    ]
    generic_update_table(
        objects=courses,
        table_name='usos_courses',
        columns=columns,
        obj_pkey=lambda c: c.course_id,
        obj_to_tuple=lambda c: (
            c.course_id, c.course_name_pl,
            c.course_name_en, c.term_id
        ))


def update_usos_programs(programs: set):
    """Update `usos_programs` table

    :param programs: Set of usos programs
    """
    columns = [
        'program_id', 'program_name_pl', 'short_program_name_pl',
        'program_name_en', 'short_program_name_en'
    ]
    generic_update_table(
        objects=programs,
        table_name='usos_programs',
        columns=columns,
        obj_pkey=lambda p: p.program_id,
        obj_to_tuple=lambda p: (
            p.program_id, p.program_name_pl, p.short_program_name_pl,
            p.program_name_en, p.short_program_name_en
        ))


@db_safe_transaction('usos')
def update_new_usos_points(points: set):
    """Insert new points into `usos_points` table

    It doesn't utilize `generic_update_table()` function because
    it doesn't have a single primary key. In this case it's
    compilation of `node_id` and `student_id` attributes.

    :param points: Set of user points
    """
    columns = [
        'node_id', 'name', 'points', 'comment',
        'grader_id', 'student_id', 'last_changed', 'course_id'
    ]
    connection = DbConnector.get_connection()
    cursor = connection.cursor(dictionary=True)
    get_pkeys_query = 'select node_id, student_id from usos_points;'
    cursor.execute(get_pkeys_query)

    pkeys = {hash((str(i['node_id']), str(i['student_id']))) for i in cursor}
    insert_data = []
    for p in points:
        if hash((str(p.node_id), str(p.student_id))) not in pkeys:
            insert_data.append((
                p.node_id, p.name, p.points, p.comment,
                p.grader_id, p.student_id, p.last_changed, p.course_id
            ))

    if len(insert_data) == 0:
        cursor.close()
        return

    insert_new_data = 'insert into usos_points ({}) values ({});'.format(
        ', '.join(columns), ', '.join(['%s' for i in range(len(columns))])
    )

    cursor.executemany(insert_new_data, insert_data)
    connection.commit()
    cursor.close()


@db_safe_transaction('usos')
def update_modified_usos_points(points: set, user: User):
    """Update `usos_points` table with new points, comment and last changed time

    :param points: Set with points that were modified
    :param user: User to whom the points belong
    """
    update_query = 'update usos_points set points = %s, comment = %s, last_changed = %s ' \
                   'where node_id = %s and student_id = %s;'
    cursor = DbConnector.get_connection().cursor()
    for p in points:
        cursor.execute(update_query, (
            p.points, p.comment, p.last_changed, p.node_id, user.usos_id
        ))

    cursor.close()


@db_safe_transaction('usos')
def generic_update_table(objects: set, table_name: str, columns: list, obj_pkey, obj_to_tuple):
    """Generic function to update tables in database

    It searches for objects that aren't in the table yet and inserts them respectively.

    :param objects: Objects to be inserted
    :param table_name: Table name that we want to insert records
    :param columns: List of columns we want to insert. First element should be primary key column name
    :param obj_pkey: Function that extracts primary key (unique) attribute from object
    For example: lambda x: x.some_primary_key_attribute
    :type obj_pkey: function
    :param obj_to_tuple: Function that converts object to tuple. Returned tuple should have the same length
    as `columns` parameter and have attributes in the same order.
    For example: if `columns` is defined as ['pkey', 'name', 'other_attr'], it should look something like this:
    lambda x: (x.pkey, x.name, x.other_attr)
    :type obj_to_tuple: function
    """
    connection = DbConnector.get_connection()
    cursor = connection.cursor()
    get_pkeys_query = 'select {} from {};'.format(columns[0], table_name)
    cursor.execute(get_pkeys_query)

    pkeys = {i for (i,) in cursor}
    insert_data = []
    for obj in objects:
        if obj_pkey(obj) not in pkeys:
            insert_data.append(obj_to_tuple(obj))

    if len(insert_data) == 0:
        cursor.close()
        return

    insert_new_data = 'insert into {} ({}) values ({});'.format(
        table_name, ', '.join(columns), ', '.join(['%s' for i in range(len(columns))])
    )

    cursor.executemany(insert_new_data, insert_data)
    connection.commit()
    cursor.close()
