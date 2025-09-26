import unicodedata, sys
import sqlite3
import csv

def strip_accents(s: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')

# Datei zeilenweise „entakzentieren“
inp, outp = "grocyproducts.csv", "grocy_ascii.csv"
with open(inp, "r", encoding="utf-8") as fin, open(outp, "w", encoding="utf-8") as fout:
    for line in fin:
        fout.write(strip_accents(line).replace("ß", "ss"))
print("Fertig ->", outp)

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
    print("CSV erfolgreich importiert  ^|^e")

if __name__ == "__main__":
    import_csv("grocyproducts.csv")
