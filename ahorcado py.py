import pygame
import random
import sys
import sqlite3

pygame.init()
WIDTH, HEIGHT = 600, 680
pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ahorcado con Pygame")
pygame.mixer.init()

sonido_inicio = pygame.mixer.Sound("sonidos/inicio.wav")
sonido_ganar = pygame.mixer.Sound("sonidos/ganar.wav")
sonido_perder = pygame.mixer.Sound("sonidos/termino.wav")

def obtener_palabras():
    conexion = sqlite3.connect("palabras.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT palabra FROM palabras")
    resultado = cursor.fetchall()
    conexion.close()
    return [r[0] for r in resultado]

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Fuente
fuente = pygame.font.SysFont('arial', 48)

# Palabras
palabras = obtener_palabras()
palabra = random.choice(palabras)
palabra_oculta = ['_'] * len(palabra)
letras_adivinadas = set()
intentos_restantes = 6
dificultad = None
intentos_maximos = 6  # Se actualizará según la dificultad

reloj = pygame.time.Clock()

def mostrar_menu():
    while True:
        pantalla.fill((240, 248, 255))  # Fondo suave
        titulo = fuente.render("Selecciona la Dificultad", True, (70, 90, 110))
        pantalla.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 100))

        # Obtener posición del mouse
        mouse_pos = pygame.mouse.get_pos()

        # Botones
        botones = [
            ("Normal", 6, (100, 250, 150, 60)),
            ("Difícil", 4, (225, 350, 150, 60)),
            ("Imposible", 2, (350, 450, 150, 60)),
        ]

        for texto, intentos, (x, y, w, h) in botones:
            # Verificar si el mouse está encima del botón
            if x <= mouse_pos[0] <= x + w and y <= mouse_pos[1] <= y + h:
                color_boton = (186, 226, 199)  # Hover (verde pastel)
            else:
                color_boton = (180, 180, 180)  # Normal

            pygame.draw.rect(pantalla, color_boton, (x, y, w, h))
            txt = pygame.font.SysFont('arial', 24).render(texto, True, (70, 90, 110))
            pantalla.blit(txt, (x + w // 2 - txt.get_width() // 2, y + h // 2 - txt.get_height() // 2))

        pygame.display.flip()

        # Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mx, my = evento.pos
                for texto, intentos, (x, y, w, h) in botones:
                    if x <= mx <= x + w and y <= my <= y + h:
                        return intentos

def agregar_palabra_a_bd(nueva_palabra):
    conexion = sqlite3.connect("palabras.db")
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO palabras (palabra) VALUES (?)", (nueva_palabra.lower(),))
    conexion.commit()
    conexion.close()

def dibujar_ahorcado(intentos):
    total_partes = 6
    partes_a_dibujar = total_partes - intentos

    if intentos_maximos == 6:
        partes = partes_a_dibujar
    elif intentos_maximos == 4:
        # Dibuja 1.5 partes por intento perdido (aprox)
        partes = round((6 / 4) * partes_a_dibujar)
    elif intentos_maximos == 2:
        # Dibuja 3 partes por intento perdido
        partes = 3 * partes_a_dibujar
    else:
        partes = partes_a_dibujar

    # Asegurarse de no pasar de 6
    partes = min(partes, 6)

    # Base de la horca
    pygame.draw.line(pantalla, NEGRO, (100, 500), (300, 500), 5)  # base
    pygame.draw.line(pantalla, NEGRO, (200, 500), (200, 100), 5)  # poste vertical
    pygame.draw.line(pantalla, NEGRO, (200, 100), (350, 100), 5)  # poste horizontal
    pygame.draw.line(pantalla, NEGRO, (350, 100), (350, 150), 5)  # cuerda

    if intentos <= 5:
        # Cabeza
        pygame.draw.circle(pantalla, NEGRO, (350, 180), 30, 3)
    if intentos <= 4:
        # Cuerpo
        pygame.draw.line(pantalla, NEGRO, (350, 210), (350, 300), 3)
    if intentos <= 3:
        # Brazo izquierdo
        pygame.draw.line(pantalla, NEGRO, (350, 240), (310, 270), 3)
    if intentos <= 2:
        # Brazo derecho
        pygame.draw.line(pantalla, NEGRO, (350, 240), (390, 270), 3)
    if intentos <= 1:
        # Pierna izquierda
        pygame.draw.line(pantalla, NEGRO, (350, 300), (310, 350), 3)
    if intentos == 0:
        # Pierna derecha
        pygame.draw.line(pantalla, NEGRO, (350, 300), (390, 350), 3)


def dibujar():
    pantalla.fill((240, 248, 255))

    # Mostrar palabra
    texto = fuente.render(' '.join(palabra_oculta), True, NEGRO)
    pantalla.blit(texto, (100, 600))

    # Mostrar letras usadas
    letras_texto = pygame.font.SysFont('arial', 24).render(f"Letras: {' '.join(sorted(letras_adivinadas))}", True, NEGRO)
    pantalla.blit(letras_texto, (100, 510))

    # Mostrar intentos restantes
    intentos_texto = pygame.font.SysFont('arial', 24).render(f"Intentos: {intentos_restantes}", True, NEGRO)
    pantalla.blit(intentos_texto, (100, 550))

    dibujar_ahorcado(intentos_restantes)

    # Botón de reinicio
    pygame.draw.rect(pantalla, (200, 200, 200), (400, 540, 150, 50))  # Botón gris
    texto_boton = pygame.font.SysFont('arial', 24).render("Reiniciar", True, NEGRO)
    pantalla.blit(texto_boton, (425, 555))

    pygame.display.flip()

def reiniciar_juego():
    global palabra, palabra_oculta, letras_adivinadas, intentos_restantes
    palabra = random.choice(palabras)
    palabra_oculta = ['_'] * len(palabra)
    letras_adivinadas = set()
    intentos_restantes = intentos_maximos

def mostrar_mensaje(texto, color):
    mensaje = fuente.render(texto, True, color)
    pantalla.blit(mensaje, (WIDTH // 2 - mensaje.get_width() // 2, 400))
    pygame.display.flip()
    pygame.time.delay(2000)

def mostrar_pantalla_final(mensaje_texto, color):
    pantalla.fill(BLANCO)
    
    mensaje = fuente.render(mensaje_texto, True, color)
    pantalla.blit(mensaje, (WIDTH // 2 - mensaje.get_width() // 2, HEIGHT // 2 - 50))

    pygame.display.flip()
    pygame.time.delay(1000)  # Espera 1 segundos antes de cerrar

sonido_inicio.play()

intentos_maximos = mostrar_menu()
intentos_restantes = intentos_maximos

# Variables para el menú de ingreso de palabras
mostrando_menu_agregar = False
texto_nueva_palabra = ""

def dibujar_menu_agregar():
    # Fondo semitransparente
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((50, 50, 50))
    pantalla.blit(overlay, (0, 0))

    # Contenedor
    rect_menu = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 - 100, 400, 200)
    pygame.draw.rect(pantalla, (240, 248, 255), rect_menu, border_radius=10)
    pygame.draw.rect(pantalla, (0, 0, 0), rect_menu, 2)

    # Título
    titulo = pygame.font.SysFont('arial', 28).render("Agregar nueva palabra", True, (0, 0, 0))
    pantalla.blit(titulo, (WIDTH//2 - titulo.get_width()//2, rect_menu.y + 20))

    # Campo de texto
    rect_input = pygame.Rect(rect_menu.x + 50, rect_menu.y + 80, 300, 40)
    pygame.draw.rect(pantalla, (255, 255, 255), rect_input)
    pygame.draw.rect(pantalla, (0, 0, 0), rect_input, 2)

    # Texto escrito
    texto_render = pygame.font.SysFont('arial', 28).render(texto_nueva_palabra, True, (0, 0, 0))
    pantalla.blit(texto_render, (rect_input.x + 10, rect_input.y + 5))

    # Instrucciones
    instrucciones = pygame.font.SysFont('arial', 20).render("Enter = guardar   |   Esc = salir", True, (0, 0, 0))
    pantalla.blit(instrucciones, (WIDTH//2 - instrucciones.get_width()//2, rect_menu.y + 140))

# Bucle principal
jugando = True
while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

        # 🟡 Si está abierto el menú de agregar palabras
        elif mostrando_menu_agregar:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if texto_nueva_palabra.strip():
                        agregar_palabra_a_bd(texto_nueva_palabra.strip())
                        palabras = obtener_palabras()
                    texto_nueva_palabra = ""
                    mostrando_menu_agregar = False

                elif evento.key == pygame.K_ESCAPE:
                    texto_nueva_palabra = ""
                    mostrando_menu_agregar = False

                elif evento.key == pygame.K_BACKSPACE:
                    texto_nueva_palabra = texto_nueva_palabra[:-1]

                else:
                    if evento.unicode.isalpha():
                        texto_nueva_palabra += evento.unicode.lower()

        # 🟢 Si está en el juego normal
        else:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_TAB:  # Abrir menú
                    mostrando_menu_agregar = True

                elif evento.unicode.isalpha() and len(evento.unicode) == 1 and evento.unicode.lower() not in letras_adivinadas:
                    letra = evento.unicode.lower()
                    letras_adivinadas.add(letra)
                    if letra in palabra:
                        for i, l in enumerate(palabra):
                            if l == letra:
                                palabra_oculta[i] = letra
                    else:
                        intentos_restantes -= 1

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                if 400 <= x <= 550 and 540 <= y <= 590:
                    reiniciar_juego()
                    sonido_inicio.play()

    if '_' not in palabra_oculta:
        dibujar()  # Asegura que se vea el dibujo final
        pygame.display.flip()
        pygame.time.delay(2000)
        sonido_ganar.play()
        mostrar_pantalla_final("¡Ganaste!", (90, 170, 120))
        jugando = False

    elif intentos_restantes == 0:
        dibujar()  # Asegura que se vea el muñeco completo
        pygame.display.flip()
        pygame.time.delay(2000)
        sonido_perder.play()
        mostrar_pantalla_final(f"¡Perdiste! Era: {palabra}", (200, 0, 0))
        jugando = False


    if mostrando_menu_agregar:
        dibujar()
        dibujar_menu_agregar()
    else:
        dibujar()

    pygame.display.flip()
    reloj.tick(30)

pygame.quit()
sys.exit()
