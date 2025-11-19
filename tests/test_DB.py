# test
import os
import sqlite3
import sys

from ahorcadopy import agregar_palabra_a_bd, obtener_palabras

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def setup_module(module):
    conexion = sqlite3.connect("palabras.db")
    cursor = conexion.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS palabras (palabra TEXT)")
    cursor.execute("DELETE FROM palabras")
    cursor.execute("INSERT INTO palabras VALUES ('python')")
    cursor.execute("INSERT INTO palabras VALUES ('ahorcado')")
    conexion.commit()
    conexion.close()


def test_obtener_palabras():
    palabras = obtener_palabras()
    assert isinstance(palabras, list)
    assert "python" in palabras
    assert "ahorcado" in palabras


def test_agregar_palabra():
    agregar_palabra_a_bd("nueva")
    palabras = obtener_palabras()
    assert "nueva" in palabras


def test_palabra_duplicada(capfd):
    agregar_palabra_a_bd("duplicada")
    agregar_palabra_a_bd("duplicada")

    captured = capfd.readouterr()
    assert "La palabra ya existe" in captured.out


def test_palabra_invalida(capfd):
    agregar_palabra_a_bd("123$$")
    captured = capfd.readouterr()
    assert "Solo se permiten letras" in captured.out
