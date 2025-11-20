from logica_ahorcado import (
    actualizar_palabra_oculta,
    inicializar_palabra_oculta,
    letra_correcta,
    restar_intento,
)


def test_inicializar_palabra_oculta():
    palabra = "python"
    oculta = inicializar_palabra_oculta(palabra)
    assert oculta == ["_", "_", "_", "_", "_", "_"]


def test_actualizar_palabra_oculta():
    palabra = "python"
    oculta = ["_", "_", "_", "_", "_", "_"]
    letra = "o"
    resultado = actualizar_palabra_oculta(palabra, oculta, letra)
    assert resultado == ["_", "_", "_", "_", "o", "_"]


def test_letra_correcta():
    palabra = "python"
    assert letra_correcta(palabra, "p") is True
    assert letra_correcta(palabra, "a") is False


def test_restar_intento():
    intentos = 5
    assert restar_intento(intentos) == 4
