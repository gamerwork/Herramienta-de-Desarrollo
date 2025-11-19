# test
import os
import sys

from ahorcadopy import agregar_palabra_a_bd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_palabra_duplicada(capfd):
    agregar_palabra_a_bd("duplicada")
    agregar_palabra_a_bd("duplicada")

    captured = capfd.readouterr()
    assert "La palabra ya existe" in captured.out


def test_palabra_invalida(capfd):
    agregar_palabra_a_bd("123$$")
    captured = capfd.readouterr()
    assert "Solo se permiten letras" in captured.out
