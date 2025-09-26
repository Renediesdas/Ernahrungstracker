import os
import sqlite3

DB_PATH="./data.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    

        # Tabellen erstellen
    cursor.execute("""
    CREATE TABLE meals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        kcal INTEGER NOT NULL,
        fat REAL
    )
    """)
    cursor.execute("""
    CREATE TABLE goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        target_kcal INTEGER NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE diary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        meal_id INTEGER,
        FOREIGN KEY(meal_id) REFERENCES meals(id)
    )
    """)
    conn.commit()
    print("Neue Datenbank erstellt.")
    conn.close()

if __name__ == "__main__":
    init_db()
