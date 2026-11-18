import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configuración de pantalla (Simulando una proporción vertical de teléfono móvil: 480x800)
ANCHO, ALTO = 480, 800
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("¡Pedido Rápido al Instante!")

# Colores (Paleta moderna y atractiva)
COLOR_FONDO = (245, 247, 250)
COLOR_PANEL = (255, 255, 255)
COLOR_TEXTO = (44, 62, 80)
COLOR_BOTON = (46, 204, 113)
COLOR_BOTON_SEC = (52, 152, 219)
COLOR_ROJO = (231, 76, 60)
COLOR_AZUL = (52, 73, 94)

# Fuentes
fuente_titulo = pygame.font.SysFont("Arial", 36, bold=True)
fuente_texto = pygame.font.SysFont("Arial", 22, bold=True)
fuente_peque = pygame.font.SysFont("Arial", 18)

# Estados del juego
ESTADO_MENU = "menu"
ESTADO_JUEGO = "juego"
ESTADO_TRIVIA = "trivia"
ESTADO_GAMEOVER = "game_over"
estado_actual = ESTADO_MENU

# Variables del juego
puntuacion = 0
monedas = 0
vidas = 3
tiempo_cliente = 100  # Barra de paciencia
cliente_actual = "Pollo Frito"
pos_jugador = 1  # 0: Izquierda, 1: Centro, 2: Derecha

# Banco de preguntas para la Trivia sorpresa
PREGUNTAS = [
    {"pregunta": "¿Cuánto es 8 x 7?", "opciones": ["54", "56", "64"], "correcta": 1},
    {"pregunta": "¿En qué continente está Venezuela?", "opciones": ["América", "África", "Europa"], "correcta": 0},
    {"pregunta": "¿Cuál es la capital de Apure?", "opciones": ["San Fernando", "Maracay", "Barinas"], "correcta": 0},
    {"pregunta": "Si un combo cuesta $5 y pagan con $10, ¿cuánto es el vuelto?", "opciones": ["$3", "$5", "$10"], "correcta": 1}
]
trivia_actual = None
opciones_rects = []

def reiniciar_juego():
    global puntuacion, monedas, vidas, tiempo_cliente, cliente_actual, pos_jugador
    puntuacion = 0
    monedas = 0
    vidas = 3
    tiempo_cliente = 100
    pos_jugador = 1
    nuevo_cliente()

def nuevo_cliente():
    global cliente_actual, tiempo_cliente
    clientes_posibles = ["Pollo Frito", "Hamburguesa", "Refresco", "Papas Fritas"]
    cliente_actual = random.choice(clientes_posibles)
    tiempo_cliente = 100

reloj = pygame.time.Clock()

while True:
    pantalla.fill(COLOR_FONDO)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if estado_actual == ESTADO_MENU:
                if 140 <= mouse_pos[0] <= 340 and 450 <= mouse_pos[1] <= 520:
                    reiniciar_juego()
                    estado_actual = ESTADO_JUEGO
                    
            elif estado_actual == ESTADO_JUEGO:
                if mouse_pos[1] > 550:
                    if mouse_pos[0] < 160:
                        pos_jugador = 0
                    elif mouse_pos[0] < 320:
                        pos_jugador = 1
                    else:
                        pos_jugador = 2
                elif 200 <= mouse_pos[1] <= 450:
                    puntuacion += 10
                    monedas += 5
                    if puntuacion % 30 == 0:
                        trivia_actual = random.choice(PREGUNTAS)
                        estado_actual = ESTADO_TRIVIA
                    else:
                        nuevo_cliente()
                        
            elif estado_actual == ESTADO_TRIVIA:
                for i, rect in enumerate(opciones_rects):
                    if rect.collidepoint(mouse_pos):
                        if i == trivia_actual["correcta"]:
                            puntuacion += 25
                            monedas += 20
                        else:
                            vidas -= 1
                        estado_actual = ESTADO_JUEGO
                        nuevo_cliente()
                        
            elif estado_actual == ESTADO_GAMEOVER:
                if 140 <= mouse_pos[0] <= 340 and 500 <= mouse_pos[1] <= 570:
                    reiniciar_juego()
                    estado_actual = ESTADO_JUEGO

    if estado_actual == ESTADO_MENU:
        titulo = fuente_titulo.render("¡PEDIDO RÁPIDO!", True, COLOR_AZUL)
        subtitulo = fuente_texto.render("Sabor que atrapa al instante", True, COLOR_BOTON_SEC)
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 200))
        pantalla.blit(subtitulo, (ANCHO//2 - subtitulo.get_width()//2, 250))
        
        btn_rect = pygame.Rect(140, 450, 200, 70)
        pygame.draw.rect(pantalla, COLOR_BOTON, btn_rect, border_radius=15)
        txt_btn = fuente_texto.render("JUGAR", True, (255, 255, 255))
        pantalla.blit(txt_btn, (btn_rect.centerx - txt_btn.get_width()//2, btn_rect.centery - txt_btn.get_height()//2))

    elif estado_actual == ESTADO_JUEGO:
        tiempo_cliente -= 0.35
        if tiempo_cliente <= 0:
            vidas -= 1
            tiempo_cliente = 100
            if vidas <= 0:
                estado_actual = ESTADO_GAMEOVER
            else:
                nuevo_cliente()

        pygame.draw.rect(pantalla, COLOR_PANEL, (0, 0, ANCHO, 80))
        txt_score = fuente_texto.render(f"Puntos: {puntuacion}", True, COLOR_TEXTO)
        txt_coins = fuente_texto.render(f"Monedas: ?? {monedas}", True, (241, 196, 15))
        txt_vidas = fuente_texto.render(f"Vidas: {'??' * vidas}", True, COLOR_ROJO)
        
        pantalla.blit(txt_score, (20, 25))
        pantalla.blit(txt_coins, (280, 25))
        pantalla.blit(txt_vidas, (20, 55))

        pygame.draw.rect(pantalla, (236, 240, 241), (30, 120, 420, 250), border_radius=15)
        txt_pedido_titulo = fuente_peque.render("CLIENTE ESPERANDO:", True, COLOR_AZUL)
        txt_pedido = fuente_titulo.render(cliente_actual, True, COLOR_ROJO)
        pantalla.blit(txt_pedido_titulo, (50, 140))
        pantalla.blit(txt_pedido, (50, 170))

        pygame.draw.rect(pantalla, (218, 225, 231), (50, 240, 380, 20), border_radius=10)
        ancho_barra = int(380 * (tiempo_cliente / 100))
        if ancho_barra > 0:
            pygame.draw.rect(pantalla, COLOR_ROJO, (50, 240, ancho_barra, 20), border_radius=10)

        txt_accion = fuente_texto.render("¡Haz clic aquí para entregar pedido!", True, COLOR_AZUL)
        pantalla.blit(txt_accion, (ANCHO//2 - txt_accion.get_width()//2, 300))

        estaciones = ["Estación 1", "Estación 2", "Estación 3"]
        for i, est in enumerate(estaciones):
            color_est = COLOR_BOTON_SEC if pos_jugador == i else (189, 195, 199)
            rect_est = pygame.Rect(30 + (i * 140), 600, 120, 120)
            pygame.draw.rect(pantalla, color_est, rect_est, border_radius=15)
            txt_est = fuente_peque.render(est, True, (255, 255, 255))
            pantalla.blit(txt_est, (rect_est.centerx - txt_est.get_width()//2, rect_est.centery - txt_est.get_height()//2))

    elif estado_actual == ESTADO_TRIVIA:
        pygame.draw.rect(pantalla, COLOR_AZUL, (30, 150, 420, 500), border_radius=20)
        txt_alerta = fuente_texto.render("¡CLIENTE VIP / RETO MENTAL!", True, (241, 196, 15))
        pantalla.blit(txt_alerta, (ANCHO//2 - txt_alerta.get_width()//2, 180))
        
        txt_preg = fuente_texto.render(trivia_actual["pregunta"], True, (255, 255, 255))
        pantalla.blit(txt_preg, (ANCHO//2 - txt_preg.get_width()//2, 250))
        
        opciones_rects = []
        for i, opc in enumerate(trivia_actual["opciones"]):
            rect_opc = pygame.Rect(70, 330 + (i * 80), 340, 60)
            pygame.draw.rect(pantalla, COLOR_PANEL, rect_opc, border_radius=10)
            opciones_rects.append(rect_opc)
            
            txt_opc = fuente_texto.render(opc, True, COLOR_TEXTO)
            pantalla.blit(txt_opc, (rect_opc.centerx - txt_opc.get_width()//2, rect_opc.centery - txt_opc.get_height()//2))

    elif estado_actual == ESTADO_GAMEOVER:
        txt_fin = fuente_titulo.render("¡JUEGO TERMINADO!", True, COLOR_ROJO)
        txt_res = fuente_texto.render(f"Puntuación Final: {puntuacion}", True, COLOR_TEXTO)
        txt_mon = fuente_texto.render(f"Monedas ganadas: ?? {monedas}", True, (241, 196, 15))
        
        pantalla.blit(txt_fin, (ANCHO//2 - txt_fin.get_width()//2, 220))
        pantalla.blit(txt_res, (ANCHO//2 - txt_res.get_width()//2, 290))
        pantalla.blit(txt_mon, (ANCHO//2 - txt_mon.get_width()//2, 330))
        
        btn_rect = pygame.Rect(140, 500, 200, 70)
        pygame.draw.rect(pantalla, COLOR_BOTON, btn_rect, border_radius=15)
        txt_btn = fuente_texto.render("REINTENTAR", True, (255, 255, 255))
        pantalla.blit(txt_btn, (btn_rect.centerx - txt_btn.get_width()//2, btn_rect.centery - txt_btn.get_height()//2))

    pygame.display.flip()
    reloj.tick(60)