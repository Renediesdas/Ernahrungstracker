from flask import Flask, render_template_string
from init_db import init_db
import sqlite3
import os

DB_PATH = "./data.db"

app = Flask(__name__)

def create_db():
    first_run = not os.path.exists(DB_PATH)
    if first_run:
        print("datenbank anlagen")
        init_db(DB_PATH)
    else:
        print("datenbank vorhanden")


def get_db():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    db = get_db()
    meals = db.execute("SELECT * FROM meals").fetchall()
    #total_kcal = sum([m["kcal"] for m in meals])
    total_kcal = 200
    return render_template_string("""
    <h1>Ernährungstracker</h1>
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
