import sqlite3
from contextlib import closing
from config import DB_PATH


def connect_db():
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_db():
    with closing(connect_db()) as conn:
        conn.execute(
    """
    CREATE TABLE IF NOT EXISTS garden(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    date TEXT NOT NULL
    )
    """
)
        conn.commit()


def insert_plant(name, quantity, date):
    with closing(connect_db()) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO garden (name, quantity, date) VALUES (?, ?, ?)",
            (name, quantity, date)
        )
        conn.commit()


def delete_plant_by_id(id_plant):
    with closing(connect_db()) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM garden WHERE id = ?",
            (id_plant,)
        )
        conn.commit()


def update_plant_name(up_name, plant_id):
    with closing(connect_db()) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE garden SET name = ? WHERE id = ?",
            (up_name, plant_id)
        )
        conn.commit()


def update_plant_quantity(up_quantity, plant_id):
    with closing(connect_db()) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE garden SET quantity = ? WHERE id = ?",
            (up_quantity, plant_id)
        )
        conn.commit()


def search_plants_by_name(plant_search):
    with closing(connect_db()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, quantity, date FROM garden WHERE name LIKE ?",
            ("%" + plant_search + "%",)
        )
        list_tuple = cursor.fetchall()
        result = [dict(row) for row in list_tuple]
    return result


def length_and_total_plant():
    with closing(connect_db()) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*), SUM(quantity) FROM garden ",
        )
        result = cursor.fetchone()
        length = result[0]
        total = result[1]
        return length, total


def max_and_min_plant():
    with closing(connect_db()) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name, quantity FROM garden ORDER BY quantity DESC LIMIT 1",
        )
        result = cursor.fetchone()
        plant_name_max = result[0]
        plant_max = result[1]

        cursor.execute(
            "SELECT name, quantity FROM garden ORDER BY quantity ASC LIMIT 1",
        )
        result = cursor.fetchone()
        plant_name_min = result[0]
        plant_min = result[1]
        return plant_name_max, plant_max, plant_name_min, plant_min


def get_plants_sorted_by_quantity():
    with closing(connect_db()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, quantity, date FROM garden ORDER BY quantity ASC",
        )
        list_tuple = cursor.fetchall()
        list_tuple_increase = [dict(row) for row in list_tuple]

        cursor.execute(
            "SELECT id, name, quantity, date FROM garden ORDER BY quantity DESC",
        )
        list_tuple = cursor.fetchall()
        list_tuple_decrease = [dict(row) for row in list_tuple]
        return list_tuple_increase, list_tuple_decrease


def get_plants_sorted_by_date():
    with closing(connect_db()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, quantity, date FROM garden ORDER BY substr(date, 7, 4) || '-' || substr(date, 4, 2) || '-' || substr(date, 1, 2) ASC",
        )
        list_tuple = cursor.fetchall()
        list_tuple_increase = [dict(row) for row in list_tuple]

        cursor.execute(
            "SELECT id, name, quantity, date FROM garden ORDER BY substr(date, 7, 4) || '-' || substr(date, 4, 2) || '-' || substr(date, 1, 2) DESC",
        )
        list_tuple = cursor.fetchall()
        list_tuple_decrease = [dict(row) for row in list_tuple]
        return list_tuple_increase, list_tuple_decrease


def get_all_plants():
    with closing(connect_db()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, quantity, date FROM garden",
        )
        list_tuple = cursor.fetchall()
        result = [dict(row) for row in list_tuple]
    return result
