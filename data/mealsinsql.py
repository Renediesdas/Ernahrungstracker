import psycopg2
import psycopg2.extras
import os

DB_CONN = os.getenv("172.22.0.11", "dbname=tracker user=tracker password=tracker host=172.22.0.11 port=5432")
food = []
nährstoffe = []

def insertmeal():
    while True:
        name = input ("Name oder Stop: ")
        if name.lower() == "stop":
            break
        gram = int(input("Gram: "))

        food.append({"Name": name, "Gram": gram})

        print(food)

    for e in food:
        print("e: ", e["Name"])
        with psycopg2.connect(DB_CONN) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM food WHERE name= %s", (e["Name"],))
                result = cur.fetchall()
                nährstoffe.append(result)
                headers = [desc[0] for desc in cur.description]

    if nährstoffe:
        print(headers)
        for row in nährstoffe:
            print(row)
    else:
        print("kein eintrag gefunden2:" , name)
    print("worked2")
                        


if __name__ == "__main__":
    insertmeal()
