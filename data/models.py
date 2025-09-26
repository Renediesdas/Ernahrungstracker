import sqlite3

conn = sqlite3.connect("data.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS meals (
    id INTEGER PRIMARY KEY,
    name TEXT,
    kcal INT,
    fat INT
)
""")

# Beispiel-Daten
conn.execute("INSERT INTO meals (name, kcal, fat) VALUES ('Bolognese', 500, 20)")
conn.execute("INSERT INTO meals (name, kcal, fat) VALUES ('Lasagne', 700, 25)")
conn.commit()
conn.close()
