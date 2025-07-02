import pygame 
from Constantes import *
from Menu import *
from Juego import *
from Configuracion import *
from Rankings import *
from Terminado import *

pygame.init()
pygame.display.set_caption("PREGUNTADOS")
icono = pygame.image.load("icono.png")
pygame.display.set_icon(icono)
pantalla = pygame.display.set_mode(PANTALLA)
datos_juego = {"puntuacion":0,"vidas":CANTIDAD_VIDAS,"nombre":"","tiempo_restante":30,"indice":0,"volumen_musica":100}
corriendo = True
reloj = pygame.time.Clock()
bandera_musica = False

ventana_actual = "menu"

while corriendo:
    reloj.tick(FPS)
    cola_eventos = pygame.event.get()
    
    if ventana_actual == "menu":
        if bandera_musica == True:
            pygame.mixer.music.stop()
            bandera_musica = False
        reiniciar_estadisticas(datos_juego)
        ventana_actual = mostrar_menu(pantalla,cola_eventos)
    elif ventana_actual == "juego":
        porcentaje_volumen = datos_juego["volumen_musica"] / 100
        
        if bandera_musica == False and datos_juego.get("musica_activa", True):
            pygame.mixer.music.load("musica.mp3")
            pygame.mixer.music.set_volume(porcentaje_volumen)
            pygame.mixer.music.play(-1)
            bandera_musica = True
        elif bandera_musica == True and not datos_juego.get("musica_activa", True):
            pygame.mixer.music.stop()
            bandera_musica = False
            
        ventana_actual = mostrar_juego(pantalla,cola_eventos,datos_juego)
    elif ventana_actual == "salir":
        corriendo = False
    elif ventana_actual == "ajustes":
        ventana_actual = mostrar_ajustes(pantalla,cola_eventos,datos_juego)
    elif ventana_actual == "rankings":
        ventana_actual = mostrar_rankings(pantalla,cola_eventos,datos_juego)
    elif ventana_actual == "terminado":
        ventana_actual = mostrar_terminado(pantalla,cola_eventos,datos_juego)

    print(ventana_actual)
    pygame.display.flip()

pygame.quit()
    
    