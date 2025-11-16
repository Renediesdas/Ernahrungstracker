# Mit dem Skript werden die zutaten zugeorndernet gespeichert in einer eigenen tabelle

import psycopg2
import psycopg2.extras
import os

DB_CONN = os.getenv("172.22.0.11", "dbname=tracker user=tracker password=tracker host=172.22.0.11 port=5432")

food = []
nährstoffe = []

gesamtnährstoffe = {
    "name": None,
    "kalorien": None,
    "protein": None,
    "fett": None,
    "kohlenhydrate": None,
    "salz": None,
    "zucker": None
                    }
kalorienlist = []
proteinlist = []
fettlist =[]
kohlenhydratelist = []
salzlist = []
zuckerlist = []

test = []


def insertmeal():

    conn = psycopg2.connect(
    dbname="tracker",
    user="tracker",
    password="tracker",
    host="172.22.0.11",
    port="5432"
    )
    cursor = conn.cursor()

    meal = input("Mealname: ")
    while True:
        name = input ("Name oder Stop: ")
        if name.lower() == "stop":
            break
        if name == "Hafer":
            name = "Haferflocken"
        if name == "Mus":
            name = "Haselnussmus"
        if name == "Saft":
            name = "Agavendicksaft"
        gram = int(input("Gram: "))
        #gram = 2

        food.append({"name": name, "gram": gram})

    cursor.execute("SELECT * FROM meal WHERE name = %s", (meal,))
    meal_id = cursor.fetchall()
    if meal_id:
        for e in meal_id:
            meal_id = e[0]
            print("meal", meal, "gefunden") 

    else:
        print("meal", meal, "nicht gefunden. Anlegen..")
        sql_mealanlegen = """
        INSERT INTO meal(name) 
        VALUES(%s)
        RETURNING id, name;
        """
        values = (meal,)

        cursor.execute(sql_mealanlegen, values)
        prufung = cursor.fetchone()

        print("prüfung", prufung)
        meal_id = prufung[0]
        prufung = "-"
        conn.commit()
  
    
    for e in food:
        g = e["gram"]
        print("e: ", e["name"], g)
        
        # with psycopg2.connect(DB_CONN) as conn:
        #     with conn.cursor() as cur:
        #         cur.execute("SELECT * FROM food WHERE name= %s", (e["name"],))
        #         result = cur.fetchall()
        #         headers = [desc[0] for desc in cur.description]

#                result = [dict(zip(headers, row)) for row in cur.fetchall()]
#                nährstoffe.append(result)

        cursor.execute("SELECT * FROM food WHERE name= %s", (e["name"],))
        result = cursor.fetchall()
        
        if result:
            for e in result:
                food_id = e[0]
        else:
            print("food nicht gefunden")
        
        print("meal_id = ", meal_id)
        print("food_id: ", food_id)
        print("gram: ", g)

        sql_zuordnung = """
        INSERT INTO meal_zutaten(meal_id, food_id, gram)
        VALUES(%s, %s, %s)
        RETURNING id
        """
        values = (meal_id,food_id,g,)
        print("values: ", values)

        cursor.execute(sql_zuordnung, values)
        prufung = cursor.fetchone()
        print("angelegt:", prufung[0])
        conn.commit()


    # sql = """
    # INSERT INTO meals(name, kalorien, protein, fett, kohlenhydrate, salz, zucker)
    # VALUES(%s, %s, %s, %s, %s, %s, %s)
    # """

    # data = (
    # gesamtnährstoffe["name"],
    # gesamtnährstoffe["kalorien"],
    # gesamtnährstoffe["protein"],
    # gesamtnährstoffe["fett"],
    # gesamtnährstoffe["kohlenhydrate"],
    # gesamtnährstoffe["salz"],
    # gesamtnährstoffe["zucker"]
    # )

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