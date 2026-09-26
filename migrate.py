import sqlite3
import json


conn = sqlite3.connect("garden.db")
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS garden(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    date TEXT NOT NULL
    )
    """
)

with open('garden.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

cursor.executemany(
    "INSERT INTO garden (name, quantity, date) VALUES (:name, :quantity, :date)",
    data
)
conn.commit()

cursor.execute(
    "SELECT * FROM garden"
)
result_garden = cursor.fetchall()
print(result_garden)
conn.commit()
conn.close()