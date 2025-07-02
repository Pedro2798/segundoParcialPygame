import random
from Constantes import *
import pygame

def mostrar_texto(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, False, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

#GENERAL
def mezclar_lista(lista_preguntas:list) -> None:
    random.shuffle(lista_preguntas)

#GENERAL
def reiniciar_estadisticas(datos_juego:dict) -> None:
    datos_juego["puntuacion"] = 0
    datos_juego["vidas"] = CANTIDAD_VIDAS
    datos_juego["nombre"] = ""
    datos_juego["tiempo_restante"] = 30
    datos_juego["respuestas_correctas_seguidas"] = 0
    # Reiniciar comodines
    datos_juego["bomba_usado"] = False
    datos_juego["x2_usado"] = False
    datos_juego["doble_chance_usado"] = False
    datos_juego["pasar_usado"] = False
    datos_juego["multiplicador_x2"] = False
    datos_juego["doble_chance"] = False
    # Reiniciar mensajes de error
    datos_juego["mensaje_error"] = ""
    datos_juego["tiempo_error"] = 0
    # Configuración de música
    datos_juego["musica_activa"] = True
    # Modo de juego
    datos_juego["modo_tiempo"] = False

#GENERAL
def verificar_respuesta(datos_juego:dict,pregunta:dict,respuesta:int,lista_preguntas:list,indice_pregunta:int) -> bool:
    if respuesta == pregunta["respuesta_correcta"]:
        # Aplicar multiplicador x2 si está activo
        puntos_ganados = PUNTUACION_ACIERTO
        if datos_juego.get("multiplicador_x2", False):
            puntos_ganados *= 2
            datos_juego["multiplicador_x2"] = False  # Desactivar después de usar
            
        datos_juego["puntuacion"] += puntos_ganados
        datos_juego["respuestas_correctas_seguidas"] += 1
        
        # Si alcanza 5 respuestas correctas seguidas, gana una vida
        if datos_juego["respuestas_correctas_seguidas"] >= 5:
            datos_juego["vidas"] += 1
            datos_juego["respuestas_correctas_seguidas"] = 0  # Reinicia el contador
            
            # También gana segundos extra
            datos_juego["tiempo_restante"] += SEGUNDOS_EXTRA
        
        # Actualizar estadísticas de la pregunta
        from Preguntas import actualizar_estadistica_pregunta
        actualizar_estadistica_pregunta(lista_preguntas, indice_pregunta, True)
        
        retorno = True
    else:
        # Verificar si tiene doble chance
        if datos_juego.get("doble_chance", False):
            datos_juego["doble_chance"] = False  # Desactivar después de usar
            retorno = False  # No perder vida ni puntos, pero marcar como incorrecta
        else:
            datos_juego["vidas"] -= 1
            datos_juego["puntuacion"] -= PUNTUACION_ERROR
            datos_juego["respuestas_correctas_seguidas"] = 0  # Reinicia el contador al fallar
            retorno = False
        
        # Actualizar estadísticas de la pregunta (incorrecta)
        from Preguntas import actualizar_estadistica_pregunta
        actualizar_estadistica_pregunta(lista_preguntas, indice_pregunta, False)
        
    return retorno

def crear_elemento_juego(textura:str,ancho:int,alto:int,pos_x:int,pos_y:int) -> dict:
    elemento_juego = {}
    elemento_juego["superficie"] = pygame.transform.scale(pygame.image.load(textura),(ancho,alto))
    elemento_juego["rectangulo"] = elemento_juego["superficie"].get_rect()
    elemento_juego["rectangulo"].x = pos_x
    elemento_juego["rectangulo"].y = pos_y
    
    return elemento_juego

def limpiar_superficie(elemento_juego:dict,textura:str,ancho:int,alto:int) -> None:
    elemento_juego["superficie"] =  pygame.transform.scale(pygame.image.load(textura),(ancho,alto))
    
def obtener_respuesta_click(boton_respuesta_uno:dict,boton_respuesta_dos:dict,boton_respuesta_tres:dict,boton_respuesta_cuatro:dict,pos_click:tuple):
    lista_aux = [boton_respuesta_uno["rectangulo"],boton_respuesta_dos["rectangulo"],boton_respuesta_tres["rectangulo"],boton_respuesta_cuatro["rectangulo"]]
    respuesta = None
    
    for i in range(len(lista_aux)):
        if lista_aux[i].collidepoint(pos_click):
            respuesta = i + 1
    
    return respuesta

def cambiar_pregunta(lista_preguntas:list,indice:int,caja_pregunta:dict,boton_respuesta_uno:dict,boton_respuesta_dos:dict,boton_respuesta_tres:dict,boton_respuesta_cuatro:dict) -> dict:
    pregunta_actual = lista_preguntas[indice]
    limpiar_superficie(caja_pregunta,"textura_pregunta.jpg",ANCHO_PREGUNTA,ALTO_PREGUNTA)
    limpiar_superficie(boton_respuesta_uno,"textura_respuesta.jpg",ANCHO_BOTON,ALTO_BOTON)
    limpiar_superficie(boton_respuesta_dos,"textura_respuesta.jpg",ANCHO_BOTON,ALTO_BOTON)
    limpiar_superficie(boton_respuesta_tres,"textura_respuesta.jpg",ANCHO_BOTON,ALTO_BOTON)
    limpiar_superficie(boton_respuesta_cuatro,"textura_respuesta.jpg",ANCHO_BOTON,ALTO_BOTON)
    
    return pregunta_actual

def crear_botones_menu() -> list:
    lista_botones = []
    pos_y = 280  # Empezar más abajo para dejar espacio al logo
    pos_x = (ANCHO-ANCHO_BOTON)//2
    for i in range(4):
        boton = crear_elemento_juego("textura_menu.jpg",ANCHO_BOTON,ALTO_BOTON,pos_x,pos_y)
        pos_y += 80
        lista_botones.append(boton)
    return lista_botones

def crear_comodines() -> list:
    """Crea los botones de comodines con fondo blanco"""
    comodines = []
    
    # Posiciones: 2 a la izquierda, 2 a la derecha de la pregunta
    pos_y_pregunta = 80
    pos_x_pregunta = (ANCHO-ANCHO_PREGUNTA)//2
    
    # Comodines izquierdos
    comodin_bomba = crear_elemento_juego("textura_respuesta.jpg", TAMAÑO_COMODIN[0], TAMAÑO_COMODIN[1], 
                                        pos_x_pregunta - 80, pos_y_pregunta + 20)
    comodin_x2 = crear_elemento_juego("textura_respuesta.jpg", TAMAÑO_COMODIN[0], TAMAÑO_COMODIN[1], 
                                     pos_x_pregunta - 80, pos_y_pregunta + 100)
    
    # Comodines derechos
    comodin_doble_chance = crear_elemento_juego("textura_respuesta.jpg", TAMAÑO_COMODIN[0], TAMAÑO_COMODIN[1], 
                                               pos_x_pregunta + ANCHO_PREGUNTA + 20, pos_y_pregunta + 20)
    comodin_pasar = crear_elemento_juego("textura_respuesta.jpg", TAMAÑO_COMODIN[0], TAMAÑO_COMODIN[1], 
                                        pos_x_pregunta + ANCHO_PREGUNTA + 20, pos_y_pregunta + 100)
    
    comodines = [comodin_bomba, comodin_x2, comodin_doble_chance, comodin_pasar]
    return comodines

def verificar_click_comodin(comodines: list, pos_click: tuple) -> int:
    """Retorna el índice del comodín clickeado (0-3) o -1 si no se clickeó ninguno"""
    for i in range(len(comodines)):
        if comodines[i]["rectangulo"].collidepoint(pos_click):
            return i
    return -1

def aplicar_comodin_bomba(pregunta_actual: dict, botones_respuesta: list) -> dict:
    """Elimina dos respuestas incorrectas, dejando solo la correcta y una incorrecta"""
    respuesta_correcta = pregunta_actual["respuesta_correcta"]
    
    # Encontrar respuestas incorrectas
    respuestas_incorrectas = []
    for i in range(1, 5):
        if i != respuesta_correcta:
            respuestas_incorrectas.append(i)
    
    # Eliminar dos respuestas incorrectas aleatoriamente
    import random
    respuestas_a_eliminar = random.sample(respuestas_incorrectas, 2)
    
    # Ocultar botones eliminados
    for i in range(len(botones_respuesta)):
        if i + 1 in respuestas_a_eliminar:
            botones_respuesta[i]["activo"] = False
    
    return pregunta_actual

def aplicar_comodin_x2(datos_juego: dict) -> None:
    """Activa el multiplicador x2 para la siguiente respuesta"""
    datos_juego["multiplicador_x2"] = True

def aplicar_comodin_doble_chance(datos_juego: dict) -> None:
    """Activa la doble chance para la siguiente respuesta incorrecta"""
    datos_juego["doble_chance"] = True

def aplicar_comodin_pasar(datos_juego: dict) -> None:
    """Marca el comodín pasar como usado"""
    datos_juego["pasar_usado"] = True
