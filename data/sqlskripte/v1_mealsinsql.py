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
        headers = [desc[0] for desc in cursor.description]

        for e in result:
            nährstoffe.append(dict(zip(headers, e)))

    #print(nährstoffe)

    if nährstoffe:
        #print(nährstoffe)
        for e in nährstoffe:
                print(e)

                for f in food:
                    if f["name"] == e["name"]:
                        print(e["name"], f["gram"])

                        kcal = ( e["kalorien"] / 100 ) * f["gram"]
                        kalorienlist.append(kcal)

                        prot = (e["protein"] / 100) * f["gram"]
                        proteinlist.append(prot)

                        fett = (e["fett"] / 100) * f["gram"]
                        fettlist.append(fett)

                        kohl = (e["kohlenhydrate"] / 100) * f["gram"]
                        kohlenhydratelist.append(kohl)

                        salz = (e["salz"] / 100) * f["gram"]
                        salzlist.append(salz)

                        zuck = (e["zucker"] / 100) * f["gram"]
                        zuckerlist.append(zuck)

    else:
        print("kein eintrag gefunden2:" , name)
    
    kcalsum = sum(kalorienlist)
    protsum = sum(proteinlist)
    fettsum = sum(fettlist)
    kohlsum = sum(kohlenhydratelist)
    salzsum = sum(salzlist)
    zucksum = sum(zuckerlist)

    gesamtnährstoffe = {
        "name": meal,
        "kalorien": kcalsum,
        "protein": protsum,
        "fett": fettsum,
        "kohlenhydrate": kohlsum,
        "salz": salzsum,
        "zucker": zucksum
                        }

    print(gesamtnährstoffe)

    sql = """
    INSERT INTO meals(name, kalorien, protein, fett, kohlenhydrate, salz, zucker)
    VALUES(%s, %s, %s, %s, %s, %s, %s)
    """

    data = (
    gesamtnährstoffe["name"],
    gesamtnährstoffe["kalorien"],
    gesamtnährstoffe["protein"],
    gesamtnährstoffe["fett"],
    gesamtnährstoffe["kohlenhydrate"],
    gesamtnährstoffe["salz"],
    gesamtnährstoffe["zucker"]
    )

    cursor.execute(sql, data)
    conn.commit()
    if cursor.rowcount == 1:
        print("angelegt")
    else:
        print("nicht angelegt")

    cursor.execute("SELECT * FROM meals")
    result = cursor.fetchall()

    if result:
        for e in result:
            print(e)
    else:
        print("nichts gefunden")

    
    




if __name__ == "__main__":
    insertmeal()