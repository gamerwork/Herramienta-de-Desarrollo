import random
import sqlite3


def obtener_palabras():
    """Devuelve la lista de palabras de la base de datos."""
    conexion = sqlite3.connect("palabras.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT palabra FROM palabras")
    resultado = cursor.fetchall()
    conexion.close()
    return [r[0] for r in resultado]


def seleccionar_palabra(palabras):
    """Selecciona una palabra al azar de la lista."""
    return random.choice(palabras)


def inicializar_palabra_oculta(palabra):
    """Crea la lista con guiones de la palabra oculta."""
    return ["_"] * len(palabra)


def actualizar_palabra_oculta(palabra, palabra_oculta, letra):
    """Actualiza la palabra oculta con la letra adivinada."""
    for i, l in enumerate(palabra):
        if l == letra:
            palabra_oculta[i] = letra
    return palabra_oculta


def letra_correcta(palabra, letra):
    """Devuelve True si la letra está en la palabra."""
    return letra in palabra


def restar_intento(intentos_restantes):
    """Resta un intento."""
    return intentos_restantes - 1
