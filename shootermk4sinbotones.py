#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 01:17:27 2022

@author: alexs2
"""
"""
IMPORTAR LAS LIBRERIAS NECESARIAS PARA EL FUNCIONAMIENTO DEL PROGRAMA, COMO TAL:
PYGAME - LIBRERÍA PARA CREACIÓN DE INSTANCIAS O RUTINAS DE PROCESAMIENTO GRÁFICO PARA ELABORACIÓN DE VIDEOJUEGOS
PYGAME/MIXER - LIBRERÍA PARA UTILIZACIÓN DE ARCHIVOS DE AUDIO
OS - PARA ACCEDER A DIRECTORIOS DEL SISTEMA
RANDOM - PARA GENERAR NUMEROS ALEATORIOS
CSV - PARA MANEJO DE ARCHIVOS .CSV
TIME - PARA CONOCER LA HORA DEL ORDENADOR
DATETIME/TIMEDELTA - PARA ASIGNAR FECHA ACTUAL A UN ARCHIVO O LINEA DE CODIGO
TIMER - PARA CRONOMETRAR UN PROCESO DE CODIGO EN TIEMPO REAL
SERIAL - PARA COMUNICACIÓN CON EL PUERTO SERIAL DEL CPU
PYNPUT/CONTROLLER - PARA ASIGNAR UN OBJETO CONTROLADOR QUE FUNCIONE A MANERA DEL TECLADO O ENTRADA USB
"""
import pygame
from pygame import mixer
import os
import random
import csv
import time
from datetime import datetime
from datetime import timedelta
from timeit import default_timer as timer
import serial
from pynput.keyboard import Controller
#COMENTAR DE LA LINEA 34 A LA LINEA 52 PARA USAR EL VIDEOJUEGO SIN TEMER EL CONTROL CONECTADO
#INICIAR LA COMUNICACION SERIAL EN EL PUERTO DONDE SE UBIQUE EL ARDUINO NANO
ser = serial.Serial("/dev/cu.usbserial-1110")
##SE REINICIA ESA CONEXION AL MOMENTO DE HACERSE, CON EL OBJETIVO DE AJUSTAR LA ESTABILIDAD Y EVITAR FALLOS
with ser:
    #SETDTR ES PARA ENVIAR UNA SEÑAL FALSE Ó 0 AL MICROCONTROLADOR
    ser.setDTR(False)
    #ESTO ES PARA DETENER CUALQUIER PROCESO DEL MICROCONTROLADOR POR UN TIEMPO DETERMINADO
    time.sleep(0.3)
    #ESTO ES PARA LIMPIAR LA TRANSMISION DE DATOS EN EL PUERTO SERIAL
    ser.flushInput()
    #SE ENVIA LA SEÑAL CONTRARIA PARA REESTABLECER EL PROCESO DE COMUNICACIÓN ENTRE CPU Y MICROCONTROLADOR
    ser.setDTR(True)

##ESTE FRAGMENTO REALIZA LO ANTERIOR DESCRITO POR SEGUNDA VEZ
ser = serial.Serial("/dev/cu.usbserial-1110", baudrate=9600)
# resetear el arduino para evitar fallos
ser.setDTR(False)
time.sleep(0.3)
ser.flushInput()
ser.setDTR(True)

#UNA VARIABLE TECLADO SE INICIALIZA COMO CONTROLADOR PARA EL INPUT DEL VIDEOJUEGO
keyboard = Controller()

#CREACION DEL NOMBRE DEL ARCHIVO
filename = "loggerdata/" + "biologger phase A " + datetime.now().strftime("%d.%m.%Y, %H:00:00") + ".csv"

#INICIAR TANTO LA REPRODUCCION DE ARCHIVOS DE AUDIO COMO LA INSTANCIA DE JUEGO PYGAME
mixer.init()
pygame.init()

#INICIAR EL CRONOMETRO
start_time = timer()

##DEFINIR LAS VARIABLES DEL ANCHO Y ALTO DE PANTALLA EN PIXELES
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

#CON BASE EN LAS VARIABLES ANTERIORES, CREAR LA VENTANA DEL VIDEOJUEGO
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#SE LE COLOCA TITULO A LA VENTANA
pygame.display.set_caption('THE ELDER JUNGLES')

#CON ESTO SE INICIALIZA LA TASA DE CUADROS POR SEGUNDO
clock = pygame.time.Clock()
FPS = 60

"""
VARIABLES NECESARIAS PARA EL VIDEOJUEGO:
GRAVITY - SIMULACION DE GRAVEDAD PARA SALTOS DEL JUGADOR (MEDIDA EN TIEMPO, ES DECIR, CUANTO TIEMPO EN SEGUNDOS PERMANECE EN EL AIRE Y CAE)
SCROLL_TRESH - VELOCIDAD DE DESPLAZAMIENTO DE CAMARA A TRAVÉS DEL ESCENARIO
ROWS, COLS - FILAS Y COLUMNAS DE TILES, U OBJETOS GRAFICOS DEL ENTORNO, CONTENIDOS EN CADA ESCENARIO
TILE_SIZE = TAMAÑO QUE VA A OCUPAR CADA CUADRO DE TILE EN LA CUADRICULA RESULTANTE DEFINIDA EN LAS VARIABLES ANTERIORES
TILE_TYPES - CUANTOS RECURSOS GRAFICOS (TILES) VAN A SER NECESARIOS PARA GENERAR TODA LA ESTRUCTURA GRAFICA DE CADA ESCENARIO
MAX_LEVELS - LIMITADOR DE NIVELES MAXIMOS EN TOTAL DEL VIDEOJUEGO
screen_scroll - INICIADOR DE VARIABLE DE DESPLAZAMIENTO, ES DECIR, AQUELLA QUE VA A DAR LA PAUTA PARA QUE EL JUGADOR SE DESPLACE HACIA UNA DIRECCION
Y LA CAMARA LO SIGA
bg_scroll - lo mismo que lo anterior, pero para el fondo de los niveles
level - CONTADOR PARA INDICAR EN QUE NIVEL SE ENCUENTRA EL JUEGO ACTUALMENTE Y CON BASE EN ESO, GENERAR LA ESTRUCTURA DE LOS ESCENARIOS
bglvl - EXISTEN DOS TIPOS DE FONDO DE NIVELES, ESTA VARIABLE SELECCIONA ENTRE AMBOS DE ACUERDO AL NIVEL EN EL QUE EL JUGADOR SE ENCUENTRE
start_game - VARIABLE QUE INICIALIZA LA PARTIDA
start_intro - VARIABLE QUE INICIALIZA LA ANIMACION DE FADE-IN PARA EL INICIO DE CADA NIVEL
"""
GRAVITY = 0.5
SCROLL_THRESH = 300
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 17
MAX_LEVELS = 14
screen_scroll = 0
bg_scroll = 0
level = 8
bglvl = 2
start_game = False
start_intro = False

#NUMERO DE MUESTRAS MÁXIMAS A OBTENER, DONDE samples ES LA VARIABLE QUE INDICA CUANTO TIEMPO VA A FUNCIONAR EL JUEGO
samples = 46000
line = 0

#DEFINIR LAS ACCIONES DEL JUGADOR, CADA DESPLAZAMIENTO A LA IZQUIERDA, DERECHA, DISPARO, O LANZAMIENTO DE GRANADA FUNCIONA
#COMO BOOLEANO
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False


#ESTE SEGMENTO INICIALIZA CADA ARCHIVO DE AUDIO
# pygame.mixer.music.load('audio/binaural_beat1.mp3')
# pygame.mixer.music.set_volume(0.3)
# pygame.mixer.music.play(-1, 0.0, 5000)
pygame.mixer.music.load("audio/drifting_into_delta.mp3")
#AJUSTAR VOLUMEN
pygame.mixer.music.set_volume(0.4)
#AJUSTAR LA REPRODUCCION PARA QUE EL ARCHIVO DE AUDIO ANTERIORMENTE DECLARADO SE REPRODUZCA INDEFINIDAMENTE 
pygame.mixer.music.play(-1, 0.0, 5000)
jump_fx = pygame.mixer.Sound('audio/jump.wav')
jump_fx.set_volume(0.05)
shot_fx = pygame.mixer.Sound('audio/shooting.wav')
shot_fx.set_volume(0.05)
grenade_fx = pygame.mixer.Sound('audio/grenade.wav')
grenade_fx.set_volume(0.05)


#CARGAR ARCHIVOS DE IMAGENES DE INTERFAZ
#IMAGENES DE BOTON
start_img = pygame.image.load('img/buttons/play_btn.png').convert_alpha()
exit_img = pygame.image.load('img/buttons/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('img/buttons/restart_btn.png').convert_alpha()
# #background

#A TRAVES DE BUCLES FOR, ALMACENADOS EN ARRAYS, SE LLAMA A LOS ARCHIVOS DE TILES .PNG NECESARIOS PARA CONSTRUIR LOS ELEMENTOS
##GRAFICOS DEL FONDO DE VIDEOJUEGO
##COMO SE MENCIONO ANTES, DADO QUE EXISTEN DOS TIPOS DE FONDO O BACKGROUND DE ESCENARIO, SE DEBE HACER ESTE PROCESO PARA CARGAR
##CADA IMAGEN CORRESPONDIENTE
bg_imgs_1 = []
bg_imgs_2 = []
for i in range(1,6):
    bg_image1 = pygame.image.load(f"img/background/firstlvl{i}.png").convert_alpha()
    ##ESCALAR LOS ARCHIVOS AL TAMAÑO DE LA VENTANA
    bg_img1 = pygame.transform.scale(bg_image1, (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_imgs_1.append(bg_img1)

for i in range(1,4):
    bg_image2 = pygame.image.load(f"img/background/secondlvl{i}.png").convert_alpha()
    bg_img2 = pygame.transform.scale(bg_image2, (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_imgs_2.append(bg_img2)

#PARA OBTENER EL ANCHO NECESARIO, SE UTILIZA EL PRIMER ARCHIVO DEL BACKGROUND 1 Y SE LE OBTIENE SU ANCHO EN PIXELES
bg_width = bg_imgs_1[0].get_width()

#definir función de background
def draw_bg(bglvl):
    ##LLENAR CON EL FONDO LA SUPERFICIE TOTAL DE LA PANTALLA
    screen.fill(BG)
    for x in range(10):
        """
        DADO QUE LOS FONDOS O BACKGROUNDS UTILIZADOS SON VARIAS CAPAS DE IMAGENES, QUE GENERAN UN EFECTO OPTICO DE PROFUNDIDAD
        (PARA MAS INFO, BUSCAR EN INTERNET QUE ES "PARALLAX"), SE DEFINE UNA VARIABLE speed QUE LO QUE HACE ES DAR UN ATRASO O DELAY
        EN EL DESPLAZAMIENTO DE CADA CAPA, Y ASI LOGRAR EL EFECTO PARALLAX
        """
        speed = 0.2
        ##DEPENDIENDO CUAL BACKGROUND SEA ELEGIDO DE ACUERDO AL NIVEL, VA A IR INCLUYENDO LAS IMAGENES A TRAVES DE UN CICLO FOR
        #Y DESPLAZANDOLAS CON LA VELOCIDAD ANTES DEFINIDA, SUMANDOLE VELOCIDAD A CADA CAPA ADICIONAL
        # ES DECIR, SI LA CAPA 1 TIENE UN DESPLAZAMIENTO DE 0.2, LA SEGUNDA TIENE UN DESPLAZAMIENTO DE 0.3 Y ASI SUCESIVAMENTE,
        # PARA DAR EL EFECTO DE PARALLAX 
        if bglvl == 1:
            for i in bg_imgs_1:
                screen.blit(i, ((x * bg_width) - bg_scroll * speed, 0))
                speed += 0.1
        if bglvl == 2:
            for i in bg_imgs_2:
                screen.blit(i, ((x * bg_width) - bg_scroll * speed, 0))
                speed += 0.1

# pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
# pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
# mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
# sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()

#GUARDAR LOS TILES EN UNA LISTA
img_list = []
#ES UN PROCEDIMIENTO PARECIDO AL DEL BACKGROUND, SOLO QUE PARA CARGAR CADA ARCHIVO DE TILES, ESCALARLO A LA PROPORCION DEFINIDA
# EN LA VENTANA
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/tiles/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

#CARGAR CADA ARCHIVO ESTATICO (DONDE LOS ARCHIVOS ESTATICOS SON LAS BALAS, LAS GRANADAS Y LAS CAJAS DE POWER-UPS)
#bullet
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
#grenade
grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()
#pick up boxes
health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load('img/icons/grenade_box.png').convert_alpha()
item_boxes = {
    'Health'    : health_box_img,
    'Ammo'      : ammo_box_img,
    'Grenade'   : grenade_box_img
}


#definir con rgb colores para ciertos elementos de la ventana
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)
CYAN = (0,200,200)

#definir el tipo de fuente y tamaño utilizado en el videojuego
font = pygame.font.SysFont('Futura', 30)

#funcion para graficar el texto en la pantalla
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

    # for x in range(5):
        # screen.blit(forrest_bg, (0,0))
        # screen.blit(forrest_sh, ((x * width) - bg_scroll * 0.5,0))
        # screen.blit(forrest_mg, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - forrest_mg.get_height() - 150))
        # screen.blit(f_fg, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - f_fg.get_height()))

# def draw_bg():
#     screen.fill(BG)
#     width = sky_img.get_width()
#     for x in range(5):
#         screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
#         screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
#         screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
#         screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))


#función para reiniciar cada nivel: el objetivo de esta funcion es vaciar los grupos de cada recurso del videojuego para 
# regenererarlos a su estado original (mismo que está dado por la definición del escenario en los archivos csv)
def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()

    #crear una lista de tiles vacia
    data = []
    ##este ciclo va ubicando las posiciones numericas de los tiles, de acuerdo con lo diseñado en cada escenario o nivel
    #y los agrega a la lista anterior
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data

"""
CLASE SOLDADO: GENERA LAS FUNCIONES NECESARIAS PARA LAS ACCIONES DEL JUGADOR Y DEL ENEMIGO
EN INIT, SE INICIALIZAN LAS VARIABLES COMO SIGUEN:
alive - para verificar si el jugador o ENEMIGO ESTA VIVO, ES DECIR, SI SU CONTADOR DE VIDA ES MAYOR A CERO
char_type - DEPENDIENDO DE SI ES JUGADOR O ENEMIGO, CARGA LOS RECURSOS GRAFICOS DE JUGADOR, MEJOR CONOCIDOS COMO SPRITE, DE ACUERDO AL VALOR DE ESTA VARIABLE
speed - VELOCIDAD A LA QUE EL OBJETO JUGADOR O ENEMIGO SE DESPLAZA
ammo - CANTIDAD NUMERICA DE MUNICIONES
start_ammo - CUANTA MUNICION EN NUMEROS ENTEROS TIENE EL JUGADOR AL INICIAR EL NIVEL
shoot_cooldown - AL DISPARAR UNA VEZ, CUANTO TIEMPO HAY QUE ESPERAR ANTES DE HACER EL SIGUIENTE DISPARO
grenades - CUANTAS GRANADAS TIENE EL JUGADOR
health - CUANTO ES EL INDICADOR DE "SALUD" DEL JUGADOR
max_health - CANTIDAD MAXIMA DE SALUD PARA EL JUGADOR
direction - EN QUÉ DIRECCION SE ESTÁ MOVIENDO, SI ES POSITIVO EL NUMERO, ES HACIA LA DERECHA (AVANZA), DE LO CONTRARIO, ES HACIA LA IZQUIERDA (RETROCEDE)
vel_y - QUE TAN RAPIDO ASCIENDE EL JUGADOR CUANDO SALTA
jump - VARIABLE BOOLEANA QUE INDICA SI EL JUGADOR HA SALTADO
in_air - VARIABLE QUE INDICA SI EL JUGADOR SIGUE EN EL AIRE DESPUES DE SALTAR
flip - VARIABLE QUE INDICA SI EL JUGADOR SE HA DADO LA VUELTA, PARA PODER GIRAR EL SPRITE, HACIENDO EL EFECTO DE QUE EL JUGADOR GRAFICAMENTE MIRA HACIA EL LADO OPUESTO
animation_list - LOS SPRITES DE JUGADOR Y ENEMIGO SE COMPONEN DE VARIAS IMAGENES Y VARIOS TIPOS DE ANIMACION (QUIETO, SALTO, DISPARO, MUERTE), ESTA VARIABLE SELECCIONA QUE TIPOS DE ANIMACIONES HAY EN CADA OBJETO JUGADOR O ENEMIGO
frame_index - DE ACUERDO CON LA ANIMACION SELECCIONADA, INDICA EN QUE CUADRO DE DICHA ANIMACION SE ENCUENTRA EN ESE MOMENTO
action - INDICA QUE ESTA HACIENDO EL JUGADOR
update_time - VARIABLE PARA INDICAR EL TIEMPO DE ACTUALIZACION CUANDO EL JUGADOR HA REALIZADO UNA ACCION DIFERENTE A LA ANTERIOR (I.E. DE AVANZAR A SALTAR)
VARIABLES ESPECIFICAS DE LA I.A. DEL ENEMIGO:
move_counter - CUANTAS VECES EL ELEMENTO ENEMIGO SE MUEVE O ACTUA
vision - RANGO DE VISION EN EL CUAL EL ELEMENTO ENEMIGO DETECTA CUANDO EL JUGADOR ESTA CERCA PARA COMENZAR A DISPARARLE
idling - VARIABLE BOOLEANA QUE INDICA SI EL ELEMENTO ENEMIGO ESTÁ QUIETO O MOVIENDOSE/ATACANDO
idling_counter - CUANTO TIEMPO PASA ENTRE EL CAMBIO DE ACCION DEL ELEMENTO ENEMIGO
"""
class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.grenades = grenades
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        #ai specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0
        
        #CARGAR TODOS LOS TIPOS DE ANIMACION DE LOS SPRITES
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            #RESETEAR UNA LISTA TEMPORAL DE IMAGENES DE ANIMACION
            temp_list = []
            #CUENTA EL NUMERO DE FRAMES INCLUIDO EN CADA TIPO DE ANIMACION
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}')) - 1
            for i in range(num_of_frames):
                #CARGA ESOS FRAMES, Y LOS REESCALA AL TAMAÑO DE CUADRICULA/ESCENARIO
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        #INDICA QUE CUADRO DEL SPRITE DEBE MOSTRARSE EN TIEMPO REAL
        self.image = self.animation_list[self.action][self.frame_index]
        #SE CREA UN RECTANGULO INVISIBLE EN CADA ELEMENTO (JUGADOR O ENEMIGO) PARA CONOCER SU REGION DE DAÑO AL ATACAR O SER ATACADO
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    #FUNCION PARA ACTUALIZAR ANIMACION, CHECANDO QUE EL ELEMENTO JUGADOR O ENEMIGO ESTE VIVO DE ACUERDO A SU BARRA DE SALUD
    def update(self):
        self.update_animation()
        self.check_alive()
        #ACTUALIZAR EL COOLDOWN DE DISPAROS
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    #FUNCION PARA MOVIMIENTO
    def move(self, moving_left, moving_right):
        #RESETEAR VARIABLES DE MOVIMIENTO
        screen_scroll = 0
        dx = 0
        dy = 0

        #ASIGNAR VARIABLES DE MOVIMIENTO SI EXISTE A LA IZQUIERDA O DERECHA
        if moving_left:
            #SI ES A LA IZQUIERDA LA VELOCIDAD DE DESPLAZAMIENTO SE VUELVE NEGATIVA
            dx = -self.speed
            #SE VOLTEAN LOS SPRITES PARA INDICAR QUE EL ELEMENTO HA CAMBIADO DE DIRECCION
            self.flip = True
            self.direction = -1
        if moving_right:
            #LO RESPECTIVO PARA LA DERECHA
            dx = self.speed
            self.flip = False
            self.direction = 1

        #SALTO
        #SI EL JUGADOR ESTA SALTANDO Y LA VARIABLE EN EL AIRE ES FALSE (PORQUE EL JUGADOR YA ALCANZO LA MAXIMA ALTURA DE SALTO POSIBLE)
        if self.jump == True and self.in_air == False:
            #LA VELOCIDAD VERTICAL SE VUELVE NEGATIVA PORQUE ASI DESCIENDE EL SPRITE
            self.vel_y = -13
            #SE INVIERTEN LAS VARIABLES DE SALTO Y EN AIRE
            self.jump = False
            self.in_air = True

        #APLICAR GRAVEDAD CUANDO SALTA, ES INCREMENTAL EL VALOR POR LO QUE LLEGA UN PUNTO 
        # EN QUE LA VELOCIDAD VERTICAL SE REINICIA AL LLEGAR A LA ALTURA MAXIMA DE SALTO
        self.vel_y += GRAVITY
        ##REINICIAR VELOCIDAD PARA COMENZAR DESCENSO
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #VERIFICAR COLISIONES CON ELEMENTOS DE TERRENO
        for tile in world.obstacle_list:
            #VERIFICAR COLISIONES EN EL EJE X
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                #SI LA I.A. CHOCA CONTRA UNA PARED, HACER QUE SE DE LA VUELTA
                if self.char_type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0
            #CHECAR COLISION EN EL EJE Y
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #VERIFICAR SI HAY SUELO POR DEBAJO DEL JUGADOR CUANDO ESTA ATERRIZANDO EN TIERRA
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #VERIFICAR SI ESTA POR ENCIMA DEL SUELO, POR EJEMPLO AL COMENZAR A SALTAR
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom


        #VERIFICAR SI EL JUGADOR COLISIONÓ CON EL ELEMENTO TILE AGUA, Y DE SER ASI VACIAR BARRA DE SALUD
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0

        #VERIFICAR SI EL JUGADOR COMPLETÓ EL NIVEL AL COLISIONAR CON EL TILE COPA DE FINALIZACION
        #VOLVIENDO TRUE LA VARIABLE LEVEL COMPLETE PARA DAR INICIO AL SIGUIENTE NIVEL
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True

        #VERIFICAR SI SE CAYÓ DEL MAPA TRAZADO DE TILES, Y DE SER ASI VACIAR BARRA DE SALUD
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0


        #VERIFICAR SI EL JUGADOR SE SALIÓ DE LOS LIMITES LATERALES DE LA PANTALLA
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        #ACTUALIZAR LA POSICION DEL RECTANGULO QUE RODEA AL JUGADOR
        self.rect.x += dx
        self.rect.y += dy

        #ACTUALIZAR EL DESPLAZAMIENTO LATERAL DE ACUERDO CON LA POSICION DEL JUGADOR
        if self.char_type == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH)\
                or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete


    #FUNCION QUE PERMITE DISPARAR
    def shoot(self):
        #SI NO HAY DISPARO ANTERIOR Y LA MUNICION ES MAYOR A CERO
        if self.shoot_cooldown == 0 and self.ammo > 0:
            #SE DA UN COOLDOWN PARA PERMITIR UNA FLUIDEZ DE DISPARO APROPIADA
            self.shoot_cooldown = 8
            #LA POSICION DE LA BALA, QUE VA AVANZANDO, SE ACTUALIZA CON EL DESPLAZAMIENTO EN EL EJE X
            bullet = Bullet(self.rect.centerx + (0.7 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            #SI HAY MULTIPLES DISPAROS, SE AÑADEN LOS RECURSOS GRAFICOS AL RENDERING EN PANTALLA
            bullet_group.add(bullet)
            #REDUCIR MUNICION POR CADA DISPARO Y REPRODUCIR SONIDO DE DISPARO
            self.ammo -= 1
            shot_fx.play()

    #FUNCION PARA LA INTELIGENCIA ARTIFICIAL DEL ELEMENTO ENEMIGO
    def ai(self):
        #SI EL ENEMIGO ESTA VIVO Y EL JUGADOR ESTA VIVO
        if self.alive and player.alive:
            #DE ACUERDO A UN NUMERO ALEATORIO, EL MOVIMIENTO AUTOMATICO DEL ENEMIGO SE DISPARA UNICAMENTE SI ESTE NUMERO ES 1
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)#0: idle
                self.idling = True
                #SE ACTUALIZA EL CONTADOR PARA REAPLICAR ESTA RUTINA CON OTRO NUMERO ALEATORIO
                self.idling_counter = 50
            #VERIFICAR SI LA I.A. YA DETECTÓ AL JUGADOR EN SU RANGO DE VISION PARA MIRARLO, ESTO SE HACE AL DETECTAR EL RECTANGULO
            #INVISIBLE QUE RODEA AL JUGADOR
            if self.vision.colliderect(player.rect):
                #DEJAR DE CORRER Y MIRAR HACIA EL JUGADOR
                self.update_action(0)#0: idle
                #DISPARAR
                self.shoot()
            else:
                #DE LO CONTRARIO, LA I.A. CAMBIA DE DIRECCION 
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    #PARA VIRAR DE DIRECCION AL ENEMIGO Y SU SPRITE, SE NIEGA LA VARIABLE DE MOVIMIENTO HACIA LA DERECHA
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)#1: CORRER
                    self.move_counter += 1
                    #ACTUALIZAR EL PERIMETRO DE VISION DE LA I.A MIENTRAS SE MUEVE
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    #DETECTAR SI YA SE PASÓ DEL LIMITE DIBUJADO DE LOS TILES
                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

        #DESPLAZARSE EN CONJUNTO CON EL SCROLL DE LA PANTALLA, PARA EVITAR QUE EL MOVIMIENTO INDEPENDIENTE DEL ENEMIGO OBSTRUYA
        #EL DESPLAZAMIENTO EN RELACION A LA POSICION DEL JUGADOR
        self.rect.x += screen_scroll


    def update_animation(self):
        #ACTUALIZAR LA ANIMACION
        ANIMATION_COOLDOWN = 22
        #ACTUALIZAR IMAGEN DE LOS SPRITES DE ACUERDO AL CUADRO ACTUAL
        self.image = self.animation_list[self.action][self.frame_index]
        #VERIFICAR SI HA PASADO TIEMPO SUFICIENTE DESDE LA ULTIMA ACTUALIZACION
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #SI LA ANIMACION YA ACABÓ SUS FRAMES INCLUIDOS, REINICIAR LA ANIMACION
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0



    def update_action(self, new_action):
        #VERIFICAR SI LA NUEVA ACCION ES DIFERENTE A LA ACCION ANTERIOR O ACTUAL
        if new_action != self.action:
            self.action = new_action
            #ACTUALIZAR LOS AJUSTES DE LA ANIMACION EN CONFORMIDAD CON EL FRAME ACTUAL
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


# VERIFICAR SI EL JUGADOR SIGUE VIVO
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3) #MUERTE

#DIBUJAR O RENDERIZAR LOS ELEMENTOS JUGADOR Y ENEMIGO EN PANTALLA
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


#CLASE MUNDO: PARA GENERAR LOS RECURSOS GRAFICOS DE CADA NIVEL
class World():
    def __init__(self):
        #LISTA DE OBSTACULOS
        self.obstacle_list = []

#PROCESAR LOS DATOS DE LOS NIVELES, CREADOS CON LA APLICACION TILED:
#TILED CREA NIVELES AL ASIGNARLE A LOS TILES UNA ENTIDAD NUMERICA, ENTONCES, DE ACUERDO A UNA DELIMITACION DE CUADRICULAS
#LOS TILES SE GENERAN AQUI DONDE ESTÉ LA POSICION DE SU ENTIDAD NUMERICA. ES DECIR, SI EL TILE DE AGUA TIENE UNA ENTIDAD NUMERICA
#12, EL TILE SE RENDERIZARÁ EN DONDE HAYAN NUMEROS 12 EN EL ARCHIVO CSV
    def process_data(self, data):
        self.level_length = len(data[0])
        #ITERAR EN CADA ENTIDAD NUMERICA DE LOS TILES
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    #AJUSTAR LOS TILES AL TAMAÑO DE CADA PORCION DE LA CUADRICULA DE ESCENARIO
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    #AQUI SE GENERAN LOS TILES DE TERRENO
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                        #AQUI LOS TILES DE AGUA
                    elif tile == 9:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                        #AQUI LOS TILES DE DECORACION
                    elif tile == 10:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                        #AQUI SE GENERA AL ELEMENTO JUGADOR
                    elif tile == 11:
                        player = Soldier('player', x * TILE_SIZE, y * TILE_SIZE, 1.65, 5, 0, 0)
                        health_bar = HealthBar(10, 10, player.health, player.health)
                        #AQUI SE GENERA AL ELEMENTO ENEMIGO
                    elif tile == 12:
                        enemy = Soldier('enemy', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 20, 0)
                        enemy_group.add(enemy)
                        #AQUI SE GENERA EL POWER-UP DE MUNICION
                    elif tile == 13:
                        item_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                        #AQUI SE GENERA EL POWER-UP DE GRANADA
                    elif tile == 14:
                        item_box = ItemBox('Grenade', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                        #AQUI SE GENERA EL POWER-UP DE SALUD
                    elif tile == 15:
                        item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                        #AQUI SE GENERA EL ELEMENTO DE FINALIZACION DE NIVEL
                    elif tile == 16:
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)

        return player, health_bar

#SE RENDERIZAN LOS ELEMENTOS GRAFICOS ANTERIORES
    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])

"""
A PARTIR DE AQUI, SE UBICAN POR SEPARADO LOS ELEMENTOS DEL ESCENARIO. A DIFERENCIA DE LA RUTINA ANTERIOR, DONDE SOLO SE IDENTIFICAN
Y GENERAN LOS ELEMENTOS EN LA CUADRICULA NUMERICA OTORGADA POR EL ARCHIVO CSV, AQUI ES DONDE OCURRE LA IMPLEMENTACION GRAFICA DE LO ANTERIOR
"""
#PARA DECORACION
class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll

#PARA AGUA
class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll

#PARA ELEMENTO DE FINAL DE NIVEL
class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


#PARA LAS CAJAS DE POWER-UPS
class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

#FUNCION PARA DESAPARECER LOS POWER-UPS EN CASO DE QUE EL JUGADOR ACCEDA A ELLOS
    def update(self):
        #DESPLAZAR DICHOS ELEMENTOS EN EL MAPA CON EL MOVIMIENTO DEL JUGADOR
        self.rect.x += screen_scroll
        #VERIFICAR SI EL JUGADOR HA TOMADO EL POWER-UP MEDIANTE LA COLISION DE SU RECTANGULO
        if pygame.sprite.collide_rect(self, player):
            #VERIFICAR QUE TIPO DE POWER-UP ES
            #SI ES DE SALUD AUMENTAR 25 AL INDICADOR
            if self.item_type == 'Health':
                player.health += 25
                #SI EL JUGADOR YA TIENE LA MAXIMA SALUD, NO HACER NADA
                if player.health > player.max_health:
                    player.health = player.max_health
            #SI ES DE MUNICIÓN, AÑADIR 15
            elif self.item_type == 'Ammo':
                player.ammo += 15
            #SI ES DE GRANADA, AÑADIR 3
            elif self.item_type == 'Grenade':
                player.grenades += 3
            #BORRAR EL POWER-UP CORRESPONDIENTE
            self.kill()


#CLASE PARA DIBUJAR LA BARRA DE SALUD
class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        #ACTUALIZAR CON LA SALUD ACTUAL
        self.health = health
        #CALCULAR LA PROPORCION DE SALUD, CON EL FIN DE DIBUJAR LA BARRA VERDE (SALUD RESTANTE) POR ENCIMA DE LA ROJA (SALUD PERDIDA)
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))


#PARA DIBUJAR EL OBJETO BALA
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        #A QUE VELOCIDAD IRÁ LA BALA
        self.speed = 20
        #QUE IMAGEN UTILIZA
        self.image = bullet_img
        #RECTANGULO INVISIBLE QUE DETECTA COLISION CON JUGADOR Y ENEMIGO
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        #HACIA QUE DIRECCION SE ESTA DISPARANDO
        self.direction = direction

    def update(self):
        #MOVER LA BALA
        self.rect.x += (self.direction * self.speed) + screen_scroll
        #SI LA BALA SALIO DE LOS LIMITES LATERALES DE LA PANTALLA, ELIMINARLA 
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        #SI LA BALA COLISIONÓ CON UN TILE DE TERRENO DE ESCENARIO, ELIMINARLA
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        #SI LA BALA COLISIONÓ CON EL ELEMENTO JUGADOR, BAJARLE 2.5 DE SALUD POR CADA BAJA Y LUEGO ELIMINAR LA BALA
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 2.5
                self.kill()
        #SI LA BALA COLISIONÓ CON EL ENEMIGO, BAJARLE 25 DE SALUD Y ELIMINAR LA BALA
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    self.kill()


#CLASE PARA GRANADA Y EFECTO DE DAÑO ASI COMO ANIMACIÓN
class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        #CUANTO TIEMPO ANTES DE QUE EXPLOTE
        self.timer = 100
        #VELOCIDAD DE DESPLAZAMIENTO EN EJE Y
        self.vel_y = -9
        #VELOCIDAD EN EJE X
        self.speed = 7
        #QUE IMAGEN SE UTILIZA PARA RENDERIZAR GRANADA
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        #HACIA QUE DIRECCION SE LANZA GRANADA
        self.direction = direction

    def update(self):
        #AUMENTAR LA VELOCIDAD DE ACUERDO CON LA GRAVEDAD, RECORDAR QUE LA VELOCIDAD EN EJE Y ES NEGATIVA
        #POR LO TANTO ESTÁ REGRESANDO SU VALOR A CERO
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y

        #VERIFICAR COLISION EN TILES DE ESCENARIO
        for tile in world.obstacle_list:
            #SI COLISIONA CON PAREDES FRENAR VELOCIDAD Y CAMBIAR DIRECCION
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
            #VERIFICAR COLISION EN EL EJE Y
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                #VERIFICAR SI HAY SUELO POR DEBAJO (CUANDO SE LANZA)
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #VERIFICAR SI ESTÁ ASCENDIENDO HASTA SU PUNTO MÁS ALTO
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom 


        #ACTUALIZAR POSICION DE LA GRANADA
        self.rect.x += dx + screen_scroll
        self.rect.y += dy

        #TIMER PARA EXPLOSION
        self.timer -= 1
        #SI EL TIMER LLEGA A CERO SE ELIMINA LA GRANADA, SE REPRODUCE SONIDO DE EXPLOSION, Y SE DIBUJA ANIMACION DE EXPLOSION
        if self.timer <= 0:
            self.kill()
            grenade_fx.play()
            explosion = Explosion(self.rect.x, self.rect.y, 0.5)
            explosion_group.add(explosion)
            #HACER DAÑO A CUALQUIERA QUE ESTÉ CERCA
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 50
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    enemy.health -= 50


#PARA DIBUJAR LA EXPLOSION DE LA GRANADA
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        #OBTENER LA ANIMACION DE EXPLOSION
        for num in range(1, 6):
            img = pygame.image.load(f'img/explosion/exp{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0


    def update(self):
        #ACTUALIZAR LA ANIMACION DE EXPLOSION
        self.rect.x += screen_scroll

        EXPLOSION_SPEED = 4
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            #SI LA ANIMACION YA TERMINÓ, ELIMINAR ANIMACION DEL RENDERING
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]


#FADE-IN O FADE-OUT PARA INICIO O FIN DE NIVEL
class ScreenFade():
    def __init__(self, direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0


    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:#FADE PARA TODA LA PANTALLA
            pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.colour, (0, SCREEN_HEIGHT // 2 +self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
        if self.direction == 2:#FADE DOWN PARA LA PANTALLA EN VERTICAL
            pygame.draw.rect(screen, self.colour, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True

        return fade_complete


#CREAR INSTANCIAS DE ANIMACION DE PANTALLA
intro_fade = ScreenFade(1, BLACK, 7)
death_fade = ScreenFade(2, CYAN, 7)


# #create buttons
# start_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 100, start_img, 8)
# exit_button = button.Button(SCREEN_WIDTH // 1 - 300, SCREEN_HEIGHT // 2 + 10, exit_img, 7)
# restart_button = button.Button(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 50, restart_img, 8)

#CREAR GRUPOS DE TILES/SPRITES PARA GENERARLOS POR CONJUNTOS EN CADA NIVEL, SEGUN SE REQUIERA
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()



#CREAR UNA LISTA DE TILES DE NIVEL VACIA
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
#CARGAR LOS DATOS DE CADA NIVEL DISEÑADO EN TILED (ARCHIVO CSV)
with open(f'level_{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
world = World()
player, health_bar = world.process_data(world_data)

#Z ES UNA BANDERA
z = 0
#RUN ES LA BANDERA PARA INICIAR LA RENDERIZACION DE LA VENTANA
run = True
#INICIALIZAR LA INTRO DE INICIO
start_intro = True
#MIENTRAS RUN SEA TRUE
while run:

    #COMENZAR A CORRER LA TASA DE ACTUALIZACION DE FRAMES
    clock.tick(FPS)
    
    #iniciar temporizador aparte

    start_game = True
    #ACTUALIZAR EL BACKGROUND
    draw_bg(bglvl)
    #RENDERIZAR EL MAPA
    world.draw()
    #MOSTRAR LA BARRA DE SALUD DEL JUGADOR
    health_bar.draw(player.health)
    #MOSTRAR LA MUNICION
    draw_text('AMMO: ', font, WHITE, 10, 35)
    for x in range(player.ammo):
        screen.blit(bullet_img, (90 + (x * 10), 35))
    # #show grenades
    # draw_text('GRENADES: ', font, WHITE, 10, 60)
    # for x in range(player.grenades):
    #     screen.blit(grenade_img, (135 + (x * 15), 60))

    #ACTUALIZAR AL JUGADOR Y RENDERIZARLO
    player.update()
    player.draw()

    #LO MISMO PARA EL ENEMIGO
    for enemy in enemy_group:
        enemy.ai()
        enemy.update()
        enemy.draw()

    #ACTUALIZAR Y RENDERIZAR CADA GRUPO DE TILE/SPRITE
    bullet_group.update()
    grenade_group.update()
    explosion_group.update()
    item_box_group.update()
    decoration_group.update()
    water_group.update()
    exit_group.update()
    bullet_group.draw(screen)
    grenade_group.draw(screen)
    explosion_group.draw(screen)
    item_box_group.draw(screen)
    decoration_group.draw(screen)
    water_group.draw(screen)
    exit_group.draw(screen)

    #MOSTRAR INTRO SI INICIA CADA NIVEL
    if start_intro == True:
        if intro_fade.fade():
            start_intro = False
            intro_fade.fade_counter = 0


    #ACTUALIZAR ACCIONES DEL JUGADOR
    if player.alive:
        #DISPARAR
        if shoot:
            player.shoot()
        #LANZAR GRANADAS
        elif grenade and grenade_thrown == False and player.grenades > 0:
            grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),\
                        player.rect.top, player.direction)
            grenade_group.add(grenade)
            #REDUCIR NUMERO DE GRANADAS SI SE LANZA UNA
            player.grenades -= 1
            grenade_thrown = True
        if player.in_air:
            player.update_action(2)#2: SALTO
        elif moving_left or moving_right:
            player.update_action(1)#1: CORRER
        else:
            player.update_action(0)#0: QUIETO
        screen_scroll, level_complete = player.move(moving_left, moving_right)
        bg_scroll -= screen_scroll
        #VERIFICAR SI EL JUGADOR HA COMPLETADO EL NIVEL
        #DE SER ASI, AVANZAR AL SIGUIENTE
        if level_complete:
            start_intro = True
            level += 1
            bg_scroll = 0
            world_data = reset_level()
            #SI EL NIVEL ES MAYOR O IGUAL A 8, CAMBIAR DE BACKGROUND
            if level >= 8:
                bglvl = 1
            else:
                pass
            #SI EL JUGADOR NO HA ALCANZADO EL ULTIMO NIVEL, CARGAR LOS ARCHIVOS CSV DE LOS NIVELES PARA RENDERIZARLOS
            if level <= MAX_LEVELS:
                #CARGAR DATOS DE JUEGO Y CREAR EL NIVEL EN PANTALLA
                with open(f'level_{level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World()
                player, health_bar = world.process_data(world_data)
            #SI YA ALCANZÓ EL MAXIMO DE NIVELES, REINICIAR DESDE EL NIVEL 1 DE MANERA ININTERRUMPIDA
            else:
                level = 1
                bglvl = 2
                #CARGAR DATOS DE JUEGO Y CREAR EL NIVEL EN PANTALLA
                with open(f'level_{level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World()
                player, health_bar = world.process_data(world_data)
    #SI EL JUGADOR PIERDE O "MUERE"        
    else:
        #DEJA DE AVANZAR EL DESPLAZAMIENTO EN PANTALLA
        screen_scroll = 0
        #INICIA EL FADE-OUT DE FIN DE NIVEL Y LUEGO EL DE FADE-IN DE INICIO DE NIVEL
        if death_fade.fade():
            death_fade.fade_counter = 0
            start_intro = True
            bg_scroll = 0
            world_data = reset_level()
            #CARGAR DATOS DE JUEGO Y CREAR EL NIVEL EN PANTALLA
            with open(f'level_{level}_data.csv', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        world_data[x][y] = int(tile)
            world = World()
            player, health_bar = world.process_data(world_data)

      #aqui va el read data del serial
    data = ser.readline().decode('utf-8')
    # print(data)
    """
    EL ARDUINO ENVIA LOS DATOS DE CADA ELEMENTO ANALOGICO SEPARADOS POR COMAS, LO QUE HACE ESTA SECCION DE CODIGO
    ES SEPARAR CADA DIGITO, TOMANDO COMO REFERENCIA DICHAS COMAS, Y ASIGNARLAS A UNA VARIABLE QUE INDIQUE UNA ACCION EN
    EL JUEGO
    """
    if data:
        izquierda = data.split(",")[0]
        derecha = data.split(",")[1]
        salto = data.split(",")[2]
        disparo = data.split(",")[3]
        granada = data.split(",")[4]
    


    for event in pygame.event.get():
        #SI SE CIERRA LA VENTANA FINALIZA EL JUEGO
        if event.type == pygame.QUIT:
            run = False
            
        # #keyboard presses
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_a:
        #         moving_left = True
        #     if event.key == pygame.K_d:
        #         moving_right = True
        #     if event.key == pygame.K_SPACE:
        #         shoot = True
                
        #     if event.key == pygame.K_q:
        #         grenade = True
        #     if event.key == pygame.K_w and player.alive:
        #         player.jump = True
        #         jump_fx.play()
        #     if event.key == pygame.K_ESCAPE:
        #         run = False


        # #keyboard button released
        # if event.type == pygame.KEYUP:
        #     if event.key == pygame.K_a:
        #         moving_left = False
        #     if event.key == pygame.K_d:
        #         moving_right = False
        #     if event.key == pygame.K_SPACE:
        #         shoot = False
        #     if event.key == pygame.K_q:
        #         grenade = False
        #         grenade_thrown = False
    
    """
    ESTE SEGMENTO DE CODIGO LEE CADA VARIABLE ANTERIOR DEFINIDA POR LA PARTE DE LECTURA DE DATOS DEL ARDUINO, Y LE ASIGNA UNA ACCION
    EN EL JUEGO
    """
    if salto == "w" and player.alive:
        player.jump = True
        jump_fx.play()
    else:
        player.jump = False
        jump_fx.stop()
            
    if izquierda == "a":
        moving_left = True
    
    elif izquierda == "0":
        moving_left = False
    
    if derecha == "d":
        moving_right = True
        
    elif derecha == "0":
        moving_right = False
        
    if disparo == "e":
        shoot = True
    
    elif disparo == "0":
        shoot = False
    
    if granada == "q":
        grenade = True
    
    elif granada == "0":
        grenade = False
        grenade_thrown = False

    #ACTUALIZA LA PANTALLA POR CADA FRAME (60FPS)
    pygame.display.update()
    """
    ESTE SEGMENTO DE CODIGO CREA UN ARCHIVO CSV, CON LOS DATOS SIGUIENTES POR COLUMNAS:
    TIMER - TIEMPO CRONOMETRADO
    DATOS - LOS DATOS ENVIADOS POR EL ARDUINO SE SEPARAN, Y SE ALMACENAN EN COLUMNAS INDEPENDIENTES 
    ESTO LO HACE CADA QUE OBTIENE UNA MEDICION DEL ARDUINO A TRAVÉS DE LA COMUNICACION EN EL PUERTO SERIAL
    """
    file = open(filename,"a")
    current_time = timer()
    timex = str(timedelta(seconds=current_time-start_time))
    dataf = timex + "," + str(data)
    file.write(dataf)
    line = line+1
    
    #SI SE LLEGÓ AL MAXIMO DE SAMPLES DEFINIDO AL INICIO (46000, QUE EQUIVALE A 15 MINUTOS DE JUEGO APROXIMADAMENTE)
    #GUARDA Y CIERRA EL ARCHIVO, ASI COMO TERMINA EL PROCESO DEL JUEGO.
    ser.flushInput()
    if line >= samples:
        file.close()
        ser.close()
pygame.mixer.music.stop()
pygame.quit()