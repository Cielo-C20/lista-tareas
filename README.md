# Lista de tareas

App web sencilla hecha con **Python + Flask + SQLite**. Permite agregar, completar y borrar tareas, y muestra tu progreso.

## Cómo ejecutarla

```bash
python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Abre http://127.0.0.1:5000 en tu navegador. La base de datos (`tareas.db`) se crea sola la primera vez.

## Estructura

- `app.py`: servidor Flask, rutas y base de datos SQLite
- `templates/index.html`: página principal
- `static/style.css`: estilos
