import pygame
import json
from datetime import datetime
from Constantes import *
from Funciones import *

pygame.init()

# Elementos de la pantalla de fin de partida
cuadro_nombre = crear_elemento_juego("textura_pregunta.jpg", CUADRO_TEXTO[0], CUADRO_TEXTO[1], (ANCHO-CUADRO_TEXTO[0])//2, 300)
boton_guardar = crear_elemento_juego("textura_menu.jpg", ANCHO_BOTON + 50, ALTO_BOTON, (ANCHO-(ANCHO_BOTON + 50))//2, 400)

def validar_nombre(nombre: str) -> bool:
    """Valida que el nombre tenga entre 3 y 10 caracteres y solo contenga letras y espacios"""
    if len(nombre) < 3 or len(nombre) > 10:
        return False
    
    # Solo permite letras, espacios y algunos caracteres especiales
    caracteres_permitidos = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáéíóúÁÉÍÓÚñÑ "
    for caracter in nombre:
        if caracter not in caracteres_permitidos:
            return False
    
    return True

def guardar_partida(nombre: str, puntuacion: int) -> None:
    """Guarda la partida en el archivo partidas.json"""
    try:
        # Intentar cargar partidas existentes
        try:
            with open("partidas.json", "r", encoding="utf-8") as archivo:
                partidas = json.load(archivo)
        except FileNotFoundError:
            partidas = []
        
        # Crear nueva partida
        nueva_partida = {
            "nombre": nombre,
            "puntuacion": puntuacion,
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        
        partidas.append(nueva_partida)
        
        # Guardar en archivo
        with open("partidas.json", "w", encoding="utf-8") as archivo:
            json.dump(partidas, archivo, indent=4, ensure_ascii=False)
            
    except Exception as e:
        print(f"Error al guardar partida: {e}")

def mostrar_terminado(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict) -> str:
    retorno = "terminado"
    nombre_ingresado = datos_juego.get("nombre", "")
    mensaje_error = datos_juego.get("mensaje_error", "")
    tiempo_error = datos_juego.get("tiempo_error", 0)
    
    # Verificar si el mensaje de error debe desaparecer
    if tiempo_error > 0:
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - tiempo_error > 3000:  # 3 segundos
            mensaje_error = ""
            datos_juego["mensaje_error"] = ""
            datos_juego["tiempo_error"] = 0
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE:
                nombre_ingresado = nombre_ingresado[:-1]
            elif evento.key == pygame.K_RETURN:
                if validar_nombre(nombre_ingresado):
                    guardar_partida(nombre_ingresado, datos_juego["puntuacion"])
                    datos_juego["nombre"] = ""  # Limpiar el nombre
                    retorno = "menu"
                else:
                    mensaje_error = "Nombre inválido (3-10 caracteres, solo letras)"
                    datos_juego["mensaje_error"] = mensaje_error
                    datos_juego["tiempo_error"] = pygame.time.get_ticks()
            elif evento.unicode.isprintable() and len(nombre_ingresado) < 10:
                nombre_ingresado += evento.unicode
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton_guardar["rectangulo"].collidepoint(evento.pos):
                    if validar_nombre(nombre_ingresado):
                        guardar_partida(nombre_ingresado, datos_juego["puntuacion"])
                        datos_juego["nombre"] = ""  # Limpiar el nombre
                        retorno = "menu"
                    else:
                        mensaje_error = "Nombre inválido (3-10 caracteres, solo letras)"
                        datos_juego["mensaje_error"] = mensaje_error
                        datos_juego["tiempo_error"] = pygame.time.get_ticks()
    
    # Actualizar el nombre en datos_juego
    datos_juego["nombre"] = nombre_ingresado
    
    # Dibujar pantalla
    try:
        fondo_terminado = pygame.transform.scale(pygame.image.load("fondo-terminado.jpg"), PANTALLA)
        pantalla.blit(fondo_terminado, (0, 0))
    except:
        pantalla.fill(COLOR_BLANCO)
    
    # Mostrar puntuación final
    mostrar_texto(pantalla, f"¡FIN DE PARTIDA!", (ANCHO//2 - 120, 100), FUENTE_PREGUNTA, COLOR_NEGRO)
    mostrar_texto(pantalla, f"Puntuación final: {datos_juego['puntuacion']}", (ANCHO//2 - 120, 180), FUENTE_TEXTO, COLOR_NEGRO)
    mostrar_texto(pantalla, "Ingresa tu nombre:", (ANCHO//2 - 80, 250), FUENTE_TEXTO, COLOR_NEGRO)
    
    # Campo de nombre (rectángulo blanco con bordes negros)
    pygame.draw.rect(pantalla, COLOR_BLANCO, cuadro_nombre["rectangulo"])
    pygame.draw.rect(pantalla, COLOR_NEGRO, cuadro_nombre["rectangulo"], 2)  # Borde negro de 2px
    mostrar_texto(pantalla, nombre_ingresado, (cuadro_nombre["rectangulo"].x + 10, cuadro_nombre["rectangulo"].y + 10), FUENTE_TEXTO, COLOR_NEGRO)
    
    # Botón guardar
    pantalla.blit(boton_guardar["superficie"], boton_guardar["rectangulo"])
    mostrar_texto(boton_guardar["superficie"], "GUARDAR", (boton_guardar["rectangulo"].width//2 - 40, 10), FUENTE_TEXTO, COLOR_NEGRO)
    
    # Mensaje de error
    if mensaje_error:
        mostrar_texto(pantalla, mensaje_error, (ANCHO//2 - 200, 500), FUENTE_TEXTO, COLOR_ROJO)
    
    return retorno
