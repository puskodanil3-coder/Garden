import sqlite3
from contextlib import closing
from config import TABLE_WIDTH, print_success
from utils import pause_and_clear, is_garden_empty, clear_console


def connecting_db():
    conn = sqlite3.connect('garden.db')
    return conn


def init_db():
    with closing(connecting_db()) as conn:
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


def add_plant_in_db(name, quantity, date):
    with closing(connecting_db()) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO garden (name, quantity, date) VALUES (?, ?, ?)",
            (name, quantity, date)
        )
        conn.commit()


def delete_plant_in_db(id_plant):
    with closing(connecting_db()) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM garden WHERE id = ?",
            (id_plant,)
        )
        conn.commit()


def update_name(up_name, plant_id):
    with closing(connecting_db()) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE garden SET name = ? WHERE id = ?",
            (up_name, plant_id)
        )
        conn.commit()


def update_quantity(up_quantity, plant_id):
    with closing(connecting_db()) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE garden SET quantity = ? WHERE id = ?",
            (up_quantity, plant_id)
        )
        conn.commit()


def load_garden():
    with closing(connecting_db()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, quantity, date FROM garden",
        )
        list_tuple = cursor.fetchall()
        result = [dict(row) for row in list_tuple]
    return result


def export_to_txt():
    plant_list = load_garden()
    if is_garden_empty(plant_list, 'нечего экспортировать'):
        pause_and_clear()
        return True
    with open('garden_report.txt', 'w', encoding='utf-8') as f:
        f.write('Список растений в саду:\n')
        f.write("-" * TABLE_WIDTH+ "\n")
        f.write(f"\n{'№':>3} {'Название':<20} {'Количество':>12} {'Дата':>12}\n")
        for number, plant in enumerate(plant_list, start=1):
            f.write(f"{number:>3} {plant['name']:<20} {plant['quantity']:>12} {plant['date']:>12}\n")
        f.write("-" * TABLE_WIDTH+ "\n")
        length = len(plant_list)
        f.write(f'\nКоличество всех видов растений в саду: {length} шт.')
        total = sum(plant['quantity'] for plant in plant_list)
        f.write(f'\nКоличество всех растений в саду: {total} шт.')

        max_plant = max(plant_list, key=lambda plant: plant['quantity'])
        f.write(f'\nСамое многочисленное растение в саду: {max_plant["name"]} - {max_plant["quantity"]} шт.')

        min_plant = min(plant_list, key=lambda plant: plant['quantity'])
        f.write(f'\nСамое малочисленное растение в саду: {min_plant["name"]} - {min_plant["quantity"]} шт.')
        
    clear_console()
    print_success('Экспорт успешно завершен')
    pause_and_clear()
