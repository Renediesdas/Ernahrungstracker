# Mit dem Skript werden die zutaten zugeorndernet gespeichert in einer eigenen tabelle

import psycopg2
import psycopg2.extras
import os

DB_CONN = os.getenv("172.22.0.11", "dbname=tracker user=tracker password=tracker host=172.22.0.11 port=5432")

food = []
nährstoffe = []

def insertmeal():

    conn = psycopg2.connect(
    dbname="tracker",
    user="tracker",
    password="tracker",
    host="172.22.0.11",
    port="5432"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT id,name FROM meal")
    result = cursor.fetchall()
    for e in result:
        print(e)

    meal = input("Mealname: ")
    mahlzeit = input("Mahlzeit: Morgen(mg)/Vormittag(vm)/Nachmittag(nm)/Abend(ab)")

    meal = f"%{meal}%"
    mahlzeit = f"%{mahlzeit}%"

    print("mealinput ",meal)
    print("mahlzeitinput ",mahlzeit)

    if mahlzeit == 'mg':
        mahlzeit = 'Morgen'
    if mahlzeit == 'vm':
        mahlzeit = 'Vormittag'
    if mahlzeit == 'nm':
        mahlzeit = 'Nachmittag'
    if mahlzeit == 'ab':
        mahlzeit = 'Abend'

    cursor.execute("SELECT id,name FROM meal WHERE name LIKE %s", (meal,))
    result = cursor.fetchone()
    if result:
        meal_id = result[0]
        meal = result[1]
    else:
        print(meal, "nicht gefunden")


    cursor.execute("SELECT id,name FROM mahlzeiten WHERE name LIKE %s", (mahlzeit,))
    result = cursor.fetchone()
    if result:
        mz_id = result[0]
        mahlzeit = result[1]
    else:
        print(mahlzeit, "nicht gefunden")

    print("mealname: ", meal)
    print("meal_id :", meal_id)
    print("mahlzeitname : ", mahlzeit)
    print("mahlzeit_id :", mz_id)

    if meal_id and mz_id:

        sql_addmeal = """
            INSERT INTO gegessen(meal, tageszeit)
            VALUES(%s, %s)
            RETURNING id
            """
        values = (meal_id,mz_id,)
        cursor.execute(sql_addmeal, values)
        conn.commit()

    else:
        print("ein eintrag fehlt")

    # cursor.execute(sql, data)
    # conn.commit()
    # if cursor.rowcount == 1:
    #     print("angelegt")
    # else:
    #     print("nicht angelegt")

    # cursor.execute("SELECT * FROM meals")
    # result = cursor.fetchall()

    # if result:
    #     for e in result:
    #         print(e)
    # else:
    #     print("nichts gefunden")

    
    




if __name__ == "__main__":
    insertmeal()