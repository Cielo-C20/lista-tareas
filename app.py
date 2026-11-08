import sqlite3
from pathlib import Path

from flask import Flask, g, redirect, render_template, request, url_for

DB_PATH = Path(__file__).parent / "tareas.db"
app = Flask(__name__)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def cerrar_db(_error):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def iniciar_db():
    with sqlite3.connect(DB_PATH) as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS tareas (
                id     INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT    NOT NULL,
                hecha  INTEGER NOT NULL DEFAULT 0,
                creada TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


iniciar_db()


@app.get("/")
def inicio():
    tareas = get_db().execute(
        "SELECT * FROM tareas ORDER BY hecha, id DESC"
    ).fetchall()
    total = len(tareas)
    hechas = sum(t["hecha"] for t in tareas)
    avance = round(hechas / total * 100) if total else 0
    return render_template(
        "index.html", tareas=tareas, total=total, hechas=hechas, avance=avance
    )


@app.post("/agregar")
def agregar():
    titulo = request.form.get("titulo", "").strip()
    if titulo:
        db = get_db()
        db.execute("INSERT INTO tareas (titulo) VALUES (?)", (titulo[:200],))
        db.commit()
    return redirect(url_for("inicio"))


@app.post("/alternar/<int:tarea_id>")
def alternar(tarea_id):
    db = get_db()
    db.execute("UPDATE tareas SET hecha = 1 - hecha WHERE id = ?", (tarea_id,))
    db.commit()
    return redirect(url_for("inicio"))


@app.post("/borrar/<int:tarea_id>")
def borrar(tarea_id):
    db = get_db()
    db.execute("DELETE FROM tareas WHERE id = ?", (tarea_id,))
    db.commit()
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=True)
