import pygame
import json
from Constantes import *
from Funciones import *

pygame.init()

boton_volver = crear_elemento_juego("textura_menu.jpg",TAMAÑO_BOTON_VOLVER[0],TAMAÑO_BOTON_VOLVER[1],(ANCHO-TAMAÑO_BOTON_VOLVER[0])//2,600)

def cargar_partidas() -> list:
    """Carga las partidas desde partidas.json y las ordena por puntuación"""
    try:
        with open("partidas.json", "r", encoding="utf-8") as archivo:
            partidas = json.load(archivo)
        # Ordenar por puntuación (de mayor a menor)
        partidas.sort(key=lambda x: x["puntuacion"], reverse=True)
        return partidas
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error al cargar partidas: {e}")
        return []

def mostrar_rankings(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict) -> str:
    retorno = "rankings"
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton_volver["rectangulo"].collidepoint(evento.pos):
                    retorno = "menu"
    
    # Dibujar pantalla
    try:
        fondo_ranking = pygame.transform.scale(pygame.image.load("fondo-ranking.jpg"), PANTALLA)
        pantalla.blit(fondo_ranking, (0, 0))
    except:
        pantalla.fill(COLOR_BLANCO)
    
    # Título
    mostrar_texto(pantalla, "TOP 10 - MEJORES PUNTUACIONES", (ANCHO//2 - 200, 50), FUENTE_PREGUNTA, COLOR_NEGRO)
    
    # Encabezados de columnas
    mostrar_texto(pantalla, "POS", (50, 120), FUENTE_TEXTO, COLOR_NEGRO)
    mostrar_texto(pantalla, "NOMBRE", (120, 120), FUENTE_TEXTO, COLOR_NEGRO)
    mostrar_texto(pantalla, "PUNTUACIÓN", (280, 120), FUENTE_TEXTO, COLOR_NEGRO)
    mostrar_texto(pantalla, "FECHA", (420, 120), FUENTE_TEXTO, COLOR_NEGRO)
    
    # Cargar y mostrar rankings
    partidas = cargar_partidas()
    
    if not partidas:
        mostrar_texto(pantalla, "No hay partidas registradas", (ANCHO//2 - 150, 300), FUENTE_TEXTO, COLOR_NEGRO)
    else:
        # Mostrar top 10
        for i in range(min(10, len(partidas))):
            partida = partidas[i]
            y_pos = 160 + (i * 35)
            
            # Número de posición
            pos_texto = f"{i+1}."
            mostrar_texto(pantalla, pos_texto, (50, y_pos), FUENTE_TEXTO, COLOR_NEGRO)
            
            # Nombre del jugador
            nombre_texto = partida["nombre"]
            mostrar_texto(pantalla, nombre_texto, (120, y_pos), FUENTE_TEXTO, COLOR_NEGRO)
            
            # Puntuación
            puntuacion_texto = f"{partida['puntuacion']} pts"
            mostrar_texto(pantalla, puntuacion_texto, (280, y_pos), FUENTE_TEXTO, COLOR_NEGRO)
            
            # Fecha
            fecha_texto = partida["fecha"]
            mostrar_texto(pantalla, fecha_texto, (420, y_pos), FUENTE_TEXTO, COLOR_NEGRO)
    
    # Botón volver
    pantalla.blit(boton_volver["superficie"],boton_volver["rectangulo"])
    mostrar_texto(pantalla, "VOLVER", (boton_volver["rectangulo"].x + 5, boton_volver["rectangulo"].y + 10), FUENTE_TEXTO, COLOR_NEGRO)
    
    return retorno
    