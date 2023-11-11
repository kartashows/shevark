from contextlib import contextmanager


CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users
(id SERIAL PRIMARY KEY,
user_id TEXT UNIQUE,
company_name TEXT);"""
CREATE_TASK_TABLE = """CREATE TABLE IF NOT EXISTS tasks
(id SERIAL PRIMARY KEY,
user_id TEXT,
file BYTEA,
file_extension TEXT,
creation_date TEXT,
FOREIGN KEY(user_id) REFERENCES users(user_id));"""

ADD_USER = "INSERT INTO users (user_id, company_name) VALUES(%s, %s) ON CONFLICT (user_id) DO NOTHING;"
ADD_TASK = """INSERT INTO tasks (user_id, file, file_extension, creation_date)
VALUES(%s, %s, %s, %s)
RETURNING tasks.id;"""

GET_COMPANY_NAME = "SELECT company_name FROM users WHERE user_id = %s;"

DELETE_TASK = "DELETE FROM tasks WHERE id = %s;"

CHECK_USER = "SELECT EXISTS (SELECT 1 FROM users WHERE user_id = %s);"


@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor

def create_tables(connection):
    with get_cursor(connection) as cursor:
        cursor.execute(CREATE_USERS_TABLE)
        cursor.execute(CREATE_TASK_TABLE)


def add_user(connection, user_id: str,  company_name: str):
    with get_cursor(connection) as cursor:
        cursor.execute(ADD_USER, (user_id, company_name))


def add_task(connection, user_id: str,  file: bytes, file_extension: str, creation_date: str) -> int:
    with get_cursor(connection) as cursor:
        cursor.execute(ADD_TASK, (user_id, file, file_extension, creation_date))
        new_task_id = cursor.fetchone()[0]
        return new_task_id

def get_company_name(connection, user_id: str) -> str:
    with get_cursor(connection) as cursor:
        cursor.execute(GET_COMPANY_NAME, (user_id,))
        name = cursor.fetchone()[0]
        return name

def remove_task(connection, task_id: str):
    with get_cursor(connection) as cursor:
        cursor.execute(DELETE_TASK, (task_id,))


def check_user_exists(connection, user_id: str) -> bool:
    with get_cursor(connection) as cursor:
        cursor.execute(CHECK_USER, (user_id,))
        exists = cursor.fetchone()[0]
        return exists

