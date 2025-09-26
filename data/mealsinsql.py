import sqlite3
import csv

DB_PATH = "data.db"

def import_csv(file_path):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(file_path, newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for item in row:
                print(item)
                cursor.execute(
                    "INSERT INTO meals (name) VALUES (?)",
                    (item,)  # kcal und fat bleiben leer
                )
    conn.commit()
    conn.close()
    print("CSV erfolgreich importiert ✅")

if __name__ == "__main__":
    import_csv("grocyproducts.csv")
