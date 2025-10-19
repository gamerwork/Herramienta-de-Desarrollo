import sqlite3

# Conexión a la base de datos (se creará si no existe)
conexion = sqlite3.connect("palabras.db")
cursor = conexion.cursor()

# Crear tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS palabras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    palabra TEXT NOT NULL
)
""")

# Insertar algunas palabras (solo la primera vez)
palabras_iniciales = ['python', 'programacion', 'ahorcado', 'desarrollador', 'computadora','utp']
for p in palabras_iniciales:
    cursor.execute("INSERT INTO palabras (palabra) VALUES (?)", (p,))

conexion.commit()
conexion.close()
