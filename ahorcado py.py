import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 600, 680
pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ahorcado con Pygame")
pygame.mixer.init()

sonido_inicio = pygame.mixer.Sound("sonidos/inicio.wav")
sonido_ganar = pygame.mixer.Sound("sonidos/ganar.wav")
sonido_perder = pygame.mixer.Sound("sonidos/termino.wav")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Fuente
fuente = pygame.font.SysFont('arial', 48)

# Palabras
palabras = ['python', 'programacion', 'ahorcado', 'desarrollador', 'computadora']
palabra = random.choice(palabras)
palabra_oculta = ['_'] * len(palabra)
letras_adivinadas = set()
intentos_restantes = 6

reloj = pygame.time.Clock()

def dibujar_ahorcado(intentos):
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
    pantalla.fill(BLANCO)

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
    intentos_restantes = 6

def mostrar_mensaje(texto, color):
    mensaje = fuente.render(texto, True, color)
    pantalla.blit(mensaje, (WIDTH // 2 - mensaje.get_width() // 2, 400))
    pygame.display.flip()
    pygame.time.delay(2000)

sonido_inicio.play()

# Bucle principal
jugando = True
while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        elif evento.type == pygame.KEYDOWN:
            letra = evento.unicode.lower()
            if letra.isalpha() and len(letra) == 1 and letra not in letras_adivinadas:
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
        sonido_ganar.play()
        mostrar_mensaje("¡Ganaste!", (0, 150, 0))
        pygame.time.delay(2000)  # Espera 2 segundos para que suene
        jugando = False
    elif intentos_restantes == 0:
        sonido_perder.play()
        mostrar_mensaje(f"¡Perdiste! Era: {palabra}", (200, 0, 0))
        pygame.time.delay(2000)
        jugando = False


    dibujar()
    reloj.tick(30)

pygame.quit()
sys.exit()
