from flask import Flask, render_template_string
from init_db import init_db
import psycopg2
import psycopg2.extras
import os

# Connection String aus Umgebungsvariablen oder fest
DB_CONN = os.getenv("172.22.0.11", "dbname=tracker user=tracker password=tracker host=172.22.0.11 port=5432")

app = Flask(__name__)

def create_db():
    #Erstellt Tabellen, wenn sie nicht existieren
    with psycopg2.connect(DB_CONN) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS meals (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    kcal INTEGER NOT NULL,
                    fat REAL
                )
           """)
        conn.commit()
    print("Tabellen gepruft/erstellt")

def get_db():
    conn = psycopg2.connect(DB_CONN)
    return conn


@app.route("/")
def index():
    with get_db() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM meals")
            meals = cur.fetchall()

    # total_kcal = sum([m["kcal"] for m in meals])
    total_kcal = 200
    return render_template_string("""
    <h1>Ernaehrungstracker</h1>
    <p>Heute gegessen: {{ kcal }} kcal</p>
    <table border=1>
      <tr><th>Meal</th><th>Kcal</th><th>Fett</th></tr>
      {% for meal in meals %}
        <tr><td>{{ meal['name'] }}</td><td>{{ meal['kcal'] }}</td><td>{{ meal['fat'] }}</td></tr>
      {% endfor %}
    </table>
    """, kcal=total_kcal, meals=meals)


if __name__ == "__main__":
    create_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
